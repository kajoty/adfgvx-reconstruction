"""Rekonstruiert die PDF-Seitenreihenfolge von childs_book.pdf und ordnet
die gedruckten Seitenzahlen den PDF-Seiten zu."""
from __future__ import annotations

import re
from pathlib import Path

PDF = Path(__file__).resolve().parent.parent / "docs" / "childs_book.pdf"


def main() -> None:
    d = PDF.read_bytes()

    # Alle Objekte mit /Type /Pages einlesen
    nodes: dict[int, list[int]] = {}
    counts: dict[int, int] = {}
    for m in re.finditer(rb"(\d+)\s+0\s+obj", d):
        num = int(m.group(1))
        seg = d[m.end():m.end() + 8000]
        head = seg[:300]
        if b"/Pages" not in head:
            continue
        kids = re.search(rb"/Kids\s*\[(.*?)\]", seg, re.S)
        if not kids:
            continue
        nodes[num] = [int(n) for n in re.findall(rb"(\d+)\s+0\s+R", kids.group(1))]
        c = re.search(rb"/Count\s+(\d+)", seg)
        counts[num] = int(c.group(1)) if c else -1

    print("Knoten (Objekt -> Anzahl Kinder, Count):")
    for k in sorted(nodes):
        print(f"  {k}: {len(nodes[k])} Kinder, Count={counts[k]}")

    root = max(counts, key=lambda k: counts[k])
    print(f"\nWurzel: {root} (Count={counts[root]})")

    order: list[int] = []

    def walk(num: int) -> None:
        if num in nodes:
            for k in nodes[num]:
                walk(k)
        else:
            order.append(num)

    walk(root)
    print("PDF-Seiten gesamt:", len(order))
    print("Erste 8 Seitenobjekte:", order[:8])
    print("Letzte 5 Seitenobjekte:", order[-5:])


if __name__ == "__main__":
    main()
