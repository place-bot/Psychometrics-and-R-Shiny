#!/usr/bin/env python3
"""Small numerical checks for Allman, Matias, and Rhodes (2009).

This script does not estimate a latent-class model. It illustrates:

1. the tripartition condition in Theorem 4;
2. row-tensor-product block probability matrices;
3. marginal recovery of item probabilities from a block;
4. invariance of the observed distribution under class-label permutation.

It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections.abc import Iterable, Sequence


def product(values: Iterable[float | int]) -> float | int:
    """Return a product without requiring a third-party numerical library."""

    result: float | int = 1
    for value in values:
        result *= value
    return result


def bernoulli_sufficient_bound(number_of_classes: int) -> int:
    """Corollary 5: p >= 2 ceil(log_2 r) + 1."""

    if number_of_classes < 1:
        raise ValueError("number_of_classes must be positive")
    return 2 * math.ceil(math.log2(number_of_classes)) + 1


def tripartition_score(
    number_of_classes: int,
    arities: Sequence[int],
    blocks: Sequence[Sequence[int]],
) -> tuple[int, tuple[int, int, int]]:
    """Compute the left side of Theorem 4 and the three block state counts."""

    if len(blocks) != 3 or any(not block for block in blocks):
        raise ValueError("blocks must contain three nonempty index sets")

    flattened = [index for block in blocks for index in block]
    if sorted(flattened) != list(range(len(arities))):
        raise ValueError("blocks must partition all observed-variable indices")

    state_counts = tuple(
        int(product(arities[index] for index in block)) for block in blocks
    )
    score = sum(min(number_of_classes, count) for count in state_counts)
    return score, state_counts


def best_tripartition(
    number_of_classes: int, arities: Sequence[int]
) -> tuple[tuple[tuple[int, ...], ...], int, tuple[int, int, int]]:
    """Find a highest-scoring tripartition by exhaustive search.

    The routine is intended for the small examples used in these notes.
    """

    if len(arities) < 3:
        raise ValueError("at least three observed variables are required")
    if any(arity < 2 for arity in arities):
        raise ValueError("each observed variable must have at least two states")

    best: tuple[tuple[tuple[int, ...], ...], int, tuple[int, int, int]] | None = None
    for assignments in itertools.product(range(3), repeat=len(arities)):
        if set(assignments) != {0, 1, 2}:
            continue
        blocks = tuple(
            tuple(index for index, block_id in enumerate(assignments) if block_id == b)
            for b in range(3)
        )
        score, counts = tripartition_score(number_of_classes, arities, blocks)
        candidate = (blocks, score, counts)
        if best is None or candidate[1] > best[1]:
            best = candidate

    if best is None:
        raise RuntimeError("no tripartition found")
    return best


def block_probability_row(
    item_success_probabilities: Sequence[float],
) -> list[float]:
    """Return probabilities for binary response patterns in lexical order."""

    probabilities: list[float] = []
    for pattern in itertools.product((0, 1), repeat=len(item_success_probabilities)):
        probability = product(
            theta if response else 1.0 - theta
            for response, theta in zip(pattern, item_success_probabilities)
        )
        probabilities.append(float(probability))
    return probabilities


def block_probability_matrix(
    theta: Sequence[Sequence[float]], item_indices: Sequence[int]
) -> list[list[float]]:
    """Build the row-tensor-product matrix for one binary item block."""

    return [
        block_probability_row([class_row[index] for index in item_indices])
        for class_row in theta
    ]


def recover_item_probability(
    block_row: Sequence[float], block_size: int, item_position: int
) -> float:
    """Marginalize a block probability row to recover one item probability."""

    patterns = itertools.product((0, 1), repeat=block_size)
    return sum(
        probability
        for pattern, probability in zip(patterns, block_row)
        if pattern[item_position] == 1
    )


def matrix_rank(matrix: Sequence[Sequence[float]], tolerance: float = 1e-12) -> int:
    """Compute numerical row rank with Gaussian elimination."""

    work = [list(map(float, row)) for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    rank = 0

    for column in range(columns):
        pivot = max(range(rank, rows), key=lambda row: abs(work[row][column]))
        if abs(work[pivot][column]) <= tolerance:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def observed_distribution(
    class_probabilities: Sequence[float],
    theta: Sequence[Sequence[float]],
) -> dict[tuple[int, ...], float]:
    """Enumerate the Bernoulli-product mixture distribution."""

    if len(class_probabilities) != len(theta):
        raise ValueError("one theta row is required for each class probability")
    if not math.isclose(sum(class_probabilities), 1.0):
        raise ValueError("class probabilities must sum to one")

    item_count = len(theta[0])
    distribution: dict[tuple[int, ...], float] = {}
    for pattern in itertools.product((0, 1), repeat=item_count):
        probability = 0.0
        for weight, class_row in zip(class_probabilities, theta):
            class_probability = product(
                item_theta if response else 1.0 - item_theta
                for response, item_theta in zip(pattern, class_row)
            )
            probability += weight * float(class_probability)
        distribution[pattern] = probability
    return distribution


def permute_classes(
    class_probabilities: Sequence[float],
    theta: Sequence[Sequence[float]],
    permutation: Sequence[int],
) -> tuple[list[float], list[list[float]]]:
    """Apply the same class permutation to mixture weights and theta rows."""

    expected = list(range(len(class_probabilities)))
    if sorted(permutation) != expected:
        raise ValueError("permutation must contain each class index once")
    return (
        [class_probabilities[index] for index in permutation],
        [list(theta[index]) for index in permutation],
    )


def format_blocks(blocks: Sequence[Sequence[int]]) -> str:
    """Format zero-based Python indices as one-based mathematical indices."""

    return " | ".join(
        "{" + ", ".join(str(index + 1) for index in block) + "}" for block in blocks
    )


def run_demo(number_of_classes: int, number_of_binary_items: int) -> None:
    """Print dimension checks and the worked example used in the notes."""

    arities = [2] * number_of_binary_items
    blocks, score, state_counts = best_tripartition(number_of_classes, arities)
    threshold = 2 * number_of_classes + 2

    print("Theorem 4 dimension check")
    print(f"  r = {number_of_classes}")
    print(f"  arities = {arities}")
    print(f"  best blocks = {format_blocks(blocks)}")
    print(f"  block state counts = {state_counts}")
    print(f"  score = {score}; threshold = {threshold}")
    print(f"  sufficient dimension condition = {score >= threshold}")
    print(
        "  Bernoulli Corollary 5 bound = "
        f"{bernoulli_sufficient_bound(number_of_classes)} items"
    )

    class_probabilities = [0.10, 0.20, 0.30, 0.40]
    theta = [
        [0.15, 0.20, 0.25, 0.30, 0.35],
        [0.30, 0.40, 0.50, 0.60, 0.70],
        [0.55, 0.65, 0.35, 0.75, 0.45],
        [0.80, 0.70, 0.85, 0.65, 0.90],
    ]
    if number_of_classes == 4 and number_of_binary_items == 5:
        print("\nWorked r=4, p=5 example")
        example_blocks = ((0, 1), (2, 3), (4,))
        matrices = [
            block_probability_matrix(theta, block) for block in example_blocks
        ]
        for block, matrix in zip(example_blocks, matrices):
            print(
                f"  block {format_blocks((block,))}: "
                f"shape={len(matrix)}x{len(matrix[0])}, rank={matrix_rank(matrix)}"
            )
        first_row = matrices[0][0]
        print(f"  first class, first block row = {[round(x, 6) for x in first_row]}")
        recovered = [
            recover_item_probability(first_row, block_size=2, item_position=position)
            for position in range(2)
        ]
        print(f"  recovered item probabilities = {[round(x, 6) for x in recovered]}")

        original = observed_distribution(class_probabilities, theta)
        permuted_pi, permuted_theta = permute_classes(
            class_probabilities, theta, [3, 1, 2, 0]
        )
        permuted = observed_distribution(permuted_pi, permuted_theta)
        maximum_difference = max(
            abs(original[pattern] - permuted[pattern]) for pattern in original
        )
        print(f"  sum of observed probabilities = {sum(original.values()):.12f}")
        print(f"  P(1,1,1,1,1) = {original[(1, 1, 1, 1, 1)]:.12f}")
        print(f"  max difference after class permutation = {maximum_difference:.3e}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classes", type=int, default=4)
    parser.add_argument("--binary-items", type=int, default=5)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    run_demo(arguments.classes, arguments.binary_items)

