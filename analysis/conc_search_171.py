#!/usr/bin/env python3
"""Permutationssuche ueber Bigramm-Konzentration (quadratfrei).

Die Konzentration sum(count^2) ist bei der wahren Permutation 1933,
bei Zufall ~1155. Sie ist ein starkes Signal, aber die wahre Permutation
ist ein isoliertes lokales Optimum. Daher: SA mit grossen Mutationen
(Block-Reverse, Rotation, mehrere Swaps) und vielen Restarts.
"""
from __future__ import annotations

import os as _os, sys as _sys, random
from collections import Counter
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from bootstrap import setup
setup()

from core.adfgvx import untranspose, substitute
from core.fitness import fitness
from solvers.analytic_solver import build_case_171


def concentration(ct: str, perm: list[int]) -> int:
    u = untranspose(ct, perm)
    c = Counter(u[i:i + 2] for i in range(0, len(u) - 1, 2))
    return sum(v * v for v in c.values())


def mutate(order: list[int], rng: random.Random) -> list[int]:
    o = order[:]
    n = len(o)
    kind = rng.random()
    if kind < 0.5:
        i, j = rng.sample(range(n), 2)
        o[i], o[j] = o[j], o[i]
    elif kind < 0.75:
        i, j = sorted(rng.sample(range(n), 2))
        o[i:j + 1] = reversed(o[i:j + 1])
    else:
        k = rng.randint(2, 4)
        idx = rng.sample(range(n), k)
        vals = [o[i] for i in idx]
        rng.shuffle(vals)
        for i, v in zip(idx, vals):
            o[i] = v
    return o


def main() -> None:
    ct, perm_true, sq_true, pt_true = build_case_171()
    n = 20
    true_order = sorted(range(n), key=lambda c: perm_true[c])
    print(f"wahre order: {true_order}")
    print(f"Konzentration wahr: {concentration(ct, true_order)}")
    rng = random.Random(12345)
    best_order = None
    best_c = -1
    for restart in range(200):
        order = rng.sample(range(n), n)
        cur = concentration(ct, order)
        T = 300.0
        for it in range(4000):
            T = max(1.0, T * 0.999)
            cand = mutate(order, rng)
            c = concentration(ct, cand)
            if c > cur or rng.random() < pow(2.718, (c - cur) / T):
                order = cand
                cur = c
            if cur > best_c:
                best_c = cur
                best_order = order[:]
        if restart % 20 == 0:
            print(f"  restart {restart:3d}: best_c={best_c}")
    print(f"\nBEST Konzentration: {best_c}")
    print(f"  order: {best_order}")
    match = sum(1 for a, b in zip(best_order, true_order) if a == b)
    print(f"  Positionen korrekt: {match}/{n}")
    pt = substitute(untranspose(ct, best_order), sq_true)
    print(f"  fitness: {fitness(pt):.2f}")
    print(f"  pt: {pt[:60]}")


if __name__ == "__main__":
    main()
