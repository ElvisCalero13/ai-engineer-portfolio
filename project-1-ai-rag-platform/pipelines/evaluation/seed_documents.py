import os
import requests


API_URL = os.getenv("API_URL", "http://localhost:8000")
SEED_DOCUMENT_PATH = "seed_documents/wellarchitected-framework.pdf"


def seed_document():
    if not os.path.exists(SEED_DOCUMENT_PATH):
        raise FileNotFoundError(f"Seed document not found: {SEED_DOCUMENT_PATH}")

    with open(SEED_DOCUMENT_PATH, "rb") as file:
        response = requests.post(
            f"{API_URL}/documents/upload",
            files={"file": file},
            timeout=300,
        )

    response.raise_for_status()
    print("Seed document uploaded successfully")
    print(response.json())


if __name__ == "__main__":
    seed_document()