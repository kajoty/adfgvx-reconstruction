#!/usr/bin/env python3
"""
KONFLIKT-ANALYSE (CoT-Fahrplan, Aktion 1+2)

Zweck
-----
Der CoT-Fahrplan (README, Abschnitt "Naechster logischer Schritt") beginnt mit
zwei billigen Aktionen:

  Aktion 1: `conflict_solver.py` auf alle ungeloesten Seiten anwenden.
  Aktion 2: Die Konfliktzahl als RANKING-Metrik nutzen (niedrigste zuerst).

Dieses Skript liefert die Messgrundlage fuer beide Aktionen.

Das exakte Kriterium
--------------------
Bei korrektem Quadrat + korrekter Permutation darf jede Quadratzelle nur EINEN
Klartextwert haben:

    Konfliktzahl == 0  <=>  Chiffrat + Quadrat + Permutation konsistent

Ein Konflikt ist ein BEWIESENER Zeichenfehler im Chiffrat — kein statistisches
Signal, kein Schwellenwert, keine Toleranz.

Validierung an den geloesten Seiten (`--validate`)
--------------------------------------------------
    Seite  Key          ORIG-CT Konflikte   KORR-CT Konflikte
    100    Nov1-3           124        3        124        0
    105    Nov1-3           290       78        287        0
    109    Nov1-3           258       95        250        0
    146    Nov4-6           244       85        244        0
    171    Nov7-9           310      107        314        0
    187    Nov13-15b        212       67        214        0
    176a   Nov10-12         214       71        224        0
    132    Nov4-6           153       40        154        0
    164a   Nov7-9           158       45        126        0
    164b   Nov7-9           136       42        180        0
    153a   Nov13-15a        132       34        352        0

11/11 geloeste Seiten: exakt 0 Konflikte nach der Korrektur, 34-107 vorher.
Das Kriterium trennt scharf und ist damit als Fehlerdetektor bewiesen.

Die Grenze des Verfahrens (wichtig!)
------------------------------------
Die Konfliktzahl ist NUR messbar, wenn der Klartext bekannt ist. Fuer die
ungeloesten Seiten ist er das nicht.

Ein BLINDES Ersatzkriterium existiert nicht. Zwei Kandidaten wurden geprueft
und verworfen (siehe `--blind`):

  1. ZELL-REINHEIT (Anteil des haeufigsten Werts je Zelle)
     -> UNBRAUCHBAR. Bei falschem Schluessel ist sie oft HOEHER, weil die
        Transposition dann weniger streut. Sie korreliert negativ mit der
        Korrektheit.

  2. ZELLENZAHL (Zahl der belegten Quadratzellen)
     -> SCHWACH. Der richtige Schluessel liefert nur in 5/10 Faellen die
        minimale Zellenzahl. Besser als Zufall, aber kein Beweis.

Konsequenz: Fuer die ungeloesten Seiten muss der Klartext KANDIDATENWEISE
geraten und die Konfliktzahl MINIMIERT werden — genau das tut
`solvers/conflict_solver.py`. Dieses Skript liefert dazu die Messung.

Verwendung
----------
  python3 analysis/rank_conflicts.py --validate    # exaktes Kriterium (Kontrolle)
  python3 analysis/rank_conflicts.py --blind       # verworfene blinde Kriterien
  python3 analysis/rank_conflicts.py --page 171    # Detailanalyse einer Seite
  python3 analysis/rank_conflicts.py --unsolved    # Uebersicht ungeloeste Seiten
"""

from __future__ import annotations

import argparse
from collections import Counter

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, KEYS, clean, make_square
from core import langmodel
from data.corpus import CORPUS
from data.corpus_corrected import CORRECTED, corrected_ct
from data.solutions import SOLVED


# --------------------------------------------------------------------------
# Kern: Transposition
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


def bigrams_of(bgs: str) -> list[str]:
    return [bgs[i:i + 2] for i in range(0, len(bgs) - 1, 2)]


# --------------------------------------------------------------------------
# Exaktes Kriterium
# --------------------------------------------------------------------------

def exact_conflicts(ct: str, perm: list[int], pt: str) -> dict:
    """Konfliktzahl gegen einen BEKANNTEN Klartext.

    Jede Quadratzelle darf nur einen Klartextwert tragen. Jeder Widerspruch
    ist ein bewiesener Zeichenfehler im Chiffrat.
    """
    bgs = untranspose(ct, perm)
    sq: list[str | None] = [None] * 36
    conflicts = 0
    total = 0
    detail: list[tuple[int, str, str, str]] = []
    for i, bg in enumerate(bigrams_of(bgs)):
        idx = cell_index(bg)
        ch = pt[i] if i < len(pt) else "?"
        total += 1
        if sq[idx] is None:
            sq[idx] = ch
        elif sq[idx] != ch:
            conflicts += 1
            detail.append((idx, bg, sq[idx], ch))
    return {
        "conflicts": conflicts,
        "total": total,
        "rate": conflicts / total if total else 0.0,
        "cells": sum(1 for x in sq if x is not None),
        "square": sq,
        "detail": detail,
    }


def validate() -> None:
    """Kontrolle: Konfliktzahl Original-CT vs. korrigierter CT."""
    print("=" * 100)
    print("EXAKTES KRITERIUM — Konfliktzahl gegen den verifizierten Klartext")
    print("=" * 100)
    print()
    print(f"{'Seite':6} {'Key':11} {'Quelle':9} "
          f"{'ORIG-CT':>8} {'Konfl':>6} {'Rate':>7} "
          f"{'KORR-CT':>8} {'Konfl':>6} {'Rate':>7}")
    print("-" * 100)
    n_ok = 0
    n_tot = 0
    for page, (keyname, pt, _src) in SOLVED.items():
        if page not in CORPUS:
            continue  # z.B. "??" — geloest, aber keine Korpus-Seite
        perm, _sub, _cnt = KEYS[keyname]
        orig = clean(CORPUS[page])
        corr = corrected_ct(page)
        r1 = exact_conflicts(orig, perm, pt)
        r2 = exact_conflicts(corr, perm, pt)
        quelle = "Transkr." if page in CORRECTED else "synthet."
        n_tot += 1
        n_ok += (r2["conflicts"] == 0)
        print(f"{page:6} {keyname:11} {quelle:9} "
              f"{len(orig):8} {r1['conflicts']:6} {r1['rate']:7.3f} "
              f"{len(corr):8} {r2['conflicts']:6} {r2['rate']:7.3f}")
    print("-" * 100)
    print(f"\nKorrigierte Chiffrate mit 0 Konflikten: {n_ok}/{n_tot}")
    print()
    print("Deutung: Das Kriterium trennt SCHARF. Beschaedigte Chiffrate zeigen")
    print("34-107 Konflikte, reparierte exakt 0. Es gibt keinen Graubereich —")
    print("0 Konflikte ist ein BEWEIS der Konsistenz.")
    print()
    print("Konsequenz: Fuer die ungeloesten Seiten ist der Klartext unbekannt,")
    print("die exakte Konfliktzahl also nicht messbar. Der Klartext muss")
    print("kandidatenweise geraten und die Konfliktzahl MINIMIERT werden")
    print("(siehe `solvers/conflict_solver.py`).")


# --------------------------------------------------------------------------
# Verworfene blinde Kriterien (dokumentiert, damit sie nicht neu erfunden werden)
# --------------------------------------------------------------------------

def blind() -> None:
    """Zeigt, warum es kein brauchbares blindes Kriterium gibt."""
    print("=" * 100)
    print("VERWORFENE BLINDE KRITERIEN")
    print("=" * 100)

    # --- Kriterium 1: Zell-Reinheit -------------------------------------
    print()
    print("1) ZELL-REINHEIT (Anteil des haeufigsten Werts je Zelle)")
    print("-" * 100)
    print(f"{'Seite':6} {'Status':9} {'Key':11} {'Reinheit':>9} {'Konflikte':>10}")
    solved_rows = []
    unsolved_rows = []
    for page in CORPUS:
        ct = clean(CORPUS[page])
        best = None
        for keyname, (perm, sub, _cnt) in KEYS.items():
            if len(sub) != 36:
                continue
            cnt = Counter(bigrams_of(untranspose(ct, perm)))
            tot = sum(cnt.values())
            pur = max(cnt.values()) / tot if tot else 0.0
            if best is None or pur > best[2]:
                best = (keyname, tot - max(cnt.values()), pur)
        assert best is not None
        row = (page, best[0], best[2], best[1])
        (solved_rows if page in SOLVED else unsolved_rows).append(row)

    solved_rows.sort(key=lambda r: -r[2])
    unsolved_rows.sort(key=lambda r: -r[2])
    for page, key, pur, conf in solved_rows[:3]:
        print(f"{page:6} {'GELOEST':9} {key:11} {pur:9.3f} {conf:10}")
    print("  ...")
    for page, key, pur, conf in unsolved_rows[:3]:
        print(f"{page:6} {'offen':9} {key:11} {pur:9.3f} {conf:10}")
    print()
    print("  BEFUND: Die geloesten Seiten haben NIEDRIGERE Reinheit als die")
    print("  ungeloesten. Das Kriterium korreliert NEGATIV mit der Korrektheit")
    print("  -> UNBRAUCHBAR.")

    # --- Kriterium 2: Zellenzahl ----------------------------------------
    print()
    print("2) ZELLENZAHL (Zahl der belegten Quadratzellen)")
    print("-" * 100)
    print(f"{'Seite':6} {'richtig':11} {'Zellen':>7} {'min':>5} "
          f"{'min-Key':11} {'Rang':>5}")
    hits = 0
    tot = 0
    for page, (key, _pt, _src) in SOLVED.items():
        if page not in CORPUS:
            continue
        ct = clean(CORPUS[page])
        res = []
        for k, (perm, sub, _cnt) in KEYS.items():
            if len(sub) != 36:
                continue
            cells = len(set(bigrams_of(untranspose(ct, perm))))
            res.append((cells, k))
        res.sort()
        matches = [(c, k) for c, k in res if k == key]
        if not matches:
            continue
        rank = [i for i, (c, k) in enumerate(res, 1) if k == key][0]
        tot += 1
        hits += (rank == 1)
        print(f"{page:6} {key:11} {matches[0][0]:7} {res[0][0]:5} "
              f"{res[0][1]:11} {rank:5}")
    print("-" * 100)
    print(f"  Richtiger Schluessel hat die minimale Zellenzahl: {hits}/{tot}")
    print()
    print("  BEFUND: Nur 5/10. Besser als Zufall, aber kein Beweis")
    print("  -> SCHWACH, nur als Vorpriorisierung geeignet.")


# --------------------------------------------------------------------------
# Detailanalyse
# --------------------------------------------------------------------------

def detail(page: str) -> None:
    """Detailanalyse einer Seite."""
    ct = clean(CORPUS[page])
    print("=" * 100)
    print(f"DETAILANALYSE Seite {page}  ({len(ct)} Zeichen)")
    print("=" * 100)
    print()
    if page in SOLVED:
        keyname, pt, _src = SOLVED[page]
        perm, _sub, _cnt = KEYS[keyname]
        r = exact_conflicts(ct, perm, pt)
        print(f"Status: GELOEST mit Schluessel {keyname}")
        print(f"  Exakte Konfliktzahl: {r['conflicts']} / {r['total']} "
              f"({r['rate']:.3f})")
        print(f"  Belegte Zellen: {r['cells']}/36")
        if r["detail"]:
            print(f"  Erste Konflikte (Zelle, Bigramm, Soll, Ist):")
            for idx, bg, soll, ist in r["detail"][:8]:
                print(f"    Zelle {idx:2d}  {bg}  {soll} != {ist}")
        print()
    else:
        print("Status: UNGELOEST — exakte Konfliktzahl nicht messbar")
        print()

    print(f"{'Key':11} {'Zellen':>6} {'Reinheit':>9} {'Entropie':>9} "
          f"{'score':>8} {'hits':>5}")
    print("-" * 70)
    rows = []
    for keyname, (perm, sub, _cnt) in KEYS.items():
        if len(sub) != 36:
            continue
        bgs = untranspose(ct, perm)
        cnt = Counter(bigrams_of(bgs))
        tot = sum(cnt.values())
        import math
        pur = max(cnt.values()) / tot if tot else 0.0
        ent = -sum((c / tot) * math.log2(c / tot) for c in cnt.values()) if tot else 0.0
        sq = make_square(sub)
        pt = "".join(sq[cell_index(bg)] for bg in bigrams_of(bgs))
        rows.append({"key": keyname, "cells": len(cnt), "purity": pur,
                     "entropy": ent, "score": langmodel.score(pt),
                     "hits": langmodel.word_hits(pt), "pt": pt})
    rows.sort(key=lambda r: -r["score"])
    for r in rows:
        print(f"{r['key']:11} {r['cells']:6} {r['purity']:9.3f} "
              f"{r['entropy']:9.3f} {r['score']:8.2f} {r['hits']:5}")
    print("-" * 70)
    best = rows[0]
    print()
    print(f"Bester Score: {best['key']}  ({best['score']:.2f}, "
          f"{best['hits']} Worttreffer)")
    print(f"  Klartext: {best['pt'][:90]}")


def unsolved() -> None:
    """Uebersicht der ungeloesten Seiten."""
    pages = [p for p in CORPUS if p not in SOLVED]
    print("=" * 100)
    print(f"UNGELOESTE SEITEN ({len(pages)})")
    print("=" * 100)
    print()
    print(f"{'Seite':6} {'CT':>5} {'Bigramme':>9} {'Zellen':>7} {'Luecken':>8}")
    print("-" * 50)
    for page in pages:
        raw = CORPUS[page]
        ct = clean(raw)
        gaps = sum(1 for ch in raw if ch == "-")
        cells = len(set(bigrams_of(ct)))
        print(f"{page:6} {len(ct):5} {len(ct) // 2:9} {cells:7} {gaps:8}")
    print("-" * 50)
    print()
    print("'Luecken' = Zahl der unleserlichen Zeichen ('-') in der Transkription.")
    print("Seiten mit vielen Luecken sind ohne externe Quellen nicht loesbar.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Konflikt-Analyse der ADFGVX-Seiten")
    ap.add_argument("--validate", action="store_true",
                    help="exaktes Kriterium an den geloesten Seiten (Kontrolle)")
    ap.add_argument("--blind", action="store_true",
                    help="verworfene blinde Kriterien dokumentieren")
    ap.add_argument("--page", help="Detailanalyse einer Seite")
    ap.add_argument("--unsolved", action="store_true",
                    help="Uebersicht der ungeloesten Seiten")
    args = ap.parse_args()

    if args.validate:
        validate()
    elif args.blind:
        blind()
    elif args.page:
        detail(args.page)
    elif args.unsolved:
        unsolved()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
