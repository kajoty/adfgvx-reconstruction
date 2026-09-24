"""Extrahiert den Text einzelner PDF-Seiten aus childs_book.pdf.

Die Seiteninhalte sind FlateDecode-komprimiert; wir dekomprimieren die
Content-Streams und ziehen die Textoperatoren (Tj/TJ) heraus.
"""
from __future__ import annotations

import re
import sys
import zlib
from pathlib import Path

PDF = Path(__file__).resolve().parent.parent / "docs" / "childs_book.pdf"


def page_order(d: bytes) -> list[int]:
    nodes: dict[int, list[int]] = {}
    counts: dict[int, int] = {}
    for m in re.finditer(rb"(\d+)\s+0\s+obj", d):
        num = int(m.group(1))
        seg = d[m.end():m.end() + 8000]
        if b"/Pages" not in seg[:300]:
            continue
        kids = re.search(rb"/Kids\s*\[(.*?)\]", seg, re.S)
        if not kids:
            continue
        nodes[num] = [int(n) for n in re.findall(rb"(\d+)\s+0\s+R", kids.group(1))]
        c = re.search(rb"/Count\s+(\d+)", seg)
        counts[num] = int(c.group(1)) if c else -1
    root = max(counts, key=lambda k: counts[k])
    order: list[int] = []

    def walk(num: int) -> None:
        if num in nodes:
            for k in nodes[num]:
                walk(k)
        else:
            order.append(num)

    walk(root)
    return order


def obj_bytes(d: bytes, num: int) -> bytes:
    m = re.search(rb"(?<![0-9])" + str(num).encode() + rb"\s+0\s+obj", d)
    if not m:
        return b""
    end = d.find(b"endobj", m.end())
    return d[m.end():end if end > 0 else len(d)]


def page_text(d: bytes, objnum: int) -> str:
    body = obj_bytes(d, objnum)
    # Content-Referenzen
    refs = [int(n) for n in re.findall(rb"/Contents\s+(\d+)\s+0\s+R", body)]
    if not refs:
        arr = re.search(rb"/Contents\s*\[(.*?)\]", body, re.S)
        if arr:
            refs = [int(n) for n in re.findall(rb"(\d+)\s+0\s+R", arr.group(1))]
    out: list[str] = []
    for r in refs:
        stream = obj_bytes(d, r)
        sm = re.search(rb"stream\r?\n", stream)
        if not sm:
            continue
        raw = stream[sm.end():]
        raw = raw.rsplit(b"endstream", 1)[0]
        try:
            data = zlib.decompress(raw)
        except Exception:
            data = raw
        for tm in re.finditer(rb"\((?:\\.|[^\\()])*\)", data):
            s = tm.group(0)[1:-1]
            s = s.replace(b"\\(", b"(").replace(b"\\)", b")").replace(b"\\\\", b"\\")
            out.append(s.decode("latin-1"))
    return "".join(out)


def main() -> None:
    d = PDF.read_bytes()
    order = page_order(d)
    targets = [int(a) for a in sys.argv[1:]] or [44, 45]
    for p in targets:
        if 1 <= p <= len(order):
            txt = page_text(d, order[p - 1])
            print(f"===== PDF-Seite {p} (Objekt {order[p - 1]}) =====")
            print(txt[:2500])
            print()


if __name__ == "__main__":
    main()
