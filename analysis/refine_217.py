#!/usr/bin/env python3
"""
VERFEINERUNG: Welche Transpositionskonvention liefert lesbaren Text?

Beobachtung: asc_back liefert score -16.7 (SA) bzw -21.1 (nachgeprueft),
mit erkennbaren deutschen Fragmenten (EIN EIGANT... ER KREUZER... THEIS...).

Das ist NAH DRAN. Wir testen systematisch:
  - Zeichen-Ebene vs Bigramm-Ebene
  - asc/desc Rang
  - pad front/back
  - Spalten-Reihenfolge beim Auslesen
  - Zeilen-Reihenfolge

Und wir nutzen einen STAERKEREN Solver (mehr Restarts, laenger).
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


def col_lengths(length, n, pad_front):
    rows = (length + n - 1) // n
    rest = length % n
    if rest == 0:
        rest = n
    if pad_front:
        return [rows - 1 if i < n - rest else rows for i in range(n)]
    return [rows if i < rest else rows - 1 for i in range(n)]


def untranspose(ct, key, *, level="char", descending=False, pad_front=False,
                read_col_major=False, row_rev=False, col_rev=False):
    """level='char': ct sind Zeichen. level='bigram': ct sind Bigramme."""
    n = len(key)
    if level == "char":
        units = list(ct)
    else:
        units = [ct[i:i + 2] for i in range(0, len(ct) - 1, 2)]
    length = len(units)
    collen = col_lengths(length, n, pad_front)
    order = sorted(range(n), key=lambda c: (key[c], c))
    if descending:
        order = order[::-1]
    cols = [None] * n
    pos = 0
    for c in order:
        cols[c] = units[pos:pos + collen[c]]
        pos += collen[c]
    rows = max(len(c) for c in cols)
    out = []
    rng = range(rows - 1, -1, -1) if row_rev else range(rows)
    for r in rng:
        crng = range(n - 1, -1, -1) if col_rev else range(n)
        for c in crng:
            if r < len(cols[c]):
                out.append(cols[c][r])
    if level == "char":
        return "".join(out)
    return "".join(out)


def decode(bigrams, square):
    return "".join(square[ALPHA.index(b[0]) * 6 + ALPHA.index(b[1])] for b in bigrams)


def fitness(text, lam=0.15):
    return langmodel.score(text) + lam * langmodel.word_hits(text)


def solve_square(bigrams, *, restarts=25, iterations=60000, seed=0, lam=0.15):
    rng = random.Random(seed)
    best = (-1e18, "", "")
    for r in range(restarts):
        sq = list(FULL)
        rng.shuffle(sq)
        cur = "".join(sq)
        cur_pt = decode(bigrams, cur)
        cur_sc = fitness(cur_pt, lam)
        temp = 4.0
        for it in range(iterations):
            i, j = rng.randrange(36), rng.randrange(36)
            if i == j:
                continue
            sq[i], sq[j] = sq[j], sq[i]
            cand = "".join(sq)
            cand_pt = decode(bigrams, cand)
            cand_sc = fitness(cand_pt, lam)
            if cand_sc > cur_sc or rng.random() < pow(2.718281828, (cand_sc - cur_sc) / temp):
                cur, cur_pt, cur_sc = cand, cand_pt, cand_sc
            else:
                sq[i], sq[j] = sq[j], sq[i]
            temp = max(0.05, temp * 0.99995)
        if cur_sc > best[0]:
            best = (cur_sc, cur, cur_pt)
    return best


def main():
    print("=" * 78)
    print("SYSTEMATISCHER TEST: Transpositionskonventionen")
    print("=" * 78)
    results = []
    for level in ["char", "bigram"]:
        for desc in [False, True]:
            for pf in [False, True]:
                for rcm in [False, True]:
                    for rr in [False, True]:
                        for cr in [False, True]:
                            sub = untranspose(CT, KEY, level=level, descending=desc,
                                              pad_front=pf, read_col_major=rcm,
                                              row_rev=rr, col_rev=cr)
                            if level == "char":
                                bgs = [sub[i:i + 2] for i in range(0, len(sub) - 1, 2)]
                            else:
                                bgs = [sub[i:i + 2] for i in range(0, len(sub) - 1, 2)]
                            sc, sq, pt = solve_square(bgs, restarts=6, iterations=25000, seed=7)
                            hits = langmodel.word_hits(pt)
                            name = f"{level}/{('desc' if desc else 'asc')}/{('front' if pf else 'back')}/{'rcm' if rcm else 'rm'}/{'rr' if rr else 'fr'}/{'cr' if cr else 'fc'}"
                            results.append((sc, hits, name, sq, pt))
    results.sort(reverse=True)
    print("\nTOP 10:")
    for sc, hits, name, sq, pt in results[:10]:
        print(f"  {sc:7.3f} hits={hits:3d}  {name}")
        print(f"      {pt[:72]}")
    print("\nBOTTOM 3:")
    for sc, hits, name, sq, pt in results[-3:]:
        print(f"  {sc:7.3f} hits={hits:3d}  {name}")
    print()
    print("=" * 78)
    print("BESTES:")
    sc, hits, name, sq, pt = results[0]
    print(f"  {name}  score={sc:.3f} hits={hits}")
    print(f"  Quadrat : {sq}")
    print(f"  Klartext: {pt}")
    print(f"  Quadrat[5]={sq[5]} (AV->E erwartet: E) -> {'PASS' if sq[5]=='E' else 'FAIL'}")


if __name__ == "__main__":
    main()
