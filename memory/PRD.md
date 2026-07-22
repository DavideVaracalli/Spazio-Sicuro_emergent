# PRD — Spazio Sicuro

## Original problem statement
Miglioramento e diffusione pubblica di "Spazio Sicuro" — web app anonima per adolescenti che vivono momenti emotivi difficili (stress, tristezza, rabbia). L'utente originale ha creato una prima versione HTML su Netlify (sweet-babka-6fe1eb.netlify.app) e chiede: (1) miglioramenti al codice HTML esistente, (2) full app + landing istituzionale per scuole/genitori, (3) kit di presentazione PDF.

## Deliverables consegnati
### 1. HTML migliorato (drop-in per Netlify)
- File: `/app/spazio-sicuro-improved.html` (30 KB) + `/app/sw.js`
- Fix: mobile touch (pointerdown/up), 100dvh, PWA installabile, safety words regex più precise, fallback SR per iOS
- Nuove modalità: **Respira** (4-4-4-4 guidato), **Mood check-in** (5 emoji, non salvato)
- Numeri emergenza: pulsante FAB persistente + messaggio critico con numeri cliccabili
- Accessibilità: aria-live, aria-modal, focus visible, Esc chiude, prefers-reduced-motion
- Aptico: vibrazione su tap importanti

### 2. Full app — Landing istituzionale
- **Frontend** (React + Tailwind + framer-motion + lucide-react + Playfair Display / Manrope)
- **Backend** (FastAPI): endpoint `/api/contact` per collaborazioni scuole (salvato in MongoDB collection `contacts`)
- Sezioni: Hero, Manifesto, Come funziona, Per Genitori, Per Scuole, Privacy, Numeri di aiuto, FAQ, Contatti, Footer
- Design: "Nighttime Introspection" — dark, editorial, non-clinical
- Floating "Ho bisogno d'aiuto" con dialog numeri emergenza
- URL: https://youth-diary-1.preview.emergentagent.com

### 3. PDF di presentazione
- File: `/app/spazio-sicuro-presentazione.pdf` (9 KB, 4 pagine A4)
- Pagine: Cover, Problema/Soluzione, Privacy/Emergenza, Adozione/Contatti
- In italiano, dark theme coerente, generato via reportlab (`scripts/generate_pdf.py`)

## User personas
- **Adolescenti (13-18)** — utenti finali del tool (accedono da mobile, no registrazione)
- **Genitori** — visitano la landing per capire cosa fanno i figli
- **Docenti / Scuole** — valutano adozione, compilano form contatti
- **Professionisti** (psicologi, associazioni) — potenziali partner istituzionali

## Core requirements
- Anonimato assoluto — mai salvare contenuti degli utenti
- Non sostituire supporto professionale — sempre suggerire risorse
- Numeri emergenza sempre accessibili
- Landing credibile per istituzioni
- Zero cost di ingresso (link condivisibile)

## Tech stack
- Frontend: React 19, Tailwind, framer-motion, lucide-react, Playfair Display + Manrope
- Backend: FastAPI + Motor + MongoDB (solo per contatti scuole)
- HTML standalone: single-file per Netlify

## Backlog / Next actions
### P0
- [ ] User carica `spazio-sicuro-improved.html` (rinominato `index.html`) + `sw.js` su Netlify
- [ ] User acquista dominio (`spaziosicuro.it` / `.org`) — consigliato Namecheap/Register.it
- [ ] User contatta 1 psicologo per validazione clinica messaggi

### P1
- [ ] Deploy landing sul dominio (Netlify/Vercel — supportano React SPA gratis)
- [ ] Integrazione email (SendGrid/Resend) per notifiche form contatti
- [ ] Analytics rispettoso privacy (Plausible/Umami)
- [ ] Privacy policy + Termini d'uso (Iubenda free tier)

### P2
- [ ] Assistente AI empatico opzionale (Claude Sonnet 4.5 via Emergent Universal Key)
- [ ] Sezione risorse/blog per docenti
- [ ] Traduzione EN per estensione europea
- [ ] Partnership Telefono Azzurro / Save the Children Italia
- [ ] Candidatura bandi Fondazione Cariplo / Compagnia di San Paolo

## Business enhancement suggerita
Aggiungere un contatore pubblico anonimo (Plausible-based) "**Nel 2026, Spazio Sicuro ha accolto X respiri**" nella landing → dà prova sociale ai docenti/genitori senza tracciare gli utenti individualmente. Aumenta la credibilità istituzionale e crea un piccolo effetto "movimento".

## Aggiornamento sessione 2 (2026-01)
- Aggiunta sezione **Download** nella landing con 3 card scaricabili
- Backend: nuovo endpoint `/api/downloads/{basic|full-app|pdf}` con FileResponse
- File pubblicati in `/app/downloads/`:
  - `spazio-sicuro-basic.zip` (11 KB) — index.html + sw.js + README
  - `spazio-sicuro-full-app.zip` (68 KB) — progetto React + FastAPI, esclusi node_modules
  - `spazio-sicuro-presentazione.pdf` (9 KB)
- Link diretti (usare dominio proprio quando disponibile):
  - {BACKEND_URL}/api/downloads/basic
  - {BACKEND_URL}/api/downloads/full-app
  - {BACKEND_URL}/api/downloads/pdf
- Aggiunto "Download" al nav
