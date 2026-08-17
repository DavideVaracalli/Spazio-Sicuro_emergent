import os
import uuid
import asyncio
import logging
from pathlib import Path
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Optional

import resend
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# ---------- Setup ----------
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

DOWNLOADS_DIR = ROOT_DIR.parent / "downloads"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Resend
RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev')
OWNER_EMAIL = os.environ.get('OWNER_EMAIL')
STATS_ADMIN_KEY = os.environ.get('STATS_ADMIN_KEY')
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY


# ---------- Lifespan ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Spazio Sicuro API — startup")
    yield
    logger.info("Spazio Sicuro API — shutdown")
    client.close()


# ---------- Rate limit ----------
def real_client_ip(request: Request) -> str:
    """
    Estrae l'IP reale del client, tenendo conto di proxy/CDN.
    In produzione (Kubernetes ingress, Cloudflare) request.client.host è l'IP
    del proxy, quindi tutti gli utenti condividerebbero lo stesso bucket.
    X-Forwarded-For contiene la catena reale: prendiamo il primo (client vero).
    """
    xff = request.headers.get('x-forwarded-for')
    if xff:
        first = xff.split(',')[0].strip()
        if first:
            return first
    return get_remote_address(request)


# Storage in-memory: si azzera ad ogni restart del backend.
# Per multi-replica produzione, valutare Redis (storage_uri="redis://...").
limiter = Limiter(key_func=real_client_ip)


async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Ritorna 'detail' invece del default 'error' → il frontend lo mostra all'utente."""
    return JSONResponse(
        status_code=429,
        content={"detail": "Hai inviato troppi messaggi. Riprova tra qualche minuto."}
    )


app = FastAPI(title="Spazio Sicuro API", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

api_router = APIRouter(prefix="/api")


# ---------- Models ----------
class ContactCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    organization: Optional[str] = Field(default=None, max_length=160)
    role: Optional[str] = Field(default=None, max_length=80)
    message: str = Field(min_length=5, max_length=4000)
    # Honeypot: campo nascosto che gli umani non compilano mai.
    # Se arriva pieno = bot → scarto silenziosamente.
    website: Optional[str] = Field(default=None, max_length=200)


class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    organization: Optional[str] = None
    role: Optional[str] = None
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContactResponse(BaseModel):
    id: str
    created_at: str


# ---------- Helpers ----------
async def send_notification_email(contact: Contact) -> None:
    """Invia email al proprietario quando arriva un contatto. Non blocca la request."""
    if not RESEND_API_KEY or not OWNER_EMAIL:
        logger.info("Email notification skipped (RESEND_API_KEY or OWNER_EMAIL missing)")
        return

    body = f"""
    <div style="font-family: -apple-system, sans-serif; max-width: 600px; padding: 24px; background: #f8f8fa; color: #1a1a2a;">
      <h2 style="margin-top:0; color:#1a1a2a;">Nuovo contatto da Spazio Sicuro</h2>
      <table style="width:100%; border-collapse: collapse; margin-top: 16px;">
        <tr><td style="padding:8px 0; color:#666; width:140px;">Nome</td><td style="padding:8px 0;"><strong>{contact.name}</strong></td></tr>
        <tr><td style="padding:8px 0; color:#666;">Email</td><td style="padding:8px 0;"><a href="mailto:{contact.email}">{contact.email}</a></td></tr>
        <tr><td style="padding:8px 0; color:#666;">Organizzazione</td><td style="padding:8px 0;">{contact.organization or "—"}</td></tr>
        <tr><td style="padding:8px 0; color:#666;">Ruolo</td><td style="padding:8px 0;">{contact.role or "—"}</td></tr>
      </table>
      <hr style="border:none; border-top:1px solid #ddd; margin: 24px 0;">
      <p style="color:#666; margin-bottom:8px;">Messaggio</p>
      <div style="background:#fff; padding:16px; border-radius:8px; border:1px solid #eee; white-space:pre-wrap;">{contact.message}</div>
      <p style="color:#999; font-size:12px; margin-top:24px;">Ricevuto il {contact.created_at.strftime('%d/%m/%Y alle %H:%M')} UTC</p>
    </div>
    """
    params = {
        "from": SENDER_EMAIL,
        "to": [OWNER_EMAIL],
        "reply_to": contact.email,
        "subject": f"Spazio Sicuro — nuovo contatto da {contact.name}",
        "html": body,
    }
    try:
        await asyncio.to_thread(resend.Emails.send, params)
        logger.info(f"Notification email sent for contact {contact.id}")
    except Exception as e:
        logger.error(f"Failed to send notification email: {e}")


async def send_confirmation_email(contact: Contact) -> None:
    """Email di conferma gentile a chi compila il form. Best-effort."""
    if not RESEND_API_KEY:
        return
    body = f"""
    <div style="font-family: -apple-system, sans-serif; max-width: 560px; padding: 24px; background: #f8f8fa; color: #1a1a2a;">
      <h2 style="margin-top:0;">Grazie, {contact.name}.</h2>
      <p style="line-height:1.6; color:#444;">
        Abbiamo ricevuto il tuo messaggio su <strong>Spazio Sicuro</strong> e ti risponderemo al più presto.
      </p>
      <p style="line-height:1.6; color:#444;">
        Spazio Sicuro è un progetto pensato per dare ad adolescenti e giovani un luogo anonimo
        dove esprimere le proprie emozioni, senza registrazione e senza salvare alcun dato.
      </p>
      <p style="line-height:1.6; color:#444;">A presto,<br>Davide — Spazio Sicuro</p>
      <hr style="border:none; border-top:1px solid #ddd; margin: 24px 0;">
      <p style="color:#999; font-size:12px;">Questa è una risposta automatica alla tua richiesta di contatto.</p>
    </div>
    """
    params = {
        "from": SENDER_EMAIL,
        "to": [contact.email],
        "subject": "Abbiamo ricevuto il tuo messaggio — Spazio Sicuro",
        "html": body,
    }
    try:
        await asyncio.to_thread(resend.Emails.send, params)
        logger.info(f"Confirmation email sent to {contact.email}")
    except Exception as e:
        logger.warning(f"Confirmation email failed (Resend free tier invia solo all'email del proprietario finché il dominio non è verificato): {e}")


def today_key() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%d')


# ---------- Routes ----------
@api_router.get("/")
async def root():
    return {"service": "Spazio Sicuro", "status": "ok"}


@api_router.get("/health")
async def health():
    return {"status": "healthy", "time": datetime.now(timezone.utc).isoformat()}


@api_router.post("/contact", response_model=ContactResponse)
@limiter.limit("5/hour")
async def create_contact(request: Request, payload: ContactCreate):
    """Riceve richieste di collaborazione da scuole, associazioni, professionisti."""
    # Honeypot check: se il campo nascosto 'website' è compilato → bot
    if payload.website:
        logger.warning(f"Honeypot triggered — contact rejected (IP {real_client_ip(request)})")
        # Rispondiamo con successo finto per non insospettire il bot
        return ContactResponse(
            id=str(uuid.uuid4()),
            created_at=datetime.now(timezone.utc).isoformat()
        )

    data = payload.model_dump(exclude={"website"})
    contact = Contact(**data)
    doc = contact.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    try:
        await db.contacts.insert_one(doc)
    except Exception as e:
        logger.error(f"Error saving contact: {e}")
        raise HTTPException(status_code=500, detail="Errore nel salvataggio")

    # Email best-effort, non bloccano la risposta
    asyncio.create_task(send_notification_email(contact))
    asyncio.create_task(send_confirmation_email(contact))

    return ContactResponse(id=contact.id, created_at=doc['created_at'])


# ---------- Statistiche anonime (nessun dato personale, solo conteggi aggregati) ----------
@api_router.post("/events/{event_type}", status_code=204)
@limiter.limit("15/minute")
async def track_event(request: Request, event_type: str):
    """Incrementa un contatore giornaliero aggregato. Nessun IP o identificativo salvato."""
    if event_type not in ("breath", "visit"):
        raise HTTPException(status_code=404, detail="Evento non valido")
    field = "breaths" if event_type == "breath" else "visits"
    await db.daily_stats.update_one(
        {"_id": today_key()}, {"$inc": {field: 1}}, upsert=True
    )
    return Response(status_code=204)


@api_router.get("/stats/public")
async def public_stats():
    """Contatore pubblico per la landing: respiri di oggi e totali."""
    today = await db.daily_stats.find_one({"_id": today_key()})
    agg = await db.daily_stats.aggregate([
        {"$group": {"_id": None, "breaths": {"$sum": "$breaths"}}}
    ]).to_list(1)
    return {
        "breaths_today": (today or {}).get("breaths", 0),
        "breaths_total": agg[0]["breaths"] if agg else 0,
    }


@api_router.get("/stats/admin")
async def admin_stats(key: str = ""):
    """Analytics privacy-friendly per il proprietario: aggregati giornalieri, zero cookie."""
    if not STATS_ADMIN_KEY or key != STATS_ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Chiave non valida")
    cursor = db.daily_stats.find().sort("_id", -1).limit(60)
    days = [
        {"date": d["_id"], "visits": d.get("visits", 0), "breaths": d.get("breaths", 0)}
        async for d in cursor
    ]
    agg = await db.daily_stats.aggregate([
        {"$group": {"_id": None, "visits": {"$sum": "$visits"}, "breaths": {"$sum": "$breaths"}}}
    ]).to_list(1)
    totals = {"visits": agg[0]["visits"], "breaths": agg[0]["breaths"]} if agg else {"visits": 0, "breaths": 0}
    contacts_count = await db.contacts.count_documents({})
    return {"totals": totals, "contacts_received": contacts_count, "last_days": days}


# ---------- Downloads (endpoint privati, non linkati pubblicamente) ----------
DOWNLOAD_FILES = {
    "basic":       ("spazio-sicuro-basic.zip",              "application/zip"),
    "full-app":    ("spazio-sicuro-full-app.zip",           "application/zip"),
    "pdf":         ("spazio-sicuro-presentazione.pdf",      "application/pdf"),
    "pdf-full":    ("spazio-sicuro-presentazione-full.pdf", "application/pdf"),
}


@api_router.get("/downloads/{key}")
async def download_file(key: str):
    if key not in DOWNLOAD_FILES:
        raise HTTPException(status_code=404, detail="File non trovato")
    filename, media_type = DOWNLOAD_FILES[key]
    path = DOWNLOADS_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File non ancora disponibile")
    return FileResponse(path=str(path), media_type=media_type, filename=filename)


app.include_router(api_router)

# ---------- CORS ----------
cors_origins_raw = os.environ.get('CORS_ORIGINS', '*')
cors_origins = [o.strip() for o in cors_origins_raw.split(',') if o.strip()]
# Se ci sono origini specifiche → allow_credentials=True è sicuro.
# Se resta '*' → disabilita credentials (browser rifiutano wildcard + credentials).
allow_credentials = cors_origins != ['*']
app.add_middleware(
    CORSMiddleware,
    allow_credentials=allow_credentials,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
