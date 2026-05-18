from datetime import datetime, timezone
from googleapiclient.discovery import build
from ..core.config import YOUTUBE_API_KEY


def get_youtube_client():
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY not found in environment variables.")
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def parse_duration(duration_str):
    """Parse ISO 8601 duration string to seconds.

    Args:
        duration_str: Duration in ISO 8601 format (e.g., PT1M30S, PT45S, PT5M)

    Returns:
        Duration in seconds as integer
    """
    import re
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0
    hours, minutes, seconds = match.groups()
    return int(hours or 0) * 3600 + int(minutes or 0) * 60 + int(seconds or 0)


def fetch_all_today_uploads(channel_id):
    """Fetch all videos from today with duration info.

    Fetches videos from search endpoint, then gets duration from videos endpoint.
    Categorization: < 4 min = short, >= 4 min = video
    """
    youtube = get_youtube_client()

    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        publishedAfter=today_start,
        maxResults=10,
        order="date",
        type="video"
    )
    response = request.execute()

    videos = []
    video_ids = []

    for item in response.get('items', []):
        video_id = item['id']['videoId']
        video_ids.append(video_id)
        videos.append({
            "title": item['snippet']['title'],
            "description": item['snippet'].get('description') or "",
            "url": f'https://www.youtube.com/watch?v={video_id}',
            "published_at": item['snippet']['publishedAt'],
            "channel": item['snippet'].get('channelTitle'),
            "video_id": video_id,
            "tags": item['snippet'].get('tags', [])
        })

    if video_ids:
        video_request = youtube.videos().list(
            part="contentDetails",
            id=",".join(video_ids)
        )
        video_response = video_request.execute()

        for video_info in video_response.get('items', []):
            vid = video_info['id']
            duration_str = video_info['contentDetails'].get('duration', 'PT0S')
            duration_seconds = parse_duration(duration_str)

            for video in videos:
                if video['video_id'] == vid:
                    video['duration_seconds'] = duration_seconds
                    video['category'] = "short" if duration_seconds < 240 else "video"
                    break

    return videos