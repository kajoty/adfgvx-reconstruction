#!/usr/bin/env python3
"""
KORREKTE Rekonstruktion der fehlenden Zeichen in Seite 171.

WARUM DIE VORHERIGE VERSION SCHEITERTE:
  Der Greedy-Alignment-Ansatz (Zeichen fuer Zeichen von links nach rechts,
  bei Ungleichheit "fehlendes Zeichen" annehmen) ist fundamental defekt:
    - Er erkennt NUR Einfuegungen, keine Loeschungen.
    - Sobald EIN Zeichen zu viel ist, verschiebt sich alles danach, und der
      Algorithmus halluziniert Einfuegungen bis zum Ende.
  Minimalbeispiel: Soll "ABCDEFGH", Ist "ABXDEFGH" (X zu viel)
    -> Greedy findet 6 Einfuegungen und produziert "ABCDEFGHXDEFGH".
  Auf Seite 171 findet Greedy 243 Einfuegungen (statt 4) und verschlechtert
  den Score von -17.187 auf -34.978.

KORREKTER ANSATZ:
  Edit-Distance-Alignment (Levenshtein) mit Backtracking. Das findet die
  MINIMALE Zahl von Einfuegungen/Loeschungen/Ersetzungen.

BEFUND (2026-09-21):
  Der echte Geheimtext CORPUS['171'] hat 310 Zeichen, der Soll-Geheimtext
  (aus Klartext + Nov7-9) hat 314. Differenz: 4 Zeichen.
  ABER: Nach Alignment stimmen nur 205/314 = 65.3% der Zeichen ueberein.
  => Es fehlen nicht nur 4 Zeichen; der Geheimtext hat ~109 zusaetzliche
     Transkriptionsfehler. Eine "Reparatur" durch Einfuegen von 4 Zeichen
     ist daher NICHT moeglich.

VERWENDUNG:
  python3 repair_171.py
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import ALPHA, KEYS, clean, make_square, substitute, transpose, untranspose
from data.corpus import CORPUS
from data.solutions import SOLVED
from core import langmodel


def edit_alignment(expected: str, actual: str) -> list[tuple[str, int, str]]:
    """Levenshtein-Alignment mit Backtracking.

    Liefert eine Liste von Operationen (op, pos, char):
      ("ins", pos, ch)  - ch fehlt in actual an Position pos
      ("del", pos, ch)  - ch ist in actual an Position pos zu viel
      ("sub", pos, ch)  - actual[pos] sollte ch sein
    """
    m, n = len(expected), len(actual)
    # DP-Tabelle
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if expected[i - 1] == actual[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,       # Loeschung in expected = Einfuegung
                dp[i][j - 1] + 1,       # Einfuegung in expected = Loeschung
                dp[i - 1][j - 1] + cost  # Match/Substitution
            )
    # Backtracking
    ops: list[tuple[str, int, str]] = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and expected[i - 1] == actual[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(("sub", j - 1, expected[i - 1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(("ins", j, expected[i - 1]))
            i -= 1
        else:
            ops.append(("del", j - 1, actual[j - 1]))
            j -= 1
    ops.reverse()
    return ops


def main() -> None:
    ct = clean(CORPUS["171"])
    perm, subkey, _cnt = KEYS["Nov7-9"]
    square = make_square(subkey)
    pt_true = SOLVED["171"][1]

    rev = {ch: ALPHA[i // 6] + ALPHA[i % 6] for i, ch in enumerate(square)}
    expected_bigrams = "".join(rev[ch] for ch in pt_true)
    expected_ct = transpose(expected_bigrams, perm)

    print("=" * 78)
    print("SEITE 171 — Korrekte Fehleranalyse (Edit-Distance-Alignment)")
    print("=" * 78)
    print(f"Geheimtext (corpus.py) : {len(ct)} Zeichen")
    print(f"Soll-Geheimtext        : {len(expected_ct)} Zeichen")
    print(f"Differenz              : {len(expected_ct) - len(ct)} Zeichen")
    print()

    ops = edit_alignment(expected_ct, ct)
    n_ins = sum(1 for o in ops if o[0] == "ins")
    n_del = sum(1 for o in ops if o[0] == "del")
    n_sub = sum(1 for o in ops if o[0] == "sub")
    print(f"Edit-Distance-Alignment: {n_ins} Einfuegungen, {n_del} Loeschungen, "
          f"{n_sub} Ersetzungen")
    print(f"  (Edit-Distanz = {n_ins + n_del + n_sub})")
    print()

    # Vergleich mit dem Greedy-Ansatz
    print("Vergleich mit Greedy-Alignment (User-Version):")
    i, j = 0, 0
    greedy = 0
    recon = list(ct)
    while i < len(expected_ct) and j < len(recon):
        if expected_ct[i] == recon[j]:
            i += 1
            j += 1
        else:
            greedy += 1
            recon.insert(j, expected_ct[i])
            i += 1
            j += 1
    print(f"  Greedy findet {greedy} Einfuegungen -> {len(recon)} Zeichen "
          f"(statt {len(expected_ct)})")
    print()

    # Rekonstruktion mit dem korrekten Alignment
    fixed = list(ct)
    offset = 0
    for op, pos, ch in ops:
        if op == "ins":
            fixed.insert(pos + offset, ch)
            offset += 1
        elif op == "sub":
            fixed[pos + offset] = ch
        # "del": Zeichen entfernen
    # Loeschungen separat (von hinten, um Indizes nicht zu verschieben)
    dels = sorted([o[1] for o in ops if o[0] == "del"], reverse=True)
    for pos in dels:
        del fixed[pos]
    fixed = "".join(fixed)

    print(f"Rekonstruierter Geheimtext: {len(fixed)} Zeichen")
    print(f"Identisch mit Soll?       : {fixed == expected_ct}")
    print()

    # Entschluesselung
    dec = substitute(untranspose(fixed, perm), square)
    print(f"Entschluesselt == Klartext?: {dec == pt_true}")
    print(f"Score                     : {langmodel.score(dec):.3f} "
          f"(Ziel {langmodel.score(pt_true):.3f})")
    print()
    print(f"Entschluesselt: {dec[:78]}")
    print(f"Erwartet      : {pt_true[:78]}")
    print()

    print("FAZIT:")
    print("  Die Edit-Distanz ist viel groesser als 4. Der Geheimtext in")
    print("  corpus.py hat nicht nur 4 fehlende Zeichen, sondern ~109")
    print("  zusaetzliche Transkriptionsfehler. Eine Reparatur durch")
    print("  Einfuegen von 4 Zeichen ist NICHT moeglich.")
    print()
    print("  => Fuer Solver-Tests den SYNTHETISCHEN Geheimtext verwenden:")
    print("     transpose(bigrams(pt_true), perm)  (siehe reconstruct_171.py)")


if __name__ == "__main__":
    main()
