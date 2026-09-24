#!/usr/bin/env python3
"""
Vollstaendige Verifikation der Artikel-Behauptung zu Seite 217.

Behauptung (prinzai.com, 17.09.2026):
  Schluesselwort : TRUPPENVERSCHIEBUNG (19 Buchstaben)
  Klartext       : EIN ENGLISCHER KREUZER EINLIEG X SEWASTOPOL X S4STEN X
                   EIN GESCHWADER DER X ALLIIERTEN FOLGT 26STEN X

Getestet wird die vollstaendige Matrix aller plausiblen Konventionen:
  - Ebene        : Zeichen (170) oder Bigramme (85)
  - Fuellrichtung: zeilenweise (row-major) oder spaltenweise (col-major)
  - Leserichtung : Spalten in Rangfolge aufsteigend oder absteigend
  - Padding      : kurze Spalten vorne oder hinten
  - Spaltenzuord.: Rang = Position (stabil) oder Rang = Buchstabe (mit Dupes)

Fuer jede Variante wird geprueft:
  A) Entschluesselung des echten Chiffrats -> Score/hits (Signal vs. Rauschen)
  B) Re-Encryption des behaupteten Klartexts -> identisch mit Chiffrat?
"""

from __future__ import annotations

import itertools

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, clean, make_square
from data.corpus import CORPUS
from core import langmodel

KEY = "TRUPPENVERSCHIEBUNG"
CT = clean(CORPUS["217"])
SQ = make_square(KEY)

# Der behauptete Klartext, ohne Leerzeichen/X-Trenner normalisiert.
PT_CLAIM_RAW = (
    "EIN ENGLISCHER KREUZER EINLIEG X SEWASTOPOL X S4STEN X "
    "EIN GESCHWADER DER X ALLIIERTEN FOLGT 26STEN X"
)
PT_CLAIM = "".join(ch for ch in PT_CLAIM_RAW.upper() if ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")


def col_lengths(length: int, n: int, pad_front: bool) -> list[int]:
    """Spaltenlaengen. pad_front=True: kurze Spalten zuerst."""
    rows = (length + n - 1) // n
    rest = length % n
    if rest == 0:
        rest = n
    if pad_front:
        return [rows - 1 if i < n - rest else rows for i in range(n)]
    return [rows if i < rest else rows - 1 for i in range(n)]


def order_of(key: str, descending: bool) -> list[int]:
    """Rangfolge der Spalten. descending=True liest Raenge rueckwaerts."""
    n = len(key)
    order = sorted(range(n), key=lambda c: (key[c], c))
    return order[::-1] if descending else order


def encrypt_variant(plain: str, key: str, *, level: str, fill_col_major: bool,
                    descending: bool, pad_front: bool) -> str:
    """Verschluesselt nach einer bestimmten Konvention."""
    n = len(key)
    rev = {ch: ALPHA[i // 6] + ALPHA[i % 6] for i, ch in enumerate(SQ)}
    units = [rev.get(ch, "??") for ch in plain.upper()]
    if level == "char":
        seq = "".join(units)
    else:
        seq = "".join(units)  # Bigramme sind bereits 2 Zeichen; Einheit = 2
    unit_len = 1 if level == "char" else 2
    n_units = len(seq) // unit_len
    units_list = [seq[i * unit_len:(i + 1) * unit_len] for i in range(n_units)]

    rows = (n_units + n - 1) // n
    grid: list[list[str | None]] = [[None] * n for _ in range(rows)]
    if fill_col_major:
        idx = 0
        for c in range(n):
            for r in range(rows):
                if idx < n_units:
                    grid[r][c] = units_list[idx]
                    idx += 1
    else:
        idx = 0
        for r in range(rows):
            for c in range(n):
                if idx < n_units:
                    grid[r][c] = units_list[idx]
                    idx += 1

    order = order_of(key, descending)
    out: list[str] = []
    for c in order:
        for r in range(rows):
            if grid[r][c] is not None:
                out.append(grid[r][c])  # type: ignore[arg-type]
    return "".join(out)


def decrypt_variant(ct: str, key: str, *, level: str, fill_col_major: bool,
                    descending: bool, pad_front: bool) -> str:
    """Entschluesselt nach einer bestimmten Konvention."""
    n = len(key)
    unit_len = 1 if level == "char" else 2
    n_units = len(ct) // unit_len
    units = [ct[i * unit_len:(i + 1) * unit_len] for i in range(n_units)]

    collen = col_lengths(n_units, n, pad_front)
    order = order_of(key, descending)

    cols: list[list[str]] = [[] for _ in range(n)]
    pos = 0
    for c in order:
        take = collen[c]
        cols[c] = units[pos:pos + take]
        pos += take

    rows = (n_units + n - 1) // n
    seq: list[str] = []
    if fill_col_major:
        for c in range(n):
            for r in range(len(cols[c])):
                seq.append(cols[c][r])
    else:
        for r in range(rows):
            for c in range(n):
                if r < len(cols[c]):
                    seq.append(cols[c][r])
    joined = "".join(seq)
    if level == "char":
        return "".join(SQ[ALPHA.index(joined[i]) * 6 + ALPHA.index(joined[i + 1])]
                       for i in range(0, len(joined) - 1, 2))
    # Bigramm-Ebene: joined besteht bereits aus Bigrammen
    return "".join(SQ[ALPHA.index(joined[i]) * 6 + ALPHA.index(joined[i + 1])]
                   for i in range(0, len(joined) - 1, 2))


def main() -> None:
    print("=" * 78)
    print("VERIFIKATION ARTIKEL-BEHAUPTUNG SEITE 217")
    print("=" * 78)
    print(f"Schluesselwort : {KEY} ({len(KEY)} Buchstaben)")
    print(f"Chiffrat       : {len(CT)} Zeichen")
    print(f"Behaupteter PT : {len(PT_CLAIM)} Zeichen")
    print(f"Quadrat        : {SQ}")
    print()

    # --- Teil A: Entschluesselung des echten Chiffrats -------------------
    print("-" * 78)
    print("TEIL A: Entschluesselung des echten Chiffrats")
    print("-" * 78)
    print(f"{'Ebene':<7} {'Fuell':<10} {'Lesen':<10} {'Pad':<6} "
          f"{'Score':>8} {'hits':>5}  Bewertung")
    print("-" * 78)

    results_a = []
    for level, fill_col_major, descending, pad_front in itertools.product(
        ["char", "bigram"], [False, True], [False, True], [False, True]
    ):
        pt = decrypt_variant(CT, KEY, level=level, fill_col_major=fill_col_major,
                             descending=descending, pad_front=pad_front)
        sc = langmodel.score(pt)
        hits = langmodel.word_hits(pt)
        verdict = "SIGNAL" if sc > -24 else "Rauschen"
        results_a.append((sc, hits, level, fill_col_major, descending, pad_front, pt))
        print(f"{level:<7} {'col' if fill_col_major else 'row':<10} "
              f"{'desc' if descending else 'asc':<10} "
              f"{'front' if pad_front else 'back':<6} "
              f"{sc:>8.3f} {hits:>5}  {verdict}")

    results_a.sort(reverse=True)
    best = results_a[0]
    print()
    print(f"BESTE Variante: Score {best[0]:.3f}, hits {best[1]}")
    print(f"  Ebene={best[2]}, Fuell={'col' if best[3] else 'row'}, "
          f"Lesen={'desc' if best[4] else 'asc'}, Pad={'front' if best[5] else 'back'}")
    print(f"  Klartext: {best[6][:80]}")
    print(f"  Referenz: echter deutscher Text liegt bei -16..-21")
    print()

    # --- Teil B: Re-Encryption des behaupteten Klartexts -----------------
    print("-" * 78)
    print("TEIL B: Re-Encryption des behaupteten Klartexts")
    print("-" * 78)
    print(f"Behaupteter Klartext: {PT_CLAIM}")
    print(f"Laenge: {len(PT_CLAIM)} Zeichen -> {len(PT_CLAIM) * 2} Chiffrezeichen")
    print(f"Chiffrat hat aber: {len(CT)} Zeichen")
    print()

    matches = []
    for level, fill_col_major, descending, pad_front in itertools.product(
        ["char", "bigram"], [False, True], [False, True], [False, True]
    ):
        enc = encrypt_variant(PT_CLAIM, KEY, level=level, fill_col_major=fill_col_major,
                              descending=descending, pad_front=pad_front)
        ok = enc == CT
        if ok:
            matches.append((level, fill_col_major, descending, pad_front))
        print(f"{level:<7} {'col' if fill_col_major else 'row':<10} "
              f"{'desc' if descending else 'asc':<10} "
              f"{'front' if pad_front else 'back':<6} "
              f"{'IDENTISCH' if ok else 'verschieden'}  {enc[:40]}")

    print()
    if matches:
        print(f"*** {len(matches)} Variante(n) reproduzieren das Chiffrat! ***")
        for m in matches:
            print(f"    {m}")
    else:
        print("*** KEINE Variante reproduziert das Chiffrat. ***")
    print()

    # --- Teil C: Laengen-Konsistenz --------------------------------------
    print("-" * 78)
    print("TEIL C: Laengen-Konsistenz")
    print("-" * 78)
    print(f"Chiffrat-Zeichen        : {len(CT)}")
    print(f"Chiffrat-Bigramme       : {len(CT) // 2}")
    print(f"Behaupteter PT-Zeichen  : {len(PT_CLAIM)}")
    print(f"Erwartete Chiffrezeichen: {len(PT_CLAIM) * 2}")
    print(f"Differenz               : {len(CT) - len(PT_CLAIM) * 2}")
    print()
    if len(CT) == len(PT_CLAIM) * 2:
        print("Laengen passen zusammen.")
    else:
        print("ACHTUNG: Laengen passen NICHT zusammen!")
        print(f"  Das Chiffrat ist {len(CT) - len(PT_CLAIM) * 2} Zeichen zu lang.")
        print(f"  Das entspricht {(len(CT) - len(PT_CLAIM) * 2) // 2} fehlenden "
              f"Klartextzeichen.")


if __name__ == "__main__":
    main()
