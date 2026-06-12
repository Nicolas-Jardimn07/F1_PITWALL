# ─────────────────────────────────────────────────────────────────────────────
#  NEWS — RSS fetcher (no API key required)
# ─────────────────────────────────────────────────────────────────────────────
import re
import requests
import streamlit as st
from xml.etree import ElementTree as ET

RSS_FEEDS = [
    "https://www.autosport.com/rss/f1/news/",
    "https://www.motorsport.com/rss/f1/news/",
    "https://racer.com/feed/",
]

F1_KEYWORDS = [
    "2026", "f1", "formula 1", "formula one", "grand prix", "gp",
    "verstappen", "hamilton", "norris", "leclerc", "russell", "antonelli",
]


@st.cache_data(ttl=1800, show_spinner=False)  # cache 30 min
def fetch_f1_news() -> list:
    """Fetch F1 news from RSS feeds. Returns list of article dicts."""
    articles = []

    for url in RSS_FEEDS:
        try:
            r = requests.get(url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code != 200:
                continue
            root    = ET.fromstring(r.content)
            channel = root.find("channel")
            if channel is None:
                continue

            for item in channel.findall("item")[:8]:
                title = item.findtext("title", "").strip()
                desc  = item.findtext("description", "").strip()
                link  = item.findtext("link", "").strip()
                pub   = item.findtext("pubDate", "").strip()
                src   = url.split("/")[2].replace("www.", "")

                desc = re.sub(r"<[^>]+>", "", desc)[:200]

                img_url = ""
                enc = item.find("enclosure")
                if enc is not None:
                    img_url = enc.get("url", "")
                if not img_url:
                    media = item.find("{http://search.yahoo.com/mrss/}content")
                    if media is not None:
                        img_url = media.get("url", "")

                if title:
                    articles.append({
                        "title":  title,
                        "desc":   desc,
                        "link":   link,
                        "date":   pub[:25] if pub else "",
                        "source": src,
                        "image":  img_url,
                    })
        except Exception:
            continue

    return articles[:24]


def filter_f1_articles(articles: list) -> list:
    """Keep only articles that mention F1-related keywords."""
    filtered = [
        a for a in articles
        if any(kw in (a["title"] + a["desc"]).lower() for kw in F1_KEYWORDS)
    ]
    return filtered if filtered else articles
