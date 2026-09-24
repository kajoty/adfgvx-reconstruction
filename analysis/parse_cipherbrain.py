#!/usr/bin/env python3
"""
Parst die Original-Transkriptionen aus dem Cipherbrain-Artikel
(docs/cipherbrain_pages/article_body.txt) und vergleicht sie mit dem
Korpus (data/corpus.py) und den Soll-Geheimtexten (data/solutions.py).

Hintergrund
-----------
Der Artikel "Unsolved ADFXVX messages from World War I" (Klaus Schmeh,
Cipherbrain, 23.02.2017) enthaelt die Geheimtexte als PNG-Bilder UND als
Klartext-Transkription im HTML. Diese Transkription ist die eigentliche
Originalquelle -- `data/corpus.py` ist nur eine (unreine) Abschrift davon.

Dieses Skript extrahiert die Transkriptionen seitenweise und stellt sie
dem Korpus gegenueber. Damit laesst sich pruefen, welche Korpus-Seiten
tatsaechlich der Originalquelle entsprechen.

Aufruf:
    python3 analysis/parse_cipherbrain.py            # Uebersicht
    python3 analysis/parse_cipherbrain.py --diff     # Zeichen-Diff je Seite
    python3 analysis/parse_cipherbrain.py --emit     # Python-Dict ausgeben
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLE = ROOT / "docs" / "cipherbrain_pages" / "article_body.txt"

# Zeilen, die zur Transkription gehoeren: nur ADFGVX-Zeichen, '-', '–', '—',
# '{', '}', '(', ')', Leerzeichen. Alles andere (Prosa) wird verworfen.
CT_LINE = re.compile(r"^[ADFGVXadfgvx\-\u2013\u2014{}()\s]+$")
PAGE_HDR = re.compile(r"^\s*Page\s+([0-9?]+)\s*(.*)$")
# Bildmarker, die zwischen Seitenkopf und Transkription stehen.
IMG_MARK = re.compile(r"^\s*\[\[IMG:.*\]\]\s*$")


def parse_article(path: Path = ARTICLE) -> dict[str, str]:
    """Liefert {seitenname: geheimtext} aus der Artikel-Transkription.

    Mehrfach vorkommende Seiten (z.B. 153, 164, 176) werden mit Suffix
    a/b/... unterschieden, sofern sie sich unterscheiden.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    pages: dict[str, list[str]] = {}
    current: str | None = None
    note = ""

    for raw in lines:
        line = raw.rstrip()
        m = PAGE_HDR.match(line)
        if m:
            num, rest = m.group(1), m.group(2).strip()
            note = rest
            key = num
            if key in pages:
                # gleiche Seitenzahl erneut -> Suffix a/b/...
                suffix = "abcdefgh"
                idx = 1
                while f"{num}{suffix[idx-1]}" in pages:
                    idx += 1
                key = f"{num}{suffix[idx-1]}"
            pages[key] = []
            current = key
            continue

        if current is None:
            continue

        # Bildmarker ignorieren (steht zwischen Seitenkopf und Transkription)
        if IMG_MARK.match(line):
            continue

        # Ende des Transkriptionsblocks: eine Prosa-Zeile
        if line.strip() and not CT_LINE.match(line):
            # "Page 176 missing 10 letters" -> Notiz, Block bleibt offen
            if line.strip().startswith("Page"):
                continue
            current = None
            continue

        if line.strip():
            pages[current].append(line)

    result: dict[str, str] = {}
    for key, ls in pages.items():
        ct = "".join(ls)
        ct = re.sub(r"[\s]", "", ct)
        if ct:
            result[key] = ct
    return result


def normalize(ct: str) -> str:
    """Vereinheitlicht Sonderzeichen: Gedankenstriche -> '-', Klein -> Gross."""
    ct = ct.replace("\u2013", "-").replace("\u2014", "-")
    ct = ct.upper()
    return ct


def main() -> None:
    from data.corpus import CORPUS
    from data.solutions import SOLVED

    art = {k: normalize(v) for k, v in parse_article().items()}

    print("=" * 78)
    print("ORIGINAL-TRANSKRIPTION AUS DEM CIPHERBRAIN-ARTIKEL")
    print("=" * 78)
    print(f"Seiten im Artikel: {len(art)}")
    for k in sorted(art, key=lambda s: (len(s), s)):
        ct = art[k]
        n_unk = ct.count("-")
        print(f"  Seite {k:6} {len(ct):4} Zeichen, {n_unk:3} unleserlich ('-')")

    print()
    print("=" * 78)
    print("VERGLEICH MIT KORPUS (data/corpus.py)")
    print("=" * 78)
    print(f"{'Seite':7} {'Korpus':>7} {'Artikel':>8} {'Treffer':>8} {'Quote':>7}  Status")
    for page in sorted(CORPUS, key=lambda s: (len(s), s)):
        raw = normalize(re.sub(r"\s", "", CORPUS[page]))
        # Artikel-Key finden (Suffixe beruecksichtigen)
        cand = [k for k in art if k == page or k.startswith(page)]
        if not cand:
            print(f"{page:7} {len(raw):7} {'-':>8} {'-':>8} {'-':>7}  nicht im Artikel")
            continue
        a = art[cand[0]]
        # Positionsvergleich
        n = min(len(raw), len(a))
        hits = sum(1 for i in range(n) if raw[i] == a[i])
        quote = hits / max(len(a), 1) * 100
        status = "IDENTISCH" if raw == a else "abweichend"
        print(f"{page:7} {len(raw):7} {len(a):8} {hits:8} {quote:6.1f}%  {status}")

    print()
    print("=" * 78)
    print("VERGLEICH MIT SOLL-GEHEIMTEXTEN (data/solutions.py)")
    print("=" * 78)
    print(f"{'Seite':7} {'Soll':>6} {'Artikel':>8} {'Treffer':>8} {'Quote':>7}  Status")
    for page in sorted(SOLVED, key=lambda s: (len(s), s)):
        soll = normalize(SOLVED[page][1])
        cand = [k for k in art if k == page or k.startswith(page)]
        if not cand:
            print(f"{page:7} {len(soll):6} {'-':>8} {'-':>8} {'-':>7}  nicht im Artikel")
            continue
        a = art[cand[0]]
        n = min(len(soll), len(a))
        hits = sum(1 for i in range(n) if soll[i] == a[i])
        quote = hits / max(len(soll), 1) * 100
        status = "IDENTISCH" if soll == a else "abweichend"
        print(f"{page:7} {len(soll):6} {len(a):8} {hits:8} {quote:6.1f}%  {status}")

    if "--diff" in sys.argv:
        print()
        print("=" * 78)
        print("ZEICHEN-DIFF (Korpus vs. Artikel)")
        print("=" * 78)
        for page in sorted(CORPUS, key=lambda s: (len(s), s)):
            raw = normalize(re.sub(r"\s", "", CORPUS[page]))
            cand = [k for k in art if k == page or k.startswith(page)]
            if not cand:
                continue
            a = art[cand[0]]
            if raw == a:
                continue
            print(f"\n--- Seite {page} (Korpus {len(raw)} / Artikel {len(a)}) ---")
            n = min(len(raw), len(a))
            diffs = [(i, raw[i], a[i]) for i in range(n) if raw[i] != a[i]]
            print(f"  {len(diffs)} abweichende Positionen (von {n} verglichen)")
            for i, x, y in diffs[:40]:
                print(f"    pos {i:4}: Korpus={x}  Artikel={y}")
            if len(diffs) > 40:
                print(f"    ... und {len(diffs) - 40} weitere")

    if "--emit" in sys.argv:
        print()
        print("=" * 78)
        print("PYTHON-DICT (Original-Transkription)")
        print("=" * 78)
        print("ARTICLE_CT: dict[str, str] = {")
        for k in sorted(art, key=lambda s: (len(s), s)):
            print(f'    "{k}": (')
            ct = art[k]
            for i in range(0, len(ct), 60):
                print(f'        "{ct[i:i+60]}"')
            print("    ),")
        print("}")


if __name__ == "__main__":
    main()
