# backend/news/deduplicator.py
from difflib import SequenceMatcher
from backend.models.schemas import Article

SIMILARITY_THRESHOLD = 0.75


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def deduplicate(articles: list[Article]) -> list[Article]:
    unique: list[Article] = []
    for article in articles:
        if not any(_similarity(article.title, seen.title) >= SIMILARITY_THRESHOLD for seen in unique):
            unique.append(article)
    return unique
