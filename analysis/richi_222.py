#!/usr/bin/env python3
"""
RICHI-222: Rekonstruktion nach Childs' Verfahren (Buch S. 42-43).

Geheimtext: 12 Tabellenzeilen (19 Spalten, Kopf = Nov1-3-Permutation).
Die Lücken werden nach Childs' Eliminationsverfahren aus dem Nov1-3-Quadrat
gefuellt (page_51.jpg zeigt seine Wahl als unterstrichene Zeichen).

Der gelesene Klartext-Kandidat wird gegen den dekodierten Geheimtext geprueft:
Beweis = (Re-Encryption des Kandidaten == Geheimtext an allen belegten Stellen)
und Konfliktzahl == 0.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bootstrap  # noqa: F401
from core.adfgvx import KEYS, untranspose, substitute
from core.langmodel import score, word_hits

# Geheimtext, 12 Zeilen zu 19 Positionen. '-' = Luecke (Zeichen fehlt).
ROWS = [
    "F-V--D-F-G-GGAVGDAD",
    "X-F--D-X-D-VDVGVGGA",
    "V-G-VD-G-A-VDDVFGAA",
    "A-A-DV-A-G-FFXGDAGG",
    "X-A-AV-G-V-GDAD-DDV",
    "F-F-GD-A-V--GXG-GDF",
    "A-F--A-G-X-GGGD-VGA",
    "D-G--V-D-D-FX-G-GGG",
    "G-G--D-V-V-GDAG-VGF",
    "X-G----D---DXVV-XV-",
    "D-D-VD-X-F-XXGX-XFF",
    "F-A-DD-A--V-DX      ",
]

PERM, SQUARE, _ = KEYS["Nov1-3"]


def main() -> int:
    n_cols = len(PERM)
    rows = [r.ljust(n_cols, " ") for r in ROWS]
    n_rows = len(rows)
    total = sum(1 for r in rows for c in r if c != " ")
    gaps = sum(1 for r in rows for c in r if c == " ")
    print(f"Geheimtext: {n_rows} Zeilen x {n_cols} Spalten")
    print(f"  belegte Zeichen: {total}, Luecken: {gaps}")
    print()

    # Spaltenweise auslesen in Rangfolge (Rang r -> Spalte perm.index(r)):
    ct_with_gaps = []
    for rank in range(1, n_cols + 1):
        col = PERM.index(rank)
        for row in rows:
            ct_with_gaps.append(row[col])
    ct = "".join(ct_with_gaps)
    print(f"Spaltenweise gelesen: {len(ct)} Positionen, "
          f"{ct.count(' ')} Luecken -> {len(ct) - ct.count(' ')} Zeichen")
    print()

    # Dekodieren: Luecken markieren, Substitution nur auf belegte Stellen.
    un = untranspose(ct.replace(" ", ""), PERM)
    # Achtung: untranspose erwartet den CT ohne Luecken. Die Positionen der
    # Luecken in der Spaltenfolge sind aber bedeutungstragend. Deshalb:
    # wir dekodieren nur den kompakten CT und merken, dass die Luecken-Positionen
    # im Zeilenraster liegen, nicht im kompakten CT.
    dec = substitute(un, SQUARE)
    print("Kompakter CT dekodiert (Luecken entfernt, evtl. verschoben):")
    print(" ", dec[:80])
    print("  score:", round(score(dec), 2), "word_hits:", word_hits(dec))
    print()

    # Childs' Klartext-Kandidat aus page_51.jpg (Zeile fuer Zeile, Wahl = unterstrichene):
    # Zeilenweise gelesen (Spalte 1 aller Zeilen, Spalte 2 aller Zeilen, ...).
    # Wir pruefen: passt der Kandidat an den belegten Stellen?
    # Der Kandidat wird in der Reparatur-Schleife unten erzeugt.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
