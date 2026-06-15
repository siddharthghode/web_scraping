import pandas as pd
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class DataCleaner:
    @staticmethod
    def clean_book_data(raw_data_list):
        if not raw_data_list:
            return []

        df = pd.DataFrame(raw_data_list)

        # Price: strip currency symbols, convert to float
        def extract_price(val):
            if pd.isna(val):
                return 0.0
            match = re.search(r'(\d+\.\d+|\d+)', str(val))
            return float(match.group(1)) if match else 0.0

        df['price'] = df['price'].apply(extract_price)

        # Rating: word → int (books.toscrape), numeric string → int, else 0
        def parse_rating(val):
            if isinstance(val, str):
                return RATING_MAP.get(val, 0)
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return 0

        df['rating'] = df['rating'].apply(parse_rating)

        # Availability: normalise to True / False
        df['availability'] = df['availability'].apply(
            lambda x: True if 'in stock' in str(x).lower() else False
        )

        # Timestamp
        df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Drop exact duplicates within this batch
        df = df.drop_duplicates(subset=['title', 'source'])

        logger.info(f"Cleaned {len(df)} records.")
        return df.to_dict('records')
