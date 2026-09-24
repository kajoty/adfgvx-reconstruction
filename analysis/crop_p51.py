#!/usr/bin/env python3
"""Croppt die Kandidaten-Tabelle von page_51 (Childs' Reparatur)."""
import pymupdf

doc = pymupdf.open("docs/childs_book.pdf")
page = doc[50]  # PDF-Seite 51
# Die Tabelle beginnt nach dem Textblock (~40% Hoehe) bis ~75%.
mat = pymupdf.Matrix(6, 6)
rect = pymupdf.Rect(60, 260, 570, 480)  # Punktkoordinaten der Tabelle
pix = page.get_pixmap(matrix=mat, clip=rect)
pix.save("/tmp/p51_table.png")
print("Tabelle:", pix.width, "x", pix.height, "-> /tmp/p51_table.png")
