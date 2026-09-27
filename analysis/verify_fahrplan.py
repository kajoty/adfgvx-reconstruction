#!/usr/bin/env python3
"""Prueft, dass der im Fahrplan gezeigte Entschluesselungsweg stimmt:
fuer jedes Kryptogramm mit CT muss decrypt(ct, perm, square) == pt sein.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bootstrap  # noqa: F401

from core.adfgvx import KEYS, clean, decrypt, make_square
from data.corpus import CORPUS
from data.corpus_corrected import corrected_ct
from data.solutions import SOLVED
from data.childs_additional import (
    RICHI_264_CT_OCR, RICHI_264_PLAINTEXT, RICHI_264_KEY,
    RICHI_274_338_KEY, RICHI_274_338_PERM, RICHI_274_TABLE, RICHI_338_TABLE,
    RICHI_274_PLAINTEXT, RICHI_338_PLAINTEXT,
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dump_fahrplan import (  # noqa: E402
    P217_KEYWORD, P217_PLAINTEXT, R222_CT, R222_CANDIDATE,
    _rank_perm, _square_from_plaintext, _table_to_ct,
)

ok = 0
fail = 0
expected = 0


def check(name: str, ct: str, pt: str, perm: list[int], square: str,
          expect_mismatch: bool = False) -> None:
    global ok, fail, expected
    got = decrypt(ct, perm, square)
    if got == pt:
        ok += 1
        print(f"  OK    {name}")
    elif expect_mismatch:
        expected += 1
        print(f"  ERW.  {name}  (Abweichung dokumentiert, siehe Fahrplan)")
    else:
        fail += 1
        print(f"  FEHL  {name}")
        for i, (a, b) in enumerate(zip(got, pt)):
            if a != b:
                print(f"        erstes Diff bei {i}: got {a!r} != pt {b!r}")
                break
        if len(got) != len(pt):
            print(f"        Laenge: got {len(got)} != pt {len(pt)}")


print("Fahrplan-Verifikation: decrypt(ct, perm, square) == pt")
print()

# Korpus geloest
for page in sorted((p for p in SOLVED if p in CORPUS),
                   key=lambda p: int("".join(c for c in p if c.isdigit()) or 0)):
    keyname, pt, _ = SOLVED[page]
    perm, square, _ = KEYS[keyname]
    check(f"Korpus {page}", corrected_ct(page), pt, perm, square)

# Seite 217
p217_perm = _rank_perm(P217_KEYWORD)
p217_sq = _square_from_plaintext(clean(CORPUS["217"]), P217_PLAINTEXT, p217_perm)
check("Seite 217", clean(CORPUS["217"]), P217_PLAINTEXT, p217_perm, p217_sq)

# Childs
# RICHI-264: braucht 2 dokumentierte Reparaturen (AD->AG, XG fehlt) -> erwartet
perm, square, _ = KEYS[RICHI_264_KEY]
check("RICHI-264", clean(RICHI_264_CT_OCR), RICHI_264_PLAINTEXT, perm, square,
      expect_mismatch=True)

# RICHI-222: CT hat Luecken, Klartext ist Kandidat -> erwartet
perm, square, _ = KEYS["Nov1-3"]
check("RICHI-222", R222_CT, R222_CANDIDATE, perm, square, expect_mismatch=True)

perm, square, _ = KEYS[RICHI_274_338_KEY]
n = len(RICHI_274_338_PERM)
check("RICHI-274", _table_to_ct(RICHI_274_TABLE, n), RICHI_274_PLAINTEXT,
      RICHI_274_338_PERM, square)
# RICHI-338: 22 CT-Fehler in der Buch-Tabelle -> erwartet
check("RICHI-338", _table_to_ct(RICHI_338_TABLE, n), RICHI_338_PLAINTEXT,
      RICHI_274_338_PERM, square, expect_mismatch=True)

print()
print(f"Ergebnis: {ok} OK, {expected} erwartete Abweichungen, {fail} FEHLER")
raise SystemExit(1 if fail else 0)
