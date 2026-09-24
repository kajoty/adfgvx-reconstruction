#!/usr/bin/env python3
"""
Korrektur-Mechanismus: Sucht Einfuege-/Loeschoperationen, die einen
Kandidaten-Klartext lesbar machen.

Idee (nach Norbert, Cipherbrain-Kommentar #23):
  "Just trying to add or remove up to 5 characters at two different
   positions, performing an exhaustive search with an n-gram value function."

Wir beschraenken uns zunaechst auf EINE Operation pro Kandidat und
bewerten mit score_german().
"""

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import KEYS, clean, decrypt, score_german
from data.corpus import CORPUS

ALPHA = "ADFGVX"


def variants(ct: str, max_ops: int = 1, window: int = 0):
    """Erzeugt Varianten von ct durch Einfuegen/Loeschen von 1..max_ops Zeichen.

    window > 0 beschraenkt die Positionen auf die ersten/letzten `window`
    Zeichen (schneller, wenn der Fehler am Rand liegt).
    """
    yield ct, []
    if max_ops < 1:
        return
    n = len(ct)
    positions = range(n) if window == 0 else list(range(min(window, n))) + \
        list(range(max(0, n - window), n))
    for i in positions:
        # Loeschen
        yield ct[:i] + ct[i + 1:], [("del", i)]
        # Einfuegen
        for ch in ALPHA:
            yield ct[:i] + ch + ct[i:], [("ins", i, ch)]


def best_for(ct: str, perm, sub, max_ops: int = 1, window: int = 0):
    best = (-1e9, None, None)
    for cand, ops in variants(ct, max_ops, window):
        pt = decrypt(cand, perm, sub)
        sc = score_german(pt)
        if sc > best[0]:
            best = (sc, pt, ops)
    return best


def main() -> None:
    print("=" * 78)
    print("Korrektur-Suche: 1 Operation (Einfuegen/Loeschen) pro Seite")
    print("=" * 78)
    for page in sorted(CORPUS, key=lambda x: int(x.rstrip("ab"))):
        ct = clean(CORPUS[page])
        overall = (-1e9, None, None, None)
        for name, (perm, sub, _cnt) in KEYS.items():
            if len(sub) != 36:
                continue
            sc, pt, ops = best_for(ct, perm, sub, max_ops=1)
            if sc > overall[0]:
                overall = (sc, name, pt, ops)
        sc, name, pt, ops = overall
        flag = "  <<< LESBAR" if sc > -4.0 else ""
        print(f"\n{page:6s} {name:10s} {sc:7.2f} {ops}{flag}")
        print(f"       {pt[:70]}")


if __name__ == "__main__":
    main()
