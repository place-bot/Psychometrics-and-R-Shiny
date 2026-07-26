#!/usr/bin/env python3
"""Leakage-safe reconstruction of Zhao and Huang's three-stage pipeline.

Expected CSV columns:

    text,label
    "计算 38 与 17 的和","O"
    "根据图表选择正确关系","M"

The original 805 item texts and source code are unavailable, so this program is
an independent implementation of the method described in the paper.  It keeps
the test set untouched, fits tokenization-independent vocabulary and IDF values
on training data, ranks features by mutual information on training data, tunes
k on validation data, and reports one final test result.

Dependencies:

    python -m pip install jieba numpy scipy scikit-learn
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass
class Dependencies:
    jieba: Any
    np: Any
    clone: Callable[..., Any]
    accuracy_score: Callable[..., float]
    balanced_accuracy_score: Callable[..., float]
    classification_report: Callable[..., dict[str, Any]]
    f1_score: Callable[..., float]
    mutual_info_classif: Callable[..., Any]
    GaussianNB: Any
    LogisticRegression: Any
    LinearSVC: Any
    train_test_split: Callable[..., Any]
    TfidfVectorizer: Any


def load_dependencies() -> Dependencies:
    try:
        import jieba
        import numpy as np
        from sklearn.base import clone
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.feature_selection import mutual_info_classif
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import (
            accuracy_score,
            balanced_accuracy_score,
            classification_report,
            f1_score,
        )
        from sklearn.model_selection import train_test_split
        from sklearn.naive_bayes import GaussianNB
        from sklearn.svm import LinearSVC
    except ImportError as error:
        raise SystemExit(
            "Missing optional dependency. Install with:\n"
            "python -m pip install jieba numpy scipy scikit-learn\n"
            f"Original import error: {error}"
        ) from error

    return Dependencies(
        jieba=jieba,
        np=np,
        clone=clone,
        accuracy_score=accuracy_score,
        balanced_accuracy_score=balanced_accuracy_score,
        classification_report=classification_report,
        f1_score=f1_score,
        mutual_info_classif=mutual_info_classif,
        GaussianNB=GaussianNB,
        LogisticRegression=LogisticRegression,
        LinearSVC=LinearSVC,
        train_test_split=train_test_split,
        TfidfVectorizer=TfidfVectorizer,
    )


def read_items(path: Path) -> tuple[list[str], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"text", "label"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise SystemExit("CSV must contain text and label columns.")
        texts: list[str] = []
        labels: list[str] = []
        for row_number, row in enumerate(reader, start=2):
            text = (row.get("text") or "").strip()
            label = (row.get("label") or "").strip()
            if not text or not label:
                raise SystemExit(
                    f"Empty text or label in CSV row {row_number}."
                )
            texts.append(text)
            labels.append(label)
    if len(texts) < 20:
        raise SystemExit("At least 20 labeled items are required.")
    if len(set(labels)) < 2:
        raise SystemExit("At least two labels are required.")
    return texts, labels


def segment(texts: list[str], jieba_module: Any) -> list[str]:
    return [" ".join(jieba_module.lcut(text)) for text in texts]


def stratified_split(
    texts: list[str],
    labels: list[str],
    *,
    seed: int,
    deps: Dependencies,
) -> tuple[list[str], list[str], list[str], list[str], list[str], list[str]]:
    train_x, temporary_x, train_y, temporary_y = deps.train_test_split(
        texts,
        labels,
        test_size=0.20,
        random_state=seed,
        stratify=labels,
    )
    validation_x, test_x, validation_y, test_y = deps.train_test_split(
        temporary_x,
        temporary_y,
        test_size=0.50,
        random_state=seed,
        stratify=temporary_y,
    )
    return train_x, validation_x, test_x, train_y, validation_y, test_y


def rank_by_mutual_information(
    x_train: Any,
    y_train: list[str],
    *,
    seed: int,
    deps: Dependencies,
) -> Any:
    occurrence = (x_train > 0).astype("int8")
    scores = deps.mutual_info_classif(
        occurrence,
        y_train,
        discrete_features=True,
        random_state=seed,
    )
    return deps.np.argsort(-scores), scores


def make_models(seed: int, deps: Dependencies) -> dict[str, Any]:
    return {
        "LR": deps.LogisticRegression(
            C=1.0,
            penalty="l2",
            solver="liblinear",
            max_iter=5000,
            random_state=seed,
        ),
        "SVM": deps.LinearSVC(
            C=1.0,
            loss="squared_hinge",
            max_iter=10000,
            random_state=seed,
        ),
        "NB": deps.GaussianNB(),
    }


def model_matrix(matrix: Any, model_name: str) -> Any:
    return matrix.toarray() if model_name == "NB" else matrix


def tune_model(
    model_template: Any,
    model_name: str,
    ranked_indices: Any,
    x_train: Any,
    y_train: list[str],
    x_validation: Any,
    y_validation: list[str],
    *,
    maximum_k: int,
    deps: Dependencies,
) -> tuple[int, float]:
    best_k = 0
    best_score = -1.0
    available = x_train.shape[1]
    for requested_k in range(5, maximum_k + 1, 5):
        k = min(requested_k, available)
        indices = ranked_indices[:k]
        model = deps.clone(model_template)
        model.fit(model_matrix(x_train[:, indices], model_name), y_train)
        predictions = model.predict(
            model_matrix(x_validation[:, indices], model_name)
        )
        score = deps.f1_score(
            y_validation, predictions, average="weighted"
        )
        if score > best_score:
            best_k = k
            best_score = score
        if k == available:
            break
    return best_k, best_score


def evaluate_configuration(
    train_x: list[str],
    validation_x: list[str],
    test_x: list[str],
    train_y: list[str],
    validation_y: list[str],
    test_y: list[str],
    *,
    ngram_max: int,
    maximum_k: int,
    seed: int,
    deps: Dependencies,
) -> dict[str, Any]:
    vectorizer = deps.TfidfVectorizer(
        analyzer="word",
        tokenizer=str.split,
        preprocessor=None,
        token_pattern=None,
        lowercase=False,
        ngram_range=(1, ngram_max),
        sublinear_tf=False,
        norm="l2",
    )
    x_train = vectorizer.fit_transform(train_x)
    x_validation = vectorizer.transform(validation_x)
    x_test = vectorizer.transform(test_x)
    ranked_indices, scores = rank_by_mutual_information(
        x_train, train_y, seed=seed, deps=deps
    )
    feature_names = vectorizer.get_feature_names_out()

    results: dict[str, Any] = {
        "ngram_range": [1, ngram_max],
        "vocabulary_size": int(x_train.shape[1]),
        "models": {},
    }
    for model_name, template in make_models(seed, deps).items():
        best_k, validation_f1 = tune_model(
            template,
            model_name,
            ranked_indices,
            x_train,
            train_y,
            x_validation,
            validation_y,
            maximum_k=maximum_k,
            deps=deps,
        )
        selected = ranked_indices[:best_k]
        model = deps.clone(template)
        model.fit(model_matrix(x_train[:, selected], model_name), train_y)
        predictions = model.predict(
            model_matrix(x_test[:, selected], model_name)
        )
        results["models"][model_name] = {
            "selected_k": int(best_k),
            "validation_weighted_f1": float(validation_f1),
            "test_accuracy": float(
                deps.accuracy_score(test_y, predictions)
            ),
            "test_weighted_f1": float(
                deps.f1_score(test_y, predictions, average="weighted")
            ),
            "test_macro_f1": float(
                deps.f1_score(test_y, predictions, average="macro")
            ),
            "test_balanced_accuracy": float(
                deps.balanced_accuracy_score(test_y, predictions)
            ),
            "test_report": deps.classification_report(
                test_y,
                predictions,
                output_dict=True,
                zero_division=0,
            ),
            "top_features": [
                {
                    "feature": str(feature_names[index]),
                    "mutual_information": float(scores[index]),
                }
                for index in selected[: min(30, best_k)]
            ],
        }
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="UTF-8 CSV with text,label")
    parser.add_argument(
        "--seed", type=int, default=2019, help="reproducible split seed"
    )
    parser.add_argument(
        "--maximum-k",
        type=int,
        default=300,
        help="largest number of retained features",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="optional JSON output path; stdout is always used",
    )
    args = parser.parse_args()
    deps = load_dependencies()
    texts, labels = read_items(args.csv)
    segmented = segment(texts, deps.jieba)
    (
        train_x,
        validation_x,
        test_x,
        train_y,
        validation_y,
        test_y,
    ) = stratified_split(segmented, labels, seed=args.seed, deps=deps)

    report: dict[str, Any] = {
        "implementation": "independent reconstruction",
        "seed": args.seed,
        "split_sizes": {
            "train": len(train_x),
            "validation": len(validation_x),
            "test": len(test_x),
        },
        "label_counts": {
            label: labels.count(label) for label in sorted(set(labels))
        },
        "configurations": [],
    }
    for ngram_max in (1, 2, 3):
        report["configurations"].append(
            evaluate_configuration(
                train_x,
                validation_x,
                test_x,
                train_y,
                validation_y,
                test_y,
                ngram_max=ngram_max,
                maximum_k=args.maximum_k,
                seed=args.seed,
                deps=deps,
            )
        )

    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
