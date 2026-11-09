"""Genera docs/Lab12_Diseno_Comparacion.pdf desde el Markdown: texto negro, tablas simples y capturas."""
from pathlib import Path
import re

import matplotlib
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SOURCE = DOCS / "Diseno_y_comparacion.md"
OUTPUT = DOCS / "Lab12_Diseno_Comparacion.pdf"

# DejaVu viene con matplotlib y cubre «·», «→», «↺» y demás símbolos del documento.
FONTS = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("DV", FONTS / "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", FONTS / "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV", boldItalic="DV-B")

BODY = ParagraphStyle("body", fontName="DV", fontSize=9.5, leading=13, spaceAfter=5)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8, leading=10, spaceAfter=0)
H1 = ParagraphStyle("h1", parent=BODY, fontName="DV-B", fontSize=15, leading=19, spaceAfter=10)
H2 = ParagraphStyle("h2", parent=BODY, fontName="DV-B", fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=5)
BULLET = ParagraphStyle("bullet", parent=BODY, leftIndent=12, bulletIndent=2)
WIDTH = letter[0] - 4 * cm


def inline(s: str) -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s.replace("`", "")


def table(rows):
    data = [[Paragraph(f"<b>{inline(c)}</b>" if r is rows[0] else inline(c), CELL) for c in r] for r in rows]
    t = Table(data, colWidths=[WIDTH / len(rows[0])] * len(rows[0]), repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def story_from_markdown():
    raw = SOURCE.read_text(encoding="utf-8").splitlines()
    out, i = [], 0
    while i < len(raw):
        s = raw[i].strip()
        if s.startswith("# "): out.append(Paragraph(inline(s[2:]), H1))
        elif s.startswith("## "): out.append(Paragraph(inline(s[3:]), H2))
        elif s.startswith("|"):
            rows = []
            while i < len(raw) and raw[i].strip().startswith("|"):
                cells = [c.strip() for c in raw[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells): rows.append(cells)
                i += 1
            out += [table(rows), Spacer(1, 6)]
            continue
        elif s.startswith("- "): out.append(Paragraph(inline(s[2:]), BULLET, bulletText="•"))
        elif s: out.append(Paragraph(inline(s), BODY))
        i += 1
    return out


CAPTURAS = [
    ("01_vista_inicial.png", "Captura 01. Power BI, avance (5 nov): vista inicial."),
    ("02_clic_Estados_Unidos_en_V2.png", "Captura 02. Avance: clic en Estados Unidos en V2."),
    ("03_clic_2020_en_V3.png", "Captura 03. Avance: clic en 2020 en V3; V1 a nivel de mes."),
    ("10_final_p1_panorama.png", "Captura 10. Versión final: 1 · Panorama (V1-V3)."),
    ("11_final_p2_detalle_2025.png", "Captura 11. Versión final: 2 · Detalle mensual (V4)."),
    ("12_final_p3_calendario_mercados.png", "Captura 12. Versión final: 3 · Calendario y mercados (V5-V7)."),
    ("13_final_p4_pronosticos.png", "Captura 13. Versión final: 4 · Pronósticos (V8, V8b, V9, V10)."),
    ("20_streamlit_A_recuperacion.png", "Captura 20. Streamlit (Lab 10): prueba A."),
    ("21_streamlit_B_mes_minimo.png", "Captura 21. Streamlit (Lab 10): prueba B."),
    ("22_streamlit_C_modelos.png", "Captura 22. Streamlit (Lab 10): prueba C."),
]


def capturas():
    out = [PageBreak(), Paragraph("Anexo. Capturas", H2)]
    for name, caption in CAPTURAS:
        path = DOCS / "capturas" / name
        if not path.exists(): continue
        w, h = ImageReader(str(path)).getSize()
        out.append(KeepTogether([Image(str(path), WIDTH, WIDTH * h / w), Paragraph(caption, BODY), Spacer(1, 10)]))
    return out


def numero(canvas, doc):
    canvas.setFont("DV", 8)
    canvas.drawRightString(letter[0] - 2 * cm, 1.2 * cm, str(doc.page))


def main():
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm, title="Laboratorio 12 · Diseño y comparación")
    doc.build(story_from_markdown() + capturas(), onFirstPage=numero, onLaterPages=numero)
    print(OUTPUT)


if __name__ == "__main__": main()
