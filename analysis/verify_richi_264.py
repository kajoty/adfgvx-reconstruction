#!/usr/bin/env python3
"""
verify_richi_264.py -- Beweis fuer RICHI-264 (Schluessel Nov1-3).

Der OCR-Geheimtext (264 Zeichen) enthaelt 2 Fehler:
  1. Bigramm 63: AD -> AG  (D/G-Verwechslung, Morse-plausibel)
  2. Nach Bigramm 64 fehlt XG (Loeschung)

Nach beiden Reparaturen gelten zwei exakte Beweise:
  1. Dekodierung:   reparierter CT -> Klartext == gespeicherter Klartext
  2. Re-Encryption: Klartext -> Chiffre == reparierter CT

Lauf:  python3 analysis/verify_richi_264.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bootstrap  # noqa: F401  setzt sys.path
from data.childs_additional import RICHI_264_CT_OCR, RICHI_264_PLAINTEXT
from core.adfgvx import KEYS, clean, untranspose, substitute, transpose


def main() -> int:
    ct = clean(RICHI_264_CT_OCR)
    pt = RICHI_264_PLAINTEXT
    perm, square, _ = KEYS["Nov1-3"]

    un = untranspose(ct, perm)

    # Reparatur 1: Bigramm 63 (Zeichen 126-128): AD -> AG
    un2 = un[:126] + "AG" + un[128:]
    # Reparatur 2: XG nach Bigramm 64 (Zeichen 130) einfuegen
    un3 = un2[:130] + "XG" + un2[130:]

    dec = substitute(un3, square)

    # Beweis 1: Dekodierung
    b1 = dec == pt

    # Beweis 2: Re-Encryption
    bg = []
    for ch in pt:
        i = square.index(ch)
        bg.append("ADFGVX"[i // 6] + "ADFGVX"[i % 6])
    b2 = untranspose(transpose("".join(bg), perm), perm) == un3

    # Vorher-Befund: wie viele Zeichen stimmten schon ohne Reparatur?
    dec_raw = substitute(un, square)
    ok_raw = sum(1 for i in range(63) if dec_raw[i] == pt[i])
    ok_raw += sum(1 for i in range(64, len(dec_raw)) if dec_raw[i] == pt[i + 1])

    print("RICHI-264, Schluessel Nov1-3")
    print(f"  CT (OCR)      : {len(ct)} Zeichen = {len(ct)//2} Bigramme")
    print(f"  CT (repariert): {len(un3)} Zeichen")
    print(f"  Klartext      : {len(pt)} Zeichen")
    print()
    print(f"  Reparatur 1: Bigramm 63 AD -> AG   (D/G-Verwechslung)")
    print(f"  Reparatur 2: XG nach Bigramm 64 eingefuegt (Loeschung im CT)")
    print()
    print(f"  Ohne Reparatur stimmten {ok_raw} von 131 Zeichen")
    print()
    print(f"  Beweis 1 (Dekodierung)  : {b1}")
    print(f"  Beweis 2 (Re-Encryption): {b2}")
    print()
    print(f"  Klartext: {pt}")

    return 0 if (b1 and b2) else 1


if __name__ == "__main__":
    raise SystemExit(main())
