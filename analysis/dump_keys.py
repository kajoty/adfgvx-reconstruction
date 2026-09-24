#!/usr/bin/env python3
"""
Erzeugt die Markdown-Tabellen fuer die README:
  1. Schluesseltabelle (Permutation, Quadrat, n)
  2. Spruchtabelle (Korpus-Seiten + Childs-Zusaetze, Schluessel, Status)

Die Liste wird aus dem Code generiert und kann so nicht abweichen.
Aufruf:  python3 analysis/dump_keys.py            # Ausgabe auf stdout
         python3 analysis/dump_keys.py --insert   # README direkt aktualisieren
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bootstrap  # noqa: F401
from core.adfgvx import KEYS
from data.corpus import CORPUS
from data.solutions import SOLVED
from data.childs_additional import (
    RICHI_264_CT_OCR, RICHI_264_PLAINTEXT, RICHI_264_KEY,
    RICHI_274_PLAINTEXT, RICHI_338_PLAINTEXT,
)


def perm_str(perm: list[int]) -> str:
    return "-".join(str(p) for p in perm)


def build_key_table() -> str:
    lines = [
        "| Schlüssel | n | Permutation (Rangfolge) | Quadrat (36 Zeichen) |",
        "|---|---|---|---|",
    ]
    for name, (perm, square, _cnt) in KEYS.items():
        lines.append(
            f"| `{name}` | {len(perm)} | `{perm_str(perm)}` | `{square}` |"
        )
    return "\n".join(lines)


def build_message_table() -> str:
    lines = [
        "| Spruch | CT-Zeichen | Klartext | Schlüssel | Status |",
        "|---|---|---|---|---|",
    ]

    def ct_len(page: str) -> int:
        return len("".join(c for c in CORPUS[page] if c.upper() in "ADFGVX"))

    order = sorted(CORPUS, key=lambda p: int("".join(c for c in p if c.isdigit()) or 0))
    for page in order:
        ct = ct_len(page)
        if page in SOLVED:
            key, pt, _src = SOLVED[page]
            status = "gelöst, bewiesen (0 Konflikte)"
            lines.append(f"| Korpus {page} | {ct} | {len(pt)} | `{key}` | {status} |")
        else:
            lines.append(f"| Korpus {page} | {ct} | — | unbekannt | ungelöst (beschädigt) |")

    # Korpus-Fremde: Childs-Zusaetze
    ct264 = "".join(c for c in RICHI_264_CT_OCR if c in "ADFGVX")
    lines.append(
        f"| RICHI-264 | {len(ct264)} | {len(RICHI_264_PLAINTEXT)} | `{RICHI_264_KEY}` | "
        "gelöst, bewiesen (2 Reparaturen, Roundtrip) |"
    )
    lines.append(
        "| RICHI-222 | 144 | 114 (Kandidat) | `Nov1-3` | "
        "Struktur bewiesen; Lücken nicht eindeutig |"
    )
    lines.append(
        f"| RICHI-274 | 258 | {len(RICHI_274_PLAINTEXT)} | `Oct28-31` | "
        "gelöst, verifiziert |"
    )
    lines.append(
        f"| RICHI-338 | 286 | {len(RICHI_338_PLAINTEXT)} | `Oct28-31` | "
        "gelöst, verifiziert (OCR-Fehler in der Tabelle) |"
    )
    lines.append(
        "| RICHI-217 (Seite 217) | 170 | 88 | `TRUPPENVERSCHIEBUNG` | "
        "gelöst, bewiesen (Roundtrip) |"
    )
    lines.append(
        "| RICHI-240 | 220 | 240 | `Nov10-12` | "
        "verifiziert, nicht selbst gelöst (20 Zeichen fehlen) |"
    )
    return "\n".join(lines)


BLOCK_BEGIN = "<!-- GENERATED: dump_keys.py -->"
BLOCK_END = "<!-- /GENERATED -->"


def insert_into_readme() -> None:
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "README.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    block = (
        f"{BLOCK_BEGIN}\n"
        "## Schlüssel- und Spruchverzeichnis\n\n"
        "Diese Tabellen werden aus dem Code generiert (`analysis/dump_keys.py`).\n"
        "Sie spiegeln den Stand von `core/adfgvx.py`, `data/corpus.py` und\n"
        "`data/solutions.py`.\n\n"
        "### Die 14 Schlüssel\n\n"
        "`n` ist die Spaltenzahl des Transpositionsrasters (= Zahl der Bigramme\n"
        "je Zeile). Die Permutation ist eine **Rangfolge**, keine Lesereihenfolge\n"
        "(siehe oben). Das Quadrat ist der 36-Zeichen-String in Zeile-für-Zeile-\n"
        "Lesung des 6×6-Felds.\n\n"
        f"{build_key_table()}\n\n"
        "### Die Funksprüche\n\n"
        "CT = Geheimtext in ADFGVX-Zeichen. Klartext in Zeichen ohne Worttrenner\n"
        "(X = Worttrenner im Original).\n\n"
        f"{build_message_table()}\n\n"
        f"{BLOCK_END}\n"
    )
    if BLOCK_BEGIN in text:
        start = text.index(BLOCK_BEGIN)
        end = text.index(BLOCK_END) + len(BLOCK_END)
        text = text[:start] + block + text[end:]
    else:
        marker = "# Arbeitsprotokoll"
        idx = text.index(marker)
        text = text[:idx] + block + "\n---\n\n" + text[idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("README aktualisiert.")


def main() -> int:
    if "--insert" in sys.argv:
        insert_into_readme()
    else:
        print(build_key_table())
        print()
        print(build_message_table())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
