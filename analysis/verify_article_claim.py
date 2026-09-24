#!/usr/bin/env python3
"""
VERIFIKATION des Artikels "GPT-6 Astra solves a WWI German radio message"
(prinzai.com) fuer ADFGVX-Seite 217 (RICHI-170).

KORREKTUR-HISTORIE
------------------
Eine fruehere Version dieser Datei behauptete, den Artikel WIDERLEGT zu haben.
Das war FALSCH. Die drei damaligen "Beweise" hatten Denkfehler:

  * "Bijektions-Beweis": verglich 6 Chiffrat-Zeichen mit 23 Klartextzeichen.
    Bei ADFGVX bildet die Substitution aber BIGRAMME (36 moegliche) auf
    Klartextzeichen ab — nicht einzelne Chiffratzeichen. Die 6 Zeichen
    (A,D,F,G,V,X) sind nur die Zeilen-/Spaltenlabels des Polybios-Quadrats.

  * "Konflikt-Beweis": benutzte die 13 Cryptologia-Schluessel statt des im
    Artikel genannten Schluesselworts TRUPPENVERSCHIEBUNG. Mit der falschen
    Transposition entstehen zwangslaeufig "Konflikte".

  * "Multiset-Beweis": Zeichenhaeufigkeiten sind bei ADFGVX irrelevant.

DIE KORREKTE VERIFIKATION (diese Datei)
---------------------------------------
  1. Transposition mit TRUPPENVERSCHIEBUNG rueckgaengig machen.
  2. Substitution: jedes Bigramm -> genau EIN Klartextzeichen (0 Konflikte).
  3. Re-Encryption: Klartext -> Bigramme -> Transposition == Original-CT.

Ergebnis: Alle drei Tests BESTEHEN. Der Artikel hat recht.

Quellen:
  - prinzai.com/p/gpt-6-astra-solves-a-wwi-german-radio
  - Childs, "The History and Principles of German Military Ciphers",
    S. 214-215 (Schluesselwort TRUPPENVERSCHIEBUNG)
  - Schmeh/Cipherbrain: unsolved-adfxvx-messages-from-world-war-i
"""

from collections import Counter, defaultdict

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, FULL, clean
from data.corpus import CORPUS
from core import langmodel

# Schluesselwort aus dem Artikel (Childs S. 214-215)
KEYWORD = "TRUPPENVERSCHIEBUNG"

# Der vom Artikel behauptete Klartext
ARTICLE_PLAINTEXT = (
    "EINENGLISCHERKREUZEREINLIEGXSEWASTOPOLXS4STENX"
    "EINGESCHWADERDERXALLIIERTENFOLGT26STENX"
)


def rank_perm(keyword: str) -> list[int]:
    """Alphabetische Rangfolge (1-basiert, Gleichstand links zuerst)."""
    return [
        sum(1 for j, other in enumerate(keyword)
            if other < ch or (other == ch and j < i)) + 1
        for i, ch in enumerate(keyword)
    ]


def untranspose(ct: str, perm: list[int]) -> str:
    """Rang-basierte Spaltentransposition rueckgaengig machen.

    WICHTIG: cols[i][r] (Spalte i, Zeile r) — nicht cols[r][i]!
    """
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


def transpose(bigrams: str, perm: list[int]) -> str:
    """Spaltentransposition (Verschluesselungsrichtung)."""
    n = len(perm)
    L = len(bigrams)
    rows = (L + n - 1) // n
    rest = L % n
    if rest == 0:
        rest = n
    cols = [bigrams[i::n] for i in range(n)]
    order = sorted(range(n), key=lambda c: perm[c])
    return "".join(cols[c] for c in order)


def decrypt_sq(bigrams: str, square: str) -> str:
    return "".join(
        square[ALPHA.index(bigrams[i]) * 6 + ALPHA.index(bigrams[i + 1])]
        for i in range(0, len(bigrams) - 1, 2)
    )


def bigrams_of(plain: str, square: str) -> str:
    rev = {ch: ALPHA[i // 6] + ALPHA[i % 6] for i, ch in enumerate(square)}
    return "".join(rev[ch] for ch in plain)


def test_1_transposition(ct: str, perm: list[int]) -> str:
    print("=" * 72)
    print("TEST 1 — TRANSPOSITION MIT TRUPPENVERSCHIEBUNG")
    print("=" * 72)
    n = len(perm)
    L = len(ct)
    rows = (L + n - 1) // n
    rest = L % n
    print(f"  Schluesselwort : {KEYWORD} ({n} Buchstaben)")
    print(f"  Rangfolge      : {perm}")
    print(f"  Chiffrat       : {L} Zeichen, {rows} Reihen, rest={rest}")
    print(f"  Spaltenlaengen : {[rows if i < rest else rows - 1 for i in range(n)]}")
    print()
    # Artikel-Behauptung pruefen: Rang 16 (T) beginnt bei Index 134
    order = sorted(range(n), key=lambda c: perm[c])
    collen = [rows if i < rest else rows - 1 for i in range(n)]
    pos = 0
    for c in order:
        if perm[c] == 16:
            print(f"  Artikel: 'T (Rang 16) beginnt beim 135. Zeichen = A'")
            print(f"  Pruefung: Index {pos} -> Zeichen '{ct[pos]}'  "
                  f"-> {'OK' if ct[pos] == 'A' else 'ABWEICHUNG'}")
            break
        pos += collen[c]
    bgs = untranspose(ct, perm)
    print(f"  Ruecktransponiert: {len(bgs)} Zeichen = {len(bgs)//2} Bigramme")
    return bgs


def test_2_substitution(bgs: str, pt: str) -> tuple[bool, str]:
    print()
    print("=" * 72)
    print("TEST 2 — SUBSTITUTION (BIGRAMM -> KLARTEXTZEICHEN)")
    print("=" * 72)
    bigrams = [bgs[i:i + 2] for i in range(0, len(bgs), 2)]
    print(f"  Bigramme: {len(bigrams)}   Klartextzeichen: {len(pt)}")
    if len(bigrams) != len(pt):
        print("  -> LAENGEN UNGLEICH -> unmoeglich")
        return False, ""
    mapping = defaultdict(Counter)
    for bg, ch in zip(bigrams, pt):
        mapping[bg][ch] += 1
    conflicts = sum(len(v) - 1 for v in mapping.values())
    print()
    print("  Bigramm -> Klartextzeichen (nach Haeufigkeit):")
    for bg in sorted(mapping, key=lambda b: -sum(mapping[b].values())):
        dist = mapping[bg]
        flag = "  <-- KONFLIKT!" if len(dist) > 1 else ""
        print(f"    {bg} ({sum(dist.values()):2d}x) -> "
              f"{', '.join(f'{c}:{n}' for c, n in dist.most_common())}{flag}")
    print()
    print(f"  Konflikte: {conflicts}")
    print(f"  Eine Substitution bildet jedes Bigramm auf GENAU EIN Zeichen ab.")
    ok = conflicts == 0
    print(f"  -> {'OK — konsistente Substitution' if ok else 'UNMOEGLICH'}")
    # Quadrat rekonstruieren
    sq = ["?"] * 36
    for bg, ch in zip(bigrams, pt):
        sq[ALPHA.index(bg[0]) * 6 + ALPHA.index(bg[1])] = ch
    return ok, "".join(sq)


def test_3_roundtrip(ct: str, pt: str, sq_partial: str, perm: list[int]) -> bool:
    print()
    print("=" * 72)
    print("TEST 3 — RE-ENCRYPTION (ROUNDTRIP)")
    print("=" * 72)
    # Fehlende Quadratzellen mit Restalphabet auffuellen
    used = set(c for c in sq_partial if c != "?")
    rest = [c for c in FULL if c not in used]
    sq = list(sq_partial)
    for i in range(36):
        if sq[i] == "?":
            sq[i] = rest.pop(0)
    sq = "".join(sq)
    print(f"  Quadrat: {sum(1 for c in sq_partial if c != '?')}/36 Zellen "
          f"aus Klartext belegt, Rest aufgefuellt.")
    print()
    print("  Rekonstruiertes Quadrat:")
    for r in range(6):
        print("    " + " ".join(sq[r * 6:(r + 1) * 6]))
    print()
    bgs2 = bigrams_of(pt, sq)
    ct2 = transpose(bgs2, perm)
    match = ct == ct2
    print(f"  Original-CT : {ct[:60]}...")
    print(f"  Rekonstr-CT : {ct2[:60]}...")
    print()
    print(f"  MATCH: {match}")
    return match


def test_4_langmodel(pt: str) -> None:
    print()
    print("=" * 72)
    print("TEST 4 — SPRACHMODELL (nur zur Info)")
    print("=" * 72)
    print(f"  score = {langmodel.score(pt):.3f}  "
          f"hits = {langmodel.word_hits(pt)}")
    print("  (Der Klartext enthaelt viele X-Worttrenner und Ziffern,")
    print("   daher ist der Score niedriger als bei normalem Fliesstext.)")


def main() -> None:
    ct = clean(CORPUS["217"])
    pt = ARTICLE_PLAINTEXT
    perm = rank_perm(KEYWORD)

    print()
    print("#" * 72)
    print("#  VERIFIKATION: 'GPT-6 ASTRA SOLVES A WWI GERMAN RADIO'")
    print("#  ADFGVX-Seite 217 (RICHI-170)")
    print("#" * 72)
    print()

    bgs = test_1_transposition(ct, perm)
    ok2, sq = test_2_substitution(bgs, pt)
    ok3 = test_3_roundtrip(ct, pt, sq, perm)
    test_4_langmodel(pt)

    print()
    print("=" * 72)
    print("FAZIT")
    print("=" * 72)
    print(f"  Test 1 (Transposition):  {'OK' if bgs else 'FEHLER'}")
    print(f"  Test 2 (Substitution):   {'OK — 0 Konflikte' if ok2 else 'FEHLER'}")
    print(f"  Test 3 (Roundtrip):      {'OK — MATCH' if ok3 else 'FEHLER'}")
    print()
    if ok2 and ok3:
        print("  -> Der Artikel-Klartext ist KONSISTENT und VERIFIZIERT.")
        print("  -> Seite 217 (RICHI-170) ist mit TRUPPENVERSCHIEBUNG GELOEST.")
        print("  -> Die fruehere 'Widerlegung' war ein Denkfehler (siehe Docstring).")
    else:
        print("  -> Verifikation FEHLGESCHLAGEN.")
    print()


if __name__ == "__main__":
    main()
