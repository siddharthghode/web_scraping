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
    def __init__(self, base_url):
        self.base_url = base_url
        self.source = "BooksToScrape_Static"

    @retry((requests.exceptions.RequestException), tries=3)
    def fetch_page(self, url):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    def scrape_books(self):
        logger.info(f"Starting static scrape on {self.base_url}")
        html = self.fetch_page(self.base_url)
        soup = BeautifulSoup(html, 'html.parser')
        
        books = []
        articles = soup.find_all('article', class_='product_pod')
        
        for article in articles:
            try:
                title = article.h3.a['title']
                price = article.find('p', class_='price_color').text
                rating = article.p['class'][1] # e.g., "star-rating Three" -> "Three"
                availability = article.find('p', class_='instock availability').text.strip()
                link = self.base_url + article.h3.a['href']
                
                books.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "availability": availability,
                    "url": link,
                    "source": self.source
                })
            except Exception as e:
                logger.error(f"Error parsing book: {e}")
        
        logger.info(f"Successfully scraped {len(books)} books from static source.")
        return books
