import requests
from newspaper import Article
import json

def fetch_top_headlines(api_key, sources=None, country='us', category=None, query=None):
    """
    Fetch top headlines from NewsAPI.org

    Parameters:
    - api_key: Your NewsAPI.org API key
    - sources: Comma-separated string of source IDs (e.g. 'bbc-news,cnn')
    - country: 2-letter ISO 3166-1 country code (default: 'us') – ignored if sources is set
    - category: Category of news (optional) – ignored if sources is set
    - query: Keywords or phrases to search for (optional)

    Returns:
    - JSON response containing articles
    """
    base_url = "https://newsapi.org/v2/top-headlines"
    
    params = {
        "apiKey": api_key
    }

    if sources:
        params["sources"] = sources
    else:
        params["country"] = country
        if category:
            params["category"] = category
    
    if query:
        params["q"] = query
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def scrape_article(url):
    """
    Scrape full article content from the URL using newspaper3k

    Parameters:
    - url: Article URL

    Returns:
    - Full article text (str) or None on failure
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

def display_headlines(articles):
    """Display headlines and descriptions from articles"""
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"Source: {article['source']['name']}")
        print(f"Published: {article['publishedAt']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")

def get_articles_with_full_text(articles):
    """
    Enrich articles with full scraped content

    Parameters:
    - articles: List of articles from NewsAPI

    Returns:
    - List of articles with added 'content' field
    """
    enriched_articles = []
    for article in articles:
        full_text = scrape_article(article['url'])
        article_data = {
            "title": article['title'],
            "url": article['url'],
            "publishedAt": article['publishedAt'],
            "source": article['source']['name'],
            "description": article['description'],
            "content": full_text
        }
        enriched_articles.append(article_data)
    return enriched_articles

def get_news():
    # Replace with your actual API key
    API_KEY = "36475236ef064840a80b1d981724c482"
    
    # Example: Get headlines from specific sources
    preferred_sources = "bbc-news,cnn,techcrunch"  # You can customize this
    
    response = fetch_top_headlines(API_KEY, sources=preferred_sources)
    
    if response and response.get("status") == "ok":
        articles = response.get("articles", [])
        print(f"Found {len(articles)} articles")
        display_headlines(articles)

        enriched_articles = get_articles_with_full_text(articles)

        # Save to a JSON file
        with open("scraped_articles.json", "w", encoding="utf-8") as f:
            json.dump(enriched_articles, f, ensure_ascii=False, indent=4)

        print("Scraped content saved to scraped_articles.json")
    else:
        print("Failed to fetch news")
