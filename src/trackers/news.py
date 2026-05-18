from .base import BaseTracker
from ..clients.news import fetch_latest_news
from ..core.config import NOTION_NEWS_DATABASE_ID, FIREBASE_CREDENTIALS_PATH
from ..core.notion import get_existing_ids, add_entry
from ..core.storage import save_to_json
from ..core import firebase


class NewsTracker(BaseTracker):
    """Tracker for news articles."""

    def __init__(self):
        super().__init__(
            database_id=NOTION_NEWS_DATABASE_ID,
            data_path="data/news.json",
            log_path="logs/news-tracker.log"
        )

    def fetch_items(self):
        """Fetch news articles from configured topics."""
        return fetch_latest_news()

    def get_category(self, item):
        """Return 'news' for all articles."""
        return "news"

    def run(self):
        """Run the tracker: check existing, fetch new, upload to Notion."""
        print("Checking Notion database for existing items...")
        existing_ids = get_existing_ids(self.database_id, id_property="Article_Id")
        print(f"Found {len(existing_ids)} existing items in Notion")

        newly_added = []

        items = self.fetch_items()
        for item in items:
            item_id = item.get('article_id')
            if item_id and item_id not in existing_ids:
                newly_added.append(item)

        if newly_added:
            print(f"Adding {len(newly_added)} new items to Notion database...")
            added_items = []
            for item in newly_added:
                category = self.get_category(item)
                result = add_entry(
                    database_id=self.database_id,
                    title=item.get("title", ""),
                    description=item.get("description", ""),
                    url=item.get("url", ""),
                    category=category,
                    channel=item.get("channel", ""),
                    published_at=item.get("published_at", ""),
                    video_id=item.get("article_id"),
                    image=item.get("image", ""),
                    channel_url=item.get("channel_url", ""),
                    is_news_db=True
                )
                if result:
                    added_items.append(item)
                    # Also add to Firebase (only if credentials file exists)
                    if FIREBASE_CREDENTIALS_PATH:
                        try:
                            fb_data = {
                                "title": item.get("title", ""),
                                "description": item.get("description", ""),
                                "url": item.get("url", ""),
                                "category": category,
                                "channel": item.get("channel", ""),
                                "published_at": item.get("published_at", ""),
                                "article_id": item.get("article_id"),
                                "read": False,
                            }
                            if item.get("image"):
                                fb_data["image"] = item.get("image")
                            if item.get("channel_url"):
                                fb_data["channel_url"] = item.get("channel_url")
                            firebase.add_entry("news_articles", fb_data, item.get("article_id"))
                        except FileNotFoundError as e:
                            print(f"Firebase skipped: {e}")
                        except Exception as e:
                            print(f"Firebase write failed: {e}")

            if added_items:
                save_to_json(added_items, self.data_path, self.log_path)
        else:
            print("No new items found today.")