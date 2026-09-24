#!/usr/bin/env python3
"""
ADFGVX-Werkzeug fuer die ungeloesten Kryptogramme aus dem Ersten Weltkrieg.

Referenz: Klaus Schmeh, "The Top 50 unsolved encrypted messages: 46",
Cipherbrain, 23.02.2017.
https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/

Verifiziert am Artikel-Beispiel (HOUSE/ROBIN -> AGDVAAFAAVGXXGXAGDXADF)
und an Seite 105 (Norberts Schluessel reproduziert den Geheimtext exakt).
"""

from __future__ import annotations

ALPHA = "ADFGVX"
FULL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


# --------------------------------------------------------------------------
# Kern: Ver- und Entschluesselung
# --------------------------------------------------------------------------

def make_square(subkey: str) -> str:
    """Baut das 6x6-Quadrat (36 Zeichen) aus einem Substitutionsschluessel.

    Ist der Schluessel bereits vollstaendig (36 eindeutige Zeichen), wird er
    unveraendert zurueckgegeben. Sonst wird er als Schluesselwort behandelt
    und mit dem Restalphabet aufgefuellt.
    """
    subkey = subkey.upper()
    if len(subkey) == 36 and len(set(subkey)) == 36:
        return subkey
    seen: list[str] = []
    for ch in subkey:
        if ch in FULL and ch not in seen:
            seen.append(ch)
    for ch in FULL:
        if ch not in seen:
            seen.append(ch)
    return "".join(seen)


def substitute(bigrams: str, square: str) -> str:
    """Ersetzt ADFGVX-Bigramme durch Klartextzeichen."""
    out = []
    for i in range(0, len(bigrams) - 1, 2):
        bg = bigrams[i:i + 2]
        out.append(square[ALPHA.index(bg[0]) * 6 + ALPHA.index(bg[1])])
    return "".join(out)


def untranspose(ct: str, perm: list[int]) -> str:
    """Macht die Spaltentransposition rueckgaengig.

    `perm` ist die RANGFOLGE: perm[c] gibt an, welchen alphabetischen Rang
    Spalte c hat. Die Spalten werden also in der Reihenfolge aufsteigender
    Raenge ausgelesen. (Das war der Knackpunkt - die naive Deutung als
    Lesereihenfolge liefert nur Kauderwelsch.)
    """
    n = len(perm)
    length = len(ct)
    rows = (length + n - 1) // n
    rest = length % n
    if rest == 0:
        rest = n
    # Spaltenlaengen: die ersten `rest` Spalten haben `rows` Zeichen
    collen = [rows if i < rest else rows - 1 for i in range(n)]
    order = sorted(range(n), key=lambda c: perm[c])
    cols: list[str | None] = [None] * n
    pos = 0
    for c in order:
        cols[c] = ct[pos:pos + collen[c]]
        pos += collen[c]
    return "".join(
        cols[c][r]  # type: ignore[index]
        for r in range(rows)
        for c in range(n)
        if r < len(cols[c])  # type: ignore[arg-type]
    )


def transpose(bigrams: str, perm: list[int]) -> str:
    """Wendet die Spaltentransposition an (fuer Verifikation)."""
    n = len(perm)
    length = len(bigrams)
    rows = (length + n - 1) // n
    grid = [bigrams[i * n:(i + 1) * n] for i in range(rows)]
    order = sorted(range(n), key=lambda c: perm[c])
    out = []
    for c in order:
        for r in range(rows):
            if c < len(grid[r]):
                out.append(grid[r][c])
    return "".join(out)


def decrypt(ct: str, perm: list[int], subkey: str) -> str:
    """Entschluesselt einen ADFGVX-Geheimtext."""
    ct = clean(ct)
    square = make_square(subkey)
    return substitute(untranspose(ct, perm), square)


def encrypt(plain: str, perm: list[int], subkey: str) -> str:
    """Verschluesselt einen Klartext (fuer Verifikation)."""
    square = make_square(subkey)
    rev = {ch: ALPHA[i // 6] + ALPHA[i % 6] for i, ch in enumerate(square)}
    bigrams = "".join(rev.get(ch, "??") for ch in plain.upper())
    return transpose(bigrams, perm)


# --------------------------------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------------------------------

def clean(text: str) -> str:
    """Entfernt alles ausser ADFGVX (Leerzeichen, Zeilenumbrueche, '-' usw.)."""
    return "".join(ch for ch in text.upper() if ch in ALPHA)


def group(text: str, size: int = 5) -> str:
    """Formatiert Text in Fuenfergruppen."""
    return " ".join(text[i:i + size] for i in range(0, len(text), size))


# Haeufigkeiten deutscher Buchstaben (in Prozent, grob gerundet)
GERMAN_FREQ = {
    "E": 17.4, "N": 9.8, "I": 7.6, "S": 7.3, "R": 7.0, "A": 6.5,
    "T": 6.2, "D": 5.1, "H": 4.8, "U": 4.4, "L": 3.4, "C": 3.1,
    "G": 3.0, "M": 2.5, "O": 2.5, "B": 1.9, "W": 1.9, "F": 1.7,
    "K": 1.2, "Z": 1.1, "P": 0.8, "V": 0.7, "J": 0.3, "Y": 0.04,
    "X": 0.03, "Q": 0.02,
}

# Typische deutsche Bigramme
GERMAN_BIGRAMS = (
    "EN", "ER", "CH", "DE", "EI", "ND", "IE", "GE", "UN", "ST",
    "IN", "TE", "ES", "AN", "BE", "NG", "HE", "RE", "SE", "NE",
    "IC", "SC", "DI", "LE", "AU", "SI", "IT", "RA", "AL", "AR",
)


def score_german(text: str) -> float:
    """Deutsche Fitness: Log-Likelihood der Buchstaben- und Bigrammhaeufigkeit.

    Ziffern und X werden abgestraft - im Klartext sind sie selten bzw. nur
    als Trenner vorhanden. Zufallstext erreicht damit deutlich niedrigere
    Werte als echter deutscher Klartext.
    """
    if not text:
        return -1e9
    import math

    score = 0.0
    for ch in text:
        p = GERMAN_FREQ.get(ch, 0.01) / 100.0
        score += math.log(p)
    for i in range(len(text) - 1):
        bg = text[i:i + 2]
        if bg in GERMAN_BIGRAMS:
            score += 2.0
    # Ziffern sind im Klartext selten
    score -= sum(1 for ch in text if ch.isdigit()) * 3.0
    return score / len(text)


# --------------------------------------------------------------------------
# Bekannte Schluessel (George Lasry, Cipherbrain-Kommentar, 24.02.2017)
#
# Format: Name -> (Transpositions-Rangliste, Substitutionsquadrat, Anzahl
#                  der damit geloesten Kryptogramme)
#
# '-' im Substitutionsschluessel = unleserliches Zeichen in der Quelle.
# Die Quadrate sind 36 Zeichen lang; make_square() fuellt Luecken auf.
# --------------------------------------------------------------------------

KEYS: dict[str, tuple[list[int], str, int]] = {
    "Sep19-21": (
        [12, 2, 7, 20, 10, 19, 1, 13, 9, 18, 3, 17, 21, 8, 14, 4, 6, 16, 11, 22, 5, 15],
        "D5613Q9KBNO0HY8EISJUTZFCW7VPML2ARG4X", 15,
    ),
    "Oct4-6": (
        [4, 13, 3, 14, 1, 16, 9, 15, 5, 19, 10, 18, 6, 17, 7, 20, 11, 21, 8, 12, 22, 2],
        "YN87PJ3WRUCIEO1SKLZX0DFBH6MT9A2QV54G", 24,
    ),
    "Oct28-31": (
        [6, 15, 12, 16, 5, 7, 14, 4, 13, 8, 11, 1, 17, 2, 10, 3, 18, 9],
        "HI20SXRUWQY8EK7O619CBJAP453FDZTGLMVN", 33,
    ),
    "Nov1-3": (
        [3, 16, 4, 15, 7, 12, 18, 6, 17, 8, 19, 1, 13, 10, 2, 14, 11, 9, 5],
        "UILOF9RCZVSX02G7QTD8WNB5JMHEKPY41A36", 100,
    ),
    "Nov4-6": (
        [7, 10, 8, 14, 3, 11, 16, 1, 6, 13, 4, 9, 15, 5, 12, 17, 2],
        "17WHFLJ5D2UPEXKVZ9O0Q3Y6R8ABGITCMS4N", 106,
    ),
    "Nov7-9": (
        [6, 12, 7, 15, 1, 11, 16, 5, 8, 14, 3, 18, 9, 13, 2, 17, 20, 10, 19, 4],
        "PRMYUW3LZGES8C71QOV29ITB40-KXH-AJNDF", 93,
    ),
    "Nov10-12": (
        [9, 12, 7, 11, 3, 8, 16, 6, 14, 2, 10, 15, 5, 13, 1, 4],
        "4ARUT1OIFSKN3-BZPVLD-JMXCWHQ2E-G0-Y-", 46,
    ),
    "Nov13-15a": (
        [13, 8, 6, 16, 7, 18, 1, 14, 9, 20, 10, 15, 17, 2, 3, 11, 5, 19, 4, 12],
        "JZLH-R--S-T-MKDWU-V-B-P--FAO-GIX-CNE", 13,
    ),
    "Nov13-15b": (
        [4, 11, 5, 14, 9, 7, 16, 1, 12, 15, 6, 10, 3, 13, 8, 2],
        "H--BMUF15PX0DJLR---S6VONKZ-AWITEGC-", 52,
    ),
    "Nov16-18": (
        [7, 12, 1, 14, 8, 16, 13, 9, 19, 3, 15, 4, 10, 18, 6, 2, 11, 17, 5],
        "WG-EITNHUB2R--FDZJS---PY-VQL-1OAXMKC", 36,
    ),
    "Nov19-21": (
        [13, 20, 3, 16, 7, 14, 4, 12, 8, 11, 5, 15, 2, 18, 17, 10, 19, 6, 1, 9],
        "LC58QH7VI2YB9EURO60GX3MTFAKP1D4NJZSW", 12,
    ),
    "Nov22-24": (
        [6, 12, 16, 7, 14, 22, 11, 18, 1, 15, 8, 10, 20, 2, 13, 21, 3, 17, 19, 5, 9, 4],
        "QNZ72XS4C0IJY3RBEKL9FD6GMTHUVWA5O8P1", 26,
    ),
    "Nov25-28": (
        [21, 9, 6, 14, 10, 20, 1, 16, 18, 7, 15, 4, 11, 22, 5, 17, 23, 2, 12, 8, 19, 3, 13],
        "HQ05DKZAOYM6BEIWTJ7PSCFLV94132NGURX8", 33,
    ),
    "Nov28-Dec1": (
        [9, 3, 14, 10, 2, 8, 15, 4, 16, 11, 5, 13, 6, 12, 1, 7],
        "782GPY5OQHF91UDNI364TLVXEAR0JZBKMCSW", 29,
    ),
}


def try_all_keys(ct: str, verbose: bool = True) -> list[tuple[float, str, str]]:
    """Probiert alle bekannten Schluessel und liefert (score, name, klartext)."""
    results = []
    for name, (perm, sub, _cnt) in KEYS.items():
        if len(sub) != 36:
            if verbose:
                print(f"  {name}: Sub-Schluessel unvollstaendig ({len(sub)} Zeichen)")
            continue
        pt = decrypt(ct, perm, sub)
        results.append((score_german(pt), name, pt))
    results.sort(reverse=True)
    return results


if __name__ == "__main__":
    # Selbsttest am Artikel-Beispiel
    sq = "HOUSEABCDFGIJKLMNPQRTVWXYZ0123456789"
    ct = encrypt("IHAVEADREAM", [18, 15, 2, 9, 14], sq)
    print("Selbsttest (HOUSE/ROBIN):", ct)
    print("Erwartet:                AGDVAAFAAVGXXGXAGDXADF")
    print("OK" if ct == "AGDVAAFAAVGXXGXAGDXADF" else "FEHLER")
