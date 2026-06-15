import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "book_tracker"
COLLECTION_NAME = "books"

# URLs for scraping (using books.toscrape.com as a safe example)
STATIC_SITE_URL = os.getenv("STATIC_SITE_URL", "http://books.toscrape.com/")
DYNAMIC_SITE_URL = os.getenv("DYNAMIC_SITE_URL", "http://books.toscrape.com/") # This site is actually static, but we'll use it to demonstrate Selenium

LOG_FILE = "logs/scraper.log"
