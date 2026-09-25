#!/usr/bin/env python3
"""
dump_messages.py -- erzeugt das ausfuehrliche Nachrichtenverzeichnis fuer die
README: pro Nachricht Geheimtext, Klartext, Schluessel, Quadrat und Permutation
einzeln und vollstaendig.

Aufruf:  python3 analysis/dump_messages.py            # stdout
         python3 analysis/dump_messages.py --insert   # README aktualisieren
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bootstrap  # noqa: F401

from core.adfgvx import ALPHA, KEYS, clean, decrypt, make_square
from data.corpus import CORPUS
from data.corpus_corrected import CORRECTED, RECONSTRUCTED, corrected_ct
from data.solutions import SOLVED
from data.childs_additional import (
    RICHI_264_CT_OCR, RICHI_264_PLAINTEXT, RICHI_264_KEY, RICHI_264_READING,
    RICHI_274_338_KEY, RICHI_274_338_PERM, RICHI_274_TABLE, RICHI_338_TABLE,
    RICHI_274_PLAINTEXT, RICHI_274_READING,
    RICHI_338_PLAINTEXT, RICHI_338_READING,
)

BLOCK_BEGIN = "<!-- GENERATED: dump_messages.py -->"
BLOCK_END = "<!-- /GENERATED -->"

# Seite 217 (RICHI-170) -- extern bewiesen, Schluesselwort statt Lasry-Key.
P217_KEYWORD = "TRUPPENVERSCHIEBUNG"
P217_PLAINTEXT = (
    "EINENGLISCHERKREUZEREINLIEGXSEWASTOPOLXS4STENX"
    "EINGESCHWADERDERXALLIIERTENFOLGT26STENX"
)
P217_READING = (
    "Ein englischer Kreuzer liegt in Sewastopol. (am) 24. Ein Geschwader "
    "der Alliierten folgt (am) 26."
)

# RICHI-222 -- Struktur bewiesen, Lueckenfuellung Kandidat.
# Die 144 ueberlieferten CT-Zeichen, aus dem Raster in
# analysis/richi_222_reconstruct.py (12 Zeilen x 19 Spalten, '-' = Luecke).
R222_ROWS = [
    "F-V--D-F-G-GGAVGDAD",
    "X-F--D-X-D-VDVGVGGA",
    "V-G-VD-G-A-VDDVFGAA",
    "A-A-DV-A-G-FFXGDAGG",
    "X-A-AV-G-V-GDAD-DDV",
    "F-F-GD-A-V--GXG-GDF",
    "A-F--A-G-X-GGGD-VGA",
    "D-G--V-D-D-FX-G-GGG",
    "G-G--D-V-V-GDAG-VGF",
    "X-G----D---DXVV-XV-",
    "D-D-VD-X-F-XXGX-XFF",
    "F-A-DD-A--V-DX",
]
R222_CT = "".join(c for r in R222_ROWS for c in r if c in ALPHA)
R222_CT_PRESERVED = len(R222_CT)
R222_CANDIDATE = (
    "TECHENDERXGESARMEEDENMERSCHDURMEINGARNAUFESERSCHLESIENANZIT"
    "UNTENSEINDERSTENNDWISSERDETERESEXKTERRMTLTAA1GRISISCASS"
)

# RICHI-240 -- verifiziert, nicht selbst geloest.
R240_CT = 220
R240_PLAINTEXT = (
    "ANOBERSTEHEERESLEITUNGX11XARMEEXALPENKORPSIMRAUMPETERREVEVERBASZX"
    "217X219XDIVISIONENUND6XRESERVEDIVISIONANDERLINIENAGYBECSKEREKVERSECX"
    "VERSECVONSERBENBESETZTX"
)
R240_READING = (
    "An Oberste Heeresleitung. 11. Armee: Alpenkorps im Raum "
    "Peterreve-Verbasz. 217.-219. Divisionen und 6. Reserve-Division an der "
    "Linie Nagybecskerek-Versec. Versec von Serben besetzt."
)


def _fmt(text: str, width: int = 60) -> str:
    """Formatiert einen langen String in Bloecke fuer den Code-Block."""
    return "\n".join(text[i:i + width] for i in range(0, len(text), width))


def _square_grid(square: str) -> str:
    """6x6-Raster des Quadrats, mit '.' fuer Luecken."""
    rows = []
    for r in range(6):
        cells = []
        for c in range(6):
            i = r * 6 + c
            ch = square[i] if i < len(square) else "-"
            cells.append(ch if ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" else ".")
        rows.append(" ".join(cells))
    return "\n".join(rows)


def _perm_table(perm: list[int]) -> str:
    """Permutation als zweizeilige Tabelle: Spalte -> Rang."""
    n = len(perm)
    cols = " | ".join(f"{c + 1:>2}" for c in range(n))
    ranks = " | ".join(f"{perm[c]:>2}" for c in range(n))
    head = " | ".join("--" for _ in range(n))
    return f"| {cols} |\n|{head}|\n| {ranks} |"


def _key_block(keyname: str) -> str:
    perm, square, cnt = KEYS[keyname]
    gaps = square.count("-")
    out = [
        f"**Schlüssel `{keyname}`** — n = {len(perm)}, "
        f"Quadrat-Lücken: {gaps}, laut Lasry-Liste {cnt}× verwendet.",
        "",
        "Permutation (Rangfolge, `perm[c]` = Rang der Spalte `c`):",
        "",
        "```",
        "-".join(str(p) for p in perm),
        "```",
        "",
        "Quadrat (36 Zeichen, zeilenweise gelesen):",
        "",
        "```",
        square,
        "```",
        "",
        "Als 6×6-Raster (`.` = unleserliche Zelle in der Quelle):",
        "",
        "```",
        _square_grid(square),
        "```",
    ]
    return "\n".join(out)


def _message_block(
    title: str,
    ct: str,
    pt: str,
    keyname: str | None,
    status: str,
    reading: str | None = None,
    note: str | None = None,
) -> str:
    out = [f"### {title}", "", f"**Status:** {status}", ""]
    if keyname:
        out += [f"**Schlüssel:** `{keyname}`", ""]
    if ct:
        out += [
            f"**Geheimtext** ({len(ct)} Zeichen, {len(ct) // 2} Bigramme):",
            "",
            "```",
            _fmt(ct),
            "```",
            "",
        ]
    if pt:
        out += [
            f"**Klartext** ({len(pt)} Zeichen):",
            "",
            "```",
            _fmt(pt),
            "```",
            "",
        ]
    if reading:
        out += [f"**Lesefassung:** {reading}", ""]
    if note:
        out += [note, ""]
    if keyname:
        out += [_key_block(keyname), ""]
    return "\n".join(out)


def build_message_details() -> str:
    parts: list[str] = []

    # ---- Korpus: geloeste Seiten -----------------------------------------
    parts.append("## Gelöste Korpus-Seiten")
    parts.append("")
    parts.append(
        "Für jede Seite: der Geheimtext, mit dem sie tatsächlich entschlüsselt "
        "wurde (korrigiert bzw. rekonstruiert), der Klartext, und der "
        "vollständige Schlüssel."
    )
    parts.append("")

    order = sorted(
        (p for p in SOLVED if p in CORPUS),
        key=lambda p: int("".join(c for c in p if c.isdigit()) or 0),
    )
    for page in order:
        keyname, pt, src = SOLVED[page]
        ct = corrected_ct(page)
        if page in CORRECTED:
            status = (
                "gelöst, **bewiesen** — Geheimtext aus unabhängiger "
                "Transkription, Roundtrip exakt, 0 Konflikte"
            )
        else:
            status = (
                "gelöst — Klartext aus dem Kommentarthread, Geheimtext "
                "synthetisch aus dem Klartext rekonstruiert (Roundtrip "
                "zirkulär)"
            )
        note = f"*Quelle des Klartexts: {src}.*"
        parts.append(
            _message_block(
                f"Korpus Seite {page}",
                ct,
                pt,
                keyname,
                status,
                note=note,
            )
        )

    # ---- Korpus: ungeloeste Seiten ---------------------------------------
    parts.append("## Ungelöste Korpus-Seiten")
    parts.append("")
    parts.append(
        "Der Geheimtext ist die Roh-Transkription aus `data/corpus.py` "
        "(`-` = unlesbares Zeichen). Kein Klartext, kein Schlüssel."
    )
    parts.append("")
    unsolved = sorted(
        (p for p in CORPUS if p not in SOLVED),
        key=lambda p: int("".join(c for c in p if c.isdigit()) or 0),
    )
    for page in unsolved:
        ct = clean(CORPUS[page])
        raw = CORPUS[page]
        gaps = raw.count("-")
        parts.append(
            _message_block(
                f"Korpus Seite {page}",
                ct,
                "",
                None,
                f"ungelöst — {gaps} unlesbare Zeichen in der Transkription",
            )
        )

    # ---- Seite 217 -------------------------------------------------------
    parts.append("## Seite 217 (RICHI-170) — extern bewiesen")
    parts.append("")
    parts.append(
        "Nicht über die Lasry-Schlüsselliste gelöst, sondern über ein "
        "**Schlüsselwort**, das beide Stufen liefert: die Permutation "
        "(alphabetische Rangfolge) und ein Keyword-Quadrat mit eingestreuten "
        "Ziffern. Verifikation: `analysis/verify_article_claim.py`."
    )
    parts.append("")
    parts.append(
        _message_block(
            "Seite 217 / RICHI-170",
            clean(CORPUS["217"]),
            P217_PLAINTEXT,
            None,
            "gelöst, **bewiesen** — Roundtrip exakt, 0 Konflikte",
            reading=P217_READING,
            note=(
                f"**Schlüsselwort:** `{P217_KEYWORD}` — daraus die "
                "Permutation (Rangfolge der 19 Buchstaben) und das Quadrat "
                "`TRUPE4 / NVSC2H / 1I6B?G / 6AQD8F / 5?JKLM / 0?WXYZ` "
                "(`?` = handschriftlich nachgetragene Ziffer)."
            ),
        )
    )

    # ---- Childs-Nachrichten ---------------------------------------------
    parts.append("## Nachrichten aus dem Childs-Buch (außerhalb des Korpus)")
    parts.append("")

    parts.append(
        _message_block(
            "RICHI-264",
            clean(RICHI_264_CT_OCR),
            RICHI_264_PLAINTEXT,
            RICHI_264_KEY,
            "gelöst, **bewiesen** — 2 Reparaturen, exakter Roundtrip",
            reading=RICHI_264_READING,
            note=(
                "**Die zwei Reparaturen:** Bigramm 63 `AD` → `AG` "
                "(D/G-Verwechslung, Morse-plausibel), und `XG` fehlt nach "
                "Bigramm 64. Vor der Reparatur stimmten bereits 130 von 131 "
                "Zeichen. Verifikation: `analysis/verify_richi_264.py`."
            ),
        )
    )

    parts.append(
        _message_block(
            "RICHI-222",
            R222_CT,
            R222_CANDIDATE,
            "Nov1-3",
            "Struktur **bewiesen**, Lückenfüllung Kandidat",
            note=(
                f"Von 114 Bigrammen sind nur 37 vollständig; 70 haben genau "
                f"eine Lücke, 7 fehlen ganz. {R222_CT_PRESERVED} CT-Zeichen "
                "sind überliefert und werden von der Re-Encryption exakt "
                "reproduziert (0 Mismatches). Der gezeigte Klartext ist der "
                "beste Beam-Search-Kandidat (64 Worttreffer), **nicht** "
                "bewiesen. Verifikation: "
                "`analysis/richi_222_reconstruct.py`."
            ),
        )
    )

    parts.append(
        _message_block(
            "RICHI-274",
            clean(RICHI_274_TABLE),
            RICHI_274_PLAINTEXT,
            RICHI_274_338_KEY,
            "gelöst, verifiziert",
            reading=RICHI_274_READING,
            note=(
                "Erste Prüfung des Schlüssels `Oct28-31` an echtem Klartext. "
                "Die Tabelle im Buch ist 15 Zeilen × 18 Zeichen."
            ),
        )
    )

    parts.append(
        _message_block(
            "RICHI-338",
            clean(RICHI_338_TABLE),
            RICHI_338_PLAINTEXT,
            RICHI_274_338_KEY,
            "gelöst, verifiziert — OCR-Fehler in der Buch-Tabelle",
            reading=RICHI_338_READING,
            note=(
                "Beginnt mit den drei zusätzlichen Einleitungszeilen "
                "`FUER SAUL WEINREICH DOPPELPUNKT`, danach derselbe Text wie "
                "RICHI-274. Die Tabelle ist 18 Zeilen × 18 Zeichen und "
                "enthält OCR-Artefakte (`5`, `f`, `P`, `%`, `i`)."
            ),
        )
    )

    parts.append(
        _message_block(
            "RICHI-240",
            "",
            R240_PLAINTEXT,
            "Nov10-12",
            "verifiziert, **nicht von diesem Projekt gelöst**",
            reading=R240_READING,
            note=(
                f"Der Geheimtext ist **nicht im Repo abgebildet** — von "
                f"{R240_CT} der 240 Zeichen überliefert. Die 20 fehlenden "
                "Zeichen wurden extern ergänzt "
                "(`VFFXX DXXVV XDXDX GXXAF`), drei Ziffern über ein "
                "französisches Aufklärungstelegramm bestimmt (7, 9, 6). "
                "Quelle: prinzai.com, 19.09.2026."
            ),
        )
    )

    return "\n".join(parts)


def insert_into_readme() -> None:
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md"
    )
    with open(path, encoding="utf-8") as f:
        text = f.read()

    block = (
        f"{BLOCK_BEGIN}\n"
        "# Nachrichtenverzeichnis\n\n"
        "Jede Nachricht einzeln: Geheimtext, Klartext, Schlüssel, Quadrat und\n"
        "Permutation. Generiert aus dem Code (`analysis/dump_messages.py`).\n\n"
        f"{build_message_details()}\n"
        f"{BLOCK_END}\n"
    )

    # Alle vorhandenen Bloecke entfernen (auch versehentliche Duplikate),
    # damit wiederholte Laeufe idempotent sind.
    while BLOCK_BEGIN in text:
        start = text.index(BLOCK_BEGIN)
        end = text.index(BLOCK_END, start) + len(BLOCK_END)
        text = text[:start] + text[end:]

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
        print(build_message_details())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
