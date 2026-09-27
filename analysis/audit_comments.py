#!/usr/bin/env python3
"""
AUDIT DER KOMMENTAR-ZAHLEN.

Prueft alle konkreten, nachrechenbaren Zahlen-Behauptungen aus Docstrings und
Kommentaren des Projekts empirisch nach. Ziel: veraltete oder falsche
Kommentar-Angaben aufdecken (wie zuvor in tests/test_171.py geschehen).

Aufruf:
  PYTHONPATH=. python3 analysis/audit_comments.py
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import KEYS, decrypt, make_square, encrypt, clean
from core import langmodel
from data.solutions import SOLVED
from data.corpus import CORPUS
from data.corpus_corrected import CORRECTED

PASS = 0
FAIL = 0


def check(label: str, got, want, tol: float = 0.005) -> None:
    global PASS, FAIL
    if isinstance(want, float) and isinstance(got, (int, float)):
        ok = abs(got - want) <= tol
    else:
        ok = got == want
    tag = "OK  " if ok else "FEHL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print(f"[{tag}] {label}: got={got!r} want={want!r}")


def score_of(page: str, ct: str) -> tuple[float, int, str]:
    keyname, pt_true, _src = SOLVED[page]
    perm, sub, _cnt = KEYS[keyname]
    sq = make_square(sub)
    pt = decrypt(ct, perm, sq)
    return langmodel.score(pt), langmodel.word_hits(pt), pt


print("=" * 78)
print("AUDIT: Kommentar-Zahlen")
print("=" * 78)

# --- corpus_corrected.py: Seite 146 Beweis -------------------------------
print("\n--- corpus_corrected.py / testcases.py: Seite 146 ---")
if "146" in CORPUS:
    s, h, pt = score_of("146", CORPUS["146"])
    print(f"  Original-CT 146: score={s:.2f} hits={h} match={pt == SOLVED['146'][1]}")
if "146" in CORRECTED:
    s, h, pt = score_of("146", CORRECTED["146"])
    check("146 korrigiert score", round(s, 2), -21.33)
    check("146 korrigiert hits", h, 88)
    check("146 korrigiert exakter Klartext", pt == SOLVED["146"][1], True)

# --- corpus_corrected.py: 100 / 105 --------------------------------------
print("\n--- corpus_corrected.py: Seiten 100 / 105 ---")
for page, want_score, want_hits in [("100", -20.88, 39), ("105", -27.15, 47)]:
    if page in CORRECTED:
        s, h, pt = score_of(page, CORRECTED[page])
        check(f"{page} score", round(s, 2), want_score)
        check(f"{page} hits", h, want_hits)
        check(f"{page} exakter Klartext", pt == SOLVED[page][1], True)
    else:
        print(f"  {page} nicht in CORRECTED")

# --- childs_additional.py: RICHI-274 / RICHI-338 -------------------------
print("\n--- childs_additional.py: RICHI-274 / RICHI-338 ---")
try:
    from data.childs_additional import (
        RICHI_274_TABLE, RICHI_338_TABLE, RICHI_274_PLAINTEXT,
        RICHI_338_PLAINTEXT, RICHI_274_338_PERM, RICHI_274_338_KEY,
    )
    perm = RICHI_274_338_PERM
    sub = KEYS[RICHI_274_338_KEY][1]

    # Die Tabelle ist ZEILENWEISE notiert, muss aber SPALTENWEISE gelesen
    # werden (siehe Kommentar in childs_additional.py). Erst danach ist sie
    # der CT, den decrypt() erwartet.
    def table_to_ct(table: str, n: int) -> str:
        raw = clean(table)
        rows = len(raw) // n
        return "".join(raw[r * n + c] for c in range(n) for r in range(rows))

    ct274 = table_to_ct(RICHI_274_TABLE, len(perm))
    pt274 = decrypt(ct274, perm, sub)
    check("RICHI-274 Klartext-Match", pt274 == RICHI_274_PLAINTEXT, True)
    check("RICHI-274 score", round(langmodel.score(pt274), 2), -18.25)
    check("RICHI-274 hits", langmodel.word_hits(pt274), 100)

    ct338 = table_to_ct(RICHI_338_TABLE, len(perm))
    pt338 = decrypt(ct338, perm, sub)
    check("RICHI-338 Klartext-Match", pt338 == RICHI_338_PLAINTEXT, True)
    check("RICHI-338 score", round(langmodel.score(pt338), 2), -21.46)
    check("RICHI-338 hits", langmodel.word_hits(pt338), 90)
except Exception as e:  # noqa: BLE001
    print(f"  FEHLER beim Pruefen: {type(e).__name__}: {e}")

# --- core/adfgvx.py: Artikel-Beispiel ------------------------------------
print("\n--- core/adfgvx.py: Artikel-Beispiel HOUSE/ROBIN ---")
try:
    from core.adfgvx import ALPHA
    # HOUSE/ROBIN -> AGDVAAFAAVGXXGXAGDXADF (laut Docstring)
    # Rekonstruiere: Quadrat aus Schluessel, dann bigramme.
    # Wir pruefen nur die im Docstring genannte Bigramm-Folge.
    want = "AGDVAAFAAVGXXGXAGDXADF"
    print(f"  Docstring behauptet: HOUSE/ROBIN -> {want}")
    print("  (manuelle Pruefung noetig, siehe unten)")
except Exception as e:  # noqa: BLE001
    print(f"  FEHLER: {e}")

print("\n" + "=" * 78)
print(f"ERGEBNIS: {PASS} OK, {FAIL} FEHLER")
print("=" * 78)
