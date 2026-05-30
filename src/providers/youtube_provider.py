import random
import time
import logging

from googleapiclient.discovery import build
from schema import build_youtube_video_schema

class YouTubeProvider:
    def __init__(self, api_key, channel_id, queries, video_id, limit):
        if not api_key:
            raise ConnectionError("Youtube Provider: Require api key")

        self.api_key = api_key
        self.queries = queries.split(',') if queries else []
        self.video_ids = video_id.split(',') if video_id else []
        self.channel_ids = channel_id.split(',') if channel_id else []
        self.limit = limit

        self.youtube_client = build('youtube', 'v3', developerKey=self.api_key)

        print("Initialized youtube provider.")

    def fetch_by_queries(self):
        if not self.youtube_client:
            raise RuntimeError("YouTube client is not initialized. Please call the setup method first.")
        if not self.queries:
            logging.warning("Queries list is empty. Skipping the process.")
            return[]

        videos = []
        seen_ids = set()

        for query in self.queries:
            try:
                request = self.youtube_client.search().list(
                    part='snippet',
                    q=query.strip(),
                    type='video',
                    maxResults=self.limit
                )
                response = request.execute()
                print(f"Fetched from query '{query.strip()}': {len(response.get('items', []))} videos")
            except Exception as e:
                logging.warning(f"Failed to fetch video by queries '{query}': {e}")
                continue

            for item in response.get('items', []):
                video_id = item['id']['videoId']
                if video_id not in seen_ids:
                    seen_ids.add(video_id)
                    videos.append(build_youtube_video_schema(item, fetch_by="query"))
            
            time.sleep(random.uniform(1, 5))
        
        return videos

    def fetch_by_video_ids(self):
        if not self.youtube_client:
            raise RuntimeError("YouTube client is not initialized. Please call the setup method first.")
        if not self.video_ids:
            logging.warning("Video ids list is empty. Skipping the process.")
            return[]

        videos = []
        seen_ids = set()

        for vid in self.video_ids:
            try:
                request = self.youtube_client.videos().list(
                    part='snippet',
                    id=vid.strip()
                )
                response = request.execute()
                print(f"Fetched video id '{vid.strip()}': {len(response.get('items', []))} videos")
            except Exception as e:
                logging.warning(f"Failed to fetch video by video id '{vid}': {e}")
                continue
 

            items = response.get('items', [])
            for item in items:
                item['id'] = {'videoId': item['id']}
                video_id = item['id']['videoId']
                if video_id not in seen_ids:
                    seen_ids.add(video_id)
                    videos.append(build_youtube_video_schema(item, fetch_by="video_id"))
            
            time.sleep(random.uniform(1, 5))
        
        return videos

    def fetch_by_channel_ids(self):
        if not self.youtube_client:
            raise RuntimeError("YouTube client is not initialized. Please call the setup method first.")
        if not self.channel_ids:
            logging.warning("Channel ids list is empty. Skipping the process.")
            return[]
        
        videos = []
        seen_ids = set()

        for cid in self.channel_ids:
            try:
                request = self.youtube_client.search().list(
                    part='snippet',
                    channelId=cid.strip(),
                    type='video',
                    maxResults=self.limit,
                    order='date'
                )
                response = request.execute()
                print(f"Fetched from channel {cid.strip()}: {len(response.get('items', []))} videos")
                
            except Exception as e:
                logging.warning(f"Failed to fetch video by channel id '{cid}': {e}")
                continue 

            for item in response.get('items', []):
                video_id = item['id']['videoId']
                if video_id not in seen_ids:
                    seen_ids.add(video_id)
                    videos.append(build_youtube_video_schema(item, fetch_by="channel_id"))

            time.sleep(random.uniform(1, 5))
        
        return videos
