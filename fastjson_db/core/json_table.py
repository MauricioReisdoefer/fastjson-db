import os
import orjson
from fastjson_db.core import JsonModel
from fastjson_db.errors import HeritageError, BadTypingError, OperationError
from typing import List

class JsonTable:
    """Represents a Table of a specific Model"""
    def __init__(self, model: JsonModel, path: str | os.PathLike):
        if not issubclass(model, JsonModel):
            raise HeritageError("JsonTable Creation Error", "'model' field should be a JsonModel subclass")
        if not isinstance(path, (str, os.PathLike)):
            raise BadTypingError("JsonTable Creation Error", "'path' must be a 'str' or 'os.PathLike'")

        self.model = model
        self.path = os.fspath(path) # Internaly always a string
        self.cache: List[dict] = [] # Holds every data in the table
        
    def _load_cache(self):
        """Loads the .json Table in Cache for faster execution"""
        try:
            with open(self.path, 'r') as f:
                json_string = f.read()
                data = orjson.loads(json_string)
                self.cache = data
        except FileNotFoundError:
            print("Error: 'data.json' not found.")
        except orjson.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            
    def insert(self, model_instance:JsonModel):
        """Inserts a user in the cache memory"""
        if type(model_instance) is not self.model:
            raise OperationError("JsonTable Insert Error", f"'insert_model' field should be a instance of {self.model}")
        self.cache.append(model_instance.to_json())
    
    def remove(self, query_id:int):
        """Removes a user in the cache memory"""
        if query_id is None:
            raise OperationError("JsonTable Remove Error", "'query_id' field cannot be None")

    def update(self, query_id:int, new_data:JsonModel):
        """Updates a user in the cache memory"""
        if query_id is None:
            raise OperationError("JsonTable Remove Error", "'query_id' field cannot be None")
        if new_data is None:
            raise OperationError("JsonTable Remove Error", "'data' field cannot be None")