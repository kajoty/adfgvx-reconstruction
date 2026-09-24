"""Ordnet die JPG-Dateien in docs/childs_pages/ den PDF-Seiten zu.

Rendert jede PDF-Seite mit PyMuPDF und vergleicht sie per normalisierter
Graustufen-Matrix (Naechster-Nachbar) mit den JPG-Dateien.
"""
from __future__ import annotations

from pathlib import Path

import pymupdf
from PIL import Image

DOCS = Path(__file__).resolve().parent.parent / "docs"
PDF = DOCS / "childs_book.pdf"
PAGES = DOCS / "childs_pages"

W, H = 64, 82


def vec(img: Image.Image) -> list[float]:
    g = img.convert("L").resize((W, H))
    px = list(g.get_flattened_data())
    avg = sum(px) / len(px)
    sd = (sum((p - avg) ** 2 for p in px) / len(px)) ** 0.5 or 1.0
    return [(p - avg) / sd for p in px]


def dist(a: list[float], b: list[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def main() -> None:
    doc = pymupdf.open(str(PDF))
    pdf_vecs: list[tuple[int, list[float]]] = []
    for i in range(doc.page_count):
        pix = doc[i].get_pixmap(dpi=72, colorspace=pymupdf.csGRAY)
        im = Image.frombytes("L", (pix.width, pix.height), pix.samples)
        pdf_vecs.append((i + 1, vec(im)))
    print(f"PDF-Seiten: {len(pdf_vecs)}")

    print("\nJPG -> PDF-Seite (bester Treffer, Abstand):")
    for j in sorted(PAGES.glob("page_*.jpg")):
        v = vec(Image.open(j))
        ranked = sorted(((dist(v, pv), p) for p, pv in pdf_vecs))
        best = ranked[:3]
        s = ", ".join(f"p{p}({d:.0f})" for d, p in best)
        print(f"  {j.name}: {s}")


if __name__ == "__main__":
    main()
