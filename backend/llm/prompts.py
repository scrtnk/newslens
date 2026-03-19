# backend/llm/prompts.py
from backend.models.schemas import Article, TopicEnum

TOPIC_CONTEXT: dict[str, str] = {
    "ai": "AI, machine learning, large language models, AI safety, and AI startups",
    "stocks": "stock markets, equities, earnings, Fed policy, and financial markets",
    "geopolitics": "international relations, wars, diplomacy, sanctions, and foreign policy",
    "technology": "consumer tech, hardware, chips, software, and startup ecosystem",
    "business": "corporate news, M&A, startups, funding rounds, and business strategy",
    "energy": "oil, gas, renewables, energy policy, and climate",
    "crypto": "cryptocurrency, blockchain, DeFi, NFTs, and Web3",
    "economy": "macroeconomics, inflation, central banks, GDP, and global trade",
}


def build_briefing_prompt(topic: TopicEnum, articles: list[Article]) -> str:
    context = TOPIC_CONTEXT.get(topic.value, topic.value)
    articles_text = "\n\n".join(
        f"[{i+1}] {a.title}\nSource: {a.source}\nURL: {a.url}\n{a.summary}"
        for i, a in enumerate(articles)
    )
    return f"""You are an expert news analyst specializing in {context}.

Below are today's top news articles on "{topic.value}":

{articles_text}

Produce a structured JSON briefing with EXACTLY this schema:
{{
  "stories": [
    {{
      "headline": "concise 1-line headline",
      "summary": "2-3 sentence factual summary",
      "why_it_matters": "1-2 sentence explanation of significance",
      "source_url": "url from the article"
    }}
  ],
  "key_terms": ["term1", "term2", "term3", "term4", "term5"],
  "things_to_watch": ["item1", "item2", "item3"]
}}

Rules:
- Include ALL {len(articles)} articles as stories, ordered by importance
- key_terms: 5 domain-specific terms a reader should know today
- things_to_watch: 3 concrete follow-up angles
- Return ONLY valid JSON, no markdown, no extra text
"""
