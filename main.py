import logging
from scrapers.static_scraper import StaticScraper
from scrapers.selenium_scraper import SeleniumScraper
from pipeline.cleaner import DataCleaner
from database.mongo import MongoDBClient
from config import STATIC_SITE_URL, DYNAMIC_SITE_URL

# Setup logging (already configured in database/mongo.py, but we'll ensure it's active)
logger = logging.getLogger(__name__)

def main():
    logger.info("--- Starting Book Tracker Automation ---")
    
    # 1. Initialize DB
    db_client = MongoDBClient()
    
    raw_data = []

    # 2. Run Static Scraper
    try:
        static_scraper = StaticScraper(STATIC_SITE_URL)
        static_books = static_scraper.scrape_books()
        raw_data.extend(static_books)
    except Exception as e:
        logger.error(f"Static scraper failed: {e}")

    # 3. Run Selenium Scraper (Optional/Demonstration)
    try:
        selenium_scraper = SeleniumScraper(DYNAMIC_SITE_URL)
        selenium_books = selenium_scraper.scrape_books()
        raw_data.extend(selenium_books)
    except Exception as e:
        logger.error(f"Selenium scraper failed: {e}")

    # 4. Data Cleaning Pipeline
    if raw_data:
        cleaner = DataCleaner()
        cleaned_data = cleaner.clean_book_data(raw_data)
        
        # 5. Store in MongoDB
        success_count = 0
        for book in cleaned_data:
            if db_client.insert_book(book):
                success_count += 1
        
        logger.info(f"Successfully processed and stored {success_count} books.")
    else:
        logger.warning("No data scraped.")

    db_client.close()
    logger.info("--- Book Tracker Automation Finished ---")

if __name__ == "__main__":
    main()
