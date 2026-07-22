# Spazio Sicuro — Full App (Landing istituzionale)

App completa React + FastAPI + MongoDB per la landing istituzionale rivolta a scuole, genitori, educatori.

## Struttura
```
spazio-sicuro-full-app/
├── frontend/       # React 19 + Tailwind + framer-motion
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env.example
├── backend/        # FastAPI + Motor (MongoDB async)
│   ├── server.py
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## Prerequisiti
- Node.js 18+ e yarn
- Python 3.9+
- MongoDB (locale o su MongoDB Atlas gratis)

## Setup locale — Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate     # su Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configura .env (copia da .env.example)
cp .env.example .env
# Modifica MONGO_URL se hai un MongoDB diverso da localhost

# Avvia
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

## Setup locale — Frontend
```bash
cd frontend
yarn install

# Configura .env
cp .env.example .env
# In .env metti REACT_APP_BACKEND_URL=http://localhost:8001

yarn start
# apre http://localhost:3000
```

## Deployment gratuito consigliato
### Opzione A: Netlify (frontend) + Railway (backend + MongoDB)
1. **Frontend su Netlify**:
   - Push del repo su GitHub
   - Su Netlify: "New site from Git" → seleziona repo → build dir `frontend`, build cmd `yarn build`, publish dir `frontend/build`
   - Env: `REACT_APP_BACKEND_URL` = URL del backend Railway
2. **Backend su Railway** (5$ crediti/mese gratis):
   - New Project → Deploy from GitHub → seleziona cartella `backend`
   - Aggiungi MongoDB plugin (o usa MongoDB Atlas free)
   - Env: `MONGO_URL`, `DB_NAME=spazio_sicuro`, `CORS_ORIGINS=https://tuosito.netlify.app`

### Opzione B: Vercel (frontend) + Render (backend)
Simile alla A, entrambi hanno free tier.

## Personalizzazione
- **Testo/contenuti**: `frontend/src/App.js` — tutto in italiano, facilmente editabile
- **Colori**: `frontend/src/index.css` (variabili `--primary`, `--bg`, ecc.)
- **Link al tool esistente**: variabile `TOOL_URL` in cima a `App.js`
- **Numeri emergenza**: modificabili sia in `App.js` (sezione Emergency e HelpDialog)

## API disponibili
- `GET  /api/health` — health check
- `POST /api/contact` — riceve form contatti scuole/collaborazioni
  - Body: `{name, email, organization?, role?, message}`
  - Salvato in MongoDB collection `contacts`

## Personalizzazioni consigliate
1. **Email notifica**: integra SendGrid o Resend in `backend/server.py` nell'endpoint `/api/contact` per ricevere email quando arriva un messaggio
2. **Analytics privacy-friendly**: aggiungi Plausible o Umami (no cookie banner necessario)
3. **Privacy policy**: aggiungi una route `/privacy-policy` con testo Iubenda free tier
