def build_youtube_video_schema(item, fetch_by):
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
        "fetch_by": fetch_by
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
        "fetch_by": {"select": {"name": video['fetch_by']}}
    }
    return properties