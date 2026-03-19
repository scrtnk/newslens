# backend/news/ranker.py
from datetime import datetime, timezone
from backend.models.schemas import Article


def _recency_score(article: Article) -> float:
    """Returns decay score in (0, 1]: 1.0 = just published, ~0.5 = 24h ago."""
    if article.published is None:
        return 0.0
    pub = article.published
    if pub.tzinfo is None:
        pub = pub.replace(tzinfo=timezone.utc)
    age_hours = (datetime.now(timezone.utc) - pub).total_seconds() / 3600
    return 1.0 / (1.0 + age_hours / 24)


def rank_articles(articles: list[Article], n: int) -> list[Article]:
    if not articles:
        return []
    return sorted(articles, key=_recency_score, reverse=True)[:n]
