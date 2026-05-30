from config import GNEWS_TOPICS, GNEWS_KEYWORDS, GNEWS_SITES, GNEWS_LOCATIONS, GNEWS_LIMIT, GNEWS_FROM_DATE
from config import NOTION_API_KEY, NOTION_NEWS_DATABASE_ID

from providers import NewsProvider
from databases import NotionDatabase
from schema import build_news_notion_properties

if __name__ == "__main__":
    news = NewsProvider(
        topics=GNEWS_TOPICS,
        keywords=GNEWS_KEYWORDS,
        sites=GNEWS_SITES,
        locations=GNEWS_LOCATIONS,
        from_date=GNEWS_FROM_DATE,
        limit=GNEWS_LIMIT
    )
    notion = NotionDatabase(
        api_key=NOTION_API_KEY,
        database_id=NOTION_NEWS_DATABASE_ID
    )

    articles = []

    articles.extend(news.fetch_by_topic())

    articles.extend(news.fetch_by_Keywords())

    articles.extend(news.fetch_by_site())

    articles.extend(news.fetch_by_location())

    for article in articles:
        is_exists = notion.check_property_value(
            property_name="url",
            target_value=article["url"],
            property_type="url"
        )

        if not is_exists:
            properties = build_news_notion_properties(article)
            respone = notion.add_row(properties=properties)
            print(f"{respone} {article['title']}")
        else:
            print('already exist in the notion.')