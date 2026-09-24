#!/usr/bin/env python3
"""Rendert PDF-Seite 50 in voller Aufloesung und croppt die RICHI-222-Tabelle."""
import fitz  # pymupdf

doc = fitz.open("docs/childs_book.pdf")
page = doc[49]  # PDF-Seite 50 (0-basiert 49)
print("Seitenmasse:", page.rect)

# Erst ganze Seite in 3x Aufloesung rendern, um die Tabelle zu lokalisieren:
mat = fitz.Matrix(3, 3)
pix = page.get_pixmap(matrix=mat)
pix.save("/tmp/pdf_p50_full.png")
print("Ganzseitig:", pix.width, "x", pix.height, "-> /tmp/pdf_p50_full.png")
