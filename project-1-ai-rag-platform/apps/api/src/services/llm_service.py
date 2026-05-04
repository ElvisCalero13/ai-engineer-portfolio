from openai import OpenAI

from src.config import settings


class LlmService:
    def __init__(self):
        self.provider = getattr(settings, "llm_provider", "local")
        
        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required")
            
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = "gpt-4o-mini"

    def generate_answer(self, question: str, context: str) -> str:
        if self.provider == "openai":
            return self._openai_generate(question, context)

        return self._local_generate(question, context)

    def _openai_generate(self, question: str, context: str) -> str:
        prompt = f"""
You are an AI assistant for a RAG platform.

Answer the user's question using ONLY the context below.
If the context does not contain the answer, say:
"I don't have enough information in the uploaded documents to answer that."

Context:
{context}

Question:
{question}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions grounded only in retrieved document context.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content
    
    def _local_generate(self, question: str, context: str) -> str:
        # simple baseline (sin LLM externo)
        if not context:
            return "I don't have enough information in the uploaded documents to answer that."

        return context[:500]