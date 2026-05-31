import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY') or None
YOUTUBE_CHANNEL_IDS = os.getenv('YOUTUBE_CHANNEL_IDS') or None
YOUTUBE_QUERIES = os.getenv('YOUTUBE_QUERIES') or None
YOUTUBE_VIDEO_IDS = os.getenv('YOUTUBE_VIDEO_IDS') or None
YOUTUBE_LIMIT = os.getenv('YOUTUBE_LIMIT') or 10
YOUTUBE_FROM_DATE = os.getenv('YOUTUBE_FROM_DATE') or 1

GNEWS_TOPICS = os.getenv('GNEWS_TOPICS') or None
GNEWS_KEYWORDS = os.getenv('GNEWS_KEYWORDS') or None
GNEWS_SITES = os.getenv('GNEWS_SITES') or None
GNEWS_LOCATIONS = os.getenv('GNEWS_LOCATIONS') or None
GNEWS_LIMIT = os.getenv('GNEWS_LIMIT') or 10
GNEWS_FROM_DATE = os.getenv('GNEWS_FROM_DATE') or 1

NOTION_API_KEY= os.getenv('NOTION_API_KEY') or None
NOTION_YOUTUBE_DATABASE_ID= os.getenv('NOTION_YOUTUBE_DATABASE_ID') or None
NOTION_NEWS_DATABASE_ID = os.getenv('NOTION_NEWS_DATABASE_ID') or None