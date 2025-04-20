def scrape_article(url, retries=2, delay=2):
    """
    Scrape full article content from the URL using newspaper3k with retries
    """
    for attempt in range(retries):
        try:
            article = Article(url, config=config)
            article.download()
            if not article.is_downloaded:
                raise Exception("Download failed or empty")
            article.parse()
            if not article.text.strip():
                raise Exception("Parsed content is empty")
            return article.text
        except Exception as e:
            print(f"[Attempt {attempt + 1}] Failed to scrape {url}: {e}")
            time.sleep(delay)
    return None
