"""Correctness grading (Part 3). Used by the evals and by the demo screen."""
import re


def normalize(text):
    text = re.sub(r"[`'\"*]", "", str(text).lower())
    return re.sub(r"\s+", " ", text).strip()


def grade(task, answer):
    """Expected fact: pass if any accepted form appears in the normalized answer."""
    truth = task["ground_truth"]
    if truth["type"] != "expected_fact":
        raise NotImplementedError(f"ground truth type {truth['type']!r}")
    answer = normalize(answer)
    return any(normalize(fact) in answer for fact in truth["any_of"])
