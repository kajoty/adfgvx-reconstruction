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

from core.adfgvx import ALPHA, FULL, clean, untranspose
from core.fitness import fitness as _fitness, fitness_parts
from solvers.base import Budget, SolverResult, check_solution, resolve_case


def decrypt_sq(bigrams: str, square: str) -> str:
    return "".join(
        square[ALPHA.index(bigrams[i]) * 6 + ALPHA.index(bigrams[i + 1])]
        for i in range(0, len(bigrams) - 1, 2)
    )


def solve(ct: str, n: int, seconds: float = 60.0, restarts: int = 0,
          seed: int = 0, verbose: bool = False) -> SolverResult:
    """SA ueber Transposition + Substitution.

    Laeuft hoechstens ``seconds`` Sekunden. Bricht ab, wenn sich der beste
    Wert 30000 Iterationen lang nicht verbessert hat.
    """
    if restarts <= 0:
        restarts = 10
    rng = random.Random(seed)
    budget = Budget(max_seconds=seconds, patience=30000)

    best = SolverResult(name="blind_solver")
    best_fit = -1e18
    best_perm = list(range(n))
    best_sq = list(FULL)

    for r in range(restarts):
        if budget.should_stop():
            break
        perm = list(range(n))
        rng.shuffle(perm)
        square = list(FULL)
        rng.shuffle(square)
        cur = _fitness(decrypt_sq(untranspose(ct, perm), "".join(square)))
        temp = 4.0
        while not budget.should_stop():
            if rng.random() < 0.5:
                # Transposition: zwei Raenge tauschen
                i, j = rng.randrange(n), rng.randrange(n)
                if i == j:
                    continue
                perm[i], perm[j] = perm[j], perm[i]
                sc = _fitness(decrypt_sq(untranspose(ct, perm), "".join(square)))
                budget.tick(sc)
                if sc >= cur or rng.random() < pow(2.718281828, (sc - cur) / temp):
                    cur = sc
                    if sc > best_fit:
                        best_fit = sc
                        best_perm = perm[:]
                        best_sq = square[:]
                else:
                    perm[i], perm[j] = perm[j], perm[i]
            else:
                # Substitution: zwei Quadratpositionen tauschen
                i, j = rng.randrange(36), rng.randrange(36)
                if i == j:
                    continue
                square[i], square[j] = square[j], square[i]
                sc = _fitness(decrypt_sq(untranspose(ct, perm), "".join(square)))
                budget.tick(sc)
                if sc >= cur or rng.random() < pow(2.718281828, (sc - cur) / temp):
                    cur = sc
                    if sc > best_fit:
                        best_fit = sc
                        best_perm = perm[:]
                        best_sq = square[:]
                else:
                    square[i], square[j] = square[j], square[i]
            temp *= 0.99997
            if temp < 0.05:
                temp = 0.05
        if verbose:
            print(f"  restart {r}: {cur:.3f} (best {best_fit:.3f})")

    sq = "".join(best_sq)
    pt = decrypt_sq(untranspose(ct, best_perm), sq)
    sc, wh, fit = fitness_parts(pt)
    best.perm = best_perm
    best.square = sq
    best.plaintext = pt
    best.score = sc
    best.hits = wh
    best.fitness = fit
    best.seconds = budget.elapsed
    best.iterations = budget.iters
    return best


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="ADFGVX-Solver: blind_solver")
    ap.add_argument("--page", default="100")
    ap.add_argument("--n", type=int, default=0,
                    help="Spaltenzahl (0 = aus dem Schluessel ableiten)")
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--restarts", type=int, default=0)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    seconds = 10.0 if args.quick else args.seconds
    ct, perm_true, sq_true, pt_true, n = resolve_case(args.page, args.n)
    print(f"Seite {args.page} ({len(ct)} Zeichen) - Blindtest, n={n}, "
          f"Zeitbudget {seconds:.0f}s")

    res = solve(ct, n, seconds=seconds, restarts=args.restarts,
                seed=args.seed, verbose=args.verbose)
    res.page = args.page
    res.n = n
    solved, why = check_solution(res.perm, res.square, res.plaintext,
                                 perm_true, sq_true, pt_true)
    res.solved = solved
    res.note = why
    print()
    print(res.summary())
    print(f"\nErwartet: {pt_true[:70]}")


if __name__ == "__main__":
    main()
