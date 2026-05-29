import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY') or None
YOUTUBE_CHANNEL_IDS = os.getenv('YOUTUBE_CHANNEL_IDS') or None
YOUTUBE_QUERIES = os.getenv('YOUTUBE_QUERIES') or None
YOUTUBE_VIDEO_IDS = os.getenv('YOUTUBE_VIDEO_IDS') or None
YOUTUBE_LIMIT = os.getenv('YOUTUBE_LIMIT') or 10

NOTION_API_KEY= os.getenv('NOTION_API_KEY') or None
NOTION_YOUTUBE_DATABASE_ID= os.getenv('NOTION_YOUTUBE_DATABASE_ID') or None