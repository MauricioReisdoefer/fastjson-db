try:
    import orjson as json_engine
except ImportError:
    import json as json_engine

import os
from dataclasses import asdict, is_dataclass
from typing import Any, List, Type, TypeVar, Dict

from fastjson_db.model import JsonModel
T = TypeVar("T", bound="JsonModel")
class JsonTable:
    """
    JsonTable works with dataclasses, ensuring that only objects of the correct type can be inserted.
    Each instance represents a "table" stored as a JSON file.
    """

    def __init__(self, path: str, model_cls: Type[T]):
        """
        Initializes the table for a specific dataclass type.

        Args:
            path (str): Path to the JSON file representing the table.
            model_cls (Type[T]): The dataclass that this table will accept.

        Raises:
            ValueError: If `model_cls` is not a dataclass.
        """
        self.path = path
        self.model_cls = model_cls

        if not is_dataclass(model_cls):
            raise ValueError("model_cls must be a dataclass")

        self._data_cache: List[Dict[str, Any]] = []
        self._loaded = False

        if os.path.exists(self.path):
            self._load_cache()
        else:
            self.save([])

    def _load_cache(self):
        """Load the JSON file into the in-memory cache."""
        with open(self.path, "rb") as file:
            self._data_cache = json_engine.loads(file.read())
        self._loaded = True

    def load(self) -> List[Dict[str, Any]]:
        """
        Loads all records from the JSON file as a list of dictionaries.

        Returns:
            List[Dict[str, Any]]: List of all records stored in the table.
        """
        if not self._loaded:
            self._load_cache()
        return self._data_cache

    def save(self, data: List[Dict[str, Any]] = None):
        """
        Saves a list of records (dictionaries) to the JSON file.

        Args:
            data (List[Dict[str, Any]], optional): Records to save. Defaults to None.
        """
        if data is not None:
            self._data_cache = data
        with open(self.path, "wb") as file:
            file.write(json_engine.dumps(self._data_cache))

    def flush(self):
        """Writes the current in-memory cache to disk."""
        self.save()

    def insert(self, obj: T) -> int:
        """
        Inserts a single dataclass object into the table and assigns a unique `_id`.

        Args:
            obj (T): The dataclass object to insert.

        Returns:
            int: The `_id` assigned to the inserted object.

        Raises:
            TypeError: If the object is not an instance of the table's dataclass.
        """
        if not isinstance(obj, self.model_cls):
            raise TypeError(f"Object must be of type {self.model_cls.__name__}")

        record = asdict(obj)
        record["_id"] = len(self._data_cache) + 1
        self._data_cache.append(record)
        obj._id = record["_id"]
        return obj._id

    def get_all(self) -> List[T]:
        """
        Retrieves all records from the table as dataclass objects.

        Returns:
            List[T]: List of dataclass instances representing all records.
        """
        return [self.model_cls(**record) for record in self._data_cache]

    def get_by(self, key: str, value: Any) -> List[T]:
        """
        Retrieves records where a given field matches a specific value.

        Args:
            key (str): The field name to search by.
            value (Any): The value to match.

        Returns:
            List[T]: List of dataclass instances that match the condition.
        """
        return [self.model_cls(**record) for record in self._data_cache if record.get(key) == value]

    def delete(self, _id: int) -> bool:
        """
        Deletes a record by its `_id`.

        Args:
            _id (int): The unique ID of the record to delete.

        Returns:
            bool: True if the record was deleted, False otherwise.
        """
        new_data = [record for record in self._data_cache if record["_id"] != _id]
        if len(new_data) != len(self._data_cache):
            self._data_cache = new_data
            return True
        return False

    def insert_many(self, objects: List[T]) -> List[int]:
        """
        Inserts multiple dataclass objects at once.

        Args:
            objs (List[T]): List of dataclass objects to insert.

        Returns:
            List[int]: List of `_id`s assigned to the inserted objects.
        """
        ids = []
        for obj in objects:
            ids.append(self.insert(obj))
        return ids

    def update(self, _id: int, new_obj: T) -> bool:
        """
        Updates a single record identified by its `_id` using a new dataclass object.

        Args:
            _id (int): The unique ID of the record to update.
            new_obj (T): A new dataclass object to replace the existing record.

        Returns:
            bool: True if the record was updated, False otherwise.

        Raises:
            TypeError: If `new_obj` is not an instance of the table's dataclass.
        """
        if not isinstance(new_obj, self.model_cls):
            raise TypeError(f"Object must be of type {self.model_cls.__name__}")

        for index, record in enumerate(self._data_cache):
            if record["_id"] == _id:
                updated_record = asdict(new_obj)
                updated_record["_id"] = _id
                self._data_cache[index] = updated_record
                return True
        return False

    def update_many(self, updates: Dict[int, T]) -> int:
        """
        Updates multiple records at once, using new dataclass objects.

        Args:
            updates (Dict[int, T]): Dictionary where keys are `_id`s and values are new dataclass objects to replace the existing records.

        Returns:
            int: Number of records updated.

        Raises:
            TypeError: If any object in `updates` is not an instance of the table's dataclass.
        """
        count = 0
        for index, record in enumerate(self._data_cache):
            _id = record.get("_id")
            if _id in updates:
                new_obj = updates[_id]
                if not isinstance(new_obj, self.model_cls):
                    raise TypeError(f"Object must be of type {self.model_cls.__name__}")
                updated_record = asdict(new_obj)
                updated_record["_id"] = _id
                self._data_cache[index] = updated_record
                count += 1
        return count
