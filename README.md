# NewsLens

AI-powered macOS menu bar app. Click a topic → get a curated news briefing: top stories, why they matter, key terms, and what to watch.

## Setup

```bash
cp .env.example .env
# Add your OpenAI API key to .env
pip install -r requirements.txt
```

## Run (development)

```bash
python -m app.main
```

A newspaper icon appears in your menu bar. Right-click to select a topic.

## Build .app

```bash
# Optional: create a proper icon first
sips -s format icns assets/icon.png --out assets/icon.icns

pyinstaller news_briefing.spec --clean
open dist/NewsLens.app
```

## Topics

🤖 AI · 📈 หุ้น · 🌍 Geopolitics · 💻 เทคโนโลยี · 💼 ธุรกิจ · ⚡ พลังงาน · 🪙 คริปโต · 🏦 เศรษฐกิจโลก

## Architecture

```
Menu bar icon (QSystemTrayIcon)
  → click topic → QThread worker
  → RSS fetch → deduplicate → rank → OpenAI GPT-4o-mini
  → HTML briefing popup (QTextBrowser)
```

## Stack

Python 3.9+, PyQt6, feedparser, openai SDK, Pydantic v2, PyInstaller
