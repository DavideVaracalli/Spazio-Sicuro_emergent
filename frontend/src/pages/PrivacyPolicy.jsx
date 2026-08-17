import { Link } from "react-router-dom";
import { ArrowLeft, Shield } from "lucide-react";

const LAST_UPDATED = "Gennaio 2026";

function PrivacyPolicy() {
  return (
    <div className="min-h-screen grain">
      <header className="nav-shell">
        <div className="section-container flex items-center justify-between py-5">
          <Link to="/" className="font-display text-xl md:text-2xl tracking-tight" data-testid="privacy-logo">
            Spazio Sicuro
          </Link>
          <Link to="/" className="inline-flex items-center gap-2 text-sm text-[color:var(--text-secondary)] hover:text-[color:var(--text)] transition-colors" data-testid="back-home">
            <ArrowLeft size={16}/> Torna alla home
          </Link>
        </div>
      </header>

      <main className="section-container py-20 md:py-32 max-w-3xl">
        <div className="bento-icon mb-8"><Shield size={22}/></div>
        <p className="text-sm uppercase tracking-[0.2em] text-[color:var(--primary)] mb-4">Informativa privacy</p>
        <h1 className="font-display text-4xl md:text-6xl leading-tight mb-6" data-testid="privacy-title">
          Privacy Policy
        </h1>
        <p className="text-sm text-[color:var(--text-muted)] mb-12">Ultimo aggiornamento: {LAST_UPDATED}</p>

        <div className="space-y-10 text-[color:var(--text-secondary)] leading-relaxed">

          <section>
            <h2 className="font-display text-2xl text-[color:var(--text)] mb-3">1. In sintesi</h2>
            <p>
              Spazio Sicuro è progettato secondo il principio della <em>privacy by design</em>.
              Non usiamo cookie di tracciamento, non facciamo profilazione, non condividiamo dati con terze parti.
              Ciò che scrivi, disegni o dici nell'app rimane esclusivamente sul tuo dispositivo, nella sessione del browser,
              e sparisce quando la chiudi.
            </p>
          </section>

          <section>
            <h2 className="font-display text-2xl text-[color:var(--text)] mb-3">2. Titolare del trattamento</h2>
            <p>
              Il titolare del trattamento è il responsabile del progetto Spazio Sicuro,
              progetto sociale indipendente senza scopo di lucro.
              Per qualsiasi richiesta relativa al trattamento dei dati puoi scrivere tramite il modulo di contatto sulla home.
            </p>
          </section>

          <section>
            <h2 className="font-display text-2xl text-[color:var(--text)] mb-3">3. Quali dati raccogliamo</h2>
            <p className="mb-4">Distinguiamo tra il <strong>tool di sfogo</strong> e la <strong>landing informativa</strong>.</p>

            <h3 className="font-display text-lg text-[color:var(--text)] mt-6 mb-2">3.1 Tool di sfogo (app anonima)</h3>
            <p><strong className="text-[color:var(--text)]">Nulla.</strong> Testi, disegni, registrazioni vocali:
              tutto vive esclusivamente nel tuo browser durante la sessione. Nessun dato viene inviato ai nostri server,
              nessun cookie viene installato, nessuna analytics viene raccolta.
            </p>

            <h3 className="font-display text-lg text-[color:var(--text)] mt-6 mb-2">3.2 Landing (questa pagina)</h3>
            <p>Sulla landing informativa non usiamo cookie di profilazione. Raccogliamo dati solo se:</p>
            <ul className="list-disc list-inside space-y-2 mt-3 pl-2">
              <li>compili volontariamente il <strong>modulo di contatto</strong> (vedi sez. 4)</li>
              <li>il tuo browser invia informazioni tecniche standard (IP, user-agent) al nostro hosting — non salvate a fini di profilazione, ma conservate temporaneamente nei log del server per motivi di sicurezza (max 30 giorni)</li>
            </ul>
          </section>

          <section>
            <h2 className="font-display text-2xl text-[color:var(--text)] mb-3">4. Modulo di contatto</h2>
            <p>Se compili il form di contatto, raccogliamo:</p>
            <ul className="list-disc list-inside space-y-2 mt-3 pl-2">
              <li><strong>Nome</strong>, <strong>email</strong>, <strong>messaggio</strong> (obbligatori)</li>
              <li><strong>Scuola/Associazione</strong>, <strong>ruolo</strong> (facoltativi)</li>
            </ul>
            <p className="mt-4">
              <strong className="text-[color:var(--text)]">Finalità:</strong> rispondere alla tua richiesta di contatto e valutare collaborazioni.
            </p>
            <p className="mt-2">
              <strong className="text-[color:var(--text)]">Base giuridica:</strong> tuo consenso (art. 6.1.a GDPR) espresso con l'invio volontario del modulo.
            </p>
            <p className="mt-2">
              <strong className="text-[color:var(--text)]">Conservazione:</strong> fino a 24 mesi dall'ultima interazione, poi cancellazione.
            </p>
            <p className="mt-2">
              <strong className="text-[color:var(--text)]">Destinatari:</strong> nessuno. I dati non vengono condivisi con terzi. Sono ospitati su MongoDB
              e la notifica arriva via email al titolare del progetto.
            </p>
          </section>

          <section>
            <h2 className="font-display text-2xl text-[color:var(--text)] mb-3">5. I tuoi diritti (GDPR)</h2>
            <p>In qualsiasi momento hai diritto a:</p>
            <ul className="list-disc list-inside space-y-2 mt-3 pl-2">
              <li>accedere ai tuoi dati</li>
              <li>chiederne rettifica o cancellazione</li>
              <li>revocare il consenso</li>
              <li>opporti al trattamento</li>
              <li>presentare reclamo al Garante Privacy (<a className="text-[color:var(--primary)] underline" href="https://www.garanteprivacy.it" target="_blank" rel="noopener noreferrer">garanteprivacy.it</a>)</li>
            </ul>
            <p className="mt-4">Per esercitare questi diritti scrivici tramite il modulo di contatto sulla home.</p>
          </section>

          <section>
            <h2 className="font-display text-2xl text-[color:var(--text)] mb-3">6. Minori</h2>
            <p>
              Spazio Sicuro è pensato anche per adolescenti. Il tool anonimo può essere usato senza limiti d'età,
              poiché non raccoglie alcun dato. Per il modulo di contatto ci aspettiamo che sia compilato da persone maggiorenni
              (docenti, genitori, educatori); minori interessati sono invitati a chiedere aiuto a un adulto di riferimento.
            </p>
          </section>

          <section>
            <h2 className="font-display text-2xl text-[color:var(--text)] mb-3">7. Cookie</h2>
            <p>
              Non installiamo cookie di profilazione né di tracciamento. Utilizziamo solo eventuali cookie tecnici strettamente
              necessari al funzionamento del sito (esenti da consenso ai sensi delle linee guida del Garante).
            </p>
          </section>

          <section>
            <h2 className="font-display text-2xl text-[color:var(--text)] mb-3">8. Modifiche</h2>
            <p>
              Questa informativa può essere aggiornata. In caso di modifiche sostanziali sarà evidenziato in questa pagina.
              La data di ultimo aggiornamento è indicata in cima.
            </p>
          </section>

          <section className="pt-8 border-t border-[color:var(--border)]">
            <p className="text-sm text-[color:var(--text-muted)]">
              Questo documento non sostituisce una consulenza legale personalizzata.
              Le informazioni sono fornite in buona fede per un progetto sociale no-profit.
            </p>
          </section>

        </div>
      </main>

      <footer className="pt-14 pb-14 border-t border-[color:var(--border)]">
        <div className="section-container text-sm text-[color:var(--text-muted)]">
          <Link to="/" className="hover:text-[color:var(--text)] transition-colors">← Spazio Sicuro</Link>
        </div>
      </footer>
    </div>
  );
}

export default PrivacyPolicy;
