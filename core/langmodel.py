#!/usr/bin/env python3
"""
Sprachmodell fuer deutsche Klartexte, aufgebaut aus einer echten
Worthaeufigkeitsliste (de_50k.txt, hermitdave/FrequencyWords).

Erzeugt:
  - MONO:  Monogrammhaeufigkeit (aus den Woertern gewichtet)
  - BIGR:  Bigrammhaeufigkeit
  - TRI:   Trigrammhaeufigkeit
  - WORDS: Menge der bekannten Woerter (fuer Worttreffer-Bonus)

Wird als Modul von den Loesern importiert.
"""

from __future__ import annotations

import math
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
# Die Worthaeufigkeitsliste liegt im Datenordner (../data/de_50k.txt).
FREQ_FILE = os.path.join(os.path.dirname(HERE), "data", "de_50k.txt")


def _load_words() -> list[tuple[str, float]]:
    words: list[tuple[str, float]] = []
    with open(FREQ_FILE, encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if len(parts) != 2:
                continue
            w, c = parts[0].upper(), float(parts[1])
            if not w.isalpha():
                continue
            words.append((w, c))
    return words


_WORDS = _load_words()
_WORD_SET = {w for w, _ in _WORDS}

# --- Monogramme -----------------------------------------------------------
_mono = Counter()
for w, c in _WORDS:
    for ch in w:
        _mono[ch] += c
_total = sum(_mono.values())
MONO = {ch: cnt / _total for ch, cnt in _mono.items()}

# --- Bigramme / Trigramme -------------------------------------------------
_big = Counter()
_tri = Counter()
for w, c in _WORDS:
    padded = "^" + w + "$"
    for i in range(len(padded) - 1):
        _big[padded[i:i + 2]] += c
    for i in range(len(padded) - 2):
        _tri[padded[i:i + 3]] += c

_big_total = sum(_big.values())
_tri_total = sum(_tri.values())
BIGR = {bg: cnt / _big_total for bg, cnt in _big.items()}
TRI = {tg: cnt / _tri_total for tg, cnt in _tri.items()}

# Logarithmen vorberechnen (mit Untergrenze fuer unbekannte n-gramme)
FLOOR = 1e-7
LOG_MONO = {ch: math.log(max(p, FLOOR)) for ch, p in MONO.items()}
LOG_BIGR = {bg: math.log(max(p, FLOOR)) for bg, p in BIGR.items()}
LOG_TRI = {tg: math.log(max(p, FLOOR)) for tg, p in TRI.items()}
LOG_FLOOR_MONO = math.log(FLOOR)
LOG_FLOOR_BIGR = math.log(FLOOR)
LOG_FLOOR_TRI = math.log(FLOOR)


def score(text: str, w_mono: float = 1.0, w_bigr: float = 1.0,
          w_tri: float = 1.0) -> float:
    """Log-Likelihood-Fitness eines Klartextkandidaten (hoeher = besser)."""
    if not text:
        return -1e18
    s = 0.0
    for ch in text:
        s += w_mono * LOG_MONO.get(ch, LOG_FLOOR_MONO)
    for i in range(len(text) - 1):
        s += w_bigr * LOG_BIGR.get(text[i:i + 2], LOG_FLOOR_BIGR)
    for i in range(len(text) - 2):
        s += w_tri * LOG_TRI.get(text[i:i + 3], LOG_FLOOR_TRI)
    return s / len(text)


def word_hits(text: str, min_len: int = 3) -> int:
    """Zaehlt, wie viele zusammenhaengende Buchstabenfolgen echte Woerter sind."""
    hits = 0
    n = len(text)
    for i in range(n):
        for j in range(i + min_len, min(n, i + 14) + 1):
            if text[i:j] in _WORD_SET:
                hits += 1
    return hits


if __name__ == "__main__":
    print(f"Woerter: {len(_WORDS)}")
    print(f"Monogramme: {len(MONO)}, Bigramme: {len(BIGR)}, Trigramme: {len(TRI)}")
    print()
    tests = [
        ("ECHTER KLARTEXT", "KEINESTOERUNGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCHAUFBELGRADX"),
        ("DEUTSCH", "DIEINFANTERIEISTANGETRETENUNDWIRDMORGENFRUEHANGREIFEN"),
        ("DEUTSCH2", "ARTILLERIEFEUERLIEGTAUFDEMHOHENWEGNORDLICHDERSTRASSE"),
    ]
    import random
    import string
    random.seed(1)
    for name, t in tests:
        print(f"{name:16s} score={score(t):8.3f}  words={word_hits(t):3d}  {t[:50]}")
    print()
    for _ in range(5):
        rnd = "".join(random.choice(string.ascii_uppercase) for _ in range(60))
        print(f"{'ZUFALL':16s} score={score(rnd):8.3f}  words={word_hits(rnd):3d}  {rnd[:50]}")
