# app/briefing_window.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from backend.models.schemas import BriefingResponse
from app.html_renderer import render_briefing


class BriefingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI News Briefing")
        self.setMinimumSize(520, 680)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 8)

        self.browser = QTextBrowser()
        self.browser.setOpenLinks(False)
        self.browser.anchorClicked.connect(self._open_link)
        self.browser.setStyleSheet("background: #1c1c1e; border: none;")
        layout.addWidget(self.browser)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(80)
        close_btn.clicked.connect(self.hide)
        btn_row.addWidget(close_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def show_briefing(self, briefing: BriefingResponse) -> None:
        self.setWindowTitle(f"Briefing: {briefing.topic.upper()}")
        html = render_briefing(briefing)
        self.browser.setHtml(html)
        self.show()
        self.raise_()
        self.activateWindow()

    def show_loading(self, topic: str) -> None:
        self.setWindowTitle(f"Loading {topic}...")
        self.browser.setHtml(
            "<body style='background:#1c1c1e;color:#f2f2f7;"
            "font-family:-apple-system;padding:40px;text-align:center'>"
            "<p style='font-size:18px'>กำลังดึงและสรุปข่าว...</p>"
            "<p style='color:#8e8e93'>อาจใช้เวลา 10–20 วินาที</p></body>"
        )
        self.show()
        self.raise_()

    def show_error(self, message: str) -> None:
        self.setWindowTitle("Error")
        self.browser.setHtml(
            f"<body style='background:#1c1c1e;color:#ff453a;"
            f"font-family:-apple-system;padding:40px'>"
            f"<p style='font-size:16px'>เกิดข้อผิดพลาด</p>"
            f"<p style='color:#d1d1d6'>{message}</p></body>"
        )
        self.show()

    def _open_link(self, url: QUrl) -> None:
        QDesktopServices.openUrl(url)
