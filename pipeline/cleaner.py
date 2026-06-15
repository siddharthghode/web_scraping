import pandas as pd
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class DataCleaner:
    @staticmethod
    def clean_book_data(raw_data_list):
        if not raw_data_list:
            return []

        df = pd.DataFrame(raw_data_list)

        # 1. Clean Price: Remove currency symbols and convert to float
        def extract_price(price_str):
            if pd.isna(price_str): return 0.0
            # Extract numbers and decimal points
            match = re.search(r'(\d+\.\d+|\d+)', str(price_str))
            return float(match.group(1)) if match else 0.0

        df['price'] = df['price'].apply(extract_price)

        # 2. Clean Rating: Convert word-based ratings to numbers (specific to books.toscrape.com)
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        df['rating'] = df['rating'].apply(lambda x: rating_map.get(x, 0) if isinstance(x, str) else x)

        # 3. Handle Missing Values
        df['author'] = df.get('author', 'Unknown')
        df['availability'] = df['availability'].apply(lambda x: True if 'In stock' in str(x) else False)

        # 4. Add Timestamp
        df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 5. Drop Duplicates
        df = df.drop_duplicates(subset=['title', 'source'])

        logger.info(f"Cleaned {len(df)} records.")
        return df.to_dict('records')
