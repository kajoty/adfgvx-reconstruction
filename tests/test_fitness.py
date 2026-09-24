#!/usr/bin/env python3
"""Testet die Fitness-Funktion gegen bekannten Klartext vs. Zufall."""

import random
import string

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import score_german

KNOWN = "KEINESTOERFNGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCHAUFBELGRADX"
KNOWN2 = "KEINESTOERUNGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCHAUFBELGRADX"

print("Bekannter Klartext (mit OCR-Fehlern):")
print(f"  {score_german(KNOWN):8.3f}  {KNOWN}")
print("Bekannter Klartext (korrigiert):")
print(f"  {score_german(KNOWN2):8.3f}  {KNOWN2}")

print("\nZufallstext (20 Durchlaeufe):")
random.seed(42)
vals = []
for _ in range(20):
    rnd = "".join(random.choice(string.ascii_uppercase + string.digits)
                  for _ in range(len(KNOWN2)))
    vals.append(score_german(rnd))
print(f"  min={min(vals):8.3f}  max={max(vals):8.3f}  avg={sum(vals)/len(vals):8.3f}")

print("\nDeutscher Klartext (Beispiele):")
for t in [
    "DIEINFANTERIEISTANGETRETENUNDWIRDMORGENFRUEHANGREIFEN",
    "KEINFEINDLICHERWIDERSTANDMEHRZUFESTSTELLENABSCHNITTGERAEUMT",
    "ARTILLERIEFEUERLIEGTAUFDEMHOHENWEGNORDLICHDERSTRASSE",
]:
    print(f"  {score_german(t):8.3f}  {t}")
