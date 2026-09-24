#!/usr/bin/env python3
"""
Extrahiert den Text von Section IX ("Solution of the ADFGVX System",
Par. 37-43) aus Friedmans "Military Cryptanalysis, Part IV -
Transposition and Fractionating Systems" (NSA ID:A59439).

Quelle: docs/41761079080022.pdf (156 Seiten, 12 MB).

Das PDF hat KEINE ToUnicode-CMap, d.h. die Tj-Strings sind in einer
Subset-Kodierung. Wir rekonstruieren den Text heuristisch:
  - Tj-Strings in Dokumentreihenfolge sammeln
  - Zeilenumbrueche anhand der Td/TD/T*-Operatoren erkennen
  - Abschnittsgrenzen ueber die Paragraphen-Marker (37., 38., ... 43.)

Ausgabe: docs/friedman_section_IX.txt (lesbar, mit Zeilennummern)
"""
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup

setup()

import re
import zlib

HERE = _os.path.dirname(_os.path.abspath(__file__))
ROOT = _os.path.dirname(HERE)
PDF = _os.path.join(ROOT, "docs", "41761079080022.pdf")
OUT = _os.path.join(ROOT, "docs", "friedman_section_IX.txt")


def decompress_streams(path):
    """Alle zlib-Streams dekomprimieren und aneinanderhaengen."""
    data = open(path, "rb").read()
    streams = re.findall(rb"stream\r?\n(.*?)endstream", data, re.S)
    out = b""
    for s in streams:
        try:
            out += zlib.decompress(s)
        except Exception:
            pass
    return out


def extract_lines(content):
    """Textzeilen aus den Tj/TJ-Operatoren rekonstruieren.

    Der OCR-Scan zerlegt jede Textzeile in viele kleine Tj-Stuecke, die
    jeweils mit einem eigenen Td positioniert werden. Wir gruppieren nach
    dem y-Versatz: gleicher y-Wert = gleiche Zeile. Zusaetzlich brechen wir
    bei einem grossen y-Sprung (> 2) hart um.
    """
    token_re = re.compile(
        rb"\((?:[^()\\]|\\.)*\)\s*Tj"
        rb"|\[(?:[^\[\]\\]|\\.)*\]\s*TJ"
        rb"|(?:[-\d.]+\s+){2}(?:Td|TD)"
        rb"|T\*"
    )
    lines = []
    cur = []
    cur_y = None

    def flush():
        if cur:
            lines.append("".join(cur))
            cur.clear()

    for m in token_re.finditer(content):
        tok = m.group(0)
        if tok.endswith(b"Tj"):
            inner = tok[tok.index(b"(") + 1:tok.rindex(b")")]
            inner = inner.replace(b"\\(", b"(").replace(b"\\)", b")")
            inner = inner.replace(b"\\\\", b"\\")
            cur.append(inner.decode("latin1"))
        elif tok.endswith(b"TJ"):
            parts = re.findall(rb"\((?:[^()\\]|\\.)*\)", tok)
            for p in parts:
                inner = p[1:-1].replace(b"\\(", b"(").replace(b"\\)", b")")
                cur.append(inner.decode("latin1"))
        else:
            nums = re.findall(rb"[-+]?[\d.]+", tok)
            if len(nums) >= 2:
                y = float(nums[1])
                if cur_y is None:
                    cur_y = y
                elif abs(y - cur_y) > 0.5:
                    flush()
                    cur_y = y
            else:
                flush()
                cur_y = None
    flush()
    return lines


def reflow(lines):
    """Fragmentierte OCR-Zeilen zu sinnvollen Absaetzen zusammenfuegen.

    Der Scan liefert pro Textzeile viele Fragmente. Wir haengen Fragmente
    aneinander, solange sie nicht offensichtlich eine neue Zeile beginnen
    (Paragraphen-Nummer, Grossbuchstaben-Ueberschrift, Seitenzahl).
    """
    out = []
    buf = ""
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        # Neuer Absatz / neue Ueberschrift?
        newpara = bool(
            re.match(r"^\d{1,2}\.\s", s)              # "37. Introductory..."
            or re.match(r"^[A-Z][A-Z ,.\-]{8,}$", s)  # Ueberschrift
            or re.match(r"^\d{1,3}$", s)              # Seitenzahl
            or re.match(r"^\(?[a-z]\)\s", s)          # "(a) ..."
        )
        if newpara and buf:
            out.append(buf)
            buf = s
        else:
            if buf and not buf.endswith(("-", " ")):
                buf += " "
            buf += s
    if buf:
        out.append(buf)
    return out


def clean_line(s):
    """OCR-Artefakte und Layout-Muell entfernen."""
    s = s.replace("\u00b7", " ").replace("\u00b7", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def find_section(lines):
    """Zeilenbereich von Section IX bestimmen.

    Anker: die Zeile, die "SECTION IX" UND "ADFGVX" enthaelt (echter
    Abschnittsanfang, nicht der Inhaltsverzeichnis-Eintrag).

    Ende: Section IX reicht laut Index von S. 97 bis S. 148 und wird von
    "SECTION XI / ANALYTICAL KEY" abgeloest. Die OCR zerlegt diese
    Ueberschrift in Fragmente ("8BC'l'IOJ!I'", "XI", "ANALYTICAL", "KEY"),
    daher wird auf das Paar "ANALYTICAL" + "KEY" geprueft. Zusaetzlich
    dienen "INDEX" und die Seitenzahl "97-148" als Notanker.

    Wichtig: Der Anker "ANALYTICAL KEY" steht erst auf S. 185, also NACH
    dem Ende von Section IX (S. 148). Section IX selbst endet mit
    Par. 58 ("Concluding remarks on transposition systems") auf S. 184.
    Der Extraktor schreibt daher bewusst bis zum ANALYTICAL-KEY-Anker und
    damit ueber Section IX hinaus, damit der Abschluss (Par. 57/58) und
    der Index vollstaendig im Textfile stehen.
    """
    start = None
    end = None
    for i, ln in enumerate(lines):
        if start is None and re.search(r"SECTION\s+IX\b", ln) \
                and re.search(r"ADFGVX", ln, re.I):
            start = i
        if start is not None and end is None and i > start + 5:
            if re.search(r"ANALYTICAL\s+KEY", ln, re.I) \
                    or re.search(r"^\s*INDEX\b", ln) \
                    or re.search(r"97\s*-\s*148", ln):
                end = i
    if start is None:
        return None, None
    if end is None:
        end = min(len(lines), start + 4000)
    return start, end


def main():
    if not _os.path.exists(PDF):
        print(f"FEHLT: {PDF}")
        return 1

    content = decompress_streams(PDF)
    raw = [clean_line(l) for l in extract_lines(content)]
    raw = [l for l in raw if l]

    start, end = find_section(raw)
    if start is None:
        print("Section IX nicht gefunden. Erste 40 Rohzeilen:")
        for l in raw[:40]:
            print(repr(l[:150]))
        return 1

    section = raw[start:end]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("Friedman, Military Cryptanalysis Part IV\n")
        f.write("Section IX: Solution of the ADFGVX System (Par. 37-58)\n")
        f.write("Quelle: docs/41761079080022.pdf (NSA ID:A59439)\n")
        f.write("Bereich: S. 97 bis S. 184 (Section IX), danach Section XI\n")
        f.write("        ANALYTICAL KEY (S. 185) und INDEX (S. 186-189).\n")
        f.write("=" * 72 + "\n\n")
        for i, ln in enumerate(section, 1):
            f.write(f"{i:5d}  {ln}\n")

    print(f"Section IX: Rohzeilen {start}..{end} ({len(section)} Zeilen)")
    print(f"Geschrieben: {OUT}")
    print()
    print("--- erste 25 Zeilen ---")
    for ln in section[:25]:
        print(ln[:190])
    return 0


if __name__ == "__main__":
    _sys.exit(main())
