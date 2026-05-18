import requests
from .config import NOTION_API_KEY


def get_headers():
    return {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def get_existing_ids(database_id, id_property="Video_id"):
    """Query Notion database and return set of existing IDs.

    Args:
        database_id: Notion database ID
        id_property: Property name for ID (Video_id for YouTube, Article_Id for News)
    """
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    existing_ids = set()
    headers = get_headers()

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


def add_entry(database_id, title, description, url, category, channel, published_at, video_id, tags="", image="", channel_url="", is_news_db=False):
    """Add an entry to Notion database.

    Args:
        is_news_db: If True, uses Article_Id/Source/Publish_At schema for News database
    """
    notion_url = "https://api.notion.com/v1/pages"
    headers = get_headers()

    if is_news_db:
        # News database schema
        properties = {
            "Title": {"title": [{"text": {"content": title}}]},
            "Description": {"rich_text": [{"text": {"content": description}}]},
            "URL": {"url": url},
            "Source": {"select": {"name": channel}},
            "Publish_At": {"date": {"start": published_at}},
            "Article_Id": {"rich_text": [{"text": {"content": video_id}}]}
        }
        if channel_url:
            properties["Source_URL"] = {"rich_text": [{"text": {"content": channel_url}}]}
    else:
        # YouTube database schema
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
            properties["Tags"] = {"multi_select": [{"name": tag} for tag in tag_list]}
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