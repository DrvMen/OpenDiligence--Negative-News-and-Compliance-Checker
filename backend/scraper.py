# scraper.py
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

from mca_live import fetch_mca_live  # NEW

NEGATIVE_KEYWORDS = [
    "fraud", "scam", "corruption", "arrest", "investigation", "lawsuit",
    "case", "penalty", "fine", "charged", "illegal", "ban", "bankruptcy",
    "crime", "money laundering", "raid", "CBI", "ED", "court", "guilty",
    "sebi", "rbi", "cbi", "enforcement", "strike off", "defaulter", "insolvency",
    "nclt", "attachment", "prosecution", "penalised", "penalty"
]


def is_negative_article(title, desc):
    text = f"{title} {desc}".lower()
    if any(word in text for word in NEGATIVE_KEYWORDS):
        return True
    polarity = TextBlob(text).sentiment.polarity
    return polarity < -0.2

# ---- Google News ----


def fetch_google_news(query):
    url = f"https://news.google.com/rss/search?q={query}+when:7d&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "xml")

        articles = []
        for item in soup.find_all("item"):
            title = item.title.text if item.title else ""
            link = item.link.text if item.link else ""
            desc = item.description.text if item.description else ""
            flag = is_negative_article(title, desc)

            articles.append({
                "source": "Google News",
                "title": title,
                "link": link,
                "description": desc,
                "pubDate": item.pubDate.text if item.pubDate else "",
                "isNegative": flag
            })
        return articles
    except Exception as e:
        print("❌ Google News error:", e)
        return []

# ---- SEBI ----


def fetch_sebi_notices(query):
    url = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3"
    items = []
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Try multiple selectors for robustness
        candidates = [".newsList li a", ".tableContent a", "a"]
        seen = set()
        for sel in candidates:
            for a in soup.select(sel)[:80]:
                title = (a.text or "").strip()
                href = a.get("href") or ""
                if not title or not href:
                    continue
                if query.lower() not in title.lower():
                    continue
                if href.startswith("/"):
                    href = "https://www.sebi.gov.in" + href
                if (title, href) in seen:
                    continue
                seen.add((title, href))
                items.append({
                    "source": "SEBI",
                    "title": title,
                    "link": href,
                    "description": "SEBI order/press note",
                    "pubDate": "",
                    "isNegative": True
                })
        return items
    except Exception as e:
        print("❌ SEBI scrape error:", e)
        return []

# ---- CBI ----


def fetch_cbi_press(query):
    url = "https://cbi.gov.in/press-releases"
    items = []
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.select(".views-row h3 a, .views-row a")[:80]:
            title = (a.text or "").strip()
            href = a.get("href") or ""
            if not title or not href:
                continue
            if query.lower() not in title.lower():
                continue
            if href.startswith("/"):
                href = "https://cbi.gov.in" + href
            items.append({
                "source": "CBI",
                "title": title,
                "link": href,
                "description": "CBI press release",
                "pubDate": "",
                "isNegative": True
            })
        return items
    except Exception as e:
        print("❌ CBI scrape error:", e)
        return []

# ---- Unified ----


def fetch_all_sources(query):
    results = []
    try:
        results.extend(fetch_google_news(query))
    except Exception as e:
        print("Google News error:", e)

    try:
        results.extend(fetch_sebi_notices(query))
    except Exception as e:
        print("SEBI scrape error:", e)

    try:
        results.extend(fetch_cbi_press(query))
    except Exception as e:
        print("CBI scrape error:", e)

    # MCA LIVE (human-in-the-loop)
    try:
        results.extend(fetch_mca_live(query))
    except Exception as e:
        print("MCA live error:", e)

    return results
