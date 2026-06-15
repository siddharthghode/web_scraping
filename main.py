import logging
from scrapers.static_scraper import StaticScraper
from scrapers.selenium_scraper import SeleniumScraper
from scrapers.shopify_scraper import ShopifyScraper
from pipeline.cleaner import DataCleaner
from database.mongo import MongoDBClient
from config import SITES

logger = logging.getLogger(__name__)

SCRAPER_MAP = {
    "static": StaticScraper,
    "selenium": SeleniumScraper,
    "shopify": ShopifyScraper,
}


def main():
    logger.info("=" * 50)
    logger.info(" Starting Book Tracker")
    logger.info(f" Sites configured: {len(SITES)}")
    logger.info("=" * 50)

    db_client = MongoDBClient()
    raw_data = []

    for site in SITES:
        scraper_class = SCRAPER_MAP.get(site["type"])
        if not scraper_class:
            logger.warning(f"Unknown type '{site['type']}' for {site['name']}, skipping.")
            continue
        try:
            logger.info(f"[{site['name']}] Starting scrape ({site['type']})...")
            scraper = scraper_class(site)
            books = scraper.scrape_books()
            raw_data.extend(books)
            logger.info(f"[{site['name']}] Collected {len(books)} records.")
        except Exception as e:
            logger.error(f"[{site['name']}] Scraper failed: {e}")

    if raw_data:
        cleaner = DataCleaner()
        cleaned_data = cleaner.clean_book_data(raw_data)
        success_count = sum(1 for book in cleaned_data if db_client.insert_book(book))
        logger.info(f"Stored {success_count}/{len(cleaned_data)} books to MongoDB.")
    else:
        logger.warning("No data scraped from any source.")

    db_client.close()
    logger.info("=" * 50)
    logger.info(" Book Tracker Finished")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
