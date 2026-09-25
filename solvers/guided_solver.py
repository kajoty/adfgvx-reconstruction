#!/usr/bin/env python3
"""
Gezielter Quadrat-Solver fuer ADFGVX.

Motivation (siehe /memories/repo/adfgvx-cryptanalysis.md):

  * Das Trigramm-Modell ist fuer historischen Militaertext AKTIV SCHAEDLICH:
    das echte Quadrat ist kein lokales Optimum (4 von 630 Nachbarn besser).
  * `word_hits` diskriminiert korrekt (echtes Quadrat 123 vs. 118/100/121).
  * `score + lambda*word_hits` macht das echte Quadrat zum perfekten lokalen
    Optimum (0/630) — aber weder Single-Swap-Hillclimbing noch Random-2-Swap-SA
    finden es (0/20 bei lambda = 0.02 / 0.05 / 0.10).

Konsequenz: Der Suchraum (630 Nachbarn pro Schritt) ist zu gross und zu
zerklueftet. Dieser Solver reduziert ihn drastisch:

  1. `uncovered_spans()` findet die Textstellen, die von KEINEM bekannten Wort
     abgedeckt sind. Nur dort kann ein Swap ueberhaupt `word_hits` erhoehen.
  2. `candidate_swaps()` sammelt nur Swaps, an denen mindestens ein Zeichen
     aus einer ungedeckten Stelle beteiligt ist.
  3. `guided_hillclimb()` bewertet diese Kandidaten vollstaendig und nimmt den
     besten. Das ist Hillclimbing mit Best-Improvement statt Zufallsswap.

Zusaetzlich: `word_hits` allein als Zielfunktion (Phase 1), danach Feinschliff
mit `score + lambda*word_hits` (Phase 2).
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
from solvers.base import Budget

A_MAP = {c: i for i, c in enumerate(ALPHA)}
GERMAN_ORDER = "ENISRATDHULCGMOBWFKZPVJYXQ" + "0123456789"

# Maximale Wortlaenge, die `word_hits` prueft (siehe langmodel.word_hits)
MAX_WORD_LEN = 14
MIN_WORD_LEN = 3


# --------------------------------------------------------------------------
# Abdeckungsanalyse
# --------------------------------------------------------------------------

def covered_mask(text: str) -> list[bool]:
    """Markiert jede Position, die Teil eines erkannten Wortes ist.

    Bevorzugt lange Woerter (greedy, laengste zuerst), damit z.B.
    WIEDERHERSTELLUNG nicht in kleinere Fragmente zerfaellt.
    """
    n = len(text)
    found: list[tuple[int, int]] = []
    for i in range(n):
        for j in range(i + MIN_WORD_LEN, min(n, i + MAX_WORD_LEN) + 1):
            if text[i:j] in langmodel._WORD_SET:
                found.append((i, j))
    found.sort(key=lambda ij: -(ij[1] - ij[0]))

    used = [False] * n
    for i, j in found:
        if not any(used[i:j]):
            for k in range(i, j):
                used[k] = True
    return used


def uncovered_spans(text: str) -> list[tuple[int, int]]:
    """Zusammenhaengende Bereiche ohne Worterkennung."""
    used = covered_mask(text)
    spans: list[tuple[int, int]] = []
    start: int | None = None
    for i, u in enumerate(used):
        if not u and start is None:
            start = i
        elif u and start is not None:
            spans.append((start, i))
            start = None
    if start is not None:
        spans.append((start, len(text)))
    return spans


def coverage(text: str) -> float:
    used = covered_mask(text)
    return sum(used) / len(text) if text else 0.0


def random_baseline_hits(length: int, trials: int = 10,
                         seed: int = 12345) -> float:
    """Erwartete `word_hits` fuer Zufallstext der Laenge `length`.

    KRITISCH (siehe /memories/repo/adfgvx-cryptanalysis.md):
    `word_hits` zaehlt alle Substrings der Laenge 3-14 aus 49378 Woertern.
    Bei ~100 Zeichen entstehen ~1000 Substrings, von denen rein statistisch
    ~25-38 zufaellig ein kurzes Wort treffen. Eine Trefferzahl von 29 auf
    einer echten Seite ist daher KEIN Erfolgsindikator — der Zufall liefert
    denselben Wert.

    Nur wenn `word_hits` deutlich ueber dieser Baseline liegt, ist die
    Zielfunktion aussagekraeftig.
    """
    rng = random.Random(seed)
    total = 0
    for _ in range(trials):
        fake = "".join(rng.choice(ALPHA) for _ in range(length))
        total += langmodel.word_hits(fake)
    return total / trials


def hits_signal(text: str, trials: int = 10) -> tuple[int, float, float]:
    """Vergleicht `word_hits(text)` mit der Zufalls-Baseline.

    Rueckgabe: (hits, baseline, faktor). Faktor < 1.5 bedeutet Rauschen.
    """
    hits = langmodel.word_hits(text)
    base = random_baseline_hits(len(text), trials=trials)
    faktor = hits / base if base > 0 else float("inf")
    return hits, base, faktor


# --------------------------------------------------------------------------
# Kandidaten-Swaps
# --------------------------------------------------------------------------

def active_positions(bigrams: list[str]) -> list[int]:
    """Quadrat-Positionen, die im Geheimtext tatsaechlich vorkommen.

    Nur diese Positionen sind aus dem Geheimtext ueberhaupt bestimmbar.
    Alle anderen (im Testfall 15 von 36) sind informationstheoretisch
    unbestimmbar und duerfen nicht durchsucht werden — sie erzeugen sonst
    ein riesiges Plateau in der Zielfunktion.
    """
    return sorted({A_MAP[b[0]] * 6 + A_MAP[b[1]] for b in bigrams if len(b) == 2})


def candidate_swaps_from_bigrams(bigrams: list[str],
                                 spans: list[tuple[int, int]],
                                 active: list[int]) -> set[tuple[int, int]]:
    """Swaps, die eine ungedeckte Stelle veraendern koennten.

    `spans` bezieht sich auf den Klartext, also auf Bigramm-Indizes.
    Beschraenkt auf die aktiven Quadrat-Positionen.

    Zwei Richtungen sind relevant:
      (a) Felder, die an ungedeckten Stellen BENUTZT werden (dort steht der
          falsche Buchstabe),
      (b) Felder direkt an den Bruchstellen (die "fast richtigen" Nachbarn).
    """
    hot: set[int] = set()
    n_bg = len(bigrams)
    for a, b in spans:
        # Spannen defensiv begrenzen (b kann == n_bg sein)
        for k in range(max(0, a), min(b, n_bg)):
            bg = bigrams[k]
            hot.add(A_MAP[bg[0]] * 6 + A_MAP[bg[1]])
        # (b) Nachbarschaft der Bruchstellen
        for k in (a - 1, a, b - 1, b):
            if 0 <= k < n_bg:
                bg = bigrams[k]
                hot.add(A_MAP[bg[0]] * 6 + A_MAP[bg[1]])

    hot &= set(active)
    swaps: set[tuple[int, int]] = set()
    for i in sorted(hot):
        for j in active:
            if i != j:
                swaps.add((min(i, j), max(i, j)))
    return swaps


# --------------------------------------------------------------------------
# Schnelle Dekodierung
# --------------------------------------------------------------------------

def make_decoder(bigrams: list[str]):
    """Erzeugt eine schnelle decode(square_list) -> Klartext-Funktion."""
    idxs = [A_MAP[b[0]] * 6 + A_MAP[b[1]] for b in bigrams if len(b) == 2]

    def decode(sq: list[str]) -> str:
        return "".join(sq[k] for k in idxs)

    return decode


# --------------------------------------------------------------------------
# Phase 1: word_hits maximieren (gezielt)
# --------------------------------------------------------------------------

def guided_hillclimb(bigrams: list[str], square: list[str],
                     rng: random.Random,
                     max_rounds: int = 60,
                     use_score: bool = False,
                     lam: float = 0.05,
                     verbose: bool = False) -> tuple[list[str], float, int]:
    """Best-Improvement-Hillclimbing ueber gezielte Kandidaten-Swaps.

    Zielfunktion:
      use_score=False -> nur `word_hits` (Phase 1)
      use_score=True  -> `score + lam*word_hits` (Phase 2)

    Der Suchraum ist auf die aktiven Quadrat-Positionen beschraenkt.

    Rueckgabe: (square, fitness, word_hits)
    """
    decode = make_decoder(bigrams)
    active = active_positions(bigrams)

    def fitness(sq: list[str]) -> tuple[float, int]:
        pt = decode(sq)
        wh = langmodel.word_hits(pt)
        if use_score:
            return langmodel.score(pt) + lam * wh, wh
        return float(wh), wh

    cur_sq = list(square)
    cur_fit, cur_wh = fitness(cur_sq)

    for rnd in range(max_rounds):
        pt = decode(cur_sq)
        spans = uncovered_spans(pt)
        if not spans:
            break
        cands = candidate_swaps_from_bigrams(bigrams, spans, active)
        if not cands:
            break

        best_gain = 0.0
        best_swap: tuple[int, int] | None = None
        best_sq: list[str] | None = None
        best_wh = cur_wh
        best_fit_cand = cur_fit

        for i, j in cands:
            cur_sq[i], cur_sq[j] = cur_sq[j], cur_sq[i]
            fit, wh = fitness(cur_sq)
            cur_sq[i], cur_sq[j] = cur_sq[j], cur_sq[i]
            if fit > cur_fit + 1e-12:
                if fit - cur_fit > best_gain:
                    best_gain = fit - cur_fit
                    best_swap = (i, j)
                    best_wh = wh
                    best_fit_cand = fit
                    cand = list(cur_sq)
                    cand[i], cand[j] = cand[j], cand[i]
                    best_sq = cand

        if best_swap is None or best_sq is None:
            break

        cur_sq = best_sq
        cur_fit = best_fit_cand  # exakter Wert statt Akkumulation
        cur_wh = best_wh
        if verbose:
            print(f"    Runde {rnd + 1:2d}: +{best_gain:.3f}  "
                  f"hits={cur_wh:3d}  swap={best_swap}")

    return cur_sq, cur_fit, cur_wh


# --------------------------------------------------------------------------
# Kombinierter Solver
# --------------------------------------------------------------------------

def solve_square(bigrams: list[str], rng: random.Random,
                 restarts: int = 20,
                 phase1_rounds: int = 60,
                 phase2_rounds: int = 40,
                 lam: float = 0.05,
                 verbose: bool = False,
                 budget: "Budget | None" = None) -> tuple[list[str], float, int]:
    """Zweiphasige gezielte Suche mit Restarts.

    Phase 1: `word_hits` maximieren (grobe Struktur finden)
    Phase 2: `score + lam*word_hits` (Feinschliff)

    Bricht ab, sobald das uebergebene ``Budget`` erschoepft ist.
    """
    from solvers.analytic_solver import initial_square

    best_sq: list[str] = []
    best_fit = -1e18
    best_wh = -1

    for r in range(restarts):
        if budget is not None and budget.should_stop():
            break
        # Start: haeufigkeitsbasiert, danach leicht perturbieren
        start = list(initial_square("".join(bigrams), rng))
        if r > 0:
            for _ in range(r):
                i, j = rng.sample(range(36), 2)
                start[i], start[j] = start[j], start[i]

        sq1, _f1, wh1 = guided_hillclimb(
            bigrams, start, rng, max_rounds=phase1_rounds,
            use_score=False, verbose=False)
        sq2, f2, wh2 = guided_hillclimb(
            bigrams, sq1, rng, max_rounds=phase2_rounds,
            use_score=True, lam=lam, verbose=False)

        if budget is not None:
            budget.tick(f2)
        if f2 > best_fit:
            best_fit = f2
            best_sq = sq2
            best_wh = wh2
        if verbose:
            print(f"  restart {r:2d}: hits={wh2:3d}  fit={f2:.3f}")

    return best_sq, best_fit, best_wh


# --------------------------------------------------------------------------
# Testrahmen
# --------------------------------------------------------------------------

def test_synthetic(restarts: int = 20, seed: int = 1,
                   verbose: bool = True) -> bool:
    from solvers.analytic_solver import build_case_171

    ct, perm_true, sq_true, pt_true = build_case_171()
    untrans = untranspose(ct, perm_true)
    bigrams = [untrans[i:i + 2] for i in range(0, len(untrans), 2)]

    print("=" * 78)
    print("GEZIELTER SOLVER — Test auf synthetischem 171er-Testfall")
    print("=" * 78)
    print(f"Ziel-Score : {langmodel.score(pt_true):.3f}")
    print(f"Ziel-hits  : {langmodel.word_hits(pt_true)}")
    print(f"Parameter  : {restarts} Restarts")
    print()

    rng = random.Random(seed)
    t0 = time.time()
    sq, fit, wh = solve_square(bigrams, rng, restarts=restarts, verbose=verbose)
    dt = time.time() - t0

    pt = substitute("".join(bigrams), "".join(sq))
    active = active_positions(bigrams)
    used_ok = all(sq[i] == sq_true[i] for i in active)
    hits, base, faktor = hits_signal(pt)
    print()
    print(f"Laufzeit   : {dt:.1f} s")
    print(f"hits       : {wh}  (Ziel {langmodel.word_hits(pt_true)})")
    print(f"Score      : {langmodel.score(pt):.3f}  "
          f"(Ziel {langmodel.score(pt_true):.3f})")
    print(f"Baseline   : {base:.1f} hits auf Zufall  ->  Faktor {faktor:.2f}"
          f"  {'(Signal)' if faktor >= 1.5 else '(RAUSCHEN!)'}")
    print(f"Aktive Pos.: {len(active)} von 36 — "
          f"{'OK' if used_ok else 'falsch'}")
    print(f"Klartext ok: {pt == pt_true}")
    print()
    print(f"Gefunden : {pt[:78]}")
    print(f"Erwartet : {pt_true[:78]}")
    ok = pt == pt_true
    print()
    print("ERGEBNIS:", "GELOEST" if ok else "NICHT GELOEST")
    return ok


def main() -> None:
    if "--page" in sys.argv:
        from data.corpus import CORPUS
        idx = sys.argv.index("--page")
        page = sys.argv[idx + 1]
        n = int(sys.argv[idx + 2]) if len(sys.argv) > idx + 2 else 20
        seconds = float(sys.argv[idx + 3]) if len(sys.argv) > idx + 3 else 60.0
        ct = clean(CORPUS[page])
        bigrams = [ct[i:i + 2] for i in range(0, len(ct), 2)]
        rng = random.Random(1)
        budget = Budget(max_seconds=seconds, patience=200)
        t0 = time.time()
        sq, fit, wh = solve_square(bigrams, rng, restarts=20, verbose=True,
                                   budget=budget)
        pt = substitute("".join(bigrams), "".join(sq))
        hits, base, faktor = hits_signal(pt)
        print(f"\nLaufzeit : {time.time() - t0:.1f} s")
        print(f"hits     : {wh}")
        print(f"Baseline : {base:.1f} auf Zufall  ->  Faktor {faktor:.2f}"
              f"  {'(Signal)' if faktor >= 1.5 else '(RAUSCHEN — Ergebnis unbrauchbar!)'}")
        print(f"Score    : {langmodel.score(pt):.3f}")
        print(f"Quadrat  : {''.join(sq)}")
        print(f"Klartext : {pt[:78]}")
    else:
        test_synthetic()


if __name__ == "__main__":
    main()
