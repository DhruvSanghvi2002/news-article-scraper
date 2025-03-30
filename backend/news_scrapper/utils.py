import requests
from bs4 import BeautifulSoup
from newspaper import Article
from datetime import datetime

NEWS_SOURCES = {
    "https://www.jagran.com/",
    "https://ndtv.in/india",
    "https://www.bbc.com/hindi"
}


def fetch_news_urls():
    """Scrapes news article URLs from the defined sources."""
    news_data = []

    for base_url in NEWS_SOURCES:
        response = requests.get(
            base_url, headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        news_urls = []

        if "jagran" in base_url:
            for link in soup.select("h3 a"):
                url = link.get("href", "")
                if url.startswith("/"):
                    url = "https://www.jagran.com" + url
                news_urls.append(url)

        elif "ndtv" in base_url:
            for link in soup.select("h2 a"):
                url = link.get("href", "")
                if url.startswith("/"):
                    url = "https://ndtv.in" + url
                news_urls.append(url)

        elif "bbc" in base_url:
            for link in soup.select("a[href*='/hindi/articles/']"):
                url = link.get("href", "")
                if url.startswith("/"):
                    url = "https://www.bbc.com" + url
                news_urls.append(url)

        news_data.extend(news_urls)

    return news_data


def scrape_news():
    article_urls = fetch_news_urls()
    news_articles = []

    for url in article_urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            news_articles.append({
                "title": article.title,
                "link": url,
                "text": article.text,
                "summary": article.summary,
                "keywords": article.keywords
            })

        except Exception as e:
            print(f"Error processing {url}: {e}")

    return news_articles
