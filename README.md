# 📚 Book Price Tracker

A modular, multi-source web scraping system that tracks book prices and availability, cleans the data, stores it in MongoDB, and displays it in a clean web dashboard.

---

## Features

- **Multi-source scraping** — scrape any number of sites in one run
- **Three scraper engines** — static (requests + BS4), dynamic (Selenium), Shopify API
- **Data cleaning pipeline** — price normalisation, rating mapping, availability parsing via Pandas
- **MongoDB storage** — upserts with full price history per book
- **Web dashboard** — per-source sections, search, sort, price history modal
- **Retry with backoff** — automatic retries on network failures
- **Configurable** — add a new site in `config.py` with no code changes

---

## Project Structure

```
BookTracker/
├── scrapers/
│   ├── static_scraper.py       # requests + BeautifulSoup (static HTML pages)
│   ├── selenium_scraper.py     # Selenium headless Chrome (JS-rendered pages)
│   └── shopify_scraper.py      # Shopify /products.json API
├── database/
│   └── mongo.py                # MongoDB connection, upsert, indexing
├── pipeline/
│   └── cleaner.py              # Pandas data cleaning pipeline
├── templates/
│   └── index.html              # Flask web dashboard
├── logs/
│   └── scraper.log             # Rotating log output
├── config.py                   # All site configs and settings
├── app.py                      # Flask web app
├── main.py                     # Scraper entry point
└── requirements.txt
```

---

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd BookTracker
pip install -r requirements.txt
```

### 2. Configure MongoDB

Start MongoDB locally:

```bash
# Ubuntu / Debian
sudo systemctl start mongodb
```

Or use MongoDB Atlas — add your URI to a `.env` file:

```env
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/
```

### 3. Run the scraper

```bash
python main.py
```

### 4. View the dashboard

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Adding a New Site

All site configuration lives in `config.py` inside the `SITES` list. No other file needs to change.

### Static site (plain HTML)

Inspect the page source in your browser (F12), find the CSS classes for each field, then add:

```python
{
    "name": "MyBookSite",
    "url": "https://example.com/books",
    "type": "static",
    "selectors": {
        "book_container": "div.book-card",    # wrapper element per book
        "title":          "h2.book-title",    # title element (text or title attr)
        "price":          "span.price",       # price element
        "rating":         "span.stars",       # rating element (last class used)
        "availability":   "span.stock",       # availability element
        "link":           "a.book-link",      # link element (href attr)
    }
},
```

### JavaScript-rendered site

Same as above but use `"type": "selenium"` — Selenium will wait for the page to render before scraping.

### Any Shopify store

No selectors needed — uses the public `/products.json` API:

```python
{
    "name": "SomeShopifyStore",
    "url": "https://somestore.com/",
    "type": "shopify",
},
```

---

## How It Works

```
python main.py
       │
       ├─ For each site in SITES (config.py)
       │       │
       │       ├─ type: static   → StaticScraper   (requests + BS4)
       │       ├─ type: selenium → SeleniumScraper  (headless Chrome)
       │       └─ type: shopify  → ShopifyScraper   (/products.json API)
       │
       ├─ DataCleaner (Pandas)
       │       ├─ Price  → strip symbols, convert to float
       │       ├─ Rating → word/string → integer (0–5)
       │       ├─ Availability → normalise to True / False
       │       └─ Timestamp → add scrape datetime
       │
       └─ MongoDBClient
               └─ Upsert by (title, source)
                  + push price_history []
```

---

## MongoDB Document Schema

```json
{
  "title":        "A Light in the Attic",
  "price":        51.77,
  "rating":       3,
  "availability": true,
  "url":          "http://books.toscrape.com/...",
  "source":       "BooksToScrape",
  "timestamp":    "2024-01-15 10:30:00",
  "price_history": [
    { "price": 51.77, "date": "2024-01-15 10:30:00" },
    { "price": 49.99, "date": "2024-01-16 10:30:00" }
  ]
}
```

---

## Dashboard

| Feature | Description |
|---|---|
| Overview stats | Total books, in stock, out of stock, source count |
| Per-source sections | Separate collapsible section for each scraped site |
| Per-section search | Filter books within a source in real time |
| Sort | By title, price (asc/desc), or rating |
| Price history | Modal showing full price history for any book |
| Sidebar nav | Jump to any source section, highlights on scroll |

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Web dashboard |
| `GET /api/stats` | JSON summary of all sources and counts |

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MONGO_URI` | `mongodb://localhost:27017/` | MongoDB connection string |

---

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP requests for static scraping |
| `beautifulsoup4` | HTML parsing |
| `selenium` | Headless Chrome for JS-rendered pages |
| `webdriver-manager` | Auto-manages ChromeDriver |
| `pandas` | Data cleaning pipeline |
| `pymongo` | MongoDB driver |
| `flask` | Web dashboard |
| `python-dotenv` | Load `.env` config |
| `lxml` | Fast HTML/XML parser |
