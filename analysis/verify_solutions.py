#!/usr/bin/env python3
"""
Verifizierte Loesungen aus dem Cipherbrain-Kommentarthread.

Korrekturen werden in FUENFERGRUPPEN-Notation angegeben (wie in den
Kommentaren), nicht in Zeichenpositionen.

Operationsformat pro Gruppe:
  ("del", gruppe, teilstring)   - Teilstring aus der Gruppe entfernen
  ("ins", gruppe, teilstring)   - Teilstring vor der Gruppe einfuegen
  ("sub", gruppe, alt, neu)     - Teilstring in der Gruppe ersetzen
  ("drop", gruppe)              - ganze Gruppe entfernen

Gruppennummern sind 1-basiert und beziehen sich auf den ORIGINAL-Geheimtext.
"""

from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()
from core.adfgvx import KEYS, clean, decrypt, make_square
from data.corpus import CORPUS
from core import langmodel


def to_groups(ct: str) -> list[str]:
    return [ct[i:i + 5] for i in range(0, len(ct), 5)]


def apply_group_ops(ct: str, ops: list[tuple]) -> str:
    groups = to_groups(ct)
    for op in ops:
        kind = op[0]
        if kind == "del":
            _, g, s = op
            groups[g - 1] = groups[g - 1].replace(s, "", 1)
        elif kind == "ins":
            _, g, s = op
            groups[g - 1] = s + groups[g - 1]
        elif kind == "sub":
            _, g, a, b = op
            groups[g - 1] = groups[g - 1].replace(a, b, 1)
        elif kind == "drop":
            _, g = op
            groups[g - 1] = ""
    return "".join(groups)


# Seite -> (Schluessel, Gruppen-Operationen, erwarteter Klartext)
SOLUTIONS: dict[str, tuple[str, list[tuple], str]] = {
    # Armin #13: drittletzte Gruppe FGDDF -> DGFGDDF (DG voranstellen)
    "100": ("Nov1-3", [("ins", 23, "DG")], "KEINESTOERUNG"),
    # Norbert #15: Gruppe 10 X weg, Gruppe 20 DG weg
    "105": ("Nov1-3", [("del", 10, "X"), ("del", 20, "DG")], "GERMANIAATAPPE"),
    # Norbert #18: Gruppen 16-19 (XXAXA DDVVV XXFXV DVDDG) -> XXAVV XXDDG
    "109": ("Nov1-3", [("drop", 16), ("drop", 17), ("drop", 18), ("drop", 19),
                       ("ins", 16, "XXAVV"), ("ins", 16, "XXDDG")],
            "ABENDMELDUNG"),
    # Norbert #19: FVXAA vor Gruppe 10 einfuegen; XAAXV XAFDX -> XAAXX
    "146": ("Nov4-6", [("ins", 10, "FVXAA"), ("sub", 47, "XAAXV", "XAAXX"),
                       ("drop", 48)], "FUNKSTELLEKERTSCHER"),
    # Norbert #20: diverse Korrekturen
    "171": ("Nov7-9", [("sub", 10, "A", "X"), ("sub", 25, "ADDVV", "ADDFX"),
                       ("sub", 30, "G", "X"), ("sub", 34, "GXVXV", "VXXVV"),
                       ("ins", 51, "DDDAA")], "INUKRAINEUNDPOLEN"),
    # Norbert #24: Gruppe 13 VADXX, Gruppe 21 XXDXV
    "187": ("Nov13-15b", [("sub", 21, "XXXDV", "XXDXV")], "STELLVXGENXKOM"),
    # Norbert #26: FVFFF nach Gruppe 3; Gruppen 25/26 -> AFFGA ADVAX DAVVV
    "176a": ("Nov10-12", [("ins", 4, "FVFFF"), ("drop", 25), ("drop", 26),
                          ("ins", 25, "AFFGA"), ("ins", 25, "ADVAX"),
                          ("ins", 25, "DAVVV")], "DURCHBRUCHVORBEREITET"),
}


def main() -> None:
    print("=" * 100)
    print("Verifikation der dokumentierten Loesungen (Gruppen-Notation)")
    print("=" * 100)
    ok_count = 0
    for page, (keyname, ops, expected) in SOLUTIONS.items():
        ct = clean(CORPUS[page])
        ct2 = apply_group_ops(ct, ops)
        perm, sub, _cnt = KEYS[keyname]
        pt = decrypt(ct2, perm, make_square(sub))
        sc = langmodel.score(pt)
        ok = pt.startswith(expected)
        ok_count += ok
        print(f"\nSeite {page:5s} {keyname:11s} Score {sc:7.2f} "
              f"{'OK' if ok else 'FEHLER'}")
        print(f"  {pt[:78]}")
    print(f"\n{ok_count}/{len(SOLUTIONS)} verifiziert")


if __name__ == "__main__":
    main()
