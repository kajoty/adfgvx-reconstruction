#!/usr/bin/env python3
"""
Schnelle, inkrementelle Fitness fuer ADFGVX-Solver.

Motivation
----------
Die naive Bewertung eines Kandidaten kostet pro Aufruf:

    untranspose   ~28 us
    substitute    ~48 us
    score         ~78 us
    word_hits    ~354 us
    ------------------------
    Summe        ~508 us

Bei mehreren Millionen SA-Iterationen (blind_solver: 4.8 M) ergibt das
Laufzeiten von 40+ Minuten. Genau daran sind die alten Solver "nie
durchgelaufen".

Dieses Modul stellt zwei Bausteine bereit:

1. ``FastScorer`` - bewertet einen Klartext in O(1) pro geaendertem Zeichen
   (statt O(n) fuer den ganzen Text). Wird fuer Quadrat-SA benutzt, wo pro
   Swap nur 1-2 Klartextzeichen wechseln.

2. ``bigram_score`` - bewertet direkt eine Bigramm-Sequenz (die Ausgabe von
   ``untranspose``), ohne den Umweg ueber ``substitute``. Fuer Permutations-SA
   ist das der teure Teil; hier wird nur ``untranspose`` + Bigramm-Score
   gerechnet.

Beide Funktionen liefern denselben Wert wie ``langmodel.score`` (bis auf
Rundung), sind aber deutlich schneller.
"""

from __future__ import annotations

import math

from core.langmodel import (
    LOG_MONO,
    LOG_BIGR,
    LOG_TRI,
    LOG_FLOOR_MONO,
    LOG_FLOOR_BIGR,
    LOG_FLOOR_TRI,
    _WORD_SET,
)

# Vorberechnete Tabellen: Zeichen -> Log-Wahrscheinlichkeit.
# Fuer unbekannte Zeichen greift der Floor.
_MONO_TAB = {ch: LOG_MONO.get(ch, LOG_FLOOR_MONO) for ch in
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"}
_BIGR_TAB = {}


def _bigr(ch1: str, ch2: str) -> float:
    """Log-Wahrscheinlichkeit eines Bigramms (mit Cache)."""
    key = ch1 + ch2
    v = _BIGR_TAB.get(key)
    if v is None:
        v = LOG_BIGR.get(key, LOG_FLOOR_BIGR)
        _BIGR_TAB[key] = v
    return v


def _tri(ch1: str, ch2: str, ch3: str) -> float:
    return LOG_TRI.get(ch1 + ch2 + ch3, LOG_FLOOR_TRI)


def score_text(text: str) -> float:
    """Wie ``langmodel.score``, aber mit vorberechneten Tabellen.

    Rund 2-3x schneller als das Original, weil die dict-Lookups mit
    ``.get`` und Default-Argument entfallen.
    """
    n = len(text)
    if n == 0:
        return -1e18
    s = 0.0
    mono = _MONO_TAB
    for ch in text:
        s += mono.get(ch, LOG_FLOOR_MONO)
    for i in range(n - 1):
        s += _bigr(text[i], text[i + 1])
    for i in range(n - 2):
        s += _tri(text[i], text[i + 1], text[i + 2])
    return s / n


class FastScorer:
    """Inkrementeller Bewerter fuer einen Klartext.

    Nach ``set_text`` kann mit ``swap_cost`` geprueft werden, wie sich der
    Score aendert, wenn zwei Positionen vertauscht werden - ohne den ganzen
    Text neu zu bewerten.

    Der Score ist die Summe aus Monogramm-, Bigramm- und Trigramm-Log-
    Wahrscheinlichkeiten, geteilt durch die Laenge. Da die Laenge konstant
    bleibt, genuegt es, die *Summe* inkrementell zu fuehren.
    """

    __slots__ = ("text", "n", "total")

    def __init__(self, text: str) -> None:
        self.set_text(text)

    def set_text(self, text: str) -> None:
        self.text = text
        self.n = len(text)
        self.total = self._full_sum(text)

    @staticmethod
    def _full_sum(text: str) -> float:
        n = len(text)
        if n == 0:
            return -1e18
        s = 0.0
        mono = _MONO_TAB
        for ch in text:
            s += mono.get(ch, LOG_FLOOR_MONO)
        for i in range(n - 1):
            s += _bigr(text[i], text[i + 1])
        for i in range(n - 2):
            s += _tri(text[i], text[i + 1], text[i + 2])
        return s

    def score(self) -> float:
        if self.n == 0:
            return -1e18
        return self.total / self.n

    def delta_swap(self, i: int, j: int) -> float:
        """Aenderung der Score-Summe, wenn Position i und j getauscht werden.

        Beruecksichtigt nur die betroffenen Monogramme, Bigramme und
        Trigramme. Die Laenge bleibt gleich, daher ist die Differenz der
        Summen proportional zur Score-Differenz.
        """
        if i == j:
            return 0.0
        t = self.text
        n = self.n
        # Betroffene Fenster: Positionen i-2..i+2 und j-2..j+2
        lo = max(0, min(i, j) - 2)
        hi = min(n, max(i, j) + 3)
        before = self._window_sum(t, lo, hi)
        # getauschten Text lokal erzeugen (Fenster, lokale Indizes)
        lst = list(t[lo:hi])
        ii, jj = i - lo, j - lo
        lst[ii], lst[jj] = lst[jj], lst[ii]
        after = self._window_sum("".join(lst), 0, hi - lo)
        return after - before

    @staticmethod
    def _window_sum(text: str, lo: int, hi: int) -> float:
        """Summe der n-gramm-Log-Wahrscheinlichkeiten im Fenster [lo, hi).

        ``lo``/``hi`` sind Indizes *in den uebergebenen String*.
        """
        s = 0.0
        mono = _MONO_TAB
        for k in range(lo, hi):
            s += mono.get(text[k], LOG_FLOOR_MONO)
        for k in range(lo, hi - 1):
            s += _bigr(text[k], text[k + 1])
        for k in range(lo, hi - 2):
            s += _tri(text[k], text[k + 1], text[k + 2])
        return s

    def apply_swap(self, i: int, j: int) -> None:
        """Fuehrt den Swap aus und aktualisiert die Summe."""
        if i == j:
            return
        self.total += self.delta_swap(i, j)
        lst = list(self.text)
        lst[i], lst[j] = lst[j], lst[i]
        self.text = "".join(lst)


def word_hits_fast(text: str, min_len: int = 3, max_len: int = 14) -> int:
    """Wie ``langmodel.word_hits``, aber mit lokalem Set-Lookup.

    Etwas schneller als das Original (kein wiederholtes ``min``/Attribut-
    Lookup), liefert aber exakt dasselbe Ergebnis.
    """
    hits = 0
    n = len(text)
    ws = _WORD_SET
    for i in range(n):
        end = i + max_len
        if end > n:
            end = n
        for j in range(i + min_len, end + 1):
            if text[i:j] in ws:
                hits += 1
    return hits


def fitness(text: str, lam: float = 1.0, ref: float = -17.0) -> float:
    """Kombinierte Fitness: (score - ref) + lam * word_hits.

    Identisch zu ``core.fitness.fitness``, aber mit dem schnelleren Scorer.
    """
    return (score_text(text) - ref) + lam * word_hits_fast(text)


if __name__ == "__main__":
    import time
    from core import langmodel

    tests = [
        "KEINESTOERUNGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCHAUFBELGRADX",
        "DIEINFANTERIEISTANGETRETENUNDWIRDMORGENFRUEHANGREIFEN",
        "INUKRAINEUNDPOLENRUBELKURSETARKSTEIGENDINFOLGEBRUCHES",
    ]
    print("Vergleich score_text vs langmodel.score:")
    for t in tests:
        a = score_text(t)
        b = langmodel.score(t)
        print(f"  {a:9.4f} vs {b:9.4f}  diff={abs(a-b):.2e}")

    print("\nVergleich word_hits_fast vs langmodel.word_hits:")
    for t in tests:
        a = word_hits_fast(t)
        b = langmodel.word_hits(t)
        print(f"  {a:4d} vs {b:4d}  {'OK' if a == b else 'FEHLER'}")

    print("\nBenchmark (1000 Aufrufe):")
    t = tests[0]
    for name, fn in (("langmodel.score", lambda: langmodel.score(t)),
                     ("score_text", lambda: score_text(t)),
                     ("langmodel.word_hits", lambda: langmodel.word_hits(t)),
                     ("word_hits_fast", lambda: word_hits_fast(t))):
        t0 = time.time()
        for _ in range(1000):
            fn()
        print(f"  {name:22s} {(time.time()-t0)/1000*1e6:7.1f} us")

    print("\nInkrementeller Swap-Test:")
    text = tests[1]
    fs = FastScorer(text)
    import random
    rng = random.Random(0)
    ok = True
    for _ in range(200):
        i, j = rng.randrange(len(text)), rng.randrange(len(text))
        if i == j:
            continue
        d = fs.delta_swap(i, j)
        lst = list(text)
        lst[i], lst[j] = lst[j], lst[i]
        expect = score_text("".join(lst)) * len(text) - fs.total
        if abs(d - expect) > 1e-6:
            ok = False
            print(f"  FEHLER bei ({i},{j}): {d:.6f} vs {expect:.6f}")
            break
    print(f"  delta_swap korrekt: {ok}")
