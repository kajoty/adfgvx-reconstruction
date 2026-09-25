#!/usr/bin/env python3
"""
Friedman-Solver fuer ADFGVX (Military Cryptanalysis Part IV, Section IX).

Anders als blind_solver.py (Simulated Annealing ueber Perm+Quadrat) nutzt
dieser Solver die STRUKTUR des Verfahrens:

  Phase 1: Spaltenbreite n bestimmen
           -> Koinzidenz-Analyse (Index of Coincidence) des Geheimtextes.
              Bei falschem n sind die Spalten "durchmischt", bei richtigem n
              stehen in jeder Spalte zusammenhaengende Bigramm-Haelften.

  Phase 2: Spaltenreihenfolge rekonstruieren
           -> Bigramm-Koinzidenz zwischen Spaltenpaaren. Zwei Spalten, die im
              Zwischentext benachbart waren, teilen sich die Bigramm-Struktur
              (die 2. Haelfte eines Bigramms in Spalte c ist die 1. Haelfte in
              Spalte c+1). Wir bauen einen Graphen und suchen den besten Pfad.

  Phase 3: Quadrat loesen
           -> Nach Ruecktransposition ist das Quadrat ein monoalphabetisches
              Substitutionsproblem: per Haeufigkeitsanalyse / n-Gramm-Fitness.

Validierung: Zuerst auf geloester Seite 171 (310 Zeichen) testen.
"""

from __future__ import annotations

import math
import random
from collections import Counter

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, KEYS, clean, decrypt, untranspose
from data.corpus import CORPUS
from data.solutions import SOLVED
from core import langmodel
from solvers.base import Budget


# --------------------------------------------------------------------------
# Phase 1: Spaltenbreite ueber Koinzidenz-Analyse
# --------------------------------------------------------------------------

def ioc(text: str) -> float:
    """Index of Coincidence (normiert auf 1.0 = Gleichverteilung)."""
    if len(text) < 2:
        return 0.0
    counts = Counter(text)
    n = len(text)
    num = sum(c * (c - 1) for c in counts.values())
    return num / (n * (n - 1))


def column_ioc(ct: str, n: int) -> float:
    """Mittlerer IoC der Spalten bei angenommener Breite n.

    Bei korrektem n enthaelt jede Spalte die 1. Haelfte der Bigramme des
    Zwischentextes -> die Zeichenverteilung ist NICHT gleichverteilt, sondern
    folgt der Verteilung der Bigramm-Anfangszeichen. Bei falschem n sind die
    Spalten zufaellig gemischt -> IoC naeher an der Gleichverteilung (1/6).
    """
    cols = split_columns(ct, n)
    return sum(ioc(c) for c in cols) / n


def lag_ioc(ct: str, n: int) -> float:
    """Koinzidenz zwischen Spalten bei Verschiebung (Friedman-Lag-Test).

    Bei korrektem n sind die Spalten c und c+1 im Zwischentext benachbart:
    die 2. Haelfte eines Bigramms in Spalte c ist die 1. Haelfte in Spalte
    c+1. Verschiebt man die Spalten um 1 Zeile gegeneinander, treffen die
    Bigramm-Haelften aufeinander -> erhoehte Koinzidenz.

    Wichtig: Vielfache der echten Breite (2n, 3n) erzeugen ebenfalls hohe
    Einzelspalten-IoC, aber KEINE Lag-Koinzidenz. Der Lag-Test trennt daher
    die echte Breite von ihren Vielfachen.
    """
    cols = split_columns(ct, n)
    total = 0.0
    pairs = 0
    for c in range(n - 1):
        a, b = cols[c], cols[c + 1]
        m = min(len(a), len(b))
        if m < 2:
            continue
        # Koinzidenz bei Verschiebung 1: a[i] == b[i-1]?
        hits = sum(1 for i in range(1, m) if a[i] == b[i - 1])
        total += hits / (m - 1)
        pairs += 1
    return total / pairs if pairs else 0.0


def best_widths(ct: str, lo: int = 12, hi: int = 26, top: int = 5):
    """Kandidaten fuer die Spaltenbreite.

    WICHTIGE ERKENNTNIS (empirisch verifiziert an Seite 171):
    Der klassische IoC-Test ist bei ADFGVX mit ZUFALLSQUADRATEN wertlos.
    Der Zwischentext ist ueber die 6 Zeichen nahezu gleichverteilt, daher
    zeigt der Spalten-IoC bei der echten Breite KEINEN Ausreisser (alle
    Werte 0.22-0.24, kein Signal bei n=20).

    Die Breite muss daher ueber den n-Gramm-Score NACH Phase 3 bestimmt
    werden (siehe solve()). Diese Funktion liefert nur eine grobe
    Vorauswahl/Vorinformation (IoC + Lag) und dient der Diagnose.
    """
    base = 1.0 / 6.0
    scored = []
    for n in range(lo, hi + 1):
        ci = column_ioc(ct, n)
        lag = lag_ioc(ct, n)
        score = abs(ci - base) + 2.0 * lag
        scored.append((score, n, ci, lag))
    scored.sort(reverse=True)
    return scored[:top]


# --------------------------------------------------------------------------
# Phase 2: Spaltenreihenfolge ueber Bigramm-Koinzidenz
# --------------------------------------------------------------------------

def split_columns(ct: str, n: int) -> list[str]:
    """Teilt den Geheimtext in die n Spalten (in Auslese-Reihenfolge)."""
    length = len(ct)
    rows = (length + n - 1) // n
    rest = length % n
    if rest == 0:
        rest = n
    collen = [rows if i < rest else rows - 1 for i in range(n)]
    cols = []
    pos = 0
    for c in range(n):
        cols.append(ct[pos:pos + collen[c]])
        pos += collen[c]
    return cols


def bigram_affinity(a: str, b: str, parity: int = 0) -> float:
    """Wie gut passt Spalte a als Vorgaenger von Spalte b?

    Im Zwischentext steht in Spalte c die 1. Haelfte und in Spalte c+1 die
    2. Haelfte jedes Bigramms - ABER nur, wenn die Zeilenparitaet stimmt.

    PARITAETS-PROBLEM (kritisch):
    - Bei GERADEM n enthaelt jede Spalte durchgehend dieselbe Bigramm-Haelfte
      (Spalte 0,2,4,... = 1. Haelfte; 1,3,5,... = 2. Haelfte).
    - Bei UNGERADEM n wechselt die Ausrichtung von Zeile zu Zeile: In Spalte c
      steht in Zeile 0 die 1. Haelfte, in Zeile 1 die 2. Haelfte usw.

    `parity` gibt an, welche Zeilen betrachtet werden (0 = gerade Zeilen,
    1 = ungerade Zeilen). Bei geradem n wird nur parity=0 genutzt.

    Gemessen wird die gegenseitige Information der Zeichenpaare (a[i], b[i]).
    """
    m = min(len(a), len(b))
    if m == 0:
        return 0.0
    idx = range(parity, m, 2) if parity >= 0 else range(m)
    aa = [a[i] for i in idx]
    bb = [b[i] for i in idx]
    if len(aa) < 2:
        return 0.0
    pairs = Counter(zip(aa, bb))
    total = sum(pairs.values())
    ca = Counter(aa)
    cb = Counter(bb)
    mi = 0.0
    for (x, y), c in pairs.items():
        pxy = c / total
        px = ca[x] / total
        py = cb[y] / total
        mi += pxy * math.log(pxy / (px * py))
    return mi


def bigram_affinity_phased(a: str, b: str, col_a: int, rows: int) -> float:
    """Phasenkorrekte Affinitaet fuer ungerades n.

    Bei ungeradem n haengt die Bigramm-Ausrichtung vom SPALTENINDEX ab:
    In Spalte c entspricht die k-te Zeile der 1. Bigramm-Haelfte, wenn
    (c * rows + k) gerade ist. Wir waehlen daher pro Spaltenpaar die
    passende Paritaet, statt global zu mitteln.

    Zusaetzlich: Bei unvollstaendigen Rasterzeilen (unterschiedliche
    Spaltenlaengen) verschiebt sich die Phase an den Raendern - wir
    beschraenken uns auf den gemeinsamen Bereich min(len(a), len(b)).
    """
    m = min(len(a), len(b))
    if m < 2:
        return 0.0
    # Phase aus dem Spaltenindex ableiten
    phase = (col_a * rows) % 2
    idx = range(phase, m, 2)
    aa = [a[i] for i in idx]
    bb = [b[i] for i in idx]
    if len(aa) < 2:
        return 0.0
    pairs = Counter(zip(aa, bb))
    total = sum(pairs.values())
    ca = Counter(aa)
    cb = Counter(bb)
    mi = 0.0
    for (x, y), c in pairs.items():
        pxy = c / total
        px = ca[x] / total
        py = cb[y] / total
        mi += pxy * math.log(pxy / (px * py))
    return mi


def order_columns(cols: list[str], n: int, beam: int = 3) -> list[int]:
    """Rekonstruiert die Spaltenreihenfolge per BEAM SEARCH ueber Affinitaet.

    Wir suchen die Permutation, die die Summe der Bigramm-Affinitaeten
    benachbarter Spalten maximiert (asymmetrisches TSP-artiges Problem).

    Statt reinem Greedy (das bei aehnlichen Affinitaeten frueh die falsche
    Kante waehlt) verfolgen wir die `beam` besten Teilpfade weiter. Das
    erhoeht die Erfolgsquote bei kurzen Geheimtexten (<400 Zeichen).

    WICHTIG: Bei asymmetrischer Matrix darf NICHT per Slice-Reversal
    optimiert werden (das dreht die Bigramm-Richtung um). Stattdessen wird
    ein Knoten herausgenommen und an anderer Stelle eingefuegt (Relocate).

    Bei ungeradem n haengt die Bigramm-Phase von der POSITION IM PFAD ab
    (nicht vom Spaltenindex): Die k-te Kante des Pfades entspricht der
    k-ten Rasterspalte, daher wird die Paritaet aus `pos_in_path` abgeleitet.
    """
    ncols = len(cols)
    rows = (len(cols[0]) if cols else 0)

    def get_affinity(i: int, j: int, pos_in_path: int) -> float:
        """Spezifische Affinitaet abhaengig von der aktuellen Position im Pfad."""
        if n % 2 == 1:
            # pos_in_path bestimmt, ob diese Spalte an ungerader/gerader
            # Stelle im Raster steht
            return bigram_affinity_phased(cols[i], cols[j], pos_in_path, rows)
        return bigram_affinity(cols[i], cols[j], 0)

    # --- Beam Search ---
    # Zustand: (score, pfad, restmenge)
    beams = [(0.0, [s], frozenset(range(ncols)) - {s}) for s in range(ncols)]

    for _ in range(ncols - 1):
        cands = []
        for score, path, remaining in beams:
            last = path[-1]
            current_pos = len(path) - 1  # Rang der aktuellen Kante im Pfad
            for nxt in remaining:
                edge_score = get_affinity(last, nxt, current_pos)
                cands.append((score + edge_score, path + [nxt],
                              remaining - {nxt}))
        cands.sort(reverse=True, key=lambda t: t[0])
        beams = cands[:beam]

    order = max(beams, key=lambda t: t[0])[1]

    # --- Relocate-Verbesserung mit dynamischem Re-Scoring ---
    def path_score(o: list[int]) -> float:
        return sum(get_affinity(o[k], o[k + 1], k) for k in range(len(o) - 1))

    improved = True
    while improved:
        improved = False
        for i in range(ncols):
            for j in range(ncols):
                if i == j:
                    continue
                cand = order[:]
                item = cand.pop(i)
                cand.insert(j, item)
                if path_score(cand) > path_score(order):
                    order = cand
                    improved = True

    return order


def order_to_perm(order: list[int]) -> list[int]:
    """Wandelt eine Lese-Reihenfolge in die Rangliste (perm) um.

    order[k] = Index der Spalte, die an k-ter Stelle ausgelesen wird.
    perm[c]  = Rang der Spalte c (kleiner Rang = frueher ausgelesen).
    """
    n = len(order)
    perm = [0] * n
    for rank, col in enumerate(order):
        perm[col] = rank
    return perm


# --------------------------------------------------------------------------
# Phase 3: Quadrat loesen (Haeufigkeit + n-Gramm, per Hill-Climbing)
# --------------------------------------------------------------------------

def decrypt_sq(bigrams: str, square: str) -> str:
    return "".join(
        square[ALPHA.index(bigrams[i]) * 6 + ALPHA.index(bigrams[i + 1])]
        for i in range(0, len(bigrams) - 1, 2)
    )


def solve_square(bigrams: str, restarts: int = 30, iterations: int = 60000,
                 seed: int = 0, budget: "Budget | None" = None) -> tuple[float, str, str]:
    """Loest das Quadrat per Hill-Climbing mit n-Gramm-Fitness.

    Bricht ab, sobald das uebergebene ``Budget`` erschoepft ist. Ohne
    Budget gilt die alte feste Iterationszahl (fuer Einzeltests).
    """
    rng = random.Random(seed)
    best = (-1e18, None, None)
    for _ in range(restarts):
        if budget is not None and budget.should_stop():
            break
        sq = list(FULL)
        rng.shuffle(sq)
        cur = langmodel.score(decrypt_sq(bigrams, "".join(sq)))
        for _ in range(iterations):
            if budget is not None and budget.should_stop():
                break
            i, j = rng.randrange(36), rng.randrange(36)
            if i == j:
                continue
            sq[i], sq[j] = sq[j], sq[i]
            sc = langmodel.score(decrypt_sq(bigrams, "".join(sq)))
            if budget is not None:
                budget.tick(sc)
            if sc >= cur:
                cur = sc
            else:
                sq[i], sq[j] = sq[j], sq[i]
        s = "".join(sq)
        if cur > best[0]:
            best = (cur, s, decrypt_sq(bigrams, s))
    return best


# --------------------------------------------------------------------------
# Gesamtpipeline
# --------------------------------------------------------------------------

def solve(ct: str, widths: list[int] | None = None, verbose: bool = True,
          quick: bool = True, lo: int = 12, hi: int = 26,
          seconds: float = 60.0):
    """Verschachtelte Pipeline: Breite x Reihenfolge x Quadrat.

    Da der IoC-Test bei Zufallsquadraten kein Signal liefert, wird die
    Spaltenbreite ueber den n-Gramm-Score bestimmt: Fuer JEDE Breite im
    Bereich [lo, hi] wird die Reihenfolge rekonstruiert und das Quadrat
    geloest. Die Breite mit dem besten Score gewinnt.

    Das gesamte Budget ``seconds`` wird gleichmaessig auf die Breiten
    verteilt, damit die Pipeline garantiert durchlaeuft.
    """
    ct = clean(ct)
    if widths is None:
        widths = list(range(lo, hi + 1))
    per_width = max(2.0, seconds / max(1, len(widths)))
    results = []
    for n in widths:
        budget = Budget(max_seconds=per_width, patience=8000)
        cols = split_columns(ct, n)
        order = order_columns(cols, n)
        perm = order_to_perm(order)
        bigrams = untranspose(ct, perm)
        if quick:
            sc, sq, pt = solve_square(bigrams, restarts=4, iterations=12000,
                                      budget=budget)
        else:
            sc, sq, pt = solve_square(bigrams, budget=budget)
        results.append((sc, n, perm, sq, pt))
        if verbose:
            print(f"  n={n:2d}  score={sc:7.2f}  {pt[:60]}")
    results.sort(reverse=True, key=lambda r: r[0])
    return results


def main() -> None:
    import sys

    page = sys.argv[1] if len(sys.argv) > 1 else "171"
    seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
    ct = clean(CORPUS[page])
    print("=" * 100)
    print(f"Friedman-Solver: Seite {page} ({len(ct)} Zeichen), "
          f"Zeitbudget {seconds:.0f}s")
    if page in SOLVED:
        print(f"  (geloest mit Schluessel {SOLVED[page][0]})")
    print("=" * 100)

    print("\nPhase 1 (Diagnose): Spaltenbreiten-Kandidaten (IoC + Lag):")
    for score, n, ci, lag in best_widths(ct):
        print(f"  n={n:2d}  IoC={ci:.4f}  Lag={lag:.4f}  Score={score:.4f}")
    print("  (Hinweis: bei Zufallsquadraten liefert IoC kein Signal -")
    print("   die Breite wird ueber den n-Gramm-Score bestimmt.)")

    print("\nPhase 2+3: Breite x Reihenfolge x Quadrat (verschachtelt):")
    results = solve(ct, seconds=seconds)

    sc, n, perm, sq, pt = results[0]
    print("\n" + "=" * 100)
    print(f"BESTES ERGEBNIS: n={n}  score={sc:.2f}")
    print(f"  perm = {perm}")
    print(f"  quadrat = {sq}")
    print(f"  klartext = {pt}")


if __name__ == "__main__":
    main()
