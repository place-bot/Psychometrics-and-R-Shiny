#!/usr/bin/env python3
"""Transparent teaching implementation for Liu, Xu, and Ying (2012).

The paper learns a DINA Q-matrix by comparing empirical positive-response
moments beta with the moments T(Q, c, g) p implied by a candidate Q-matrix.
For each candidate Q, nuisance parameters are fitted by DINA EM, and a
row-wise hill-climbing search updates one item at a time.

This script is an independent implementation.  The article did not publish
source code, a software version, or random seeds.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
from typing import Sequence

import numpy as np


Array = np.ndarray


Q1 = np.array(
    [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1],
    ],
    dtype=int,
)

Q2 = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [1, 1, 0, 0],
        [1, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
        [1, 1, 1, 0],
        [1, 1, 0, 1],
        [1, 0, 1, 1],
        [0, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
    ],
    dtype=int,
)

Q3 = np.array(
    [
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 0, 1],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 0, 1, 1],
    ],
    dtype=int,
)


PAPER_TABLE_1 = {
    "Q1": {500: 94, 1000: 100, 2000: 100, 4000: 100},
    "Q2": {500: 82, 1000: 100, 2000: 100, 4000: 100},
    "Q3": {500: 38, 1000: 98, 2000: 100, 4000: 100},
}

PAPER_TABLE_2 = {"Q2": {500: 94}, "Q3": {500: 70}}

PAPER_TABLE_3 = {
    0.05: {1000: 78, 2000: 98, 4000: 100},
    0.15: {1000: 71, 2000: 94, 4000: 99},
    0.25: {1000: 41, 2000: 76, 4000: 95},
}


@dataclass(frozen=True)
class DinaFit:
    c: Array
    g: Array
    p: Array
    log_likelihood: float
    iterations: int
    converged: bool


@dataclass(frozen=True)
class SearchStep:
    iteration: int
    item: int
    objective_before: float
    objective_after: float
    relative_drop: float
    accepted: bool


def attribute_profiles(k: int) -> Array:
    """Profiles ordered as binary integers: 00, 01, 10, 11, ... ."""
    return np.array(list(itertools.product([0, 1], repeat=k)), dtype=int)


def ideal_response(q: Array, profiles: Array) -> Array:
    """Return eta[j, a] = 1 when profile a covers every 1 in q-row j."""
    q = np.asarray(q, dtype=int)
    profiles = np.asarray(profiles, dtype=int)
    return np.all(profiles[None, :, :] >= q[:, None, :], axis=2).astype(float)


def response_probabilities(q: Array, c: Array, g: Array, profiles: Array) -> Array:
    """Return P(R_j=1 | alpha) as a J by 2^K matrix."""
    eta = ideal_response(q, profiles)
    c = np.asarray(c, dtype=float)[:, None]
    g = np.asarray(g, dtype=float)[:, None]
    return g + (c - g) * eta


def item_subsets(
    j: int,
    max_order: int,
    max_rows: int | None = None,
) -> list[tuple[int, ...]]:
    """Build 1-way, then 2-way, ... item combinations in lexicographic order."""
    subsets: list[tuple[int, ...]] = []
    for order in range(1, min(j, max_order) + 1):
        for subset in itertools.combinations(range(j), order):
            subsets.append(subset)
            if max_rows is not None and len(subsets) >= max_rows:
                return subsets
    return subsets


def t_matrix(
    q: Array,
    c: Array,
    g: Array,
    profiles: Array,
    subsets: Sequence[Sequence[int]],
) -> Array:
    """Stack B-vectors; each row is an elementwise product over selected items."""
    item_prob = response_probabilities(q, c, g, profiles)
    return np.vstack([np.prod(item_prob[list(s), :], axis=0) for s in subsets])


def empirical_beta(y: Array, subsets: Sequence[Sequence[int]]) -> Array:
    """Observed proportions answering every item in each subset correctly."""
    y = np.asarray(y, dtype=float)
    return np.array([np.mean(np.prod(y[:, list(s)], axis=1)) for s in subsets])


def implied_beta(t: Array, p: Array) -> Array:
    return np.asarray(t, dtype=float) @ np.asarray(p, dtype=float)


def s_objective(t: Array, p: Array, beta: Array) -> float:
    """Equation (14): Euclidean distance ||T p - beta||_2."""
    return float(np.linalg.norm(implied_beta(t, p) - beta))


def _logsumexp(x: Array, axis: int) -> Array:
    maximum = np.max(x, axis=axis, keepdims=True)
    return np.squeeze(maximum + np.log(np.sum(np.exp(x - maximum), axis=axis, keepdims=True)), axis)


def fit_dina_em(
    y: Array,
    q: Array,
    *,
    max_iter: int = 500,
    tol: float = 1e-8,
    clip: float = 1e-6,
) -> DinaFit:
    """Marginal-maximum-likelihood DINA fit for fixed Q."""
    y = np.asarray(y, dtype=float)
    q = np.asarray(q, dtype=int)
    n, j = y.shape
    if q.shape[0] != j:
        raise ValueError("Q rows must equal the number of response columns")
    profiles = attribute_profiles(q.shape[1])
    eta = ideal_response(q, profiles)
    m = profiles.shape[0]

    p = np.full(m, 1.0 / m)
    g = np.clip(np.mean(y, axis=0) * 0.45, 0.05, 0.35)
    c = np.clip(0.55 + np.mean(y, axis=0) * 0.40, 0.65, 0.95)
    previous = -np.inf
    converged = False

    for iteration in range(1, max_iter + 1):
        prob = np.clip(g[:, None] + (c[:, None] - g[:, None]) * eta, clip, 1.0 - clip)
        log_conditional = y @ np.log(prob) + (1.0 - y) @ np.log(1.0 - prob)
        log_joint = log_conditional + np.log(np.clip(p, clip, 1.0))[None, :]
        log_marginal = _logsumexp(log_joint, axis=1)
        log_likelihood = float(np.sum(log_marginal))
        posterior = np.exp(log_joint - log_marginal[:, None])

        p_new = np.clip(np.mean(posterior, axis=0), clip, None)
        p_new /= np.sum(p_new)
        expected_positive = y.T @ posterior
        expected_total = np.sum(posterior, axis=0)[None, :]

        master_num = np.sum(expected_positive * eta, axis=1)
        master_den = np.sum(expected_total * eta, axis=1)
        nonmaster_num = np.sum(expected_positive * (1.0 - eta), axis=1)
        nonmaster_den = np.sum(expected_total * (1.0 - eta), axis=1)

        c_new = np.divide(master_num, master_den, out=c.copy(), where=master_den > clip)
        g_new = np.divide(nonmaster_num, nonmaster_den, out=g.copy(), where=nonmaster_den > clip)
        c_new = np.clip(c_new, clip, 1.0 - clip)
        g_new = np.clip(g_new, clip, 1.0 - clip)

        p, c, g = p_new, c_new, g_new
        if abs(log_likelihood - previous) < tol:
            converged = True
            break
        previous = log_likelihood

    return DinaFit(
        c=c,
        g=g,
        p=p,
        log_likelihood=log_likelihood,
        iterations=iteration,
        converged=converged,
    )


def profiled_objective(
    y: Array,
    q: Array,
    subsets: Sequence[Sequence[int]],
    *,
    max_em_iter: int = 500,
) -> tuple[float, DinaFit]:
    """Equation (17): fit nuisance parameters, then evaluate the S-distance."""
    fit = fit_dina_em(y, q, max_iter=max_em_iter)
    profiles = attribute_profiles(q.shape[1])
    t = t_matrix(q, fit.c, fit.g, profiles, subsets)
    return s_objective(t, fit.p, empirical_beta(y, subsets)), fit


def row_patterns(k: int, include_zero: bool = True) -> Array:
    patterns = attribute_profiles(k)
    return patterns if include_zero else patterns[1:]


def hill_climb_q(
    y: Array,
    q0: Array,
    subsets: Sequence[Sequence[int]],
    *,
    early_stop: float | None = None,
    include_zero: bool = True,
    max_search_iter: int = 50,
    max_em_iter: int = 300,
) -> tuple[Array, list[SearchStep]]:
    """Algorithm 1: best whole-row update among every item neighborhood."""
    current = np.asarray(q0, dtype=int).copy()
    patterns = row_patterns(current.shape[1], include_zero=include_zero)
    current_s, _ = profiled_objective(y, current, subsets, max_em_iter=max_em_iter)
    history: list[SearchStep] = []

    for iteration in range(1, max_search_iter + 1):
        best_s = current_s
        best_item = -1
        best_q = current.copy()
        for item in range(current.shape[0]):
            for pattern in patterns:
                if np.array_equal(pattern, current[item]):
                    continue
                candidate = current.copy()
                candidate[item] = pattern
                value, _ = profiled_objective(y, candidate, subsets, max_em_iter=max_em_iter)
                if value < best_s - 1e-12:
                    best_s, best_item, best_q = value, item, candidate

        relative_drop = (current_s - best_s) / max(current_s, 1e-15)
        accepted = best_item >= 0
        if early_stop is not None and relative_drop < early_stop:
            accepted = False
        history.append(
            SearchStep(
                iteration=iteration,
                item=best_item,
                objective_before=current_s,
                objective_after=best_s,
                relative_drop=relative_drop,
                accepted=accepted,
            )
        )
        if not accepted:
            break
        current, current_s = best_q, best_s
    return current, history


def simulate_dina(
    q: Array,
    n: int,
    *,
    c: float | Array = 0.8,
    g: float | Array = 0.2,
    p: Array | None = None,
    seed: int = 20260725,
) -> tuple[Array, Array]:
    """Simulate profiles and responses under DINA."""
    rng = np.random.default_rng(seed)
    q = np.asarray(q, dtype=int)
    j, k = q.shape
    profiles = attribute_profiles(k)
    if p is None:
        p = np.full(2**k, 1.0 / (2**k))
    c_array = np.broadcast_to(np.asarray(c, dtype=float), (j,))
    g_array = np.broadcast_to(np.asarray(g, dtype=float), (j,))
    profile_index = rng.choice(2**k, size=n, p=p)
    selected_profiles = profiles[profile_index]
    eta = ideal_response(q, selected_profiles).T
    probability = g_array[None, :] + (c_array - g_array)[None, :] * eta
    return selected_profiles, rng.binomial(1, probability)


def toy_t_matrix_demo() -> None:
    """Reproduce Equations (8)--(13) with the paper's displayed profile order."""
    profiles = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=int)
    q = np.array([[1, 0], [0, 1], [1, 1]], dtype=int)
    q_prime = np.array([[1, 0], [0, 1], [1, 0]], dtype=int)
    subsets_3 = [(0,), (1,), (2,)]
    subsets_4 = subsets_3 + [(0, 1)]
    c = np.ones(3)
    g = np.zeros(3)
    t_q = t_matrix(q, c, g, profiles, subsets_3).astype(int)
    t_prime = t_matrix(q_prime, c, g, profiles, subsets_3).astype(int)
    t_augmented = t_matrix(q, c, g, profiles, subsets_4).astype(int)

    expected_q = np.array([[0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]])
    expected_prime = np.array([[0, 1, 0, 1], [0, 0, 1, 1], [0, 1, 0, 1]])
    expected_augmented = np.vstack([expected_q, [0, 0, 0, 1]])
    np.testing.assert_array_equal(t_q, expected_q)
    np.testing.assert_array_equal(t_prime, expected_prime)
    np.testing.assert_array_equal(t_augmented, expected_augmented)

    print("profiles (paper order):")
    print(profiles)
    print("T(Q), Equation (9):")
    print(t_q)
    print("T(Q'), Equation (10):")
    print(t_prime)
    print("T(Q) with item-pair row, Equation (13):")
    print(t_augmented)


def paper_table_checks() -> None:
    for table in (PAPER_TABLE_1, PAPER_TABLE_2):
        for row in table.values():
            for recovered in row.values():
                if not 0 <= recovered <= 100:
                    raise AssertionError("paper recovery count must be between 0 and 100")
    for row in PAPER_TABLE_3.values():
        for recovered in row.values():
            if not 0 <= recovered <= 100:
                raise AssertionError("paper recovery count must be between 0 and 100")
    print("published table counts loaded and range-checked")
    print("Table 1:", PAPER_TABLE_1)
    print("Table 2:", PAPER_TABLE_2)
    print("Table 3:", PAPER_TABLE_3)
    print("editorial discrepancy: Table 1 reports Q1/N=500 as 94; prose reports 98")


def simulation_demo(n: int, seed: int) -> None:
    """Small transparent run; it is not a reproduction of the 100-replication tables."""
    q_true = np.array(
        [[1, 0], [0, 1], [1, 1], [1, 0], [0, 1], [1, 1]],
        dtype=int,
    )
    _, y = simulate_dina(q_true, n, seed=seed)
    q0 = q_true.copy()
    q0[5] = [1, 0]
    subsets = item_subsets(q_true.shape[0], max_order=3, max_rows=max(20, n // 10))
    estimated, history = hill_climb_q(
        y,
        q0,
        subsets,
        include_zero=False,
        early_stop=None,
        max_search_iter=4,
        max_em_iter=250,
    )
    print("true Q:")
    print(q_true)
    print("starting Q:")
    print(q0)
    for step in history:
        print(
            f"iteration={step.iteration} item={step.item + 1 if step.item >= 0 else '-'} "
            f"S={step.objective_before:.6f}->{step.objective_after:.6f} "
            f"drop={100 * step.relative_drop:.2f}% accepted={step.accepted}"
        )
    print("estimated Q:")
    print(estimated)
    print("exact recovery:", bool(np.array_equal(estimated, q_true)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("all", "toy", "tables", "simulate"),
        default="all",
    )
    parser.add_argument("--examinees", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260725)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.mode in ("all", "toy"):
        toy_t_matrix_demo()
    if args.mode in ("all", "tables"):
        paper_table_checks()
    if args.mode in ("all", "simulate"):
        simulation_demo(args.examinees, args.seed)


if __name__ == "__main__":
    main()
