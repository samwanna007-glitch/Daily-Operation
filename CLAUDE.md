# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Daily Tracker Suite** - A Python application with two content trackers:
- **YouTube Tracker**: Fetches YouTube videos via API and stores metadata in Notion
- **News Tracker**: Fetches news articles via GNews API and stores them in Notion

Both trackers implement deduplication before inserting records.

## Development Commands

```bash
# Run YouTube tracker
cd src && python main_youtube.py

# Run News tracker
cd src && python main_news.py

# Install dependencies
pip install -r requirements.txt

# No test framework configured - manual testing via main scripts
```

## Architecture

```
src/
├── main_youtube.py           Entry point for YouTube tracker
├── main_news.py              Entry point for News tracker
├── config.py                 Centralized environment variables (python-dotenv)
├── schema.py                 Schema builders for Notion property structures
├── providers/
│   ├── youtube_provider.py   YouTube API client (google-api-python-client)
│   └── news_provider.py      GNews API client
└── databases/
    └── notion_database.py    Notion API integration (deduplication + insertion)
```

**src/utils/formatDate.py** - Date formatting utilities for API time filters

### Data Flow

Both trackers follow the same pattern:
1. Entry point initializes provider and NotionDatabase
2. Provider fetches content (by queries/IDs/topics/etc.)
3. Each item is checked against Notion via check_property_value() (deduplication)
4. New items are formatted via schema builder and inserted via add_row()

### Provider Pattern

Providers implement multiple fetch methods that:
- Use random delays (time.sleep(random.uniform(1, 5))) between API calls for rate limiting
- Maintain seen_* sets to deduplicate within a single run
- Return list of normalized video/article dictionaries

## Configuration

**Required for YouTube tracker:** YOUTUBE_API_KEY, NOTION_API_KEY, NOTION_YOUTUBE_DATABASE_ID, plus at least one of YOUTUBE_CHANNEL_IDS, YOUTUBE_QUERIES, or YOUTUBE_VIDEO_IDS

**Required for News tracker:** NOTION_API_KEY, NOTION_NEWS_DATABASE_ID, plus at least one of GNEWS_TOPICS, GNEWS_KEYWORDS, GNEWS_SITES, or GNEWS_LOCATIONS

## Workflow

- **Trigger:** Daily at 00:00 UTC via GitHub Actions (.github/workflows/youtube-tracker.yml for YouTube, create similar for News)
- **Deduplication:** Checks unique property (video_id for YouTube, url for News) against existing Notion entries
- **Rate limiting:** Random 1-5 second delays between API fetch operations

