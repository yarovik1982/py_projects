import feedparser
import requests
from bs4 import BeautifulSoup
from config import RSS_URL, DEFAULT_IMAGE

def get_latest_articles():
    feed = feedparser.parse(RSS_URL)
    articles = []
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = BeautifulSoup(entry.summary, "html.parser").text.strip()

        # Попробуем найти изображение
        image_url = None
        soup = BeautifulSoup(entry.summary, "html.parser")
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            image_url = img_tag["src"]
        else:
            image_url = DEFAULT_IMAGE

        articles.append({
            "title": title,
            "link": link,
            "summary": summary,
            "image": image_url
        })
    return articles
