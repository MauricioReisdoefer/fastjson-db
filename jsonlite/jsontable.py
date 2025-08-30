try:
    import orjson as json_engine
except ImportError:
    import json as json_engine

import os
from dataclasses import asdict, is_dataclass
from typing import Any, List, Type, TypeVar, Dict

T = TypeVar("T")

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

        if not os.path.exists(self.path):
            self.save([])

    def load(self) -> List[Dict[str, Any]]:
        """
        Loads all records from the JSON file as a list of dictionaries.

        Returns:
            List[Dict[str, Any]]: List of all records stored in the table.
        """
        with open(self.path, "rb") as file:
            return json_engine.loads(file.read())

    def save(self, data: List[Dict[str, Any]]):
        """
        Saves a list of records (dictionaries) to the JSON file.

        Args:
            data (List[Dict[str, Any]]): Records to save.
        """
        with open(self.path, "wb") as file:
            file.write(json_engine.dumps(data))

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

        data = self.load()
        record = asdict(obj)
        record["_id"] = len(data) + 1
        data.append(record)
        self.save(data)
        obj._id = record["_id"]
        return obj._id

    def get_all(self) -> List[T]:
        """
        Retrieves all records from the table as dataclass objects.

        Returns:
            List[T]: List of dataclass instances representing all records.
        """
        return [self.model_cls(**record) for record in self.load()]

    def get_by(self, key: str, value: Any) -> List[T]:
        """
        Retrieves records where a given field matches a specific value.

        Args:
            key (str): The field name to search by.
            value (Any): The value to match.

        Returns:
            List[T]: List of dataclass instances that match the condition.
        """
        return [self.model_cls(**record) for record in self.load() if record.get(key) == value]

    def delete(self, _id: int) -> bool:
        """
        Deletes a record by its `_id`.

        Args:
            _id (int): The unique ID of the record to delete.

        Returns:
            bool: True if the record was deleted, False otherwise.
        """
        data = self.load()
        new_data = [record for record in data if record["_id"] != _id]
        if len(new_data) != len(data):
            self.save(new_data)
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
        for object in objects:
            ids.append(self.insert(object))
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

        data = self.load()
        for index, record in enumerate(data):
            if record["_id"] == _id:
                updated_record = asdict(new_obj)
                updated_record["_id"] = _id
                data[index] = updated_record
                self.save(data)
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
        data = self.load()

        for index, record in enumerate(data):
            _id = record.get("_id")
            if _id in updates:
                new_obj = updates[_id]
                if not isinstance(new_obj, self.model_cls):
                    raise TypeError(f"Object must be of type {self.model_cls.__name__}")
                updated_record = asdict(new_obj)
                updated_record["_id"] = _id
                data[index] = updated_record
                count += 1

        self.save(data)
        return count
