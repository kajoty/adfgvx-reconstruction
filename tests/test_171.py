#!/usr/bin/env python3
"""
Harter Unittest fuer ADFGVX-Solver auf Basis von Seite 171.

WARUM DIESER TEST:
  Die Transkription von Seite 171 in corpus.py ist fehlerhaft (4 unleserliche
  Zeichen als '-' + ~109 weitere Transkriptionsfehler). Sie taugt NICHT als
  Solver-Test. Stattdessen wird der Geheimtext SYNTHETISCH aus dem bekannten
  Klartext + Schluessel erzeugt (transpose(bigr_pt, perm)).

  Damit ist der Testfall garantiert konsistent:
    decrypt(ct_synth, perm, square) == pt_true   (Score -17.187)

BEFUND (2026-09-21):
  blind_solver.py scheitert AUCH auf diesem perfekten Testfall:
    - 5 Restarts x 60k Iterationen  -> Score -26.793
    - 20 Restarts x 100k Iterationen -> Score -25.102
    - Ziel: -17.187
  => Der Solver ist das Problem, nicht die Daten.

FITNESS-LANDSCHAFT (gemessen):
  - Echte Permutation ist ein PERFEKTES lokales Optimum (0/190 Nachbarn besser)
  - Echtes Quadrat ist fast optimal (4/630 Nachbarn besser)
  - Echte Perm + Zufallsquadrat: -36.4 (Perm allein wertlos)
  - Hill-Climbing Perm MIT bekanntem Quadrat: -26.18 (scheitert!)
  - Hill-Climbing Quadrat MIT bekannter Perm: -19.31 (fast, aber nicht ganz)
  => Die Permutation ist das schwierige Teilproblem. Die Fitness-Landschaft
     ist ein "Needle in a Haystack": Perm und Quadrat muessen GLEICHZEITIG
     fast perfekt sein, sonst gibt es kein Gradientensignal.

VERWENDUNG:
  python3 test_171.py
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import KEYS, make_square, decrypt
from data.solutions import SOLVED
from analysis.reconstruct_171 import target_ciphertext
from core import langmodel


def build_case() -> tuple[str, list[int], str, str]:
    """Liefert (ct_synth, perm, square, pt_true) fuer Seite 171."""
    keyname, pt_true, _src = SOLVED["171"]
    perm, sub, _cnt = KEYS[keyname]
    sq = make_square(sub)
    ct_synth = target_ciphertext("171")
    return ct_synth, perm, sq, pt_true


def test_consistency() -> bool:
    """Der synthetische Geheimtext muss exakt zum Klartext passen."""
    ct, perm, sq, pt_true = build_case()
    pt = decrypt(ct, perm, sq)
    ok = pt == pt_true
    print(f"[{'OK' if ok else 'FEHLER'}] Konsistenz: "
          f"decrypt(ct_synth) == pt_true  (Score {langmodel.score(pt):.3f})")
    return ok


def test_length() -> bool:
    """Laenge: 2 * len(pt_true) == len(ct_synth)."""
    ct, _perm, _sq, pt_true = build_case()
    ok = len(ct) == 2 * len(pt_true)
    print(f"[{'OK' if ok else 'FEHLER'}] Laenge: {len(ct)} == 2*{len(pt_true)}")
    return ok


def test_solver(restarts: int = 5, iterations: int = 60000) -> bool:
    """Der Solver muss den Klartext finden (erwartet: schlaegt fehl)."""
    from solvers.blind_solver import solve

    ct, perm, sq, pt_true = build_case()
    target = langmodel.score(pt_true)
    sc, p, s, pt = solve(ct, 20, restarts=restarts, iterations=iterations,
                         seed=1)
    ok = pt == pt_true
    print(f"[{'OK' if ok else 'FEHLER'}] Solver: Score {sc:.3f} "
          f"(Ziel {target:.3f}), Perm korrekt: {p == perm}")
    return ok


def main() -> None:
    print("=" * 78)
    print("HARTER UNITTEST: Seite 171 (synthetischer Geheimtext)")
    print("=" * 78)
    results = [
        test_length(),
        test_consistency(),
        test_solver(),
    ]
    print()
    print(f"{sum(results)}/{len(results)} Tests bestanden")
    if not results[-1]:
        print()
        print("Der Solver scheitert auf einem PERFEKTEN Testfall.")
        print("=> Das Problem liegt im Solver, nicht in den Daten.")


if __name__ == "__main__":
    main()
