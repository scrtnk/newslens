# app/html_renderer.py
from backend.models.schemas import BriefingResponse

TOPIC_LABELS = {
    "ai": "🤖 AI",
    "stocks": "📈 หุ้น",
    "geopolitics": "🌍 Geopolitics",
    "technology": "💻 เทคโนโลยี",
    "business": "💼 ธุรกิจ",
    "energy": "⚡ พลังงาน",
    "crypto": "🪙 คริปโต",
    "economy": "🏦 เศรษฐกิจโลก",
}

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
    background: #1c1c1e; color: #f2f2f7;
    padding: 20px; font-size: 14px; line-height: 1.6;
}
h1 { font-size: 20px; font-weight: 700; margin-bottom: 4px; color: #ffffff; }
.meta { font-size: 11px; color: #8e8e93; margin-bottom: 20px; }
.story { background: #2c2c2e; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
.story h2 { font-size: 15px; font-weight: 600; color: #ffffff; margin-bottom: 8px; }
.story p { color: #d1d1d6; margin-bottom: 8px; font-size: 13px; }
.matters { background: #1c3a5e; border-left: 3px solid #0a84ff;
           padding: 8px 12px; border-radius: 0 8px 8px 0; margin-bottom: 8px; }
.matters span { color: #64b5f6; font-size: 12px; font-weight: 600; }
.matters p { color: #c9e0f7; font-size: 13px; margin: 0; }
.source a { font-size: 11px; color: #0a84ff; text-decoration: none; }
.section { background: #2c2c2e; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
.section h3 { font-size: 13px; font-weight: 600; color: #8e8e93;
              text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }
.tag { display: inline-block; background: #3a3a3c; color: #d1d1d6;
       padding: 4px 10px; border-radius: 20px; font-size: 12px; margin: 3px; }
.watch-item { color: #d1d1d6; font-size: 13px; padding: 4px 0;
              border-bottom: 1px solid #3a3a3c; }
.watch-item:last-child { border-bottom: none; }
.two-col { display: flex; gap: 12px; }
.two-col > div { flex: 1; }
"""


def _esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                .replace('"', "&quot;").replace("'", "&#39;"))


def render_briefing(briefing: BriefingResponse) -> str:
    topic_label = TOPIC_LABELS.get(briefing.topic, briefing.topic)
    date_str = briefing.generated_at.strftime("%d %b %Y, %H:%M UTC")

    stories_html = ""
    for i, story in enumerate(briefing.stories, 1):
        stories_html += f"""
<div class="story">
  <h2>{i}. {_esc(story.headline)}</h2>
  <p>{_esc(story.summary)}</p>
  <div class="matters">
    <span>ทำไมเรื่องนี้สำคัญ</span>
    <p>{_esc(story.why_it_matters)}</p>
  </div>
  <p class="source"><a href="{story.source_url}">อ่านต้นฉบับ ↗</a></p>
</div>"""

    terms_html = "".join(f'<span class="tag">{_esc(t)}</span>' for t in briefing.key_terms)
    watch_html = "".join(f'<div class="watch-item">→ {_esc(w)}</div>' for w in briefing.things_to_watch)

    return f"""<!DOCTYPE html>
<html lang="th">
<head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>
<h1>สรุปข่าว: {topic_label}</h1>
<div class="meta">Generated {date_str}</div>
{stories_html}
<div class="two-col">
  <div class="section">
    <h3>📚 คำ/เทคนิคที่ควรรู้</h3>
    {terms_html}
  </div>
  <div class="section">
    <h3>🔭 มุมที่ควรติดตาม</h3>
    {watch_html}
  </div>
</div>
</body></html>"""
