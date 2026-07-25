#!/usr/bin/env python3
"""Exact small-matrix checks for Kruskal (1977).

The script illustrates:

1. ordinary rank versus Kruskal rank;
2. the sufficient condition k_A + k_B + k_C >= 2R + 2;
3. invariance under a common permutation and compensating scalings;
4. a non-unique decomposition when one factor has repeated columns.

It is a teaching demo, not a general CP decomposition algorithm.
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]
Matrix = list[list[Fraction]]
Tensor = list[list[list[Fraction]]]


def as_fraction_matrix(matrix: Sequence[Sequence[Number]]) -> Matrix:
    """Convert a rectangular matrix to exact rational arithmetic."""

    result = [[Fraction(value) for value in row] for row in matrix]
    if not result or not result[0]:
        raise ValueError("matrix must be nonempty")
    width = len(result[0])
    if any(len(row) != width for row in result):
        raise ValueError("matrix must be rectangular")
    return result


def matrix_rank(matrix: Sequence[Sequence[Number]]) -> int:
    """Return exact row/column rank by Gaussian elimination."""

    work = as_fraction_matrix(matrix)
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
        work[rank] = [value / pivot_value for value in work[rank]]

        for row in range(row_count):
            if row == rank:
                continue
            factor = work[row][column]
            if factor == 0:
                continue
            work[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(work[row], work[rank])
            ]

        rank += 1
        if rank == row_count:
            break

    return rank


def select_columns(
    matrix: Sequence[Sequence[Number]],
    indices: Sequence[int],
) -> Matrix:
    """Return the submatrix containing the requested columns."""

    source = as_fraction_matrix(matrix)
    return [[row[index] for index in indices] for row in source]


def kruskal_rank(matrix: Sequence[Sequence[Number]]) -> int:
    """Compute exact column Kruskal rank by exhaustive enumeration."""

    source = as_fraction_matrix(matrix)
    column_count = len(source[0])
    result = 0

    for size in range(1, column_count + 1):
        every_subset_is_independent = all(
            matrix_rank(select_columns(source, indices)) == size
            for indices in itertools.combinations(range(column_count), size)
        )
        if not every_subset_is_independent:
            break
        result = size

    return result


def triple_product(
    a: Sequence[Sequence[Number]],
    b: Sequence[Sequence[Number]],
    c: Sequence[Sequence[Number]],
) -> Tensor:
    """Construct [A,B,C] exactly."""

    a_matrix = as_fraction_matrix(a)
    b_matrix = as_fraction_matrix(b)
    c_matrix = as_fraction_matrix(c)
    component_count = len(a_matrix[0])
    if len(b_matrix[0]) != component_count or len(c_matrix[0]) != component_count:
        raise ValueError("all factors must have the same number of columns")

    return [
        [
            [
                sum(
                    (
                        a_matrix[i][component]
                        * b_matrix[j][component]
                        * c_matrix[k][component]
                        for component in range(component_count)
                    ),
                    Fraction(0),
                )
                for k in range(len(c_matrix))
            ]
            for j in range(len(b_matrix))
        ]
        for i in range(len(a_matrix))
    ]


def permute_and_scale_columns(
    matrix: Sequence[Sequence[Number]],
    permutation: Sequence[int],
    scales: Sequence[Number],
) -> Matrix:
    """Apply a common column ordering followed by componentwise scales."""

    source = as_fraction_matrix(matrix)
    column_count = len(source[0])
    if sorted(permutation) != list(range(column_count)):
        raise ValueError("permutation must contain each column index once")
    if len(scales) != column_count:
        raise ValueError("one scale is required for each component")

    exact_scales = [Fraction(value) for value in scales]
    return [
        [
            row[old_index] * exact_scales[new_index]
            for new_index, old_index in enumerate(permutation)
        ]
        for row in source
    ]


def transpose(matrix: Sequence[Sequence[Number]]) -> Matrix:
    """Transpose a rectangular matrix."""

    source = as_fraction_matrix(matrix)
    return [list(column) for column in zip(*source)]


def multiply(
    left: Sequence[Sequence[Number]],
    right: Sequence[Sequence[Number]],
) -> Matrix:
    """Multiply two matrices exactly."""

    a = as_fraction_matrix(left)
    b = as_fraction_matrix(right)
    if len(a[0]) != len(b):
        raise ValueError("matrix dimensions are incompatible")
    return [
        [
            sum(
                (a[i][k] * b[k][j] for k in range(len(b))),
                Fraction(0),
            )
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def inverse_2_by_2(matrix: Sequence[Sequence[Number]]) -> Matrix:
    """Invert a nonsingular 2 by 2 matrix exactly."""

    source = as_fraction_matrix(matrix)
    if len(source) != 2 or len(source[0]) != 2:
        raise ValueError("this helper accepts only 2 by 2 matrices")
    a, b = source[0]
    c, d = source[1]
    determinant = a * d - b * c
    if determinant == 0:
        raise ValueError("matrix is singular")
    return [
        [d / determinant, -b / determinant],
        [-c / determinant, a / determinant],
    ]


def tensors_equal(left: Tensor, right: Tensor) -> bool:
    """Compare exact tensors."""

    return left == right


def full_rank_example() -> None:
    """Check the R=3 example and the intrinsic equivalence."""

    a = as_fraction_matrix(
        [
            [1, 0, 1],
            [0, 1, 1],
            [1, 1, 0],
        ]
    )
    b = as_fraction_matrix(
        [
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 1],
        ]
    )
    c = as_fraction_matrix(
        [
            [1, 2, 1],
            [0, 1, 1],
            [1, 0, 1],
        ]
    )

    ordinary_ranks = tuple(matrix_rank(matrix) for matrix in (a, b, c))
    k_ranks = tuple(kruskal_rank(matrix) for matrix in (a, b, c))
    component_count = 3
    left_side = sum(k_ranks)
    threshold = 2 * component_count + 2

    permutation = (1, 2, 0)
    lambda_scales = (Fraction(2), Fraction(1, 2), Fraction(1))
    mu_scales = (Fraction(3), Fraction(1), Fraction(1, 3))
    nu_scales = (Fraction(1, 6), Fraction(2), Fraction(3))
    scale_products = tuple(
        x * y * z
        for x, y, z in zip(lambda_scales, mu_scales, nu_scales)
    )

    transformed_a = permute_and_scale_columns(a, permutation, lambda_scales)
    transformed_b = permute_and_scale_columns(b, permutation, mu_scales)
    transformed_c = permute_and_scale_columns(c, permutation, nu_scales)
    original_tensor = triple_product(a, b, c)
    transformed_tensor = triple_product(
        transformed_a,
        transformed_b,
        transformed_c,
    )

    differences = [
        abs(original_tensor[i][j][k] - transformed_tensor[i][j][k])
        for i in range(len(original_tensor))
        for j in range(len(original_tensor[0]))
        for k in range(len(original_tensor[0][0]))
    ]

    print("Full-rank R=3 example")
    print(f"  ordinary ranks = {ordinary_ranks}")
    print(f"  Kruskal ranks = {k_ranks}")
    print(f"  condition: {left_side} >= {threshold} -> {left_side >= threshold}")
    print(f"  tensor rank certified as R = {component_count}")
    print(f"  componentwise scale products = {scale_products}")
    print(f"  max difference after permutation/scaling = {max(differences)}")


def non_unique_example() -> None:
    """Show matrix-factorization freedom when C has repeated columns."""

    identity = as_fraction_matrix([[1, 0], [0, 1]])
    c = as_fraction_matrix([[1, 1]])
    q = as_fraction_matrix([[1, 1], [0, 1]])
    q_inverse_transpose = transpose(inverse_2_by_2(q))

    original_tensor = triple_product(identity, identity, c)
    transformed_tensor = triple_product(q, q_inverse_transpose, c)
    k_ranks = (
        kruskal_rank(identity),
        kruskal_rank(identity),
        kruskal_rank(c),
    )
    left_side = sum(k_ranks)
    threshold = 2 * 2 + 2

    print("\nNon-unique matrix-like example")
    print(f"  Kruskal ranks = {k_ranks}")
    print(f"  condition: {left_side} >= {threshold} -> {left_side >= threshold}")
    print(
        "  Q @ (Q^{-T})^T = "
        f"{multiply(q, transpose(q_inverse_transpose))}"
    )
    print(
        "  equal tensors from a non-monomial Q = "
        f"{tensors_equal(original_tensor, transformed_tensor)}"
    )


def rank_versus_kruskal_rank_example() -> None:
    """Display two matrices with equal ordinary rank and different K-rank."""

    first = as_fraction_matrix([[1, 0, 1], [0, 1, 1]])
    second = as_fraction_matrix([[1, 1, 0], [0, 0, 1]])

    print("Ordinary rank versus Kruskal rank")
    print(
        "  A1: "
        f"rank = {matrix_rank(first)}, k-rank = {kruskal_rank(first)}"
    )
    print(
        "  A2: "
        f"rank = {matrix_rank(second)}, k-rank = {kruskal_rank(second)}"
    )
    print()


def main() -> None:
    """Run all exact checks."""

    rank_versus_kruskal_rank_example()
    full_rank_example()
    non_unique_example()


if __name__ == "__main__":
    main()
