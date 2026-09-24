#!/usr/bin/env python3
"""
SYNTHETISCHE TESTFAELLE fuer die ADFGVX-Solver.

Warum diese Datei existiert
---------------------------
`corpus.py` enthaelt die UNREINEN Original-Transkriptionen der abgefangenen
Funksprueche (Empfangs-/Uebertragungsfehler). Die Klartexte in `solutions.py`
gehoeren dagegen zu den von Norbert/Armin manuell KORRIGIERTEN Geheimtexten.

Beweis (Seite 146, Norbert #19):
  Original-CT + Nov4-6  -> score -33.13,  4 hits, 15.6% Zeichen-Uebereinstimmung
  Korrigierter CT + Nov4-6 -> score -21.33, 88 hits, EXAKT der Soll-Klartext

=> Re-Encryption-/decrypt-Tests gegen `corpus.py` sind sinnlos. Ein Solver,
   der dort scheitert, ist damit NICHT widerlegt.

Diese Datei erzeugt stattdessen FEHLERFREIE Testfaelle direkt aus den
bekannten Klartexten:

    ct_synth = transpose(bigrams(pt_true), perm)

Eigenschaften:
  - garantiert loesbar (decrypt(ct_synth, perm, sub) == pt_true)
  - exakt die Laenge des echten Chiffrats (2 * len(pt_true))
  - gleiche Statistik wie ein echter ADFGVX-Text

Ein Solver, der diese Testfaelle NICHT loest, ist nachweislich defekt.
Ein Solver, der sie loest, ist noch nicht bewiesen - er muss zusaetzlich
auf den korrigierten echten Chiffraten bestehen.
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, KEYS, decrypt, encrypt, make_square, transpose
from data.solutions import SOLVED


def bigrams_of(plain: str, subkey: str) -> str:
    """Wandelt Klartext in ADFGVX-Bigramme um (Schritt 1 der Verschluesselung)."""
    square = make_square(subkey)
    rev = {ch: ALPHA[i // 6] + ALPHA[i % 6] for i, ch in enumerate(square)}
    return "".join(rev.get(ch, "??") for ch in plain.upper())


def synthetic_ct(page: str) -> str:
    """Baut den fehlerfreien Geheimtext einer geloesten Seite."""
    keyname, pt, _src = SOLVED[page]
    perm, sub, _cnt = KEYS[keyname]
    return transpose(bigrams_of(pt, sub), perm)


def build_all() -> dict[str, dict]:
    """Erzeugt alle Testfaelle und prueft sie sofort gegen decrypt()."""
    cases: dict[str, dict] = {}
    for page, (keyname, pt, src) in SOLVED.items():
        perm, sub, _cnt = KEYS[keyname]
        ct = synthetic_ct(page)
        back = decrypt(ct, perm, sub)
        cases[page] = {
            "key": keyname,
            "perm": perm,
            "sub": sub,
            "pt": pt,
            "ct": ct,
            "roundtrip_ok": back == pt,
            "src": src,
        }
    return cases


def main() -> None:
    from core import langmodel

    cases = build_all()
    print("=" * 100)
    print("SYNTHETISCHE TESTFAELLE (fehlerfrei, garantiert loesbar)")
    print("=" * 100)
    print(f"{'Seite':6s} {'Key':11s} {'PT':>4s} {'CT':>4s} {'score':>8s} "
          f"{'hits':>5s} {'Roundtrip':>10s}")
    print("-" * 100)

    ok = 0
    for page, c in cases.items():
        sc = langmodel.score(c["pt"])
        hits = langmodel.word_hits(c["pt"])
        rt = "OK" if c["roundtrip_ok"] else "FEHLER"
        if c["roundtrip_ok"]:
            ok += 1
        print(f"{page:6s} {c['key']:11s} {len(c['pt']):4d} {len(c['ct']):4d} "
              f"{sc:8.2f} {hits:5d} {rt:>10s}")

    print("-" * 100)
    print(f"{ok}/{len(cases)} Testfaelle mit korrektem Roundtrip.")
    print()
    print("Hinweis: 'score'/'hits' beziehen sich auf den KLARTEXT (Zielwert).")
    print("Ein Solver muss diesen Wert aus dem CT rekonstruieren.")


if __name__ == "__main__":
    main()
