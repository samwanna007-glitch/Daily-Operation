from typing import Any

import requests
from .config import NOTION_API_KEY


class NotionClient:
    """Base class for Notion API operations."""

    @staticmethod
    def get_headers():
        return {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    @staticmethod
    def fetch_existing_ids(database_id, id_property):
        """Query Notion database and return set of existing IDs.

        Args:
            database_id: Notion database ID
            id_property: Property name for ID
        """
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        existing_ids = set[Any]()
        headers = NotionClient.get_headers()

        payload = {
            "page_size": 100,
            "sorts": [
                {
                    "timestamp": "created_time",
                    "direction": "descending"
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                for page in data.get("results", []):
                    props = page.get("properties", {})
                    id_prop = props.get(id_property, {})
                    rich_text_list = id_prop.get("rich_text", [])
                    if rich_text_list:
                        item_id = rich_text_list[0].get("text", {}).get("content", "")
                        if item_id:
                            existing_ids.add(item_id)
                return existing_ids
            else:
                print(f"Error fetching from Notion: {response.status_code}")
                return set()
        except Exception as e:
            print(f"Error querying Notion: {e}")
            return set()


class YouTubeNotion(NotionClient):
    """Notion client for YouTube database operations."""

    def get_existing_ids(self, database_id, id_property="Video_id"):
        """Query Notion database and return set of existing IDs.

        Args:
            database_id: Notion database ID
            id_property: Property name for ID (default: Video_id)
        """
        return NotionClient.fetch_existing_ids(database_id, id_property)

    def add_entry(self, database_id, title, description, url, category, channel, published_at, video_id, tags="", image="", channel_url=""):
        """Add an entry to Notion YouTube database.

        Args:
            database_id: Notion database ID
            title: Video title
            description: Video description
            url: Video URL
            category: "video" or "short"
            channel: Channel name
            published_at: Publish date
            video_id: YouTube video ID
            tags: Comma-separated tags
            image: Thumbnail URL
            channel_url: Channel URL
        """
        notion_url = "https://api.notion.com/v1/pages"
        headers = self.get_headers()

        properties = {
            "Title": {"title": [{"text": {"content": title}}]},
            "Description": {"rich_text": [{"text": {"content": description}}]},
            "URL": {"url": url},
            "Category": {"select": {"name": category}},
            "Channel": {"select": {"name": channel}},
            "Publish_At": {"date": {"start": published_at}},
            "Video_id": {"rich_text": [{"text": {"content": video_id}}]}
        }
        if tags:
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            properties["Tags"] = {"multi_select": [{"name": t} for t in tag_list]}
        if image:
            properties["Image"] = {"url": image}
        if channel_url:
            properties["Source_URL"] = {"url": channel_url}

        payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }

        response = requests.post(notion_url, headers=headers, json=payload)

        if response.status_code == 200:
            print(f"Success! '{title}' has been added to Notion.")
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None


class NewsNotion(NotionClient):
    """Notion client for News database operations."""

    def get_existing_ids(self, database_id, id_property="Article_Id"):
        """Query Notion database and return set of existing IDs.

        Args:
            database_id: Notion database ID
            id_property: Property name for ID (default: Article_Id)
        """
        return NotionClient.fetch_existing_ids(database_id, id_property)

    def add_entry(self, database_id, title, description, url, source, published_at, article_id, image="", source_url=""):
        """Add an entry to Notion News database.

        Args:
            database_id: Notion database ID
            title: Article title
            description: Article description
            url: Article URL
            source: Source/publication name
            published_at: Publish date
            article_id: Article ID
            image: Article image URL
            source_url: Source website URL
        """
        notion_url = "https://api.notion.com/v1/pages"
        headers = self.get_headers()

        properties = {
            "Title": {"title": [{"text": {"content": title}}]},
            "Description": {"rich_text": [{"text": {"content": description}}]},
            "URL": {"url": url},
            "Source": {"select": {"name": source}},
            "Publish_At": {"date": {"start": published_at}},
            "Article_Id": {"rich_text": [{"text": {"content": article_id}}]}
        }
        if source_url:
            properties["Source_URL"] = {"url": source_url}
        if image:
            properties["Image_URL"] = {"url": image}

        payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }

        response = requests.post(notion_url, headers=headers, json=payload)

        if response.status_code == 200:
            print(f"Success! '{title}' has been added to Notion.")
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None


# Module-level functions for backward compatibility
def get_headers():
    return NotionClient.get_headers()


def get_existing_ids(database_id, id_property="Video_id"):
    client = YouTubeNotion()
    return client.get_existing_ids(database_id, id_property)


def add_entry(database_id, title, description, url, category, channel, published_at, video_id, tags="", image="", channel_url="", is_news_db=False):
    """Add an entry to Notion database.

    Args:
        is_news_db: If True, uses Article_Id/Source/Publish_At schema for News database
    """
    if is_news_db:
        client = NewsNotion()
        return client.add_entry(database_id, title, description, url, channel, published_at, video_id, image, channel_url)
    else:
        client = YouTubeNotion()
        return client.add_entry(database_id, title, description, url, category, channel, published_at, video_id, tags, image, channel_url)