from gemini_client import generate_text


def summarize_text(text: str) -> str:
    return generate_text(
        "Summarize the following educational text. Preserve the key ideas and "
        "important terms, using concise bullet points.\n\n"
        f"Text:\n{text}"
    )