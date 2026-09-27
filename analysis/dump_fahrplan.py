#!/usr/bin/env python3
"""
dump_fahrplan.py -- erzeugt einen FAHRPLAN, der JEDES Kryptogramm einzeln
darstellt und den vollstaendigen Entschluesselungsweg zeigt:

  1. Wie sieht die verschluesselte Nachricht aus? (Geheimtext, gruppiert)
  2. Wie ist der Schluessel? (Name, n, Quelle)
  3. Wie ist die Permutation? (Rangfolge + Leseordnung)
  4. Wie ist das Quadrat? (36 Zeichen + 6x6-Raster)
  5. Wie entschluesselt man? (Schritt 1 Transposition, Schritt 2 Substitution)
  6. Wie lautet die entschluesselte Nachricht? (Klartext + Lesefassung)

Aufruf:  python3 analysis/dump_fahrplan.py            # stdout
         python3 analysis/dump_fahrplan.py --write    # docs/FAHRPLAN_ENTSCHLUESSELUNG.md
         python3 analysis/dump_fahrplan.py --pages    # docs/fahrplan/*.md + Index
         python3 analysis/dump_fahrplan.py --html     # docs/fahrplan/*.html + Index
"""
from __future__ import annotations

import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bootstrap  # noqa: F401

from core.adfgvx import ALPHA, KEYS, clean, make_square, substitute, untranspose
from data.corpus import CORPUS
from data.corpus_corrected import CORRECTED, corrected_ct
from data.solutions import SOLVED
from data.childs_additional import (
    RICHI_264_CT_OCR, RICHI_264_PLAINTEXT, RICHI_264_KEY, RICHI_264_READING,
    RICHI_274_338_KEY, RICHI_274_338_PERM, RICHI_274_TABLE, RICHI_338_TABLE,
    RICHI_274_PLAINTEXT, RICHI_274_READING,
    RICHI_338_PLAINTEXT, RICHI_338_READING,
)

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
R222_CANDIDATE = (
    "TECHENDERXGESARMEEDENMERSCHDURMEINGARNAUFESERSCHLESIENANZIT"
    "UNTENSEINDERSTENNDWISSERDETERESEXKTERRMTLTAA1GRISISCASS"
)

# RICHI-240 -- verifiziert, nicht selbst geloest.
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


# --------------------------------------------------------------------------
# Formatierung
# --------------------------------------------------------------------------

def _fmt(text: str, width: int = 60) -> str:
    return "\n".join(text[i:i + width] for i in range(0, len(text), width))


def _groups(text: str, size: int = 5) -> str:
    return " ".join(text[i:i + size] for i in range(0, len(text), size))


def _square_grid(square: str) -> str:
    rows = []
    for r in range(6):
        cells = []
        for c in range(6):
            i = r * 6 + c
            ch = square[i] if i < len(square) else "-"
            cells.append(ch if ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" else ".")
        rows.append(" ".join(cells))
    return "\n".join(rows)


def _perm_reading_order(perm: list[int]) -> list[int]:
    """Leseordnung: Spaltenindizes in aufsteigender Rangfolge."""
    return sorted(range(len(perm)), key=lambda c: perm[c])


def _rank_perm(keyword: str) -> list[int]:
    """Alphabetische Rangfolge eines Schluesselworts (1-basiert, Gleichstand links zuerst)."""
    return [
        sum(1 for j, other in enumerate(keyword)
            if other < ch or (other == ch and j < i)) + 1
        for i, ch in enumerate(keyword)
    ]


def _table_to_ct(table: str, n: int) -> str:
    """Wandelt eine zeilenweise notierte Buch-Tabelle in den CT um.

    Die Tabellen in childs_additional.py sind ZEILENWEISE notiert, muessen
    aber SPALTENWEISE gelesen werden, um den CT zu ergeben, den decrypt()
    erwartet (siehe Kommentar in data/childs_additional.py).
    """
    raw = clean(table)
    rows = len(raw) // n
    return "".join(raw[r * n + c] for c in range(n) for r in range(rows))


def _square_from_plaintext(ct: str, pt: str, perm: list[int]) -> str:
    """Rekonstruiert das Quadrat aus CT+PT (wie verify_article_claim.py).

    Nur fuer Seite 217: das Schluesselwort liefert die Permutation, das
    Quadrat wird aus dem Paar (Geheimtext, Klartext) hergeleitet.
    """
    from core.adfgvx import FULL

    bgs = untranspose(clean(ct), perm)
    sq = ["?"] * 36
    for i, ch in enumerate(pt):
        bg = bgs[2 * i:2 * i + 2]
        if len(bg) == 2:
            sq[ALPHA.index(bg[0]) * 6 + ALPHA.index(bg[1])] = ch
    used = set(c for c in sq if c != "?")
    rest = [c for c in FULL if c not in used]
    for i in range(36):
        if sq[i] == "?":
            sq[i] = rest.pop(0)
    return "".join(sq)


def _col_lengths(length: int, n: int) -> list[int]:
    rows = (length + n - 1) // n
    rest = length % n
    if rest == 0:
        rest = n
    return [rows if i < rest else rows - 1 for i in range(n)]


# --------------------------------------------------------------------------
# Der Entschluesselungsweg (Schritt fuer Schritt, mit echten Zwischenwerten)
# --------------------------------------------------------------------------

def _decrypt_steps(ct: str, perm: list[int], square: str) -> str:
    """Zeigt die zwei Entschluesselungsschritte mit echten Zwischenwerten."""
    ct = clean(ct)
    square = make_square(square)
    n = len(perm)
    collen = _col_lengths(len(ct), n)
    order = _perm_reading_order(perm)
    zwischentext = untranspose(ct, perm)
    klartext = substitute(zwischentext, square)

    out = []
    out.append("**Schritt 1 — Spaltentransposition rueckgaengig machen**")
    out.append("")
    out.append(
        f"Der Geheimtext hat {len(ct)} Zeichen. Bei n = {n} Spalten ergibt das "
        f"{len(ct) // n} volle Zeilen; die Spaltenlaengen sind "
        f"`{collen[0]}`×{collen.count(collen[0])}"
        + (f" und `{collen[-1]}`×{collen.count(collen[-1])}" if len(set(collen)) > 1 else "")
        + "."
    )
    out.append("")
    out.append(
        "Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer "
        "**Raenge** ausgelesen. Zum Entschluesseln liest man sie in genau "
        "dieser Reihenfolge wieder ein:"
    )
    out.append("")
    out.append("```")
    out.append("Leseordnung (Spaltenindex, 0-basiert): " + ", ".join(str(c) for c in order))
    out.append("```")
    out.append("")
    out.append(
        "Danach zeilenweise lesen -> **Zwischentext** (ADFGVX-Bigramme):"
    )
    out.append("")
    out.append("```")
    out.append(_fmt(zwischentext))
    out.append("```")
    out.append("")
    out.append("**Schritt 2 — Substitution rueckgaengig machen**")
    out.append("")
    out.append(
        "Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = "
        "Zeile, zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen "
        "an dieser Stelle ist der Klartextbuchstabe."
    )
    out.append("")
    out.append("```")
    out.append(_fmt(klartext))
    out.append("```")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Ein Kryptogramm-Block
# --------------------------------------------------------------------------

def _cryptogram_block(
    title: str,
    ct: str,
    pt: str,
    keyname: str | None,
    status: str,
    reading: str | None = None,
    note: str | None = None,
    perm_override: list[int] | None = None,
    square_override: str | None = None,
) -> str:
    out = [f"## {title}", "", f"**Status:** {status}", ""]

    # 1. Geheimtext
    if ct:
        out += [
            f"### 1. Die verschluesselte Nachricht",
            "",
            f"{len(ct)} Zeichen = {len(ct) // 2} Bigramme. "
            "Gruppiert in Fuenfergruppen (Transkriptions-Konvention):",
            "",
            "```",
            _groups(ct),
            "```",
            "",
        ]
    else:
        out += [
            "### 1. Die verschluesselte Nachricht",
            "",
            "*Kein Geheimtext im Repo abgebildet.*",
            "",
        ]

    # 2./3./4. Schluessel, Permutation, Quadrat
    if keyname:
        perm, square, cnt = KEYS[keyname]
        if perm_override is not None:
            perm = perm_override
        if square_override is not None:
            square = square_override
        out += [
            "### 2. Der Schluessel",
            "",
            f"**`{keyname}`** — n = {len(perm)} Spalten, laut Lasry-Liste "
            f"{cnt}× verwendet.",
            "",
            "### 3. Die Permutation",
            "",
            "Rangfolge: `perm[c]` = alphabetischer Rang der Spalte `c` "
            "(1 = kleinster Rang, wird zuerst ausgelesen).",
            "",
            "```",
            "-".join(str(p) for p in perm),
            "```",
            "",
            "Leseordnung (Spalten in aufsteigender Rangfolge):",
            "",
            "```",
            ", ".join(str(c) for c in _perm_reading_order(perm)),
            "```",
            "",
            "### 4. Das Quadrat",
            "",
            "36 Zeichen, zeilenweise gelesen:",
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
            "",
        ]
    elif perm_override is not None and square_override is not None:
        out += [
            "### 2. Der Schluessel",
            "",
            f"**Schluesselwort `{P217_KEYWORD}`** — liefert die Permutation. "
            "Das Quadrat wird aus dem Paar (Geheimtext, Klartext) "
            "rekonstruiert (26 von 36 Zellen direkt belegt, Rest aufgefuellt).",
            "",
            "### 3. Die Permutation",
            "",
            "Rangfolge der 19 Buchstaben des Schluesselworts:",
            "",
            "```",
            "-".join(str(p) for p in perm_override),
            "```",
            "",
            "### 4. Das Quadrat",
            "",
            "```",
            square_override,
            "```",
            "",
            "```",
            _square_grid(square_override),
            "```",
            "",
        ]

    # 5. Entschluesselungsweg
    if ct and (keyname or (perm_override and square_override)):
        if keyname:
            perm, square, _ = KEYS[keyname]
            if perm_override is not None:
                perm = perm_override
            if square_override is not None:
                square = square_override
        else:
            perm, square = perm_override, square_override
        out += [
            "### 5. Wie man entschluesselt",
            "",
            _decrypt_steps(ct, perm, square),
            "",
        ]
    elif keyname:
        out += [
            "### 5. Wie man entschluesselt",
            "",
            "*Nicht moeglich — der Geheimtext ist nicht im Repo abgebildet. "
            "Der Klartext stammt aus einer externen Quelle.*",
            "",
        ]

    # 6. Klartext
    if pt:
        out += [
            "### 6. Die entschluesselte Nachricht",
            "",
            f"**Klartext** ({len(pt)} Zeichen, `X` = Worttrenner):",
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
    return "\n".join(out)


# --------------------------------------------------------------------------
# Gesamtdokument
# --------------------------------------------------------------------------

def build_fahrplan() -> str:
    parts: list[str] = []
    parts.append("# Fahrplan: Jedes Kryptogramm einzeln entschluesselt")
    parts.append("")
    parts.append(
        "Fuer jede Nachricht: (1) der Geheimtext, (2) der Schluessel, "
        "(3) die Permutation, (4) das Quadrat, (5) der Entschluesselungsweg "
        "Schritt fuer Schritt, (6) der Klartext."
    )
    parts.append("")
    parts.append(
        "**Verfahren (ADFGVX, 1918):** Zuerst wird der Klartext ueber ein "
        "6×6-Quadrat in ADFGVX-Bigramme substituiert, dann werden die "
        "Bigramm-Zeichen per Spaltentransposition umsortiert. Entschluesselt "
        "wird in umgekehrter Reihenfolge: erst Transposition rueckgaengig, "
        "dann Substitution."
    )
    parts.append("")

    # ---- Geloeste Korpus-Seiten -----------------------------------------
    parts.append("# A. Geloeste Korpus-Seiten")
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
                "geloest, **bewiesen** — Geheimtext aus unabhaengiger "
                "Transkription, Roundtrip exakt"
            )
        else:
            status = (
                "geloest — Klartext aus dem Kommentarthread, Geheimtext "
                "synthetisch aus dem Klartext rekonstruiert (Roundtrip "
                "zirkulaer)"
            )
        parts.append(
            _cryptogram_block(
                f"Korpus Seite {page}",
                ct,
                pt,
                keyname,
                status,
                note=f"*Quelle des Klartexts: {src}.*",
            )
        )

    # ---- Ungeloeste Korpus-Seiten ---------------------------------------
    parts.append("# B. Ungeloeste Korpus-Seiten")
    parts.append("")
    parts.append(
        "Der Geheimtext ist die Roh-Transkription aus `data/corpus.py` "
        "(`-` = unlesbares Zeichen). Kein Schluessel, kein Klartext — "
        "deshalb nur Schritt 1."
    )
    parts.append("")
    unsolved = sorted(
        (p for p in CORPUS if p not in SOLVED),
        key=lambda p: int("".join(c for c in p if c.isdigit()) or 0),
    )
    for page in unsolved:
        ct = clean(CORPUS[page])
        gaps = CORPUS[page].count("-")
        parts.append(
            _cryptogram_block(
                f"Korpus Seite {page}",
                ct,
                "",
                None,
                f"ungeloest — {gaps} unlesbare Zeichen in der Transkription",
            )
        )

    # ---- Seite 217 -------------------------------------------------------
    parts.append("# C. Seite 217 (RICHI-170) — extern bewiesen")
    parts.append("")
    parts.append(
        "Nicht ueber die Lasry-Liste geloest, sondern ueber das "
        "**Schluesselwort** `TRUPPENVERSCHIEBUNG`: es liefert die "
        "Permutation, das Quadrat wird aus dem Paar (Geheimtext, Klartext) "
        "rekonstruiert."
    )
    parts.append("")
    p217_perm = _rank_perm(P217_KEYWORD)
    p217_square = _square_from_plaintext(clean(CORPUS["217"]), P217_PLAINTEXT, p217_perm)
    parts.append(
        _cryptogram_block(
            "Seite 217 / RICHI-170",
            clean(CORPUS["217"]),
            P217_PLAINTEXT,
            None,
            "geloest, **bewiesen** — Roundtrip exakt, 0 Konflikte",
            reading=P217_READING,
            perm_override=p217_perm,
            square_override=p217_square,
        )
    )

    # ---- Childs-Nachrichten ---------------------------------------------
    parts.append("# D. Nachrichten aus dem Childs-Buch (ausserhalb des Korpus)")
    parts.append("")

    parts.append(
        _cryptogram_block(
            "RICHI-264",
            clean(RICHI_264_CT_OCR),
            RICHI_264_PLAINTEXT,
            RICHI_264_KEY,
            "geloest, **bewiesen** — 2 Reparaturen, exakter Roundtrip",
            reading=RICHI_264_READING,
            note=(
                "**Die zwei Reparaturen:** Bigramm 63 `AD` → `AG` "
                "(D/G-Verwechslung, Morse-plausibel), und `XG` fehlt nach "
                "Bigramm 64."
            ),
        )
    )

    parts.append(
        _cryptogram_block(
            "RICHI-222",
            R222_CT,
            R222_CANDIDATE,
            "Nov1-3",
            "Struktur **bewiesen**, Lueckenfuellung Kandidat",
            note=(
                "Von 114 Bigrammen sind nur 37 vollstaendig; 70 haben genau "
                "eine Luecke, 7 fehlen ganz. Der gezeigte Klartext ist der "
                "beste Beam-Search-Kandidat, **nicht** bewiesen."
            ),
        )
    )

    parts.append(
        _cryptogram_block(
            "RICHI-274",
            _table_to_ct(RICHI_274_TABLE, len(RICHI_274_338_PERM)),
            RICHI_274_PLAINTEXT,
            RICHI_274_338_KEY,
            "geloest, verifiziert (Roundtrip)",
            reading=RICHI_274_READING,
            note=(
                "Die Tabelle im Buch ist 15 Zeilen × 18 Zeichen und "
                "**zeilenweise** notiert; fuer die Entschluesselung wird sie "
                "**spaltenweise** gelesen (der oben gezeigte Geheimtext ist "
                "bereits die spaltenweise Lesung). Schluessel `Oct28-31` "
                "erstmals an echtem Klartext geprueft."
            ),
            perm_override=RICHI_274_338_PERM,
        )
    )

    parts.append(
        _cryptogram_block(
            "RICHI-338",
            _table_to_ct(RICHI_338_TABLE, len(RICHI_274_338_PERM)),
            RICHI_338_PLAINTEXT,
            RICHI_274_338_KEY,
            "geloest, **NICHT** roundtrip-verifiziert (22 CT-Fehler in der Tabelle)",
            reading=RICHI_338_READING,
            note=(
                "Beginnt mit den drei Einleitungszeilen "
                "`FUER SAUL WEINREICH DOPPELPUNKT`. Die Tabelle ist 18 Zeilen "
                "× 18 Zeichen und enthaelt OCR-Artefakte (`5`, `f`, `P`, `%`, "
                "`i`). Re-Encryption des Klartexts ergibt 22 Abweichungen — "
                "der Klartext ist sprachlich plausibel, aber nicht hart belegt."
            ),
            perm_override=RICHI_274_338_PERM,
        )
    )

    parts.append(
        _cryptogram_block(
            "RICHI-240",
            "",
            R240_PLAINTEXT,
            "Nov10-12",
            "verifiziert, **nicht von diesem Projekt geloest**",
            reading=R240_READING,
            note=(
                "Der Geheimtext ist **nicht im Repo abgebildet** — von 240 "
                "Zeichen sind 220 ueberliefert. Die 20 fehlenden Zeichen "
                "wurden extern ergaenzt (`VFFXX DXXVV XDXDX GXXAF`), drei "
                "Ziffern ueber ein franzoesisches Aufklaerungstelegramm "
                "bestimmt (7, 9, 6). Quelle: prinzai.com, 19.09.2026."
            ),
        )
    )

    return "\n".join(parts)


def write_doc() -> None:
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "docs", "FAHRPLAN_ENTSCHLUESSELUNG.md",
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_fahrplan())
    print(f"geschrieben: {path}")


# --------------------------------------------------------------------------
# Einzelseiten: docs/fahrplan/<slug>.md + Index
# --------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(ROOT, "docs", "fahrplan")


def _slug(title: str) -> str:
    """Dateiname aus dem Titel: 'Korpus Seite 100' -> 'korpus-100'."""
    s = title.lower()
    s = s.replace("korpus seite ", "korpus-").replace("seite ", "seite-")
    s = s.replace(" ", "-").replace("/", "-")
    return "".join(c for c in s if c.isalnum() or c in "-_.")


def _page_header(title: str, section: str, index: int, total: int,
                 prev_slug: str | None, next_slug: str | None) -> str:
    nav = []
    if prev_slug:
        nav.append(f"[← vorherige]({prev_slug}.md)")
    nav.append("[Index](README.md)")
    if next_slug:
        nav.append(f"[naechste →]({next_slug}.md)")
    return (
        f"# {title}\n\n"
        f"*{section} — Kryptogramm {index} von {total}*\n\n"
        f"{' | '.join(nav)}\n\n---\n"
    )


def _page_footer(prev_slug: str | None, next_slug: str | None) -> str:
    nav = []
    if prev_slug:
        nav.append(f"[← vorherige]({prev_slug}.md)")
    nav.append("[Index](README.md)")
    if next_slug:
        nav.append(f"[naechste →]({next_slug}.md)")
    return "\n---\n\n" + " | ".join(nav) + "\n"


def _collect_pages() -> list[tuple[str, str, str]]:
    """Liefert (slug, titel, abschnitt, block) fuer alle 28 Kryptogramme."""
    return [(s, t, sec, b) for s, t, sec, b, _d in _collect_data()]


def _collect_data() -> list[tuple[str, str, str, str, dict]]:
    """Wie _collect_pages(), liefert zusaetzlich die Rohdaten fuer HTML.

    Das dict enthaelt: ct, pt, keyname, status, reading, note, perm, square,
    cnt, gaps, solved.
    """
    pages: list[tuple[str, str, str, str, dict]] = []

    order = sorted(
        (p for p in SOLVED if p in CORPUS),
        key=lambda p: int("".join(c for c in p if c.isdigit()) or 0),
    )
    for page in order:
        keyname, pt, src = SOLVED[page]
        ct = corrected_ct(page)
        if page in CORRECTED:
            status = (
                "geloest, **bewiesen** — Geheimtext aus unabhaengiger "
                "Transkription, Roundtrip exakt"
            )
        else:
            status = (
                "geloest — Klartext aus dem Kommentarthread, Geheimtext "
                "synthetisch aus dem Klartext rekonstruiert (Roundtrip "
                "zirkulaer)"
            )
        title = f"Korpus Seite {page}"
        perm, square, cnt = KEYS[keyname]
        pages.append((
            _slug(title), title, "A. Geloeste Korpus-Seiten",
            _cryptogram_block(title, ct, pt, keyname, status,
                              note=f"*Quelle des Klartexts: {src}.*"),
            dict(ct=ct, pt=pt, keyname=keyname, status=status, reading=None,
                 note=f"*Quelle des Klartexts: {src}.*", perm=perm,
                 square=square, cnt=cnt, gaps=0, solved=True),
        ))

    unsolved = sorted(
        (p for p in CORPUS if p not in SOLVED),
        key=lambda p: int("".join(c for c in p if c.isdigit()) or 0),
    )
    for page in unsolved:
        ct = clean(CORPUS[page])
        gaps = CORPUS[page].count("-")
        title = f"Korpus Seite {page}"
        status = f"ungeloest — {gaps} unlesbare Zeichen in der Transkription"
        pages.append((
            _slug(title), title, "B. Ungeloeste Korpus-Seiten",
            _cryptogram_block(title, ct, "", None, status),
            dict(ct=ct, pt="", keyname=None, status=status, reading=None,
                 note=None, perm=None, square=None, cnt=None, gaps=gaps,
                 solved=False),
        ))

    p217_perm = _rank_perm(P217_KEYWORD)
    p217_square = _square_from_plaintext(clean(CORPUS["217"]), P217_PLAINTEXT, p217_perm)
    title = "Seite 217 / RICHI-170"
    status = "geloest, **bewiesen** — Roundtrip exakt, 0 Konflikte"
    pages.append((
        _slug(title), title, "C. Seite 217 (RICHI-170)",
        _cryptogram_block(
            title, clean(CORPUS["217"]), P217_PLAINTEXT, None, status,
            reading=P217_READING, perm_override=p217_perm,
            square_override=p217_square,
        ),
        dict(ct=clean(CORPUS["217"]), pt=P217_PLAINTEXT, keyname=None,
             status=status, reading=P217_READING, note=None, perm=p217_perm,
             square=p217_square, cnt=None, gaps=0, solved=True,
             keyword=P217_KEYWORD),
    ))

    childs = [
        ("RICHI-264", clean(RICHI_264_CT_OCR), RICHI_264_PLAINTEXT, RICHI_264_KEY,
         "geloest, **bewiesen** — 2 Reparaturen, exakter Roundtrip",
         RICHI_264_READING,
         "**Die zwei Reparaturen:** Bigramm 63 `AD` → `AG` (D/G-Verwechslung, "
         "Morse-plausibel), und `XG` fehlt nach Bigramm 64.", None),
        ("RICHI-222", R222_CT, R222_CANDIDATE, "Nov1-3",
         "Struktur **bewiesen**, Lueckenfuellung Kandidat", None,
         "Von 114 Bigrammen sind nur 37 vollstaendig; 70 haben genau eine "
         "Luecke, 7 fehlen ganz. Der gezeigte Klartext ist der beste "
         "Beam-Search-Kandidat, **nicht** bewiesen.", None),
        ("RICHI-274", _table_to_ct(RICHI_274_TABLE, len(RICHI_274_338_PERM)),
         RICHI_274_PLAINTEXT, RICHI_274_338_KEY,
         "geloest, verifiziert (Roundtrip)", RICHI_274_READING,
         "Die Tabelle im Buch ist 15 Zeilen × 18 Zeichen und **zeilenweise** "
         "notiert; fuer die Entschluesselung wird sie **spaltenweise** gelesen "
         "(der oben gezeigte Geheimtext ist bereits die spaltenweise Lesung). "
         "Schluessel `Oct28-31` erstmals an echtem Klartext geprueft.",
         RICHI_274_338_PERM),
        ("RICHI-338", _table_to_ct(RICHI_338_TABLE, len(RICHI_274_338_PERM)),
         RICHI_338_PLAINTEXT, RICHI_274_338_KEY,
         "geloest, **NICHT** roundtrip-verifiziert (22 CT-Fehler in der Tabelle)",
         RICHI_338_READING,
         "Beginnt mit den drei Einleitungszeilen `FUER SAUL WEINREICH "
         "DOPPELPUNKT`. Die Tabelle ist 18 Zeilen × 18 Zeichen und enthaelt "
         "OCR-Artefakte (`5`, `f`, `P`, `%`, `i`). Re-Encryption des Klartexts "
         "ergibt 22 Abweichungen — der Klartext ist sprachlich plausibel, aber "
         "nicht hart belegt.", RICHI_274_338_PERM),
        ("RICHI-240", "", R240_PLAINTEXT, "Nov10-12",
         "verifiziert, **nicht von diesem Projekt geloest**", R240_READING,
         "Der Geheimtext ist **nicht im Repo abgebildet** — von 240 Zeichen "
         "sind 220 ueberliefert. Die 20 fehlenden Zeichen wurden extern "
         "ergaenzt (`VFFXX DXXVV XDXDX GXXAF`), drei Ziffern ueber ein "
         "franzoesisches Aufklaerungstelegramm bestimmt (7, 9, 6). Quelle: "
         "prinzai.com, 19.09.2026.", None),
    ]
    for name, ct, pt, key, status, reading, note, perm in childs:
        if key:
            kperm, ksquare, kcnt = KEYS[key]
            if perm is not None:
                kperm = perm
        else:
            kperm = ksquare = kcnt = None
        pages.append((
            _slug(name), name, "D. Nachrichten aus dem Childs-Buch",
            _cryptogram_block(name, ct, pt, key, status, reading=reading,
                              note=note, perm_override=perm),
            dict(ct=ct, pt=pt, keyname=key, status=status, reading=reading,
                 note=note, perm=kperm, square=ksquare, cnt=kcnt, gaps=0,
                 solved=bool(ct)),
        ))

    return pages


def write_pages() -> None:
    os.makedirs(PAGES_DIR, exist_ok=True)
    pages = _collect_pages()
    total = len(pages)

    # Alte Seiten entfernen (falls Titel sich aendern)
    for fn in os.listdir(PAGES_DIR):
        if fn.endswith(".md") and fn != "README.md":
            os.remove(os.path.join(PAGES_DIR, fn))

    for i, (slug, title, section, block) in enumerate(pages):
        prev_slug = pages[i - 1][0] if i > 0 else None
        next_slug = pages[i + 1][0] if i + 1 < total else None
        # Der Block beginnt mit "## <Titel>" — auf der Einzelseite steht der
        # Titel schon im Kopf, also die erste Zeile entfernen.
        lines = block.split("\n")
        if lines and lines[0].startswith("## "):
            lines = lines[1:]
            while lines and not lines[0].strip():
                lines = lines[1:]
        body = (
            _page_header(title, section, i + 1, total, prev_slug, next_slug)
            + "\n" + "\n".join(lines) + "\n"
            + _page_footer(prev_slug, next_slug)
        )
        with open(os.path.join(PAGES_DIR, f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write(body)

    # Index
    idx = [
        "# Fahrplan — Einzelseiten",
        "",
        f"{total} Kryptogramme, je eine eigene Seite. Jede Seite zeigt: "
        "(1) Geheimtext, (2) Schluessel, (3) Permutation, (4) Quadrat, "
        "(5) Entschluesselungsweg, (6) Klartext.",
        "",
        "Gesamtdokument: [`../FAHRPLAN_ENTSCHLUESSELUNG.md`](../FAHRPLAN_ENTSCHLUESSELUNG.md)",
        "",
    ]
    cur_section = None
    for i, (slug, title, section, _block) in enumerate(pages):
        if section != cur_section:
            cur_section = section
            idx += ["", f"## {section}", ""]
        idx.append(f"{i + 1}. [{title}]({slug}.md)")
    idx.append("")
    with open(os.path.join(PAGES_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx))

    print(f"geschrieben: {total} Seiten + Index in {PAGES_DIR}")


# --------------------------------------------------------------------------
# HTML-Seiten: docs/fahrplan/*.html + Index (klickibunti)
# --------------------------------------------------------------------------

HTML_DIR = os.path.join(ROOT, "docs", "fahrplan")

CSS = """
:root {
  --bg: #0f1117; --panel: #171a23; --panel2: #1e2230; --line: #2b3145;
  --fg: #e6e9f0; --dim: #9aa3b8; --accent: #6ea8fe; --accent2: #ffd166;
  --ok: #4ade80; --warn: #fbbf24; --bad: #f87171;
  --mono: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 16px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.wrap { max-width: 980px; margin: 0 auto; padding: 28px 20px 80px; }
header.top {
  border-bottom: 1px solid var(--line); padding-bottom: 18px; margin-bottom: 26px;
}
header.top h1 { margin: 0 0 6px; font-size: 1.9rem; letter-spacing: -0.02em; }
header.top .sub { color: var(--dim); font-size: 0.95rem; }
nav.pager {
  display: flex; gap: 10px; flex-wrap: wrap; align-items: center;
  margin: 18px 0; font-size: 0.92rem;
}
nav.pager a, nav.pager span {
  padding: 7px 13px; border: 1px solid var(--line); border-radius: 999px;
  background: var(--panel); color: var(--fg);
}
nav.pager a:hover { border-color: var(--accent); background: var(--panel2); text-decoration: none; }
nav.pager .idx { border-color: var(--accent); color: var(--accent); }
nav.pager .off { color: #4a5169; }
section.card {
  background: var(--panel); border: 1px solid var(--line); border-radius: 14px;
  padding: 20px 22px; margin: 18px 0;
}
section.card > h2 {
  margin: 0 0 14px; font-size: 1.12rem; color: var(--accent2);
  display: flex; align-items: center; gap: 10px;
}
section.card > h2 .num {
  display: inline-flex; align-items: center; justify-content: center;
  width: 26px; height: 26px; border-radius: 8px; font-size: 0.85rem;
  background: var(--panel2); border: 1px solid var(--line); color: var(--accent);
}
pre {
  background: #0b0d13; border: 1px solid var(--line); border-radius: 10px;
  padding: 14px 16px; overflow-x: auto; font-family: var(--mono);
  font-size: 0.86rem; line-height: 1.5; margin: 12px 0;
}
code { font-family: var(--mono); font-size: 0.88em; }
p code, li code { background: var(--panel2); padding: 1px 6px; border-radius: 5px; }
.status {
  display: inline-block; padding: 5px 12px; border-radius: 999px;
  font-size: 0.85rem; border: 1px solid var(--line); background: var(--panel2);
}
.status.ok { border-color: #2f6b45; color: var(--ok); }
.status.warn { border-color: #6b5a2f; color: var(--warn); }
.status.bad { border-color: #6b3030; color: var(--bad); }
.note {
  border-left: 3px solid var(--accent); background: var(--panel2);
  padding: 12px 16px; border-radius: 0 10px 10px 0; margin: 14px 0;
  font-size: 0.93rem; color: #cfd6e6;
}
.grid6 {
  display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px;
  max-width: 340px; margin: 14px 0;
}
.grid6 div {
  aspect-ratio: 1; display: flex; align-items: center; justify-content: center;
  background: var(--panel2); border: 1px solid var(--line); border-radius: 8px;
  font-family: var(--mono); font-size: 1.05rem; font-weight: 600;
}
.grid6 div.gap { color: #4a5169; }
.grid6 div.hl { border-color: var(--accent); color: var(--accent); }
.perm { display: flex; flex-wrap: wrap; gap: 6px; margin: 14px 0; }
.perm div {
  min-width: 42px; padding: 7px 4px; text-align: center; border-radius: 8px;
  background: var(--panel2); border: 1px solid var(--line); font-family: var(--mono);
}
.perm div .r { display: block; font-size: 0.72rem; color: var(--dim); }
.perm div .c { display: block; font-size: 0.95rem; font-weight: 600; }
.perm div.first { border-color: var(--accent); }
.perm div.first .c { color: var(--accent); }
.ct { font-family: var(--mono); letter-spacing: 0.06em; word-break: break-all; }
.pt { font-family: var(--mono); letter-spacing: 0.04em; word-break: break-all; color: var(--ok); }
.steps { counter-reset: s; }
.step { border-left: 2px solid var(--line); padding-left: 16px; margin: 16px 0; }
.step h3 { margin: 0 0 8px; font-size: 1rem; color: var(--accent); }
table.idx { width: 100%; border-collapse: collapse; margin: 16px 0; }
table.idx th, table.idx td {
  text-align: left; padding: 9px 12px; border-bottom: 1px solid var(--line);
  font-size: 0.94rem;
}
table.idx th { color: var(--dim); font-weight: 600; font-size: 0.82rem;
  text-transform: uppercase; letter-spacing: 0.06em; }
table.idx tr:hover td { background: var(--panel2); }
table.idx td.n { color: var(--dim); width: 44px; font-family: var(--mono); }
h2.sec {
  margin: 34px 0 10px; font-size: 1.15rem; color: var(--accent2);
  border-bottom: 1px solid var(--line); padding-bottom: 8px;
}
footer.foot { margin-top: 40px; color: var(--dim); font-size: 0.85rem;
  border-top: 1px solid var(--line); padding-top: 16px; }
@media (max-width: 620px) {
  .wrap { padding: 18px 14px 60px; }
  header.top h1 { font-size: 1.45rem; }
  .grid6 { max-width: 100%; }
}
"""


def _esc(text: str) -> str:
    return html.escape(text, quote=False)


def _md_inline(text: str) -> str:
    """Minimales Markdown -> HTML: **fett**, *kursiv*, `code`."""
    out = _esc(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+?)`", r"<code>\1</code>", out)
    return out


def _html_page(title: str, section: str, index: int, total: int,
               prev_slug: str | None, next_slug: str | None,
               body: str) -> str:
    def pager() -> str:
        bits = []
        if prev_slug:
            bits.append(f'<a href="{prev_slug}.html">← vorherige</a>')
        else:
            bits.append('<span class="off">← vorherige</span>')
        bits.append('<a class="idx" href="index.html">Index</a>')
        if next_slug:
            bits.append(f'<a href="{next_slug}.html">naechste →</a>')
        else:
            bits.append('<span class="off">naechste →</span>')
        return '<nav class="pager">' + "".join(bits) + "</nav>"

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(title)} — ADFGVX-Fahrplan</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
<h1>{_esc(title)}</h1>
<div class="sub">{_esc(section)} — Kryptogramm {index} von {total}</div>
</header>
{pager()}
{body}
{pager()}
<footer class="foot">
ADFGVX-Fahrplan · erzeugt von <code>analysis/dump_fahrplan.py --html</code> ·
<a href="../FAHRPLAN_ENTSCHLUESSELUNG.md">Gesamtdokument (Markdown)</a>
</footer>
</div>
</body>
</html>
"""


def _html_square(square: str) -> str:
    cells = []
    for i in range(36):
        ch = square[i] if i < len(square) else "-"
        if ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            cells.append(f"<div>{_esc(ch)}</div>")
        else:
            cells.append('<div class="gap">·</div>')
    return '<div class="grid6">' + "".join(cells) + "</div>"


def _html_perm(perm: list[int]) -> str:
    order = _perm_reading_order(perm)
    first = order[0] if order else -1
    cells = []
    for c, r in enumerate(perm):
        cls = "first" if c == first else ""
        cells.append(
            f'<div class="{cls}"><span class="r">Sp {c}</span>'
            f'<span class="c">{r}</span></div>'
        )
    return '<div class="perm">' + "".join(cells) + "</div>"


def _html_decrypt_steps(ct: str, perm: list[int], square: str) -> str:
    ct = clean(ct)
    square = make_square(square)
    n = len(perm)
    collen = _col_lengths(len(ct), n)
    order = _perm_reading_order(perm)
    zwischentext = untranspose(ct, perm)
    klartext = substitute(zwischentext, square)

    lens = f"<code>{collen[0]}</code>×{collen.count(collen[0])}"
    if len(set(collen)) > 1:
        lens += f" und <code>{collen[-1]}</code>×{collen.count(collen[-1])}"

    return f"""<div class="steps">
<div class="step">
<h3>Schritt 1 — Spaltentransposition rueckgaengig machen</h3>
<p>Der Geheimtext hat {len(ct)} Zeichen. Bei n = {n} Spalten ergibt das
{len(ct) // n} volle Zeilen; die Spaltenlaengen sind {lens}.</p>
<p>Die Spalten wurden beim Verschluesseln in der Reihenfolge ihrer
<strong>Raenge</strong> ausgelesen. Zum Entschluesseln liest man sie in genau
dieser Reihenfolge wieder ein:</p>
<pre>Leseordnung (Spaltenindex, 0-basiert): {", ".join(str(c) for c in order)}</pre>
<p>Danach zeilenweise lesen → <strong>Zwischentext</strong> (ADFGVX-Bigramme):</p>
<pre class="ct">{_esc(_fmt(zwischentext))}</pre>
</div>
<div class="step">
<h3>Schritt 2 — Substitution rueckgaengig machen</h3>
<p>Jedes Bigramm ist eine Koordinate im 6×6-Quadrat: erstes Zeichen = Zeile,
zweites = Spalte (A=0, D=1, F=2, G=3, V=4, X=5). Das Zeichen an dieser Stelle
ist der Klartextbuchstabe.</p>
<pre class="pt">{_esc(_fmt(klartext))}</pre>
</div>
</div>"""


def _html_block(data: dict) -> str:
    ct = data["ct"]
    pt = data["pt"]
    perm = data["perm"]
    square = data["square"]
    status = data["status"]
    out: list[str] = []

    # Status-Badge
    low = status.lower()
    if "nicht" in low and ("verifiziert" in low or "bewiesen" in low):
        cls = "warn"
    elif "ungeloest" in low:
        cls = "bad"
    elif "kandidat" in low:
        cls = "warn"
    else:
        cls = "ok"
    out.append(f'<p><span class="status {cls}">{_md_inline(status)}</span></p>')

    # 1. Geheimtext
    if ct:
        out.append(
            '<section class="card"><h2><span class="num">1</span>'
            "Die verschluesselte Nachricht</h2>"
            f"<p>{len(ct)} Zeichen = {len(ct) // 2} Bigramme. Gruppiert in "
            "Fuenfergruppen (Transkriptions-Konvention):</p>"
            f'<pre class="ct">{_esc(_groups(ct))}</pre></section>'
        )
    else:
        out.append(
            '<section class="card"><h2><span class="num">1</span>'
            "Die verschluesselte Nachricht</h2>"
            "<p><em>Kein Geheimtext im Repo abgebildet.</em></p></section>"
        )

    # 2./3./4.
    if data.get("keyname"):
        out.append(
            '<section class="card"><h2><span class="num">2</span>'
            "Der Schluessel</h2>"
            f"<p><code>{_esc(data['keyname'])}</code> — n = {len(perm)} Spalten, "
            f"laut Lasry-Liste {data['cnt']}× verwendet.</p></section>"
        )
        out.append(
            '<section class="card"><h2><span class="num">3</span>'
            "Die Permutation</h2>"
            "<p>Rangfolge: <code>perm[c]</code> = alphabetischer Rang der "
            "Spalte <code>c</code> (1 = kleinster Rang, wird zuerst "
            "ausgelesen).</p>"
            + _html_perm(perm)
            + "<p>Leseordnung (Spalten in aufsteigender Rangfolge):</p>"
            f'<pre>{", ".join(str(c) for c in _perm_reading_order(perm))}</pre>'
            "</section>"
        )
        out.append(
            '<section class="card"><h2><span class="num">4</span>'
            "Das Quadrat</h2>"
            f'<pre class="ct">{_esc(square)}</pre>'
            "<p>Als 6×6-Raster (<code>·</code> = unleserliche Zelle):</p>"
            + _html_square(square)
            + "</section>"
        )
    elif perm is not None and square is not None:
        out.append(
            '<section class="card"><h2><span class="num">2</span>'
            "Der Schluessel</h2>"
            f"<p><strong>Schluesselwort <code>{_esc(data.get('keyword', P217_KEYWORD))}"
            "</code></strong> — liefert die Permutation. Das Quadrat wird aus "
            "dem Paar (Geheimtext, Klartext) rekonstruiert (26 von 36 Zellen "
            "direkt belegt, Rest aufgefuellt).</p></section>"
        )
        out.append(
            '<section class="card"><h2><span class="num">3</span>'
            "Die Permutation</h2>"
            "<p>Rangfolge der Buchstaben des Schluesselworts:</p>"
            + _html_perm(perm)
            + "</section>"
        )
        out.append(
            '<section class="card"><h2><span class="num">4</span>'
            "Das Quadrat</h2>"
            f'<pre class="ct">{_esc(square)}</pre>'
            + _html_square(square)
            + "</section>"
        )

    # 5.
    if ct and perm is not None and square is not None:
        out.append(
            '<section class="card"><h2><span class="num">5</span>'
            "Wie man entschluesselt</h2>"
            + _html_decrypt_steps(ct, perm, square)
            + "</section>"
        )
    elif data.get("keyname"):
        out.append(
            '<section class="card"><h2><span class="num">5</span>'
            "Wie man entschluesselt</h2>"
            "<p><em>Nicht moeglich — der Geheimtext ist nicht im Repo "
            "abgebildet. Der Klartext stammt aus einer externen Quelle.</em></p>"
            "</section>"
        )

    # 6.
    if pt:
        body = (
            '<section class="card"><h2><span class="num">6</span>'
            "Die entschluesselte Nachricht</h2>"
            f"<p><strong>Klartext</strong> ({len(pt)} Zeichen, "
            "<code>X</code> = Worttrenner):</p>"
            f'<pre class="pt">{_esc(_fmt(pt))}</pre>'
        )
        if data.get("reading"):
            body += f"<p><strong>Lesefassung:</strong> {_esc(data['reading'])}</p>"
        body += "</section>"
        out.append(body)

    if data.get("note"):
        out.append(f'<div class="note">{_md_inline(data["note"])}</div>')

    return "\n".join(out)


def _html_index(pages: list[tuple[str, str, str, str, dict]]) -> str:
    total = len(pages)
    rows = []
    cur = None
    for i, (slug, title, section, _b, data) in enumerate(pages):
        if section != cur:
            cur = section
            rows.append(f'<tr><td colspan="3"><h2 class="sec">{_esc(section)}</h2></td></tr>')
        low = data["status"].lower()
        if "ungeloest" in low:
            badge = '<span class="status bad">ungeloest</span>'
        elif "kandidat" in low or ("nicht" in low and "verifiziert" in low):
            badge = '<span class="status warn">teilweise</span>'
        else:
            badge = '<span class="status ok">geloest</span>'
        rows.append(
            f'<tr><td class="n">{i + 1}</td>'
            f'<td><a href="{slug}.html">{_esc(title)}</a></td>'
            f"<td>{badge}</td></tr>"
        )

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ADFGVX-Fahrplan — Index</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
<h1>ADFGVX-Fahrplan</h1>
<div class="sub">{total} Kryptogramme, je eine eigene Seite</div>
</header>
<section class="card">
<p>Jede Seite zeigt sechs Abschnitte: <strong>1.</strong> die verschluesselte
Nachricht, <strong>2.</strong> den Schluessel, <strong>3.</strong> die
Permutation, <strong>4.</strong> das Quadrat, <strong>5.</strong> den
Entschluesselungsweg Schritt fuer Schritt, <strong>6.</strong> die
entschluesselte Nachricht.</p>
<p>Gesamtdokument: <a href="../FAHRPLAN_ENTSCHLUESSELUNG.md">FAHRPLAN_ENTSCHLUESSELUNG.md</a>
· Markdown-Fassung: <a href="README.md">README.md</a></p>
</section>
<table class="idx">
<thead><tr><th>#</th><th>Kryptogramm</th><th>Status</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody>
</table>
<footer class="foot">
ADFGVX-Fahrplan · erzeugt von <code>analysis/dump_fahrplan.py --html</code>
</footer>
</div>
</body>
</html>
"""


def write_html() -> None:
    os.makedirs(HTML_DIR, exist_ok=True)
    pages = _collect_data()
    total = len(pages)

    for fn in os.listdir(HTML_DIR):
        if fn.endswith(".html"):
            os.remove(os.path.join(HTML_DIR, fn))

    for i, (slug, title, section, _block, data) in enumerate(pages):
        prev_slug = pages[i - 1][0] if i > 0 else None
        next_slug = pages[i + 1][0] if i + 1 < total else None
        doc = _html_page(title, section, i + 1, total, prev_slug, next_slug,
                         _html_block(data))
        with open(os.path.join(HTML_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(doc)

    with open(os.path.join(HTML_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(_html_index(pages))

    print(f"geschrieben: {total} HTML-Seiten + index.html in {HTML_DIR}")


def main() -> int:
    if "--write" in sys.argv:
        write_doc()
    elif "--pages" in sys.argv:
        write_pages()
    elif "--html" in sys.argv:
        write_html()
    else:
        print(build_fahrplan())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
