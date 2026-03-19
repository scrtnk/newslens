# tests/test_deduplicator.py
from backend.news.deduplicator import deduplicate
from backend.models.schemas import Article
from tests.fixtures.sample_articles import SAMPLE_ARTICLES


def test_removes_near_duplicate_titles():
    # "OpenAI launches GPT-5 model" vs "OpenAI launches GPT-5" → similarity ~0.93
    articles = [
        Article(title="OpenAI launches GPT-5 model", summary="", url="https://a.com", source="A"),
        Article(title="OpenAI launches GPT-5", summary="", url="https://b.com", source="B"),
        Article(title="Google announces new chip", summary="", url="https://c.com", source="C"),
    ]
    result = deduplicate(articles)
    assert len(result) == 2
    assert any(a.title == "Google announces new chip" for a in result)


def test_keeps_all_unique():
    assert len(deduplicate(SAMPLE_ARTICLES)) == len(SAMPLE_ARTICLES)


def test_empty_list():
    assert deduplicate([]) == []
