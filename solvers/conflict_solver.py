#!/usr/bin/env python3
"""
Konflikt-Solver: Fehlersuche im Geheimtext ueber die Konfliktzahl.

Idee (neu, aus reverse_square.py):
  Bei korrektem Quadrat + korrekter Permutation darf jede Quadratzelle
  nur EINEN Klartextwert haben. Jeder Widerspruch ist ein Fehler im
  Geheimtext (fehlendes / ueberzaehliges / falsches Zeichen).

  Die Konfliktzahl ist damit ein EXAKTES Kriterium (nicht statistisch):
      0 Konflikte  <=>  Geheimtext + Quadrat + Permutation konsistent.

Verfahren:
  1. Fuer einen Kandidaten (perm, square) die Konfliktzahl berechnen.
  2. Fehlerpositionen suchen (Zeichen loeschen / einfuegen / ersetzen),
     die die Konfliktzahl minimieren.
  3. Bei 0 Konflikten: Klartext ausgeben.

Verwendung:
  python3 conflict_solver.py --test          # Validierung an Seite 105/146
  python3 conflict_solver.py --page 217      # auf Seite 217 anwenden
"""

from __future__ import annotations

import argparse
import random
from collections import Counter

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, KEYS, clean, make_square
from data.corpus import CORPUS
from data.solutions import SOLVED


# --------------------------------------------------------------------------
# Kern: Transposition + Konfliktzahl
# --------------------------------------------------------------------------

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


def cell_index(bg: str) -> int:
    return ALPHA.index(bg[0]) * 6 + ALPHA.index(bg[1])


def conflict_count(bgs: str) -> int:
    """Zaehlt Widersprueche: dieselbe Zelle mit verschiedenen Klartextwerten.

    Ohne bekannten Klartext ist der Klartextwert unbekannt. Wir koennen aber
    pruefen, ob die Zuordnung Zelle -> Klartextwert eine Funktion ist.
    Dazu brauchen wir den Klartext ... den wir nicht haben.

    => Fuer den BLINDEN Fall nutzen wir ein anderes Kriterium:
       Die Anzahl DISTINKTER Zellen, die mehrfach belegt sind, gewichtet
       mit der Streuung. Ein korrektes Quadrat erzeugt eine Bijektion
       zwischen Zellen und Klartextzeichen.
    """
    raise NotImplementedError


# --------------------------------------------------------------------------
# Blindes Kriterium: Zell-Belegungsstatistik
# --------------------------------------------------------------------------

def cell_stats(bgs: str) -> tuple[int, int, float]:
    """Liefert (distinkte Zellen, Gesamt-Bigramme, Entropie der Belegung).

    Bei korrekter Transposition + korrektem Quadrat gilt:
      - Jede Zelle entspricht genau einem Klartextzeichen.
      - Die Belegungshaeufigkeit der Zellen sollte der deutschen
        Buchstabenhaeufigkeit folgen (nach Substitution).
    """
    import math
    counts = Counter(bgs[i:i + 2] for i in range(0, len(bgs) - 1, 2))
    total = sum(counts.values())
    if total == 0:
        return 0, 0, 0.0
    ent = -sum((c / total) * math.log(c / total) for c in counts.values())
    return len(counts), total, ent


# --------------------------------------------------------------------------
# Bekannter Klartext: exakte Konfliktzahl
# --------------------------------------------------------------------------

def reverse_square(ct: str, perm: list[int], pt: str):
    """Rekonstruiert das Quadrat aus ct+pt. Liefert (sq, konflikte, detail)."""
    bgs = untranspose(ct, perm)
    sq: list[str | None] = [None] * 36
    conflicts = 0
    detail: list[tuple[int, str, str, str]] = []
    for i in range(0, len(bgs) - 1, 2):
        bg = bgs[i:i + 2]
        if len(bg) < 2:
            break
        idx = cell_index(bg)
        ch = pt[i // 2] if i // 2 < len(pt) else "?"
        if sq[idx] is None:
            sq[idx] = ch
        elif sq[idx] != ch:
            conflicts += 1
            detail.append((idx, bg, sq[idx], ch))
    return sq, conflicts, detail


# --------------------------------------------------------------------------
# Fehlersuche: welche Einzeloperation minimiert die Konflikte?
# --------------------------------------------------------------------------

def try_deletions(ct: str, perm: list[int], pt: str, top: int = 10):
    """Probiert, ein Zeichen zu loeschen. Liefert beste Kandidaten."""
    results = []
    for pos in range(len(ct)):
        ct2 = ct[:pos] + ct[pos + 1:]
        _, conf, _ = reverse_square(ct2, perm, pt)
        results.append((conf, pos, "del"))
    results.sort()
    return results[:top]


def try_insertions(ct: str, perm: list[int], pt: str, top: int = 10):
    """Probiert, ein Zeichen einzufuegen (alle 6 ADFGVX-Zeichen)."""
    results = []
    for pos in range(len(ct) + 1):
        for ch in ALPHA:
            ct2 = ct[:pos] + ch + ct[pos:]
            _, conf, _ = reverse_square(ct2, perm, pt)
            results.append((conf, pos, f"ins {ch}"))
    results.sort()
    return results[:top]


def try_substitutions(ct: str, perm: list[int], pt: str, top: int = 10):
    """Probiert, ein Zeichen zu ersetzen."""
    results = []
    for pos in range(len(ct)):
        for ch in ALPHA:
            if ch == ct[pos]:
                continue
            ct2 = ct[:pos] + ch + ct[pos + 1:]
            _, conf, _ = reverse_square(ct2, perm, pt)
            results.append((conf, pos, f"sub {ct[pos]}->{ch}"))
    results.sort()
    return results[:top]


def greedy_repair(ct: str, perm: list[int], pt: str, max_steps: int = 20,
                  verbose: bool = False):
    """Greedy: wiederholt die beste Einzeloperation, bis 0 Konflikte."""
    cur = ct
    _, conf, _ = reverse_square(cur, perm, pt)
    history = []
    for step in range(max_steps):
        if conf == 0:
            break
        cands = []
        cands += try_deletions(cur, perm, pt, top=3)
        cands += try_insertions(cur, perm, pt, top=3)
        cands += try_substitutions(cur, perm, pt, top=3)
        cands.sort()
        best_conf, pos, op = cands[0]
        if best_conf >= conf:
            break  # keine Verbesserung mehr
        if op == "del":
            cur = cur[:pos] + cur[pos + 1:]
        elif op.startswith("ins "):
            ch = op.split()[1]
            cur = cur[:pos] + ch + cur[pos:]
        else:  # sub
            ch = op.split("->")[1]
            cur = cur[:pos] + ch + cur[pos + 1:]
        history.append((conf, best_conf, pos, op))
        conf = best_conf
        if verbose:
            print(f"    Schritt {step + 1}: {op} @ {pos}  -> {conf} Konflikte")
    return cur, conf, history


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

def test_known(page: str, verbose: bool = True) -> None:
    """Validierung: Konflikte muessen durch Fehlersuche auf 0 fallen."""
    keyname, pt, src = SOLVED[page]
    ct = clean(CORPUS[page])
    perm, sub, _ = KEYS[keyname]
    _, conf0, _ = reverse_square(ct, perm, pt)
    print(f"\nSeite {page} ({keyname}) — Start: {conf0} Konflikte")
    if conf0 == 0:
        print("  bereits konsistent")
        return
    cur, conf, hist = greedy_repair(ct, perm, pt, max_steps=30, verbose=verbose)
    print(f"  Ergebnis: {conf} Konflikte nach {len(hist)} Operationen")
    if conf == 0:
        print("  -> Geheimtext vollstaendig repariert!")
        print(f"  -> Laenge: {len(ct)} -> {len(cur)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="Validierung an geloesten Seiten")
    ap.add_argument("--page", help="Seite, auf die der Solver angewendet wird")
    ap.add_argument("--key", help="Schluesselname (z.B. Nov22-24)")
    args = ap.parse_args()

    if args.test:
        print("=" * 88)
        print("VALIDIERUNG: Konflikt-Reparatur an geloesten Seiten")
        print("=" * 88)
        for page in ["105", "146", "171", "176a"]:
            test_known(page, verbose=False)
        return

    if args.page:
        page = args.page
        ct = clean(CORPUS[page])
        print(f"Seite {page}: {len(ct)} Zeichen")
        if args.key:
            perm, sub, _ = KEYS[args.key]
            print(f"Schluessel: {args.key}")
            bgs = untranspose(ct, perm)
            n_cells, total, ent = cell_stats(bgs)
            print(f"  Zellen belegt: {n_cells}/36, Bigramme: {total}, Entropie: {ent:.3f}")
        return

    ap.print_help()


if __name__ == "__main__":
    main()
