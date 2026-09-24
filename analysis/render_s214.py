#!/usr/bin/env python3
"""Rendert PDF-Seiten 53-54 (Childs S. 214-215: TRUPPENVERSCHIEBUNG)."""
import pymupdf

doc = pymupdf.open("docs/childs_book.pdf")
for n in (53, 54):
    page = doc[n - 1]
    pix = page.get_pixmap(matrix=pymupdf.Matrix(3, 3))
    out = f"/tmp/childs_p{n}.png"
    pix.save(out)
    print(f"PDF-Seite {n} -> {out} ({pix.width}x{pix.height})")
