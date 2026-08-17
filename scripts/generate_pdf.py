"""
PDF versione BASE — con screenshot reali del tool su Netlify.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

BG        = HexColor("#0f0f0f")
SURFACE   = HexColor("#1a1a2a")
PRIMARY   = HexColor("#aabeff")
TEXT      = HexColor("#f1f1f1")
TEXT_SEC  = HexColor("#c8c8d4")
TEXT_MUT  = HexColor("#8a8a9a")
BORDER    = HexColor("#26263a")

BODY   = "Helvetica"
BODY_B = "Helvetica-Bold"
BODY_L = "Helvetica-Oblique"

PAGE_W, PAGE_H = A4
CX = PAGE_W / 2
ASSETS = "/app/pdf_assets"

def draw_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

def draw_footer(c, page_num, total):
    c.setFillColor(TEXT_MUT)
    c.setFont(BODY, 8)
    c.drawCentredString(CX, 12*mm, f"Spazio Sicuro   ·   {page_num} / {total}")

def draw_top(c, label):
    c.setFillColor(PRIMARY)
    c.setFont(BODY, 8)
    c.drawCentredString(CX, PAGE_H - 15*mm, label.upper())

def draw_screenshot(c, img_path, y_top, height_mm=110, caption=None):
    """Disegna uno screenshot centrato con cornice tenue e didascalia opzionale."""
    img = ImageReader(img_path)
    iw, ih = img.getSize()
    aspect = iw / ih
    h = height_mm * mm
    w = h * aspect
    if w > PAGE_W - 40*mm:
        w = PAGE_W - 40*mm
        h = w / aspect
    x = (PAGE_W - w) / 2
    y = y_top - h
    # sottile cornice
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.roundRect(x - 1*mm, y - 1*mm, w + 2*mm, h + 2*mm, 2*mm, stroke=1, fill=0)
    c.drawImage(img, x, y, width=w, height=h, mask='auto')
    if caption:
        c.setFillColor(TEXT_MUT)
        c.setFont(BODY_L, 9)
        c.drawCentredString(CX, y - 7*mm, caption)
    return y

def wrap_center(c, text, y, max_width, font, size, leading, color=TEXT_SEC):
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
                lines.append(line); line = w
        if line: lines.append(line)
        lines.append("")
    if lines and lines[-1] == "": lines.pop()
    for l in lines:
        c.drawCentredString(CX, y, l)
        y -= leading
    return y

# =========================================================
def page_cover(c):
    draw_bg(c)
    c.setFillColor(PRIMARY)
    c.setFont(BODY, 8.5)
    c.drawCentredString(CX, PAGE_H - 35*mm, "S P A Z I O   S I C U R O")

    c.setFillColor(TEXT)
    c.setFont(BODY_B, 30)
    c.drawCentredString(CX, PAGE_H - 55*mm, "Uno spazio dove respirare,")
    c.drawCentredString(CX, PAGE_H - 68*mm, "senza giudizio.")

    c.setFillColor(TEXT_SEC)
    c.setFont(BODY_L, 12)
    c.drawCentredString(CX, PAGE_H - 82*mm, "un piccolo spazio digitale · anonimo · gratuito")

    # Screenshot pagina benvenuto centrale
    draw_screenshot(c, f"{ASSETS}/screen1_welcome.png", PAGE_H - 92*mm, height_mm=145,
                    caption="La pagina di benvenuto — un solo pulsante per entrare")

    draw_footer(c, 1, 4)
    c.showPage()

def page_modes(c):
    draw_bg(c)
    draw_top(c, "come funziona")

    c.setFillColor(TEXT)
    c.setFont(BODY_B, 22)
    c.drawCentredString(CX, PAGE_H - 30*mm, "Quattro modi per lasciare andare.")

    wrap_center(c,
        "Uno stato d'animo opzionale, quattro modalità.\n"
        "Nessuna scelta è giusta. Nessuna è sbagliata.",
        PAGE_H - 45*mm, 140*mm, BODY, 11, 15, TEXT_SEC)

    draw_screenshot(c, f"{ASSETS}/screen2_modes.png", PAGE_H - 78*mm, height_mm=155,
                    caption="Stato d'animo + Scrivi · Disegna · Parla · Respira")

    draw_footer(c, 2, 4)
    c.showPage()

def page_breath_privacy(c):
    draw_bg(c)
    draw_top(c, "respiro guidato")

    c.setFillColor(TEXT)
    c.setFont(BODY_B, 20)
    c.drawCentredString(CX, PAGE_H - 30*mm, "Un cerchio che respira con te.")

    wrap_center(c,
        "Quando le parole non bastano, resta il respiro.\n"
        "Tecnica 4-4-4-4 — quattro secondi dentro, quattro sospesi, quattro fuori, quattro di pausa.",
        PAGE_H - 45*mm, 150*mm, BODY, 10.5, 14, TEXT_SEC)

    draw_screenshot(c, f"{ASSETS}/screen3_breath.png", PAGE_H - 74*mm, height_mm=110,
                    caption="La modalità Respira — semplice, silenziosa, calmante")

    # sezione privacy
    y = PAGE_H - 200*mm
    c.setStrokeColor(BORDER); c.setLineWidth(0.4)
    c.line(CX - 20*mm, y, CX + 20*mm, y)
    c.setFillColor(TEXT)
    c.setFont(BODY_B, 16)
    c.drawCentredString(CX, y - 12*mm, "E nulla di tutto questo viene salvato.")
    wrap_center(c,
        "Niente cookie. Niente analytics. Niente registrazione.\n"
        "Testi, disegni, voci: vivono solo nella sessione. Poi spariscono.",
        y - 25*mm, 150*mm, BODY, 10.5, 14, TEXT_SEC)

    draw_footer(c, 3, 4)
    c.showPage()

def page_help_close(c):
    draw_bg(c)
    draw_top(c, "quando serve aiuto")

    c.setFillColor(TEXT)
    c.setFont(BODY_B, 20)
    c.drawCentredString(CX, PAGE_H - 30*mm, "Non sei solo.")

    wrap_center(c,
        "Se le parole diventano troppo pesanti, un pulsante è sempre lì:\n"
        "quattro numeri gratuiti e anonimi, a portata di tocco.",
        PAGE_H - 45*mm, 150*mm, BODY, 10.5, 14, TEXT_SEC)

    draw_screenshot(c, f"{ASSETS}/screen4_help.png", PAGE_H - 74*mm, height_mm=105,
                    caption="Il pannello di aiuto — sempre visibile in alto a destra")

    # Chiusura
    y = PAGE_H - 200*mm
    c.setStrokeColor(BORDER); c.setLineWidth(0.4)
    c.line(CX - 20*mm, y, CX + 20*mm, y)

    c.setFillColor(TEXT)
    c.setFont(BODY_L, 13)
    c.drawCentredString(CX, y - 15*mm, "Non salviamo storie.")
    c.drawCentredString(CX, y - 24*mm, "Ma qualcuno, stasera, respirerà un po' meglio.")

    c.setFillColor(PRIMARY)
    c.setFont(BODY_B, 11)
    c.drawCentredString(CX, y - 40*mm, "E questo è già abbastanza.")

    draw_footer(c, 4, 4)
    c.showPage()

# =========================================================
def build_pdf(output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle("Spazio Sicuro")
    c.setAuthor("Spazio Sicuro")
    c.setSubject("Uno spazio dove respirare, senza giudizio.")
    page_cover(c)
    page_modes(c)
    page_breath_privacy(c)
    page_help_close(c)
    c.save()

if __name__ == "__main__":
    out = "/app/spazio-sicuro-presentazione.pdf"
    build_pdf(out)
    print(f"PDF con screenshot creato: {out}")
    print(f"Dimensione: {os.path.getsize(out)/1024:.1f} KB")
