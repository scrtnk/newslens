# tests/test_fetcher.py
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.news.fetcher import fetch_articles
from backend.models.schemas import Article, TopicEnum


def _mock_entry(title, summary, link, source_title, dt):
    entry = MagicMock()
    entry.title = title
    entry.summary = summary
    entry.link = link
    entry.source.title = source_title
    entry.published_parsed = dt.timetuple()
    return entry


def test_fetch_articles_returns_articles():
    with patch("feedparser.parse") as mock_parse:
        feed = MagicMock()
        feed.entries = [_mock_entry("Test", "Summary", "https://x.com", "Src", datetime(2026, 3, 19))]
        mock_parse.return_value = feed

        result = fetch_articles(TopicEnum.ai)

    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(a, Article) for a in result)


def test_fetch_skips_empty_title_entries():
    with patch("feedparser.parse") as mock_parse:
        feed = MagicMock()
        bad = MagicMock()
        bad.title = ""
        feed.entries = [bad]
        mock_parse.return_value = feed

        result = fetch_articles(TopicEnum.ai)

    assert result == []
