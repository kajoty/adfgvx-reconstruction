#!/usr/bin/env python3
"""
Systematische Suche mit der vollstaendigen Lasry-Schluesselliste.

Fuer jede Seite wird jeder Schluessel getestet. Schluessel mit Luecken ('-')
werden zunaechst mit dem Restalphabet aufgefuellt; zusaetzlich wird die
Lueckenposition variiert, falls noetig.

Bewertung mit dem deutschen Sprachmodell.
"""

from __future__ import annotations

from itertools import permutations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, KEYS, clean, decrypt, untranspose
from data.corpus import CORPUS
from core import langmodel

THRESHOLD = -24.0


def fill_gaps(sub: str) -> list[str]:
    """Erzeugt Kandidaten fuer ein Quadrat mit Luecken.

    '-' wird durch die fehlenden Zeichen des Alphabets ersetzt. Bei wenigen
    Luecken werden alle Permutationen der fehlenden Zeichen probiert.
    """
    missing = [ch for ch in FULL if ch not in sub.replace("-", "")]
    gaps = sub.count("-")
    if gaps == 0:
        return [sub]
    if gaps > 6:
        # zu viele Luecken: nur eine Auffuellung (Restalphabet in Reihenfolge)
        out = []
        it = iter(missing)
        for ch in sub:
            out.append(next(it) if ch == "-" else ch)
        return ["".join(out)]
    results = []
    for perm in permutations(missing, gaps):
        it = iter(perm)
        results.append("".join(next(it) if ch == "-" else ch for ch in sub))
    return results


def main() -> None:
    print("=" * 100)
    print("Systematische Suche: Seite x Schluessel (mit Luecken-Auffuellung)")
    print("=" * 100)

    hits = []
    for page in sorted(CORPUS, key=lambda x: int(x.rstrip("ab"))):
        ct = clean(CORPUS[page])
        best = (-1e18, None, None, None)
        for name, (perm, sub, _cnt) in KEYS.items():
            for sq in fill_gaps(sub):
                pt = decrypt(ct, perm, sq)
                sc = langmodel.score(pt)
                if sc > best[0]:
                    best = (sc, name, sq, pt)
        sc, name, sq, pt = best
        flag = "  <<< LESBAR" if sc > THRESHOLD else ""
        if sc > THRESHOLD:
            hits.append((page, name, sq, sc, pt))
        print(f"{page:6s} {sc:8.2f} {name:11s}{flag}")
        print(f"       {pt[:80]}")

    print()
    print("=" * 100)
    print(f"LESBARE SEITEN (Score > {THRESHOLD}): {len(hits)}")
    print("=" * 100)
    for page, name, sq, sc, pt in hits:
        print(f"\nSeite {page} / {name}  (Score {sc:.2f})")
        print(f"  Quadrat: {sq}")
        print(f"  Klartext: {pt}")


if __name__ == "__main__":
    main()
