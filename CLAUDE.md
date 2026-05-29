# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Daily Tracker Suite** - A Python application for tracking YouTube content:
- Fetches YouTube videos by queries, video IDs, or channel IDs
- Stores metadata in Notion database with deduplication

**Version:** 1.0.0

## Development Commands

```bash
# Run YouTube tracker
python src/main_youtube.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

```
src/
├── main_youtube.py           Entry point
├── config.py                 Environment variable configuration
├── schema.py                 Schema builders for Notion properties
├── providers/
│   └── youtube_provider.py   YouTube API client with search capabilities
└── databases/
    └── notion_database.py    Notion API integration
```

- **src/main_youtube.py** - Entry point orchestrating YouTubeProvider and NotionDatabase
- **src/config.py** - Centralized environment variables using python-dotenv
- **src/schema.py** - Builds Notion-compatible property structures from YouTube data
- **src/providers/youtube_provider.py** - `YouTubeProvider` class with `fetch_by_queries()`, `fetch_by_video_ids()`, `fetch_by_channel_ids()` methods
- **src/databases/notion_database.py** - `NotionDatabase` class with `check_property_value()` for deduplication and `add_row()` for insertion

## Configuration

Required environment variables (see `.env.example`):
- `YOUTUBE_API_KEY` - Google YouTube Data API v3 key
- `YOUTUBE_CHANNEL_IDS` - Comma-separated list of channel IDs to monitor
- `YOUTUBE_QUERIES` - Optional: Comma-separated search queries
- `YOUTUBE_VIDEO_IDS` - Optional: Comma-separated specific video IDs
- `YOUTUBE_LIMIT` - Optional: Max results per query (default: 10)
- `NOTION_API_KEY` - Notion integration key
- `NOTION_YOUTUBE_DATABASE_ID` - Target Notion database ID

## Workflow

- **Trigger:** Daily at 00:00 UTC via GitHub Actions
- **Deduplication:** Checks `video_id` property against existing Notion entries before adding
- **Rate limiting:** Includes random delays between fetch operations to avoid API rate limits