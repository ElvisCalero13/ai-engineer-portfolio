def keyword_recall(answer: str, expected_keywords: list[str]) -> float:
    answer_lower = answer.lower()

    matched = [
        keyword for keyword in expected_keywords
        if keyword.lower() in answer_lower
    ]

    if not expected_keywords:
        return 0.0

    return len(matched) / len(expected_keywords)


def passed(score: float, threshold: float = 0.6) -> bool:
    return score >= threshold