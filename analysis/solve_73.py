"""Loesungsversuch Seite 73: alle 14 Schluessel durchprobieren."""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, KEYS, clean, decrypt
from data.corpus import CORPUS
from core import langmodel

ct = clean(CORPUS["73"])
print(f"Seite 73: {len(ct)} Zeichen = {len(ct)//2} Bigramme")
print(f"Lesbarkeitsschwelle: score >= -24")
print()
print(f"{'Key':12} {'n':>3} {'score':>9} {'hits':>5}  Klartext-Anfang")
print("-" * 90)
results = []
for name, (perm, sub, cnt) in KEYS.items():
    if len(sub) != 36:
        continue
    try:
        pt = decrypt(ct, perm, sub)
    except Exception as e:
        print(f"{name:12} FEHLER: {e}")
        continue
    sc = langmodel.score(pt)
    h = langmodel.word_hits(pt)
    results.append((sc, h, name, pt))
    print(f"{name:12} {len(perm):3} {sc:9.3f} {h:5}  {pt[:40]}")

print("-" * 90)
results.sort(reverse=True)
best = results[0]
print(f"Bestes: {best[2]} score={best[0]:.3f} hits={best[1]}")
print(f"-> {'LESBAR!' if best[0] >= -24 else 'Rauschen (kein Treffer)'}")
