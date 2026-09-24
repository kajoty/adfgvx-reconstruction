#!/usr/bin/env python3
"""
Erschoepfende Suche nach der Konvention, die Seite 217 mit dem
Artikel-Schluessel TRUPPENVERSCHIEBUNG entschluesselt.

Der Artikel beschreibt:
  - 19 Spalten, 18x9 + 1x8 Zeichen (Zeichen-Ebene!)
  - Spalten werden nach Rang ausgelesen (T=Rang15 bei Pos 134, R=Rang12 bei 107)
  - Quadrat aus TRUPPENVERSCHIEBUNG, AV -> E

Getestet wird die VOLLSTAENDIGE Matrix:
  - Ebene: Zeichen (170) oder Bigramme (85)
  - Spaltenreihenfolge im Chiffrat: Rang aufsteigend / absteigend /
    Wortreihenfolge / Wortreihenfolge rueckwaerts
  - Klartext-Leserichtung: zeilenweise / spaltenweise
  - Zeilenrichtung: vorwaerts / rueckwaerts
  - Spaltenrichtung: vorwaerts / rueckwaerts
  - Padding: kurze Spalte vorne / hinten

Zusaetzlich: Brute-Force ueber ALLE 19! Spaltenreihenfolgen ist zu gross,
aber wir koennen pruefen, ob es ueberhaupt eine Permutation gibt, die
lesbaren Text liefert — via Hillclimbing auf der Spaltenreihenfolge.
"""

from __future__ import annotations

import itertools
import random

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, clean, make_square
from data.corpus import CORPUS
from core import langmodel

KEY = "TRUPPENVERSCHIEBUNG"
CT = clean(CORPUS["217"])
SQ = make_square(KEY)
N = len(KEY)
L = len(CT)

PT_CLAIM = "EINENGLISCHERKREUZEREINLIEGXSEWASTOPOLXS4STENXEINGESCHWADERDERXALLIIERTENFOLGT26STENX"


def col_lengths(length: int, n: int, pad_front: bool) -> list[int]:
    rows = (length + n - 1) // n
    rest = length % n
    if rest == 0:
        rest = n
    if pad_front:
        return [rows - 1 if i < n - rest else rows for i in range(n)]
    return [rows if i < rest else rows - 1 for i in range(n)]


def rank_order(key: str, descending: bool) -> list[int]:
    n = len(key)
    o = sorted(range(n), key=lambda c: (key[c], c))
    return o[::-1] if descending else o


def decrypt_with_order(ct: str, order: list[int], *, level: str,
                       read_col_major: bool, row_rev: bool, col_rev: bool,
                       pad_front: bool) -> str:
    """Entschluesselt mit explizit gegebener Spaltenreihenfolge `order`."""
    unit = 1 if level == "char" else 2
    n_units = len(ct) // unit
    units = [ct[i * unit:(i + 1) * unit] for i in range(n_units)]
    collen = col_lengths(n_units, N, pad_front)

    cols: list[list[str]] = [[] for _ in range(N)]
    pos = 0
    for c in order:
        cols[c] = units[pos:pos + collen[c]]
        pos += collen[c]

    rows = (n_units + N - 1) // N
    seq: list[str] = []
    if read_col_major:
        col_iter = range(N - 1, -1, -1) if col_rev else range(N)
        for c in col_iter:
            r_iter = range(len(cols[c]) - 1, -1, -1) if row_rev else range(len(cols[c]))
            for r in r_iter:
                seq.append(cols[c][r])
    else:
        r_iter = range(rows - 1, -1, -1) if row_rev else range(rows)
        col_iter = range(N - 1, -1, -1) if col_rev else range(N)
        for r in r_iter:
            for c in col_iter:
                if r < len(cols[c]):
                    seq.append(cols[c][r])
    joined = "".join(seq)
    return "".join(SQ[ALPHA.index(joined[i]) * 6 + ALPHA.index(joined[i + 1])]
                   for i in range(0, len(joined) - 1, 2))


def main() -> None:
    print("=" * 78)
    print("ERSCHOEPFENDE SUCHE: Seite 217 mit TRUPPENVERSCHIEBUNG")
    print("=" * 78)
    print(f"Chiffrat: {L} Zeichen, {L // 2} Bigramme")
    print(f"Behaupteter Klartext: {len(PT_CLAIM)} Zeichen")
    print()

    orders = {
        "rank_asc": rank_order(KEY, False),
        "rank_desc": rank_order(KEY, True),
        "word": list(range(N)),
        "word_rev": list(range(N - 1, -1, -1)),
    }

    results = []
    for oname, order in orders.items():
        for level in ["char", "bigram"]:
            for read_col_major in [False, True]:
                for row_rev in [False, True]:
                    for col_rev in [False, True]:
                        for pad_front in [False, True]:
                            pt = decrypt_with_order(
                                CT, order, level=level,
                                read_col_major=read_col_major,
                                row_rev=row_rev, col_rev=col_rev,
                                pad_front=pad_front)
                            sc = langmodel.score(pt)
                            hits = langmodel.word_hits(pt)
                            results.append((sc, hits, oname, level,
                                            read_col_major, row_rev, col_rev,
                                            pad_front, pt))

    results.sort(reverse=True)
    print(f"Getestete Varianten: {len(results)}")
    print()
    print("TOP 10:")
    print(f"{'Score':>8} {'hits':>5}  {'order':<10} {'Ebene':<7} "
          f"{'read':<5} {'rowrev':<7} {'colrev':<7} {'pad':<6} Klartext")
    print("-" * 78)
    for sc, hits, oname, level, rcm, rr, cr, pf, pt in results[:10]:
        print(f"{sc:>8.3f} {hits:>5}  {oname:<10} {level:<7} "
              f"{'col' if rcm else 'row':<5} {str(rr):<7} {str(cr):<7} "
              f"{'front' if pf else 'back':<6} {pt[:30]}")

    print()
    print(f"BESTER Score: {results[0][0]:.3f} (echter Text: -16..-21)")
    print(f"BESTE hits : {results[0][1]} (echter Text Seite 217 unbekannt, "
          f"Seite 171: 123 bei 157 Zeichen)")
    print()

    # --- Vergleich: Was waere der Score, wenn der behauptete Klartext
    #     tatsaechlich der Klartext waere?
    print("-" * 78)
    print("REFERENZ: Score des BEHAUPTETEN Klartexts")
    print("-" * 78)
    print(f"  score = {langmodel.score(PT_CLAIM):.3f}")
    print(f"  hits  = {langmodel.word_hits(PT_CLAIM)}")
    print()
    print("  -> Wenn der behauptete Klartext echt waere, muesste die")
    print("     Entschluesselung diesen Score erreichen.")
    print()

    # --- Hillclimbing auf der Spaltenreihenfolge -------------------------
    print("-" * 78)
    print("HILLCLIMBING auf der Spaltenreihenfolge (Zeichen-Ebene, row-major)")
    print("-" * 78)
    rng = random.Random(1)
    best_overall = None
    for restart in range(30):
        order = list(range(N))
        rng.shuffle(order)
        cur = decrypt_with_order(CT, order, level="char",
                                 read_col_major=False, row_rev=False,
                                 col_rev=False, pad_front=False)
        cur_sc = langmodel.score(cur)
        improved = True
        while improved:
            improved = False
            for i in range(N):
                for j in range(i + 1, N):
                    order[i], order[j] = order[j], order[i]
                    cand = decrypt_with_order(CT, order, level="char",
                                              read_col_major=False,
                                              row_rev=False, col_rev=False,
                                              pad_front=False)
                    sc = langmodel.score(cand)
                    if sc > cur_sc:
                        cur_sc = sc
                        cur = cand
                        improved = True
                    else:
                        order[i], order[j] = order[j], order[i]
        if best_overall is None or cur_sc > best_overall[0]:
            best_overall = (cur_sc, list(order), cur)
    print(f"  Bestes Ergebnis: score={best_overall[0]:.3f}")
    print(f"  Reihenfolge: {best_overall[1]}")
    print(f"  Klartext: {best_overall[2][:60]}")
    print(f"  hits: {langmodel.word_hits(best_overall[2])}")
    print()
    print("  -> Wenn Hillclimbing ueber ALLE Spaltenreihenfolgen nur")
    print("     Zufallsniveau erreicht, ist der Schluessel falsch.")


if __name__ == "__main__":
    main()
