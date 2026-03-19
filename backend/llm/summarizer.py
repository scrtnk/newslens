# backend/llm/summarizer.py
import json
from datetime import datetime, timezone
from openai import OpenAI
from backend.config import get_settings
from backend.models.schemas import Article, BriefingResponse, StorySummary, TopicEnum
from backend.llm.prompts import build_briefing_prompt


def _make_client() -> OpenAI:
    """Lazy factory — called inside summarize() so import never triggers OpenAI init."""
    return OpenAI(api_key=get_settings().openai_api_key)


def summarize(topic: TopicEnum, articles: list[Article]) -> BriefingResponse:
    client = _make_client()
    completion = client.chat.completions.create(
        model=get_settings().openai_model,
        messages=[{"role": "user", "content": build_briefing_prompt(topic, articles)}],
        temperature=0.3,
    )
    raw = completion.choices[0].message.content
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw: {raw[:200]}")
    return BriefingResponse(
        topic=topic.value,
        stories=[StorySummary(**s) for s in data["stories"]],
        key_terms=data["key_terms"],
        things_to_watch=data["things_to_watch"],
        generated_at=datetime.now(timezone.utc),
    )
