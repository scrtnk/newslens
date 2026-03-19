# tests/test_html_renderer.py
from datetime import datetime, timezone
from app.html_renderer import render_briefing
from backend.models.schemas import BriefingResponse, StorySummary


def make_briefing():
    return BriefingResponse(
        topic="ai",
        stories=[
            StorySummary(
                headline="OpenAI releases GPT-5",
                summary="OpenAI announced GPT-5 with improved reasoning.",
                why_it_matters="Lowers cost of AI applications significantly.",
                source_url="https://example.com/article1",
            )
        ],
        key_terms=["inference cost", "reasoning model", "agent", "fine-tuning", "RLHF"],
        things_to_watch=["competitor response", "pricing", "open-source alternatives"],
        generated_at=datetime(2026, 3, 19, 10, 0, tzinfo=timezone.utc),
    )


def test_render_returns_html_string():
    html = render_briefing(make_briefing())
    assert isinstance(html, str)
    assert "<html" in html


def test_render_includes_headline():
    html = render_briefing(make_briefing())
    assert "OpenAI releases GPT-5" in html


def test_render_includes_key_terms():
    html = render_briefing(make_briefing())
    assert "inference cost" in html


def test_render_includes_things_to_watch():
    html = render_briefing(make_briefing())
    assert "competitor response" in html


def test_render_includes_source_link():
    html = render_briefing(make_briefing())
    assert "https://example.com/article1" in html
