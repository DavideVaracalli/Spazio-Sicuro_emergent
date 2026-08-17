from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
import uuid
from datetime import datetime, timezone

DOWNLOADS_DIR = Path(__file__).parent.parent / "downloads"

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI(title="Spazio Sicuro API")
api_router = APIRouter(prefix="/api")


# ---------- Models ----------
class ContactCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    organization: Optional[str] = Field(default=None, max_length=160)
    role: Optional[str] = Field(default=None, max_length=80)
    message: str = Field(min_length=5, max_length=4000)


class Contact(ContactCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContactResponse(BaseModel):
    id: str
    created_at: str


# ---------- Routes ----------
@api_router.get("/")
async def root():
    return {"service": "Spazio Sicuro", "status": "ok"}


@api_router.get("/health")
async def health():
    return {"status": "healthy", "time": datetime.now(timezone.utc).isoformat()}


@api_router.post("/contact", response_model=ContactResponse)
async def create_contact(payload: ContactCreate):
    """Riceve richieste di collaborazione da scuole, associazioni, professionisti."""
    contact = Contact(**payload.model_dump())
    doc = contact.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    try:
        await db.contacts.insert_one(doc)
    except Exception as e:
        logger.error(f"Error saving contact: {e}")
        raise HTTPException(status_code=500, detail="Errore nel salvataggio")
    return ContactResponse(id=contact.id, created_at=doc['created_at'])


# ---------- Downloads ----------
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
    return FileResponse(
        path=str(path),
        media_type=media_type,
        filename=filename,
    )


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
