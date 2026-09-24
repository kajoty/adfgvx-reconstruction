"""Hilfsskript: Zeigt den Text nach einem Suchbegriff im PDF-Stream an.

Reines Python (zlib + re), da auf diesem Server keine PDF-Werkzeuge
installiert sind (kein pdftotext/pdftoppm/tesseract).
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

import re
import zlib


def streams(pdf_path):
    data = open(pdf_path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n", data):
        start = m.end()
        end = data.find(b"endstream", start)
        if end == -1:
            continue
        try:
            out.append((m.start(), zlib.decompress(data[start:end])))
        except Exception:
            continue
    return out


def main():
    pdf = _sys.argv[1]
    needle = _sys.argv[2].encode("latin-1")
    span = int(_sys.argv[3]) if len(_sys.argv) > 3 else 6000
    for off, dec in streams(pdf):
        if needle in dec:
            txt = dec.decode("latin-1")
            i = txt.find(needle.decode("latin-1"))
            print("=== stream offset", off, "len", len(dec))
            print(txt[i:i + span])
            return
    print("not found:", needle)


if __name__ == "__main__":
    main()
