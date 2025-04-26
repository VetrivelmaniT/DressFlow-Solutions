import os
import pymongo
import logging
from typing import Dict, Any


class MongoDBManager:
    def __init__(self, db_name: str, collection_name: str):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def insert_data(self, data: Dict[str, Any]) -> None:
        try:
            self.collection.insert_one(data)
            self.logger.info(f"Data successfully inserted into MongoDB: {data}")
        except Exception as e:
            self.logger.error(f"Error inserting data into MongoDB: {e}")
            raise
    
    
    
    def test_mongo_connection(self):
        pdf_text = pdf_text[:5000]
        try:
            self.mongo_client.admin.command('ping')
            self.logger.info("MongoDB connection is successful.")
        except Exception as e:
            self.logger.error(f"MongoDB connection failed: {str(e)}")
            
    