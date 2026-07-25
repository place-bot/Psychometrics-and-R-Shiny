#!/usr/bin/env python3
"""Exact teaching checks for Xu (2017).

The script verifies four algebraic objects used in the paper:

1. completeness, C1, and the DINA structural version of C2;
2. equivalence between exact-pattern probabilities and T-matrix marginals;
3. Proposition 3's invertible translation of the T-matrix;
4. a two-item nonidentifiability example when C1 holds and C2 fails.

All calculations use fractions from the Python standard library.  These
finite checks illustrate the paper; they do not constitute a numerical proof
of Theorem 1 for arbitrary K and J.
"""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction
from typing import Iterable, Sequence

Vector = tuple[int, ...]
Matrix = list[list[Fraction]]


def product(values: Iterable[Fraction]) -> Fraction:
    """Return an exact product."""

    result = Fraction(1)
    for value in values:
        result *= value
    return result


def binary_vectors(dimension: int) -> list[Vector]:
    """Return binary vectors ordered first by Hamming weight, then lexically."""

    return sorted(
        itertools.product((0, 1), repeat=dimension),
        key=lambda vector: (sum(vector), vector),
    )


def is_subset(left: Vector, right: Vector) -> bool:
    """Return whether left is componentwise no larger than right."""

    return all(a <= b for a, b in zip(left, right))


def unit_vector(dimension: int, index: int) -> Vector:
    """Return a standard basis vector."""

    return tuple(1 if position == index else 0 for position in range(dimension))


def is_complete(q_matrix: Sequence[Vector]) -> bool:
    """Check whether Q contains every row of I_K."""

    attribute_count = len(q_matrix[0])
    return all(
        unit_vector(attribute_count, index) in q_matrix
        for index in range(attribute_count)
    )


def remove_one_identity_block(q_matrix: Sequence[Vector]) -> list[Vector] | None:
    """Remove one copy of I_K, returning the remaining rows if possible."""

    remaining = list(q_matrix)
    attribute_count = len(q_matrix[0])
    for index in range(attribute_count):
        row = unit_vector(attribute_count, index)
        if row not in remaining:
            return None
        remaining.remove(row)
    return remaining


def has_c1(q_matrix: Sequence[Vector]) -> bool:
    """Check whether Q contains two disjoint copies of I_K."""

    remainder = remove_one_identity_block(q_matrix)
    return remainder is not None and remove_one_identity_block(remainder) is not None


def dina_structural_c2(q_matrix: Sequence[Vector]) -> bool:
    """Check C2 using only Q for a DINA model with 1-s_j > g_j.

    After removing two identity blocks, DINA distinguishes e_k from zero on
    a remaining item exactly when that item's q-vector equals e_k.
    """

    remainder = remove_one_identity_block(q_matrix)
    if remainder is None:
        return False
    remainder = remove_one_identity_block(remainder)
    if remainder is None:
        return False
    attribute_count = len(q_matrix[0])
    return all(
        unit_vector(attribute_count, index) in remainder
        for index in range(attribute_count)
    )


def dina_theta(
    q_matrix: Sequence[Vector],
    guessing: Sequence[Fraction],
    slipping: Sequence[Fraction],
) -> Matrix:
    """Construct Theta with rows indexed by items and columns by profiles."""

    if not (len(q_matrix) == len(guessing) == len(slipping)):
        raise ValueError("Q, guessing, and slipping must have the same length")
    profiles = binary_vectors(len(q_matrix[0]))
    return [
        [
            Fraction(1) - slip if is_subset(q_row, profile) else guess
            for profile in profiles
        ]
        for q_row, guess, slip in zip(q_matrix, guessing, slipping)
    ]


def t_matrix(theta: Matrix) -> tuple[list[Vector], Matrix]:
    """Build Xu's marginal T-matrix from a J by class-count Theta."""

    item_count = len(theta)
    response_subsets = binary_vectors(item_count)
    class_count = len(theta[0])
    matrix = [
        [
            product(
                theta[item][latent_class]
                for item, included in enumerate(subset)
                if included
            )
            for latent_class in range(class_count)
        ]
        for subset in response_subsets
    ]
    return response_subsets, matrix


def observed_distribution(theta: Matrix, proportions: Sequence[Fraction]) -> dict[Vector, Fraction]:
    """Enumerate the Bernoulli-product mixture distribution."""

    if len(theta[0]) != len(proportions):
        raise ValueError("one proportion is required for each latent class")
    if sum(proportions) != 1:
        raise ValueError("proportions must sum to one")

    distribution: dict[Vector, Fraction] = {}
    for response in binary_vectors(len(theta)):
        distribution[response] = sum(
            (
                proportions[latent_class]
                * product(
                    theta[item][latent_class]
                    if answered_correctly
                    else Fraction(1) - theta[item][latent_class]
                    for item, answered_correctly in enumerate(response)
                )
                for latent_class in range(len(proportions))
            ),
            Fraction(0),
        )
    return distribution


def subset_marginals(
    distribution: dict[Vector, Fraction],
    subsets: Sequence[Vector],
) -> list[Fraction]:
    """Convert exact response-pattern probabilities to subset marginals."""

    return [
        sum(
            (
                probability
                for response, probability in distribution.items()
                if is_subset(subset, response)
            ),
            Fraction(0),
        )
        for subset in subsets
    ]


def matrix_vector_product(matrix: Matrix, vector: Sequence[Fraction]) -> list[Fraction]:
    """Multiply a matrix by a vector exactly."""

    return [
        sum(
            (entry * weight for entry, weight in zip(row, vector)),
            Fraction(0),
        )
        for row in matrix
    ]


def matrix_product(left: Matrix, right: Matrix) -> Matrix:
    """Multiply two exact matrices."""

    if len(left[0]) != len(right):
        raise ValueError("incompatible matrix dimensions")
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                Fraction(0),
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def translation_matrix(subsets: Sequence[Vector], shift: Sequence[Fraction]) -> Matrix:
    """Construct D(theta*) in Proposition 3."""

    index = {subset: position for position, subset in enumerate(subsets)}
    dimension = len(subsets)
    result = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    for row_position, row_subset in enumerate(subsets):
        for column_subset in subsets:
            if not is_subset(column_subset, row_subset):
                continue
            coefficient = Fraction((-1) ** (sum(row_subset) - sum(column_subset)))
            coefficient *= product(
                shift[item]
                for item, (row_bit, column_bit) in enumerate(
                    zip(row_subset, column_subset)
                )
                if row_bit == 1 and column_bit == 0
            )
            result[row_position][index[column_subset]] = coefficient
    return result


def shifted_theta(theta: Matrix, shift: Sequence[Fraction]) -> Matrix:
    """Subtract item-specific shifts from every latent-class column."""

    if len(theta) != len(shift):
        raise ValueError("one shift is required for each item")
    return [
        [entry - shift_value for entry in row]
        for row, shift_value in zip(theta, shift)
    ]


def matrix_rank(matrix: Matrix) -> int:
    """Compute exact rank with Gaussian elimination."""

    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            factor = work[row][column]
            if factor == 0:
                continue
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def maximum_difference(
    left: dict[Vector, Fraction],
    right: dict[Vector, Fraction],
) -> Fraction:
    """Return the largest absolute entrywise difference."""

    return max(abs(left[key] - right[key]) for key in left)


def run_demo(attributes: int) -> None:
    """Run the checks reported in the accompanying notes."""

    if attributes < 1:
        raise ValueError("attributes must be positive")
    identity = [unit_vector(attributes, index) for index in range(attributes)]
    q_two_blocks = identity + identity
    q_three_blocks = identity + identity + identity

    print("Design checks")
    for name, q_matrix in (
        ("two I_K blocks", q_two_blocks),
        ("three I_K blocks", q_three_blocks),
    ):
        print(
            f"  {name}: complete={is_complete(q_matrix)}, "
            f"C1={has_c1(q_matrix)}, "
            f"DINA structural C2={dina_structural_c2(q_matrix)}"
        )

    q_matrix = q_three_blocks
    item_count = len(q_matrix)
    guessing = [Fraction(1, 5) + Fraction(item % 2, 20) for item in range(item_count)]
    slipping = [Fraction(1, 10) + Fraction(item % 3, 50) for item in range(item_count)]
    theta = dina_theta(q_matrix, guessing, slipping)
    class_count = 2**attributes
    raw_weights = [Fraction(index + 1) for index in range(class_count)]
    total_weight = sum(raw_weights)
    proportions = [weight / total_weight for weight in raw_weights]

    subsets, marginal_matrix = t_matrix(theta)
    distribution = observed_distribution(theta, proportions)
    direct_marginals = subset_marginals(distribution, subsets)
    t_marginals = matrix_vector_product(marginal_matrix, proportions)
    print("\nT-matrix check")
    print(f"  shape = {len(marginal_matrix)} x {len(marginal_matrix[0])}")
    print(f"  exact rank = {matrix_rank(marginal_matrix)}")
    print(f"  T p equals response-derived marginals = {t_marginals == direct_marginals}")

    shift = [
        theta[item][(item % class_count)]
        for item in range(item_count)
    ]
    transformation = translation_matrix(subsets, shift)
    _, translated_directly = t_matrix(shifted_theta(theta, shift))
    translated_by_d = matrix_product(transformation, marginal_matrix)
    print("\nProposition 3 check")
    print(
        "  T(Theta - theta* 1^T) equals D(theta*) T(Theta) = "
        f"{translated_directly == translated_by_d}"
    )
    print(
        "  diagonal of D is all one = "
        f"{all(transformation[i][i] == 1 for i in range(len(transformation)))}"
    )

    q_counterexample = [(1,), (1,)]
    theta_a = [
        [Fraction(1, 5), Fraction(4, 5)],
        [Fraction(3, 10), Fraction(9, 10)],
    ]
    proportions_a = [Fraction(2, 5), Fraction(3, 5)]
    theta_b = [
        [Fraction(13, 50), Fraction(43, 50)],
        [Fraction(93, 250), Fraction(237, 250)],
    ]
    proportions_b = [Fraction(1, 2), Fraction(1, 2)]
    distribution_a = observed_distribution(theta_a, proportions_a)
    distribution_b = observed_distribution(theta_b, proportions_b)
    print("\nC1-without-C2 counterexample")
    print(
        f"  complete={is_complete(q_counterexample)}, "
        f"C1={has_c1(q_counterexample)}, "
        f"DINA structural C2={dina_structural_c2(q_counterexample)}"
    )
    print(f"  parameter sets differ = {(theta_a, proportions_a) != (theta_b, proportions_b)}")
    print(f"  maximum distribution difference = {maximum_difference(distribution_a, distribution_b)}")
    print(
        "  P(11) = "
        f"{distribution_a[(1, 1)]} = {float(distribution_a[(1, 1)]):.3f}"
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--attributes",
        type=int,
        default=2,
        help="number of attributes in the C1/C2 and T-matrix checks (default: 2)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    run_demo(arguments.attributes)
