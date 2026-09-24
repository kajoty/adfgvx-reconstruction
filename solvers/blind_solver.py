#!/usr/bin/env python3
"""
Kombinierter ADFGVX-Loeser.

Sucht gleichzeitig:
  - die Transpositions-Rangliste (Permutation der Spalten)
  - das Substitutionsquadrat (36 Zeichen)
  - optionale Einfuege-/Loeschkorrekturen im Geheimtext

Verfahren: Simulated Annealing ueber alle drei Komponenten, bewertet mit
dem deutschen Sprachmodell (langmodel.score).

Das ist der Ansatz, mit dem Lasry et al. ADFGVX-Kryptogramme loesen.
"""

from __future__ import annotations

import random

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, clean
from core import langmodel


def untranspose(ct: str, perm: list[int]) -> str:
    n = len(perm)
    length = len(ct)
    rows = (length + n - 1) // n
    rest = length % n
    if rest == 0:
        rest = n
    collen = [rows if i < rest else rows - 1 for i in range(n)]
    order = sorted(range(n), key=lambda c: perm[c])
    cols: list[str | None] = [None] * n
    pos = 0
    for c in order:
        cols[c] = ct[pos:pos + collen[c]]
        pos += collen[c]
    return "".join(
        cols[c][r]  # type: ignore[index]
        for r in range(rows)
        for c in range(n)
        if r < len(cols[c])  # type: ignore[arg-type]
    )


def decrypt_sq(bigrams: str, square: str) -> str:
    return "".join(
        square[ALPHA.index(bigrams[i]) * 6 + ALPHA.index(bigrams[i + 1])]
        for i in range(0, len(bigrams) - 1, 2)
    )


def evaluate(ct: str, perm: list[int], square: str) -> float:
    return langmodel.score(decrypt_sq(untranspose(ct, perm), square))


def solve(ct: str, n: int, restarts: int = 10, iterations: int = 120000,
          seed: int = 0, verbose: bool = False):
    """SA ueber Transposition + Substitution."""
    rng = random.Random(seed)
    best_overall = (-1e18, None, None)

    for r in range(restarts):
        perm = list(range(n))
        rng.shuffle(perm)
        square = list(FULL)
        rng.shuffle(square)
        cur = evaluate(ct, perm, "".join(square))
        best_local = cur
        best_state = (perm[:], square[:])
        temp = 4.0
        for it in range(iterations):
            if rng.random() < 0.5:
                # Transposition: zwei Raenge tauschen
                i, j = rng.randrange(n), rng.randrange(n)
                if i == j:
                    continue
                perm[i], perm[j] = perm[j], perm[i]
                sc = evaluate(ct, perm, "".join(square))
                if sc >= cur or rng.random() < pow(2.718281828, (sc - cur) / temp):
                    cur = sc
                    if sc > best_local:
                        best_local = sc
                        best_state = (perm[:], square[:])
                else:
                    perm[i], perm[j] = perm[j], perm[i]
            else:
                # Substitution: zwei Quadratpositionen tauschen
                i, j = rng.randrange(36), rng.randrange(36)
                if i == j:
                    continue
                square[i], square[j] = square[j], square[i]
                sc = evaluate(ct, perm, "".join(square))
                if sc >= cur or rng.random() < pow(2.718281828, (sc - cur) / temp):
                    cur = sc
                    if sc > best_local:
                        best_local = sc
                        best_state = (perm[:], square[:])
                else:
                    square[i], square[j] = square[j], square[i]
            temp *= 0.99997
            if temp < 0.05:
                temp = 0.05
        if best_local > best_overall[0]:
            p, sq = best_state
            best_overall = (best_local, p, "".join(sq))
        if verbose:
            print(f"  restart {r}: {best_local:.3f}")

    sc, perm, square = best_overall
    return sc, perm, square, decrypt_sq(untranspose(ct, perm), square)


def main() -> None:
    from data.corpus import CORPUS

    ct = clean(CORPUS["100"])
    print(f"Seite 100 ({len(ct)} Zeichen) - Blindtest, Periode unbekannt")
    for n in (19, 20, 21, 22):
        sc, perm, sq, pt = solve(ct, n, restarts=4, iterations=60000, seed=7)
        print(f"  n={n:2d}  score={sc:8.3f}  {pt[:55]}")


if __name__ == "__main__":
    main()
