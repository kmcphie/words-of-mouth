import requests
from newspaper import Article, Config
import json
import time
import os

# Categories to fetch from NewsAPI
CATEGORIES = ['business', 'entertainment', 'health', 'science', 'sports', 'technology']

# Domains known to block scraping
BLOCKED_DOMAINS = [
    "barrons.com", "wsj.com", "axios.com", "forbes.com",
    "marketwatch.com", "houstonchronicle.com", "cpsc.gov",
    "9news.com", "thestreet.com", "penncapital-star.com"
]

# Set up a user-agent to mimic a browser
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10

def fetch_top_headlines(api_key, category, country='us'):
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "country": country,
        "category": category,
        "pageSize": 100
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {category} news: {response.status_code}")
        print(response.text)
        return None

def should_skip(url):
    return any(blocked in url for blocked in BLOCKED_DOMAINS)

def scrape_article(url):
    try:
        article = Article(url, config=config)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

def enrich_articles(articles, failed_scrapes):
    enriched = []
    for article in articles:
        url = article.get("url")
        if not url or should_skip(url):
            print(f"Skipping blocked or missing URL: {url}")
            failed_scrapes.append({"reason": "Blocked or missing", "url": url})
            continue

        full_text = scrape_article(url)
        if not full_text:
            failed_scrapes.append({"reason": "Scrape failed", "url": url})
            continue

        enriched.append({
            "title": article.get("title"),
            "url": url,
            "publishedAt": article.get("publishedAt"),
            "source": article.get("source", {}).get("name"),
            "description": article.get("description"),
            "content": full_text
        })
    return enriched

def scrape_news():
    API_KEY = "36475236ef064840a80b1d981724c482"

    all_articles_by_category = {}
    failed_scrapes = []

    for category in CATEGORIES:
        print(f"\n🔍 Fetching category: {category}")
        response = fetch_top_headlines(API_KEY, category=category)

        if response and response.get("status") == "ok":
            articles = response.get("articles", [])
            print(f"→ Found {len(articles)} articles for {category}")

            enriched_articles = enrich_articles(articles, failed_scrapes)
            all_articles_by_category[category] = enriched_articles

            time.sleep(1)
        else:
            print(f"❌ Failed to fetch articles for category: {category}")
            failed_scrapes.append({
                "reason": "Fetch failed",
                "category": category,
                "status_code": response.get("status") if response else "no response"
            })

    with open("clustered_articles_by_category.json", "w", encoding="utf-8") as f:
        json.dump(all_articles_by_category, f, ensure_ascii=False, indent=4)

    with open("failed_scrapes.json", "w", encoding="utf-8") as f:
        json.dump(failed_scrapes, f, ensure_ascii=False, indent=4)

    print("\n✅ All articles saved to clustered_articles_by_category.json")
    print("📄 Failed scrapes saved to failed_scrapes.json")

def get_news(category=None):
    """
    Load previously scraped news from JSON.
    """
    if not os.path.exists("clustered_articles_by_category.json"):
        raise FileNotFoundError("The news data file does not exist. Run scrape_news() first.")

    with open("clustered_articles_by_category.json", "r", encoding="utf-8") as f:
        all_articles_by_category = json.load(f)

    if category:
        if isinstance(category, list):
            return {cat: all_articles_by_category.get(cat, []) for cat in category}
        else:
            return all_articles_by_category.get(category, [])
    return all_articles_by_category

def get_news_text(category=None, max_articles=2):
    """
    Returns the text content of the first `max_articles` news articles for each category.
    """
    print(category)
    articles_by_category = get_news(category)
    output_lines = []

    if category:
        if isinstance(articles_by_category, dict):  # category is a list
            for cat, articles in articles_by_category.items():
                for article in articles[:max_articles]:
                    content = article.get("content", "")
                    if content:
                        output_lines.append(content)
        elif isinstance(articles_by_category, list):  # single category
            for article in articles_by_category[:max_articles]:
                content = article.get("content", "")
                if content:
                    output_lines.append(content)
    else:
        for cat, articles in articles_by_category.items():
            for article in articles[:max_articles]:
                content = article.get("content", "")
                if content:
                    output_lines.append(content)
    print("Output lines: ", output_lines)
    return "\n\n".join(output_lines)
