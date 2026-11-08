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
    for filename, caption in [
        ("01_vista_inicial.png", "Power BI: vista inicial del avance"),
        ("02_clic_Estados_Unidos_en_V2.png", "Power BI: clic en Estados Unidos (avance)"),
        ("03_clic_2020_en_V3.png", "Power BI: clic en 2020 (avance)")]:
        path = DOCS / "capturas" / filename
        if path.exists():
            fig, ax = plt.subplots(figsize=(8.27, 11.69), dpi=150)
            ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
            ax.text(.06, .96, caption, transform=ax.transAxes, fontsize=12, color="#1F4E79", fontweight="bold", va="top")
            panel = fig.add_axes([.05, .22, .90, .62])
            panel.imshow(imread(path)); panel.axis("off")
            ax.text(.06, .12, "Evidencia del avance; no documenta las páginas añadidas.",
                    transform=ax.transAxes, fontsize=8, color="#607080")
            pdf.savefig(fig); plt.close(fig)
    pdf.close()
    print(OUTPUT)


if __name__ == "__main__": main()
