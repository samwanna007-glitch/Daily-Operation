# Daily Tracker Suite

A Python application with two independent trackers that fetches YouTube videos and news headlines, storing metadata in Notion databases.

**Version:** 1.0.0

## Features

- **YouTube Tracker**: Automatically fetches videos uploaded today from configured YouTube channels
- **News Tracker**: Fetches top news headlines every 6 hours using GNews API
- Deduplicates entries by ID to prevent duplicates
- Stores metadata in Notion database
- Tracks processed items in local JSON files
- Automated execution via GitHub Actions

## Setup

**Note:** Data files (`data/videos.json`, `data/news.json`) and logs are gitignored and will not be committed to the repository. They exist as local runtime caches only.

**How History Works:** Deduplication happens via the Notion database (which queries existing entries before adding new ones). GitHub Action runs are stateless - each run checks the current Notion database for existing items.

### 1. Google Cloud Console

Enable the YouTube Data API v3 and create an API key.

### 2. Notion Database

Create Notion databases with these properties:

- **Title** (required)
- **Description** (text)
- **URL** (url)
- **Category** (select)
- **Channel** (text)
- **Publish_Date** (date)

### 3. Environment Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

## Usage

```bash
# Run YouTube tracker
python main.py

# Run News tracker
python main_news.py

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Required environment variables:

| Variable                  | Description                           |
| ------------------------- | ------------------------------------- |
| `YOUTUBE_API_KEY`         | Google YouTube Data API v3 key        |
| `YOUTUBE_CHANNEL_IDS`     | Comma-separated list of channel IDs |
| `NOTION_API_KEY`          | Notion integration key                |
| `NOTION_DATABASE_ID`      | YouTube Notion database ID            |
| `NOTION_NEWS_DATABASE_ID` | News Notion database ID               |
| `NEWS_API_KEY`            | GNews API key                         |
| `NEWS_TOPICS`             | Optional: Comma-separated news topics |
| `NEWS_KEYWORDS`           | Optional: Comma-separated search keywords (takes precedence over topics) |
| `NEWS_EXCLUDE`            | Optional: Comma-separated terms to exclude from results |
| `LOG_LEVEL`               | Optional: Logging level (default: INFO) |
| `FIREBASE_CREDENTIALS_PATH` | Optional: Path to Firebase service account JSON (enables Firebase storage) |

### News Topics

GNews supports the following predefined topics for `NEWS_TOPICS`:

| Topic            | Description      |
| ---------------- | ---------------- |
| `breaking-news`  | Breaking news    |
| `world`          | World news       |
| `entertainment`  | Entertainment    |
| `environment`    | Environment      |
| `food`           | Food             |
| `health`         | Health           |
| `politics`       | Politics         |
| `science`        | Science          |
| `sports`         | Sports           |
| `technology`     | Technology       |

**Example:** `NEWS_TOPICS=technology,science`

### Keyword Search

Use `NEWS_KEYWORDS` to search for specific terms (e.g., "gemini", "chatgpt", "claude"). Uses GNews search endpoint.

**Example:** `NEWS_KEYWORDS=gemini,chatgpt,claude`

**Behavior:**
- If both `NEWS_KEYWORDS` and `NEWS_TOPICS` are set, both are fetched
- If only one is set, that source is used

### Exclude Terms

Use `NEWS_EXCLUDE` to filter out unwanted topics (e.g., crypto, stocks).

**Example:** `NEWS_EXCLUDE=crypto,stocks`

**Query format:** Keywords are combined into a single OR query with exclusions applied:
```
q=(gemini OR chatgpt OR claude) AND NOT crypto AND NOT stocks
```

### Notion Database Properties

**Required properties (create in Notion):**
- Title, Description, URL, Category, Channel, Publish_Date, Video_id
- For News database: Article_Id (instead of Video_id, for deduplication)

**Optional properties (add manually if desired):**
- `Image` (type: URL) - Article image URL
- `Content` (type: Text) - Article body content (truncated on free GNews tier)
- `Source_URL` (type: URL) - Direct link to source website

## Architecture

```
.
├── main.py              # YouTube tracker entry point
├── main_news.py         # News tracker entry point
├── src/
│   ├── clients/
│   │   ├── youtube.py   # YouTube API client
│   │   └── news.py      # GNews API client
│   ├── core/
│   │   ├── notion.py    # Notion API integration
│   │   ├── storage.py   # JSON persistence
│   │   ├── config.py    # Environment configuration
│   │   └── firebase.py  # Optional Firebase integration
│   └── trackers/
│       ├── base.py      # Base tracker with shared logic
│       ├── youtube.py   # YouTube tracker implementation
│       └── news.py      # News tracker implementation
├── data/
│   ├── videos.json      # Tracked videos storage (gitignored, local cache)
│   └── news.json        # Tracked news storage (gitignored, local cache)
└── logs/
    ├── tracker.log      # YouTube tracker logs (gitignored)
    └── news-tracker.log # News tracker logs (gitignored)
```

## Automation

YouTube tracker runs daily at 00:00 UTC. News tracker runs every 6 hours (00:00, 06:00, 12:00, 18:00 UTC).

To enable GitHub Actions:

1. Push this repository to GitHub
2. Add secrets in repository settings:
   - `YOUTUBE_API_KEY`
   - `YOUTUBE_CHANNEL_IDS`
   - `NOTION_API_KEY`
   - `NOTION_DATABASE_ID`
   - `NOTION_NEWS_DATABASE_ID`
   - `NEWS_API_KEY`
   - `NEWS_TOPICS`
   - `NEWS_KEYWORDS`
   - `NEWS_EXCLUDE`
   - `LOG_LEVEL`
   - `FIREBASE_SERVICE_ACCOUNT` (optional): Your Firebase service account JSON (entire file content as a string)
