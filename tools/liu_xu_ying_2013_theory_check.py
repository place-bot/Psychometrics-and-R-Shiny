#!/usr/bin/env python3
"""Computational checks for Liu, Xu, and Ying (2013).

The article proves consistency of self-learning Q-matrix estimators through
saturated response moments, full-rank T-matrices, and column-space separation.
It does not report simulations or release source code.  This independent
teaching implementation checks the paper's finite-dimensional identities and
illustrates recovery in one small enumerated example.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from scipy.optimize import minimize


Array = np.ndarray


TRUE_Q = np.array(
    [
        [1, 0],
        [0, 1],
        [1, 1],
        [1, 1],
    ],
    dtype=int,
)

TRUE_P = np.array([0.10, 0.20, 0.30, 0.40])
TRUE_C = np.array([0.85, 0.82, 0.90, 0.88])
TRUE_G = np.array([0.15, 0.18, 0.10, 0.12])


@dataclass(frozen=True)
class FitResult:
    loss: float
    p: Array
    success: bool


def attribute_profiles(k: int) -> Array:
    """Return profiles in lexicographic order: 00, 01, 10, 11, ... ."""
    return np.array(list(itertools.product([0, 1], repeat=k)), dtype=int)


def item_subsets(m: int, include_empty: bool = False) -> list[tuple[int, ...]]:
    """Return subsets ordered by size and then lexicographically."""
    result: list[tuple[int, ...]] = [()] if include_empty else []
    for order in range(1, m + 1):
        result.extend(itertools.combinations(range(m), order))
    return result


def ideal_response(q: Array, profiles: Array) -> Array:
    """Return xi[i, a], the capability indicator for item i and profile a."""
    q = np.asarray(q, dtype=int)
    profiles = np.asarray(profiles, dtype=int)
    return np.all(profiles[None, :, :] >= q[:, None, :], axis=2).astype(float)


def item_response_probabilities(
    q: Array,
    c: Array,
    g: Array,
    profiles: Array,
) -> Array:
    """Return P(R_i=1 | A=a) for every item and attribute profile."""
    xi = ideal_response(q, profiles)
    c = np.asarray(c, dtype=float)[:, None]
    g = np.asarray(g, dtype=float)[:, None]
    return g + (c - g) * xi


def t_matrix_full(
    q: Array,
    c: Array,
    g: Array,
    *,
    include_empty: bool = False,
) -> tuple[Array, list[tuple[int, ...]], Array]:
    """Build the noisy T-matrix with all 2^k profile columns.

    The paper writes the zero-profile contribution separately as p_0 g.  Keeping
    all columns gives the equivalent augmented matrix used in Proposition 6.6.
    """
    q = np.asarray(q, dtype=int)
    profiles = attribute_profiles(q.shape[1])
    probabilities = item_response_probabilities(q, c, g, profiles)
    subsets = item_subsets(q.shape[0], include_empty=include_empty)
    rows = []
    for subset in subsets:
        if len(subset) == 0:
            rows.append(np.ones(profiles.shape[0]))
        else:
            rows.append(np.prod(probabilities[list(subset), :], axis=0))
    return np.vstack(rows), subsets, profiles


def deterministic_t_nonzero(q: Array) -> tuple[Array, list[tuple[int, ...]], Array]:
    """Build the paper's saturated T(Q), excluding the zero profile."""
    q = np.asarray(q, dtype=int)
    m, k = q.shape
    profiles = attribute_profiles(k)[1:]
    xi = ideal_response(q, profiles)
    subsets = item_subsets(m)
    rows = [np.prod(xi[list(subset), :], axis=0) for subset in subsets]
    return np.vstack(rows), subsets, profiles


def empirical_moments(
    responses: Array,
    subsets: Sequence[Sequence[int]],
) -> Array:
    """Compute the alpha-vector of joint positive-response proportions."""
    responses = np.asarray(responses, dtype=float)
    return np.array(
        [np.mean(np.prod(responses[:, list(subset)], axis=1)) for subset in subsets]
    )


def fit_simplex(t_matrix: Array, target: Array) -> FitResult:
    """Profile out the attribute distribution on the probability simplex."""
    t_matrix = np.asarray(t_matrix, dtype=float)
    target = np.asarray(target, dtype=float)
    n_profiles = t_matrix.shape[1]

    def objective(p: Array) -> float:
        residual = t_matrix @ p - target
        return 0.5 * float(residual @ residual)

    def gradient(p: Array) -> Array:
        return t_matrix.T @ (t_matrix @ p - target)

    result = minimize(
        objective,
        np.full(n_profiles, 1.0 / n_profiles),
        jac=gradient,
        method="SLSQP",
        bounds=[(0.0, 1.0)] * n_profiles,
        constraints={
            "type": "eq",
            "fun": lambda p: float(np.sum(p) - 1.0),
            "jac": lambda p: np.ones_like(p),
        },
        options={"ftol": 1e-12, "maxiter": 500},
    )
    residual = float(np.linalg.norm(t_matrix @ result.x - target))
    return FitResult(loss=residual, p=result.x, success=bool(result.success))


def candidate_q_matrices(m: int, k: int) -> Iterable[Array]:
    """Enumerate Q-matrices whose rows require at least one attribute."""
    nonzero_rows = attribute_profiles(k)[1:]
    for rows in itertools.product(nonzero_rows, repeat=m):
        yield np.asarray(rows, dtype=int)


def canonical_q(q: Array) -> tuple[int, ...]:
    """Canonicalize Q under all attribute-column permutations."""
    q = np.asarray(q, dtype=int)
    return min(
        tuple(q[:, permutation].ravel())
        for permutation in itertools.permutations(range(q.shape[1]))
    )


def guessing_removal_matrix(
    g: Array,
    subsets: Sequence[tuple[int, ...]],
) -> Array:
    """Construct the inclusion-exclusion row transform D from Proposition 6.6.

    Input moments are ordered as the empty-set moment followed by the nonempty
    subsets.  Each output row is E[prod_i(R_i-g_i)] for one nonempty subset.
    """
    g = np.asarray(g, dtype=float)
    all_subsets = [()] + list(subsets)
    subset_index = {subset: index for index, subset in enumerate(all_subsets)}
    d_matrix = np.zeros((len(subsets), len(all_subsets)))

    for row, subset in enumerate(subsets):
        subset_set = set(subset)
        for order in range(len(subset) + 1):
            for chosen in itertools.combinations(subset, order):
                missing = tuple(sorted(subset_set.difference(chosen)))
                coefficient = (-1.0) ** len(missing)
                if missing:
                    coefficient *= float(np.prod(g[list(missing)]))
                d_matrix[row, subset_index[tuple(chosen)]] = coefficient
    return d_matrix


def sample_dina(
    rng: np.random.Generator,
    n: int,
    q: Array,
    p: Array,
    c: Array,
    g: Array,
) -> Array:
    profiles = attribute_profiles(q.shape[1])
    profile_index = rng.choice(len(profiles), size=n, p=p)
    probability = item_response_probabilities(q, c, g, profiles)
    return (rng.random((n, q.shape[0])) < probability[:, profile_index].T).astype(int)


def structural_checks() -> None:
    deterministic_t, subsets, _ = deterministic_t_nonzero(TRUE_Q)
    rank = int(np.linalg.matrix_rank(deterministic_t))

    noisy_augmented, augmented_subsets, _ = t_matrix_full(
        TRUE_Q,
        TRUE_C,
        TRUE_G,
        include_empty=True,
    )
    d_matrix = guessing_removal_matrix(TRUE_G, augmented_subsets[1:])
    transformed = d_matrix @ noisy_augmented

    zero = np.zeros_like(TRUE_G)
    c_minus_g = TRUE_C - TRUE_G
    centered, _, _ = t_matrix_full(TRUE_Q, c_minus_g, zero)
    expected = np.column_stack([np.zeros(centered.shape[0]), centered[:, 1:]])
    transform_error = float(np.max(np.abs(transformed - expected)))

    permuted = TRUE_Q[:, ::-1]
    original_t, _, _ = t_matrix_full(TRUE_Q, TRUE_C, TRUE_G)
    permuted_t, _, _ = t_matrix_full(permuted, TRUE_C, TRUE_G)
    permutation_error = float(np.max(np.abs(original_t - permuted_t[:, [0, 2, 1, 3]])))

    print("STRUCTURAL CHECKS")
    print(f"saturated deterministic T shape: {deterministic_t.shape}")
    print(f"rank(T): {rank} (target {2 ** TRUE_Q.shape[1] - 1})")
    print(f"number of nonempty item subsets: {len(subsets)}")
    print(f"rank(augmented noisy T): {np.linalg.matrix_rank(noisy_augmented)}")
    print(f"max error in D*T_cg = (0,T_(c-g)): {transform_error:.3e}")
    print(f"column-permutation identity error: {permutation_error:.3e}")


def population_separation() -> None:
    true_t, subsets, _ = t_matrix_full(TRUE_Q, TRUE_C, TRUE_G)
    target = true_t @ TRUE_P
    true_class = canonical_q(TRUE_Q)
    results: list[tuple[float, bool, Array]] = []

    for candidate in candidate_q_matrices(*TRUE_Q.shape):
        candidate_t, _, _ = t_matrix_full(candidate, TRUE_C, TRUE_G)
        fit = fit_simplex(candidate_t, target)
        results.append((fit.loss, canonical_q(candidate) == true_class, candidate))

    equivalent = [value for value in results if value[1]]
    inequivalent = [value for value in results if not value[1]]
    best_wrong = min(inequivalent, key=lambda value: value[0])
    zero_loss = sum(value[0] < 1e-7 for value in results)

    print("POPULATION SEPARATION")
    print(f"candidate matrices: {len(results)}")
    print(f"matrices in the true column-permutation class: {len(equivalent)}")
    print(f"candidates with numerical zero loss: {zero_loss}")
    print(f"best inequivalent loss: {best_wrong[0]:.6f}")
    print("best inequivalent Q:")
    print(best_wrong[2])
    print(f"target moments: {len(subsets)} saturated joint probabilities")


def positivity_counterexample() -> None:
    deterministic_c = np.ones(TRUE_Q.shape[0])
    deterministic_g = np.zeros(TRUE_Q.shape[0])
    all_master = np.array([0.0, 0.0, 0.0, 1.0])
    true_t, _, _ = t_matrix_full(TRUE_Q, deterministic_c, deterministic_g)
    target = true_t @ all_master
    matching = 0
    total = 0

    for candidate in candidate_q_matrices(*TRUE_Q.shape):
        candidate_t, _, _ = t_matrix_full(candidate, deterministic_c, deterministic_g)
        fit = fit_simplex(candidate_t, target)
        total += 1
        matching += int(fit.loss < 1e-7)

    print("C4 COUNTEREXAMPLE")
    print("population distribution: all mass on attribute profile 11")
    print(f"candidate matrices reproducing the moments: {matching}/{total}")
    print("every nonempty item-set moment equals 1")


def finite_sample_check(seed: int, replicates: int) -> None:
    rng = np.random.default_rng(seed)
    candidates = list(candidate_q_matrices(*TRUE_Q.shape))
    candidate_t = [t_matrix_full(q, TRUE_C, TRUE_G)[0] for q in candidates]
    subsets = t_matrix_full(TRUE_Q, TRUE_C, TRUE_G)[1]
    true_class = canonical_q(TRUE_Q)
    sample_sizes = [100, 500, 2000]

    print("FINITE-SAMPLE ILLUSTRATION")
    print(f"seed: {seed}; replicates per N: {replicates}")
    for n in sample_sizes:
        recovered = 0
        losses = []
        for _ in range(replicates):
            responses = sample_dina(rng, n, TRUE_Q, TRUE_P, TRUE_C, TRUE_G)
            alpha = empirical_moments(responses, subsets)
            fitted = [fit_simplex(t_matrix, alpha).loss for t_matrix in candidate_t]
            winner = candidates[int(np.argmin(fitted))]
            recovered += int(canonical_q(winner) == true_class)
            losses.append(float(np.min(fitted)))
        rate = recovered / replicates
        print(
            f"N={n:4d}: class recovery={recovered}/{replicates} "
            f"({rate:.1%}), mean winning loss={np.mean(losses):.5f}"
        )
    print("These numbers are a teaching illustration, not results from the article.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("all", "structural", "separation", "counterexample", "finite"),
        default="all",
    )
    parser.add_argument("--seed", type=int, default=20260726)
    parser.add_argument("--replicates", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.mode in ("all", "structural"):
        structural_checks()
    if args.mode in ("all", "separation"):
        population_separation()
    if args.mode in ("all", "counterexample"):
        positivity_counterexample()
    if args.mode in ("all", "finite"):
        finite_sample_check(args.seed, args.replicates)


if __name__ == "__main__":
    main()
