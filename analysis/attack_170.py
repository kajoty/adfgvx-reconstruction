#!/usr/bin/env python3
"""Reproduzierbarer Angriff auf Seite 170 (RICHI-240).

Seite 170 hat ein bekanntes Transpositionsschluesselwort, aber das
Substitutionsquadrat Nov10-12 enthaelt noch ``-``-Luecken. Dieses Skript
behauptet daher keine Loesung. Es misst nur, ob die beobachtete Anomalie
durch wenige Zeichenkorrekturen erklaert werden kann.

Getestet werden:
  * unveraenderter Korpus-Score,
  * alle Ein-Zeichen-Substitutionen im transponierten Geheimtext,
  * gezielte Ersetzungen der ersten Koordinate eines Bigramms,
  * eine Shuffle-/Zufalls-Baseline gleicher Laenge.

Aufruf:
    PYTHONPATH=. python3 analysis/attack_170.py --samples 10000
"""

from __future__ import annotations

import argparse
import itertools
import os as _os
import random
import sys as _sys
from dataclasses import dataclass

_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup

setup()

from core.adfgvx import ALPHA, KEYS, clean, make_square, substitute, untranspose
from core.fitness import fitness_parts
from data.corpus import CORPUS


@dataclass(frozen=True)
class Candidate:
    fitness: float
    score: float
    hits: int
    operation: str
    text: str


def measure(text: str, operation: str) -> Candidate:
    score, hits, fit = fitness_parts(text)
    return Candidate(fit, score, hits, operation, text)


def top_insert(candidates: list[Candidate], candidate: Candidate, limit: int = 10):
    candidates.append(candidate)
    candidates.sort(key=lambda item: item.fitness, reverse=True)
    del candidates[limit:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=10000,
                        help="Anzahl der Zufallsproben (default: 10000)")
    parser.add_argument("--seed", type=int, default=170,
                        help="Seed fuer reproduzierbare Baselines")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    ct = clean(CORPUS["170"])
    perm, subkey, _ = KEYS["Nov10-12"]
    square = make_square(subkey)
    bgs = untranspose(ct, perm)

    baseline_text = substitute(bgs, square)
    baseline = measure(baseline_text, "original")
    one_ct: list[Candidate] = []
    one_coord: list[Candidate] = []
    two_coord: list[Candidate] = []

    # Jede einzelne Korrektur im beobachteten/transponierten Geheimtext.
    for pos, old in enumerate(ct):
        for new in ALPHA:
            if new == old:
                continue
            repaired = ct[:pos] + new + ct[pos + 1:]
            text = substitute(untranspose(repaired, perm), square)
            top_insert(one_ct, measure(text, f"ct[{pos}] {old}->{new}"))

    # Die Analyse vermutet Fehler in Koordinate 1 der Bigramme. Hier werden
    # diese Positionen direkt im Zwischenstrom einzeln korrigiert.
    for pair in range(len(bgs) // 2):
        pos = pair * 2
        old = bgs[pos]
        for new in ALPHA:
            if new == old:
                continue
            repaired = bgs[:pos] + new + bgs[pos + 1:]
            text = substitute(repaired, square)
            top_insert(one_coord, measure(text, f"bg[{pair}].1 {old}->{new}"))

    # Zwei Korrekturen in Koordinate 1. Das ist noch vollstaendig
    # enumerierbar (53*52/2 * 5*5 Kandidaten) und vermeidet einen
    # voreingenommenen Hill-Climb.
    for pair_a, pair_b in itertools.combinations(range(len(bgs) // 2), 2):
        pos_a, pos_b = pair_a * 2, pair_b * 2
        for new_a in ALPHA:
            if new_a == bgs[pos_a]:
                continue
            for new_b in ALPHA:
                if new_b == bgs[pos_b]:
                    continue
                repaired = list(bgs)
                repaired[pos_a] = new_a
                repaired[pos_b] = new_b
                text = substitute("".join(repaired), square)
                top_insert(two_coord, measure(
                    text, f"bg[{pair_a}].1 {bgs[pos_a]}->{new_a}, "
                    f"bg[{pair_b}].1 {bgs[pos_b]}->{new_b}"))

    # Nullmodell 1: gleiche Buchstabenhaeufigkeit, aber zufaellige Reihenfolge.
    shuffled: list[float] = []
    chars = list(ct)
    for _ in range(args.samples):
        rng.shuffle(chars)
        shuffled.append(measure(substitute(untranspose("".join(chars), perm), square), "shuffle").fitness)

    # Nullmodell 2: gleichverteiltes ADFGVX-Chiffrat gleicher Laenge.
    random_scores: list[float] = []
    for _ in range(args.samples):
        random_ct = "".join(rng.choice(ALPHA) for _ in range(len(ct)))
        random_scores.append(measure(substitute(untranspose(random_ct, perm), square), "random").fitness)

    def percentile(value: float, values: list[float]) -> float:
        return 100.0 * sum(item <= value for item in values) / len(values)

    print("SEITE 170 — SYSTEMATISCHER EIN-ZEICHEN-ANGRIFF")
    print(f"Laenge: {len(ct)} CT-Zeichen / {len(ct) // 2} Bigramme")
    print(f"Schluessel: Nov10-12; Quadrat: {len(subkey)} Zeichen, Luecken werden aufgefuellt")
    print(f"Baseline: score={baseline.score:.3f} hits={baseline.hits} fitness={baseline.fitness:.3f}")
    print()
    print("Beste CT-Substitutionen:")
    for item in one_ct[:10]:
        print(f"  {item.fitness:8.3f} score={item.score:7.3f} hits={item.hits:2d} {item.operation:18s} {item.text}")
    print()
    print("Beste Korrekturen an Bigramm-Koordinate 1:")
    for item in one_coord[:10]:
        print(f"  {item.fitness:8.3f} score={item.score:7.3f} hits={item.hits:2d} {item.operation:18s} {item.text}")
    print()
    print("Beste ZWEI Korrekturen an Bigramm-Koordinate 1:")
    for item in two_coord[:10]:
        print(f"  {item.fitness:8.3f} score={item.score:7.3f} hits={item.hits:2d} {item.operation:32s} {item.text}")
    print()
    print("Zufalls-Baselines:")
    print(f"  Shuffle: mean={sum(shuffled)/len(shuffled):.3f} max={max(shuffled):.3f} "
          f"original percentile={percentile(baseline.fitness, shuffled):.1f}%")
    print(f"  Uniform: mean={sum(random_scores)/len(random_scores):.3f} max={max(random_scores):.3f} "
          f"original percentile={percentile(baseline.fitness, random_scores):.1f}%")
    print()
    print("Interpretation: Ein Kandidat ist erst interessant, wenn er die Baseline")
    print("deutlich uebertrifft und zugleich einen stabilen Worttreffer-/Score-Gewinn zeigt.")


if __name__ == "__main__":
    main()