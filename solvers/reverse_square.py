#!/usr/bin/env python3
"""
Rueckrechnung des Substitutionsquadrats aus geloesten Nachrichten.

Idee:
  Nach Rueckgaengigmachen der Transposition liegen Bigramme vor.
  Jedes Bigramm (z.B. 'AV') adressiert eine Zelle des 6x6-Quadrats.
  Der Klartext an dieser Stelle verraet den Inhalt der Zelle.

  Stimmt das Quadrat, darf jede Zelle nur EINEN Klartextwert haben.
  Jeder Widerspruch ("Konflikt") ist ein Beweis fuer einen Fehler im
  Geheimtext (fehlendes/ueberzaehliges/falsches Zeichen).

Verwendung:
  python3 reverse_square.py            # unkorrigierte Geheimtexte
  python3 reverse_square.py --fixed    # mit Korrekturen aus verify_solutions
"""

from __future__ import annotations

import sys

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, KEYS, clean, make_square
from data.corpus import CORPUS
from data.solutions import SOLVED


def untranspose(ct: str, perm: list[int]) -> str:
    """Macht die Spaltentransposition rueckgaengig (Ranglisten-Konvention)."""
    n = len(perm)
    order = sorted(range(n), key=lambda c: perm[c])
    L = len(ct)
    rows = (L + n - 1) // n
    rest = L % n
    if rest == 0:
        rest = n
    collen = [rows if i < rest else rows - 1 for i in range(n)]
    cols = [""] * n
    pos = 0
    for c in order:
        cols[c] = ct[pos:pos + collen[c]]
        pos += collen[c]
    return "".join(cols[i][r] for r in range(rows) for i in range(n)
                   if r < len(cols[i]))


def reverse_square(ct: str, perm: list[int], pt: str):
    """Rekonstruiert das Quadrat. Liefert (quadrat, konflikte, belegung)."""
    bgs = untranspose(ct, perm)
    sq: list[str | None] = [None] * 36
    conflicts = 0
    conflict_detail: list[tuple[int, str, str, str]] = []
    for i in range(0, len(bgs) - 1, 2):
        bg = bgs[i:i + 2]
        if len(bg) < 2:
            break
        idx = ALPHA.index(bg[0]) * 6 + ALPHA.index(bg[1])
        ch = pt[i // 2] if i // 2 < len(pt) else "?"
        if sq[idx] is None:
            sq[idx] = ch
        elif sq[idx] != ch:
            conflicts += 1
            conflict_detail.append((idx, bg, sq[idx], ch))
    return sq, conflicts, conflict_detail


def apply_group_ops(ct: str, ops: list[tuple]) -> str:
    """Wendet die dokumentierten Gruppen-Korrekturen an (aus verify_solutions)."""
    groups = [ct[i:i + 5] for i in range(0, len(ct), 5)]
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


def main() -> None:
    use_fixed = "--fixed" in sys.argv

    # Korrekturen aus verify_solutions laden (falls vorhanden)
    try:
        from analysis.verify_solutions import SOLUTIONS as FIXES
    except Exception:
        FIXES = {}

    print("=" * 96)
    print("RUECKRECHNUNG DES SUBSTITUTIONSQUADRATS AUS GELOESTEN NACHRICHTEN")
    print(f"Modus: {'KORRIGIERTE Geheimtexte' if use_fixed else 'UNKORRIGIERTE Geheimtexte'}")
    print("=" * 96)
    print()
    print(f"{'Seite':6s} {'Schluessel':12s} {'Zellen':>7s} {'Konflikte':>10s}  Bewertung")
    print("-" * 96)

    total_conf = 0
    rows = []
    for page, (keyname, pt_known, src) in SOLVED.items():
        if page == "??":
            continue
        ct = clean(CORPUS[page])
        if use_fixed and page in FIXES:
            _k, ops, _exp = FIXES[page]
            ct = apply_group_ops(ct, ops)
        perm, sub, _cnt = KEYS[keyname]
        sq, conflicts, detail = reverse_square(ct, perm, pt_known)
        filled = sum(1 for c in sq if c is not None)
        total_conf += conflicts
        verdict = "OK" if conflicts == 0 else ("fast OK" if conflicts <= 5 else "FEHLER")
        rows.append((page, keyname, filled, conflicts, verdict, sq, sub, detail))
        print(f"{page:6s} {keyname:12s} {filled:3d}/36 {conflicts:10d}  {verdict}")

    print("-" * 96)
    print(f"Summe Konflikte: {total_conf}")
    print()

    # Detailansicht: rekonstruiertes vs. veroeffentlichtes Quadrat
    print("=" * 96)
    print("DETAIL: rekonstruiertes Quadrat vs. veroeffentlichtes Quadrat")
    print("=" * 96)
    for page, keyname, filled, conflicts, verdict, sq, sub, detail in rows:
        if conflicts > 5:
            continue
        recon = "".join(c if c is not None else "?" for c in sq)
        print(f"\nSeite {page} ({keyname}) — {conflicts} Konflikte")
        print(f"  rekonstruiert: {recon}")
        print(f"  veroeffentl.:  {sub}")
        # Uebereinstimmung zaehlen
        agree = sum(1 for a, b in zip(recon, sub) if a != "?" and a == b)
        known = sum(1 for a in recon if a != "?")
        print(f"  Uebereinstimmung: {agree}/{known} bekannte Zellen")
        if detail:
            print(f"  Konflikte (Zelle, Bigramm, erwartet, tatsaechlich):")
            for idx, bg, a, b in detail[:10]:
                print(f"    Zelle {idx:2d} ({bg}) -> {a!r} vs {b!r}")


if __name__ == "__main__":
    main()
