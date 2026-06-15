import requests
import logging

logger = logging.getLogger(__name__)

class ShopifyScraper:
    def __init__(self, site_config):
        self.base_url = site_config["url"].rstrip("/")
        self.source = site_config["name"]

    def scrape_books(self):
        logger.info(f"Starting Shopify API scrape on {self.base_url}")
        books = []
        page = 1

        while True:
            try:
                url = f"{self.base_url}/products.json?limit=250&page={page}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                products = response.json().get("products", [])

                if not products:
                    break

                for product in products:
                    variant = product["variants"][0] if product["variants"] else {}
                    books.append({
                        "title": product.get("title", "N/A"),
                        "price": variant.get("price", "0"),
                        "rating": "N/A",
                        "availability": "In stock" if variant.get("available", False) else "Out of stock",
                        "url": f"{self.base_url}/products/{product.get('handle', '')}",
                        "source": self.source
                    })

                page += 1
            except Exception as e:
                logger.error(f"Shopify scrape failed on page {page}: {e}")
                break

        logger.info(f"Scraped {len(books)} books from {self.source}.")
        return books
