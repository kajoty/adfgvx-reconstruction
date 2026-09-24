#!/usr/bin/env python3
"""
NEUER LOESUNGSANSATZ fuer Seite 217.

KERNIDEE (Korrektur einer falschen Annahme):
  Der Artikel sagt NICHT, dass das Quadrat aus TRUPPENVERSCHIEBUNG gebaut wird.
  Er sagt:
    - TRUPPENVERSCHIEBUNG ist das TRANSPOSITIONSWORT (19 Buchstaben)
    - Das Quadrat wird separat GEZEIGT (Bild)
    - AV -> E ist ein Beispiel aus diesem Quadrat

  Bisher wurde faelschlich angenommen: Quadrat = make_square(TRUPPENVERSCHIEBUNG).
  Das ist falsch. Das Quadrat ist UNBEKANNT.

ZWEITE KORREKTUR:
  Der Artikel beschreibt 19 Spalten a 9 ZEICHEN (Zeichen-Ebene).
  adfgvx.py transponiert aber BIGRAMME. Das ist eine andere Konvention!

  Bei Zeichen-Ebene: 170 Zeichen -> 19 Spalten (18x9 + 1x8)
  Bei Bigramm-Ebene: 85 Bigramme -> 19 Spalten (85 = 4*19 + 9 -> 9x5 + 10x4)

  Der Artikel sagt explizit "18 columns with 9 symbols each and 1 column
  with 8 symbols" -> das ist ZEICHEN-Ebene (170 Zeichen).

LOESUNGSWEG:
  1. Transposition rueckgaengig machen (Transpositionswort bekannt)
     -> ergibt die substituierte Zeichenfolge (170 Zeichen)
  2. Substitution loesen: 36x36-Quadrat finden, das lesbaren Text ergibt
     -> das ist ein monoalphabetisches Substitutionsproblem auf Bigrammen
  3. Constraint: AV -> E (Quadrat[5] = 'E')

WICHTIG: Nach Schritt 1 haben wir 170 Zeichen = 85 Bigramme.
Die Substitution bildet jedes Bigramm auf ein Klartextzeichen ab.
"""

from __future__ import annotations

import random

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, clean
from data.corpus import CORPUS
from core import langmodel

KEY = "TRUPPENVERSCHIEBUNG"
CT = clean(CORPUS["217"])
N = len(KEY)
L = len(CT)


def untranspose_chars(ct: str, key: str, *, descending: bool = False,
                      pad_front: bool = False) -> str:
    """Macht die Spaltentransposition auf ZEICHEN-Ebene rueckgaengig.

    Der Artikel: 19 Spalten, 18x9 + 1x8 Zeichen. Spalten werden nach
    Rang ausgelesen (T=Rang15 bei Pos 134).
    """
    n = len(key)
    length = len(ct)
    rows = (length + n - 1) // n
    rest = length % n
    if rest == 0:
        rest = n
    if pad_front:
        collen = [rows - 1 if i < n - rest else rows for i in range(n)]
    else:
        collen = [rows if i < rest else rows - 1 for i in range(n)]
    order = sorted(range(n), key=lambda c: (key[c], c))
    if descending:
        order = order[::-1]
    cols: list[str] = [""] * n
    pos = 0
    for c in order:
        cols[c] = ct[pos:pos + collen[c]]
        pos += collen[c]
    return "".join(cols[c][r] for r in range(rows) for c in range(n)
                   if r < len(cols[c]))


def bigrams_of(s: str) -> list[str]:
    return [s[i:i + 2] for i in range(0, len(s) - 1, 2)]


def decode(bigrams: list[str], square: str) -> str:
    return "".join(square[ALPHA.index(b[0]) * 6 + ALPHA.index(b[1])]
                   for b in bigrams)


def fitness(text: str, lam: float = 0.15) -> float:
    return langmodel.score(text) + lam * langmodel.word_hits(text)


def solve_square(bigrams: list[str], *, restarts: int = 30,
                 iterations: int = 80000, seed: int = 0,
                 lam: float = 0.15, verbose: bool = False) -> tuple[float, str, str]:
    """Simulated Annealing auf dem 36x36-Quadrat."""
    rng = random.Random(seed)
    best_sc = -1e18
    best_sq = ""
    best_pt = ""
    for r in range(restarts):
        square = list(FULL)
        rng.shuffle(square)
        cur = "".join(square)
        cur_pt = decode(bigrams, cur)
        cur_sc = fitness(cur_pt, lam)
        temp = 4.0
        for it in range(iterations):
            i, j = rng.randrange(36), rng.randrange(36)
            if i == j:
                continue
            square[i], square[j] = square[j], square[i]
            cand = "".join(square)
            cand_pt = decode(bigrams, cand)
            cand_sc = fitness(cand_pt, lam)
            if cand_sc > cur_sc or rng.random() < pow(2.718281828, (cand_sc - cur_sc) / temp):
                cur, cur_pt, cur_sc = cand, cand_pt, cand_sc
            else:
                square[i], square[j] = square[j], square[i]
            temp *= 0.99995
            if temp < 0.05:
                temp = 0.05
        if cur_sc > best_sc:
            best_sc, best_sq, best_pt = cur_sc, cur, cur_pt
        if verbose:
            print(f"  Restart {r:2d}: score={cur_sc:7.3f} hits={langmodel.word_hits(cur_pt):3d}")
    return best_sc, best_sq, best_pt


def main() -> None:
    print("=" * 78)
    print("NEUER ANSATZ: Zeichen-Ebene-Transposition + unbekanntes Quadrat")
    print("=" * 78)
    print(f"Chiffrat: {L} Zeichen")
    print(f"Transpositionswort: {KEY} ({N} Buchstaben)")
    print()

    # Schritt 1: Transposition rueckgaengig machen
    print("-" * 78)
    print("SCHRITT 1: Transposition rueckgaengig machen (Zeichen-Ebene)")
    print("-" * 78)
    variants = {}
    for desc in [False, True]:
        for pf in [False, True]:
            sub = untranspose_chars(CT, KEY, descending=desc, pad_front=pf)
            name = f"{'desc' if desc else 'asc'}_{'front' if pf else 'back'}"
            variants[name] = sub
            print(f"  {name:<12}: {sub[:50]}")
    print()

    # Schritt 2: Substitution loesen fuer jede Variante
    print("-" * 78)
    print("SCHRITT 2: Quadrat loesen (Simulated Annealing)")
    print("-" * 78)
    overall_best = None
    for name, sub in variants.items():
        bgs = bigrams_of(sub)
        print(f"\n  Variante {name} ({len(bgs)} Bigramme):")
        sc, sq, pt = solve_square(bgs, restarts=10, iterations=40000,
                                  seed=1, verbose=False)
        hits = langmodel.word_hits(pt)
        print(f"    score={sc:7.3f}  hits={hits:3d}")
        print(f"    Quadrat: {sq}")
        print(f"    Klartext: {pt[:70]}")
        if overall_best is None or sc > overall_best[0]:
            overall_best = (sc, name, sq, pt)

    print()
    print("=" * 78)
    print("BESTES ERGEBNIS")
    print("=" * 78)
    sc, name, sq, pt = overall_best
    print(f"  Variante: {name}")
    print(f"  score   : {sc:.3f}  (echter Text: -16..-21)")
    print(f"  hits    : {langmodel.word_hits(pt)}")
    print(f"  Quadrat : {sq}")
    print(f"  Klartext: {pt}")
    print()
    print(f"  Quadrat[5] = {sq[5]}  (Artikel: AV -> E, also Quadrat[5]='E')")
    print(f"  -> {'PASS' if sq[5] == 'E' else 'FAIL'}")


if __name__ == "__main__":
    main()
