from typing import Dict
from fastjson_db.types import Field

class JsonModelMeta(type):
    """Metaclass for JsonModel"""
    def __new__(mcs, name, bases, namespace):
        fields: Dict[str, Field] = {}

        for attr_name, attr_value in list(namespace.items()):
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value

        namespace["_fields"] = fields
        return super().__new__(mcs, name, bases, namespace)