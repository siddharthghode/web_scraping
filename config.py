import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "book_tracker"
COLLECTION_NAME = "books"
LOG_FILE = "logs/scraper.log"

# ---------------------------------------------------------------------------
# SITES — add, remove or comment out entries to control what gets scraped.
#
# Fields:
#   name        : Display name, used as the source tag in the database.
#   url         : Full URL of the page to scrape.
#   type        : Scraper engine to use —
#                   "static"   → requests + BeautifulSoup (fast, no JS)
#                   "selenium" → headless Chrome (JS-rendered pages)
#                   "shopify"  → Shopify /products.json API (no selectors needed)
#   selectors   : CSS selectors for static / selenium types.
#                 Keys: book_container, title, price, rating, availability, link
# ---------------------------------------------------------------------------
SITES = [
    {
        "name": "blah blah",
        "url": "https://idriesshahfoundation.org/books/the-hundred-tales-of-wisdom/?gad_source=1&gad_campaignid=15498754015&gbraid=0AAAAADo_UPhLlmDv5D_i6DQ-WJxRCFpDS&gclid=Cj0KCQjwo_PRBhDNARIsAEcVALVjD_WyuYt354f8KiHF1uzge8h16n3C_bCl1Ljz7hDOLDXf935GjLYaAobCEALw_wcB",
        "type": "selenium",
    }
    # -----------------------------------------------------------------------
    # Template — copy and fill in to add a new site
    # -----------------------------------------------------------------------
    # {
    #     "name": "MySite",
    #     "url": "https://example.com/books",
    #     "type": "static",          # or "selenium" for JS-rendered pages
    #     "selectors": {
    #         "book_container": "div.book-card",
    #         "title": "h2.title",
    #         "price": "span.price",
    #         "rating": "span.stars",
    #         "availability": "span.stock",
    #         "link": "a.book-link",
    #     }
    # },
]
