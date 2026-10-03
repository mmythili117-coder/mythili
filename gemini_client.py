import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_text(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
    )
    text = response.text
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


def generate_json(prompt: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json"
        ),
    )
    text = response.text
    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    try:
        result = json.loads(text)
    except json.JSONDecodeError as error:
        raise RuntimeError("Gemini returned invalid JSON.") from error

    if not isinstance(result, dict):
        raise RuntimeError("Gemini returned an unexpected JSON structure.")
    return result