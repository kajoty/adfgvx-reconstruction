#!/usr/bin/env python3
"""
Gemeinsame Basis fuer alle ADFGVX-Solver.

Warum diese Datei existiert
---------------------------
Die Solver im Projekt liefen "nie durch": Sie hatten feste, viel zu hohe
Iterationszahlen (z.B. blind_solver: 4 Restarts x 60000 Iterationen x 4
Perioden = 960000 Bewertungen, jede ~500 us -> 8 Minuten pro Periode).
Ohne Zeitbudget und ohne Konvergenz-Abbruch liefen sie entweder ewig oder
wurden vom Nutzer abgebrochen.

Diese Basis stellt bereit:

* ``Budget`` - Zeit- und Iterationsbudget mit ``should_stop()``.
* ``SolverResult`` - einheitliches Ergebnisobjekt (perm, square, pt, score,
  hits, fitness, geloest?).
* ``evaluate`` - eine Bewertung eines Kandidaten (Perm + Quadrat).
* ``check_solution`` - prueft einen Kandidaten gegen eine bekannte Loesung.
* ``run_cli`` - einheitliche Kommandozeile fuer alle Solver.

Alle Solver sollen diese Basis benutzen, damit sie:
  1. in vernuenftiger Zeit durchlaufen (Zeitbudget),
  2. bei Stillstand aufhoeren (Konvergenz),
  3. ein einheitliches Ergebnis liefern (vergleichbar),
  4. sich gegen bekannte Seiten testen lassen (Regression).
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass, field

from core.adfgvx import ALPHA, FULL, clean, substitute, untranspose
from core.fitness import fitness as _fitness, fitness_parts, is_readable
from core import langmodel


# --------------------------------------------------------------------------
# Ergebnis
# --------------------------------------------------------------------------
@dataclass
class SolverResult:
    """Einheitliches Ergebnis eines Solver-Laufs."""

    name: str
    page: str | None = None
    n: int = 0
    perm: list[int] = field(default_factory=list)
    square: str = ""
    plaintext: str = ""
    score: float = -1e18
    hits: int = 0
    fitness: float = -1e18
    seconds: float = 0.0
    iterations: int = 0
    solved: bool = False
    note: str = ""

    def summary(self) -> str:
        flag = "GELOEST" if self.solved else "nicht geloest"
        head = f"[{self.name}] {flag}"
        if self.page:
            head += f" Seite {self.page}"
        if self.n:
            head += f" n={self.n}"
        return (
            f"{head}\n"
            f"  score={self.score:8.3f}  hits={self.hits:4d}  "
            f"fitness={self.fitness:8.3f}\n"
            f"  Zeit={self.seconds:6.1f}s  Iterationen={self.iterations}\n"
            f"  Klartext: {self.plaintext[:70]}"
            + (f"\n  Hinweis: {self.note}" if self.note else "")
        )


# --------------------------------------------------------------------------
# Budget
# --------------------------------------------------------------------------
class Budget:
    """Zeit- und Iterationsbudget.

    ``should_stop()`` wird in der SA-Schleife aufgerufen. Es liefert True,
    sobald das Zeitbudget erschoepft ist oder die maximale Iterationszahl
    erreicht wurde. Zusaetzlich kann ein Konvergenz-Kriterium gesetzt
    werden: Wenn sich der beste Wert seit ``patience`` Iterationen nicht
    verbessert hat, wird abgebrochen.
    """

    __slots__ = ("t0", "max_seconds", "max_iters", "iters", "patience",
                 "_best", "_last_improve")

    def __init__(self, max_seconds: float = 60.0, max_iters: int = 10**9,
                 patience: int = 0) -> None:
        self.t0 = time.time()
        self.max_seconds = max_seconds
        self.max_iters = max_iters
        self.iters = 0
        self.patience = patience
        self._best = -1e18
        self._last_improve = 0

    def tick(self, value: float | None = None) -> None:
        self.iters += 1
        if value is not None and value > self._best:
            self._best = value
            self._last_improve = self.iters

    def should_stop(self) -> bool:
        if self.iters >= self.max_iters:
            return True
        if time.time() - self.t0 >= self.max_seconds:
            return True
        if self.patience and (self.iters - self._last_improve) >= self.patience:
            return True
        return False

    @property
    def elapsed(self) -> float:
        return time.time() - self.t0


# --------------------------------------------------------------------------
# Bewertung
# --------------------------------------------------------------------------
def evaluate(ct: str, perm: list[int], square: str) -> tuple[float, int, float, str]:
    """Bewertet einen Kandidaten.

    Rueckgabe: (score, word_hits, fitness, klartext)
    """
    inter = untranspose(ct, perm)
    pt = substitute(inter, square)
    sc, wh, fit = fitness_parts(pt)
    return sc, wh, fit, pt


def check_solution(perm: list[int], square: str, pt: str,
                   perm_true: list[int], sq_true: str,
                   pt_true: str) -> tuple[bool, str]:
    """Prueft einen Kandidaten gegen eine bekannte Loesung.

    Rueckgabe: (geloest?, Beschreibung)
    """
    pt_ok = pt == pt_true
    sq_ok = square == sq_true
    perm_ok = perm == perm_true
    if pt_ok:
        return True, "Klartext exakt"
    parts = []
    if perm_ok:
        parts.append("Permutation korrekt")
    if sq_ok:
        parts.append("Quadrat korrekt")
    if not parts:
        # Teilfortschritt melden
        n = len(perm_true)
        same = sum(1 for a, b in zip(perm, perm_true) if a == b)
        parts.append(f"Perm {same}/{n} Positionen")
    return False, ", ".join(parts)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def build_parser(name: str, default_page: str | None = None) -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=f"ADFGVX-Solver: {name}")
    ap.add_argument("--page", default=default_page,
                    help="Seite aus dem Korpus (z.B. 105, 171)")
    ap.add_argument("--n", type=int, default=0,
                    help="Spaltenzahl (0 = aus dem Schluessel ableiten)")
    ap.add_argument("--seconds", type=float, default=60.0,
                    help="Zeitbudget in Sekunden (Standard 60)")
    ap.add_argument("--restarts", type=int, default=0,
                    help="Anzahl Neustarts (0 = Standard des Solvers)")
    ap.add_argument("--seed", type=int, default=1, help="Zufallsseed")
    ap.add_argument("--quick", action="store_true",
                    help="Kurzer Lauf (10 s) fuer schnelle Tests")
    ap.add_argument("--verbose", action="store_true", help="Zwischenstaende")
    return ap


def resolve_case(page: str | None, n: int):
    """Loest eine Seite in (ct, perm_true, sq_true, pt_true, n) auf.

    Nutzt die verifizierten Daten aus ``data.corpus_corrected``. Ist die
    Seite dort nicht enthalten, wird ``data.corpus``/``data.solutions``
    verwendet.
    """
    from data.solutions import SOLVED
    from core.adfgvx import KEYS

    if page is None:
        page = "171"

    # Bevorzugt: verifizierte Korrektur
    try:
        from data.corpus_corrected import corrected_ct
        ct = corrected_ct(page)
    except Exception:
        from data.corpus import CORPUS
        ct = clean(CORPUS[page])

    key_name = SOLVED[page][0]
    perm_true = list(KEYS[key_name][0])
    sq_true = KEYS[key_name][1]
    pt_true = SOLVED[page][1]
    if n <= 0:
        n = len(perm_true)
    return ct, perm_true, sq_true, pt_true, n


def run_cli(name: str, solve_fn, default_page: str | None = None) -> None:
    """Einheitlicher CLI-Einstieg fuer alle Solver.

    ``solve_fn(ct, n, seconds, restarts, seed, verbose)`` muss ein
    ``SolverResult`` liefern.
    """
    ap = build_parser(name, default_page)
    args = ap.parse_args()
    seconds = 10.0 if args.quick else args.seconds

    ct, perm_true, sq_true, pt_true, n = resolve_case(args.page, args.n)
    print(f"Seite {args.page or '171'}: {len(ct)} Zeichen, n={n}, "
          f"Zeitbudget {seconds:.0f}s")

    res = solve_fn(ct, n, seconds=seconds, restarts=args.restarts,
                   seed=args.seed, verbose=args.verbose)
    res.page = args.page or "171"
    res.n = n

    solved, why = check_solution(res.perm, res.square, res.plaintext,
                                 perm_true, sq_true, pt_true)
    res.solved = solved
    res.note = why
    print()
    print(res.summary())
    print()
    print(f"Erwartet: {pt_true[:70]}")


if __name__ == "__main__":
    # Selbsttest: Budget und Ergebnisobjekt
    b = Budget(max_seconds=0.05)
    while not b.should_stop():
        b.tick(1.0)
    print(f"Budget-Test: {b.iters} Iterationen in {b.elapsed:.3f}s")

    r = SolverResult(name="test", page="171", n=20, score=-17.2, hits=123,
                     fitness=122.8, plaintext="INUKRAINEUNDPOLEN")
    print(r.summary())
