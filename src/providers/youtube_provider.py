from googleapiclient.discovery import build
from schema import build_youtube_video_schema

class YouTubeProvider:
    def __init__(self, api_key, channel_id, queries, video_id, limit):
        if not api_key:
            raise ConnectionError("Youtube Provider: Require api key")

        self.api_key = api_key
        self.channel_id = channel_id
        self.queries = queries.split(',') if queries else []
        self.video_ids = video_id.split(',') if video_id else []
        self.channel_ids = channel_id.split(',') if channel_id else []
        self.limit = limit

        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def fetch_by_queries(self):
        if not self.youtube:
            return []

        videos = []
        seen_ids = set()

        for query in self.queries:
            try:
                request = self.youtube.search().list(
                    part='snippet',
                    q=query.strip(),
                    type='video',
                    maxResults=self.limit
                )
                response = request.execute()
                print(f"Fetched from query '{query.strip()}': {len(response.get('items', []))} videos")
            except Exception as e:
                raise ValueError(f"error fetch the video by query: {e}") 

            for item in response.get('items', []):
                video_id = item['id']['videoId']
                if video_id not in seen_ids:
                    seen_ids.add(video_id)
                    videos.append(build_youtube_video_schema(item, fetch_by="query"))

        return videos

    def fetch_by_video_ids(self):
        if not self.youtube or not self.video_ids:
            return []

        videos = []
        seen_ids = set()

        for vid in self.video_ids:
            try:
                request = self.youtube.videos().list(
                    part='snippet',
                    id=vid.strip()
                )
                response = request.execute()
                print(f"Fetched video id '{vid.strip()}': {len(response.get('items', []))} videos")
            except Exception as e:
                raise ValueError(f"error fetch the video by video id: {e}") 

            items = response.get('items', [])
            for item in items:
                item['id'] = {'videoId': item['id']}
                video_id = item['id']['videoId']
                if video_id not in seen_ids:
                    seen_ids.add(video_id)
                    videos.append(build_youtube_video_schema(item, fetch_by="video_id"))

        return videos

    def fetch_by_channel_ids(self):
        if not self.youtube or not self.channel_ids:
            return []

        videos = []
        seen_ids = set()

        for cid in self.channel_ids:
            try:
                request = self.youtube.search().list(
                    part='snippet',
                    channelId=cid.strip(),
                    type='video',
                    maxResults=self.limit,
                    order='date'
                )
                response = request.execute()
                print(f"Fetched from channel {cid.strip()}: {len(response.get('items', []))} videos")
            except Exception as e:
                raise ValueError(f"error fetch the video by channel id: {e}") 

            for item in response.get('items', []):
                video_id = item['id']['videoId']
                if video_id not in seen_ids:
                    seen_ids.add(video_id)
                    videos.append(build_youtube_video_schema(item, fetch_by="channel_id"))

        return videos
