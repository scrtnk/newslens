from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    max_articles_per_topic: int = 20
    top_n_articles: int = 5

    TOPIC_RSS_FEEDS: ClassVar[dict[str, list[str]]] = {
        "ai": [
            "https://feeds.feedburner.com/venturebeat/SZYF",
            "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        ],
        "stocks": [
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US",
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        ],
        "geopolitics": [
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
            "https://feeds.bbci.co.uk/news/world/rss.xml",
        ],
        "technology": [
            "https://techcrunch.com/feed/",
            "https://www.theverge.com/rss/index.xml",
        ],
        "business": [
            "https://feeds.bloomberg.com/markets/news.rss",
            "https://www.ft.com/rss/home/us",
        ],
        "energy": [
            "https://www.oilprice.com/rss/main",
            "https://rss.nytimes.com/services/xml/rss/nyt/Climate.xml",
        ],
        "crypto": [
            "https://coindesk.com/arc/outboundfeeds/rss/",
            "https://cointelegraph.com/rss",
        ],
        "economy": [
            "https://www.economist.com/finance-and-economics/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml",
        ],
    }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Lazy: Settings() is only constructed on first call, so imports never crash without .env."""
    return Settings()
