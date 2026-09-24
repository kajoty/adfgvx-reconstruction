#!/usr/bin/env python3
"""Rendert PDF-Seite 51 (Childs' Klartext-Rekonstruktion von RICHI-222)."""
import pymupdf

doc = pymupdf.open("docs/childs_book.pdf")
page = doc[50]  # PDF-Seite 51
mat = pymupdf.Matrix(3, 3)
pix = page.get_pixmap(matrix=mat)
pix.save("/tmp/pdf_p51_full.png")
print("Seite 51:", pix.width, "x", pix.height, "-> /tmp/pdf_p51_full.png")
