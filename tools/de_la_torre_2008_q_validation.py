#!/usr/bin/env python3
"""Transparent reproduction of de la Torre's (2008) Q-validation idea.

The script implements the computational heart of the sequential EM-based
delta method:

1. fit a DINA model under a provisional Q-matrix;
2. retain the posterior class weights from that fit;
3. regroup those expected counts under candidate q-vectors;
4. calculate candidate guessing, slipping, and delta = 1 - s - g;
5. search sequentially by adding one attribute at a time.

It also includes the paper's five-attribute hypothetical item and all eleven
Q-misspecification conditions from Table 4. This is an independent teaching
implementation. The article reports that its original program was written in
Ox, but does not publish that source code.
"""

from __future__ import annotations

import argparse
import itertools
import random
from dataclasses import dataclass
from statistics import fmean
from typing import Iterable, List, Sequence, Tuple

from de_la_torre_2009_dina_em import (
    PAPER_Q_MATRIX,
    EMResult,
    Pattern,
    ResponseRow,
    all_attribute_patterns,
    e_step,
    fit_dina_em,
    ideal_response,
    ideal_response_matrix,
    m_step,
    simulate_responses,
)


@dataclass(frozen=True)
class Candidate:
    """Candidate q-vector and its implied DINA item parameters."""

    q_vector: Pattern
    guessing: float
    slipping: float
    delta: float


@dataclass(frozen=True)
class ExpectedCounts:
    """Posterior expected examinee and correct-response counts by class."""

    examinees: Tuple[Tuple[float, ...], ...]
    correct: Tuple[Tuple[float, ...], ...]


def posterior_expected_counts(
    responses: Sequence[ResponseRow],
    posterior: Sequence[Sequence[float]],
) -> ExpectedCounts:
    """Build N_jl and R_jl from one fitted DINA posterior distribution."""

    if not responses or len(responses) != len(posterior):
        raise ValueError("responses and posterior must have the same positive length")
    item_count = len(responses[0])
    class_count = len(posterior[0])
    examinees = [[0.0] * class_count for _ in range(item_count)]
    correct = [[0.0] * class_count for _ in range(item_count)]

    for response, weights in zip(responses, posterior):
        if len(response) != item_count or len(weights) != class_count:
            raise ValueError("response or posterior matrix is ragged")
        for class_index, weight in enumerate(weights):
            for item_index, observed in enumerate(response):
                examinees[item_index][class_index] += weight
                if observed:
                    correct[item_index][class_index] += weight

    return ExpectedCounts(
        tuple(tuple(row) for row in examinees),
        tuple(tuple(row) for row in correct),
    )


def candidate_from_counts(
    item_index: int,
    q_vector: Pattern,
    patterns: Sequence[Pattern],
    counts: ExpectedCounts,
) -> Candidate:
    """Compute equations for g-hat, s-hat, and delta-hat for one candidate."""

    if not any(q_vector):
        raise ValueError("the all-zero q-vector is excluded")
    group_n = [0.0, 0.0]
    group_r = [0.0, 0.0]
    for class_index, pattern in enumerate(patterns):
        state = ideal_response(pattern, q_vector)
        group_n[state] += counts.examinees[item_index][class_index]
        group_r[state] += counts.correct[item_index][class_index]
    if min(group_n) <= 0.0:
        raise ZeroDivisionError("candidate creates an empty ideal-response group")

    guessing = group_r[0] / group_n[0]
    slipping = (group_n[1] - group_r[1]) / group_n[1]
    return Candidate(
        q_vector=q_vector,
        guessing=guessing,
        slipping=slipping,
        delta=1.0 - slipping - guessing,
    )


def all_nonzero_q_vectors(attribute_count: int) -> List[Pattern]:
    """Return the 2^K - 1 candidates considered by exhaustive search."""

    return [
        pattern
        for pattern in itertools.product((0, 1), repeat=attribute_count)
        if any(pattern)
    ]


def exhaustive_search(
    item_index: int,
    patterns: Sequence[Pattern],
    counts: ExpectedCounts,
) -> List[Candidate]:
    """Rank every nonzero q-vector by estimated item discrimination."""

    candidates = [
        candidate_from_counts(item_index, q_vector, patterns, counts)
        for q_vector in all_nonzero_q_vectors(len(patterns[0]))
    ]
    return sorted(candidates, key=lambda candidate: candidate.delta, reverse=True)


def sequential_search(
    item_index: int,
    patterns: Sequence[Pattern],
    counts: ExpectedCounts,
    cutoff: float,
) -> Tuple[Candidate, Tuple[Tuple[Candidate, ...], ...]]:
    """Apply the paper's forward delta search and epsilon stopping rule."""

    if cutoff < 0.0:
        raise ValueError("cutoff must be nonnegative")
    attribute_count = len(patterns[0])
    selected: List[int] = []
    accepted: Candidate | None = None
    history: List[Tuple[Candidate, ...]] = []

    while len(selected) < attribute_count:
        step_candidates = []
        for attribute in range(attribute_count):
            if attribute in selected:
                continue
            q_vector = tuple(
                int(index in selected or index == attribute)
                for index in range(attribute_count)
            )
            step_candidates.append(
                candidate_from_counts(item_index, q_vector, patterns, counts)
            )
        step_candidates.sort(key=lambda candidate: candidate.delta, reverse=True)
        history.append(tuple(step_candidates))
        best = step_candidates[0]

        if accepted is not None and best.delta - accepted.delta <= cutoff:
            break
        selected = [
            index for index, required in enumerate(best.q_vector) if required
        ]
        accepted = best

    if accepted is None:
        raise RuntimeError("sequential search did not evaluate a candidate")
    return accepted, tuple(history)


def hypothetical_counts() -> Tuple[List[Pattern], ExpectedCounts]:
    """Expected counts for the paper's item requiring attributes 1 and 2."""

    patterns = all_attribute_patterns(5)
    true_q = (1, 1, 0, 0, 0)
    probabilities = [
        0.80 if ideal_response(pattern, true_q) else 0.20
        for pattern in patterns
    ]
    return patterns, ExpectedCounts(
        examinees=(tuple(1.0 for _ in patterns),),
        correct=(tuple(probabilities),),
    )


def misspecified_q_matrix(condition: int) -> Tuple[Pattern, ...]:
    """Construct one of Table 4's conditions, numbered 0 through 11."""

    if condition not in range(12):
        raise ValueError("condition must be between 0 and 11")
    q_matrix = [list(row) for row in PAPER_Q_MATRIX]
    replacements = {
        1: {0: (0, 1, 0, 0, 0)},
        2: {0: (1, 1, 0, 0, 0)},
        3: {10: (0, 1, 1, 0, 0)},
        4: {10: (0, 1, 0, 0, 0)},
        5: {10: (1, 1, 1, 0, 0)},
        6: {20: (0, 1, 1, 0, 0)},
        7: {20: (0, 0, 1, 0, 0)},
        8: {20: (0, 1, 1, 1, 0)},
        9: {20: (0, 0, 1, 1, 0)},
        10: {20: (0, 0, 1, 1, 1)},
        11: {
            0: (1, 1, 0, 0, 0),
            10: (1, 0, 1, 0, 0),
            20: (0, 1, 1, 1, 0),
        },
    }
    for item_index, replacement in replacements.get(condition, {}).items():
        q_matrix[item_index] = list(replacement)
    return tuple(tuple(row) for row in q_matrix)


def changed_items(condition: int) -> Tuple[int, ...]:
    """Return zero-based indices altered in one Table 4 condition."""

    return tuple(
        index
        for index, (truth, provisional) in enumerate(
            zip(PAPER_Q_MATRIX, misspecified_q_matrix(condition))
        )
        if truth != provisional
    )


def mean_guess_plus_slip(result: EMResult) -> float:
    """Test-level criterion used in the paper's comparisons."""

    return fmean(result.guessing) + fmean(result.slipping)


def proposed_q_matrix(
    patterns: Sequence[Pattern],
    counts: ExpectedCounts,
    cutoff: float,
) -> Tuple[Pattern, ...]:
    """Run sequential search for every item and assemble a candidate Q."""

    return tuple(
        sequential_search(item_index, patterns, counts, cutoff)[0].q_vector
        for item_index in range(len(counts.examinees))
    )


def continue_em(
    responses: Sequence[ResponseRow],
    q_matrix: Sequence[Pattern],
    initial: EMResult,
    cycles: int,
) -> EMResult:
    """Run the paper's small number of additional EM cycles under a new Q."""

    if cycles < 1:
        raise ValueError("cycles must be positive")
    patterns = all_attribute_patterns(len(q_matrix[0]))
    eta = ideal_response_matrix(patterns, q_matrix)
    guessing = list(initial.guessing)
    slipping = list(initial.slipping)
    priors = list(initial.priors)
    posterior = initial.posterior
    log_likelihood = initial.log_likelihood

    for _ in range(cycles):
        posterior, log_likelihood = e_step(
            responses,
            eta,
            guessing,
            slipping,
            priors,
        )
        guessing, slipping = m_step(responses, eta, posterior)
        priors = [
            sum(row[class_index] for row in posterior) / len(responses)
            for class_index in range(len(patterns))
        ]

    posterior, log_likelihood = e_step(
        responses,
        eta,
        guessing,
        slipping,
        priors,
    )
    return EMResult(
        guessing=guessing,
        slipping=slipping,
        priors=priors,
        posterior=posterior,
        log_likelihood=log_likelihood,
        iterations=cycles,
        converged=False,
    )


def format_q(q_vector: Iterable[int]) -> str:
    """Format a q-vector compactly for terminal output."""

    return "".join(str(value) for value in q_vector)


def print_hypothetical_item() -> None:
    """Reproduce Tables 1-2's central sequential-search calculation."""

    patterns, counts = hypothetical_counts()
    selected, history = sequential_search(0, patterns, counts, cutoff=0.0)
    print("Hypothetical item: true q = 11000, g = s = .20")
    for step, candidates in enumerate(history, start=1):
        rendered = ", ".join(
            f"{format_q(candidate.q_vector)}:{candidate.delta:.2f}"
            for candidate in candidates
        )
        print(f"  step {step}: {rendered}")
    print(
        "  selected "
        f"{format_q(selected.q_vector)} with "
        f"g={selected.guessing:.2f}, s={selected.slipping:.2f}, "
        f"delta={selected.delta:.2f}"
    )


def run_condition(
    condition: int,
    examinees: int,
    cutoffs: Sequence[float],
    seed: int,
    tolerance: float,
    max_iterations: int,
    compare_q: bool,
    additional_cycles: int,
) -> None:
    """Simulate once, fit a provisional Q, and validate its altered rows."""

    rng = random.Random(seed)
    true_parameters = [0.20] * len(PAPER_Q_MATRIX)
    responses, _ = simulate_responses(
        examinees,
        PAPER_Q_MATRIX,
        true_parameters,
        true_parameters,
        rng,
    )
    provisional = misspecified_q_matrix(condition)
    result = fit_dina_em(
        responses,
        provisional,
        tolerance=tolerance,
        max_iterations=max_iterations,
        update_prior=True,
    )
    patterns = all_attribute_patterns(5)
    counts = posterior_expected_counts(responses, result.posterior)

    print(f"\nCondition {condition}")
    print(
        f"  N={examinees}, iterations={result.iterations}, "
        f"converged={result.converged}, "
        f"mean(g)+mean(s)={mean_guess_plus_slip(result):.4f}"
    )
    targets = changed_items(condition) or (0, 10, 20)
    for item_index in targets:
        print(
            f"  item {item_index + 1}: "
            f"true={format_q(PAPER_Q_MATRIX[item_index])}, "
            f"provisional={format_q(provisional[item_index])}"
        )
        for cutoff in cutoffs:
            proposed, _ = sequential_search(
                item_index,
                patterns,
                counts,
                cutoff=cutoff,
            )
            print(
                f"    epsilon={cutoff:>5.3f}: "
                f"q={format_q(proposed.q_vector)}, "
                f"g={proposed.guessing:.3f}, "
                f"s={proposed.slipping:.3f}, "
                f"delta={proposed.delta:.3f}"
            )
        exhaustive = exhaustive_search(item_index, patterns, counts)[0]
        print(
            "    exhaustive maximum: "
            f"q={format_q(exhaustive.q_vector)}, "
            f"delta={exhaustive.delta:.3f}"
        )

    if compare_q:
        print("\n  Test-level candidate-Q comparison")
        for cutoff in cutoffs:
            proposal = proposed_q_matrix(patterns, counts, cutoff)
            updated = continue_em(
                responses,
                proposal,
                result,
                cycles=additional_cycles,
            )
            changed = sum(
                proposed != original
                for proposed, original in zip(proposal, provisional)
            )
            correct = sum(
                proposed == truth
                for proposed, truth in zip(proposal, PAPER_Q_MATRIX)
            )
            print(
                f"    epsilon={cutoff:>5.3f}: "
                f"changed={changed:>2}, "
                f"correct_rows={correct:>2}/30, "
                f"mean(g)+mean(s)={mean_guess_plus_slip(updated):.4f}"
            )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--condition",
        type=int,
        default=11,
        choices=range(12),
        help="Table 4 condition to reproduce (default: 11)",
    )
    parser.add_argument(
        "--examinees",
        type=int,
        default=1200,
        help="simulated sample size (paper: 5000)",
    )
    parser.add_argument(
        "--cutoffs",
        type=float,
        nargs="+",
        default=(0.00, 0.01, 0.05, 0.10, 0.20),
        help="epsilon values used by sequential search",
    )
    parser.add_argument("--seed", type=int, default=2008)
    parser.add_argument("--tolerance", type=float, default=0.001)
    parser.add_argument("--max-iterations", type=int, default=500)
    parser.add_argument(
        "--compare-q",
        action="store_true",
        help="assemble each candidate Q and run additional EM cycles",
    )
    parser.add_argument(
        "--additional-cycles",
        type=int,
        default=5,
        help="EM cycles for --compare-q (paper simulation: 5)",
    )
    parser.add_argument(
        "--paper-scale",
        action="store_true",
        help="override N with the paper's N=5000",
    )
    args = parser.parse_args()
    if args.examinees < 1:
        parser.error("--examinees must be positive")
    if any(value < 0.0 for value in args.cutoffs):
        parser.error("--cutoffs must be nonnegative")
    if args.additional_cycles < 1:
        parser.error("--additional-cycles must be positive")
    return args


def main() -> None:
    """Run the exact hypothetical example and one stochastic condition."""

    args = parse_args()
    print_hypothetical_item()
    run_condition(
        condition=args.condition,
        examinees=5000 if args.paper_scale else args.examinees,
        cutoffs=args.cutoffs,
        seed=args.seed,
        tolerance=args.tolerance,
        max_iterations=args.max_iterations,
        compare_q=args.compare_q,
        additional_cycles=args.additional_cycles,
    )


if __name__ == "__main__":
    main()
