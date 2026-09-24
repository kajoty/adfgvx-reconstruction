#!/usr/bin/env python3
"""
GELOESTE ADFGVX-KRYPTOGRAMME aus der Klausis-Krypto-Kolumne (Cipherbrain).

Quelle: Kommentarthread zum Artikel "ADFGVX" (Klaus Schmeh, 2017).
Loesungen von Norbert (Kommentare #15, #18, #19, #20, #24, #26, #32, #37,
#41, #42, #49, #53), Armin (#13), Max Baertl (#16/#17/#39) und
George Lasry (#50).

Notation im Klartext:
  X  = Worttrenner (Leerzeichen)
  -  = unleserliches Zeichen im Original
  Zahlen/Buchstaben = Klartextzeichen

Die Klartexte sind die von den Kommentatoren veroeffentlichten Ergebnisse.
Sie wurden mit dem deutschen Sprachmodell (langmodel.py) validiert:
alle erreichen Scores deutlich ueber der Zufallsschwelle.
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core import langmodel

# Seite -> (Schluessel, Klartext, Quelle)
SOLVED: dict[str, tuple[str, str, str]] = {
    "100": (
        "Nov1-3",
        "KEINESTOERUNGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCHAUFBELGRADX",
        "Armin #13 / Norbert #40",
    ),
    "105": (
        "Nov1-3",
        "GERMANIAATAPPEKONSTANTINOPELXRFUERMITTEHMEERDIVIC9VNZUXTEL9VRX62X"
        "DOV2TTELEGRXN0X58XISTELTX32141XQ4XAXVOMX4CNOVEMBERNULEDIGTXA8MIRAL"
        "STAFX32398XB",
        "Norbert #15 / Max Baertl #39",
    ),
    "109": (
        "Nov1-3",
        "OXKXMXABENDMELDUNGXS4V4XUMBJRGA8GLETZTEVTVILEBEEVUETX1WEITEDEFDUX"
        "NIV5IMMARSCH4UFBELGRADERKAVV2XSONSTKEINEEDMILNISSEXXASOXK511",
        "Norbert #18 / Max Baertl #39",
    ),
    "146": (
        "Nov4-6",
        "FUNKSTELLEKERTSCHERHAE9TRB12X1FXR4FNAMENRICHARDEMILKARLXFUNKSTELLE"
        "NDORTIGENBEREICHSBENACHRICHTIGENXNACHRICHTENCHEF4BG7834X",
        "Norbert #19 / Max Baertl #39",
    ),
    "171": (
        "Nov7-9",
        "INUKRAINEUNDPOLENRUBELKURSETARKSTEIGENDINFOLGEBRUCHESZWISCHENDEUTS"
        "CHLANDUNDSOWJETREGIERUNGUNDERWARTUNGDERWIEDERHERSTELLUNGRUSSLANDSD"
        "URCHDEUTSCHLANDUNDENTENTE",
        "Norbert #20 / Max Baertl #39",
    ),
    "187": (
        "Nov13-15b",
        "SELLVXGENXKOMX9XAXKXBRESLAUXXBITTEWEGENDRINGENDERNOTLAGEINBEKLEIDU"
        "NGX4000XPAARSTIEFELZUNAECHSTNACHXODERBERG",
        "Norbert #24 / Max Baertl #39",
    ),
    "176a": (
        "Nov10-12",
        "DURCHBRUCHVORBEREITETXDURCHBRUCHSRICHTUNGNACHNORDENODERNORDOSTENER"
        "FOLGENWIRDXKANNJETZTNOCHNICHTBEEURTEILTWERDENX",
        "Norbert #26 / Max Baertl #39",
    ),
    "132": (
        "Nov4-6",
        "FUEREILVESEXWIEDERHOLETTELEGRXVONVIERTERPERIODEINFUENFTERX"
        "GEBETSORDER5MINXVVV",
        "Norbert #37 / Max Baertl #39",
    ),
    "??": (
        "Nov22-24",
        "ABSXMIDIV5XEILMELDGX24NX24NXARMADAKERTSCHXBRINGTENTENTEFLOTTEZWODI"
        "VISIONENXNEUSEELAENDERXENGLXUXFRANZOXMITXNURXOHLXKORPSFRISCHX3Y52",
        "Norbert #32 / Max Baertl #39",
    ),
    "164a": (
        "Nov7-9",
        "ELXDIEHOEHEX828XHOEHELX9IRXOXSONSTKEINEEREIGNISSEVONBEDEUTUNGXX",
        "Norbert #41 / #44",
    ),
    "164b": (
        "Nov7-9",
        "XINXTEMESVARXBEFRIEDNISXUNDXDIVVONXMIRCONACHWESTENUNDSUEDENWEGX"
        "LEIDERWEGEVOMGEGNERBESETZTX",
        "Norbert #42 / #43",
    ),
    "153a": (
        "Nov13-15a",
        "RUSSISCHEUNDPOLNHEERESVERKEHRVOLLERFASSENXWICHTIGESBESONDERESAUSPO"
        "LNVERKEHRUEBEROHLSTATIONVERZIFFERTFUNKENXSOWEITFERNSCHREIBERVERBDG"
        "NICHTARBEICETXRESTSSCHRIFTLICHXNACHCHEFX0X01",
        "George Lasry #50 / Norbert #53",
    ),
}


def main() -> None:
    print("=" * 100)
    print("GELOESTE ADFGVX-KRYPTogramme (Klausis Krypto Kolumne)")
    print("=" * 100)
    for page, (key, pt, src) in SOLVED.items():
        sc = langmodel.score(pt)
        print(f"\nSeite {page:5s} | Schluessel {key:11s} | Score {sc:7.2f} | {src}")
        print(f"  {pt}")
    print(f"\n{len(SOLVED)} Kryptogramme geloest.")


if __name__ == "__main__":
    main()
