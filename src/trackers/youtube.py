from .base import BaseTracker
from ..clients.youtube import fetch_all_today_uploads
from ..core.config import YOUTUBE_CHANNEL_IDS, NOTION_DATABASE_ID, FIREBASE_CREDENTIALS_PATH
from ..core.notion import get_existing_ids, add_entry
from ..core.storage import save_to_json
from ..core import firebase


class YouTubeTracker(BaseTracker):
    """Tracker for YouTube videos and shorts."""

    def __init__(self):
        super().__init__(
            database_id=NOTION_DATABASE_ID,
            data_path="data/videos.json",
            log_path="logs/tracker.log"
        )

    def fetch_items(self):
        """Fetch all uploads (videos and shorts) from all configured channels."""
        all_items = []
        for channel_id in YOUTUBE_CHANNEL_IDS:
            try:
                items = fetch_all_today_uploads(channel_id)
                all_items.extend(items)
            except Exception as e:
                print(f"Error checking channel {channel_id}: {e}")
        return all_items

    def get_category(self, item):
        """Get category based on duration (< 4 min = short, >= 4 min = video)."""
        return item.get("category", "video")

    def run(self):
        """Run the tracker: check existing, fetch new, upload to Notion."""
        print("Checking Notion database for existing items...")
        existing_ids = get_existing_ids(self.database_id)
        print(f"Found {len(existing_ids)} existing items in Notion")

        newly_added = []

        items = self.fetch_items()
        for item in items:
            item_id = item.get('video_id') or item.get('article_id')
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
                    video_id=item.get("video_id") or item.get("article_id"),
                    tags=item.get("tags", ""),
                    image=item.get("image", "")
                )
                if result:
                    added_items.append(item)
                    # Also add to Firebase (only if credentials file exists)
                    if FIREBASE_CREDENTIALS_PATH:
                        try:
                            tags = item.get("tags", [])
                            if isinstance(tags, str):
                                tags = [t.strip() for t in tags.split(",") if t.strip()]
                            fb_data = {
                                "title": item.get("title", ""),
                                "description": item.get("description", ""),
                                "url": item.get("url", ""),
                                "category": category,
                                "channel": item.get("channel", ""),
                                "published_at": item.get("published_at", ""),
                                "video_id": item.get("video_id"),
                                "tags": tags,
                                "read": False,
                            }
                            if item.get("image"):
                                fb_data["image"] = item.get("image")
                            if item.get("channel_url"):
                                fb_data["channel_url"] = item.get("channel_url")
                            firebase.add_entry("youtube_videos", fb_data, item.get("video_id"))
                        except FileNotFoundError as e:
                            print(f"Firebase skipped: {e}")
                        except Exception as e:
                            print(f"Firebase write failed: {e}")

            if added_items:
                save_to_json(added_items, self.data_path, self.log_path)
        else:
            print("No new items found today.")