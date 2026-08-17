# PRD — Spazio Sicuro

## Original problem statement
Miglioramento e diffusione pubblica di "Spazio Sicuro" — web app anonima per adolescenti che vivono momenti emotivi difficili. L'utente ha creato una prima versione HTML su Netlify e chiede: (1) miglioramenti al codice HTML, (2) full app + landing istituzionale per scuole/genitori, (3) kit PDF, (4) preparazione a deploy in produzione.

## Deliverables consegnati
### 1. HTML migliorato (drop-in per Netlify)
`/app/spazio-sicuro-improved.html` (30 KB) + `/app/sw.js`. Fix mobile touch, PWA, safety words regex precise, respirazione guidata, mood check-in, help FAB persistente.

### 2. Full app landing (React + FastAPI + MongoDB) — PRODUCTION-READY
- **Frontend**: React 19 + Tailwind + framer-motion + lucide-react + react-router-dom
- **Backend**: FastAPI + Motor + lifespan + slowapi (rate limit XFF-aware) + Resend (email)
- **Sezioni landing**: Hero, Manifesto, Come funziona, Genitori, Scuole, Privacy, Numeri d'aiuto, FAQ, Contatti + Footer con link a /privacy
- **Pagina /privacy**: Privacy Policy GDPR italiana completa (10 sezioni)
- **SEO**: meta tag OG/Twitter, favicon SVG, /og-image.svg 1200x630, robots.txt, sitemap.xml, _redirects Netlify
- **Sicurezza**: honeypot antibot su contact form, rate limit 5/hour per IP reale (X-Forwarded-For aware), CORS env-driven
- **Notifica email**: quando arriva contatto, Resend manda email formattata al proprietario (skip silenzioso se chiavi mancanti)

### 3. PDF di presentazione (`/app/downloads/spazio-sicuro-presentazione.pdf`)
4 pagine A4 (90 KB) con screenshot reali del tool coerenti con la versione base. Endpoint privati /api/downloads mantenuti per uso proprietario.

## Environment variables da configurare per production deploy

### backend/.env
```
MONGO_URL=<mongodb-atlas-connection-string>
DB_NAME=spazio_sicuro
CORS_ORIGINS=https://spaziosicuro.it,https://www.spaziosicuro.it
RESEND_API_KEY=re_xxxxxxxxxxxx  # da resend.com/api-keys (free tier 100 email/day)
SENDER_EMAIL=noreply@spaziosicuro.it  # o "onboarding@resend.dev" prima della verifica del dominio
OWNER_EMAIL=tua@email.it
```

### frontend/.env
```
REACT_APP_BACKEND_URL=https://api.spaziosicuro.it
REACT_APP_TOOL_URL=https://spaziosicuro.it (o quello Netlify attuale)
```

## Deploy — Passi consigliati
1. Compra dominio (Register.it / Namecheap) ~10€/anno — es. `spaziosicuro.it`
2. MongoDB Atlas free tier (M0) → prendi la connection string
3. Backend su Railway/Render → env variables sopra
4. Frontend build (`yarn build`) → deploy su Netlify (drag&drop `build/` folder o via Git)
5. Configura DNS: apex `@` → Netlify, `api` → Railway
6. Resend: verifica il dominio per usare `noreply@spaziosicuro.it`
7. Google Search Console: verifica sito, submit sitemap.xml
8. Testing produzione: submit form → deve arrivare email

## Testing status
- **Iteration 1**: 100% pass — 16/16 pytest backend, 100% frontend E2E
- **Iteration 2**: 100% pass ma 1 CRITICAL (rate limit shared bucket) → risolto
- **Iteration 3**: 100% pass — 33/33 pytest — tutti fix verificati, 0 critical issue

## Backlog / P1-P2 (dopo deploy iniziale)
- Analytics privacy-friendly (Plausible/Umami) — placeholder già in index.html
- Traduzione EN per estensione europea
- Assistente AI empatico anonimo (Claude Sonnet 4.5 via Emergent LLM Key)
- Partnership Telefono Azzurro / Save the Children Italia
- Candidatura bandi Fondazione Cariplo / Compagnia di San Paolo (5K-30K€ tipici)
- 5x1000 se costituisci APS
- URL assoluti (canonical, sitemap, robots) quando dominio disponibile
- Retry-After header su 429
- BackgroundTasks per email Resend (invece di asyncio.create_task)

## Aggiornamento 17/06/2026 (fork) — Email Resend ATTIVATE
- RESEND_API_KEY configurata in backend/.env (fornita dall'utente, account registrato con davide.varacalli.spaziosicuro@gmail.com)
- OWNER_EMAIL = davide.varacalli.spaziosicuro@gmail.com
- Test reale eseguito: email inviata con successo (log: "Notification email sent")
- Verifica completa post-fork: health OK, form contatti OK (salvataggio DB), honeypot OK, download endpoints OK (basic/full-app/pdf 200), landing page OK
- Nota free tier Resend: le email arrivano SOLO all'indirizzo di registrazione finché non si verifica un dominio; mittente = onboarding@resend.dev (controllare spam)
