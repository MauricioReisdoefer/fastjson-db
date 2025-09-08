import os
from fastjson_db.core import JsonModel
from fastjson_db.errors import HeritageError, BadTypingError

class JsonTable:
    """Represents a Table of a specific Model"""
    def __init__(self, model: JsonModel, path: str | os.PathLike):
        if not issubclass(model, JsonModel):
            raise HeritageError("JsonTable Creation Error", "'model' field should be a JsonModel subclass")
        if not isinstance(path, (str, os.PathLike)):
            raise BadTypingError("JsonTable Creation Error", "'path' must be a 'str' or 'os.PathLike'")

        self.model = model
        self.path = os.fspath(path) # Internaly always a string
