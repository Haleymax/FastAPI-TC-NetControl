from datetime import datetime, timezone
from typing import Dict, Any, Mapping

from pymongo import MongoClient

mongo_database = 'api'

class Mongo:
    def __init__(self, uri: str, database_name:str) -> None:
        self.client = MongoClient(uri)
        self.db = self.client[database_name]

    def c(self, collection):
        return self.db.get_collection(collection)

    def find_one(self, collection:str, query:[Dict[str, Any]]) -> Mapping[str, Any] | Any:
        result = self.c(collection).find_one(query)
        return result

    def find_all(self, collection:str, query:[Dict[str, Any]]) -> Mapping[str, Any] | Any:
        result = self.c(collection).find(query)
        return result
