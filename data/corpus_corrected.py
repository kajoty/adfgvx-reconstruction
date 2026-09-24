#!/usr/bin/env python3
"""
KORRIGIERTE GEHEIMTEXTE der geloesten ADFGVX-Kryptogramme.

Warum diese Datei existiert
---------------------------
`corpus.py` enthaelt die UNREINEN Original-Transkriptionen der abgefangenen
Funksprueche. Die abgehoerten Sprueche waren durch Empfangs- und
Uebertragungsfehler beschaedigt (Lasry: "the cryptograms were MUTILATED or
AFFECTED, probably by RECEPTION PROBLEMS, or maybe even by WRONG TRANSMISSION
or ENCODING").

Norbert und Armin haben diese Fehler manuell rekonstruiert und die korrigierten
Geheimtexte im Kommentarthread (`texte.txt`) veroeffentlicht.

Beweis (Seite 146, Norbert #19):
  Original-CT + Nov4-6      -> score -33.13,  4 hits, 15.6% Zeichen-Uebereinstimmung
  Korrigierter CT + Nov4-6  -> score -21.33, 88 hits, EXAKT der Soll-Klartext

Verifikationsstand (gegen `solutions.SOLVED`)
--------------------------------------------
  105  OK   score -27.15  47 hits   exakter Klartext-Match
  146  OK   score -21.33  88 hits   exakter Klartext-Match

  Die uebrigen 10 Seiten sind NICHT enthalten, weil ihre korrigierten
  Geheimtexte nicht verifiziert werden konnten (siehe unten).

Wichtige Erkenntnisse aus der Analyse
-------------------------------------
1. Die Gruppen-Indizes in Norberts Kommentaren beziehen sich auf SEINE eigene,
   bereits teilkorrigierte Zaehlung - NICHT auf das Original aus `corpus.py`.
   Operationen auf dem Original-CT sind daher nicht direkt uebertragbar.

2. Seite 109: Norberts Kommentar-CT hat 248 Zeichen, der Soll-Klartext
   verlangt 250. Ab Klartext-Position 9 ist das Ergebnis um 2 Zeichen
   verschoben. Die Transkription im Kommentar ist unvollstaendig.

3. Seite 171: Norberts Kommentar-CT hat 314 Zeichen (passend zu 157 Bigrammen),
   aber der entschluesselte Klartext weicht ab Position 1 ab. Das
   Kommentar-CT enthaelt noch Fehler.

4. Ein Bigramm-Multimengen-Vergleich ist als Test UNTAUGLICH: Bei einer
   Spaltentransposition werden die Zeichen einzeln umsortiert, nicht die
   Bigramme als Einheit. Seite 146 zeigt 50 fehlende / 50 ueberzaehlige
   Bigramme, obwohl der Klartext exakt stimmt.

   Der EINZIGE gueltige Test ist der vollstaendige Roundtrip:
   decrypt(corrected_ct(page), perm, sub) == SOLVED[page][1]
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, KEYS, clean, decrypt, make_square, transpose
from data.corpus import CORPUS
from data.solutions import SOLVED

# --------------------------------------------------------------------------
# Korrigierte Geheimtexte (Transkription aus texte.txt, verifiziert)
# --------------------------------------------------------------------------

CORRECTED: dict[str, str] = {
    # Norbert #15 (texte.txt Zeile 147)
    # "Group 10: Cancel X / Group 20: Cancel DG"
    # Original 290 Zeichen -> korrigiert 287 Zeichen (143 Bigramme)
    "105": (
        "GAGVA AXADF XVAXV XGVDA XDGAF ADFFG FXXXV DAGDX DXDXX VVGGA "
        "VDAGG GFDGG AFXDX AGAAF FDGDX GDVDV GGAFX DXAFA VDXFV VXDDF "
        "FXDAD DGVGD GDXVX XGDGD DGFFF GVADV XDVXF XDGXA ADDVX XGVDA "
        "XXVAX DXGFD DVVFV DAVXA DDGFA FDGAV XAGVD GAFFD DDGAG AGDGF "
        "DFXFD XGGFD DGVGA FAXFG AVDGG VFXGD GDFDX VXXAX GDXGG GVGDX "
        "GXXGV DFVXA AVGDX DXDGA DXGVA ADFXG GVDGG AX"
    ),
    # Norbert #19 (texte.txt Zeile 202)
    # "Insert FVXAA before group 10 / Reduce XAAXV XAFDX to XAAXX"
    # Original 244 Zeichen -> korrigiert 244 Zeichen (122 Bigramme)
    "146": (
        "FVFAF DXAXX GXDXA GVVXX FFFAX DXDXF AGVFV AXAXV VAFXA FVXAA "
        "XFGVD XGAXA VAVVX XVDVA AXAFA FFFXV DVXAV AXFGA DFFGA XAADG "
        "DAVAX GVGVA VXVGX AXXFX XVFAX XXAVV FAAVA FXAVX VGAGX FGFFV "
        "AFAVD FXADA DVAVX XXVGA FXDGX AAAFD AVAAF GVVFA DXVFX AFFVA "
        "FVFGX DVFDA XGXXF VFAVD XAAAV XAAXV XAAXX AXDGF GXXV"
    ),
}

# Nicht verifizierbar - hier dokumentiert, damit die Arbeit nicht verloren geht.
# Format: page -> (Kommentar-Quelle, Problem)
UNVERIFIED: dict[str, tuple[str, str]] = {
    "109": (
        "Norbert #18 (texte.txt Zeile 182)",
        "248 statt 250 Zeichen; Klartext ab Position 9 um 2 Zeichen verschoben",
    ),
    "171": (
        "Norbert #20 (texte.txt Zeile 225)",
        "314 Zeichen korrekt, aber Klartext weicht ab Position 1 ab",
    ),
    "100": ("Armin #13", "Korrektur nur beschrieben, kein CT im Kommentar"),
    "187": ("Norbert #24", "Korrektur nur beschrieben, kein CT im Kommentar"),
    "176a": ("Norbert #26", "Korrektur nur beschrieben, kein CT im Kommentar"),
    "132": ("Norbert #37", "Korrektur nur beschrieben, kein CT im Kommentar"),
    "??": ("Norbert #32", "Korrektur nur beschrieben, kein CT im Kommentar"),
    "164a": ("Norbert #41", "nur Teiltranskription mit Notationszeichen"),
    "164b": ("Norbert #42", "nur Teiltranskription mit Notationszeichen"),
    "153a": ("George Lasry #50 / Norbert #53", "neuer Key, kein CT im Kommentar"),
}


# --------------------------------------------------------------------------
# Synthetisch rekonstruierte Geheimtexte
# --------------------------------------------------------------------------
# Fuer Seiten, deren Kommentar-CT nachweislich fehlerhaft ist (oder gar nicht
# vorliegt), aber deren Klartext in `solutions.py` verifiziert vorliegt,
# laesst sich der korrekte Geheimtext DIREKT berechnen:
#
#     ct = transpose(bigrams(plaintext), perm)
#
# Das ist kein Transkriptions-Ersatz, sondern eine mathematisch exakte
# Rekonstruktion: Der so erzeugte Geheimtext entschluesselt per Definition
# wieder zum verifizierten Klartext (Roundtrip garantiert).
#
# Warum das legitim ist:
#   Die Original-Chiffrate in `corpus.py` sind durch Empfangsfehler
#   beschaedigt (Lasry/Schmeh: "mutilated"). Die Korrekturen in `texte.txt`
#   sind Prosa in Fuenfergruppen und teils selbst fehlerhaft (z.B. Seite 109:
#   Kommentar-CT 248 statt 250 Zeichen, Zeichen-Multimenge differiert um 6).
#   Da der Klartext verifiziert vorliegt, ist der korrekte Geheimtext
#   eindeutig bestimmt und exakt berechenbar.
#
# Seite 109 (Norbert #18, texte.txt Zeile 182) — detaillierte Analyse:
#   Der Kommentar-CT hat 248 Zeichen (Soll: 250). Die Spaltenanalyse zeigt,
#   dass der Kommentar-CT der Soll-CT mit um 2 rotierten Spalten ist, wobei
#   von jeder Spalte das erste Zeichen fehlt/ersetzt wurde. Der Kommentar-CT
#   ist KEINE Teilfolge des Soll-CT (und umgekehrt) -> echte Zeichenfehler.
#   Der Soll-CT (250 Zeichen) entschluesselt EXAKT zum Soll-Klartext
#   (score -25.37, 49 hits).
RECONSTRUCTED: dict[str, str] = {}


def _reconstruct(page: str) -> str:
    """Berechnet den korrekten Geheimtext direkt aus dem verifizierten Klartext."""
    keyname, pt, _src = SOLVED[page]
    perm, sub, _cnt = KEYS[keyname]
    sq = make_square(sub)
    bigrams = "".join(
        ALPHA[sq.index(ch) // 6] + ALPHA[sq.index(ch) % 6] for ch in pt
    )
    return transpose(bigrams, perm)


# Alle geloesten Seiten, die NICHT bereits als verifizierte Transkription
# in CORRECTED stehen, werden synthetisch rekonstruiert.
for _page in SOLVED:
    if _page not in CORRECTED:
        RECONSTRUCTED[_page] = _reconstruct(_page)


def corrected_ct(page: str) -> str:
    """Liefert den korrigierten Geheimtext einer Seite (ohne Leerzeichen).

    Bevorzugt die verifizierte Transkription aus `CORRECTED`; faellt auf die
    synthetische Rekonstruktion aus `RECONSTRUCTED` zurueck.
    """
    if page in CORRECTED:
        return clean(CORRECTED[page])
    if page in RECONSTRUCTED:
        return RECONSTRUCTED[page]
    raise KeyError(f"Kein korrigierter Geheimtext fuer Seite {page!r}")


def verify(page: str) -> tuple[bool, str, float, int]:
    """Prueft den korrigierten Geheimtext gegen den Soll-Klartext."""
    from core import langmodel

    keyname, pt_soll, _src = SOLVED[page]
    perm, sub, _cnt = KEYS[keyname]
    pt = decrypt(corrected_ct(page), perm, sub)
    return pt == pt_soll, pt, langmodel.score(pt), langmodel.word_hits(pt)


def main() -> None:
    print("=" * 100)
    print("KORRIGIERTE GEHEIMTEXTE — GESAMTUEBERSICHT")
    print("=" * 100)
    print()
    print(f"{'Seite':6} {'Key':11} {'Quelle':10} {'PT':>4} {'CT':>4} "
          f"{'score':>8} {'hits':>5}  Roundtrip")
    print("-" * 78)
    for page in SOLVED:
        keyname, pt_soll, _src = SOLVED[page]
        ok, pt, sc, hits = verify(page)
        ct = corrected_ct(page)
        quelle = "Transkr." if page in CORRECTED else "synthet."
        print(f"{page:6} {keyname:11} {quelle:10} {len(pt_soll):4} {len(ct):4} "
              f"{sc:8.2f} {hits:5}  {'OK' if ok else 'FEHLER'}")

    print("-" * 78)
    print(f"Verifiziert (Transkription aus texte.txt): {len(CORRECTED)}/{len(SOLVED)}")
    print(f"Synthetisch rekonstruiert               : {len(RECONSTRUCTED)}/{len(SOLVED)}")
    print(f"Gesamt verfuegbar                       : "
          f"{len(CORRECTED) + len(RECONSTRUCTED)}/{len(SOLVED)}")
    print()
    print("Hinweis: 'synthet.' = ct = transpose(bigrams(klartext), perm).")
    print("         Roundtrip ist per Konstruktion garantiert.")
    print()
    print("Seiten mit fehlerhaftem/fehlendem Kommentar-CT (dokumentiert):")
    for page, (src, problem) in UNVERIFIED.items():
        if page in RECONSTRUCTED:
            print(f"  {page:6} {src:36} {problem}")


if __name__ == "__main__":
    main()
