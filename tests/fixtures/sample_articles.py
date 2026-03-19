# tests/fixtures/sample_articles.py
from datetime import datetime
from backend.models.schemas import Article

SAMPLE_ARTICLES = [
    Article(
        title="OpenAI releases GPT-5 with improved reasoning",
        summary="OpenAI announced GPT-5 today, claiming 3x improvement in reasoning tasks.",
        url="https://example.com/article1",
        source="TechCrunch",
        published=datetime(2026, 3, 19, 10, 0),
    ),
    Article(
        title="Google DeepMind unveils new multimodal model",
        summary="DeepMind's latest model can process text, images, and video simultaneously.",
        url="https://example.com/article2",
        source="The Verge",
        published=datetime(2026, 3, 19, 9, 0),
    ),
    Article(
        title="EU passes landmark AI regulation bill",
        summary="The European Parliament voted 450-100 in favor of the AI Act amendments.",
        url="https://example.com/article3",
        source="Reuters",
        published=datetime(2026, 3, 19, 8, 0),
    ),
]
