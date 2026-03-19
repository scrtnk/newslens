# app/worker.py
from PyQt6.QtCore import QObject, pyqtSignal
from backend.models.schemas import TopicEnum
from backend.news.fetcher import fetch_articles
from backend.news.deduplicator import deduplicate
from backend.news.ranker import rank_articles
from backend.llm.summarizer import summarize
from backend.config import get_settings


class BriefingWorker(QObject):
    briefing_ready = pyqtSignal(object)   # emits BriefingResponse
    error_occurred = pyqtSignal(str)      # emits error message string

    def __init__(self, topic: TopicEnum):
        super().__init__()
        self.topic = topic

    def run(self) -> None:
        try:
            articles = fetch_articles(self.topic)
            if not articles:
                self.error_occurred.emit(f"ไม่พบข่าวสำหรับหัวข้อ: {self.topic.value}")
                return
            articles = deduplicate(articles)
            top = rank_articles(articles, n=get_settings().top_n_articles)
            briefing = summarize(self.topic, top)
            self.briefing_ready.emit(briefing)
        except Exception as e:
            self.error_occurred.emit(str(e))
