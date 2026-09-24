#!/usr/bin/env python3
"""Systematische Suche nach den 11 ungeloesten Korpus-Seiten im Childs-Buch.

Quelle: docs/childs_djvu.txt (OCR von archive.org, identifier 41784789082381).
Titel: "German Military Ciphers From February To November 1918" (J. R. Childs,
herausgegeben von W. F. Friedman, 63 Seiten).

Ziel: Pruefen, ob eine der ungeloesten Seiten (73, 152, 153b, 158, 170, 176b,
187b, 189, 198, 215, 217) im Buch als vollstaendiges Kryptogramm steht. Falls
ja, koennte die Buch-Transkription die beschaedigte Korpus-Transkription
ersetzen (Schritt 1: bessere Transkriptionen).

Ergebnis (2026-09-23): KEIN Treffer. Das Buch enthaelt nur Beispiel-Fragmente
und die RICHI-Nachrichten 152, 168, 222, 274, 338 (Oktober 1918) — keine davon
ist eine der 11 ungeloesten Korpus-Seiten.

Aufruf:
    python3 analysis/childs_scan.py            # Uebersicht
    python3 analysis/childs_scan.py --seqs     # alle ADFGVX-Sequenzen
    python3 analysis/childs_scan.py --page 217 # Detailvergleich einer Seite
"""
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup

setup()

import re

HERE = _os.path.dirname(_os.path.abspath(__file__))
ROOT = _os.path.dirname(HERE)
BOOK = _os.path.join(ROOT, "docs", "childs_djvu.txt")

UNSOLVED = ["73", "152", "153b", "158", "170", "176b",
            "187b", "189", "198", "215", "217"]

# Bekannte RICHI-Nachrichten im Buch (Oktober/November 1918, NICHT im Korpus).
# Alle wurden gegen die 11 ungeloesten Seiten geprueft -> LCB = 0.
KNOWN_RICHI = {
    "RICHI-152": "Oktober 9, 1918 (Faktor 22-2, Schluessel Okt 4-6)",
    "RICHI-168": "gepaart mit RICHI-222",
    "RICHI-222": "November 3, 1918 (13 Teile, 2 fehlend, 67+11 Zeichen fehlen)",
    "RICHI-264": "November 1, 1918 (2. Teil, 264 Zeichen, Schluessel Nov 1-3)",
    "RICHI-266": "November 2, 1918 (Wiederholung von 264)",
    "RICHI-274": "Oktober 30, 1918 (Duplikat von 338 minus 3 Zeilen)",
    "RICHI-338": "Oktober 30, 1918 (Schluessel Okt 28-31)",
}

# Vollstaendige Transkriptionen der wichtigsten RICHI-Nachrichten aus dem Buch.
# ACHTUNG: Keine davon ist eine der 11 ungeloesten Korpus-Seiten (LCB=0).
RICHI_TEXTS = {
    # Zeilen 11165-11185, Spaltenform (10 Zeilen x 26 Zeichen + Rest)
    "RICHI-264": (
        "DVDVFDVFAGXVXFFFVGGGAGGXAXDXGFXVVDDGFGFDFAVGVDAFGF"
        "GXDFDXVVDGDGVFFGDXDGAXAXV"
        "GVGAAAVFVGVFDGDXAFDXAXGVF"
        "AGDDDVGDVVGGDGGGVAADDGDVF"
        "VDDDXDVXDXDVDVAVGXVVDFVFD"
        "AXDGDAVGXDDDADGFVGDGAVAXD"
        "ADDGGFDFAGGFAXGFFXDGGGVGA"
        "FDFXXDAGAVGDVVFGXGFVFDXAA"
        "VAGAGAAVGDGGGFDVAGGVXAADD"
        "DDAVAVVADGDGDD"
    ),
    # Zeilen 10620-10650, Spaltenform (16 Zeilen x 18 Zeichen)
    "RICHI-274": (
        "AAGAGVVAFFFDXAVAXG"
        "AAXAXXXDDXDFDFVGFF"
        "XFAGDGDAAFXFFVVAGD"
        "FAAVXFAVVDGAGAADXG"
        "AAAGGXXAAFXADFXVFD"
        "VDXDXVFAVXAFXXGGAV"
        "DAFXFFAAFXDXXXAVFX"
        "XVFXXDXDGDXGDXFVVF"
        "FDAVXAXGAAXAFAADGF"
        "DAXGVFGFFXXDXFAAFD"
        "DXVAVFVXFVDDXFAAXD"
        "AAAADAFDADXFAFDAFX"
        "GAAVXDXXDXFGGAAVDX"
        "ADVDGFVAAAXVAGAVAX"
        "AXDAVAVDAAXADFXXVX"
        "GXVD"
    ),
    # Zeilen 10660-10700, Spaltenform (16 Zeilen x 18 Zeichen)
    "RICHI-338": (
        "VVDAFVAXFDADADGDGX"
        "AADDFAAXDADDXAXFFG"
        "XAFGVAVXXXGAGFAXFG"
        "VAVAFDDXAGVXAXDXDA"
        "VGXGXXAFAXXFGFAAFF"
        "VADXFDADGDGDFXDAFV"
        "ADAAFFAVXFXDFAXAA"
        "XVXAXGAVGGXGGDVFAF"
        "GGFAFDADXVXDFAAFX"
        "AVAXAXFVFFAVXAXVX"
        "FVXFFXAFXXDDXXADGX"
        "ADXFVDVGVXAXFDDXAA"
        "AAGAGFDAGVFXFAGFDF"
        "AAVXFXAFAVFXDXFDDF"
        "DAFVXAXFADADDVXDFF"
        "AVXAFAFAAVXDXXDDAGA"
    ),
}


def load_sequences(min_len=40):
    """Alle ADFGVX-Zeichenfolgen >= min_len aus dem Buch-OCR extrahieren."""
    txt = open(BOOK, encoding="utf-8", errors="replace").read()
    raw = re.findall(r"[ADFGVXadfgvx][ADFGVXadfgvx \n]{40,}", txt)
    out = set()
    for s in raw:
        c = re.sub(r"[^ADFGVXadfgvx]", "", s).upper()
        if len(c) >= min_len:
            out.add(c)
    return sorted(out, key=len, reverse=True)


def lcb(a, b, floor=10):
    """Laengster gemeinsamer Block (Longest Common Block) zweier Strings."""
    for L in range(min(len(a), len(b)), floor - 1, -1):
        for i in range(len(a) - L + 1):
            if a[i:i + L] in b:
                return L
    return 0


def main():
    if not _os.path.exists(BOOK):
        print(f"FEHLT: {BOOK}")
        print("Download: curl -sL -o docs/childs_djvu.txt "
              "https://archive.org/download/41784789082381/41784789082381_djvu.txt")
        return 1

    from data.corpus import CORPUS
    from core.adfgvx import clean

    seqs = load_sequences()
    print(f"Childs-Buch: {len(seqs)} ADFGVX-Sequenzen >= 40 Zeichen")
    print(f"Laengen: {[len(c) for c in seqs][:30]}")
    print()

    if "--seqs" in _sys.argv:
        for c in seqs:
            print(f"{len(c):4d}  {c}")
        return 0

    if "--page" in _sys.argv:
        page = _sys.argv[_sys.argv.index("--page") + 1]
        ct = clean(CORPUS[page])
        print(f"Seite {page}: {len(ct)} Zeichen")
        print(ct)
        print()
        for c in seqs:
            n = lcb(ct, c, floor=8)
            if n >= 8:
                print(f"  LCB={n:3d}  gegen Sequenz len={len(c)}")
        return 0

    print("=== Suche der 11 ungeloesten Korpus-Seiten im Buch ===")
    print(f"{'Seite':6s} {'len':>5s}  {'LCB':>4s}  Status")
    for p in UNSOLVED:
        ct = clean(CORPUS[p])
        best = max((lcb(ct, c, floor=8) for c in seqs), default=0)
        status = "TREFFER!" if best >= 30 else ("schwach" if best >= 12 else "kein")
        print(f"{p:6s} {len(ct):5d}  {best:4d}  {status}")

    print()
    print("=== Bekannte RICHI-Nachrichten im Buch (nicht im Korpus) ===")
    for name, desc in KNOWN_RICHI.items():
        print(f"  {name:12s} {desc}")
    print()
    print("=== Gegenprobe: RICHI-Texte vs. ungeloeste Seiten ===")
    for name, raw in RICHI_TEXTS.items():
        c = re.sub(r"[^ADFGVX]", "", raw.upper())
        best = max((lcb(clean(CORPUS[p]), c, floor=8) for p in UNSOLVED),
                   default=0)
        print(f"  {name:12s} len={len(c):4d}  max LCB gegen ungeloeste = {best}")
    print()
    print("FAZIT: Keine der 11 ungeloesten Seiten steht im Childs-Buch.")
    print("Das Buch enthaelt nur Beispiel-Fragmente + RICHI 152/168/222/264/266/")
    print("274/338 (Oktober/November 1918). Der Korpus stammt aus Schmehs")
    print("Cipherbrain-Artikel und ist eine ANDERE Auswahl.")
    return 0


if __name__ == "__main__":
    _sys.exit(main())
