import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  PenLine, Palette, Mic, Wind,
  Shield, Heart, School, Phone,
  LifeBuoy, Plus, Minus, ArrowRight, Send, Check, X, Menu
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Link al tool esistente — cambiabile da .env quando avrai il dominio del tool
const TOOL_URL = process.env.REACT_APP_TOOL_URL || "https://sweet-babka-6fe1eb.netlify.app/";

// Fade-in animation on scroll
const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  show:   { opacity: 1, y: 0, transition: { duration: 1, ease: [0.22, 1, 0.36, 1] } }
};

const NAV_LINKS = [
  { href: "#manifesto",  label: "Manifesto" },
  { href: "#come",       label: "Come funziona" },
  { href: "#genitori",   label: "Genitori" },
  { href: "#scuole",     label: "Scuole" },
  { href: "#privacy",    label: "Privacy" },
  { href: "#faq",        label: "FAQ" },
  { href: "#contatti",   label: "Contatti" }
];

const EMERGENCY_NUMBERS = [
  { n: "112",           l: "Emergenza",            s: "Se sei in pericolo immediato" },
  { n: "19696",         l: "Telefono Azzurro",     s: "Per minori · 24 ore su 24 · gratuito" },
  { n: "02 2327 2327",  l: "Telefono Amico",       s: "Ascolto anonimo · 10:00–24:00" },
  { n: "800 86 10 61",  l: "Prevenzione Suicidio", s: "Samaritans Onlus" }
];

// ---------- NAV ----------
function NavDesktop() {
  return (
    <nav className="hidden lg:flex items-center gap-8">
      {NAV_LINKS.map(l => (
        <a key={l.href} href={l.href}
           className="text-sm text-[color:var(--text-secondary)] hover:text-[color:var(--text)] transition-colors"
           data-testid={`nav-${l.label.toLowerCase().replace(/\s/g,'-')}`}>
          {l.label}
        </a>
      ))}
      <a href={TOOL_URL} target="_blank" rel="noopener noreferrer"
         className="btn-primary text-sm" data-testid="nav-cta">
        Entra <ArrowRight size={16} />
      </a>
    </nav>
  );
}

function NavMobile({ onClose }) {
  return (
    <motion.div className="lg:hidden border-t border-[color:var(--border)]"
      initial={{opacity:0, height:0}} animate={{opacity:1, height:"auto"}} exit={{opacity:0, height:0}}
      transition={{duration:0.3}}
      style={{background:"rgba(15,15,15,0.98)"}}>
      <div className="section-container py-6 flex flex-col gap-4">
        {NAV_LINKS.map(l => (
          <a key={l.href} href={l.href} onClick={onClose}
             className="text-base text-[color:var(--text-secondary)] hover:text-[color:var(--text)]"
             data-testid={`mnav-${l.label.toLowerCase().replace(/\s/g,'-')}`}>
            {l.label}
          </a>
        ))}
        <a href={TOOL_URL} target="_blank" rel="noopener noreferrer"
           className="btn-primary text-sm w-fit mt-2" data-testid="mnav-cta">
          Entra nello Spazio <ArrowRight size={16} />
        </a>
      </div>
    </motion.div>
  );
}

function Nav() {
  const [open, setOpen] = useState(false);
  return (
    <header className="nav-shell" data-testid="main-nav">
      <div className="section-container flex items-center justify-between py-5">
        <a href="#top" className="flex items-center gap-3" data-testid="nav-logo">
          <img src="/logo-icon.svg" alt="" className="h-9 md:h-11 w-auto" />
          <span className="text-xl md:text-2xl font-semibold tracking-tight" style={{color:"#F3F1EC"}}>Spazio Sicuro</span>
        </a>
        <NavDesktop />
        <button className="lg:hidden text-[color:var(--text)]" onClick={() => setOpen(!open)}
                aria-label="Menu" data-testid="menu-toggle">
          {open ? <X size={22}/> : <Menu size={22}/>}
        </button>
      </div>
      <AnimatePresence>
        {open && <NavMobile onClose={() => setOpen(false)} />}
      </AnimatePresence>
    </header>
  );
}

// ---------- HERO ----------
function Hero() {
  return (
    <section id="top" className="relative pt-24 md:pt-36 pb-24 md:pb-40 overflow-hidden">
      <div className="absolute inset-0 pointer-events-none"
           style={{
             background: "radial-gradient(800px 500px at 15% 10%, rgba(170,190,255,0.06), transparent 60%), radial-gradient(600px 400px at 85% 90%, rgba(170,190,255,0.04), transparent 60%)"
           }}/>
      <div className="section-container relative">
        <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true, margin:"-100px"}}
                    className="max-w-3xl">
          <p className="text-sm uppercase tracking-[0.2em] text-[color:var(--text-muted)] mb-8" data-testid="hero-eyebrow">
            Uno spazio digitale · Anonimo · Non giudicante
          </p>
          <h1 className="font-display text-4xl md:text-6xl lg:text-7xl font-normal leading-[1.05] text-[color:var(--text)] mb-8"
              data-testid="hero-title">
            Uno spazio dove <em className="text-[color:var(--primary)] not-italic">respirare</em>,
            senza giudizio.
          </h1>
          <p className="text-lg md:text-xl text-[color:var(--text-secondary)] leading-relaxed max-w-2xl mb-12"
             data-testid="hero-subtitle">
            Un luogo privato dove adolescenti e giovani possono sfogarsi attraverso la scrittura,
            il disegno, la voce o il respiro. Nessuna registrazione. Nessun dato salvato.
          </p>
          <div className="flex flex-wrap items-center gap-4">
            <a href={TOOL_URL} target="_blank" rel="noopener noreferrer"
               className="btn-primary" data-testid="hero-cta-primary">
              Entra nello Spazio Sicuro <ArrowRight size={18}/>
            </a>
            <a href="#come" className="btn-ghost" data-testid="hero-cta-secondary">
              Come funziona
            </a>
          </div>
          <BreathCounter />
        </motion.div>
      </div>
    </section>
  );
}

// ---------- CONTATORE ANONIMO ----------
function BreathCounter() {
  const [stats, setStats] = useState(null);
  useEffect(() => {
    axios.get(`${API}/stats/public`).then(r => setStats(r.data)).catch(() => {});
  }, []);
  if (!stats || stats.breaths_total < 1) return null;
  return (
    <motion.p initial={{opacity:0}} animate={{opacity:1}} transition={{duration:1, delay:0.4}}
              className="mt-10 flex items-center gap-2.5 text-sm text-[color:var(--text-muted)]"
              data-testid="breath-counter">
      <Wind size={15} className="text-[color:var(--primary)] shrink-0"/>
      <span>
        <strong className="text-[color:var(--text-secondary)] font-medium">{stats.breaths_today}</strong>
        {" "}respir{stats.breaths_today === 1 ? "o fatto" : "i fatti"} oggi
        {" "}· <strong className="text-[color:var(--text-secondary)] font-medium">{stats.breaths_total}</strong> in totale — tutti anonimi
      </span>
    </motion.p>
  );
}

// ---------- MANIFESTO ----------
function Manifesto() {
  return (
    <section id="manifesto" className="py-24 md:py-32 relative">
      <div className="section-container">
        <div className="grid lg:grid-cols-12 gap-12 items-start">
          <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true, margin:"-100px"}}
                      className="lg:col-span-5">
            <p className="text-sm uppercase tracking-[0.2em] text-[color:var(--primary)] mb-6">Manifesto</p>
            <h2 className="font-display text-3xl md:text-5xl leading-tight text-[color:var(--text)]">
              Silenzio. Ascolto.<br/>Nessuna pretesa.
            </h2>
          </motion.div>
          <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true, margin:"-100px"}}
                      className="lg:col-span-7 space-y-6 text-[color:var(--text-secondary)] text-lg leading-relaxed">
            <p>
              Molti adolescenti vivono emozioni intense senza avere un luogo dove esprimerle.
              La paura del giudizio, lo stigma della salute mentale, la difficoltà di aprirsi
              con adulti o professionisti: tutto porta alla chiusura.
            </p>
            <p>
              <strong className="text-[color:var(--text)] font-medium">
                Spazio Sicuro è un piccolo respiro digitale.
              </strong>{" "}
              Un luogo privato e anonimo dove sfogarsi liberamente — scrivendo, disegnando, parlando o solo respirando.
              Non salviamo nulla. Non chiediamo nulla.
            </p>
            <p>
              Non sostituisce un percorso professionale. È solo un posto dove fermarsi un momento,
              guardarsi dentro, e ricordarsi che quello che si prova è umano.
            </p>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

// ---------- COME FUNZIONA ----------
const MODES = [
  { icon: PenLine, title: "Scrivi",  desc: "Metti in parole ciò che pesa. Nessuno leggerà mai." },
  { icon: Palette, title: "Disegna", desc: "Lascia che il gesto dica ciò che le parole non riescono." },
  { icon: Mic,     title: "Parla",   desc: "La voce libera. Il microfono resta solo sul tuo dispositivo." },
  { icon: Wind,    title: "Respira", desc: "Una respirazione guidata per ritrovare il centro." }
];

function ModeCard({ mode, index }) {
  const Icon = mode.icon;
  return (
    <motion.div variants={fadeUp} initial="hidden" whileInView="show"
                viewport={{once:true, margin:"-50px"}} transition={{delay: index * 0.1}}
                className="editorial-card group hover:border-[color:var(--primary)]/30 transition-colors"
                data-testid={`mode-card-${mode.title.toLowerCase()}`}>
      <div className="bento-icon mb-6"><Icon size={22}/></div>
      <h3 className="font-display text-2xl md:text-3xl mb-3">{mode.title}</h3>
      <p className="text-[color:var(--text-secondary)] leading-relaxed">{mode.desc}</p>
    </motion.div>
  );
}

function ComeFunziona() {
  return (
    <section id="come" className="py-24 md:py-32 border-t border-[color:var(--border)]">
      <div className="section-container">
        <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}
                    className="max-w-2xl mb-16">
          <p className="text-sm uppercase tracking-[0.2em] text-[color:var(--primary)] mb-6">Come funziona</p>
          <h2 className="font-display text-3xl md:text-5xl leading-tight mb-6">
            Quattro modi per<br/>lasciare andare.
          </h2>
          <p className="text-lg text-[color:var(--text-secondary)] leading-relaxed">
            Si entra senza registrazione. Si sceglie una modalità. Al termine si può
            <em> lasciare andare</em> o <em>eliminare</em>. Tutto sparisce.
          </p>
        </motion.div>
        <div className="grid md:grid-cols-2 gap-6">
          {MODES.map((m, i) => <ModeCard key={m.title} mode={m} index={i} />)}
        </div>
        <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}
                    className="mt-16 text-center">
          <a href={TOOL_URL} target="_blank" rel="noopener noreferrer"
             className="btn-primary" data-testid="come-cta">
            Provalo ora <ArrowRight size={18}/>
          </a>
        </motion.div>
      </div>
    </section>
  );
}

// ---------- GENITORI ----------
function ForParents() {
  return (
    <div id="genitori" className="grid lg:grid-cols-12 gap-12">
      <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}
                  className="lg:col-span-5">
        <div className="bento-icon mb-6"><Heart size={22}/></div>
        <p className="text-sm uppercase tracking-[0.2em] text-[color:var(--primary)] mb-4">Per i genitori</p>
        <h2 className="font-display text-3xl md:text-5xl leading-tight">Un supporto non invasivo.</h2>
      </motion.div>
      <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}
                  className="lg:col-span-7 space-y-6 text-[color:var(--text-secondary)] text-lg leading-relaxed">
        <p>
          Sappiamo che è difficile essere presenti senza essere invadenti.
          Spazio Sicuro non è un'app di monitoraggio, non raccoglie dati, non manda notifiche.
        </p>
        <p>
          È semplicemente un luogo dove i vostri figli possono fermarsi, sentirsi accolti, e — se serve —
          ricevere subito i contatti di aiuto giusti. Nulla di ciò che scrivono o dicono viene salvato o condiviso.
        </p>
        <ul className="space-y-3 pt-4">
          <li className="flex gap-3 items-start"><Check size={18} className="text-[color:var(--primary)] mt-1 shrink-0"/>Nessuna registrazione, nessun account</li>
          <li className="flex gap-3 items-start"><Check size={18} className="text-[color:var(--primary)] mt-1 shrink-0"/>Nessun dato salvato o inviato a server</li>
          <li className="flex gap-3 items-start"><Check size={18} className="text-[color:var(--primary)] mt-1 shrink-0"/>Numeri di aiuto sempre a portata</li>
        </ul>
      </motion.div>
    </div>
  );
}

// ---------- SCUOLE ----------
function ForSchools() {
  return (
    <div id="scuole" className="grid lg:grid-cols-12 gap-12">
      <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}
                  className="lg:col-span-5">
        <div className="bento-icon mb-6"><School size={22}/></div>
        <p className="text-sm uppercase tracking-[0.2em] text-[color:var(--primary)] mb-4">Per le scuole</p>
        <h2 className="font-display text-3xl md:text-5xl leading-tight">Uno strumento di prevenzione.</h2>
      </motion.div>
      <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}
                  className="lg:col-span-7 space-y-6 text-[color:var(--text-secondary)] text-lg leading-relaxed">
        <p>
          Spazio Sicuro può essere integrato nei progetti di benessere e prevenzione scolastica.
          È gratuito, sicuro, e non richiede installazione: basta un link.
        </p>
        <p>
          Complementa gli sportelli d'ascolto senza sostituirli: uno spazio a disposizione degli studenti
          anche fuori dagli orari, quando l'ansia arriva alle tre di notte.
        </p>
        <div className="pt-4">
          <a href="#contatti" className="btn-ghost" data-testid="scuole-cta">
            Attiviamo una collaborazione <ArrowRight size={16}/>
          </a>
        </div>
      </motion.div>
    </div>
  );
}

function ParentsSchools() {
  return (
    <section className="py-24 md:py-32 border-t border-[color:var(--border)]">
      <div className="section-container space-y-24">
        <ForParents />
        <hr className="hr-soft"/>
        <ForSchools />
      </div>
    </section>
  );
}

// ---------- PRIVACY ----------
function Privacy() {
  return (
    <section id="privacy" className="py-24 md:py-40 border-t border-[color:var(--border)] text-center">
      <div className="section-container">
        <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}>
          <div className="bento-icon mx-auto mb-8"><Shield size={22}/></div>
          <h2 className="font-display text-4xl md:text-6xl lg:text-7xl leading-none tracking-tight" data-testid="privacy-heading">
            Zero cookie.<br/>
            <span className="text-[color:var(--primary)]">Zero tracciamento.</span><br/>
            Zero dati salvati.
          </h2>
          <p className="mt-12 max-w-2xl mx-auto text-lg text-[color:var(--text-secondary)] leading-relaxed">
            Non registriamo nulla. Non usiamo analytics invasive. Non chiediamo il consenso perché
            non c'è nulla da tracciare. Ciò che scrivi vive solo nella tua sessione, e sparisce quando la chiudi.
          </p>
        </motion.div>
      </div>
    </section>
  );
}

// ---------- EMERGENZA ----------
function EmergencyItem({ number }) {
  return (
    <a href={`tel:${number.n.replace(/\s/g,'')}`}
       className="emerg-item" data-testid={`emergency-${number.n.replace(/\s/g,'')}`}>
      <Phone size={20} className="shrink-0 text-[#ffbaba]"/>
      <div>
        <div className="font-medium text-[color:var(--text)]">{number.n} · {number.l}</div>
        <div className="text-sm text-[color:var(--text-muted)]">{number.s}</div>
      </div>
    </a>
  );
}

function Emergency() {
  return (
    <section className="py-24 md:py-32 border-t border-[color:var(--border)]">
      <div className="section-container max-w-3xl">
        <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}>
          <div className="bento-icon mb-6" style={{background:"rgba(229,115,115,0.08)", borderColor:"rgba(229,115,115,0.2)", color:"#ffbaba"}}>
            <LifeBuoy size={22}/>
          </div>
          <p className="text-sm uppercase tracking-[0.2em] text-[#ffbaba] mb-4">Non sei solo</p>
          <h2 className="font-display text-3xl md:text-5xl leading-tight mb-6">Numeri di aiuto.</h2>
          <p className="text-[color:var(--text-secondary)] text-lg mb-10 leading-relaxed">
            Se stai vivendo un momento difficile, queste linee sono gratuite, anonime e attive.
            Chiamare non è debolezza: è un atto di cura.
          </p>
          <div className="grid sm:grid-cols-2 gap-4">
            {EMERGENCY_NUMBERS.map(n => <EmergencyItem key={n.n} number={n} />)}
          </div>
        </motion.div>
      </div>
    </section>
  );
}

// ---------- FAQ ----------
const FAQ_ITEMS = [
  { q: "Chi c'è dietro Spazio Sicuro?",
    a: "Un progetto indipendente nato dall'idea di offrire ai più giovani un luogo di sfogo digitale sicuro e gratuito. Non è affiliato ad aziende private e non ha scopo di lucro." },
  { q: "L'app raccoglie dati personali?",
    a: "No. Non c'è registrazione, non ci sono cookie di tracciamento, non salviamo nulla. Ogni sessione è temporanea." },
  { q: "Sostituisce il supporto di uno psicologo?",
    a: "Assolutamente no. È uno spazio di sfogo immediato, complementare al supporto professionale. In presenza di disagio intenso l'app suggerisce di rivolgersi a professionisti o linee di aiuto." },
  { q: "Come posso portarlo nella mia scuola?",
    a: "Basta condividere il link con studenti e docenti — non serve installazione né configurazione. Se desideri materiali di presentazione per collegi o progetti, contattaci." },
  { q: "È adatto anche agli adulti?",
    a: "Sì. Anche se pensato per adolescenti, l'esperienza funziona per chiunque desideri un momento di sfogo anonimo." },
  { q: "Come posso sostenere il progetto?",
    a: "Condividerlo con chi potrebbe averne bisogno è già molto. Per collaborazioni istituzionali o supporto strutturato, scrivici tramite il modulo di contatto." }
];

function FAQItem({ item, isOpen, onToggle }) {
  return (
    <div className="border-b border-[color:var(--border)]" data-testid={`faq-item-${item.q}`}>
      <button className="w-full flex items-center justify-between py-6 text-left"
              onClick={onToggle} aria-expanded={isOpen}>
        <span className="font-display text-lg md:text-xl pr-4">{item.q}</span>
        <span className="shrink-0 text-[color:var(--text-secondary)]">
          {isOpen ? <Minus size={20}/> : <Plus size={20}/>}
        </span>
      </button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div initial={{height:0, opacity:0}} animate={{height:"auto", opacity:1}}
                      exit={{height:0, opacity:0}} transition={{duration:0.4, ease:[0.22,1,0.36,1]}}
                      className="overflow-hidden">
            <p className="pb-6 text-[color:var(--text-secondary)] leading-relaxed">{item.a}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function FAQ() {
  const [openKey, setOpenKey] = useState(null);
  return (
    <section id="faq" className="py-24 md:py-32 border-t border-[color:var(--border)]">
      <div className="section-container max-w-3xl">
        <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}>
          <p className="text-sm uppercase tracking-[0.2em] text-[color:var(--primary)] mb-4">Domande frequenti</p>
          <h2 className="font-display text-3xl md:text-5xl leading-tight mb-12">FAQ</h2>
        </motion.div>
        <div>
          {FAQ_ITEMS.map(it => (
            <FAQItem key={it.q} item={it}
                     isOpen={openKey === it.q}
                     onToggle={() => setOpenKey(openKey === it.q ? null : it.q)} />
          ))}
        </div>
      </div>
    </section>
  );
}

// ---------- CONTATTI ----------
const INITIAL_CONTACT = { name:"", email:"", organization:"", role:"", message:"", website:"" };

function ContactForm({ form, onChange, onSubmit, status }) {
  return (
    <motion.form variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}
                 onSubmit={onSubmit} className="grid md:grid-cols-2 gap-4" data-testid="contact-form">
      <input required minLength={1} className="field" placeholder="Nome" value={form.name} onChange={onChange('name')} data-testid="contact-name"/>
      <input required type="email" className="field" placeholder="Email" value={form.email} onChange={onChange('email')} data-testid="contact-email"/>
      <input className="field" placeholder="Scuola / Associazione (facoltativo)" value={form.organization} onChange={onChange('organization')} data-testid="contact-org"/>
      <input className="field" placeholder="Ruolo (facoltativo)" value={form.role} onChange={onChange('role')} data-testid="contact-role"/>
      <textarea required minLength={5} className="field md:col-span-2" rows={6} placeholder="Il tuo messaggio..."
                value={form.message} onChange={onChange('message')} data-testid="contact-message"/>

      {/* Honeypot: campo nascosto agli umani, i bot lo compileranno e verranno scartati */}
      <div style={{position:"absolute", left:"-9999px", width:"1px", height:"1px", overflow:"hidden"}} aria-hidden="true">
        <label>Sito web (non compilare)
          <input type="text" tabIndex={-1} autoComplete="off"
                 value={form.website} onChange={onChange('website')} data-testid="contact-honeypot"/>
        </label>
      </div>

      <div className="md:col-span-2 flex flex-wrap items-center gap-4 pt-2">
        <button type="submit" className="btn-primary" disabled={status.state==='loading'} data-testid="contact-submit">
          {status.state==='loading' ? 'Invio…' : (<>Invia messaggio <Send size={16}/></>)}
        </button>
        {status.state==='success' && (
          <span className="text-sm text-[color:var(--primary)] flex items-center gap-2" data-testid="contact-success">
            <Check size={16}/> {status.msg}
          </span>
        )}
        {status.state==='error' && (
          <span className="text-sm text-[#ff8a8a] flex items-center gap-2" data-testid="contact-error">
            <X size={16}/> {status.msg}
          </span>
        )}
      </div>
    </motion.form>
  );
}

function Contact() {
  const [form, setForm] = useState(INITIAL_CONTACT);
  const [status, setStatus] = useState({ state: "idle", msg: "" });

  const onChange = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    setStatus({state:"loading", msg:""});
    try {
      const res = await axios.post(`${API}/contact`, form);
      if (res.data && res.data.id) {
        setStatus({state:"success", msg:"Grazie. Ti risponderemo appena possibile."});
        setForm(INITIAL_CONTACT);
      }
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setStatus({state:"error", msg: typeof detail === 'string' ? detail : "Si è verificato un errore. Riprova."});
    }
  };

  return (
    <section id="contatti" className="py-24 md:py-32 border-t border-[color:var(--border)]">
      <div className="section-container max-w-3xl">
        <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{once:true}}>
          <p className="text-sm uppercase tracking-[0.2em] text-[color:var(--primary)] mb-4">Collaboriamo</p>
          <h2 className="font-display text-3xl md:text-5xl leading-tight mb-6">
            Sei un docente, un genitore,<br/>un professionista?
          </h2>
          <p className="text-[color:var(--text-secondary)] text-lg leading-relaxed mb-12">
            Scrivici per parlare di come Spazio Sicuro può entrare nella tua scuola o comunità,
            o semplicemente per condividere un pensiero. Rispondiamo a tutti.
          </p>
        </motion.div>
        <ContactForm form={form} onChange={onChange} onSubmit={onSubmit} status={status} />
      </div>
    </section>
  );
}

// ---------- FOOTER ----------
function Footer() {
  return (
    <footer className="pt-14 pb-24 md:pb-14 border-t border-[color:var(--border)]">
      <div className="section-container">
        <div className="flex flex-wrap items-start justify-between gap-8">
          <div>
            <div className="flex items-center gap-2.5 mb-3">
              <img src="/logo-icon.svg" alt="" className="h-8 w-auto" />
              <span className="text-lg font-semibold tracking-tight" style={{color:"#F3F1EC"}}>Spazio Sicuro</span>
            </div>
            <p className="text-sm text-[color:var(--text-muted)] max-w-md leading-relaxed">
              Uno spazio digitale anonimo per esprimere emozioni senza giudizio.
              Progetto sociale indipendente, senza fini di lucro.
            </p>
          </div>
          <div className="text-sm text-[color:var(--text-muted)] space-y-1">
            <p>© {new Date().getFullYear()} Spazio Sicuro</p>
            <p>Non sostituisce un supporto professionale.</p>
            <p className="pt-2">
              <Link to="/privacy" className="hover:text-[color:var(--text)] transition-colors underline underline-offset-4" data-testid="footer-privacy">
                Privacy Policy
              </Link>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}

// ---------- HELP DIALOG ----------
function HelpNumberRow({ number }) {
  return (
    <a href={`tel:${number.n.replace(/\s/g,'')}`} className="emerg-item">
      <Phone size={18} className="text-[#ffbaba]"/>
      <div>
        <div className="font-medium">{number.n} · {number.l}</div>
        <div className="text-xs text-[color:var(--text-muted)]">{number.s}</div>
      </div>
    </a>
  );
}

function HelpDialog({ open, onClose }) {
  useEffect(() => {
    if (!open) return undefined;
    const handleKey = (event) => { if (event.key === 'Escape') onClose(); };
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <motion.div initial={{opacity:0}} animate={{opacity:1}}
                className="fixed inset-0 z-[100] flex items-center justify-center p-4"
                style={{background:"rgba(0,0,0,0.75)", backdropFilter:"blur(8px)"}}
                onClick={onClose} role="dialog" aria-modal="true">
      <motion.div initial={{y:20, opacity:0}} animate={{y:0, opacity:1}} transition={{duration:0.4}}
                  onClick={(e) => e.stopPropagation()}
                  className="editorial-card w-full max-w-md" data-testid="help-dialog">
        <div className="flex items-start justify-between mb-4">
          <h3 className="font-display text-2xl">Non sei solo</h3>
          <button onClick={onClose} className="text-[color:var(--text-secondary)]" aria-label="Chiudi"><X size={20}/></button>
        </div>
        <p className="text-sm text-[color:var(--text-secondary)] mb-6">
          Se stai vivendo un momento difficile, queste linee sono gratuite, anonime e attive.
        </p>
        <div className="space-y-2">
          {EMERGENCY_NUMBERS.map(n => <HelpNumberRow key={n.n} number={n} />)}
        </div>
      </motion.div>
    </motion.div>
  );
}

// ---------- APP ----------
function App() {
  const [helpOpen, setHelpOpen] = useState(false);
  useEffect(() => {
    // Conteggio visite aggregato, zero cookie: una sola ping per sessione di navigazione
    if (!sessionStorage.getItem("ss_visit")) {
      sessionStorage.setItem("ss_visit", "1");
      axios.post(`${API}/events/visit`).catch(() => {});
    }
  }, []);
  return (
    <div className="min-h-screen grain">
      <Nav />
      <main>
        <Hero />
        <Manifesto />
        <ComeFunziona />
        <ParentsSchools />
        <Privacy />
        <Emergency />
        <FAQ />
        <Contact />
      </main>
      <Footer />

      <button className="help-fab" onClick={() => setHelpOpen(true)} data-testid="help-fab"
              aria-label="Ho bisogno d'aiuto ora">
        <LifeBuoy size={16}/> Ho bisogno d'aiuto
      </button>

      <AnimatePresence>
        {helpOpen && <HelpDialog open={helpOpen} onClose={() => setHelpOpen(false)} />}
      </AnimatePresence>
    </div>
  );
}

export default App;
