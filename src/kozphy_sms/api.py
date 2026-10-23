"""Local-only demo API. No authentication or rate limiting."""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .core import analyze

app = FastAPI(title="Kozphy SMS Risk Intelligence", version="0.1.0")


class AnalyzeRequest(BaseModel):
    text: str = Field(max_length=5000)


@app.post("/analyze")
def analyze_sms(payload: AnalyzeRequest) -> dict:
    return analyze(payload.text)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": "rules-v0.1"}
