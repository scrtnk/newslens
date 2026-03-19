# tests/test_summarizer.py
import json, pytest
from unittest.mock import patch, MagicMock
from backend.llm.summarizer import summarize
from backend.models.schemas import TopicEnum, BriefingResponse
from tests.fixtures.sample_articles import SAMPLE_ARTICLES

MOCK_RESPONSE = {
    "stories": [{
        "headline": "OpenAI releases GPT-5",
        "summary": "OpenAI announced GPT-5 today.",
        "why_it_matters": "Raises the bar for AI reasoning.",
        "source_url": "https://example.com/article1",
    }],
    "key_terms": ["reasoning model", "inference cost", "agent", "fine-tuning", "RLHF"],
    "things_to_watch": ["competitor response", "pricing", "open-source alternatives"],
}


def _mock_client(content: str):
    """Returns a mock OpenAI client whose .chat.completions.create() returns content."""
    msg = MagicMock(); msg.content = content
    choice = MagicMock(); choice.message = msg
    completion = MagicMock(); completion.choices = [choice]
    client = MagicMock()
    client.chat.completions.create.return_value = completion
    return client


def test_returns_briefing_response():
    with patch("backend.llm.summarizer._make_client",
               return_value=_mock_client(json.dumps(MOCK_RESPONSE))):
        result = summarize(TopicEnum.ai, SAMPLE_ARTICLES[:1])
    assert isinstance(result, BriefingResponse)
    assert result.topic == "ai"
    assert len(result.key_terms) == 5


def test_raises_on_invalid_json():
    with patch("backend.llm.summarizer._make_client",
               return_value=_mock_client("not json")):
        with pytest.raises(ValueError, match="LLM returned invalid JSON"):
            summarize(TopicEnum.ai, SAMPLE_ARTICLES[:1])
