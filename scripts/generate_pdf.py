"""
Generatore PDF di presentazione — Spazio Sicuro.
Produce un PDF A4 elegante, 4 pagine, in italiano.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import os

# Try registering nicer fonts. Fallback silently.
FONTS_DIR = Path(__file__).parent / "fonts"

def _try_font(name, path):
    try:
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
            return True
    except Exception:
        return False
    return False

# System fonts fallback
DISPLAY = "Helvetica-Bold"
BODY    = "Helvetica"
BODY_L  = "Helvetica-Oblique"

# Colors
BG        = HexColor("#0f0f0f")
SURFACE   = HexColor("#161624")
PRIMARY   = HexColor("#aabeff")
TEXT      = HexColor("#f2f2f5")
TEXT_SEC  = HexColor("#a1a1b5")
TEXT_MUT  = HexColor("#71718a")
BORDER    = HexColor("#2a2a3d")
EMERGENCY = HexColor("#e57373")

PAGE_W, PAGE_H = A4
MARGIN_X = 22 * mm
MARGIN_Y = 22 * mm

def draw_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

def draw_footer(c, page_num, total):
    c.setFillColor(TEXT_MUT)
    c.setFont(BODY, 8)
    c.drawString(MARGIN_X, 12*mm, "Spazio Sicuro · uno spazio anonimo per esprimere emozioni")
    c.drawRightString(PAGE_W - MARGIN_X, 12*mm, f"{page_num} / {total}")

def draw_header(c, subtitle=None):
    c.setFillColor(PRIMARY)
    c.setFont(BODY, 8)
    c.drawString(MARGIN_X, PAGE_H - 15*mm, "SPAZIO SICURO")
    if subtitle:
        c.setFillColor(TEXT_MUT)
        c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 15*mm, subtitle.upper())

def wrap_text(c, text, x, y, max_width, font, size, leading, color=TEXT):
    """Wrap plain text respecting explicit \\n."""
    c.setFillColor(color)
    c.setFont(font, size)
    for para in text.split("\n"):
        words = para.split()
        line = ""
        for w in words:
            probe = (line + " " + w).strip()
            if c.stringWidth(probe, font, size) <= max_width:
                line = probe
            else:
                c.drawString(x, y, line)
                y -= leading
                line = w
        if line:
            c.drawString(x, y, line)
            y -= leading
        y -= leading * 0.35
    return y

# =========================================================
# PAGE 1 — Cover
# =========================================================
def page_cover(c):
    draw_bg(c)

    # Subtle circle accent
    c.setStrokeColor(HexColor("#1c1c30"))
    c.setLineWidth(0.6)
    c.circle(PAGE_W - 40*mm, PAGE_H - 60*mm, 55*mm, stroke=1, fill=0)
    c.circle(PAGE_W - 40*mm, PAGE_H - 60*mm, 35*mm, stroke=1, fill=0)

    c.setFillColor(PRIMARY)
    c.setFont(BODY, 9)
    c.drawString(MARGIN_X, PAGE_H - 35*mm, "PROGETTO SOCIALE · 2026")

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 46)
    c.drawString(MARGIN_X, PAGE_H - 70*mm, "Spazio Sicuro")

    c.setFillColor(TEXT_SEC)
    c.setFont(BODY_L, 16)
    c.drawString(MARGIN_X, PAGE_H - 82*mm, "Uno spazio dove respirare, senza giudizio.")

    # Divider
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.4)
    c.line(MARGIN_X, PAGE_H - 100*mm, PAGE_W - MARGIN_X, PAGE_H - 100*mm)

    # Description block
    c.setFillColor(TEXT)
    c.setFont(BODY, 11.5)
    y = PAGE_H - 115*mm
    text = (
        "Spazio Sicuro è una web app anonima, gratuita e non giudicante\n"
        "dove adolescenti e giovani possono sfogare emozioni intense\n"
        "attraverso scrittura, disegno, voce o respirazione guidata.\n\n"
        "Nessuna registrazione. Nessun dato salvato.\n"
        "Solo un momento per fermarsi e respirare."
    )
    y = wrap_text(c, text, MARGIN_X, y, PAGE_W - 2*MARGIN_X, BODY, 11.5, 15, TEXT)

    # Highlight box
    box_y = 55*mm
    c.setFillColor(SURFACE)
    c.roundRect(MARGIN_X, box_y, PAGE_W - 2*MARGIN_X, 30*mm, 4*mm, stroke=0, fill=1)
    c.setFillColor(PRIMARY)
    c.setFont(BODY, 8)
    c.drawString(MARGIN_X + 8*mm, box_y + 22*mm, "PER SCUOLE · GENITORI · EDUCATORI")
    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 13)
    c.drawString(MARGIN_X + 8*mm, box_y + 13*mm, "Uno strumento di prevenzione e benessere emotivo.")
    c.setFillColor(TEXT_SEC)
    c.setFont(BODY, 9.5)
    c.drawString(MARGIN_X + 8*mm, box_y + 6*mm, "Attivabile in qualsiasi scuola con un semplice link. Gratuito, sicuro, senza installazione.")

    draw_footer(c, 1, 4)
    c.showPage()

# =========================================================
# PAGE 2 — Il progetto
# =========================================================
def page_manifesto(c):
    draw_bg(c)
    draw_header(c, "Il progetto")

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 24)
    c.drawString(MARGIN_X, PAGE_H - 35*mm, "Il problema")

    c.setFillColor(TEXT_SEC)
    y = PAGE_H - 45*mm
    y = wrap_text(c,
        "Molti adolescenti vivono emozioni intense senza avere uno spazio dove esprimerle.\n"
        "La paura del giudizio, lo stigma della salute mentale e la difficoltà di aprirsi\n"
        "con adulti o professionisti portano spesso a chiusura, isolamento, comportamenti\n"
        "impulsivi. Il telefono è sempre in tasca, ma raramente offre un vero luogo di sfogo.",
        MARGIN_X, y, PAGE_W - 2*MARGIN_X, BODY, 11, 15, TEXT_SEC)

    # Section 2
    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 24)
    c.drawString(MARGIN_X, y - 10*mm, "La soluzione")

    y = y - 20*mm
    y = wrap_text(c,
        "Spazio Sicuro è una web app privata, anonima e temporanea.\n"
        "L'utente entra senza registrazione e sceglie come esprimersi:\n"
        "scrivendo, disegnando, parlando o respirando.\n"
        "Al termine può \"lasciare andare\" o \"eliminare\" tutto. Nulla resta.",
        MARGIN_X, y, PAGE_W - 2*MARGIN_X, BODY, 11, 15, TEXT_SEC)

    # 4 mode boxes
    y_box = y - 15*mm
    box_w = (PAGE_W - 2*MARGIN_X - 12*mm) / 4
    modes = [("Scrivi", "Mettere in parole"),
             ("Disegna", "Gesto liberatorio"),
             ("Parla", "Voce non registrata"),
             ("Respira", "4-4-4-4 guidato")]
    for i, (title, desc) in enumerate(modes):
        x = MARGIN_X + i * (box_w + 4*mm)
        c.setFillColor(SURFACE)
        c.roundRect(x, y_box - 30*mm, box_w, 30*mm, 3*mm, stroke=0, fill=1)
        c.setFillColor(PRIMARY)
        c.setFont(DISPLAY, 14)
        c.drawString(x + 5*mm, y_box - 10*mm, title)
        c.setFillColor(TEXT_MUT)
        c.setFont(BODY, 8.5)
        c.drawString(x + 5*mm, y_box - 17*mm, desc)

    # Valore per la comunità
    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 20)
    c.drawString(MARGIN_X, y_box - 45*mm, "Valore per la comunità")

    lines = [
        ("Per gli adolescenti", "uno spazio di sfogo immediato, sicuro e privo di stigma."),
        ("Per i genitori", "un supporto emotivo non invasivo, senza tracciamento."),
        ("Per le scuole", "uno strumento di prevenzione integrabile nei progetti di benessere."),
    ]
    yy = y_box - 55*mm
    for label, val in lines:
        c.setFillColor(PRIMARY)
        c.setFont(DISPLAY, 11)
        c.drawString(MARGIN_X, yy, label)
        c.setFillColor(TEXT_SEC)
        c.setFont(BODY, 10.5)
        c.drawString(MARGIN_X + 50*mm, yy, val)
        yy -= 8*mm

    draw_footer(c, 2, 4)
    c.showPage()

# =========================================================
# PAGE 3 — Privacy & Sicurezza
# =========================================================
def page_privacy(c):
    draw_bg(c)
    draw_header(c, "Privacy e responsabilità")

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 28)
    c.drawString(MARGIN_X, PAGE_H - 40*mm, "Privacy assoluta.")

    c.setFillColor(TEXT_SEC)
    y = PAGE_H - 55*mm
    y = wrap_text(c,
        "Spazio Sicuro è stato progettato secondo il principio della \"privacy by design\":\n"
        "nulla viene raccolto perché non c'è nulla da tracciare.",
        MARGIN_X, y, PAGE_W - 2*MARGIN_X, BODY, 11, 15, TEXT_SEC)

    # Zero cards
    zeros = [
        ("Zero cookie", "Nessun cookie di tracciamento, nessuna analytics invasiva."),
        ("Zero dati", "Nulla di ciò che l'utente scrive, disegna o dice viene salvato."),
        ("Zero registrazione", "Non serve alcun account. Nessuna email, nessun profilo."),
    ]
    yz = y - 10*mm
    for label, desc in zeros:
        c.setFillColor(SURFACE)
        c.roundRect(MARGIN_X, yz - 18*mm, PAGE_W - 2*MARGIN_X, 16*mm, 3*mm, stroke=0, fill=1)
        c.setFillColor(PRIMARY)
        c.setFont(DISPLAY, 13)
        c.drawString(MARGIN_X + 6*mm, yz - 8*mm, label)
        c.setFillColor(TEXT_SEC)
        c.setFont(BODY, 10)
        c.drawString(MARGIN_X + 55*mm, yz - 8*mm, desc)
        yz -= 20*mm

    # Responsabilità
    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 18)
    c.drawString(MARGIN_X, yz - 5*mm, "Responsabilità e limiti")

    y2 = yz - 15*mm
    y2 = wrap_text(c,
        "Spazio Sicuro non sostituisce un supporto psicologico professionale.\n"
        "In presenza di segnali di disagio intenso, l'app riconosce automaticamente\n"
        "parole-chiave e propone all'utente i numeri di aiuto: 112, Telefono Azzurro (19696),\n"
        "Telefono Amico, Prevenzione Suicidio.",
        MARGIN_X, y2, PAGE_W - 2*MARGIN_X, BODY, 10.5, 14, TEXT_SEC)

    # Emergency box
    y3 = y2 - 8*mm
    c.setFillColor(HexColor("#2a0f0f"))
    c.roundRect(MARGIN_X, y3 - 34*mm, PAGE_W - 2*MARGIN_X, 32*mm, 3*mm, stroke=0, fill=1)
    c.setFillColor(EMERGENCY)
    c.setFont(BODY, 8)
    c.drawString(MARGIN_X + 6*mm, y3 - 7*mm, "SEMPRE ACCESSIBILI NELL'APP")
    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 12)
    c.drawString(MARGIN_X + 6*mm, y3 - 14*mm, "112  ·  Emergenza")
    c.drawString(MARGIN_X + 6*mm, y3 - 20*mm, "19696  ·  Telefono Azzurro (minori)")
    c.drawString(MARGIN_X + 6*mm, y3 - 26*mm, "02 2327 2327  ·  Telefono Amico")
    c.drawString(MARGIN_X + 6*mm, y3 - 32*mm, "800 86 10 61  ·  Prevenzione Suicidio")

    draw_footer(c, 3, 4)
    c.showPage()

# =========================================================
# PAGE 4 — Adozione & Contatti
# =========================================================
def page_adoption(c):
    draw_bg(c)
    draw_header(c, "Adozione e collaborazioni")

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 24)
    c.drawString(MARGIN_X, PAGE_H - 35*mm, "Come portarlo nella tua scuola.")

    y = PAGE_H - 50*mm
    steps = [
        ("1", "Condivisione", "Basta condividere il link con studenti e docenti. Nessuna installazione."),
        ("2", "Informazione", "Presentazione in classe o assemblea: 15 minuti bastano per introdurre lo strumento."),
        ("3", "Integrazione", "Complementare agli sportelli d'ascolto: attivo anche fuori orario scolastico."),
        ("4", "Feedback", "Raccogliamo insieme feedback anonimi per migliorare progressivamente."),
    ]
    for num, title, desc in steps:
        c.setFillColor(PRIMARY)
        c.setFont(DISPLAY, 18)
        c.drawString(MARGIN_X, y, num)
        c.setFillColor(TEXT)
        c.setFont(DISPLAY, 13)
        c.drawString(MARGIN_X + 12*mm, y, title)
        c.setFillColor(TEXT_SEC)
        c.setFont(BODY, 10)
        c.drawString(MARGIN_X + 12*mm, y - 6*mm, desc)
        y -= 18*mm

    # Ambiti
    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 18)
    c.drawString(MARGIN_X, y - 5*mm, "Ambiti di adozione")

    yy = y - 15*mm
    ambiti = ["Scuole secondarie di primo e secondo grado", "Servizi educativi giovanili",
              "Centri di salute mentale", "Progetti di prevenzione e benessere emotivo",
              "Oratori, associazioni di quartiere"]
    for a in ambiti:
        c.setFillColor(PRIMARY)
        c.circle(MARGIN_X + 1*mm, yy + 1.2*mm, 0.8*mm, stroke=0, fill=1)
        c.setFillColor(TEXT_SEC)
        c.setFont(BODY, 10.5)
        c.drawString(MARGIN_X + 6*mm, yy, a)
        yy -= 6.5*mm

    # Contact block
    yc = yy - 10*mm
    c.setFillColor(SURFACE)
    c.roundRect(MARGIN_X, yc - 28*mm, PAGE_W - 2*MARGIN_X, 26*mm, 3*mm, stroke=0, fill=1)
    c.setFillColor(PRIMARY)
    c.setFont(BODY, 8)
    c.drawString(MARGIN_X + 8*mm, yc - 8*mm, "CONTATTI")
    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 14)
    c.drawString(MARGIN_X + 8*mm, yc - 15*mm, "Scriveteci per attivare una collaborazione.")
    c.setFillColor(TEXT_SEC)
    c.setFont(BODY, 10)
    c.drawString(MARGIN_X + 8*mm, yc - 22*mm, "Attraverso il modulo sul sito · Rispondiamo a tutti.")

    draw_footer(c, 4, 4)
    c.showPage()

# =========================================================
def build_pdf(output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle("Spazio Sicuro — Presentazione")
    c.setAuthor("Spazio Sicuro")
    c.setSubject("Presentazione del progetto")

    page_cover(c)
    page_manifesto(c)
    page_privacy(c)
    page_adoption(c)

    c.save()

if __name__ == "__main__":
    out = "/app/spazio-sicuro-presentazione.pdf"
    build_pdf(out)
    print(f"PDF creato: {out}")
    print(f"Dimensione: {os.path.getsize(out)/1024:.1f} KB")
