import json
import os
import html
from datetime import datetime


def save_to_json(items, file_path, log_path="logs/tracker.log"):
    """Save items to JSON file with deduplication.

    Args:
        items: List of item dictionaries
        file_path: Path to JSON file
        log_path: Path to log file
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    existing_ids = {v['video_id'] for v in data if 'video_id' in v}
    existing_ids.update({v['article_id'] for v in data if 'article_id' in v})

    new_count = 0
    for item in items:
        item_id = item.get('video_id') or item.get('article_id')
        if item_id and item_id not in existing_ids:
            cleaned_item = {
                "title": html.unescape(item.get("title", "")),
                "description": html.unescape(item.get("description", "")),
                "url": item.get("url", ""),
                "published_at": item.get("published_at", ""),
                "channel": item.get("channel", ""),
                "tags": ", ".join(item.get("tags", [])) if item.get("tags") else ""
            }
            if 'video_id' in item:
                cleaned_item['video_id'] = item.get('video_id')
            if 'article_id' in item:
                cleaned_item['article_id'] = item.get('article_id')

            data.append(cleaned_item)
            new_count += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    if new_count > 0:
        log_save(new_count, log_path)

    return new_count


def log_save(count, log_path="logs/tracker.log"):
    """Log a save operation."""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] Items collected and saved ({count} items)\n")