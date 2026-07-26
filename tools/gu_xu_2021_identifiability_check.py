#!/usr/bin/env python3
"""Independent checks for Gu and Xu (2021).

The script implements the structural conditions in Theorems 1, 4, and 5
without third-party packages.  It also audits the small 5 x 2 search space
used in the paper and can inspect the authors' Q_aa.mat file when supplied.

Usage:
    python tools/gu_xu_2021_identifiability_check.py
    python tools/gu_xu_2021_identifiability_check.py \
        --author-mat path/to/Identify_Q/simulations/Q_aa.mat
"""

from __future__ import annotations

import argparse
import itertools
import math
import struct
from pathlib import Path
from typing import Iterable, Sequence

Matrix = tuple[tuple[int, ...], ...]


def as_matrix(rows: Iterable[Iterable[int]]) -> Matrix:
    q = tuple(tuple(int(value) for value in row) for row in rows)
    if not q or not q[0]:
        raise ValueError("Q must have at least one row and one column")
    width = len(q[0])
    if any(len(row) != width for row in q):
        raise ValueError("Q must be rectangular")
    if any(value not in (0, 1) for row in q for value in row):
        raise ValueError("Q must be binary")
    return q


def identity_row_indices(q: Matrix) -> tuple[int, ...] | None:
    """Return one row index for every unit vector, or None."""
    k = len(q[0])
    selected: list[int] = []
    for column in range(k):
        target = tuple(int(index == column) for index in range(k))
        try:
            selected.append(q.index(target))
        except ValueError:
            return None
    return tuple(selected)


def theorem1_conditions(q: Matrix) -> dict[str, object]:
    """Check A (complete), B (distinct Q-star columns), and C (three uses)."""
    q = as_matrix(q)
    k = len(q[0])
    identity = identity_row_indices(q)
    complete = identity is not None
    if complete:
        q_star = tuple(row for index, row in enumerate(q) if index not in identity)
        star_columns = tuple(
            tuple(row[column] for row in q_star) for column in range(k)
        )
        distinct = len(set(star_columns)) == k
    else:
        q_star = ()
        star_columns = ()
        distinct = False
    counts = tuple(sum(row[column] for row in q) for column in range(k))
    repeated = all(count >= 3 for count in counts)
    return {
        "A_complete": complete,
        "B_distinct": distinct,
        "C_repeated": repeated,
        "strictly_identifiable": complete and distinct and repeated,
        "identity_rows": identity,
        "q_star": q_star,
        "q_star_columns": star_columns,
        "attribute_counts": counts,
    }


def has_attribute_item_matching(q: Matrix) -> bool:
    """Hall/matching check for generic completeness."""
    q = as_matrix(q)
    j, k = len(q), len(q[0])
    if j < k:
        return False
    for item_indices in itertools.permutations(range(j), k):
        if all(q[item_indices[column]][column] == 1 for column in range(k)):
            return True
    return False


def theorem4_witness(q: Matrix) -> tuple[tuple[int, ...], ...] | None:
    """Find disjoint generically complete Q1/Q2 and a nonzero-column tail."""
    q = as_matrix(q)
    j, k = len(q), len(q[0])
    if j < 2 * k + 1:
        return None
    indices = tuple(range(j))
    for first in itertools.combinations(indices, k):
        if not has_attribute_item_matching(tuple(q[index] for index in first)):
            continue
        after_first = tuple(index for index in indices if index not in first)
        for second in itertools.combinations(after_first, k):
            if not has_attribute_item_matching(tuple(q[index] for index in second)):
                continue
            tail = tuple(index for index in after_first if index not in second)
            if all(any(q[index][column] for index in tail) for column in range(k)):
                return first, second, tail
    return None


def canonical_under_column_swap(q: Matrix) -> tuple[int, ...]:
    """Canonical representation for K=2 under a global column swap."""
    if len(q[0]) != 2:
        raise ValueError("This helper is only defined for K=2")
    original = tuple(value for row in q for value in row)
    swapped = tuple(value for row in q for value in reversed(row))
    return min(original, swapped)


def all_five_by_two_candidates() -> tuple[Matrix, ...]:
    """Enumerate nonzero-row 5 x 2 matrices modulo column swapping."""
    row_types = ((0, 1), (1, 0), (1, 1))
    unique: dict[tuple[int, ...], Matrix] = {}
    for rows in itertools.product(row_types, repeat=5):
        q = as_matrix(rows)
        unique.setdefault(canonical_under_column_swap(q), q)
    return tuple(unique.values())


def canonical_row_form(q: Matrix) -> tuple[tuple[int, int], ...]:
    """Collapse row permutations and the global K=2 column swap."""
    direct = tuple(sorted(q))
    swapped = tuple(sorted(tuple(reversed(row)) for row in q))
    return min(direct, swapped)


def load_author_q_aa(path: Path) -> tuple[Matrix, ...]:
    """Read the authors' uncompressed MATLAB v5 Q_aa array.

    The public file stores a 5 x 2 x 121 double array named Q_aa.  This small
    parser intentionally checks that exact representation and fails loudly for
    a different MAT-file layout.
    """
    raw = path.read_bytes()
    if not raw.startswith(b"MATLAB 5.0 MAT-file"):
        raise ValueError("expected an uncompressed MATLAB v5 MAT-file")
    marker = raw.find(b"Q_aa")
    if marker < 0:
        raise ValueError("Q_aa variable not found")
    data_tag = raw.find(struct.pack("<II", 9, 5 * 2 * 121 * 8), marker)
    if data_tag < 0:
        raise ValueError("expected 5 x 2 x 121 miDOUBLE payload not found")
    values = struct.unpack_from("<1210d", raw, data_tag + 8)
    matrices = []
    for page in range(121):
        base = page * 10
        matrices.append(
            as_matrix(
                [
                    [int(values[base + row + 5 * column]) for column in range(2)]
                    for row in range(5)
                ]
            )
        )
    return tuple(matrices)


def paper_examples() -> dict[str, Matrix]:
    return {
        "Q5_generic_DINA": as_matrix(
            [(0, 1), (1, 0), (1, 0), (0, 1), (0, 1)]
        ),
        "Q15_strict_DINA": as_matrix(
            [(0, 1), (1, 1), (1, 0), (1, 0), (0, 1)]
        ),
        "Q18_strict_DINA": as_matrix(
            [(0, 1), (1, 1), (1, 1), (1, 0), (0, 1)]
        ),
        "Q27_generic_GDINA": as_matrix(
            [(0, 1), (1, 1), (1, 1), (1, 1), (0, 1)]
        ),
        "Q54_generic_GDINA": as_matrix(
            [(0, 1), (1, 1), (1, 1), (1, 1), (1, 0)]
        ),
        "Q81_generic_GDINA": as_matrix(
            [(0, 1), (1, 1), (1, 1), (1, 1), (1, 1)]
        ),
    }


def k8_example() -> Matrix:
    identity = tuple(
        tuple(int(row == column) for column in range(8)) for row in range(8)
    )
    tail = (
        (0, 0, 1, 1, 1, 0, 1, 1),
        (0, 1, 0, 1, 0, 1, 1, 1),
        (1, 0, 0, 0, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 0, 1),
    )
    return identity + tail


def print_matrix_summary(name: str, q: Matrix) -> None:
    t1 = theorem1_conditions(q)
    witness = theorem4_witness(q)
    print(
        f"{name:20s} "
        f"A={int(t1['A_complete'])} "
        f"B={int(t1['B_distinct'])} "
        f"C={int(t1['C_repeated'])} "
        f"strict={int(t1['strictly_identifiable'])} "
        f"generic-complete={int(has_attribute_item_matching(q))} "
        f"D+E={int(witness is not None)} "
        f"counts={t1['attribute_counts']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--author-mat",
        type=Path,
        help="optional path to the authors' simulations/Q_aa.mat",
    )
    args = parser.parse_args()

    print("Paper examples")
    for name, q in paper_examples().items():
        print_matrix_summary(name, q)

    q8 = k8_example()
    expected_minimum = 8 + math.ceil(math.log2(8)) + 1
    assert len(q8) == expected_minimum == 12
    assert theorem1_conditions(q8)["strictly_identifiable"]
    print_matrix_summary("K8_J12_example", q8)

    candidates = all_five_by_two_candidates()
    strict = tuple(q for q in candidates if theorem1_conditions(q)["strictly_identifiable"])
    general = tuple(q for q in candidates if theorem4_witness(q) is not None)
    strict_forms = {canonical_row_form(q) for q in strict}
    general_forms = {canonical_row_form(q) for q in general}
    assert len(candidates) == 122
    assert len(strict) == 45
    assert len(strict_forms) == 2
    assert len(general) == 71
    assert len(general_forms) == 6
    print("\nIndependent 5 x 2 enumeration")
    print(f"column-swap classes: {len(candidates)}")
    print(f"Theorem 1 candidates: {len(strict)}; row/column forms: {len(strict_forms)}")
    print(f"Theorem 4 candidates: {len(general)}; row/column forms: {len(general_forms)}")

    if args.author_mat:
        author = load_author_q_aa(args.author_mat)
        author_keys = {canonical_under_column_swap(q) for q in author}
        full_keys = {canonical_under_column_swap(q) for q in candidates}
        missing = full_keys - author_keys
        assert len(author) == len(author_keys) == 121
        assert len(missing) == 1
        missing_flat = next(iter(missing))
        missing_q = as_matrix(
            missing_flat[index : index + 2] for index in range(0, 10, 2)
        )
        print("\nAudit of the authors' Q_aa.mat")
        print(f"stored candidates: {len(author)}")
        print(f"missing column-swap class: {missing_q}")
        print(
            "The omitted ordered candidate has the same row-multiset form as Q81; "
            "the six structural forms reported for Study V remain represented."
        )


if __name__ == "__main__":
    main()
