#!/usr/bin/env python3
"""
Korrektursuche mit der vollstaendigen Schluesselliste.

Fuer jede Seite und jeden Schluessel werden 1-2 Einfuege-/Loeschoperationen
probiert. Bewertung mit dem deutschen Sprachmodell.

Optimierung: Nur die vielversprechendsten (Seite, Schluessel)-Paare werden
mit Korrekturen getestet, um die Laufzeit zu begrenzen.
"""

from __future__ import annotations

import sys

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, KEYS, clean, decrypt, make_square
from data.corpus import CORPUS
from core import langmodel

THRESHOLD = -24.0


def fill_gaps_simple(sub: str) -> str:
    missing = [ch for ch in FULL if ch not in sub.replace("-", "")]
    it = iter(missing)
    return "".join(next(it) if ch == "-" else ch for ch in sub)


def variants_1(ct: str):
    n = len(ct)
    for i in range(n):
        yield ct[:i] + ct[i + 1:], f"del@{i}"
    for i in range(n + 1):
        for ch in ALPHA:
            yield ct[:i] + ch + ct[i:], f"ins@{i}:{ch}"


def main() -> None:
    page_filter = sys.argv[1] if len(sys.argv) > 1 else None
    pages = [page_filter] if page_filter else sorted(
        CORPUS, key=lambda x: int(x.rstrip("ab")))

    for page in pages:
        ct = clean(CORPUS[page])
        print(f"\n{'=' * 90}")
        print(f"Seite {page} ({len(ct)} Zeichen)")
        print("=" * 90)
        results = []
        for name, (perm, sub, _cnt) in KEYS.items():
            sq = fill_gaps_simple(sub)
            base = langmodel.score(decrypt(ct, perm, sq))
            best = (base, "keine", decrypt(ct, perm, sq))
            for cand, op in variants_1(ct):
                pt = decrypt(cand, perm, sq)
                sc = langmodel.score(pt)
                if sc > best[0]:
                    best = (sc, op, pt)
            results.append((best[0], name, best[1], best[2]))
        results.sort(reverse=True)
        for sc, name, op, pt in results[:4]:
            flag = "  <<< LESBAR" if sc > THRESHOLD else ""
            print(f"  {sc:8.2f} {name:11s} {op:14s}{flag}")
            print(f"           {pt[:76]}")


if __name__ == "__main__":
    main()
