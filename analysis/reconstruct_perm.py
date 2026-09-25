#!/usr/bin/env python3
"""Rekonstruiert die Permutation aus dem SOLL-Klartext (mit Toleranz).

Idee: Wenn der SOLL-Klartext (fast) korrekt ist, dann muss es eine
Spaltenreihenfolge geben, die den CT in genau diesen Klartext ueberfuehrt.
Wir suchen sie, indem wir fuer jede Spalte pruefen, welcher CT-Block zu
welchem Klartext-Block passt.
"""
from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import clean, make_square, KEYS, ALPHA
from data.corpus import CORPUS
from data.solutions import SOLVED


def bigrams_of(pt: str, sq: str) -> str:
    rev = {ch: ALPHA[i // 6] + ALPHA[i % 6] for i, ch in enumerate(sq)}
    return "".join(rev.get(ch, "??") for ch in pt)


def main() -> None:
    for page in ["100", "105", "146", "171"]:
        key = SOLVED[page][0]
        perm, sub, _ = KEYS[key]
        sq = make_square(sub)
        ct = clean(CORPUS[page])
        pt = SOLVED[page][1]
        n = len(perm)
        L = len(ct)
        bgs = bigrams_of(pt, sq)
        print(f"=== Seite {page} (key {key}, n={n}) ===")
        print(f"  len(pt)={len(pt)} len(bgs)={len(bgs)} len(ct)={L}")
        # Spaltenlaengen
        rows = (L + n - 1) // n
        rest = L % n or n
        collen = [rows if i < rest else rows - 1 for i in range(n)]
        # CT-Bloecke in Auslesereihenfolge
        pos = 0
        blocks = []
        for c in range(n):
            blocks.append(ct[pos:pos + collen[c]])
            pos += collen[c]
        # Klartext-Bigramm-Spalten (Spalte c hat collen[c] Zeichen)
        bpos = 0
        bcols = []
        for c in range(n):
            bcols.append(bgs[bpos:bpos + collen[c]])
            bpos += collen[c]
        # Zuordnung: welcher CT-Block passt zu welcher Klartext-Spalte?
        # Toleranz: Hamming-Distanz
        mapping = {}
        for bi, blk in enumerate(blocks):
            best = None
            bestd = 999
            for ci, bc in enumerate(bcols):
                d = sum(1 for a, b in zip(blk, bc) if a != b)
                if d < bestd:
                    bestd = d
                    best = ci
            mapping[bi] = (best, bestd)
        print(f"  Zuordnung (Auslesepos -> (Spalte, Hamming)):")
        for bi in range(n):
            print(f"    {bi:2d} -> {mapping[bi]}")
        # Wie viele eindeutig?
        cols_used = [mapping[bi][0] for bi in range(n)]
        print(f"  eindeutig? {len(set(cols_used)) == n}")
        print()


if __name__ == "__main__":
    main()
