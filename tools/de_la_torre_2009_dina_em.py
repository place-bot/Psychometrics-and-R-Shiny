#!/usr/bin/env python3
"""A small, transparent EM implementation for de la Torre (2009).

The program follows the saturated DINA model described in the paper:

* binary attributes and a known Q-matrix;
* a fixed uniform prior over the 2^K attribute patterns by default;
* E-step posterior weights over attribute patterns;
* closed-form M-step updates for guessing and slipping;
* the observed-information approximation in Appendix Equation A15.

It reproduces the paper's simulation design when called with
--examinees 2000 --replications 100. The smaller defaults finish quickly.
This is a teaching implementation, not the original Ox program.
"""

from __future__ import annotations

import argparse
import itertools
import math
import random
from dataclasses import dataclass
from statistics import fmean, stdev
from typing import List, Optional, Sequence, Tuple

Pattern = Tuple[int, ...]
ResponseRow = List[int]
Matrix = List[List[float]]


PAPER_Q_MATRIX: Tuple[Pattern, ...] = (
    (1, 0, 0, 0, 0),
    (0, 1, 0, 0, 0),
    (0, 0, 1, 0, 0),
    (0, 0, 0, 1, 0),
    (0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0),
    (0, 1, 0, 0, 0),
    (0, 0, 1, 0, 0),
    (0, 0, 0, 1, 0),
    (0, 0, 0, 0, 1),
    (1, 1, 0, 0, 0),
    (1, 0, 1, 0, 0),
    (1, 0, 0, 1, 0),
    (1, 0, 0, 0, 1),
    (0, 1, 1, 0, 0),
    (0, 1, 0, 1, 0),
    (0, 1, 0, 0, 1),
    (0, 0, 1, 1, 0),
    (0, 0, 1, 0, 1),
    (0, 0, 0, 1, 1),
    (1, 1, 1, 0, 0),
    (1, 1, 0, 1, 0),
    (1, 1, 0, 0, 1),
    (1, 0, 1, 1, 0),
    (1, 0, 1, 0, 1),
    (1, 0, 0, 1, 1),
    (0, 1, 1, 1, 0),
    (0, 1, 1, 0, 1),
    (0, 1, 0, 1, 1),
    (0, 0, 1, 1, 1),
)


@dataclass
class EMResult:
    """Values returned by the EM routine."""

    guessing: List[float]
    slipping: List[float]
    priors: List[float]
    posterior: Matrix
    log_likelihood: float
    iterations: int
    converged: bool


def all_attribute_patterns(attribute_count: int) -> List[Pattern]:
    """Enumerate the 2^K binary attribute patterns."""

    if attribute_count < 1:
        raise ValueError("attribute_count must be positive")
    return list(itertools.product((0, 1), repeat=attribute_count))


def validate_q_matrix(q_matrix: Sequence[Sequence[int]]) -> None:
    """Validate a nonempty binary Q-matrix with no all-zero item rows."""

    if not q_matrix or not q_matrix[0]:
        raise ValueError("Q-matrix must be nonempty")
    width = len(q_matrix[0])
    for row in q_matrix:
        if len(row) != width:
            raise ValueError("Q-matrix must be rectangular")
        if any(value not in (0, 1) for value in row):
            raise ValueError("Q-matrix must be binary")
        if sum(row) == 0:
            raise ValueError("each item must require at least one attribute")


def ideal_response(pattern: Sequence[int], q_row: Sequence[int]) -> int:
    """Equation 1: eta is one iff every required attribute is mastered."""

    return int(all(alpha >= required for alpha, required in zip(pattern, q_row)))


def ideal_response_matrix(
    patterns: Sequence[Pattern],
    q_matrix: Sequence[Sequence[int]],
) -> List[List[int]]:
    """Return eta[l][j] for every class and item."""

    return [
        [ideal_response(pattern, q_row) for q_row in q_matrix]
        for pattern in patterns
    ]


def simulate_responses(
    examinee_count: int,
    q_matrix: Sequence[Sequence[int]],
    guessing: Sequence[float],
    slipping: Sequence[float],
    rng: random.Random,
) -> Tuple[List[ResponseRow], List[Pattern]]:
    """Simulate from equiprobable attribute patterns as in the paper."""

    patterns = all_attribute_patterns(len(q_matrix[0]))
    if len(guessing) != len(q_matrix) or len(slipping) != len(q_matrix):
        raise ValueError("one guessing and slipping value is required per item")

    responses: List[ResponseRow] = []
    sampled_patterns: List[Pattern] = []
    for _ in range(examinee_count):
        pattern = patterns[rng.randrange(len(patterns))]
        sampled_patterns.append(pattern)
        row = []
        for q_row, guess, slip in zip(q_matrix, guessing, slipping):
            eta = ideal_response(pattern, q_row)
            probability = 1.0 - slip if eta else guess
            row.append(int(rng.random() < probability))
        responses.append(row)
    return responses, sampled_patterns


def clamp_probability(value: float, epsilon: float = 1e-8) -> float:
    """Keep logarithms and score denominators finite."""

    return min(1.0 - epsilon, max(epsilon, value))


def e_step(
    responses: Sequence[ResponseRow],
    eta: Sequence[Sequence[int]],
    guessing: Sequence[float],
    slipping: Sequence[float],
    priors: Sequence[float],
) -> Tuple[Matrix, float]:
    """Compute posterior class probabilities and the marginal log likelihood."""

    posterior: Matrix = []
    log_likelihood = 0.0

    for response in responses:
        log_weights = []
        for class_index, class_eta in enumerate(eta):
            log_weight = math.log(clamp_probability(priors[class_index]))
            for x, state, guess, slip in zip(
                response,
                class_eta,
                guessing,
                slipping,
            ):
                probability = guess if state == 0 else 1.0 - slip
                probability = clamp_probability(probability)
                log_weight += (
                    math.log(probability)
                    if x
                    else math.log(1.0 - probability)
                )
            log_weights.append(log_weight)

        maximum = max(log_weights)
        scaled = [math.exp(value - maximum) for value in log_weights]
        denominator = sum(scaled)
        posterior.append([value / denominator for value in scaled])
        log_likelihood += maximum + math.log(denominator)

    return posterior, log_likelihood


def m_step(
    responses: Sequence[ResponseRow],
    eta: Sequence[Sequence[int]],
    posterior: Sequence[Sequence[float]],
) -> Tuple[List[float], List[float]]:
    """Appendix A10-A11: update guessing and slipping from expected counts."""

    item_count = len(responses[0])
    expected_state_counts = [[0.0, 0.0] for _ in range(item_count)]
    expected_correct_counts = [[0.0, 0.0] for _ in range(item_count)]

    for response, weights in zip(responses, posterior):
        for class_index, weight in enumerate(weights):
            for item_index, state in enumerate(eta[class_index]):
                expected_state_counts[item_index][state] += weight
                if response[item_index]:
                    expected_correct_counts[item_index][state] += weight

    guessing = []
    slipping = []
    for item_index in range(item_count):
        count_zero, count_one = expected_state_counts[item_index]
        correct_zero, correct_one = expected_correct_counts[item_index]
        guess = correct_zero / count_zero
        slip = (count_one - correct_one) / count_one
        guessing.append(clamp_probability(guess))
        slipping.append(clamp_probability(slip))

    return guessing, slipping


def fit_dina_em(
    responses: Sequence[ResponseRow],
    q_matrix: Sequence[Sequence[int]],
    tolerance: float = 1e-4,
    max_iterations: int = 1000,
    update_prior: bool = False,
) -> EMResult:
    """Fit the saturated DINA model with fixed or empirical priors."""

    validate_q_matrix(q_matrix)
    if not responses or any(len(row) != len(q_matrix) for row in responses):
        raise ValueError("response matrix has incompatible dimensions")
    patterns = all_attribute_patterns(len(q_matrix[0]))
    eta = ideal_response_matrix(patterns, q_matrix)
    class_count = len(patterns)
    item_count = len(q_matrix)

    guessing = [0.25] * item_count
    slipping = [0.25] * item_count
    priors = [1.0 / class_count] * class_count
    posterior: Matrix = []
    log_likelihood = float("-inf")

    for iteration in range(1, max_iterations + 1):
        posterior, log_likelihood = e_step(
            responses,
            eta,
            guessing,
            slipping,
            priors,
        )
        new_guessing, new_slipping = m_step(responses, eta, posterior)
        new_priors = priors
        if update_prior:
            examinee_count = len(responses)
            new_priors = [
                sum(row[class_index] for row in posterior) / examinee_count
                for class_index in range(class_count)
            ]

        maximum_change = max(
            abs(old - new)
            for old, new in zip(
                guessing + slipping + priors,
                new_guessing + new_slipping + new_priors,
            )
        )
        guessing = new_guessing
        slipping = new_slipping
        priors = new_priors

        if maximum_change < tolerance:
            posterior, log_likelihood = e_step(
                responses,
                eta,
                guessing,
                slipping,
                priors,
            )
            return EMResult(
                guessing,
                slipping,
                priors,
                posterior,
                log_likelihood,
                iteration,
                True,
            )

    posterior, log_likelihood = e_step(
        responses,
        eta,
        guessing,
        slipping,
        priors,
    )
    return EMResult(
        guessing,
        slipping,
        priors,
        posterior,
        log_likelihood,
        max_iterations,
        False,
    )


def inverse_matrix(matrix: Matrix) -> Optional[Matrix]:
    """Invert a square matrix with Gauss-Jordan elimination."""

    size = len(matrix)
    augmented = [
        list(row) + [float(row_index == column) for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]

    for column in range(size):
        pivot = max(
            range(column, size),
            key=lambda row_index: abs(augmented[row_index][column]),
        )
        if abs(augmented[pivot][column]) < 1e-12:
            return None
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        pivot_value = augmented[column][column]
        augmented[column] = [
            value / pivot_value for value in augmented[column]
        ]

        for row_index in range(size):
            if row_index == column:
                continue
            factor = augmented[row_index][column]
            if factor == 0.0:
                continue
            augmented[row_index] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(
                    augmented[row_index],
                    augmented[column],
                )
            ]

    return [row[size:] for row in augmented]


def appendix_standard_errors(
    responses: Sequence[ResponseRow],
    q_matrix: Sequence[Sequence[int]],
    result: EMResult,
) -> Optional[Tuple[List[float], List[float]]]:
    """Approximate SEs using the observed information in Equation A15."""

    patterns = all_attribute_patterns(len(q_matrix[0]))
    eta = ideal_response_matrix(patterns, q_matrix)
    item_count = len(q_matrix)
    parameter_count = 2 * item_count
    information = [
        [0.0 for _ in range(parameter_count)]
        for _ in range(parameter_count)
    ]

    for response, weights in zip(responses, result.posterior):
        score = [0.0] * parameter_count
        for item_index in range(item_count):
            posterior_eta_one = sum(
                weight
                for class_eta, weight in zip(eta, weights)
                if class_eta[item_index] == 1
            )
            posterior_eta_zero = 1.0 - posterior_eta_one
            guess = result.guessing[item_index]
            slip = result.slipping[item_index]
            x = response[item_index]

            score[2 * item_index] = (
                posterior_eta_zero
                * (x - guess)
                / (guess * (1.0 - guess))
            )
            score[2 * item_index + 1] = (
                posterior_eta_one
                * ((1.0 - slip) - x)
                / ((1.0 - slip) * slip)
            )

        for row_index in range(parameter_count):
            for column_index in range(row_index, parameter_count):
                value = score[row_index] * score[column_index]
                information[row_index][column_index] += value
                if row_index != column_index:
                    information[column_index][row_index] += value

    covariance = inverse_matrix(information)
    if covariance is None:
        return None
    diagonal = [covariance[index][index] for index in range(parameter_count)]
    if any(value < 0.0 for value in diagonal):
        return None

    guessing_se = [
        math.sqrt(diagonal[2 * item_index])
        for item_index in range(item_count)
    ]
    slipping_se = [
        math.sqrt(diagonal[2 * item_index + 1])
        for item_index in range(item_count)
    ]
    return guessing_se, slipping_se


def summarize_group(
    values: Sequence[Sequence[float]],
    indices: Sequence[int],
) -> float:
    """Average values over replications and selected items."""

    return fmean(
        replication[item_index]
        for replication in values
        for item_index in indices
    )


def empirical_standard_deviation(
    values: Sequence[Sequence[float]],
    indices: Sequence[int],
) -> float:
    """Average itemwise empirical SD over replications."""

    if len(values) < 2:
        return float("nan")
    return fmean(
        stdev(replication[item_index] for replication in values)
        for item_index in indices
    )


def run_simulation(args: argparse.Namespace) -> None:
    """Run a compact version of the paper's simulation study."""

    rng = random.Random(args.seed)
    item_count = len(PAPER_Q_MATRIX)
    true_guessing = [0.20] * item_count
    true_slipping = [0.20] * item_count
    guessing_estimates: List[List[float]] = []
    slipping_estimates: List[List[float]] = []
    guessing_standard_errors: List[List[float]] = []
    slipping_standard_errors: List[List[float]] = []
    iterations = []

    for replication in range(args.replications):
        responses, _ = simulate_responses(
            args.examinees,
            PAPER_Q_MATRIX,
            true_guessing,
            true_slipping,
            rng,
        )
        result = fit_dina_em(
            responses,
            PAPER_Q_MATRIX,
            tolerance=args.tolerance,
            max_iterations=args.max_iterations,
            update_prior=args.update_prior,
        )
        standard_errors = appendix_standard_errors(
            responses,
            PAPER_Q_MATRIX,
            result,
        )
        if standard_errors is None:
            raise RuntimeError("observed information matrix was not invertible")

        guess_se, slip_se = standard_errors
        guessing_estimates.append(result.guessing)
        slipping_estimates.append(result.slipping)
        guessing_standard_errors.append(guess_se)
        slipping_standard_errors.append(slip_se)
        iterations.append(result.iterations)
        print(
            f"replication {replication + 1:>3}: "
            f"iterations={result.iterations:>3}, "
            f"converged={result.converged}, "
            f"logLik={result.log_likelihood:.2f}"
        )

    one_attribute = [index for index, row in enumerate(PAPER_Q_MATRIX) if sum(row) == 1]
    two_attributes = [index for index, row in enumerate(PAPER_Q_MATRIX) if sum(row) == 2]
    three_attributes = [index for index, row in enumerate(PAPER_Q_MATRIX) if sum(row) == 3]

    print("\nDesign")
    print(f"  examinees = {args.examinees}")
    print(f"  items = {item_count}")
    print(f"  attributes = {len(PAPER_Q_MATRIX[0])}")
    print(f"  replications = {args.replications}")
    print(f"  fixed uniform prior = {not args.update_prior}")
    print(f"  convergence tolerance = {args.tolerance}")
    print(f"  mean iterations = {fmean(iterations):.1f}")

    print("\nGrouped recovery summary")
    print(
        "required  mean(g)  mean(s)  mean(SE_g)  mean(SE_s)  "
        "empSD_g  empSD_s"
    )
    for required, indices in (
        (1, one_attribute),
        (2, two_attributes),
        (3, three_attributes),
    ):
        print(
            f"{required:>8}  "
            f"{summarize_group(guessing_estimates, indices):>7.3f}  "
            f"{summarize_group(slipping_estimates, indices):>7.3f}  "
            f"{summarize_group(guessing_standard_errors, indices):>10.3f}  "
            f"{summarize_group(slipping_standard_errors, indices):>10.3f}  "
            f"{empirical_standard_deviation(guessing_estimates, indices):>7.3f}  "
            f"{empirical_standard_deviation(slipping_estimates, indices):>7.3f}"
        )


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--examinees",
        type=int,
        default=500,
        help="number of simulated examinees (paper: 2000)",
    )
    parser.add_argument(
        "--replications",
        type=int,
        default=3,
        help="number of simulated data sets (paper: 100)",
    )
    parser.add_argument("--seed", type=int, default=2009)
    parser.add_argument("--tolerance", type=float, default=1e-4)
    parser.add_argument("--max-iterations", type=int, default=1000)
    parser.add_argument(
        "--update-prior",
        action="store_true",
        help="use the empirical-Bayes extension discussed as future work",
    )
    args = parser.parse_args()
    if args.examinees < 1 or args.replications < 1:
        parser.error("examinees and replications must be positive")
    return args


if __name__ == "__main__":
    run_simulation(parse_args())
