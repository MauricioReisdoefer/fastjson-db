try:
    import orjson as json_engine
except ImportError:
    import json as json_engine

import os
from typing import Any, List, Dict

class JsonDB:
    """
    A simple JSON-based database for storing and manipulating records.
    Each record is a dictionary with a unique '_id' assigned automatically.
    """

    def __init__(self, path: str):
        """
        Initializes the database. Creates the JSON file if it doesn't exist.

        Args:
            path (str): Path to the JSON file.
        """
        self.path = path
        if not os.path.exists(self.path):
            self.save([])

    def load(self) -> List[Dict[str, Any]]:
        """
        Loads all records from the JSON file.

        Returns:
            List[Dict[str, Any]]: List of all records.
        """
        with open(self.path, "rb") as file:
            return json_engine.loads(file.read())

    def save(self, data: List[Dict[str, Any]]):
        """
        Saves the provided data to the JSON file.

        Args:
            data (List[Dict[str, Any]]): List of records to save.
        """
        with open(self.path, "wb") as file:
            file.write(json_engine.dumps(data))

    def insert(self, record: Dict[str, Any]) -> int:
        """
        Inserts a single record into the database and assigns a unique '_id'.

        Args:
            record (Dict[str, Any]): The record to insert.

        Returns:
            int: The '_id' assigned to the inserted record.
        """
        data = self.load()
        record["_id"] = len(data) + 1
        data.append(record)
        self.save(data)
        return record["_id"]

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all records from the database.

        Returns:
            List[Dict[str, Any]]: List of all records.
        """
        return self.load()

    def get_by(self, key: str, value: Any) -> List[Dict[str, Any]]:
        """
        Retrieves records where a given key matches a specific value.

        Args:
            key (str): The key to search by.
            value (Any): The value to match.

        Returns:
            List[Dict[str, Any]]: List of matching records.
        """
        return [register for register in self.load() if register.get(key) == value]

    def update(self, _id: int, updates: Dict[str, Any]) -> bool:
        """
        Updates a single record identified by its '_id'.

        Args:
            _id (int): The unique ID of the record to update.
            updates (Dict[str, Any]): Dictionary of fields to update.

        Returns:
            bool: True if the record was updated, False otherwise.
        """
        data = self.load()
        for record in data:
            if record["_id"] == _id:
                record.update(updates)
                self.save(data)
                return True
        return False

    def delete(self, _id: int) -> bool:
        """
        Deletes a record by its '_id'.

        Args:
            _id (int): The unique ID of the record to delete.

        Returns:
            bool: True if the record was deleted, False otherwise.
        """
        data = self.load()
        new_data = [register for register in data if register["_id"] != _id]
        if len(new_data) != len(data):
            self.save(new_data)
            return True
        return False

    def insert_many(self, records: List[Dict[str, Any]]) -> List[int]:
        """
        Inserts multiple records at once and assigns unique '_id's.

        Args:
            records (List[Dict[str, Any]]): List of records to insert.

        Returns:
            List[int]: List of assigned IDs for the inserted records.
        """
        data = self.load()
        ids = []
        next_id = len(data) + 1
        for record in records:
            record["_id"] = next_id
            data.append(record)
            ids.append(next_id)
            next_id += 1
        self.save(data)
        return ids

    def update_many(self, updates: Dict[int, Dict[str, Any]]) -> int:
        """
        Updates multiple records at once based on their '_id's.

        Args:
            updates (Dict[int, Dict[str, Any]]): Dictionary where keys are '_id's 
                and values are dictionaries of fields to update.

        Returns:
            int: Number of records updated.
        """
        data = self.load()
        count = 0
        for record in data:
            _id = record.get("_id")
            if _id in updates:
                record.update(updates[_id])
                count += 1
        self.save(data)
        return count
