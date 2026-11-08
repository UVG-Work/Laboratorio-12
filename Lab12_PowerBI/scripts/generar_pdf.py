"""Produce el PDF final desde el Markdown cuando Word no está disponible."""
from pathlib import Path
import re
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.image import imread

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SOURCE = DOCS / "Diseno_y_comparacion.md"
OUTPUT = DOCS / "Lab12_Diseno_Comparacion.pdf"


def clean(s: str) -> str:
    return s.replace("**", "").replace("`", "").replace("  ", " ").strip()


def lines_from_markdown():
    raw = SOURCE.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(raw):
        s = raw[i].strip()
        if not s:
            yield ("space", "")
        elif s.startswith("# "):
            yield ("title", clean(s[2:]))
        elif s.startswith("## "):
            yield ("heading", clean(s[3:]))
        elif s.startswith("| "):
            rows = []
            while i < len(raw) and raw[i].strip().startswith("|"):
                cells = [clean(x) for x in raw[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", x) for x in cells): rows.append(cells)
                i += 1
            i -= 1
            if rows:
                head = rows[0]
                for row in rows[1:]:
                    yield ("table", "  |  ".join(f"{h}: {v}" for h, v in zip(head, row)))
        elif s.startswith("- "):
            yield ("bullet", "• " + clean(s[2:]))
        else:
            yield ("body", clean(s))
        i += 1


def main():
    fig = None; ax = None; y = 0; page = 0
    pdf = PdfPages(OUTPUT)
    def new_page():
        nonlocal fig, ax, y, page
        if fig is not None:
            pdf.savefig(fig); plt.close(fig)
        page += 1
        fig, ax = plt.subplots(figsize=(8.27, 11.69), dpi=150)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        ax.add_patch(plt.Rectangle((0, .955), 1, .045, color="#1F4E79"))
        ax.text(.06, .973, "UVG  •  LABORATORIO 12  •  OBSERVATORIO DE TURISMO", fontsize=8,
                color="white", va="center", fontweight="bold")
        ax.text(.06, .032, "Diseño y comparación  |  8 de noviembre de 2026", fontsize=7, color="#607080")
        ax.text(.94, .032, str(page), fontsize=7, color="#607080", ha="right")
        y = .92
    new_page()
    for kind, content in lines_from_markdown():
        if kind == "space": y -= .009; continue
        size = 17 if kind == "title" else 12 if kind == "heading" else 7.5 if kind == "table" else 8.2
        width = 46 if kind == "title" else 82 if kind == "heading" else 102 if kind == "table" else 108
        wrapped = textwrap.wrap(content, width=width, break_long_words=False, break_on_hyphens=False) or [""]
        lineheight = .018 if kind in ("title", "heading") else .0147
        extra = .013 if kind in ("title", "heading") else .006 if kind == "table" else .004
        need = len(wrapped) * lineheight + extra
        if y - need < .065: new_page()
        color = "#1F4E79" if kind in ("title", "heading") else "#222A30"
        for line in wrapped:
            ax.text(.06, y, line, fontsize=size, color=color, va="top",
                    fontweight="bold" if kind in ("title", "heading") else "normal")
            y -= lineheight
        y -= extra
    pdf.savefig(fig); plt.close(fig)
    avance = "Evidencia del avance (5 nov): V1-V3 y su filtrado cruzado."
    final = "Versión final abierta en Power BI Desktop 2.159.1231.0 (8 nov), vista inicial de la página."
    for filename, caption, note in [
        ("01_vista_inicial.png", "Captura 01 · Power BI: vista inicial del avance", avance),
        ("02_clic_Estados_Unidos_en_V2.png", "Captura 02 · Clic en Estados Unidos en V2 (avance)", avance),
        ("03_clic_2020_en_V3.png", "Captura 03 · Clic en 2020 en V3; V1 a nivel de mes (avance)", avance),
        ("10_final_p1_panorama.png", "Captura 10 · Final: 1 · Panorama (V1-V3)", final),
        ("11_final_p2_detalle_2025.png", "Captura 11 · Final: 2 · Detalle mensual (V4)", final),
        ("12_final_p3_calendario_mercados.png", "Captura 12 · Final: 3 · Calendario y mercados (V5-V7)", final),
        ("13_final_p4_pronosticos.png", "Captura 13 · Final: 4 · Pronósticos (V8, V8b, V9, V10)", final)]:
        path = DOCS / "capturas" / filename
        if path.exists():
            fig, ax = plt.subplots(figsize=(8.27, 11.69), dpi=150)
            ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
            ax.text(.06, .96, caption, transform=ax.transAxes, fontsize=12, color="#1F4E79", fontweight="bold", va="top")
            panel = fig.add_axes([.05, .22, .90, .62])
            panel.imshow(imread(path)); panel.axis("off")
            ax.text(.06, .12, note,
                    transform=ax.transAxes, fontsize=8, color="#607080")
            pdf.savefig(fig); plt.close(fig)
    pdf.close()
    print(OUTPUT)


if __name__ == "__main__": main()
