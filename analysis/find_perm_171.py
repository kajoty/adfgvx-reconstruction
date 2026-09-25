#!/usr/bin/env python3
"""Sucht die korrekte Permutation fuer Seite 171 (Quadrat Nov7-9 gegeben).

Ansatz: Hill-Climbing / SA auf der Spaltenreihenfolge, bewertet mit dem
Sprachmodell-Score. Wenn die KEYS-Permutation falsch ist, sollte dieser
Solver eine bessere finden.
"""
from __future__ import annotations

import os as _os, sys as _sys, random
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import clean, make_square, KEYS, ALPHA, substitute
from core import langmodel
from data.corpus import CORPUS
from data.solutions import SOLVED


def untranspose_order(ct: str, order: list[int]) -> str:
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


def main() -> None:
    page = "171"
    key = SOLVED[page][0]
    perm, sub, _ = KEYS[key]
    sq = make_square(sub)
    ct = clean(CORPUS[page])
    n = len(perm)
    rng = random.Random(42)

    def evaluate(order: list[int]) -> float:
        bgs = untranspose_order(ct, order)
        pt = substitute(bgs, sq)
        return langmodel.score(pt)

    # Start: KEYS-Permutation
    start = sorted(range(n), key=lambda c: perm[c])
    print(f"Start (KEYS): score={evaluate(start):.2f}")

    best_order = start[:]
    best_score = evaluate(start)
    for restart in range(30):
        order = start[:] if restart == 0 else rng.sample(range(n), n)
        cur = evaluate(order)
        T = 5.0
        for it in range(20000):
            T = max(0.05, T * 0.9997)
            i, j = rng.sample(range(n), 2)
            order[i], order[j] = order[j], order[i]
            new = evaluate(order)
            if new > cur or rng.random() < pow(2.718, (new - cur) / T):
                cur = new
            else:
                order[i], order[j] = order[j], order[i]
            if cur > best_score:
                best_score = cur
                best_order = order[:]
        print(f"  restart {restart:2d}: best={best_score:7.2f}")
    bgs = untranspose_order(ct, best_order)
    pt = substitute(bgs, sq)
    print(f"\nBEST score={best_score:.2f}")
    print(f"  order={best_order}")
    print(f"  pt={pt[:70]}")
    print(f"SOLL={SOLVED[page][1][:70]}")


if __name__ == "__main__":
    main()
