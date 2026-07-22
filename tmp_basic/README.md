# Spazio Sicuro — Versione Base (single-file HTML)

## Come pubblicarla su Netlify (5 minuti, gratis)

### Metodo 1: drag & drop (più semplice)
1. Vai su https://app.netlify.com/drop
2. Trascina **l'intera cartella** (contenente `index.html` + `sw.js`) nel riquadro
3. Netlify ti darà subito un URL tipo `nome-random.netlify.app`
4. Da "Site settings" → "Change site name" puoi rinominarlo (es. `spazio-sicuro`)

### Metodo 2: HTML editor (se usi già Netlify HTML editor)
1. Apri `index.html` con un editor di testo (Blocco Note, VS Code, TextEdit)
2. **Seleziona tutto** (Ctrl+A / Cmd+A) e **copia** (Ctrl+C / Cmd+C)
3. Incolla nell'HTML editor della piattaforma
4. **IMPORTANTE**: se l'editor non supporta più file, il service worker (`sw.js`) non funzionerà — l'app funziona lo stesso, semplicemente senza modalità offline. Puoi ignorare `sw.js`.

## File inclusi
- `index.html` → il file principale (rinominalo così su Netlify)
- `sw.js` → service worker per PWA offline (opzionale)

## Cosa fare dopo
1. Prova il link su desktop e mobile
2. Su mobile, aggiungi alla schermata home (diventa PWA installabile)
3. Compra un dominio (~10€/anno) e collegalo da Netlify → Domain settings
