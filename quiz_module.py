from gemini_client import generate_json


def generate_quiz(topic: str, number_of_questions: int) -> dict:
    result = generate_json(
        "Create a multiple-choice quiz and return only a JSON object with this shape: "
        '{"questions":[{"question":"...","options":["..."],'
        '"correct_answer":"...","explanation":"..."}]}. '
        f"Create exactly {number_of_questions} questions about {topic!r}. "
        "Each question must have four options, and correct_answer must exactly "
        "match one option."
    )
    questions = result.get("questions")
    if not isinstance(questions, list) or len(questions) != number_of_questions:
        raise RuntimeError("Gemini returned an invalid quiz.")

    for question in questions:
        if (
            not isinstance(question, dict)
            or not isinstance(question.get("question"), str)
            or not isinstance(question.get("options"), list)
            or not all(isinstance(option, str) for option in question["options"])
            or not isinstance(question.get("correct_answer"), str)
            or not isinstance(question.get("explanation"), str)
        ):
            raise RuntimeError("Gemini returned an invalid quiz question.")

    return {"topic": topic, "questions": questions}