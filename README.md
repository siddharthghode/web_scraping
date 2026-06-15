# Smart Book Price & Availability Tracker

A modular web scraping automation system that tracks book prices and availability from multiple sources, cleans the data using Pandas, and stores it in MongoDB.

## Features
- **Static Scraping**: Uses `Requests` and `BeautifulSoup4` for fast data extraction from static pages.
- **Dynamic Scraping**: Uses `Selenium WebDriver` for handling JavaScript-rendered content and interactions.
- **Data Cleaning Pipeline**: Employs `Pandas` for data normalization, cleaning, and transformation.
- **NoSQL Database**: Integrated with `MongoDB` for flexible, document-based storage of scraped records and price history.
- **Reliability**: Implements retry mechanisms with exponential backoff, comprehensive logging, and robust exception handling.
- **Modular Architecture**: Separated concerns for scraping, cleaning, and database management.

## Project Structure
```
BookTracker/
├── scrapers/           # Scraping modules (Static & Selenium)
├── database/           # Database interaction layer (MongoDB)
├── pipeline/           # Data processing and cleaning (Pandas)
├── logs/               # Log files
├── config.py           # Project configuration
├── requirements.txt    # Python dependencies
└── main.py             # Main entry point
```

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure MongoDB is running locally or provide a `MONGO_URI` in a `.env` file.
3. Run the tracker:
   ```bash
   python main.py
   ```

## Workflow
1. **Extraction**: Scrapers fetch raw data from target websites.
2. **Transformation**: The data cleaner processes prices, ratings, and timestamps.
3. **Loading**: Processed data is upserted into MongoDB, maintaining a history of price changes.
