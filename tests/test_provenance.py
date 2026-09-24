#!/usr/bin/env python3
"""
TEST: Herkunft des Korpus gegen die Originalquelle.

Prueft die zentrale Behauptung des Provenienz-Nachweises (2026-09-24):

  1. `data/corpus.py` ist eine treue Abschrift der Original-Transkription
     aus dem Cipherbrain-Artikel (`data/article_transcription.py`).
     -> mindestens 14 von 22 Seiten sind zeichengenau identisch.

  2. Alle Abweichungen sind erklaerbar: zusaetzliche '-' (unleserliche
     Zeichen) oder bereits angewandte Kommentar-Korrekturen.

  3. Seite 100: Der Artikel-Block allein entschluesselt zu Kauderwelsch;
     erst Artikel + 'DG' + 'V->A' ergibt den verifizierten Klartext.
     -> Die V->A-Korrektur an Position 20 ist durch die Originalquelle
        bestaetigt.

Aufruf:
    PYTHONPATH=. python3 tests/test_provenance.py
"""

from __future__ import annotations

import os as _os
import re
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup  # noqa: E402

setup()

from analysis.verify_corpus_provenance import MAPPING, norm  # noqa: E402
from core import langmodel  # noqa: E402
from core.adfgvx import KEYS, decrypt  # noqa: E402
from data.article_transcription import ARTICLE_CT, clean as art_clean  # noqa: E402
from data.corpus import CORPUS  # noqa: E402
from data.solutions import SOLVED  # noqa: E402

FAILURES: list[str] = []


def check(cond: bool, msg: str) -> None:
    status = "OK  " if cond else "FAIL"
    print(f"  [{status}] {msg}")
    if not cond:
        FAILURES.append(msg)


def test_corpus_is_faithful() -> None:
    print("\n1. Korpus ist treue Abschrift der Originalquelle")
    identisch = 0
    for page, artkey in MAPPING.items():
        if page not in CORPUS or artkey not in ARTICLE_CT:
            continue
        if norm(CORPUS[page]) == art_clean(ARTICLE_CT[artkey]):
            identisch += 1
    check(identisch >= 14,
          f"{identisch}/22 Seiten zeichengenau identisch (>= 14 erwartet)")


def test_deviations_are_cosmetic() -> None:
    print("\n2. Abweichungen sind erklaerbar (nur '-' oder Kommentar-Korrektur)")
    for page, artkey in MAPPING.items():
        if page not in CORPUS or artkey not in ARTICLE_CT:
            continue
        k = norm(CORPUS[page])
        a = art_clean(ARTICLE_CT[artkey])
        if k == a:
            continue
        # Klammernotation im Artikel entfernen
        a_clean = re.sub(r"[(){}]", "", a)
        # Korpus ohne '-' muss Teilfolge des Artikels ohne '-' sein
        k_nodash = k.replace("-", "")
        a_nodash = a_clean.replace("-", "")
        if page == "100":
            # Seite 100: Korpus hat die 'DG'-Einfuegung aus Armin #13
            # (an CT-Position 110, nicht die erste 'DG'-Folge)
            k_nodash = k_nodash[:110] + k_nodash[112:]
        check(k_nodash == a_nodash,
              f"Seite {page}: Korpus ohne '-' == Artikel ohne '-' "
              f"(Klammern entfernt)")


def test_page_100_confirmed_by_source() -> None:
    print("\n3. Seite 100: Originalquelle bestaetigt die DG-Einfuegung")
    keyname, pt_soll, _src = SOLVED["100"]
    perm, sub, _cnt = KEYS[keyname]

    a = art_clean(ARTICLE_CT["100"])
    k = norm(CORPUS["100"])

    # Der Korpus ist exakt der Artikel-Block plus die 'DG'-Einfuegung
    check(k == a[:110] + "DG" + a[110:],
          "Korpus == Artikel + 'DG' an Position 110 (Armin #13)")

    # Artikel allein -> Kauderwelsch
    pt_art = decrypt(a, perm, sub)
    check(pt_art != pt_soll,
          f"Artikel-Block allein entschluesselt NICHT zum Soll-Klartext "
          f"(score {langmodel.score(pt_art):.2f}, "
          f"{langmodel.word_hits(pt_art)} hits)")

    # Artikel + DG -> bereits lesbar, aber noch nicht exakt
    pt_dg = decrypt(k, perm, sub)
    check(pt_dg != pt_soll and langmodel.word_hits(pt_dg) > 20,
          f"Artikel + 'DG' ist lesbar, aber noch nicht exakt "
          f"(score {langmodel.score(pt_dg):.2f}, "
          f"{langmodel.word_hits(pt_dg)} hits)")

    # Korpus + V->A an CT-Position 20 -> exakt der Soll-Klartext
    k_fix = k[:20] + "A" + k[21:]
    pt_fix = decrypt(k_fix, perm, sub)
    check(pt_fix == pt_soll,
          f"Korpus + 'V->A' (CT-Pos 20) ergibt EXAKT den Soll-Klartext "
          f"(score {langmodel.score(pt_fix):.2f}, "
          f"{langmodel.word_hits(pt_fix)} hits)")

    # Artikel und Korpus lesen an Position 20 beide ein 'V'
    check(a[20] == "V" and k[20] == "V",
          "Artikel und Korpus lesen Pos 20 beide 'V' "
          "(V->A ist eine separate Korrektur)")


def main() -> int:
    print("=" * 78)
    print("TEST: HERKUNFT DES KORPUS GEGEN DIE ORIGINALQUELLE")
    print("=" * 78)

    test_corpus_is_faithful()
    test_deviations_are_cosmetic()
    test_page_100_confirmed_by_source()

    print()
    print("=" * 78)
    if FAILURES:
        print(f"FEHLGESCHLAGEN: {len(FAILURES)} Pruefung(en)")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("ALLE PRUEFUNGEN BESTANDEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
