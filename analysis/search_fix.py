#!/usr/bin/env python3
"""
Systematische Suche: Seite x Schluessel x Korrektur.

Fuer jede Seite und jeden bekannten Schluessel wird geprueft, ob eine
Einfuege-/Loeschoperation an EINER Position den Klartext lesbar macht.
Bewertung mit dem echten deutschen Sprachmodell (langmodel.score).

Schwellwert: Score > -24 gilt als "lesbar" (echter Klartext liegt bei
-16 bis -22, Zufall bei -27 bis -35).
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, KEYS, clean, decrypt, make_square
from data.corpus import CORPUS
from core import langmodel

THRESHOLD = -24.0


def variants(ct: str):
    """Alle Ein-Zeichen-Varianten: Loeschen oder Einfuegen."""
    n = len(ct)
    for i in range(n):
        yield ct[:i] + ct[i + 1:], f"del@{i}"
    for i in range(n + 1):
        for ch in ALPHA:
            yield ct[:i] + ch + ct[i:], f"ins@{i}:{ch}"


def main() -> None:
    results = []
    for page in sorted(CORPUS, key=lambda x: int(x.rstrip("ab"))):
        ct = clean(CORPUS[page])
        best = (-1e18, None, None, None)
        for name, (perm, sub, _cnt) in KEYS.items():
            sq = make_square(sub)
            # ohne Korrektur
            pt = decrypt(ct, perm, sq)
            sc = langmodel.score(pt)
            if sc > best[0]:
                best = (sc, name, "keine", pt)
            # mit Korrektur
            for cand, op in variants(ct):
                pt = decrypt(cand, perm, sq)
                sc = langmodel.score(pt)
                if sc > best[0]:
                    best = (sc, name, op, pt)
        sc, name, op, pt = best
        flag = "  <<< LESBAR" if sc > THRESHOLD else ""
        results.append((page, sc, name, op, pt))
        print(f"{page:6s} {sc:8.3f} {name:10s} {op:14s}{flag}")
        print(f"       {pt[:72]}")

    print()
    print("=" * 78)
    print(f"LESBARE SEITEN (Score > {THRESHOLD}):")
    print("=" * 78)
    for page, sc, name, op, pt in results:
        if sc > THRESHOLD:
            print(f"\nSeite {page} / {name} / {op}  (Score {sc:.2f})")
            print(f"  {pt}")


if __name__ == "__main__":
    main()
