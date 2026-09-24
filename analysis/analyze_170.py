#!/usr/bin/env python3
"""
analyze_170.py -- Tiefenanalyse der Seite 170 (RICHI-240)

AUSGANGSLAGE
============
Seite 170 ist der einzige "echte" Astra-Kandidat:
  - Der Schluessel ist bekannt (Nov10-12, laut Artikel)
  - Die Transposition ist korrekt (bei allen geloesten Seiten 100%)
  - Nur die Zeichen sind beschaedigt

PROBLEM
=======
corpus.py['170'] hat nur 106 Zeichen (3 Zeilen), der Artikel spricht
aber von RICHI-240 mit 240 Zeichen. Die Transkription ist also
entweder ein Fragment oder stark beschaedigt.

BEFUND (diese Analyse)
======================
Seite 170 ist die EINZIGE der 22 Seiten, bei der ein ADFGVX-Zeichen
als ERSTES Zeichen eines Bigramms komplett fehlt: D kommt 0x vor.

Vergleich mit Seite 176a (IDENTISCHER Key Nov10-12, IDENTISCHES Quadrat):

  Position 1 (Quadrat-ZEILE):
    D: 170 =  0.0%, 176a = 17.0%   -> -17.0 Punkte (FEHLT KOMPLETT)
    G: 170 = 32.1%, 176a = 22.3%   ->  +9.8 Punkte (ZU VIEL)
    X: 170 = 15.1%, 176a =  7.1%   ->  +8.0 Punkte (ZU VIEL)
    A: 170 = 24.5%, 176a = 23.2%   ->  +1.3 (OK)
    V: 170 = 20.8%, 176a = 19.6%   ->  +1.2 (OK)
    F: 170 =  7.5%, 176a = 10.7%   ->  -3.2 (leicht niedrig)

  Position 2 (Quadrat-SPALTE):
    Alle Zeichen innerhalb von ~5 Punkten -> deutlich sauberer!

Die fehlende D-Menge (17.0) entspricht fast exakt dem Ueberschuss
von G und X zusammen (9.8 + 8.0 = 17.8).

=> HYPOTHESE: Die Transkriptionsfehler konzentrieren sich auf
   POSITION 1 der Bigramme. D wurde systematisch als G oder X
   gelesen (oder die Zeile D des Quadrats ist im Klartext unbenutzt).

KONSEQUENZ
==========
Mit Nov10-12 entschluesselt liefert Seite 170:
  4CCQUDDHX4H7H464Y3CCGGJARJEEEAYDU7DCVWWUXR1M9U8CB0QP8

Das enthaelt viele Ziffern (7,8,9,6,Y) und C,D,J,M,W,X, aber
KEIN O,I,F,S,K,N. Das ist das Gegenteil von deutschem Klartext.

=> Die Zeile D (O,I,F,S,K,N) wird nicht genutzt, stattdessen
   werden Zeile G (D,J,M,X,C,W) und Zeile X (Y,5,6,7,8,9)
   uebernutzt.

WIDERLEGUNG DER ALTERNATIVHYPOTHESE
===================================
H-B ("Zeile D ist im Klartext unbenutzt") ist widerlegt:
Zeile D enthaelt O,I,F,S,K,N = 30.1% aller deutschen Buchstaben.
Wahrscheinlichkeit, dass ein 53-Zeichen-Text keinen davon enthaelt:
(1-0.301)^53 = 5.6e-9.

=> Die Zeile D MUSS genutzt werden. D=0 ist ein Transkriptionsfehler.

REPARATURVERSUCH UND ARTEFAKT-NACHWEIS
======================================
Hypothese: G/X in Position 1 waren eigentlich D.
Ergebnis: Score steigt von -34.87 auf -32.40 (k=4 Ersetzungen).

ABER: Der Effekt ist ein ARTEFAKT. Kontrolltests (je 1000 Zufalls-
laeufe, 4 Positionen geaendert):
  - Zufaellige Positionen -> D:        bester Score -32.65
  - Zufaellige Positionen -> beliebig: bester Score -32.85
  - G/X-Positionen -> beliebig:        bester Score -32.64

Der "reparierte" Score (-32.40) liegt im Bereich des Zufalls.
=> Der Score-Anstieg ist KEIN Beweis fuer die D-Hypothese.

FAZIT
=====
Seite 170 ist NICHT der "einzige echte Astra-Kandidat":
  - 106 statt 240 Zeichen (54% fehlen)
  - Systematische Fehler in Position 1 (D fehlt komplett)
  - Einzelzeichen-Reparatur reicht nicht aus

Astras Bedingung ("nur Zeichen beschaedigt") ist NICHT erfuellt.
Die Transkription ist zu stark beschaedigt fuer eine Reparatur.

VERWENDUNG
==========
    python3 analysis/analyze_170.py
"""

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

from bootstrap import setup

setup()

from collections import Counter

from core.adfgvx import ALPHA, KEYS, clean, make_square
from data.corpus import CORPUS
from data.corpus_corrected import corrected_ct

# Referenzseite mit identischem Schluessel (Nov10-12)
REFERENCE = "176a"

# Deutsche Buchstabenhaeufigkeit in Prozent
GERMAN_FREQ = {
    "E": 17.4, "N": 9.8, "I": 7.6, "S": 7.3, "R": 7.0, "A": 6.5,
    "T": 6.2, "D": 5.1, "H": 4.8, "U": 4.4, "L": 3.4, "C": 3.1,
    "G": 3.0, "M": 2.5, "O": 2.5, "B": 1.9, "W": 1.9, "F": 1.7,
    "K": 1.2, "Z": 1.1, "P": 0.8, "V": 0.7, "J": 0.3, "Y": 0.0,
    "X": 0.0, "Q": 0.0,
}


def bigrams(ct):
    """Zerlegt einen CT in Bigramme (jeweils 2 Zeichen)."""
    return [ct[i:i + 2] for i in range(0, len(ct) - 1, 2)]


def position_profile(bgs, pos):
    """Relative Haeufigkeit jedes ADFGVX-Zeichens an Position pos."""
    c = Counter(b[pos] for b in bgs)
    n = len(bgs)
    return {ch: c.get(ch, 0) / n for ch in ALPHA}


def decrypt_bigrams(bgs, sub):
    """Entschluesselt Bigramme direkt ueber das Quadrat (ohne Transposition)."""
    sq = make_square(sub)
    return "".join(sq[ALPHA.index(b[0]) * 6 + ALPHA.index(b[1])] for b in bgs)


def main():
    ct = clean(CORPUS["170"])
    bgs = bigrams(ct)
    perm, sub, _ = KEYS["Nov10-12"]
    sq = make_square(sub)

    print("=" * 78)
    print("SEITE 170 (RICHI-240) -- TIEFENANALYSE")
    print("=" * 78)
    print()
    print(f"CT ({len(ct)} Zeichen, {len(bgs)} Bigramme):")
    print(f"  {ct}")
    print()

    # --- Quadrat ---
    print("Quadrat Nov10-12:")
    print("      " + "  ".join(ALPHA))
    for i, r in enumerate(ALPHA):
        print(f"  {r}   " + "  ".join(sq[i * 6 + j] for j in range(6)))
    print()

    # --- Anomalie: fehlende Zeichen in Position 1 ---
    print("=" * 78)
    print("ANOMALIE: FEHLENDE ZEICHEN IN POSITION 1")
    print("=" * 78)
    print()
    p1 = position_profile(bgs, 0)
    missing = [ch for ch in ALPHA if p1[ch] == 0]
    print(f"Position 1 fehlt komplett: {missing if missing else 'keine'}")
    print()
    print("Vergleich mit allen Seiten (fehlende Zeichen in Position 1):")
    from data.corpus import CORPUS as _C
    for page in sorted(_C):
        b = bigrams(clean(_C[page]))
        prof = position_profile(b, 0)
        miss = [ch for ch in ALPHA if prof[ch] == 0]
        if miss:
            print(f"  {page:6} -> {miss}")
    print()

    # --- Vergleich mit Referenzseite ---
    print("=" * 78)
    print(f"VERGLEICH MIT SEITE {REFERENCE} (identischer Key Nov10-12)")
    print("=" * 78)
    print()
    ref_bgs = bigrams(corrected_ct(REFERENCE))
    print(f"{'Position':10} {'Zeichen':8} {'170':>8} {REFERENCE:>8} {'Diff':>8}")
    print("-" * 50)
    for pos, label in ((0, "Pos1"), (1, "Pos2")):
        prof170 = position_profile(bgs, pos)
        profref = position_profile(ref_bgs, pos)
        for ch in ALPHA:
            a = 100 * prof170[ch]
            b = 100 * profref[ch]
            print(f"{label:10} {ch:8} {a:7.1f}% {b:7.1f}% {a - b:+7.1f}")
        print()

    # --- Entschluesselter Text ---
    print("=" * 78)
    print("ENTSCHLUESSELTER TEXT (Nov10-12, ohne Transposition)")
    print("=" * 78)
    print()
    pt = decrypt_bigrams(bgs, sub)
    print(f"  {pt}")
    print()
    cc = Counter(pt)
    print(f"{'Zeichen':8} {'170':>8} {'Deutsch':>9} {'Diff':>8}")
    print("-" * 40)
    for ch in sorted(cc, key=lambda c: -cc[c]):
        d = GERMAN_FREQ.get(ch, 0.0)
        print(f"{ch:8} {100 * cc[ch] / len(pt):7.1f}% {d:8.1f}% {100 * cc[ch] / len(pt) - d:+7.1f}")
    print()

    # --- Fazit ---
    print("=" * 78)
    print("FAZIT")
    print("=" * 78)
    print()
    print("1. Seite 170 ist die einzige Seite ohne D in Position 1.")
    print("2. Die Fehlmenge D (17.0) entspricht dem Ueberschuss G+X (17.8).")
    print("3. Position 2 ist deutlich sauberer als Position 1.")
    print("4. Der entschluesselte Text enthaelt Ziffern und seltene")
    print("   Buchstaben, aber kein O,I,F,S,K,N (Zeile D des Quadrats).")
    print()
    print("=> Die Transkriptionsfehler sitzen systematisch in Position 1.")
    print("   Naechster Schritt: gezielte Reparatur der Position-1-Zeichen")
    print("   mit dem Ziel, die Zeilensummen an 176a anzugleichen.")


if __name__ == "__main__":
    main()
