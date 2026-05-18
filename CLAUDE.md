# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Daily Tracker Suite** - A Python application with two independent trackers:
1. **YouTube Tracker** - Fetches YouTube video uploads from specified channels daily
2. **News Tracker** - Fetches top news headlines every 6 hours using GNews API

Each tracker uses its own Notion database.

**Version:** 1.0.0

## Development Commands

```bash
# Run YouTube tracker
python main.py

# Run News tracker
python main_news.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

```
main.py / main_news.py          Entry points
    |                              |
    ▼                              ▼
src/trackers/                   src/trackers/
├── youtube.py                  ├── news.py
└── base.py                     └── base.py
    |
    ▼
src/clients/
├── youtube.py                  src/clients/news.py
└── (API clients)
    |
    ▼
src/core/
├── notion.py                   (Notion API integration)
├── storage.py                  (JSON persistence)
├── config.py                   (environment variables)
└── firebase.py                 (optional Firebase integration)
```

- **main.py** - YouTube tracker entry point using `YouTubeTracker.run()`
- **main_news.py** - News tracker entry point using `NewsTracker.run()`
- **src/trackers/base.py** - Abstract `BaseTracker` class with shared orchestration logic
- **src/trackers/youtube.py** - `YouTubeTracker` extending BaseTracker
- **src/trackers/news.py** - `NewsTracker` extending BaseTracker
- **src/clients/youtube.py** - YouTube API client with `fetch_all_today_uploads()`
- **src/clients/news.py** - GNews API client with `fetch_latest_news()`
- **src/core/notion.py** - Notion API integration with `add_entry()`, `get_existing_ids()`
- **src/core/storage.py** - Generic JSON persistence with deduplication
- **src/core/config.py** - Centralized environment variable configuration
- **data/videos.json** - Stored YouTube video metadata (gitignored, local cache)
- **data/news.json** - Stored news article metadata (gitignored, local cache)
- **logs/tracker.log** - YouTube tracker log output (gitignored)
- **logs/news-tracker.log** - News tracker log output (gitignored)
- **.env** - Environment configuration (API keys, channel IDs, Notion credentials)
- **.github/workflows/youtube-tracker.yml** - Daily at 00:00 UTC
- **.github/workflows/news-tracker.yml** - Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)

## Configuration

Required environment variables (see `.env.example`):
- `YOUTUBE_API_KEY` - Google YouTube Data API v3 key
- `YOUTUBE_CHANNEL_IDS` - Comma-separated list of channel IDs
- `NOTION_API_KEY` - Notion integration key
- `NOTION_DATABASE_ID` - YouTube Notion database ID
- `NOTION_NEWS_DATABASE_ID` - News Notion database ID
- `NEWS_API_KEY` - GNews API key (for news tracker)
- `NEWS_TOPICS` - Optional: Comma-separated news topics (e.g., "technology,science")
- `NEWS_KEYWORDS` - Optional: Comma-separated search keywords (takes precedence over topics)
- `NEWS_EXCLUDE` - Optional: Comma-separated terms to exclude from results
- `LOG_LEVEL` - Optional: Logging level (default: INFO)
- `FIREBASE_CREDENTIALS_PATH` - Optional: Path to Firebase service account JSON (enables Firebase storage)

## Notes

**Note:** `data/videos.json`, `data/news.json`, and `logs/*.log` are gitignored. These are local runtime caches that should not be committed.

**How History Works:** GitHub Actions are stateless - deduplication happens via Notion database queries (`get_existing_ids()`). Each run checks the current Notion database before adding items. Local JSON files are created fresh each run if they don't exist.

- YouTube tracker uses `NOTION_DATABASE_ID`
- News tracker uses `NOTION_NEWS_DATABASE_ID`
- Videos are categorized as "video" or "short" based on duration (< 4 min = short, ≥ 4 min = video)
- News articles use "news" category
- News tracker requires a GNews API key (free tier available at gnews.dev)
- GitHub Actions need `NEWS_API_KEY` and `NEWS_TOPICS` secrets configured
- Adding new tracker types: extend `BaseTracker` and implement `fetch_items()` and `get_category()`