"""
PDF versione BASE — coerente visivamente con il tool single-file HTML.
Estetica: silenzio, centralità, poco per pagina, tanto respiro.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os

BG        = HexColor("#0f0f0f")
SURFACE   = HexColor("#1a1a2a")
PRIMARY   = HexColor("#aabeff")
TEXT      = HexColor("#f1f1f1")
TEXT_SEC  = HexColor("#c8c8d4")
TEXT_MUT  = HexColor("#8a8a9a")
BORDER    = HexColor("#26263a")
EMERGENCY = HexColor("#ffbaba")
EMERG_BG  = HexColor("#2a0f0f")

DISPLAY = "Helvetica"
DISPLAY_B = "Helvetica-Bold"
BODY    = "Helvetica"
BODY_L  = "Helvetica-Oblique"

PAGE_W, PAGE_H = A4
CX = PAGE_W / 2

def draw_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

def draw_footer(c, page_num, total):
    c.setFillColor(TEXT_MUT)
    c.setFont(BODY, 8)
    c.drawCentredString(CX, 15*mm, f"— {page_num} / {total} —")

def draw_top(c, label):
    c.setFillColor(TEXT_MUT)
    c.setFont(BODY, 8)
    c.drawCentredString(CX, PAGE_H - 18*mm, label.upper())

def center_wrap(c, text, y, max_width, font, size, leading, color=TEXT):
    """Wrap text and center each line."""
    c.setFillColor(color)
    c.setFont(font, size)
    lines = []
    for para in text.split("\n"):
        words = para.split()
        line = ""
        for w in words:
            probe = (line + " " + w).strip()
            if c.stringWidth(probe, font, size) <= max_width:
                line = probe
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        lines.append("")  # blank line between paragraphs
    if lines and lines[-1] == "":
        lines.pop()
    for l in lines:
        c.drawCentredString(CX, y, l)
        y -= leading
    return y

# =========================================================
# PAGE 1 — Cover
# =========================================================
def page_cover(c):
    draw_bg(c)

    # Sottile cerchio, come il cerchio del respiro nel tool
    c.setStrokeColor(HexColor("#1c1c2c"))
    c.setLineWidth(0.5)
    c.circle(CX, PAGE_H - 90*mm, 40*mm, stroke=1, fill=0)
    c.circle(CX, PAGE_H - 90*mm, 25*mm, stroke=1, fill=0)

    c.setFillColor(PRIMARY)
    c.setFont(BODY, 8.5)
    c.drawCentredString(CX, PAGE_H - 45*mm, "S P A Z I O   S I C U R O")

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 34)
    c.drawCentredString(CX, PAGE_H - 130*mm, "Uno spazio dove respirare,")
    c.drawCentredString(CX, PAGE_H - 143*mm, "senza giudizio.")

    c.setFillColor(TEXT_SEC)
    c.setFont(BODY_L, 13)
    c.drawCentredString(CX, PAGE_H - 165*mm, "un piccolo spazio digitale · anonimo · gratuito")

    # Al centro-basso: pulsante stilizzato come nel tool
    btn_w, btn_h = 80*mm, 12*mm
    btn_x = CX - btn_w/2
    btn_y = PAGE_H - 210*mm
    c.setFillColor(SURFACE)
    c.roundRect(btn_x, btn_y, btn_w, btn_h, 5*mm, stroke=0, fill=1)
    c.setFillColor(TEXT)
    c.setFont(BODY, 11)
    c.drawCentredString(CX, btn_y + 4.5*mm, "Entra")

    draw_footer(c, 1, 4)
    c.showPage()

# =========================================================
# PAGE 2 — Cosa è
# =========================================================
def page_what(c):
    draw_bg(c)
    draw_top(c, "cosa è")

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 22)
    c.drawCentredString(CX, PAGE_H - 55*mm, "Non è un'app.")
    c.drawCentredString(CX, PAGE_H - 68*mm, "Non è una terapia.")
    c.drawCentredString(CX, PAGE_H - 81*mm, "È solo un momento.")

    y = PAGE_H - 110*mm
    y = center_wrap(c,
        "Una pagina web che si apre da un link.\n"
        "Senza registrazione. Senza account.\n"
        "Nulla viene salvato. Nulla viene inviato.\n\n"
        "Al termine, si può lasciare andare o eliminare. Tutto sparisce.",
        y, 130*mm, BODY, 11.5, 16, TEXT_SEC)

    # Elenco modalità come pulsanti verticali (come nel tool)
    y = y - 12*mm
    modes = [("Scrivi",  "scrivere ciò che pesa"),
             ("Disegna", "un gesto liberatorio"),
             ("Parla",   "dire ad alta voce"),
             ("Respira", "respirazione guidata")]
    btn_w, btn_h = 100*mm, 10*mm
    for title, desc in modes:
        bx = CX - btn_w/2
        c.setFillColor(SURFACE)
        c.roundRect(bx, y - btn_h, btn_w, btn_h, 3*mm, stroke=0, fill=1)
        c.setFillColor(TEXT)
        c.setFont(BODY, 11)
        c.drawString(bx + 8*mm, y - btn_h + 3.5*mm, title)
        c.setFillColor(TEXT_MUT)
        c.setFont(BODY, 9)
        c.drawRightString(bx + btn_w - 8*mm, y - btn_h + 3.5*mm, desc)
        y -= btn_h + 3*mm

    draw_footer(c, 2, 4)
    c.showPage()

# =========================================================
# PAGE 3 — Privacy & Aiuto
# =========================================================
def page_privacy(c):
    draw_bg(c)
    draw_top(c, "privacy")

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 26)
    c.drawCentredString(CX, PAGE_H - 55*mm, "Niente da tracciare.")

    y = PAGE_H - 80*mm
    y = center_wrap(c,
        "Non usiamo cookie.\n"
        "Non usiamo analytics.\n"
        "Non salviamo testi, disegni, voci.\n\n"
        "Non c'è nulla da nascondere,\n"
        "perché non c'è nulla da conservare.",
        y, 130*mm, BODY, 12, 17, TEXT_SEC)

    # Sottile separatore
    y = y - 15*mm
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.4)
    c.line(CX - 20*mm, y, CX + 20*mm, y)

    y = y - 15*mm
    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 16)
    c.drawCentredString(CX, y, "Se il peso è troppo,")
    c.drawCentredString(CX, y - 10*mm, "questi numeri esistono per te.")

    # Numeri: uno per riga, centrati come i pulsanti del tool
    y = y - 25*mm
    numeri = [
        ("112",            "Emergenza"),
        ("19696",          "Telefono Azzurro · minori · 24 su 24"),
        ("02 2327 2327",   "Telefono Amico · 10:00–24:00"),
        ("800 86 10 61",   "Prevenzione Suicidio · Samaritans Onlus"),
    ]
    for num, desc in numeri:
        c.setFillColor(EMERG_BG)
        bx = CX - 75*mm
        c.roundRect(bx, y - 9*mm, 150*mm, 9*mm, 2.5*mm, stroke=0, fill=1)
        c.setFillColor(EMERGENCY)
        c.setFont(BODY, 10.5)
        c.drawString(bx + 8*mm, y - 6*mm, num)
        c.setFillColor(TEXT_SEC)
        c.setFont(BODY, 9)
        c.drawRightString(bx + 150*mm - 8*mm, y - 6*mm, desc)
        y -= 12*mm

    draw_footer(c, 3, 4)
    c.showPage()

# =========================================================
# PAGE 4 — Chiusura & Uso
# =========================================================
def page_close(c):
    draw_bg(c)
    draw_top(c, "come portarlo a chi ne ha bisogno")

    c.setFillColor(TEXT)
    c.setFont(DISPLAY, 24)
    c.drawCentredString(CX, PAGE_H - 55*mm, "Basta un link.")

    y = PAGE_H - 78*mm
    y = center_wrap(c,
        "Niente installazioni. Niente formazione. Niente budget.\n"
        "Chiunque abbia una connessione può usarlo.\n\n"
        "Puoi condividerlo con studenti, figli, colleghi.\n"
        "Puoi presentarlo in cinque minuti.\n"
        "Puoi lasciare che sia lì, in silenzio, per quando servirà.",
        y, 140*mm, BODY, 11.5, 16, TEXT_SEC)

    # Sottile separatore
    y = y - 20*mm
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.4)
    c.line(CX - 20*mm, y, CX + 20*mm, y)

    y = y - 20*mm
    c.setFillColor(TEXT)
    c.setFont(BODY_L, 14)
    c.drawCentredString(CX, y, "Non salviamo storie.")
    c.setFont(BODY_L, 14)
    c.drawCentredString(CX, y - 8*mm, "Ma qualcuno, stasera,")
    c.drawCentredString(CX, y - 16*mm, "respirerà un po' meglio.")

    c.setFillColor(PRIMARY)
    c.setFont(DISPLAY, 12)
    c.drawCentredString(CX, y - 34*mm, "E questo è già abbastanza.")

    draw_footer(c, 4, 4)
    c.showPage()

# =========================================================
def build_pdf(output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle("Spazio Sicuro")
    c.setAuthor("Spazio Sicuro")
    c.setSubject("Uno spazio dove respirare, senza giudizio.")
    page_cover(c)
    page_what(c)
    page_privacy(c)
    page_close(c)
    c.save()

if __name__ == "__main__":
    out = "/app/spazio-sicuro-presentazione.pdf"
    build_pdf(out)
    print(f"PDF versione base creato: {out}")
    print(f"Dimensione: {os.path.getsize(out)/1024:.1f} KB")
