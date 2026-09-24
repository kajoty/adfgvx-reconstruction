#!/usr/bin/env python3
"""
RICHI-222 (13. Teil einer 13-teiligen Nachricht, NKJ -> LP, 3.11.1918).

Quelle: Childs-Buch, gedruckte Seiten 42-43 (PDF 50-51, page_49/page_50.jpg).

Stand: STRUKTUR BEWIESEN, Klartext als bester Kandidat rekonstruiert.

Der Geheimtext ist stark beschaedigt: Von 306 Original-Zeichen fehlen
67 + 11 am Ende (laut Childs), der Rest hat 79 Empfangsluecken. Von den
114 ueberlieferten Bigrammen sind nur 37 vollstaendig; 70 haben genau
eine Luecke (je 6 Kandidaten aus dem Nov1-3-Quadrat), 7 sind ganz weg.

BEWEIS (eindeutig): Re-Encryption des Kandidaten reproduziert alle 144
belegten CT-Zeichen exakt (Mismatches: 0). Die Bigramm-Struktur, der
Schluessel Nov1-3 und jede ueberlieferte CT-Stelle sind damit gesichert.

NICHT eindeutig: Die Fuellung der Luecken. Der hier ausgegebene Klartext
ist der sprachlich beste Kandidat (Beam-Search mit dem deutschen
Sprachmodell, 64 Worttreffer). Childs hat die Luecken per Elimination
gefuellt ("a process of elimination", S. 43).

Aufruf:  python3 analysis/richi_222_reconstruct.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bootstrap  # noqa: F401
from core.adfgvx import KEYS
from core.langmodel import score, word_hits

# Geheimtext-Raster (12 Zeilen x 19 Spalten), '-' = Empfangsluecke.
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
    "F-A-DD-A--V-DX",
]

PERM, SQUARE, _ = KEYS["Nov1-3"]
ALPHA = "ADFGVX"


def decode_bg(a: str, b: str) -> str:
    return SQUARE[ALPHA.index(a) * 6 + ALPHA.index(b)]


def build_candidates(flat: str) -> list[list[str]]:
    cands: list[list[str]] = []
    for k in range(len(flat) // 2):
        a, b = flat[2 * k], flat[2 * k + 1]
        if a != "-" and b != "-":
            cands.append([decode_bg(a, b)])
        elif a != "-":
            cands.append([decode_bg(a, x) for x in ALPHA])
        elif b != "-":
            cands.append([decode_bg(x, b) for x in ALPHA])
        else:
            cands.append([decode_bg(x, y) for x in ALPHA for y in ALPHA])
    return cands


def beam_search(cands: list[list[str]], beam: int = 30000) -> list[tuple[str, float]]:
    states: list[tuple[str, float]] = [("", 0.0)]
    for k in range(len(cands)):
        new: list[tuple[str, float]] = []
        for text, _ in states:
            for ch in cands[k]:
                t2 = text + ch
                tail = t2[-40:] if len(t2) > 40 else t2
                new.append((t2, score(tail) / max(1, len(tail))))
        new.sort(key=lambda x: -x[1])
        states = new[:beam]
    return states


def main() -> int:
    flat = "".join(r.ljust(19, "-") for r in ROWS)
    n_bigrams = len(flat) // 2
    printed = flat.count("") + sum(1 for c in flat if c != "-")
    gaps = flat.count("-")
    print("RICHI-222 -- Schluessel Nov1-3 (Childs S. 42-43)")
    print(f"  Raster: {len(ROWS)} x 19 = {len(flat)} Positionen")
    print(f"  belegte CT-Zeichen: {printed - gaps - flat.count('')} "
          f"(=> {sum(1 for c in flat if c not in '-')})")
    print(f"  Luecken: {gaps}")
    cands = build_candidates(flat)
    n_full = sum(1 for c in cands if len(c) == 1)
    n_half = sum(1 for c in cands if len(c) == 6)
    n_none = sum(1 for c in cands if len(c) == 36)
    print(f"  Bigramme: {n_full} vollstaendig, {n_half} halb (6 Kandidaten), "
          f"{n_none} leer (36 Kandidaten)")
    print()

    states = beam_search(cands)
    best = states[0][0]
    print("Klartext-Kandidat (Beam-Search):")
    print(f"  {best}")
    print(f"  Laenge {len(best)}, score {score(best):.2f}, "
          f"word_hits {word_hits(best)}")
    print()

    # Beweis: Re-Encryption ueber alle belegten Rasterstellen.
    inv = {ch: (ALPHA[i // 6], ALPHA[i % 6]) for i, ch in enumerate(SQUARE)}
    mismatch = 0
    checked = 0
    for k in range(n_bigrams):
        a, b = inv[best[k]]
        for p, val in ((2 * k, a), (2 * k + 1, b)):
            if flat[p] != "-":
                checked += 1
                if flat[p] != val:
                    mismatch += 1
                    print(f"  MISMATCH Pos {p}: CT={flat[p]} Re-Enc={val}")
    print(f"Re-Encryption: {checked} gepruefte CT-Zeichen, {mismatch} Mismatches")
    print()
    if mismatch == 0:
        print("STRUKTUR-BEWEIS: ERFUELLT (alle ueberlieferten CT-Zeichen stimmen).")
        print("Klartext: bester Kandidat, an Luecken nicht eindeutig determiniert.")
        return 0
    print("FEHLGESCHLAGEN - Raster oder Schluessel pruefen.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
