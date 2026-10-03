from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import recommend_learning_path

load_dotenv()

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# -----------------------------
# Request Models
# -----------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class QuizRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    number_of_questions: int = Field(
        default=5,
        ge=1,
        le=10
    )


class RecommendationRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    current_level: str = Field(
        default="Beginner",
        max_length=50
    )

    goal: str = Field(
        default="Understand the topic",
        max_length=1000
    )


# -----------------------------
# Home Page
# -----------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# -----------------------------
# Q&A
# -----------------------------

@app.post("/qa")
async def qa(payload: TextRequest):

    answer = answer_question(
        payload.text
    )

    return {
        "answer": answer
    }


# -----------------------------
# Explanation
# -----------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    explanation = explain_topic(
        payload.text
    )

    return {
        "explanation": explanation
    }


# -----------------------------
# Quiz
# -----------------------------

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    return generate_quiz(
        payload.topic,
        payload.number_of_questions
    )


# -----------------------------
# Summarization
# -----------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    summary = summarize_text(
        payload.text
    )

    return {
        "summary": summary
    }


# -----------------------------
# Learning Recommendations
# -----------------------------

@app.post(
    "/learn/recommendations"
)
async def learning_recommendations(
    payload: RecommendationRequest
):

    return recommend_learning_path(
        payload.topic,
        payload.current_level,
        payload.goal
    )