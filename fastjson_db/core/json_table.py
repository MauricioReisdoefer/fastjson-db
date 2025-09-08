import os
import orjson
from fastjson_db.core import JsonModel
from fastjson_db.errors import HeritageError, BadTypingError, OperationError
from typing import Dict

class JsonTable:
    """Represents a Table of a specific Model with validated fast in-memory cache."""

    def __init__(self, model: type[JsonModel], path: str | os.PathLike):
        if not issubclass(model, JsonModel):
            raise HeritageError("JsonTable Creation Error", "'model' field should be a JsonModel subclass")
        if not isinstance(path, (str, os.PathLike)):
            raise BadTypingError("JsonTable Creation Error", "'path' must be a 'str' or 'os.PathLike'")

        self.model = model
        self.path = os.fspath(path)
        self.cache: Dict[int, JsonModel] = {}  # Store objects directly for speed

    def _load_cache(self):
        """Load JSON from file into cache (objects stored directly)."""
        try:
            with open(self.path, 'rb') as f:
                data = orjson.loads(f.read())
                # Store model instances directly, avoiding extra dict creation
                self.cache = {item['id']: self.model(**item) for item in data}
        except FileNotFoundError:
            print(f"Warning: '{self.path}' not found. Starting empty table.")
            self.cache = {}
        except orjson.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            self.cache = {}

    def insert(self, model_instance: JsonModel):
        """Insert a model instance into cache with validation."""
        if not isinstance(model_instance, self.model):
            raise OperationError("Insert Error", f"Expected instance of {self.model}")
        self.cache[model_instance.id] = model_instance

    def remove(self, query_id: int):
        """Remove a model instance from cache with validation."""
        if query_id not in self.cache:
            raise OperationError("Remove Error", f"ID {query_id} not found")
        del self.cache[query_id]

    def update(self, query_id: int, new_data: JsonModel):
        """Update a model instance in cache with validation."""
        if query_id not in self.cache:
            raise OperationError("Update Error", f"ID {query_id} not found")
        if not isinstance(new_data, self.model):
            raise OperationError("Update Error", f"Expected instance of {self.model}")
        self.cache[query_id] = new_data

    def get(self, query_id: int):
        """Get a model instance by ID with validation."""
        if query_id not in self.cache:
            raise OperationError("Get Error", f"ID {query_id} not found")
        return self.cache[query_id]
