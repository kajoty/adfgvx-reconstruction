#!/usr/bin/env python3
"""
Substitutionsloeser: Bei bekanntem Transpositionsschluessel das Quadrat
per Simulated Annealing finden.

Nach der Ruecktransposition liegen die Bigramme in Klartextreihenfolge vor.
Gesucht: Zuordnung der 36 Bigramme zu 36 Klartextzeichen.

Verfahren: SA ueber die Quadrat-Permutation, bewertet mit der gemeinsamen
Fitness (Sprachmodell + Worttreffer, siehe core/fitness.py).

Wichtig (Lehre aus dem alten Solver):
  * Die Zuordnung Seite -> Schluessel steht NUR in data/solutions.py.
    Frueher stand hier fest KEYS["Nov7-9"] - das ist der Schluessel fuer
    164a/164b/171, NICHT fuer 105. Mit dem falschen Schluessel kann der
    Solver nie konvergieren.
  * Feste Iterationszahlen (10 x 60000) liessen den Solver minutenlang
    laufen. Jetzt gibt es ein Zeitbudget und einen Konvergenz-Abbruch.
"""

from __future__ import annotations

import random

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, clean, substitute, untranspose
from core.fitness import fitness as _fitness, fitness_parts
from solvers.base import Budget, SolverResult, check_solution, resolve_case


def decrypt_sq(bigrams: str, square: str) -> str:
    return "".join(
        square[ALPHA.index(bigrams[i]) * 6 + ALPHA.index(bigrams[i + 1])]
        for i in range(0, len(bigrams) - 1, 2)
    )


def solve_sub(ct: str, perm: list[int], seconds: float = 60.0,
              restarts: int = 0, seed: int = 0,
              verbose: bool = False) -> SolverResult:
    """SA ueber das Quadrat bei fester Permutation.

    Laeuft hoechstens ``seconds`` Sekunden und bricht ab, wenn sich der
    beste Wert 20000 Iterationen lang nicht verbessert hat.
    """
    if restarts <= 0:
        restarts = 20
    bigrams = untranspose(clean(ct), perm)
    rng = random.Random(seed)
    budget = Budget(max_seconds=seconds, patience=20000)

    best = SolverResult(name="sub_solver", perm=list(perm))
    best_fit = -1e18
    best_sq = list(FULL)

    for r in range(restarts):
        if budget.should_stop():
            break
        square = list(FULL)
        rng.shuffle(square)
        cur = _fitness(decrypt_sq(bigrams, "".join(square)))
        temp = 4.0
        while not budget.should_stop():
            i, j = rng.randrange(36), rng.randrange(36)
            if i == j:
                continue
            square[i], square[j] = square[j], square[i]
            sc = _fitness(decrypt_sq(bigrams, "".join(square)))
            budget.tick(sc)
            if sc >= cur or rng.random() < pow(2.718281828, (sc - cur) / temp):
                cur = sc
                if sc > best_fit:
                    best_fit = sc
                    best_sq = square[:]
            else:
                square[i], square[j] = square[j], square[i]
            temp *= 0.99997
            if temp < 0.05:
                temp = 0.05
        if verbose:
            print(f"  restart {r}: {cur:.3f} (best {best_fit:.3f})")

    sq = "".join(best_sq)
    pt = decrypt_sq(bigrams, sq)
    sc, wh, fit = fitness_parts(pt)
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

    ap = argparse.ArgumentParser(description="ADFGVX-Solver: sub_solver")
    ap.add_argument("--page", default="105")
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--restarts", type=int, default=0)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    from core.adfgvx import KEYS
    from data.solutions import SOLVED

    seconds = 10.0 if args.quick else args.seconds
    ct, perm_true, sq_true, pt_true, n = resolve_case(args.page, 0)
    key_name = SOLVED[args.page][0]
    perm = list(KEYS[key_name][0])

    print(f"Seite {args.page} ({len(ct)} Zeichen), Transposition {key_name}, "
          f"Quadrat unbekannt, Zeitbudget {seconds:.0f}s")
    print(f"Referenz: score={_fitness(pt_true):.3f} "
          f"hits={fitness_parts(pt_true)[1]}")

    res = solve_sub(ct, perm, seconds=seconds, restarts=args.restarts,
                    seed=args.seed, verbose=args.verbose)
    res.page = args.page
    res.n = n
    solved, why = check_solution(res.perm, res.square, res.plaintext,
                                 perm_true, sq_true, pt_true)
    res.solved = solved
    res.note = why
    print()
    print(res.summary())
    print(f"\nQuadrat korrekt? {res.square == sq_true}")


if __name__ == "__main__":
    main()
