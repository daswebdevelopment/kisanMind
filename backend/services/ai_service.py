from __future__ import annotations

import os

from groq import Groq

SYSTEM_PROMPT = (
    "You are KisanMind, an expert agricultural advisor for Indian farmers. "
    "You have deep knowledge of: Indian crops, seasons and farming practices; "
    "Pest and disease identification and treatment; Soil health and fertilizer recommendations; "
    "Government schemes for farmers; Mandi prices and selling advice. "
    "Always respond in simple, easy to understand language. "
    "Be concise and practical. If you don't know something, say so honestly. "
    "Never give harmful advice."
)

MODEL_NAME = "llama3-8b-8192"


def generate_farmer_answer(question: str) -> str:
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing")

    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question.strip()},
        ],
        temperature=0.7,
        max_tokens=500,
        timeout=8,
    )

    answer = completion.choices[0].message.content if completion.choices else None
    if not answer:
        raise RuntimeError("Groq returned an empty answer")
    return answer.strip()
