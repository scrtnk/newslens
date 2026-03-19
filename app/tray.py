# app/tray.py
from typing import Optional
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QThread
from backend.models.schemas import TopicEnum
from app.briefing_window import BriefingWindow
from app.worker import BriefingWorker

TOPIC_LABELS = {
    TopicEnum.ai:          "🤖 AI",
    TopicEnum.stocks:      "📈 หุ้น",
    TopicEnum.geopolitics: "🌍 Geopolitics",
    TopicEnum.technology:  "💻 เทคโนโลยี",
    TopicEnum.business:    "💼 ธุรกิจ",
    TopicEnum.energy:      "⚡ พลังงาน",
    TopicEnum.crypto:      "🪙 คริปโต",
    TopicEnum.economy:     "🏦 เศรษฐกิจโลก",
}


class TrayApp(QSystemTrayIcon):
    def __init__(self, icon: QIcon, parent=None):
        super().__init__(icon, parent)
        self.window = BriefingWindow()
        self._thread: Optional[QThread] = None
        self._worker: Optional[BriefingWorker] = None
        self._build_menu()
        self.setToolTip("AI News Briefing")

    def _build_menu(self) -> None:
        menu = QMenu()
        for topic, label in TOPIC_LABELS.items():
            action = QAction(label, self)
            action.triggered.connect(lambda checked, t=topic: self._fetch(t))
            menu.addAction(action)
        menu.addSeparator()
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)
        self.setContextMenu(menu)

    def _fetch(self, topic: TopicEnum) -> None:
        # Ignore if already fetching
        if self._thread and self._thread.isRunning():
            return

        self.window.show_loading(topic.value)

        self._thread = QThread()
        self._worker = BriefingWorker(topic)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.briefing_ready.connect(self.window.show_briefing)
        self._worker.briefing_ready.connect(self._thread.quit)
        self._worker.error_occurred.connect(self.window.show_error)
        self._worker.error_occurred.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)   # prevent memory leak
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()
