#!/usr/bin/env python3
"""
Gezielter Angriff auf Seite 152 (104 Zeichen = 52 Bigramme).

Ansatz (v2, schnell):
  Nutzt den analytischen Solver (solvers/analytic_solver.py):
    - Quadrat per Haeufigkeitsanalyse + Hill-Climbing (Warmstart)
    - Simulated Annealing ueber die Transpositions-Permutation
  Das ist ~400x schneller als die alte SA-Variante (solve_152.py).

Ablauf:
  1. Grobe Suche ueber alle Perioden n=13..26.
  2. Feintuning der besten Kandidaten mit mehr Restarts/Iterationen.
  3. Ausgabe der Top-Kandidaten mit Quadrat und Permutation.

Aufruf:
  PYTHONPATH=. python3 analysis/solve_152_fast.py
  PYTHONPATH=. python3 analysis/solve_152_fast.py --quick   # nur Grobsuche
"""

from __future__ import annotations

import argparse
import os as _os
import sys as _sys
import time

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import clean
from core import langmodel
from data.corpus import CORPUS
from solvers.analytic_solver import solve


def coarse_search(ct: str, n_min: int = 13, n_max: int = 26,
                  restarts: int = 3, iterations: int = 300,
                  seed: int = 42) -> list[tuple]:
    """Grobe Suche ueber alle Perioden. Gibt (score, hits, n, perm, sq, pt)."""
    results = []
    for n in range(n_min, n_max + 1):
        t0 = time.time()
        sc, perm, sq, pt = solve(ct, key_len=n, restarts=restarts,
                                 iterations=iterations, seed=seed)
        hits = langmodel.word_hits(pt)
        results.append((sc, hits, n, perm, sq, pt))
        print(f"  n={n:2}: score={sc:8.3f} hits={hits:3} "
              f"({time.time()-t0:5.1f}s)  {pt[:45]}", flush=True)
    return results


def refine(ct: str, n: int, seeds: int = 6, restarts: int = 4,
           iterations: int = 800) -> tuple:
    """Feintuning einer Periode mit mehreren Seeds."""
    best = (-1e18, None, None, None)
    for seed in range(seeds):
        sc, perm, sq, pt = solve(ct, key_len=n, restarts=restarts,
                                 iterations=iterations, seed=seed)
        if sc > best[0]:
            best = (sc, perm, sq, pt)
    return best


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true",
                    help="nur Grobsuche, kein Feintuning")
    ap.add_argument("--top", type=int, default=4,
                    help="Anzahl der fein zu optimierenden Kandidaten")
    args = ap.parse_args()

    ct = clean(CORPUS["152"])
    print(f"Seite 152: {len(ct)} Zeichen = {len(ct)//2} Bigramme")
    print(f"Lesbarkeitsschwelle: score >= -24")
    print()

    print("=== GROBSUCHE (n=13..26) ===", flush=True)
    t0 = time.time()
    results = coarse_search(ct)
    print(f"Grobsuche fertig in {time.time()-t0:.1f}s")
    print()

    results.sort(reverse=True)

    if args.quick:
        print("=== TOP-5 (nur Grobsuche) ===")
        for sc, hits, n, perm, sq, pt in results[:5]:
            print(f"  n={n} score={sc:.3f} hits={hits}")
            print(f"    PT: {pt}")
        return

    print(f"=== FEINTUNING der Top-{args.top} ===", flush=True)
    refined = []
    for sc0, hits0, n, _, _, _ in results[:args.top]:
        t0 = time.time()
        sc, perm, sq, pt = refine(ct, n)
        hits = langmodel.word_hits(pt)
        refined.append((sc, hits, n, perm, sq, pt))
        print(f"  n={n:2}: {sc0:.3f} -> {sc:.3f}  hits={hits:3} "
              f"({time.time()-t0:5.1f}s)", flush=True)
    print()

    refined.sort(reverse=True)
    print("=" * 72)
    print("TOP-KANDIDATEN:")
    for sc, hits, n, perm, sq, pt in refined:
        print(f"  n={n} score={sc:.3f} hits={hits}")
        print(f"    PT:  {pt}")
        print(f"    SQ:  {sq}")
        print(f"    PERM: {perm}")
        print()


if __name__ == "__main__":
    main()
