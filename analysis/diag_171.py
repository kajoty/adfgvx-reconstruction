#!/usr/bin/env python3
"""Diagnose: Warum entschluesselt kein Schluessel Seite 171?

Prueft systematisch:
  1. Konfliktzahl fuer alle n (mit Nov7-9-Quadrat)
  2. Identity-Permutation fuer alle n
  3. Ob die Konfliktzahl 0 wirklich Korrektheit bedeutet
"""
from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from collections import defaultdict

from core.adfgvx import clean, make_square, KEYS, ALPHA, substitute
from core import langmodel
from data.corpus import CORPUS
from data.solutions import SOLVED


def untranspose_order(ct: str, order: list[int]) -> str:
    """Liest Spalten in gegebener Reihenfolge aus (order[k] = k-te Spalte)."""
    n = len(order)
    L = len(ct)
    rows = (L + n - 1) // n
    rest = L % n or n
    collen = [rows if i < rest else rows - 1 for i in range(n)]
    cols: list[str | None] = [None] * n
    pos = 0
    for c in order:
        cols[c] = ct[pos:pos + collen[c]]
        pos += collen[c]
    return "".join(
        cols[c][r] for r in range(rows) for c in range(n) if r < len(cols[c])  # type: ignore
    )


def conflicts(bgs: str, sq: str) -> int:
    m: dict[str, set[str]] = defaultdict(set)
    for i in range(0, len(bgs) - 1, 2):
        bg = bgs[i:i + 2]
        ch = sq[ALPHA.index(bg[0]) * 6 + ALPHA.index(bg[1])]
        m[bg].add(ch)
    return sum(len(v) - 1 for v in m.values())


def main() -> None:
    page = "171"
    key = SOLVED[page][0]
    perm, sub, _ = KEYS[key]
    sq = make_square(sub)
    ct = clean(CORPUS[page])
    L = len(ct)
    print(f"Seite {page}: key={key} len(ct)={L} len(perm)={len(perm)}")
    print()

    print("=== Identity-Permutation fuer alle n ===")
    for n in range(10, 30):
        bgs = untranspose_order(ct, list(range(n)))
        pt = substitute(bgs, sq)
        sc = langmodel.score(pt)
        c = conflicts(bgs, sq)
        print(f"  n={n:2d} score={sc:7.2f} conflicts={c:3d}  {pt[:40]}")

    print()
    print("=== Nov7-9-Permutation (Rang) ===")
    order = sorted(range(len(perm)), key=lambda c: perm[c])
    bgs = untranspose_order(ct, order)
    pt = substitute(bgs, sq)
    print(f"  score={langmodel.score(pt):7.2f} conflicts={conflicts(bgs, sq)}")
    print(f"  {pt[:60]}")

    print()
    print("=== Konfliktzahl fuer alle KEYS-Perms (n=len(perm)) ===")
    for name, (p, s, _c) in KEYS.items():
        sq2 = make_square(s)
        o = sorted(range(len(p)), key=lambda c: p[c])
        bgs = untranspose_order(ct, o)
        c = conflicts(bgs, sq2)
        pt = substitute(bgs, sq2)
        sc = langmodel.score(pt)
        print(f"  {name:12s} n={len(p):2d} conflicts={c:3d} score={sc:7.2f}")


if __name__ == "__main__":
    main()
