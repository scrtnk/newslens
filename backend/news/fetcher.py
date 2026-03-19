# backend/news/fetcher.py
from __future__ import annotations
import sys
import feedparser
from datetime import datetime
from time import mktime
from typing import Optional
from backend.models.schemas import Article, TopicEnum
from backend.config import get_settings


def _parse_entry(entry, feed_url: str) -> Optional[Article]:
    try:
        title = getattr(entry, "title", "").strip()
        if not title:
            return None
        summary = getattr(entry, "summary", "") or ""
        url = getattr(entry, "link", "")
        try:
            source = entry.source.title
        except AttributeError:
            source = feed_url.split("/")[2]
        published = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                published = datetime.fromtimestamp(mktime(entry.published_parsed))
            except Exception:
                pass
        return Article(title=title, summary=summary, url=url, source=source, published=published)
    except Exception:
        return None


def fetch_articles(topic: TopicEnum) -> list:
    cfg = get_settings()
    feeds = cfg.TOPIC_RSS_FEEDS.get(topic.value, [])
    articles = []
    errors = []
    for feed_url in feeds:
        try:
            parsed = feedparser.parse(feed_url)
            for entry in parsed.entries[: cfg.max_articles_per_topic]:
                article = _parse_entry(entry, feed_url)
                if article:
                    articles.append(article)
        except Exception as exc:
            errors.append(f"{feed_url}: {exc}")
            continue
    if not articles and errors:
        print(f"[fetcher] All feeds failed for {topic.value}: {errors}", file=sys.stderr)
    return articles
