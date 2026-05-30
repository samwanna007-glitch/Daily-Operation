import random
import time
import logging
import urllib.parse

from gnews import GNews
from schema import build_news_article_schema


class NewsProvider:
    def __init__(self, topics, keywords, sites, locations, limit, from_date):
        self.topics = [c.strip().lower() for c in topics.split(',')] if topics else []
        self.keywords = [q.strip() for q in keywords.split(',')] if keywords else []
        self.sites = [s.strip() for s in sites.split(',')] if sites else []
        self.locations = [l.strip() for l in locations.split(',')] if locations else []
        self.limit = int(limit) if limit else 10
        self.period = f'{int(from_date) if from_date else 1}d'

        self.gnews_client = GNews(language='en', country='US', period=self.period, max_results=self.limit)

        print("Initialized news provider.")

    def fetch_by_topic(self):
        if not self.gnews_client:
            raise RuntimeError("GNews client is not initialized. Please call the setup method first.")
        if not self.topics:
            logging.warning("Topic list is empty. Skipping the process.")
            return[]

        articles = []
        seen_urls = set()

        for topic in self.topics:
            try:
                response = self.gnews_client.get_news_by_topic(topic)
                print(f"Fetched from topic '{topic}': {len(response)} articles")
            except Exception as e:
                logging.warning(f"Failed to fetch news by topic '{topic}': {e}")
                continue

            for item in response:
                article_url = item.get('url')
                if article_url and article_url not in seen_urls:
                    seen_urls.add(article_url)
                    articles.append(build_news_article_schema(item, fetch_by="topic"))

            time.sleep(random.uniform(1, 5))

        return articles

    def fetch_by_Keywords(self):
        if not self.gnews_client:
            raise RuntimeError("GNews client is not initialized. Please call the setup method first.")
        if not self.keywords:
            logging.warning("Keywords list is empty. Skipping the process.")
            return[]

        articles = []
        seen_urls = set()

        for keyword in self.keywords:
            try:
                response = self.gnews_client.get_news(keyword)
                print(f"Fetched from keyword '{keyword}': {len(response)} articles")
            except Exception as e:
                logging.warning(f"Failed to fetch news by keyword '{keyword}': {e}")
                continue

            for item in response:
                article_url = item.get('url')
                if article_url and article_url not in seen_urls:
                    seen_urls.add(article_url)
                    articles.append(build_news_article_schema(item, fetch_by="keyword"))

            time.sleep(random.uniform(1, 5))

        return articles

    def fetch_by_site(self):
        if not self.gnews_client:
            raise RuntimeError("GNews client is not initialized. Please call the setup method first.")
        if not self.sites:
            logging.warning("Sites list is empty. Skipping the process.")
            return []

        articles = []
        seen_urls = set()

        for site in self.sites:
            try:
                response = self.gnews_client.get_news_by_site(site)
                print(f"Fetched from site '{site}': {len(response)} articles")
            except Exception as e:
                logging.warning(f"Failed to fetch news by site '{site}': {e}")
                continue

            for item in response:
                article_url = item.get('url')
                if article_url and article_url not in seen_urls:
                    seen_urls.add(article_url)
                    articles.append(build_news_article_schema(item, fetch_by="site"))
            time.sleep(random.uniform(1, 5))

        return articles

    def fetch_by_location(self):
        if not self.gnews_client:
            raise RuntimeError("GNews client is not initialized. Please call the setup method first.")
        if not self.locations:
            logging.warning("Locations list is empty. Skipping the process.")
            return []

        articles = []
        seen_urls = set()

        for location in self.locations:
            try:
                response = self.gnews_client.get_news_by_location(urllib.parse.quote(location))
                print(f"Fetched from location '{location}': {len(response)} articles")
            except Exception as e:
                logging.warning(f"Failed to fetch news by location '{location}': {e}")
                continue

            for item in response:
                article_url = item.get('url')
                if article_url and article_url not in seen_urls:
                    seen_urls.add(article_url)
                    articles.append(build_news_article_schema(item, fetch_by="location"))

            time.sleep(random.uniform(1, 5))

        return articles