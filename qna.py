from gemini_client import generate_text


def answer_question(question: str) -> str:
    return generate_text(
        "Answer the learner's question clearly and accurately. "
        "Use concise language and explain important terms.\n\n"
        f"Question: {question}"
    )