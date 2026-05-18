import requests
from ..core.config import NEWS_API_KEY, NEWS_TOPICS, NEWS_KEYWORDS, NEWS_EXCLUDE


def fetch_latest_news(topics=None, keywords=None):
    """Fetch latest news articles from GNews API.

    Args:
        topics: Optional list of topics. Uses NEWS_TOPICS from config if not provided.
        keywords: Optional list of keywords. Uses NEWS_KEYWORDS from config if not provided.
    """
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not found in environment variables.")

    keywords = keywords or NEWS_KEYWORDS
    topics = topics or NEWS_TOPICS
    exclude = NEWS_EXCLUDE

    if not keywords and not topics:
        raise ValueError("No news configuration. Set NEWS_TOPICS or NEWS_KEYWORDS in .env")

    all_articles = []

    # Fetch by keywords - combined into single OR query for efficiency
    if keywords:
        url = "https://gnews.io/api/v4/search"

        # Build combined query with OR logic
        keywords_str = "(" + " OR ".join(keywords) + ")"
        query = keywords_str

        # Add exclusion terms with explicit AND NOT
        if exclude:
            query += " AND NOT " + " NOT ".join(exclude)

        params = {
            "token": NEWS_API_KEY,
            "q": query,
            "lang": "en",
            "max": 20,
            "in": "title,description",
            "sortby": "publishedAt"
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                for article in data.get("articles", []):
                    article_data = {
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "url": article.get("url", ""),
                        "image": article.get("image", ""),
                        "published_at": article.get("publishedAt", ""),
                        "channel": article.get("source", {}).get("name", "Unknown"),
                        "channel_url": article.get("source", {}).get("url", ""),
                        "article_id": article.get("url", "").split("/")[-1][:30]
                    }
                    all_articles.append(article_data)
        except Exception as e:
            print(f"Error fetching news for keywords: {e}")

    # Fetch by topics if provided
    if topics:
        for topic in topics:
            url = "https://gnews.io/api/v4/top-headlines"
            params = {
                "token": NEWS_API_KEY,
                "topic": topic,
                "lang": "en",
                "max": 10
            }

            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    for article in data.get("articles", []):
                        article_data = {
                            "title": article.get("title", ""),
                            "description": article.get("description", ""),
                            "url": article.get("url", ""),
                            "image": article.get("image", ""),
                            "published_at": article.get("publishedAt", ""),
                            "channel": article.get("source", {}).get("name", "Unknown"),
                            "channel_url": article.get("source", {}).get("url", ""),
                            "article_id": article.get("url", "").split("/")[-1][:30]
                        }
                        all_articles.append(article_data)
            except Exception as e:
                print(f"Error fetching news for topic '{topic}': {e}")

    return all_articles