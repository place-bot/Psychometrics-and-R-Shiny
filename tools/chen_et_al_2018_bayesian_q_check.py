#!/usr/bin/env python3
"""Small exact checks for Chen et al. (2018), Bayesian DINA Q estimation.

This script is an independent teaching implementation.  It does not replace
the authors' Rcpp code.  It checks four claims/implementation details that are
easy to verify exactly at small scale:

1. the three identification restrictions used by the paper;
2. connectedness of the single-entry-flip graph when K=2 and J=6;
3. the paper's Table 1 summaries and method comparisons;
4. entry-wise posterior majority can leave the identified Q space even when
   every sampled Q matrix is identified.
"""

from __future__ import annotations

from collections import deque
from itertools import product

import numpy as np


def is_identified(q: np.ndarray) -> bool:
    """Check the three restrictions in equations (11)--(12).

    For a binary Q matrix, containing two row-permuted copies of I_K is
    equivalent to having at least two copies of every unit row e_k.
    """

    if q.ndim != 2 or not np.isin(q, (0, 1)).all():
        return False
    _, k = q.shape
    nonzero_rows = np.all(q.sum(axis=1) > 0)
    three_items_per_attribute = np.all(q.sum(axis=0) >= 3)
    two_identity_copies = all(
        np.sum(np.all(q == np.eye(k, dtype=int)[attribute], axis=1)) >= 2
        for attribute in range(k)
    )
    return bool(nonzero_rows and three_items_per_attribute and two_identity_copies)


def enumerate_identified_q(j: int = 6, k: int = 2) -> list[np.ndarray]:
    """Enumerate the identified space for the small K=2 example."""

    nonzero_rows = [
        np.asarray(row, dtype=int)
        for row in product((0, 1), repeat=k)
        if any(row)
    ]
    return [
        np.vstack(rows)
        for rows in product(nonzero_rows, repeat=j)
        if is_identified(np.vstack(rows))
    ]


def matrix_key(q: np.ndarray) -> tuple[int, ...]:
    return tuple(int(value) for value in q.ravel())


def one_flip_neighbors(q: np.ndarray, state_keys: set[tuple[int, ...]]) -> list[tuple[int, ...]]:
    """Return all identified states reachable by one binary-entry flip."""

    neighbors: list[tuple[int, ...]] = []
    for row in range(q.shape[0]):
        for column in range(q.shape[1]):
            proposal = q.copy()
            proposal[row, column] = 1 - proposal[row, column]
            key = matrix_key(proposal)
            if key in state_keys:
                neighbors.append(key)
    return neighbors


def connected_component_size(states: list[np.ndarray]) -> int:
    """Breadth-first search on the support graph of the B=1 proposal."""

    state_keys = {matrix_key(q) for q in states}
    shape = states[0].shape
    start = next(iter(state_keys))
    seen = {start}
    queue = deque([start])
    while queue:
        key = queue.popleft()
        q = np.asarray(key, dtype=int).reshape(shape)
        for neighbor in one_flip_neighbors(q, state_keys):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen)


# Columns are K, N, rho, MH whole-Q recovery, CGibbs whole-Q recovery,
# Gibbs whole-Q recovery, followed by the three entry-wise percentages.
TABLE_1 = np.asarray(
    [
        (3, 500, 0, 91, 95, 94, 95.89, 98.22, 97.12),
        (3, 1000, 0, 94, 99, 95, 97.59, 99.61, 97.93),
        (3, 2000, 0, 96, 92, 90, 98.52, 97.33, 95.11),
        (3, 4000, 0, 98, 88, 91, 99.56, 96.33, 95.42),
        (3, 500, 0.05, 87, 99, 82, 93.25, 99.63, 92.96),
        (3, 1000, 0.05, 92, 99, 90, 94.67, 99.64, 94.41),
        (3, 2000, 0.05, 93, 95, 90, 97.89, 98.52, 95.18),
        (3, 4000, 0.05, 94, 88, 88, 98.78, 96.33, 95.20),
        (3, 500, 0.15, 93, 99, 91, 97.42, 99.63, 95.44),
        (3, 1000, 0.15, 95, 99, 92, 98.51, 99.67, 95.89),
        (3, 2000, 0.15, 96, 95, 94, 99.29, 98.10, 97.65),
        (3, 4000, 0.15, 95, 91, 89, 99.35, 97.39, 94.04),
        (3, 500, 0.25, 92, 99, 90, 98.70, 99.98, 94.55),
        (3, 1000, 0.25, 96, 98, 94, 99.42, 99.65, 96.20),
        (3, 2000, 0.25, 96, 94, 93, 99.92, 98.10, 95.83),
        (3, 4000, 0.25, 97, 89, 91, 99.88, 95.57, 95.76),
        (4, 500, 0, 60, 97, 59, 91.42, 99.92, 89.81),
        (4, 1000, 0, 67, 91, 67, 93.11, 97.29, 92.24),
        (4, 2000, 0, 76, 79, 73, 94.52, 94.54, 93.96),
        (4, 4000, 0, 87, 51, 82, 95.50, 87.02, 95.25),
        (4, 500, 0.05, 37, 98, 40, 82.00, 99.13, 83.39),
        (4, 1000, 0.05, 52, 94, 58, 88.57, 98.36, 89.87),
        (4, 2000, 0.05, 48, 90, 53, 88.02, 97.44, 89.28),
        (4, 4000, 0.05, 53, 53, 51, 89.50, 89.62, 88.94),
        (4, 500, 0.15, 34, 96, 40, 81.61, 99.43, 83.09),
        (4, 1000, 0.15, 44, 88, 60, 84.87, 96.83, 92.00),
        (4, 2000, 0.15, 55, 90, 53, 89.13, 97.17, 88.97),
        (4, 4000, 0.15, 56, 74, 52, 89.92, 91.64, 89.19),
        (4, 500, 0.25, 35, 97, 37, 81.78, 99.58, 82.94),
        (4, 1000, 0.25, 43, 96, 58, 84.67, 98.57, 90.24),
        (4, 2000, 0.25, 55, 85, 54, 89.87, 95.64, 89.80),
        (4, 4000, 0.25, 55, 79, 51, 90.09, 94.07, 89.30),
    ],
    dtype=float,
)


def table_one_summary() -> None:
    method_names = ("MH", "CGibbs", "Gibbs")
    for k in (3, 4):
        rows = TABLE_1[TABLE_1[:, 0] == k]
        whole_q_means = rows[:, 3:6].mean(axis=0)
        entry_means = rows[:, 6:9].mean(axis=0)
        print(f"K={k} mean whole-Q recovery: " + ", ".join(
            f"{name}={value:.2f}" for name, value in zip(method_names, whole_q_means)
        ))
        print(f"K={k} mean entry accuracy: " + ", ".join(
            f"{name}={value:.2f}" for name, value in zip(method_names, entry_means)
        ))

    k4_dependent = TABLE_1[(TABLE_1[:, 0] == 4) & (TABLE_1[:, 2] > 0)]
    cgibbs_is_best = np.all(
        k4_dependent[:, 4] >= k4_dependent[:, [3, 5]].max(axis=1)
    )
    print(f"CGibbs best/tied on every K=4, rho>0 whole-Q condition: {cgibbs_is_best}")


def entrywise_majority_counterexample(states: list[np.ndarray]) -> None:
    """Display a fixed counterexample relevant to the current edina package."""

    draws = [
        np.asarray(
            [[1, 0], [1, 0], [1, 0], [0, 1], [0, 1], [0, 1]], dtype=int
        ),
        np.asarray(
            [[1, 0], [1, 0], [0, 1], [1, 0], [0, 1], [0, 1]], dtype=int
        ),
        np.asarray(
            [[1, 0], [1, 0], [0, 1], [0, 1], [1, 0], [0, 1]], dtype=int
        ),
    ]
    assert all(is_identified(draw) for draw in draws)
    assert all(matrix_key(draw) in {matrix_key(q) for q in states} for draw in draws)
    majority = (np.mean(draws, axis=0) > 0.5).astype(int)
    print("Every one of three posterior draws is identified:", all(
        is_identified(draw) for draw in draws
    ))
    print("Entry-wise majority matrix:")
    print(majority)
    print("Entry-wise majority is identified:", is_identified(majority))
    print("Column sums of entry-wise majority:", majority.sum(axis=0).tolist())


def main() -> None:
    states = enumerate_identified_q()
    component_size = connected_component_size(states)
    print(f"Identified states for K=2, J=6: {len(states)}")
    print(f"States reached by one-flip graph: {component_size}")
    print(f"One-flip graph connected: {component_size == len(states)}")
    table_one_summary()
    entrywise_majority_counterexample(states)


if __name__ == "__main__":
    main()
