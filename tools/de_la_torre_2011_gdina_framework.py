#!/usr/bin/env python3
"""Teaching implementation of de la Torre's (2011) G-DINA framework.

This script implements the main computational chain in the paper:

1. generate full and item-reduced attribute patterns;
2. simulate A-CDM, DINA, or DINO responses using the paper's Table 1 Q-matrix;
3. estimate a saturated identity-link G-DINA model by EM;
4. transform success probabilities with a saturated design matrix;
5. estimate an observed-information covariance matrix;
6. test the A-CDM restriction item by item with a Wald statistic.

The paper reports 1,000 data sets for each generating model, I=2,000,
J=30, and K=5. It does not state the attribute-pattern distribution in
the simulation section. This script uses a uniform distribution over
the 2^K patterns and labels that choice as a reproduction assumption.

This is a transparent teaching implementation. For applied analysis,
use the maintained GDINA R package:
https://github.com/Wenchao-Ma/GDINA

Dependency: NumPy.
"""

from __future__ import print_function

import argparse
import itertools
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np


Q_PAPER = np.asarray(
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
        [1, 1, 1, 0, 0],
        [1, 1, 0, 1, 0],
        [1, 1, 0, 0, 1],
        [1, 0, 1, 1, 0],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 0, 1],
        [0, 1, 0, 1, 1],
        [0, 0, 1, 1, 1],
    ],
    dtype=int,
)


@dataclass
class FitResult:
    probabilities: List[np.ndarray]
    prior: np.ndarray
    posterior: np.ndarray
    iterations: int
    converged: bool
    log_likelihood: float


def attribute_patterns(k: int) -> np.ndarray:
    """Return patterns in the paper's subset order.

    For k=3 the order is:
    000, 100, 010, 001, 110, 101, 011, 111.
    """

    patterns = list(itertools.product((0, 1), repeat=k))
    patterns.sort(key=lambda row: (sum(row), tuple(-value for value in row)))
    return np.asarray(patterns, dtype=int)


def effect_subsets(k: int) -> List[Tuple[int, ...]]:
    """Return intercept, main-effect, and interaction subsets."""

    subsets: List[Tuple[int, ...]] = [()]
    for size in range(1, k + 1):
        subsets.extend(itertools.combinations(range(k), size))
    return subsets


def design_matrix(k: int, model: str = "GDINA") -> np.ndarray:
    """Construct an item design matrix."""

    model_upper = model.upper()
    patterns = attribute_patterns(k)

    if model_upper == "GDINA":
        subsets = effect_subsets(k)
        matrix = np.ones((len(patterns), len(subsets)), dtype=float)
        for row_index, pattern in enumerate(patterns):
            for column_index, subset in enumerate(subsets[1:], start=1):
                matrix[row_index, column_index] = float(
                    all(pattern[position] == 1 for position in subset)
                )
        return matrix

    if model_upper == "DINA":
        return np.column_stack(
            (np.ones(len(patterns)), np.all(patterns == 1, axis=1).astype(float))
        )

    if model_upper == "DINO":
        return np.column_stack(
            (np.ones(len(patterns)), np.any(patterns == 1, axis=1).astype(float))
        )

    if model_upper in {"ACDM", "LLM", "RRUM"}:
        return np.column_stack((np.ones(len(patterns)), patterns.astype(float)))

    raise ValueError("unknown model: {0}".format(model))


def item_group_maps(
    q_matrix: np.ndarray, full_patterns: np.ndarray
) -> Tuple[List[np.ndarray], List[np.ndarray], List[np.ndarray]]:
    """Map full latent classes to item-specific reduced latent groups."""

    mappings: List[np.ndarray] = []
    memberships: List[np.ndarray] = []
    reduced_patterns: List[np.ndarray] = []

    for q_row in q_matrix:
        required = np.flatnonzero(q_row)
        local_patterns = attribute_patterns(len(required))
        lookup = {
            tuple(pattern.tolist()): index
            for index, pattern in enumerate(local_patterns)
        }
        mapping = np.asarray(
            [lookup[tuple(pattern[required].tolist())] for pattern in full_patterns],
            dtype=int,
        )
        membership = np.zeros((len(full_patterns), len(local_patterns)), dtype=float)
        membership[np.arange(len(full_patterns)), mapping] = 1.0
        mappings.append(mapping)
        memberships.append(membership)
        reduced_patterns.append(local_patterns)

    return mappings, memberships, reduced_patterns


def generating_probabilities(
    q_matrix: np.ndarray, generating_model: str
) -> List[np.ndarray]:
    """Create the paper's 0.20-to-0.80 item probabilities."""

    model = generating_model.upper()
    item_probabilities: List[np.ndarray] = []

    for q_row in q_matrix:
        k_item = int(q_row.sum())
        patterns = attribute_patterns(k_item)
        mastered = patterns.sum(axis=1)

        if model == "ACDM":
            probabilities = 0.20 + (0.60 / k_item) * mastered
        elif model == "DINA":
            probabilities = np.where(mastered == k_item, 0.80, 0.20)
        elif model == "DINO":
            probabilities = np.where(mastered > 0, 0.80, 0.20)
        else:
            raise ValueError("generating model must be ACDM, DINA, or DINO")

        item_probabilities.append(probabilities.astype(float))

    return item_probabilities


def simulate_responses(
    examinees: int,
    q_matrix: np.ndarray,
    generating_model: str,
    rng: np.random.Generator,
) -> Tuple[np.ndarray, np.ndarray]:
    """Simulate uniformly distributed attribute patterns and responses."""

    full_patterns = attribute_patterns(q_matrix.shape[1])
    mappings, _, _ = item_group_maps(q_matrix, full_patterns)
    probabilities = generating_probabilities(q_matrix, generating_model)

    latent_class = rng.integers(0, len(full_patterns), size=examinees)
    data = np.zeros((examinees, len(q_matrix)), dtype=int)

    for item, mapping in enumerate(mappings):
        person_probability = probabilities[item][mapping[latent_class]]
        data[:, item] = (rng.random(examinees) < person_probability).astype(int)

    return data, full_patterns[latent_class]


def initial_probabilities(reduced_patterns: Sequence[np.ndarray]) -> List[np.ndarray]:
    """Create stable, mildly monotone starting probabilities."""

    initial: List[np.ndarray] = []
    for patterns in reduced_patterns:
        k_item = patterns.shape[1]
        values = 0.25 + 0.50 * patterns.sum(axis=1) / k_item
        initial.append(values.astype(float))
    return initial


def e_step(
    data: np.ndarray,
    mappings: Sequence[np.ndarray],
    probabilities: Sequence[np.ndarray],
    prior: np.ndarray,
) -> Tuple[np.ndarray, float]:
    """Compute full-profile posteriors with log-sum-exp stabilization."""

    n_people = data.shape[0]
    log_joint = np.broadcast_to(np.log(prior), (n_people, len(prior))).copy()

    for item, mapping in enumerate(mappings):
        p_by_class = np.clip(probabilities[item][mapping], 1e-8, 1.0 - 1e-8)
        response = data[:, item][:, None]
        log_joint += response * np.log(p_by_class)[None, :]
        log_joint += (1 - response) * np.log1p(-p_by_class)[None, :]

    row_max = log_joint.max(axis=1, keepdims=True)
    exponentiated = np.exp(log_joint - row_max)
    row_sum = exponentiated.sum(axis=1, keepdims=True)
    posterior = exponentiated / row_sum
    log_likelihood = float(np.sum(row_max[:, 0] + np.log(row_sum[:, 0])))
    return posterior, log_likelihood


def fit_saturated_gdina(
    data: np.ndarray,
    q_matrix: np.ndarray,
    tolerance: float = 1e-4,
    max_iterations: int = 500,
    update_prior: bool = True,
) -> Tuple[FitResult, List[np.ndarray], List[np.ndarray], List[np.ndarray]]:
    """Fit saturated identity-link G-DINA by EM."""

    full_patterns = attribute_patterns(q_matrix.shape[1])
    mappings, memberships, reduced_patterns = item_group_maps(
        q_matrix, full_patterns
    )
    probabilities = initial_probabilities(reduced_patterns)
    prior = np.full(len(full_patterns), 1.0 / len(full_patterns), dtype=float)
    converged = False
    log_likelihood = float("-inf")

    for iteration in range(1, max_iterations + 1):
        posterior, log_likelihood = e_step(data, mappings, probabilities, prior)
        new_probabilities: List[np.ndarray] = []

        for item, membership in enumerate(memberships):
            reduced_posterior = posterior @ membership
            expected_total = reduced_posterior.sum(axis=0)
            expected_correct = reduced_posterior.T @ data[:, item]
            values = np.divide(
                expected_correct,
                expected_total,
                out=probabilities[item].copy(),
                where=expected_total > 1e-10,
            )
            new_probabilities.append(np.clip(values, 0.005, 0.995))

        new_prior = posterior.mean(axis=0) if update_prior else prior.copy()
        new_prior = np.clip(new_prior, 1e-12, None)
        new_prior /= new_prior.sum()

        maximum_change = max(
            max(
                float(np.max(np.abs(new - old)))
                for new, old in zip(new_probabilities, probabilities)
            ),
            float(np.max(np.abs(new_prior - prior))),
        )

        probabilities = new_probabilities
        prior = new_prior

        if maximum_change < tolerance:
            converged = True
            break

    posterior, log_likelihood = e_step(data, mappings, probabilities, prior)
    result = FitResult(
        probabilities=probabilities,
        prior=prior,
        posterior=posterior,
        iterations=iteration,
        converged=converged,
        log_likelihood=log_likelihood,
    )
    return result, mappings, memberships, reduced_patterns


def observed_probability_covariance(
    item: int,
    data: np.ndarray,
    fit: FitResult,
    membership: np.ndarray,
) -> np.ndarray:
    """Approximate Var(P_j) from the paper's equations (16)-(17)."""

    probabilities = np.clip(fit.probabilities[item], 1e-7, 1.0 - 1e-7)
    reduced_posterior = fit.posterior @ membership
    residual_scale = (
        data[:, item][:, None] - probabilities[None, :]
    ) / (probabilities * (1.0 - probabilities))[None, :]
    score = reduced_posterior * residual_scale
    information = score.T @ score
    return np.linalg.pinv(information, rcond=1e-10)


def regularized_gamma_q(shape: float, value: float) -> float:
    """Upper regularized incomplete gamma Q(shape, value).

    This Numerical Recipes style implementation avoids a SciPy dependency.
    """

    if value < 0.0 or shape <= 0.0:
        raise ValueError("invalid incomplete-gamma arguments")
    if value == 0.0:
        return 1.0

    log_gamma = math.lgamma(shape)
    epsilon = 3e-14
    tiny = 1e-300
    max_steps = 500

    if value < shape + 1.0:
        term = 1.0 / shape
        total = term
        rising = shape
        for _ in range(max_steps):
            rising += 1.0
            term *= value / rising
            total += term
            if abs(term) < abs(total) * epsilon:
                break
        lower = total * math.exp(-value + shape * math.log(value) - log_gamma)
        return max(0.0, min(1.0, 1.0 - lower))

    b_value = value + 1.0 - shape
    c_value = 1.0 / tiny
    d_value = 1.0 / b_value
    fraction = d_value
    for index in range(1, max_steps + 1):
        coefficient = -index * (index - shape)
        b_value += 2.0
        d_value = coefficient * d_value + b_value
        if abs(d_value) < tiny:
            d_value = tiny
        c_value = b_value + coefficient / c_value
        if abs(c_value) < tiny:
            c_value = tiny
        d_value = 1.0 / d_value
        change = d_value * c_value
        fraction *= change
        if abs(change - 1.0) < epsilon:
            break

    upper = math.exp(-value + shape * math.log(value) - log_gamma) * fraction
    return max(0.0, min(1.0, upper))


def chi_square_survival(statistic: float, degrees_freedom: int) -> float:
    """Return P(Chi-square_df >= statistic)."""

    if degrees_freedom <= 0:
        raise ValueError("degrees of freedom must be positive")
    return regularized_gamma_q(degrees_freedom / 2.0, statistic / 2.0)


def wald_acdm(
    item: int,
    q_matrix: np.ndarray,
    data: np.ndarray,
    fit: FitResult,
    membership: np.ndarray,
) -> Tuple[float, int, float]:
    """Test zero identity-link interaction effects for one item."""

    k_item = int(q_matrix[item].sum())
    if k_item <= 1:
        raise ValueError("A-CDM and saturated models coincide for one-attribute items")

    saturated_design = design_matrix(k_item, "GDINA")
    transformation = np.linalg.inv(saturated_design)
    probability = fit.probabilities[item]
    delta = transformation @ probability
    probability_covariance = observed_probability_covariance(
        item, data, fit, membership
    )
    delta_covariance = (
        transformation @ probability_covariance @ transformation.T
    )

    interaction_start = 1 + k_item
    restrictions = delta[interaction_start:]
    restriction_covariance = delta_covariance[
        interaction_start:, interaction_start:
    ]
    inverse = np.linalg.pinv(restriction_covariance, rcond=1e-10)
    statistic = float(restrictions.T @ inverse @ restrictions)
    degrees_freedom = len(restrictions)
    p_value = chi_square_survival(statistic, degrees_freedom)
    return statistic, degrees_freedom, p_value


def transform_probabilities(
    probabilities: np.ndarray, link: str
) -> np.ndarray:
    """Transform saturated probabilities into effect parameters."""

    k_item = int(round(math.log(len(probabilities), 2)))
    matrix = design_matrix(k_item, "GDINA")
    clipped = np.clip(probabilities, 1e-8, 1.0 - 1e-8)
    link_lower = link.lower()

    if link_lower == "identity":
        transformed = clipped
    elif link_lower == "logit":
        transformed = np.log(clipped / (1.0 - clipped))
    elif link_lower == "log":
        transformed = np.log(clipped)
    else:
        raise ValueError("link must be identity, logit, or log")

    return np.linalg.solve(matrix, transformed)


def weighted_identity_fit(
    probabilities: np.ndarray,
    expected_counts: np.ndarray,
    model: str,
) -> Tuple[np.ndarray, np.ndarray]:
    """Apply the paper's weighted least-squares formula (29)."""

    k_item = int(round(math.log(len(probabilities), 2)))
    matrix = design_matrix(k_item, model)
    weighted_cross_product = matrix.T @ (expected_counts[:, None] * matrix)
    right_hand_side = matrix.T @ (expected_counts * probabilities)
    parameters = np.linalg.solve(weighted_cross_product, right_hand_side)
    return parameters, matrix @ parameters


def algebra_demo() -> None:
    """Print the three-attribute design matrix and a two-attribute example."""

    print("Saturated K*=3 design matrix")
    print(design_matrix(3, "GDINA").astype(int))

    probability = np.asarray([0.20, 0.35, 0.50, 0.80], dtype=float)
    print("\nTwo-attribute saturated probabilities")
    print("pattern order: 00, 10, 01, 11")
    print("P:", np.array2string(probability, precision=4))

    for link in ("identity", "logit", "log"):
        parameters = transform_probabilities(probability, link)
        print(
            "{0:>8s} effects: {1}".format(
                link, np.array2string(parameters, precision=4)
            )
        )

    counts = np.asarray([100.0, 80.0, 60.0, 40.0])
    for model in ("DINA", "DINO", "ACDM"):
        parameters, fitted = weighted_identity_fit(probability, counts, model)
        print(
            "{0:>8s} weighted parameters: {1}; fitted P: {2}".format(
                model,
                np.array2string(parameters, precision=4),
                np.array2string(fitted, precision=4),
            )
        )


def parse_alpha(text: str) -> List[float]:
    values = [float(value.strip()) for value in text.split(",") if value.strip()]
    if not values or any(value <= 0.0 or value >= 1.0 for value in values):
        raise argparse.ArgumentTypeError("alpha values must lie between 0 and 1")
    return values


def summarize_rejections(
    p_values: Dict[int, List[float]], alpha_levels: Sequence[float]
) -> None:
    """Print rejection rates by item attribute count."""

    print("\nA-CDM item-level Wald rejection rates")
    header = "required" + "".join("  alpha={0:<5g}".format(a) for a in alpha_levels)
    print(header)
    for k_item in sorted(p_values):
        values = np.asarray(p_values[k_item], dtype=float)
        rates = [float(np.mean(values < alpha)) for alpha in alpha_levels]
        print(
            "{0:>8d}".format(k_item)
            + "".join("  {0:>11.3f}".format(rate) for rate in rates)
            + "  (tests={0})".format(len(values))
        )


def run_simulation(args: argparse.Namespace) -> None:
    rng = np.random.default_rng(args.seed)
    p_values: Dict[int, List[float]] = {2: [], 3: []}
    iterations: List[int] = []
    converged_count = 0

    for replication in range(1, args.replications + 1):
        data, _ = simulate_responses(
            args.examinees, Q_PAPER, args.model, rng
        )
        fit, _, memberships, _ = fit_saturated_gdina(
            data=data,
            q_matrix=Q_PAPER,
            tolerance=args.tolerance,
            max_iterations=args.max_iterations,
            update_prior=not args.fixed_prior,
        )
        iterations.append(fit.iterations)
        converged_count += int(fit.converged)

        for item, q_row in enumerate(Q_PAPER):
            k_item = int(q_row.sum())
            if k_item <= 1:
                continue
            _, _, p_value = wald_acdm(
                item=item,
                q_matrix=Q_PAPER,
                data=data,
                fit=fit,
                membership=memberships[item],
            )
            p_values[k_item].append(p_value)

        print(
            "replication {0:>4d}: iterations={1:>3d}, "
            "converged={2}, logLik={3:.2f}".format(
                replication,
                fit.iterations,
                fit.converged,
                fit.log_likelihood,
            )
        )

    print("\nDesign")
    print("  generating model =", args.model)
    print("  examinees =", args.examinees)
    print("  items =", len(Q_PAPER))
    print("  attributes =", Q_PAPER.shape[1])
    print("  replications =", args.replications)
    print("  attribute distribution = uniform (reproduction assumption)")
    print("  prior updated in EM =", not args.fixed_prior)
    print("  convergence tolerance =", args.tolerance)
    print(
        "  converged fits = {0}/{1}".format(
            converged_count, args.replications
        )
    )
    print("  mean iterations = {0:.1f}".format(float(np.mean(iterations))))
    summarize_rejections(p_values, args.alpha)

    print("\nPaper benchmark")
    print("  A-CDM true: Type I rejection rates should track alpha.")
    print("  DINA/DINO true: paper reports power 1.0 at .01, .05, and .10.")
    print("  Paper used 1,000 data sets per generating model.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reproduce the main G-DINA/ACDM Wald logic from de la Torre (2011)."
    )
    parser.add_argument(
        "--model",
        choices=("ACDM", "DINA", "DINO"),
        default="ACDM",
        help="data-generating model",
    )
    parser.add_argument("--examinees", type=int, default=2000)
    parser.add_argument(
        "--replications",
        type=int,
        default=3,
        help="paper uses 1000 for each generating model",
    )
    parser.add_argument(
        "--alpha",
        type=parse_alpha,
        default=parse_alpha("0.01,0.05,0.10"),
        help="comma-separated Wald significance levels",
    )
    parser.add_argument("--seed", type=int, default=2011)
    parser.add_argument("--tolerance", type=float, default=1e-4)
    parser.add_argument("--max-iterations", type=int, default=500)
    parser.add_argument(
        "--fixed-prior",
        action="store_true",
        help="keep a uniform attribute prior instead of updating it",
    )
    parser.add_argument(
        "--demo-only",
        action="store_true",
        help="show matrix transformations without fitting simulated data",
    )
    return parser


def validate_arguments(args: argparse.Namespace) -> None:
    if args.examinees <= 0:
        raise ValueError("--examinees must be positive")
    if args.replications <= 0:
        raise ValueError("--replications must be positive")
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")
    if args.max_iterations <= 0:
        raise ValueError("--max-iterations must be positive")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    validate_arguments(args)
    algebra_demo()
    if not args.demo_only:
        print()
        run_simulation(args)


if __name__ == "__main__":
    main()
