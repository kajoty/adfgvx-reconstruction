#!/usr/bin/env python3
"""Sucht die korrekte Permutation fuer Seite 171 mit Fitness (score + word_hits).

Verfeinerung von find_perm_171.py: nutzt core.fitness und mehr Restarts.
"""
from __future__ import annotations

import os as _os, sys as _sys, random
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import clean, make_square, KEYS, ALPHA, substitute
from core import langmodel
from core.fitness import fitness, fitness_parts
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
    rng = random.Random(7)

    def evaluate(order: list[int]) -> float:
        bgs = untranspose_order(ct, order)
        pt = substitute(bgs, sq)
        return fitness(pt)

    start = sorted(range(n), key=lambda c: perm[c])
    print(f"Start (KEYS): {fitness_parts(substitute(untranspose_order(ct, start), sq))}")

    best_order = start[:]
    best_score = evaluate(start)
    for restart in range(60):
        order = start[:] if restart == 0 else rng.sample(range(n), n)
        cur = evaluate(order)
        T = 8.0
        for it in range(30000):
            T = max(0.02, T * 0.9998)
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
        if restart % 10 == 0:
            print(f"  restart {restart:2d}: best={best_score:7.2f}")
    bgs = untranspose_order(ct, best_order)
    pt = substitute(bgs, sq)
    print(f"\nBEST fitness={best_score:.2f} parts={fitness_parts(pt)}")
    print(f"  order={best_order}")
    print(f"  pt={pt[:80]}")
    print(f"SOLL={SOLVED[page][1][:80]}")


if __name__ == "__main__":
    main()
