import json
import requests
import os

from metrics import keyword_recall, passed

EVAL_MODE = os.getenv("EVAL_MODE", "retrieval")  # retrieval | answer
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
TOP_K = int(os.getenv("TOP_K", "5"))

if EVAL_MODE == "retrieval":
    API_URL = f"{API_BASE_URL}/chat/retrieve"
else:
    API_URL = f"{API_BASE_URL}/chat"

def load_dataset(path: str = "eval_dataset.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def ask_rag(question: str) -> dict:
    payload = {"question": question}

    if EVAL_MODE == "retrieval":
        payload["limit"] = TOP_K
    else:
        payload["top_k"] = TOP_K

    response = requests.post(
        API_URL,
        json=payload,
        timeout=180,
    )
    response.raise_for_status()
    return response.json()


def main():
    dataset = load_dataset()

    total = 0
    passed_count = 0
    minimum_pass_rate = 0.7
    
    print("\nRAG Evaluation Results")
    print("=" * 50)

    for item in dataset:
        question = item["question"]
        expected_keywords = item["expected_keywords"]

        result = ask_rag(question)
        if EVAL_MODE == "retrieval":
            answer = " ".join([chunk["text"] for chunk in result["results"]])
        else:
            answer = result["answer"]

        score = keyword_recall(answer, expected_keywords)
        is_passed = passed(score)

        total += 1
        passed_count += int(is_passed)

        print(f"\nQuestion: {question}")
        print(f"Answer: {answer}")
        print(f"Keyword Recall: {score:.2f}")
        print(f"Passed: {is_passed}")

    pass_rate = passed_count / total if total else 0

    print("\nSummary")
    print("=" * 50)
    print(f"Mode: {EVAL_MODE}")
    print(f"Total tests: {total}")
    print(f"Passed: {passed_count}")
    print(f"Pass rate: {pass_rate:.2%}")

    if pass_rate < minimum_pass_rate:
        raise SystemExit(
            f"RAG evaluation failed. Pass rate {pass_rate:.2%} is below required {minimum_pass_rate:.2%}"
        )

    print("RAG evaluation passed")

if __name__ == "__main__":
    main()