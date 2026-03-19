# tests/test_ranker.py
from datetime import datetime, timezone, timedelta
from backend.news.ranker import rank_articles
from backend.models.schemas import Article


def _article(title, hours_ago, source="src"):
    return Article(
        title=title, summary="", url=f"https://{source}.com", source=source,
        published=datetime.now(timezone.utc) - timedelta(hours=hours_ago),
    )


def test_returns_top_n():
    articles = [_article(f"Article {i}", i) for i in range(10)]
    assert len(rank_articles(articles, n=3)) == 3


def test_prefers_recent():
    result = rank_articles([_article("Old", 48), _article("New", 1)], n=2)
    assert result[0].title == "New"


def test_handles_fewer_than_n():
    assert len(rank_articles([_article("Only", 1)], n=5)) == 1


def test_empty():
    assert rank_articles([], n=5) == []
