#!/usr/bin/env python3
"""
Substitutionsloeser: Bei bekanntem Transpositionsschluessel das Quadrat
per Simulated Annealing finden.

Nach der Ruecktransposition liegen die Bigramme in Klartextreihenfolge vor.
Gesucht: Zuordnung der 36 Bigramme zu 36 Klartextzeichen.

Verfahren: SA ueber die Quadrat-Permutation, bewertet mit langmodel.score.
Zusaetzlich: Worttreffer-Bonus, damit echte Woerter bevorzugt werden.
"""

from __future__ import annotations

import random

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, clean, untranspose
from core import langmodel


def decrypt_sq(bigrams: str, square: str) -> str:
    return "".join(
        square[ALPHA.index(bigrams[i]) * 6 + ALPHA.index(bigrams[i + 1])]
        for i in range(0, len(bigrams) - 1, 2)
    )


def fitness(text: str) -> float:
    """Sprachmodell-Score plus Bonus fuer echte Woerter."""
    return langmodel.score(text) + 0.15 * langmodel.word_hits(text)


def solve_sub(ct: str, perm: list[int], restarts: int = 20,
              iterations: int = 100000, seed: int = 0,
              verbose: bool = False) -> tuple[float, str, str]:
    bigrams = untranspose(clean(ct), perm)
    rng = random.Random(seed)
    best_overall = (-1e18, None, None)

    for r in range(restarts):
        square = list(FULL)
        rng.shuffle(square)
        cur = fitness(decrypt_sq(bigrams, "".join(square)))
        best_local = cur
        best_sq = square[:]
        temp = 4.0
        for _ in range(iterations):
            i, j = rng.randrange(36), rng.randrange(36)
            if i == j:
                continue
            square[i], square[j] = square[j], square[i]
            sc = fitness(decrypt_sq(bigrams, "".join(square)))
            if sc >= cur or rng.random() < pow(2.718281828, (sc - cur) / temp):
                cur = sc
                if sc > best_local:
                    best_local, best_sq = sc, square[:]
            else:
                square[i], square[j] = square[j], square[i]
            temp *= 0.99997
            if temp < 0.05:
                temp = 0.05
        if best_local > best_overall[0]:
            sq = "".join(best_sq)
            best_overall = (best_local, sq, decrypt_sq(bigrams, sq))
        if verbose:
            print(f"  restart {r}: {best_local:.3f}")

    return best_overall


def main() -> None:
    from core.adfgvx import KEYS
    from data.corpus import CORPUS
    from data.solutions import SOLVED

    # WICHTIG: Die Zuordnung Seite -> Schluessel steht NUR in solutions.py.
    # Frueher stand hier KEYS["Nov7-9"] — das ist der Schluessel fuer 164a/164b/171,
    # NICHT fuer 105. Mit dem falschen Schluessel kann der Solver nie konvergieren.
    page = "105"
    key_name = SOLVED[page][0]
    ct = clean(CORPUS[page])
    perm = KEYS[key_name][0]
    sq_true = KEYS[key_name][1]
    pt_true = SOLVED[page][1]

    print(f"Seite {page} ({len(ct)} Zeichen), Transposition {key_name}, "
          f"Quadrat unbekannt")
    print(f"Referenz-Score (bekanntes Quadrat): "
          f"{langmodel.score(pt_true):.3f}  hits={langmodel.word_hits(pt_true)}")
    print()
    sc, sq, pt = solve_sub(ct, perm, restarts=10, iterations=60000, seed=1,
                           verbose=True)
    print()
    print(f"BEST score={sc:.3f}  hits={langmodel.word_hits(pt)}")
    print(f"Quadrat: {sq}")
    print(f"Klartext: {pt}")
    print()
    print(f"Quadrat korrekt? {sq == sq_true}")


if __name__ == "__main__":
    main()
