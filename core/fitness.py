#!/usr/bin/env python3
"""
Gemeinsame Fitness-Funktion fuer alle ADFGVX-Solver.

Warum diese Datei existiert
---------------------------
Die Solver im Projekt benutzten bisher unterschiedliche Fitness-Masse:

  * nur `langmodel.score`  -> Overfitting. Der Solver verbiegt Quadrat und
    Permutation so, dass sie das Sprachmodell taeuschen. Der Text sieht dann
    "gut" aus (Score besser als echter deutscher Text), enthaelt aber keine
    echten Woerter. Genau das passierte bei Seite 152.
  * nur `langmodel.word_hits` -> Plateaus. Die Suche bleibt stehen, weil
    viele verschiedene Texte dieselbe Trefferzahl haben.

Die Loesung ist eine gewichtete Kombination beider Signale. Das
Sprachmodell liefert den glatten Gradienten, die Worttreffer den ehrlichen
Beleg. Zusaetzlich wird der Score auf einen Referenzwert normiert, damit
die Gewichte unabhaengig von der Textlaenge funktionieren.
"""

from __future__ import annotations

from core import langmodel

# Referenz-Score eines echten deutschen Militaertextes (empirisch gemessen).
# Siehe docs/HANDBUCH.md, Abschnitt 4.
REF_SCORE = -17.0

# Standardgewicht der Worttreffer. Empirisch bestimmt (siehe Sweep in der
# Commit-Historie): Bei lam=1.0 trennt die Fitness echten Text (35-40),
# Overfit-Text (30) und Rauschen (-2) am besten.
DEFAULT_LAMBDA = 1.0


def fitness(text: str, lam: float = DEFAULT_LAMBDA) -> float:
    """Gewichtete Fitness: Sprachmodell + Worttreffer.

    Hoeher ist besser. Der Score wird um REF_SCORE verschoben, damit beide
    Terme in derselben Groessenordnung liegen.
    """
    if not text:
        return -1e18
    sc = langmodel.score(text)
    wh = langmodel.word_hits(text)
    return (sc - REF_SCORE) + lam * wh


def fitness_parts(text: str) -> tuple[float, int, float]:
    """Gibt (score, word_hits, fitness) zurueck - fuer Diagnose und Logs."""
    sc = langmodel.score(text)
    wh = langmodel.word_hits(text)
    return sc, wh, (sc - REF_SCORE) + DEFAULT_LAMBDA * wh


def is_readable(text: str, min_score: float = -24.0,
                min_hits: int = 15) -> bool:
    """Ehrlicher Lesbarkeits-Test.

    Ein Text gilt nur dann als lesbar, wenn BEIDE Bedingungen erfuellt sind:
    der Score liegt im Bereich echter deutscher Texte UND es gibt genug
    Worttreffer. Der Score allein reicht nicht (Overfitting-Gefahr).
    """
    sc = langmodel.score(text)
    wh = langmodel.word_hits(text)
    return sc >= min_score and wh >= min_hits


if __name__ == "__main__":
    tests = [
        ("ECHTER TEXT", "DERANGRIFFBEGINNTBEIDENANHOEHENBEIMORGENGRAUEN"),
        ("GELOEST 171", "INUKRAINEUNDPOLENRUBELKURSETARKSTEIGENDINFOLGEBRUCHES"),
        ("OVERFIT 152", "FSEMEIMITSATZENKGEBERNEUNDWOLESELTORETUNENUNNISCHREU"),
        ("RAUSCHEN", "XBKAUMMPCRUDAAD1VHLTEELEICJCBLBEFLELFKWZ7P0KVURTNKZBRNN"),
    ]
    print(f"{'Text':<14} {'score':>8} {'hits':>5} {'fitness':>9}  lesbar?")
    print("-" * 55)
    for name, t in tests:
        sc, wh, fit = fitness_parts(t)
        print(f"{name:<14} {sc:>8.3f} {wh:>5d} {fit:>9.3f}  "
              f"{'ja' if is_readable(t) else 'nein'}")
