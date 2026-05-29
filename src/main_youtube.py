from config import YOUTUBE_API_KEY, YOUTUBE_CHANNEL_IDS, YOUTUBE_QUERIES, YOUTUBE_VIDEO_IDS, YOUTUBE_LIMIT
from config import NOTION_API_KEY, NOTION_YOUTUBE_DATABASE_ID

from providers import YouTubeProvider
from databases import NotionDatabase
from schema import build_youtube_notion_properties

import random
import time

if __name__ == "__main__":
    youtube = YouTubeProvider(
        api_key=YOUTUBE_API_KEY,
        channel_id=YOUTUBE_CHANNEL_IDS,
        queries=YOUTUBE_QUERIES,
        video_id=YOUTUBE_VIDEO_IDS,
        limit=YOUTUBE_LIMIT
    )
    notion = NotionDatabase(
        api_key=NOTION_API_KEY, 
        database_id=NOTION_YOUTUBE_DATABASE_ID
    )

    print("pass the install youtube and notion")

    videos = []
    
    videos.extend(youtube.fetch_by_queries())
    print("fetch by query complete.")
    time.sleep(random.uniform(1, 10))
    
    videos.extend(youtube.fetch_by_video_ids())
    print("fetch by video id complete.")
    time.sleep(random.uniform(1, 10))

    videos.extend(youtube.fetch_by_channel_ids())
    print("fetch by channel id complete.")    
    
    for video in videos:
        is_exsits = notion.check_property_value(
            property_name="video_id", 
            target_value=video["video_id"], 
            property_type="rich_text"
        )

        if not is_exsits:
            properties = build_youtube_notion_properties(video)
            respone = notion.add_row(properties=properties)
            print(f"{respone} {video['title']}")
        else:
            print('already exist in the notion.')