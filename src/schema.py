from utils.formatDate import parse_gnews_date_to_iso

def build_youtube_video_schema(item, fetch_by, fetch_value):
    snippet = item.get('snippet', {})
    video = {
        "video_id": item['id']['videoId'],
        "title": snippet.get('title'),
        "channel": snippet.get('channelTitle'),
        "channel_id": snippet.get('channelId'),
        "description": snippet.get('description'),
        "published_at": snippet.get('publishedAt'),
        "live_broadcast_content": snippet.get('liveBroadcastContent'),
        "link": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
        "thumbnail": snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
        "fetch_by": fetch_by,
        "fetch_value": fetch_value
    }
    return video

def build_youtube_notion_properties(video):
    properties = {
        "title": {"title": [{"text": {"content": video['title']}}]},
        "video_id": {"rich_text": [{"text": {"content": video['video_id']}}]},
        "channel": {"select": {"name": video['channel']}},
        "channel_id": {"rich_text": [{"text": {"content": video['channel_id']}}]},
        "description": {"rich_text": [{"text": {"content": video['description']}}]},
        "published_at": {"date": {"start": video['published_at']}},
        "live_broadcast_content": {"select": {"name": video['live_broadcast_content']}},
        "link": {"url": f"https://www.youtube.com/watch?v={video['video_id']}"},
        "thumbnail": {
            "files": [{
                "type": "external",
                "name": "Thumbnail Image",
                "external": {"url": video["thumbnail"]}
            }]
        },
        "fetch_by": {"select": {"name": video['fetch_by']}},
        "fetch_value": {"select": {"name": video['fetch_value']}},
    }
    return properties

def build_news_article_schema(item, fetch_by, fetch_value):
    article = {
        "title": item.get('title'),
        "description": item.get('description'),
        "url": item.get('url'),
        "published_at": item.get('published date'),
        "publisher_title": item.get('publisher').get('title'),
        "publisher_url": item.get('publisher').get('href'),
        "fetch_by": fetch_by,
        "fetch_value": fetch_value
    }
    return article

def build_news_notion_properties(article):
    properties = {
        "title": {"title": [{"text": {"content": article.get('title')}}]},
        "description": {"rich_text": [{"text": {"content": article['description']}}]},
        "published_at": {"date": {"start": parse_gnews_date_to_iso(article['published_at'])}},
        "url": {"url": article['url']},
        "publisher_title": {"rich_text": [{"text": {"content": article['publisher_title']}}]},
        "publisher_url": {"url": article['publisher_url']},
        "fetch_by": {"select": {"name": article['fetch_by']}},
        "fetch_value": {"select": {"name": article['fetch_value']}},
    }
    return properties