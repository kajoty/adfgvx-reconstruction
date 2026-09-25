#!/usr/bin/env python3
"""
Analytischer ADFGVX-Solver.

Löst das 6x6-Substitutionsquadrat für eine hypothetische Permutation
analytisch/frequenzbasiert über eine innere Hill-Climbing-Schleife.
"""

from __future__ import annotations
import random
import sys
import time

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, clean, untranspose, substitute
from core import langmodel
from core.fitness import fitness as _fitness, fitness_parts
from solvers.base import Budget

# Pre-calculated Index mapping for fast execution
A_MAP = {c: i for i, c in enumerate(ALPHA)}

# Deutsche Buchstabenhaeufigkeit als Zielreihenfolge fuer die Initialisierung
GERMAN_ORDER = "ENISRATDHULCGMOBWFKZPVJYXQ" + "0123456789"


def _bigram_counts(untransposed_ct: str) -> dict[str, int]:
    """Haeufigkeit der 36 Bigramme im ruecktransponierten Text."""
    counts: dict[str, int] = {}
    for i in range(0, len(untransposed_ct) - 1, 2):
        bg = untransposed_ct[i:i + 2]
        counts[bg] = counts.get(bg, 0) + 1
    return counts


def initial_square(untransposed_ct: str, rng: random.Random) -> str:
    """Haeufigkeitsbasiertes Startquadrat.

    Die haeufigsten Bigramme werden auf die haeufigsten Klartextzeichen
    gelegt. Das ist die klassische Initialisierung fuer monoalphabetische
    Substitution und spart viele Hill-Climbing-Schritte.
    """
    counts = _bigram_counts(untransposed_ct)
    ranked = sorted(counts, key=lambda bg: -counts[bg])
    square: list[str | None] = [None] * 36
    used: set[str] = set()
    for bg in ranked:
        idx = A_MAP[bg[0]] * 6 + A_MAP[bg[1]]
        if square[idx] is None:
            for ch in GERMAN_ORDER:
                if ch not in used:
                    square[idx] = ch
                    used.add(ch)
                    break
    rest = [ch for ch in FULL if ch not in used]
    rng.shuffle(rest)
    for i in range(36):
        if square[i] is None:
            square[i] = rest.pop()
    return "".join(square)  # type: ignore[arg-type]


def solve_square_for_perm(untransposed_ct: str, steps: int = 1500,
                          rng: random.Random | None = None,
                          init: str | None = None) -> tuple[str, float]:
    """
    Findet das optimale 6x6-Quadrat für einen bereits rücktransponierten
    Zwischentext über Hill-Climbing (monoalphabetische Substitution).

    `init` ist ein Warmstart-Quadrat (z.B. aus dem vorherigen
    Permutationsschritt). Ohne Warmstart wird ein haeufigkeitsbasiertes
    Startquadrat erzeugt.
    """
    if rng is None:
        rng = random.Random()

    if len(untransposed_ct) % 2 != 0:
        untransposed_ct = untransposed_ct[:-1]

    bigrams = [untransposed_ct[i : i + 2] for i in range(0, len(untransposed_ct), 2)]
    
    # 1. Startquadrat (36 Zeichen!)
    if init is not None and len(init) == 36:
        sq = list(init)
    else:
        sq = list(initial_square(untransposed_ct, rng))

    def decode_fast(square_list: list[str]) -> str:
        pt = []
        for b in bigrams:
            if len(b) == 2:
                r, c = A_MAP[b[0]], A_MAP[b[1]]
                pt.append(square_list[r * 6 + c])
        return "".join(pt)

    # WICHTIG: Die gemeinsame Fitness (score + lam*word_hits) statt nur
    # langmodel.score. Nur der Score fuehrt zu Overfitting (siehe Seite 152).
    curr_pt = decode_fast(sq)
    curr_score = _fitness(curr_pt)

    best_sq = list(sq)
    best_score = curr_score

    # 2. Hill-Climbing auf dem Quadrat
    for _ in range(steps):
        i, j = rng.sample(range(36), 2)
        sq[i], sq[j] = sq[j], sq[i]

        cand_pt = decode_fast(sq)
        cand_score = _fitness(cand_pt)

        if cand_score > curr_score:
            curr_score = cand_score
            if cand_score > best_score:
                best_score = cand_score
                best_sq = list(sq)
        else:
            sq[i], sq[j] = sq[j], sq[i]  # Revert

    return "".join(best_sq), best_score


def _affinity_perm(ct: str, n: int) -> list[int]:
    """Startpermutation aus der Bigramm-Affinitaet (Beam-Search).

    Nutzt die bewaehrte Spaltenordnungs-Strategie aus friedman_solver.
    Faellt bei Fehlern auf eine Zufallspermutation zurueck.
    """
    try:
        from solvers.friedman_solver import split_columns, order_columns, order_to_perm
        cols = split_columns(ct, n)
        order = order_columns(cols, n)
        return order_to_perm(order)
    except Exception:
        p = list(range(n))
        random.Random(0).shuffle(p)
        return p


def solve(
    ct: str,
    key_len: int = 20,
    restarts: int = 5,
    iterations: int = 200,
    seed: int = 1,
    sq_steps: int = 1500,
    sq_steps_fast: int = 600,
    verbose: bool = False,
    seconds: float = 60.0,
) -> tuple[float, list[int], str, str]:
    """
    Analytische Haupt-Schnittstelle.

    Sucht die optimale Permutation der Länge key_len. Jede Permutations-Candidate
    wird durch das optimal aufgelöste Quadrat bewertet.

    Das Quadrat wird als Warmstart weitergereicht, damit die Bewertung
    benachbarter Permutationen vergleichbar bleibt (glatter Gradient).

    Die erste Permutation kommt aus einer Beam-Search ueber Bigramm-Affinitaet
    (siehe friedman_solver.order_columns). Reines Zufalls-Shuffle findet bei
    20 Spalten (20! Moeglichkeiten) nie die richtige Reihenfolge.

    Laeuft hoechstens ``seconds`` Sekunden (Zeitbudget), damit der Solver
    garantiert durchlaeuft.
    """
    rng = random.Random(seed)
    budget = Budget(max_seconds=seconds)

    # Gute Startpermutation aus der Bigramm-Affinitaet.
    start_perm = _affinity_perm(ct, key_len)

    global_best_score = -1e18
    global_best_perm: list[int] = []
    global_best_sq = ""
    global_best_pt = ""

    for restart in range(restarts):
        if budget.should_stop():
            break
        # Initialisiere Permutation: beim ersten Restart die Affinitaets-
        # Permutation, danach leichte Varianten davon.
        if restart == 0:
            curr_perm = list(start_perm)
        else:
            curr_perm = list(start_perm)
            for _ in range(restart):
                i, j = rng.sample(range(key_len), 2)
                curr_perm[i], curr_perm[j] = curr_perm[j], curr_perm[i]

        untrans = untranspose(ct, curr_perm)
        curr_sq, curr_score = solve_square_for_perm(
            untrans, steps=sq_steps, rng=rng)

        best_perm = list(curr_perm)
        best_score = curr_score
        best_sq = curr_sq
        warm = curr_sq  # Warmstart fuer den naechsten Schritt

        # Die Temperatur muss zur Groessenordnung der Fitness passen.
        # Die gemeinsame Fitness liegt bei echten Texten um 40-65, nicht
        # bei 1.0. Eine feste Starttemperatur von 1.0 friert die Suche ein.
        temp = max(2.0, abs(curr_score) * 0.05)
        temp_min = temp * 0.02
        for it in range(iterations):
            if budget.should_stop():
                break
            # Transposition-Mutation (Tausche 2 Spalten)
            cand_perm = list(curr_perm)
            i, j = rng.sample(range(key_len), 2)
            cand_perm[i], cand_perm[j] = cand_perm[j], cand_perm[i]

            untrans_cand = untranspose(ct, cand_perm)
            cand_sq, cand_score = solve_square_for_perm(
                untrans_cand, steps=sq_steps_fast, rng=rng, init=warm)
            budget.tick(cand_score)

            # SA-Akzeptanz: erlaubt auch mal schlechtere Permutationen
            if (cand_score >= curr_score
                    or rng.random() < pow(2.718281828,
                                          (cand_score - curr_score) / temp)):
                curr_perm = cand_perm
                curr_score = cand_score
                warm = cand_sq
                if cand_score > best_score:
                    best_score = cand_score
                    best_perm = list(cand_perm)
                    best_sq = cand_sq
            temp *= 0.99
            if temp < temp_min:
                temp = temp_min

        if best_score > global_best_score:
            global_best_score = best_score
            global_best_perm = list(best_perm)
            global_best_sq = best_sq
            untrans_final = untranspose(ct, global_best_perm)
            global_best_pt = substitute(untrans_final, global_best_sq)

        if verbose:
            print(f"  restart {restart}: {best_score:.3f}")

    return global_best_score, global_best_perm, global_best_sq, global_best_pt


# --------------------------------------------------------------------------
# Testrahmen
# --------------------------------------------------------------------------

def build_case_171() -> tuple[str, list[int], str, str]:
    """Synthetischer, garantiert fehlerfreier Testfall fuer Seite 171."""
    from core.adfgvx import KEYS, make_square
    from data.solutions import SOLVED
    from analysis.reconstruct_171 import target_ciphertext

    keyname, pt_true, _src = SOLVED["171"]
    perm, sub, _cnt = KEYS[keyname]
    sq = make_square(sub)
    return target_ciphertext("171"), perm, sq, pt_true


def test_synthetic(restarts: int = 5, iterations: int = 200,
                   seed: int = 1, seconds: float = 60.0) -> bool:
    """Validiert den analytischen Solver am synthetischen 171er-Testfall."""
    ct, perm_true, sq_true, pt_true = build_case_171()
    target = langmodel.score(pt_true)
    print("=" * 78)
    print("ANALYTISCHER SOLVER — Test auf synthetischem 171er-Testfall")
    print("=" * 78)
    print(f"Geheimtext : {len(ct)} Zeichen (fehlerfrei)")
    print(f"Ziel-Score : {target:.3f}")
    print(f"Parameter  : {restarts} Restarts x {iterations} Perm-Schritte, "
          f"Zeitbudget {seconds:.0f}s")
    print()

    t0 = time.time()
    sc, perm, sq, pt = solve(ct, 20, restarts=restarts, iterations=iterations,
                             seed=seed, verbose=True, seconds=seconds)
    dt = time.time() - t0

    print()
    print(f"Laufzeit        : {dt:.1f} s")
    print(f"Score           : {sc:.3f}  (Ziel {target:.3f})")
    print(f"Permutation ok  : {perm == perm_true}")
    print(f"Quadrat ok      : {sq == sq_true}")
    print(f"Klartext ok     : {pt == pt_true}")
    print()
    print(f"Gefunden : {pt[:78]}")
    print(f"Erwartet : {pt_true[:78]}")
    ok = pt == pt_true
    print()
    print("ERGEBNIS:", "GELOEST" if ok else "NICHT GELOEST")
    return ok


def test_page(page: str, n: int, restarts: int = 5, iterations: int = 200,
              seed: int = 1, seconds: float = 60.0) -> None:
    """Blindtest auf einer echten (fehlerhaften) Corpus-Seite."""
    from data.corpus import CORPUS

    ct = clean(CORPUS[page])
    print("=" * 78)
    print(f"ANALYTISCHER SOLVER — Blindtest Seite {page} "
          f"({len(ct)} Zeichen, n={n}), Zeitbudget {seconds:.0f}s")
    print("=" * 78)
    t0 = time.time()
    sc, perm, sq, pt = solve(ct, n, restarts=restarts, iterations=iterations,
                             seed=seed, verbose=True, seconds=seconds)
    print()
    print(f"Laufzeit : {time.time() - t0:.1f} s")
    print(f"Score    : {sc:.3f}")
    print(f"Perm     : {perm}")
    print(f"Quadrat  : {sq}")
    print(f"Klartext : {pt[:78]}")


def main() -> None:
    from solvers.base import build_parser

    ap = build_parser("analytic_solver", default_page=None)
    args = ap.parse_args()
    if args.page is None:
        test_synthetic()
        return
    seconds = 10.0 if args.quick else args.seconds
    n = args.n if args.n > 0 else 20
    test_page(args.page, n, seconds=seconds)


if __name__ == "__main__":
    main()