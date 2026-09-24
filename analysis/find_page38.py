"""Findet die gedruckte Seitenzahl 38 in der OCR-Datei des Childs-Buchs."""
from __future__ import annotations

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
TEXT = DOCS / "childs_djvu.txt"


def main() -> None:
    t = TEXT.read_text(encoding="utf-8", errors="replace")
    print(f"Datei: {TEXT} ({len(t)} Zeichen)")
    for pat in (r"\n\s*3[SB8]\s*\n", r"\n\s*38\s*\n"):
        hits = list(re.finditer(pat, t))
        print(f"Muster {pat!r}: {len(hits)} Treffer")
        for m in hits:
            ctx = t[max(0, m.start() - 150):m.start()].replace("\n", " ")[-110:]
            print(f"  {m.group(0)!r} @ {m.start()} | ...{ctx}")


if __name__ == "__main__":
    main()
