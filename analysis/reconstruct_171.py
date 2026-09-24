#!/usr/bin/env python3
"""
Rekonstruktion der fehlenden Zeichen in Seite 171.

BEFUND (2026-09-21):
  Der Rohgeheimtext CORPUS['171'] enthaelt 4 Bindestriche ('-'). Diese
  stehen fuer unleserliche Zeichen im Original (siehe solutions.py:
  "- = unleserliches Zeichen im Original"). clean() entfernt sie, wodurch
  der Geheimtext auf 310 statt 314 Zeichen schrumpft.

  Die Sequenz [ch for ch in raw if ch in 'ADFGVX-'] hat exakt 314 Zeichen
  und damit die korrekte Laenge (157 Klartextzeichen * 2).

  ABER: Nach Ersetzen der Bindestriche durch die aus dem Klartext
  berechneten Zielzeichen stimmen nur 205/314 = 65.3% der Zeichen ueberein.
  Der Geheimtext hat also ZUSAETZLICHE Transkriptionsfehler.

VERWENDUNG:
  python3 reconstruct_171.py            # Diagnose
  python3 reconstruct_171.py --synth    # synthetischen Geheimtext ausgeben
"""

from __future__ import annotations

import sys

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import KEYS, clean, decrypt, make_square, transpose
from data.corpus import CORPUS
from data.solutions import SOLVED


def raw_sequence(page: str) -> str:
    """Alle ADFGVX-Zeichen UND Bindestriche in Originalreihenfolge."""
    raw = CORPUS[page]
    return "".join(ch for ch in raw if ch in "ADFGVX-")


def target_ciphertext(page: str) -> str:
    """Geheimtext, der aus dem bekannten Klartext + Schluessel folgt."""
    keyname, pt, _src = SOLVED[page]
    perm, sub, _cnt = KEYS[keyname]
    sq = make_square(sub)
    rev = {ch: "ADFGVX"[i // 6] + "ADFGVX"[i % 6] for i, ch in enumerate(sq)}
    bigr = "".join(rev[ch] for ch in pt)
    return transpose(bigr, perm)


def diagnose(page: str = "171") -> None:
    raw = CORPUS[page]
    seq = raw_sequence(page)
    target = target_ciphertext(page)
    keyname, pt_true, _src = SOLVED[page]
    perm, sub, _cnt = KEYS[keyname]

    print("=" * 78)
    print(f"SEITE {page} — Rekonstruktion der fehlenden Zeichen")
    print("=" * 78)
    print(f"Rohgeheimtext          : {len(raw)} Zeichen")
    print(f"clean() entfernt       : {len(raw) - len(clean(raw))} Zeichen")
    print(f"Sequenz (ADFGVX + '-') : {len(seq)} Zeichen")
    print(f"  davon Bindestriche   : {seq.count('-')}")
    print(f"Ziel (aus Klartext)    : {len(target)} Zeichen")
    print()

    # Bindestrich-Positionen
    print("Bindestrich-Positionen (Sequenzindex):")
    for i, ch in enumerate(seq):
        if ch == "-":
            print(f"  {i:3d}: ...{seq[max(0, i - 6):i + 7]}...")
    print()

    # Rekonstruktion: Bindestriche durch Zielzeichen ersetzen
    recon = "".join(target[i] if ch == "-" else ch for i, ch in enumerate(seq))
    match = sum(1 for a, b in zip(recon, target) if a == b)
    print(f"Rekonstruiert vs. Ziel : {match}/{len(target)} = "
          f"{match / len(target):.3f}")
    print()

    # Entschluesselung
    sq = make_square(sub)
    pt = decrypt(recon, perm, sq)
    m2 = sum(1 for a, b in zip(pt, pt_true) if a == b)
    print(f"Entschluesselt         : {pt[:78]}")
    print(f"Klartext-Treffer       : {m2}/{len(pt_true)} = "
          f"{m2 / len(pt_true):.3f}")
    print()

    # Spaltenanalyse
    n = len(perm)
    order = sorted(range(n), key=lambda c: perm[c])
    print(f"Breite n={n}, Auslesereihenfolge: {order}")
    print()

    def collen_of(L: int) -> list[int]:
        rows = (L + n - 1) // n
        rest = L % n or n
        return [rows if i < rest else rows - 1 for i in range(n)]

    def split_readorder(text: str) -> list[str]:
        cl = collen_of(len(text))
        cols, pos = [], 0
        for k in range(n):
            cols.append(text[pos:pos + cl[k]])
            pos += cl[k]
        return cols

    cols_recon = split_readorder(recon)
    cols_tg = split_readorder(target)
    print("Spaltenvergleich (Ausleseposition):")
    for k in range(n):
        a, b = cols_recon[k], cols_tg[k]
        common = sum(1 for x, y in zip(a, b) if x == y)
        flag = "  <-- LAENGENDIFFERENZ" if len(a) != len(b) else ""
        print(f"  pos {k:2d} col {order[k]:2d}: {common:2d}/{len(b):2d}{flag}")
    print()

    print("FAZIT:")
    print("  - 4 Bindestriche = 4 unleserliche Zeichen im Original")
    print("  - Sequenz hat korrekte Laenge (314)")
    print(f"  - Aber nur {100 * match / len(target):.1f}% Zeichen stimmen mit dem "
          "Ziel ueberein")
    print("  - => Zusaetzliche Transkriptionsfehler im Geheimtext")
    print("  - Klartext + Schluessel sind korrekt (Aehnlichkeit 0.76 vs. "
          "Zufall 0.26)")


def synth(page: str = "171") -> None:
    """Gibt den synthetischen (fehlerfreien) Geheimtext aus."""
    print(target_ciphertext(page))


if __name__ == "__main__":
    if "--synth" in sys.argv:
        synth()
    else:
        diagnose()
