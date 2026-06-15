import logging
from pymongo import MongoClient, ASCENDING
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MongoDBClient:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self.db = self.client[DB_NAME]
            self.collection = self.db[COLLECTION_NAME]
            self.client.server_info()
            self._ensure_indexes()
            logger.info("Connected to MongoDB successfully.")
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            self.client = None

    def _ensure_indexes(self):
        self.collection.create_index(
            [("title", ASCENDING), ("source", ASCENDING)], unique=True
        )

    def insert_book(self, book_data):
        if self.client is None:
            logger.warning("MongoDB client is not connected. Data not saved.")
            return False
        try:
            self.collection.update_one(
                {"title": book_data["title"], "source": book_data["source"]},
                {
                    "$set": book_data,
                    "$push": {"price_history": {"price": book_data["price"], "date": book_data["timestamp"]}}
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error inserting data into MongoDB: {e}")
            return False

    def close(self):
        if self.client:
            self.client.close()
