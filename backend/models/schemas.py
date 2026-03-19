from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional


class TopicEnum(str, Enum):
    ai = "ai"
    stocks = "stocks"
    geopolitics = "geopolitics"
    technology = "technology"
    business = "business"
    energy = "energy"
    crypto = "crypto"
    economy = "economy"


class Article(BaseModel):
    title: str
    summary: str
    url: str
    source: str
    published: Optional[datetime] = None


class StorySummary(BaseModel):
    headline: str
    summary: str
    why_it_matters: str
    source_url: str


class BriefingResponse(BaseModel):
    topic: str
    stories: list[StorySummary]
    key_terms: list[str]
    things_to_watch: list[str]
    generated_at: datetime
