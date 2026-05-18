import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_IDS = [cid.strip() for cid in os.getenv("YOUTUBE_CHANNEL_IDS", "").split(",") if cid.strip()]

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_NEWS_DATABASE_ID = os.getenv("NOTION_NEWS_DATABASE_ID")

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_TOPICS = [t.strip() for t in os.getenv("NEWS_TOPICS", "").split(",") if t.strip()]
NEWS_KEYWORDS = [k.strip() for k in os.getenv("NEWS_KEYWORDS", "").split(",") if k.strip()]
NEWS_EXCLUDE = [e.strip() for e in os.getenv("NEWS_EXCLUDE", "").split(",") if e.strip()]

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")