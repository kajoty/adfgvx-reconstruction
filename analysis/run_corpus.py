#!/usr/bin/env python3
"""Testet alle Kryptogramme des Korpus gegen alle bekannten Schluessel."""

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import KEYS, clean, decrypt, group, score_german
from data.corpus import CORPUS


def main() -> None:
    print("=" * 78)
    print("ADFGVX-Korpus gegen bekannte Schluessel testen")
    print("=" * 78)
    print()

    hits: list[tuple[str, str, float, str]] = []

    for page, raw in CORPUS.items():
        ct = clean(raw)
        print(f"--- Seite {page} ({len(ct)} Zeichen, {len(ct)//2} Klartextzeichen) ---")
        results = []
        for name, (perm, sub, _cnt) in KEYS.items():
            if len(sub) != 36:
                continue
            pt = decrypt(ct, perm, sub)
            results.append((score_german(pt), name, pt))
        results.sort(reverse=True)
        for sc, name, pt in results[:3]:
            marker = ""
            if sc > 0.5:
                marker = "  <<< LESBAR?"
                hits.append((page, name, sc, pt))
            print(f"  {name:10s} score={sc:6.2f}  {pt[:60]}{marker}")
        print()

    print("=" * 78)
    print("TREFFER (score > 0.5)")
    print("=" * 78)
    if not hits:
        print("Keine.")
    for page, name, sc, pt in hits:
        print(f"\nSeite {page} / {name} (score {sc:.2f}):")
        print(f"  {pt}")


if __name__ == "__main__":
    main()
