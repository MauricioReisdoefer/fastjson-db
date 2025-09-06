try:
    import orjson as json_engine
except ImportError:
    import json as json_engine

import os
from dataclasses import is_dataclass, fields
from typing import Any, List, Type, TypeVar, Dict

from .errors.model_table_errors import NotDataclassModelError, InvalidModel
from .datatypes.serializer import serialize_value, deserialize_value
from .datatypes.unique import Unique
from .jsonuniquer import JsonUniquer
from fastjson_db.model import JsonModel
from typing import get_origin

import tempfile

T = TypeVar("T", bound="JsonModel")

class JsonTable:
    def __init__(self, path: str, model_cls: Type[T]):
        self.path = path
        self.model_cls = model_cls
        
        if not is_dataclass(model_cls):
            raise NotDataclassModelError("model_cls must be a dataclass")
        if not issubclass(model_cls, JsonModel):
            raise InvalidModel("model_cls must inherit from JsonModel")
        if "_id" not in model_cls.__annotations__:
            raise InvalidModel("model_cls must define an _id field explicitly")
        
        self.uniquers = {}
        for f in fields(model_cls):
            if get_origin(f.type) is Unique:
                self.uniquers[f.name] = JsonUniquer(path, model_cls.__name__, f.name)

        self._data_cache: List[Dict[str, Any]] = []
        self._loaded = False

        if os.path.exists(self.path):
            self._load_cache()
        else:
            self.save([])

    def _load_cache(self):
        if not os.path.exists(self.path) or os.path.getsize(self.path) == 0:
            self._data_cache = []
            self.flush()
            return
        with open(self.path, "rb") as file:
            self._data_cache = json_engine.loads(file.read())

    def load(self) -> List[Dict[str, Any]]:
        if not self._loaded:
            self._load_cache()
        return self._data_cache

    def save(self, data: List[Dict[str, Any]] = None):
        if data is not None:
            self._data_cache = data
        temp_file_fd, temp_file_path = tempfile.mkstemp(dir=os.path.dirname(self.path), suffix=".tmp")

        try:
            with os.fdopen(temp_file_fd, "wb") as temp_file:
                temp_file.write(json_engine.dumps(self._data_cache))
                
            os.replace(temp_file_path, self.path)
        except Exception as e:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise e

    def flush(self):
        self.save()

    def insert(self, obj: T) -> int:
        if not isinstance(obj, self.model_cls):
            raise InvalidModel(f"Object must be of type {self.model_cls.__name__}")

        record = {
            f.name: serialize_value(getattr(obj, f.name))
            for f in fields(obj)
            if f.name != "_table"
        }
        
        # Verificação "pré-inserção"
        for f in fields(self.model_cls):
            if f.name in self.uniquers:
                value = getattr(obj, f.name)
                if isinstance(value, Unique):
                    value = value.value
                if value in self.uniquers[f.name]._values:
                    raise ValueError(f"Unique constraint violated: {value}")
                
        for f in fields(self.model_cls):
            if f.name in self.uniquers:
                value = getattr(obj, f.name)
                if isinstance(value, Unique):
                    value = value.value
                self.uniquers[f.name].add(value)

        record["_id"] = len(self._data_cache) + 1
        self._data_cache.append(record)
        obj._id = record["_id"]
        return obj._id

    def get_all(self) -> List[T]:
        objs = []
        for record in self._data_cache:
            clean_record = {k: v for k, v in record.items() if k != "_table"}
            # DESSERIALIZAÇÃO automática
            for f in fields(self.model_cls):
                if f.name in clean_record:
                    clean_record[f.name] = deserialize_value(clean_record[f.name], f.type)
            objs.append(self.model_cls(**clean_record))
        return objs

    def get_by(self, key: str, value: Any) -> List[T]:
        objs = []
        for record in self._data_cache:
            if record.get(key) == value:
                clean_record = {k: v for k, v in record.items() if k != "_table"}
                for f in fields(self.model_cls):
                    if f.name in clean_record:
                        clean_record[f.name] = deserialize_value(clean_record[f.name], f.type)
                objs.append(self.model_cls(**clean_record))
        return objs

    def delete(self, _id: int) -> bool:
        record_to_delete = next((r for r in self._data_cache if r["_id"] == _id), None)
        if not record_to_delete:
            return False

        # Removing from JsonUniquer
        for f in fields(self.model_cls):
            if f.name in self.uniquers:
                val = record_to_delete.get(f.name)
                if isinstance(val, str) and get_origin(f.type) is Unique:
                    self.uniquers[f.name].remove(val)
                elif isinstance(val, Unique):
                    self.uniquers[f.name].remove(val.value)

        self._data_cache = [r for r in self._data_cache if r["_id"] != _id]
        return True

    def insert_many(self, objects: List[T]) -> List[int]:
        return [self.insert(obj) for obj in objects]

    def update(self, _id: int, new_obj: T) -> bool:
        if not isinstance(new_obj, self.model_cls):
            raise InvalidModel(f"Object must be of type {self.model_cls.__name__}")
        for idx, record in enumerate(self._data_cache):
            if record["_id"] == _id:
                updated_record = {f.name: serialize_value(getattr(new_obj, f.name)) for f in fields(new_obj)}
                updated_record["_id"] = _id
                self._data_cache[idx] = updated_record
                return True
        return False

    def update_many(self, updates: Dict[int, T]) -> int:
        count = 0
        for idx, record in enumerate(self._data_cache):
            _id = record.get("_id")
            if _id in updates:
                new_obj = updates[_id]
                if not isinstance(new_obj, self.model_cls):
                    raise InvalidModel(f"Object must be of type {self.model_cls.__name__}")
                updated_record = {f.name: serialize_value(getattr(new_obj, f.name)) for f in fields(new_obj)}
                updated_record["_id"] = _id
                self._data_cache[idx] = updated_record
                count += 1
        return count
