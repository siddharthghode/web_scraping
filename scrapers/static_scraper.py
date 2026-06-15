import requests
from bs4 import BeautifulSoup
import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

def retry(exceptions, tries=3, delay=2, backoff=2):
    """Retry decorator with exponential backoff."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"{e}, Retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return wrapper
    return decorator

class StaticScraper:
    def __init__(self, site_config):
        self.base_url = site_config["url"]
        self.source = site_config["name"]
        self.selectors = site_config["selectors"]

    @retry((requests.exceptions.RequestException), tries=3)
    def fetch_page(self, url):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    def scrape_books(self):
        from urllib.parse import urljoin
        logger.info(f"Starting static scrape on {self.base_url}")
        html = self.fetch_page(self.base_url)
        soup = BeautifulSoup(html, 'html.parser')

        books = []
        s = self.selectors
        articles = soup.select(s["book_container"])

        for article in articles:
            try:
                title_el = article.select_one(s["title"])
                price_el = article.select_one(s["price"])
                rating_el = article.select_one(s["rating"])
                avail_el = article.select_one(s["availability"])
                link_el = article.select_one(s["link"])

                books.append({
                    "title": title_el.get("title") or title_el.text.strip(),
                    "price": price_el.text.strip() if price_el else "N/A",
                    "rating": rating_el["class"][-1] if rating_el else "N/A",
                    "availability": avail_el.text.strip() if avail_el else "N/A",
                    "url": urljoin(self.base_url, link_el["href"]) if link_el else self.base_url,
                    "source": self.source
                })
            except Exception as e:
                logger.error(f"Error parsing book: {e}")

        logger.info(f"Scraped {len(books)} books from {self.source}.")
        return books
