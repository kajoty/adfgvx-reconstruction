#!/usr/bin/env python3
"""
Gezielter Angriff auf Seite 152 (104 Zeichen = 52 Bigramme).

Ansatz:
  Stufe 1: Simulated Annealing ueber die Transpositions-Rangliste (Periode n).
  Stufe 2: Fuer jede Kandidaten-Transposition wird das Substitutionsquadrat
           per Haeufigkeitsanalyse (deutsche Buchstabenverteilung) bestimmt.

Bewertung: langmodel.score + lambda * word_hits.
"""

from __future__ import annotations

import random
import sys

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, clean
from data.corpus import CORPUS
from core import langmodel

LAMBDA = 0.15


def untranspose(ct: str, perm: list[int]) -> str:
    n = len(perm)
    order = sorted(range(n), key=lambda c: perm[c])
    L = len(ct)
    rows = (L + n - 1) // n
    rest = L % n
    if rest == 0:
        rest = n
    collen = [rows if i < rest else rows - 1 for i in range(n)]
    cols = [""] * n
    pos = 0
    for c in order:
        cols[c] = ct[pos:pos + collen[c]]
        pos += collen[c]
    return "".join(
        cols[i][r] for r in range(rows) for i in range(n) if r < len(cols[i])
    )


def decrypt_sq(bigrams: str, square: str) -> str:
    return "".join(
        square[ALPHA.index(bigrams[i]) * 6 + ALPHA.index(bigrams[i + 1])]
        for i in range(0, len(bigrams) - 1, 2)
    )


def fitness(pt: str) -> float:
    return langmodel.score(pt) + LAMBDA * langmodel.word_hits(pt)


def solve_square(bigrams: str, restarts: int = 12, iters: int = 40000,
                 seed: int = 0) -> tuple[float, str, str]:
    """SA nur ueber das Quadrat (Transposition fix)."""
    rng = random.Random(seed)
    best = (-1e18, None, None)
    for _ in range(restarts):
        sq = list(FULL)
        rng.shuffle(sq)
        cur = fitness(decrypt_sq(bigrams, "".join(sq)))
        bl = cur
        bs = sq[:]
        temp = 3.0
        for _ in range(iters):
            i, j = rng.randrange(36), rng.randrange(36)
            if i == j:
                continue
            sq[i], sq[j] = sq[j], sq[i]
            sc = fitness(decrypt_sq(bigrams, "".join(sq)))
            if sc >= cur or rng.random() < pow(2.718281828, (sc - cur) / temp):
                cur = sc
                if sc > bl:
                    bl = sc
                    bs = sq[:]
            else:
                sq[i], sq[j] = sq[j], sq[i]
            temp *= 0.9999
            if temp < 0.05:
                temp = 0.05
        if bl > best[0]:
            best = (bl, bs, decrypt_sq(bigrams, "".join(bs)))
    return best[0], "".join(best[1]), best[2]


def attack(ct: str, n: int, restarts: int = 6, iters: int = 30000,
           seed: int = 0, verbose: bool = False):
    """SA ueber Transposition; Quadrat per innerem SA."""
    rng = random.Random(seed)
    best = (-1e18, None, None, None)
    for r in range(restarts):
        perm = list(range(n))
        rng.shuffle(perm)
        bgs = untranspose(ct, perm)
        sc, sq, pt = solve_square(bgs, restarts=3, iters=8000, seed=seed + r)
        cur = sc
        bl = cur
        bp = perm[:]
        bsq = sq
        bpt = pt
        temp = 2.0
        for it in range(iters):
            i, j = rng.randrange(n), rng.randrange(n)
            if i == j:
                continue
            perm[i], perm[j] = perm[j], perm[i]
            bgs = untranspose(ct, perm)
            sc, sq, pt = solve_square(bgs, restarts=1, iters=3000,
                                      seed=seed + r * 1000 + it)
            if sc >= cur or rng.random() < pow(2.718281828, (sc - cur) / temp):
                cur = sc
                if sc > bl:
                    bl = sc
                    bp = perm[:]
                    bsq = sq
                    bpt = pt
            else:
                perm[i], perm[j] = perm[j], perm[i]
            temp *= 0.9995
            if temp < 0.1:
                temp = 0.1
        if bl > best[0]:
            best = (bl, bp, bsq, bpt)
        if verbose:
            print(f"  n={n} restart {r}: {bl:.3f} hits={langmodel.word_hits(bpt)}")
    return best


def main() -> None:
    ct = clean(CORPUS["152"])
    print(f"Seite 152: {len(ct)} Zeichen = {len(ct)//2} Bigramme")
    print(f"Lesbarkeitsschwelle: score >= -24")
    print()

    results = []
    for n in range(13, 27):
        sc, perm, sq, pt = attack(ct, n, restarts=4, iters=4000, seed=42)
        hits = langmodel.word_hits(pt)
        results.append((sc, hits, n, perm, sq, pt))
        print(f"  n={n:2}: score={sc:8.3f} hits={hits:3}  {pt[:40]}")

    results.sort(reverse=True)
    print()
    print("=" * 70)
    print("TOP-3:")
    for sc, hits, n, perm, sq, pt in results[:3]:
        print(f"  n={n} score={sc:.3f} hits={hits}")
        print(f"    PT: {pt}")
        print(f"    SQ: {sq}")
        print()


if __name__ == "__main__":
    main()
