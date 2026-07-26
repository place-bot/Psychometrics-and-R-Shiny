#!/usr/bin/env python3
"""Independent numerical audit for Zhao and Huang (2019).

This script uses only the Python standard library.  It checks the published
item counts and result tables, constructs simple class-imbalance baselines,
quantifies the resolution of the reported test accuracy, and compares the
paper's printed Equation (9) with the usual support-weighted F1 definition.

It does not reproduce the fitted classifiers because the 805 item texts and
the authors' source code are not publicly available.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from typing import Iterable


CATEGORY_COUNTS = {
    "Using calculators": 3,
    "Statistics": 10,
    "Large integers": 25,
    "Logic": 32,
    "Operations of fractions": 46,
    "Graphical representation": 65,
    "Measurement": 83,
    "Mathematical thinking": 139,
    "Operations of integers": 666,
}

PAPER_RESULTS = {
    "unigram": {
        "LR": {"selected": (74.1, 73.5), "all": (72.5, 69.5)},
        "SVM": {"selected": (74.3, 72.8), "all": (71.1, 68.1)},
        "NB": {"selected": (84.0, 84.7), "all": (21.3, 22.4)},
    },
    "unigram+bigram": {
        "LR": {"selected": (74.6, 72.5), "all": (72.7, 69.7)},
        "SVM": {"selected": (74.9, 72.0), "all": (71.1, 68.1)},
        "NB": {"selected": (84.6, 85.2), "all": (69.1, 67.3)},
    },
    "unigram+bigram+trigram": {
        "LR": {"selected": (75.3, 73.1), "all": (72.5, 69.4)},
        "SVM": {"selected": (74.9, 72.0), "all": (71.3, 68.3)},
        "NB": {"selected": (85.2, 85.6), "all": (68.9, 67.2)},
    },
}


@dataclass(frozen=True)
class Confusion:
    """Binary confusion table with O and M as the two true classes."""

    actual_o_pred_o: int
    actual_o_pred_m: int
    actual_m_pred_o: int
    actual_m_pred_m: int

    @property
    def n(self) -> int:
        return sum(asdict(self).values())

    @property
    def actual_o(self) -> int:
        return self.actual_o_pred_o + self.actual_o_pred_m

    @property
    def actual_m(self) -> int:
        return self.actual_m_pred_o + self.actual_m_pred_m

    @property
    def predicted_o(self) -> int:
        return self.actual_o_pred_o + self.actual_m_pred_o

    @property
    def predicted_m(self) -> int:
        return self.actual_o_pred_m + self.actual_m_pred_m

    @property
    def accuracy(self) -> float:
        return (
            self.actual_o_pred_o + self.actual_m_pred_m
        ) / self.n


def f1(tp: int, fp: int, fn: int) -> float:
    denominator = 2 * tp + fp + fn
    return 0.0 if denominator == 0 else 2 * tp / denominator


def per_class_f1(confusion: Confusion) -> tuple[float, float]:
    f1_o = f1(
        confusion.actual_o_pred_o,
        confusion.actual_m_pred_o,
        confusion.actual_o_pred_m,
    )
    f1_m = f1(
        confusion.actual_m_pred_m,
        confusion.actual_o_pred_m,
        confusion.actual_m_pred_o,
    )
    return f1_o, f1_m


def support_weighted_f1(confusion: Confusion) -> float:
    """Standard weighted F1 used by scikit-learn."""

    f1_o, f1_m = per_class_f1(confusion)
    return (
        confusion.actual_o * f1_o + confusion.actual_m * f1_m
    ) / confusion.n


def printed_equation_9_f1(confusion: Confusion) -> float:
    """F1 obtained from the prediction-count weights printed in Equation (9)."""

    f1_o, f1_m = per_class_f1(confusion)
    return (
        confusion.predicted_o * f1_o + confusion.predicted_m * f1_m
    ) / confusion.n


def wilson_interval(
    successes: int, trials: int, z: float = 1.959963984540054
) -> tuple[float, float]:
    p = successes / trials
    denominator = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / denominator
    half_width = (
        z
        * math.sqrt(
            p * (1 - p) / trials + z * z / (4 * trials * trials)
        )
        / denominator
    )
    return center - half_width, center + half_width


def rounded_percent(value: float) -> float:
    return round(100 * value, 1)


def plausible_test_sizes(
    total: int, target_percent: float, fractions: Iterable[float]
) -> list[tuple[int, int, float]]:
    """Find nearby denominators that can produce the reported rounded value."""

    candidates: list[tuple[int, int, float]] = []
    for fraction in fractions:
        center = total * fraction
        for n in range(max(1, math.floor(center) - 2), math.ceil(center) + 3):
            for correct in range(n + 1):
                accuracy = correct / n
                if rounded_percent(accuracy) == target_percent:
                    candidates.append((n, correct, accuracy))
    return sorted(set(candidates))


def compatible_confusions(
    n: int,
    actual_o_candidates: Iterable[int],
    target_accuracy: float,
    target_weighted_f1: float,
) -> list[Confusion]:
    matches: list[Confusion] = []
    for actual_o in actual_o_candidates:
        actual_m = n - actual_o
        for true_o in range(actual_o + 1):
            for true_m in range(actual_m + 1):
                confusion = Confusion(
                    actual_o_pred_o=true_o,
                    actual_o_pred_m=actual_o - true_o,
                    actual_m_pred_o=actual_m - true_m,
                    actual_m_pred_m=true_m,
                )
                if (
                    rounded_percent(confusion.accuracy) == target_accuracy
                    and rounded_percent(support_weighted_f1(confusion))
                    == target_weighted_f1
                ):
                    matches.append(confusion)
    return matches


def build_report() -> dict[str, object]:
    total = sum(CATEGORY_COUNTS.values())
    o_count = CATEGORY_COUNTS["Operations of integers"]
    m_count = CATEGORY_COUNTS["Mathematical thinking"]
    binary_total = o_count + m_count
    majority_share = o_count / binary_total
    all_o = Confusion(
        actual_o_pred_o=o_count,
        actual_o_pred_m=0,
        actual_m_pred_o=m_count,
        actual_m_pred_m=0,
    )

    feature_gains: dict[str, dict[str, dict[str, float]]] = {}
    for representation, models in PAPER_RESULTS.items():
        feature_gains[representation] = {}
        for model, values in models.items():
            selected_accuracy, selected_f1 = values["selected"]
            all_accuracy, all_f1 = values["all"]
            feature_gains[representation][model] = {
                "accuracy_gain_pp": round(
                    selected_accuracy - all_accuracy, 1
                ),
                "f1_gain_pp": round(selected_f1 - all_f1, 1),
            }

    test_size_candidates = plausible_test_sizes(
        binary_total, 85.2, [0.10]
    )
    likely_test_n = 81
    likely_correct = 69
    interval = wilson_interval(likely_correct, likely_test_n)
    likely_o = round(likely_test_n * majority_share)
    confusion_matches = compatible_confusions(
        likely_test_n,
        [likely_o - 1, likely_o, likely_o + 1],
        85.2,
        85.6,
    )

    return {
        "source_counts": {
            "categories": CATEGORY_COUNTS,
            "total_items": total,
            "binary_subset_items": binary_total,
            "operations_of_integers": o_count,
            "mathematical_thinking": m_count,
            "majority_share": majority_share,
        },
        "majority_baselines": {
            "all_O_accuracy": all_o.accuracy,
            "all_O_standard_weighted_f1": support_weighted_f1(all_o),
            "all_O_printed_equation_9_f1": printed_equation_9_f1(all_o),
            "best_accuracy_gain_pp": round(
                85.2 - 100 * all_o.accuracy, 3
            ),
        },
        "feature_selection_gains": feature_gains,
        "k_grid": {
            "values": list(range(5, 301, 5)),
            "candidate_count_per_model_and_representation": 60,
        },
        "test_resolution": {
            "reported_best_accuracy_percent": 85.2,
            "possible_near_10_percent_split": [
                {
                    "test_n": n,
                    "correct": correct,
                    "accuracy": accuracy,
                }
                for n, correct, accuracy in test_size_candidates
            ],
            "likely_test_n": likely_test_n,
            "likely_correct": likely_correct,
            "one_item_percentage_points": 100 / likely_test_n,
            "wilson_95_interval": interval,
        },
        "compatible_best_result_confusions": [
            {
                **asdict(confusion),
                "accuracy": confusion.accuracy,
                "standard_weighted_f1": support_weighted_f1(confusion),
                "printed_equation_9_f1": printed_equation_9_f1(
                    confusion
                ),
            }
            for confusion in confusion_matches
        ],
    }


def print_human_report(report: dict[str, object]) -> None:
    counts = report["source_counts"]
    baselines = report["majority_baselines"]
    resolution = report["test_resolution"]

    print("Zhao & Huang (2019) numerical audit")
    print("=" * 41)
    print(
        f"Nine-category total: {counts['total_items']}; "
        f"O+M subset: {counts['binary_subset_items']}"
    )
    print(
        f"O share: {100 * counts['majority_share']:.3f}%; "
        f"all-O accuracy: {100 * baselines['all_O_accuracy']:.3f}%"
    )
    print(
        "All-O standard support-weighted F1: "
        f"{100 * baselines['all_O_standard_weighted_f1']:.3f}%"
    )
    print(
        "All-O F1 under printed Equation (9): "
        f"{100 * baselines['all_O_printed_equation_9_f1']:.3f}%"
    )
    print(
        "Best reported accuracy gain over all-O: "
        f"{baselines['best_accuracy_gain_pp']:.3f} percentage points"
    )
    print()

    print("Feature-selection gains (percentage points)")
    for representation, models in report["feature_selection_gains"].items():
        print(f"  {representation}")
        for model, gains in models.items():
            print(
                f"    {model}: accuracy {gains['accuracy_gain_pp']:+.1f}, "
                f"F1 {gains['f1_gain_pp']:+.1f}"
            )
    print()

    print(
        "k grid: 5..300 by 5 "
        f"({report['k_grid']['candidate_count_per_model_and_representation']} "
        "candidate sizes)"
    )
    print("Test-size candidates near a 10% split for 85.2% accuracy:")
    for candidate in resolution["possible_near_10_percent_split"]:
        print(
            f"  n={candidate['test_n']}, "
            f"correct={candidate['correct']}, "
            f"accuracy={100 * candidate['accuracy']:.3f}%"
        )
    low, high = resolution["wilson_95_interval"]
    print(
        f"If n=81 and correct=69, one item is "
        f"{resolution['one_item_percentage_points']:.3f} points and the "
        f"Wilson 95% interval is [{100 * low:.1f}%, {100 * high:.1f}%]."
    )
    print()

    print(
        "Confusion tables compatible with 85.2% accuracy and 85.6% "
        "standard weighted F1:"
    )
    for confusion in report["compatible_best_result_confusions"]:
        print(
            "  "
            f"O->O {confusion['actual_o_pred_o']}, "
            f"O->M {confusion['actual_o_pred_m']}, "
            f"M->O {confusion['actual_m_pred_o']}, "
            f"M->M {confusion['actual_m_pred_m']}; "
            f"Eq.(9)={100 * confusion['printed_equation_9_f1']:.1f}%"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the report as JSON instead of formatted text",
    )
    args = parser.parse_args()
    report = build_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human_report(report)


if __name__ == "__main__":
    main()
