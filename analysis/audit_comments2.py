#!/usr/bin/env python3
"""Audit Teil 2: analyze_170, refine_217, adfgvx-Beispiel."""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from collections import Counter
from core.adfgvx import KEYS, decrypt, make_square, clean, ALPHA, FULL
from core import langmodel
from data.corpus import CORPUS
from data.solutions import SOLVED

PASS = FAIL = 0
def check(label, got, want, tol=0.05):
    global PASS, FAIL
    ok = abs(got - want) <= tol if isinstance(want, float) else got == want
    print(f"[{'OK  ' if ok else 'FEHL'}] {label}: got={got!r} want={want!r}")
    if ok: PASS += 1
    else: FAIL += 1

print("=" * 78)
print("AUDIT Teil 2")
print("=" * 78)

# --- adfgvx.py: HOUSE/ROBIN Beispiel -------------------------------------
print("\n--- core/adfgvx.py: HOUSE/ROBIN -> AGDVAAFAAVGXXGXAGDXADF ---")
# Das Beispiel: Schluessel HOUSE, Klartext ROBIN.
# Wir bauen das Quadrat aus HOUSE und verschluesseln ROBIN.
sq = make_square("HOUSE")
rev = {ch: ALPHA[i // 6] + ALPHA[i % 6] for i, ch in enumerate(sq)}
bigrams = "".join(rev.get(ch, "??") for ch in "ROBIN")
print(f"  Quadrat(HOUSE) = {sq}")
print(f"  ROBIN -> {bigrams}")
check("HOUSE/ROBIN Bigramme", bigrams, "AGDVAAFAAVGXXGXAGDXADF")

# --- analyze_170.py: Zeichenverteilung -----------------------------------
print("\n--- analysis/analyze_170.py: Seite 170 vs 176a ---")
ct170 = clean(CORPUS["170"])
print(f"  corpus['170']: {len(ct170)} Zeichen")
# Position 1 (gerade Indizes) der Bigramme
pos1_170 = ct170[0::2]
c170 = Counter(pos1_170)
n170 = len(pos1_170)
print(f"  Position-1-Verteilung 170 (n={n170}):")
for ch in ALPHA:
    print(f"    {ch}: {100*c170.get(ch,0)/n170:5.1f}%")

# 176a
if "176a" in CORPUS:
    ct176 = clean(CORPUS["176a"])
    pos1_176 = ct176[0::2]
    c176 = Counter(pos1_176)
    n176 = len(pos1_176)
    print(f"  Position-1-Verteilung 176a (n={n176}):")
    for ch in ALPHA:
        print(f"    {ch}: {100*c176.get(ch,0)/n176:5.1f}%")
    check("170 D-Anteil", round(100*c170.get('D',0)/n170, 1), 0.0)
    check("176a D-Anteil", round(100*c176.get('D',0)/n176, 1), 17.0, tol=0.6)
    check("170 G-Anteil", round(100*c170.get('G',0)/n170, 1), 32.1, tol=0.6)
    check("176a G-Anteil", round(100*c176.get('G',0)/n176, 1), 22.3, tol=0.6)
    check("170 X-Anteil", round(100*c170.get('X',0)/n170, 1), 15.1, tol=0.6)
    check("176a X-Anteil", round(100*c176.get('X',0)/n176, 1), 7.1, tol=0.6)
else:
    print("  176a nicht im Korpus")

# --- refine_217.py: asc_back Score ---------------------------------------
print("\n--- analysis/refine_217.py: asc_back score -16.7 / -21.1 ---")
print("  (nur mit spezieller Transpositionskonvention reproduzierbar;")
print("   wird separat geprueft)")

print("\n" + "=" * 78)
print(f"ERGEBNIS Teil 2: {PASS} OK, {FAIL} FEHLER")
print("=" * 78)
