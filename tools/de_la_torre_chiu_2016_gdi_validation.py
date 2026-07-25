#!/usr/bin/env python3
"""Transparent GDI/PVAF calculations for de la Torre and Chiu (2016).

The script has two purposes:

1. reproduce the paper's Table 1 example exactly;
2. expose the complete empirical validation pipeline:
   provisional G-DINA fit -> posterior class weights -> nonparametric
   full-class item success probabilities -> exhaustive q-vector search.

The optional simulation follows the main Study 1 design: J=30, K=5,
higher-order attributes, reduced-model response functions, random Q-entry
errors, and a PVAF cutoff of .95. The paper used N=2,000 and 100 replications
per condition. Use ``--paper-scale`` for those settings.

This is an independent teaching implementation. The paper's Ox source was
not published. Applied analyses should use a maintained implementation such
as ``GDINA::Qval()`` and should combine empirical suggestions with expert
review.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np

from de_la_torre_2011_gdina_framework import (
    Q_PAPER,
    attribute_patterns,
    fit_saturated_gdina,
)


@dataclass(frozen=True)
class GDIResult:
    """One candidate q-vector and its GDI/PVAF values."""

    q_vector: tuple[int, ...]
    gdi: float
    pvaf: float


TABLE1_WEIGHTS = np.asarray(
    [
        0.053,
        0.076,
        0.039,
        0.057,
        0.069,
        0.047,
        0.068,
        0.078,
        0.037,
        0.081,
        0.073,
        0.055,
        0.056,
        0.083,
        0.069,
        0.059,
    ],
    dtype=float,
)

TABLE1_PATTERNS = np.asarray(
    [
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 1],
        [1, 0, 1, 1],
        [0, 1, 1, 1],
        [1, 1, 1, 1],
    ],
    dtype=int,
)

TABLE1_PROBABILITIES = np.asarray(
    [
        0.225,
        0.225,
        0.225,
        0.225,
        0.225,
        0.225,
        0.225,
        0.725,
        0.225,
        0.225,
        0.225,
        0.225,
        0.225,
        0.225,
        0.225,
        0.725,
    ],
    dtype=float,
)


def all_nonzero_q_vectors(attribute_count: int) -> list[tuple[int, ...]]:
    """Return all 2^K - 1 candidates, grouped by number of attributes."""

    candidates = [
        tuple(int(value) for value in pattern)
        for pattern in itertools.product((0, 1), repeat=attribute_count)
        if any(pattern)
    ]
    candidates.sort(key=lambda row: (sum(row), tuple(-value for value in row)))
    return candidates


def collapsed_success_profile(
    q_vector: Sequence[int],
    patterns: np.ndarray,
    weights: np.ndarray,
    probabilities: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Collapse full latent classes to the groups induced by a q-vector."""

    required = np.flatnonzero(np.asarray(q_vector, dtype=int))
    if len(required) == 0:
        raise ValueError("the all-zero q-vector is excluded")
    if len(patterns) != len(weights) or len(weights) != len(probabilities):
        raise ValueError("patterns, weights, and probabilities must align")
    if not np.isclose(float(weights.sum()), 1.0, atol=1e-8):
        raise ValueError("class weights must sum to one")

    local_patterns = attribute_patterns(len(required))
    lookup = {
        tuple(pattern.tolist()): index
        for index, pattern in enumerate(local_patterns)
    }
    group = np.asarray(
        [lookup[tuple(pattern[required].tolist())] for pattern in patterns],
        dtype=int,
    )
    group_weight = np.bincount(
        group, weights=weights, minlength=len(local_patterns)
    )
    weighted_success = np.bincount(
        group, weights=weights * probabilities, minlength=len(local_patterns)
    )
    group_probability = np.divide(
        weighted_success,
        group_weight,
        out=np.zeros_like(weighted_success),
        where=group_weight > 0.0,
    )
    return group_weight, group_probability


def gdi(
    q_vector: Sequence[int],
    patterns: np.ndarray,
    weights: np.ndarray,
    probabilities: np.ndarray,
) -> float:
    """Compute equation (10), the weighted between-group variance."""

    group_weight, group_probability = collapsed_success_profile(
        q_vector, patterns, weights, probabilities
    )
    mean_probability = float(np.sum(group_weight * group_probability))
    return float(
        np.sum(group_weight * (group_probability - mean_probability) ** 2)
    )


def exhaustive_search(
    patterns: np.ndarray,
    weights: np.ndarray,
    probabilities: np.ndarray,
    epsilon: float = 0.95,
) -> tuple[GDIResult, list[GDIResult]]:
    """Apply the paper's exhaustive GDI/PVAF and parsimony rule."""

    if not 0.0 <= epsilon <= 1.0:
        raise ValueError("epsilon must be between zero and one")
    candidates = all_nonzero_q_vectors(patterns.shape[1])
    full_q = tuple(1 for _ in range(patterns.shape[1]))
    maximum = gdi(full_q, patterns, weights, probabilities)
    if maximum <= 0.0:
        raise ValueError("the saturated GDI is zero; PVAF is undefined")

    results = [
        GDIResult(
            q_vector=candidate,
            gdi=(value := gdi(candidate, patterns, weights, probabilities)),
            pvaf=value / maximum,
        )
        for candidate in candidates
    ]
    appropriate = [result for result in results if result.pvaf >= epsilon]
    if not appropriate:
        raise RuntimeError("the full q-vector should always pass the cutoff")
    minimum_size = min(sum(result.q_vector) for result in appropriate)
    finalists = [
        result
        for result in appropriate
        if sum(result.q_vector) == minimum_size
    ]
    selected = max(finalists, key=lambda result: result.gdi)
    return selected, results


def estimate_full_class_probabilities(
    responses: np.ndarray,
    posterior: np.ndarray,
    smoothing: float = 1e-10,
) -> np.ndarray:
    """Estimate p_j(alpha) from posterior expected counts.

    This is Liu's (2017) equation (4) and the calculation used by the current
    GDINA implementation. It deliberately does not reuse the item-local
    probability table from the provisional model.
    """

    class_count = posterior.sum(axis=0)
    expected_correct = posterior.T @ responses
    return (expected_correct + smoothing) / (
        class_count[:, None] + 2.0 * smoothing
    )


def higher_order_attributes(
    examinees: int, rng: np.random.Generator
) -> np.ndarray:
    """Generate the paper's five higher-order binary attributes."""

    intercepts = np.asarray([-1.0, -0.5, 0.0, 0.5, 1.0])
    slopes = np.full(5, 1.5)
    theta = rng.normal(size=examinees)
    logits = slopes[None, :] * (theta[:, None] - intercepts[None, :])
    mastery = 1.0 / (1.0 + np.exp(-logits))
    return (rng.random((examinees, 5)) < mastery).astype(int)


def reduced_model_probability(
    local_pattern: np.ndarray,
    model: str,
    p0: float,
    p1: float,
) -> float:
    """Return one of the five Study 1 response functions."""

    mastered = int(local_pattern.sum())
    required = len(local_pattern)
    dina = p1 if mastered == required else p0
    dino = p1 if mastered > 0 else p0
    acdm = p0 + (p1 - p0) * mastered / required

    model_upper = model.upper()
    if model_upper == "DINA":
        return dina
    if model_upper == "DINO":
        return dino
    if model_upper == "ACDM":
        return acdm
    if model_upper == "DINA-ACDM":
        return 0.5 * (dina + acdm)
    if model_upper == "DINO-ACDM":
        return 0.5 * (dino + acdm)
    raise ValueError("unknown Study 1 generating model")


def simulate_study1_responses(
    attributes: np.ndarray,
    q_matrix: np.ndarray,
    model: str,
    p0: float,
    p1: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Simulate responses under one of the paper's five reduced models."""

    responses = np.zeros((len(attributes), len(q_matrix)), dtype=int)
    for item, q_row in enumerate(q_matrix):
        required = np.flatnonzero(q_row)
        local = attributes[:, required]
        probabilities = np.asarray(
            [
                reduced_model_probability(row, model, p0, p1)
                for row in local
            ],
            dtype=float,
        )
        responses[:, item] = (
            rng.random(len(attributes)) < probabilities
        ).astype(int)
    return responses


def randomly_misspecify_q(
    q_matrix: np.ndarray,
    error_count: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Flip random Q entries while retaining nonempty item rows/attributes."""

    if error_count < 1 or error_count >= q_matrix.size:
        raise ValueError("error_count is outside the valid range")
    for _ in range(10_000):
        candidate = q_matrix.copy()
        positions = rng.choice(candidate.size, size=error_count, replace=False)
        flat = candidate.reshape(-1)
        flat[positions] = 1 - flat[positions]
        if np.all(candidate.sum(axis=1) > 0) and np.all(candidate.sum(axis=0) > 0):
            return candidate
    raise RuntimeError("failed to generate a nonempty misspecified Q-matrix")


def q_recovery_summary(
    truth: np.ndarray, provisional: np.ndarray, suggested: np.ndarray
) -> dict[str, float]:
    """Return the four contingency-table rates used in Tables 4 and 5."""

    wrong_entry = provisional != truth
    correct_entry = ~wrong_entry
    wrong_vector = np.any(provisional != truth, axis=1)
    correct_vector = ~wrong_vector

    def percentage(values: np.ndarray) -> float:
        return 100.0 * float(np.mean(values)) if len(values) else float("nan")

    return {
        "entry_wrong_corrected": percentage(
            (suggested == truth)[wrong_entry]
        ),
        "entry_correct_retained": percentage(
            (suggested == truth)[correct_entry]
        ),
        "vector_wrong_corrected": percentage(
            np.all(suggested[wrong_vector] == truth[wrong_vector], axis=1)
        ),
        "vector_correct_retained": percentage(
            np.all(
                suggested[correct_vector] == truth[correct_vector], axis=1
            )
        ),
    }


def validate_one_dataset(
    responses: np.ndarray,
    provisional_q: np.ndarray,
    epsilon: float,
    tolerance: float,
    max_iterations: int,
) -> tuple[np.ndarray, int, bool]:
    """Fit the provisional model and suggest every q-vector."""

    fit, _, _, _ = fit_saturated_gdina(
        data=responses,
        q_matrix=provisional_q,
        tolerance=tolerance,
        max_iterations=max_iterations,
        update_prior=True,
    )
    patterns = attribute_patterns(provisional_q.shape[1])
    class_probabilities = estimate_full_class_probabilities(
        responses, fit.posterior
    )
    suggested = np.zeros_like(provisional_q)
    for item in range(responses.shape[1]):
        selected, _ = exhaustive_search(
            patterns,
            fit.prior,
            class_probabilities[:, item],
            epsilon,
        )
        suggested[item] = np.asarray(selected.q_vector, dtype=int)
    return suggested, fit.iterations, fit.converged


def table1_demo(epsilon: float) -> None:
    """Print the paper's deterministic example and its exhaustive ranking."""

    patterns = TABLE1_PATTERNS
    print("Table 1 deterministic check")
    print("  weight sum =", f"{TABLE1_WEIGHTS.sum():.3f}")

    for label, candidate in (
        ("correct", (1, 1, 1, 0)),
        ("overspecified", (1, 1, 1, 1)),
        ("under+over", (0, 1, 1, 1)),
    ):
        value = gdi(
            candidate, patterns, TABLE1_WEIGHTS, TABLE1_PROBABILITIES
        )
        print(
            "  {0:>13s} q={1} GDI={2:.6f}".format(
                label, "".join(map(str, candidate)), value
            )
        )

    group_weight, group_probability = collapsed_success_profile(
        (1, 1, 1, 0),
        patterns,
        TABLE1_WEIGHTS,
        TABLE1_PROBABILITIES,
    )
    print(
        "  collapsed group 000-: w={0:.3f}, p={1:.3f}".format(
            group_weight[0], group_probability[0]
        )
    )
    print("  note: the printed paper denominator should be 0.053 + 0.037")

    selected, results = exhaustive_search(
        patterns, TABLE1_WEIGHTS, TABLE1_PROBABILITIES, epsilon
    )
    print(
        "  selected at epsilon={0:.3f}: q={1}, GDI={2:.6f}, PVAF={3:.6f}".format(
            epsilon,
            "".join(map(str, selected.q_vector)),
            selected.gdi,
            selected.pvaf,
        )
    )
    print("  best candidate at each size")
    for size in range(1, 5):
        best = max(
            (result for result in results if sum(result.q_vector) == size),
            key=lambda result: result.gdi,
        )
        print(
            "    K*={0}: q={1}, GDI={2:.6f}, PVAF={3:.6f}".format(
                size,
                "".join(map(str, best.q_vector)),
                best.gdi,
                best.pvaf,
            )
        )


def mean_results(rows: Iterable[dict[str, float]]) -> dict[str, float]:
    rows_list = list(rows)
    return {
        key: float(np.mean([row[key] for row in rows_list]))
        for key in rows_list[0]
    }


def run_simulation(args: argparse.Namespace) -> None:
    rng = np.random.default_rng(args.seed)
    examinees = 2000 if args.paper_scale else args.examinees
    replications = 100 if args.paper_scale else args.replications
    results = []
    converged = 0
    iteration_counts = []

    for replication in range(replications):
        attributes = higher_order_attributes(examinees, rng)
        responses = simulate_study1_responses(
            attributes,
            Q_PAPER,
            args.model,
            args.p0,
            args.p1,
            rng,
        )
        errors = 7 if (not args.paper_scale or replication < 50) else 8
        provisional = randomly_misspecify_q(Q_PAPER, errors, rng)
        suggested, iterations, did_converge = validate_one_dataset(
            responses,
            provisional,
            args.epsilon,
            args.tolerance,
            args.max_iterations,
        )
        results.append(q_recovery_summary(Q_PAPER, provisional, suggested))
        converged += int(did_converge)
        iteration_counts.append(iterations)
        print(
            "replication {0:>3d}: errors={1}, EM iterations={2}, converged={3}".format(
                replication + 1, errors, iterations, did_converge
            )
        )

    average = mean_results(results)
    print("\nStudy 1 teaching reproduction")
    print("  model =", args.model)
    print("  N, J, K =", examinees, len(Q_PAPER), Q_PAPER.shape[1])
    print("  p0, p1 =", args.p0, args.p1)
    print("  epsilon =", args.epsilon)
    print("  replications =", replications)
    print("  converged =", f"{converged}/{replications}")
    print("  mean EM iterations =", f"{np.mean(iteration_counts):.1f}")
    print(
        "  misspecified entries corrected =",
        f"{average['entry_wrong_corrected']:.1f}%",
    )
    print(
        "  correct entries retained =",
        f"{average['entry_correct_retained']:.1f}%",
    )
    print(
        "  misspecified q-vectors corrected =",
        f"{average['vector_wrong_corrected']:.1f}%",
    )
    print(
        "  correct q-vectors retained =",
        f"{average['vector_correct_retained']:.1f}%",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reproduce GDI/PVAF Q-matrix validation calculations."
    )
    parser.add_argument(
        "--model",
        choices=("DINA", "DINA-ACDM", "ACDM", "DINO-ACDM", "DINO"),
        default="DINA",
    )
    parser.add_argument("--examinees", type=int, default=1200)
    parser.add_argument("--replications", type=int, default=1)
    parser.add_argument("--p0", type=float, default=0.20)
    parser.add_argument("--p1", type=float, default=0.80)
    parser.add_argument("--epsilon", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=2016)
    parser.add_argument("--tolerance", type=float, default=1e-4)
    parser.add_argument("--max-iterations", type=int, default=500)
    parser.add_argument(
        "--demo-only",
        action="store_true",
        help="run only the exact Table 1 calculation",
    )
    parser.add_argument(
        "--paper-scale",
        action="store_true",
        help="use N=2,000 and 100 replications",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.examinees < 50 or args.replications < 1:
        raise ValueError("examinees must be >= 50 and replications >= 1")
    if not 0.0 < args.p0 < args.p1 < 1.0:
        raise ValueError("require 0 < p0 < p1 < 1")
    table1_demo(args.epsilon)
    if not args.demo_only:
        print()
        run_simulation(args)


if __name__ == "__main__":
    main()
