#!/usr/bin/env python3
"""
Alternierender ADFGVX-Solver.

Warum ein neuer Solver?
-----------------------
Die vorhandenen Solver scheiterten alle am selben Problem: Permutation und
Quadrat sind GEKOPPELT. Man kann sie nicht nacheinander loesen.

  * `friedman_solver` ordnet die Spalten per Bigramm-Affinitaet. Das
    funktioniert nur, wenn das Quadrat schon bekannt ist. Bei einem
    Zufallsquadrat liefert die Affinitaet kein Signal (1/20 Positionen).
  * `analytic_solver` sucht die Permutation per SA, bewertet aber jede
    Permutation mit einem frisch geloesten Quadrat. Die Landschaft ist
    dadurch so verrauscht, dass SA nichts findet.
  * `guided_solver` loest das Quadrat sehr gut, kennt aber die Permutation
    nicht.

Dieser Solver wechselt stattdessen ab:

  1. Quadrat optimieren (gegeben die aktuelle Permutation)
  2. Permutation optimieren (gegeben das aktuelle Quadrat)
  3. Wiederholen, bis sich nichts mehr verbessert

Das ist der klassische EM-artige Ansatz fuer gekoppelte Probleme. Jeder
Schritt ist fuer sich einfach; erst die Abwechslung loest das Ganze.

Fitness: die gemeinsame Funktion aus core/fitness.py (score + lam*word_hits).
Nur der Score fuehrt zu Overfitting (Seite 152), nur word_hits zu Plateaus.
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

A_MAP = {c: i for i, c in enumerate(ALPHA)}
GERMAN_ORDER = "ENISRATDHULCGMOBWFKZPVJYXQ" + "0123456789"


# --------------------------------------------------------------------------
# Quadrat-Schritt
# --------------------------------------------------------------------------

def _decode(bigrams: list[str], sq: list[str]) -> str:
    return "".join(sq[A_MAP[b[0]] * 6 + A_MAP[b[1]]] for b in bigrams if len(b) == 2)


def _initial_square(bigrams: list[str], rng: random.Random) -> list[str]:
    """Haeufigkeitsbasiertes Startquadrat (haeufigste Bigramme -> haeufigste
    deutsche Buchstaben)."""
    counts: dict[str, int] = {}
    for b in bigrams:
        if len(b) == 2:
            counts[b] = counts.get(b, 0) + 1
    ranked = sorted(counts, key=lambda b: -counts[b])
    sq: list[str | None] = [None] * 36
    used: set[str] = set()
    for bg in ranked:
        idx = A_MAP[bg[0]] * 6 + A_MAP[bg[1]]
        if sq[idx] is None:
            for ch in GERMAN_ORDER:
                if ch not in used:
                    sq[idx] = ch
                    used.add(ch)
                    break
    rest = [ch for ch in FULL if ch not in used]
    rng.shuffle(rest)
    for i in range(36):
        if sq[i] is None:
            sq[i] = rest.pop()
    return sq  # type: ignore[return-value]


def optimize_square(bigrams: list[str], sq: list[str], rng: random.Random,
                    steps: int = 4000) -> tuple[list[str], float]:
    """Hill-Climbing auf dem Quadrat mit der gemeinsamen Fitness.

    Nur die im Geheimtext vorkommenden Positionen werden getauscht. Alle
    anderen sind informationstheoretisch unbestimmbar und erzeugen nur ein
    Plateau.
    """
    active = sorted({A_MAP[b[0]] * 6 + A_MAP[b[1]] for b in bigrams if len(b) == 2})
    if len(active) < 2:
        return sq, _fitness(_decode(bigrams, sq))

    cur = list(sq)
    cur_fit = _fitness(_decode(bigrams, cur))
    best = list(cur)
    best_fit = cur_fit

    for _ in range(steps):
        i, j = rng.sample(active, 2)
        cur[i], cur[j] = cur[j], cur[i]
        fit = _fitness(_decode(bigrams, cur))
        if fit > cur_fit:
            cur_fit = fit
            if fit > best_fit:
                best_fit = fit
                best = list(cur)
        else:
            cur[i], cur[j] = cur[j], cur[i]

    return best, best_fit


# --------------------------------------------------------------------------
# Permutations-Schritt
# --------------------------------------------------------------------------

def _bigram_concentration(ct: str, perm: list[int]) -> float:
    """Konzentration der Bigramme im ruecktransponierten Text.

    Die richtige Spaltenreihenfolge erzeugt WENIGE, HAEUFIGE Bigramme
    (die Substitution erhaelt die Zipf-Verteilung des Klartexts). Eine
    falsche Reihenfolge mischt die Zeichen und erzeugt viele seltene
    Bigramme.

    Mass: Summe der quadrierten Haeufigkeiten. Empirisch trennt das die
    wahre Permutation (1933) klar von Zufall (1079-1285) - und zwar OHNE
    Kenntnis des Quadrats. Das ist der Schluessel zur Permutationssuche.
    """
    u = untranspose(ct, perm)
    counts: dict[str, int] = {}
    for i in range(0, len(u) - 1, 2):
        bg = u[i:i + 2]
        counts[bg] = counts.get(bg, 0) + 1
    return float(sum(v * v for v in counts.values()))


def optimize_perm(ct: str, perm: list[int], sq: list[str],
                  rng: random.Random, steps: int = 400) -> tuple[list[int], float]:
    """Permutationssuche ueber Bigramm-Konzentration.

    WICHTIG: Diese Suche nutzt NICHT das Quadrat und NICHT die Fitness.
    Sie maximiert allein die Bigramm-Konzentration im ruecktransponierten
    Text. Das ist ein reines Transpositions-Signal und funktioniert auch
    bei unbekanntem Quadrat.

    Warum nicht die Fitness? Die Fitness-Landschaft ist bei einem
    Zufallsquadrat extrem zerklueftet: Zufalls-Permutationen liegen bei
    -16 bis -1, die wahre bei +123. Es gibt keine graduelle Annaeherung.
    Die Bigramm-Konzentration dagegen ist glatt und monoton.

    Zugtypen: Swap und Relocate, Best-Improvement.
    """
    n = len(perm)

    def conc(p: list[int]) -> float:
        return _bigram_concentration(ct, p)

    cur = list(perm)
    cur_c = conc(cur)
    best = list(cur)
    best_c = cur_c

    # Simulated Annealing: Best-Improvement-Hillclimbing bleibt bei 20
    # Spalten in einem lokalen Optimum haengen (1551 statt 1933). SA mit
    # hoher Starttemperatur verlaesst diese Optima.
    #
    # Die Konzentration korreliert mit der Zahl korrekter Positionen
    # (0-8: ~1150, 14: 1309, 16: 1459, 18: 1933). Es gibt also einen
    # Gradienten, aber mit einer Klippe bei 18. Die Temperatur muss hoch
    # genug sein, um das Plateau zu ueberwinden.
    temp = max(200.0, cur_c * 0.15)
    temp_min = max(1.0, temp * 0.0005)
    for _ in range(steps * n * 4):
        prev = list(cur)
        # Groessere Mutationen: 1-3 Spalten bewegen
        nmut = rng.choice([1, 1, 2, 3])
        for _ in range(nmut):
            if rng.random() < 0.5:
                i, j = rng.sample(range(n), 2)
                cur[i], cur[j] = cur[j], cur[i]
            else:
                i, j = rng.sample(range(n), 2)
                item = cur.pop(i)
                cur.insert(j, item)

        c = conc(cur)
        if c >= cur_c or rng.random() < pow(2.718281828, (c - cur_c) / temp):
            cur_c = c
            if c > best_c:
                best_c = c
                best = list(cur)
        else:
            cur = prev  # Revert
        temp *= 0.9998
        if temp < temp_min:
            temp = temp_min

    # Rueckgabe: Permutation und die zugehoerige Fitness (fuer den Vergleich).
    # Ohne gueltiges Quadrat wird nur die Konzentration zurueckgegeben.
    if len(sq) == 36 and all(len(c) == 1 for c in sq):
        fit = _fitness(substitute(untranspose(ct, best), "".join(sq)))
    else:
        fit = best_c
    return best, fit


# --------------------------------------------------------------------------
# Haupt-Solver
# --------------------------------------------------------------------------

def solve(ct: str, n: int, restarts: int = 8, rounds: int = 12,
          sq_steps: int = 4000, perm_steps: int = 400,
          seed: int = 1, verbose: bool = False, seconds: float = 60.0
          ) -> tuple[float, list[int], str, str]:
    """Alternierende Optimierung von Permutation und Quadrat.

    Rueckgabe: (fitness, perm, quadrat, klartext)

    Laeuft hoechstens ``seconds`` Sekunden (Zeitbudget).
    """
    ct = clean(ct)
    rng = random.Random(seed)
    budget = Budget(max_seconds=seconds)

    g_best_fit = -1e18
    g_best_perm: list[int] = []
    g_best_sq = ""
    g_best_pt = ""

    for r in range(restarts):
        if budget.should_stop():
            break
        perm = list(range(n))
        rng.shuffle(perm)

        # Schritt 1: Permutation ueber Bigramm-Konzentration (quadratfrei).
        # Das liefert die richtige Spaltenreihenfolge, unabhaengig vom Quadrat.
        perm, _ = optimize_perm(ct, perm, [""] * 36, rng, steps=perm_steps)

        # Schritt 2: Quadrat fuer diese Permutation loesen.
        bigrams = [untranspose(ct, perm)[i:i + 2]
                   for i in range(0, len(ct) - 1, 2)]
        sq = _initial_square(bigrams, rng)

        prev_fit = -1e18
        fit = -1e18
        for rnd in range(rounds):
            if budget.should_stop():
                break
            # Quadrat optimieren
            sq, fit_sq = optimize_square(bigrams, sq, rng, steps=sq_steps)
            # Permutation feinjustieren (jetzt mit Quadrat-Signal)
            perm, fit = optimize_perm(ct, perm, sq, rng, steps=perm_steps)
            budget.tick(fit)
            # Bigramme neu ableiten
            bigrams = [untranspose(ct, perm)[i:i + 2]
                       for i in range(0, len(ct) - 1, 2)]

            if verbose:
                print(f"  r={r} runde={rnd:2d}  fit={fit:8.3f}")

            # Konvergenz: keine Verbesserung mehr
            if fit <= prev_fit + 1e-6:
                break
            prev_fit = fit

        if fit > g_best_fit:
            g_best_fit = fit
            g_best_perm = list(perm)
            g_best_sq = "".join(sq)
            g_best_pt = substitute(untranspose(ct, perm), g_best_sq)

    return g_best_fit, g_best_perm, g_best_sq, g_best_pt


# --------------------------------------------------------------------------
# Testrahmen
# --------------------------------------------------------------------------

def build_case_171():
    from core.adfgvx import KEYS, make_square
    from data.solutions import SOLVED
    from analysis.reconstruct_171 import target_ciphertext
    keyname, pt_true, _src = SOLVED["171"]
    perm, sub, _cnt = KEYS[keyname]
    return target_ciphertext("171"), perm, make_square(sub), pt_true


def test_synthetic(restarts: int = 8, rounds: int = 12, seed: int = 1,
                   seconds: float = 60.0) -> bool:
    ct, perm_true, sq_true, pt_true = build_case_171()
    print("=" * 78)
    print("ALTERNIERENDER SOLVER — Test auf synthetischem 171er-Testfall")
    print("=" * 78)
    print(f"Geheimtext : {len(ct)} Zeichen (fehlerfrei)")
    print(f"Ziel-Fitness: {_fitness(pt_true):.3f}  "
          f"(score={langmodel.score(pt_true):.3f}, "
          f"hits={langmodel.word_hits(pt_true)})")
    print(f"Zeitbudget : {seconds:.0f}s")
    print()

    t0 = time.time()
    fit, perm, sq, pt = solve(ct, 20, restarts=restarts, rounds=rounds,
                              seed=seed, verbose=True, seconds=seconds)
    dt = time.time() - t0

    sc, wh, _ = fitness_parts(pt)
    print()
    print(f"Laufzeit        : {dt:.1f} s")
    print(f"Fitness         : {fit:.3f}")
    print(f"Score           : {sc:.3f}")
    print(f"Worttreffer     : {wh}")
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


def main() -> None:
    if "--page" in sys.argv:
        idx = sys.argv.index("--page")
        page = sys.argv[idx + 1]
        n = int(sys.argv[idx + 2]) if len(sys.argv) > idx + 2 else 20
        seconds = float(sys.argv[idx + 3]) if len(sys.argv) > idx + 3 else 60.0
        from data.corpus import CORPUS
        ct = clean(CORPUS[page])
        print(f"ALTERNIERENDER SOLVER — Seite {page} ({len(ct)} Zeichen, n={n}), "
              f"Zeitbudget {seconds:.0f}s")
        t0 = time.time()
        fit, perm, sq, pt = solve(ct, n, verbose=True, seconds=seconds)
        sc, wh, _ = fitness_parts(pt)
        print(f"\nLaufzeit : {time.time() - t0:.1f} s")
        print(f"Fitness  : {fit:.3f}  score={sc:.3f}  hits={wh}")
        print(f"Perm     : {perm}")
        print(f"Quadrat  : {sq}")
        print(f"Klartext : {pt}")
    else:
        test_synthetic()


if __name__ == "__main__":
    main()
