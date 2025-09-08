from typing import Dict
from fastjson_db.types import Field
from fastjson_db.errors import BadTypingError
from fastjson_db.core.json_model_meta import JsonModelMeta

class JsonModel(metaclass=JsonModelMeta):
    """Base Model for all Models in FastJson-DB"""
    _fields: Dict[str, Field]

    def __init__(self, **kwargs):
        for field_name, field in self._fields.items():
            if field_name in kwargs:
                value = kwargs[field_name]

                if not isinstance(value, field.type):
                    raise BadTypingError(
                        "Bad Typing",
                        f"Field '{field_name}' must be {field.type.__name__}, got {type(value).__name__}"
                    )
                if field.validator and not field.validator(value):
                    raise ValueError(f"Validation failed for field '{field_name}'")

                setattr(self, field_name, value)
            else:
                setattr(self, field_name, None)

    def to_json(self):
        result = {}
        for name, field in self._fields.items():
            value = getattr(self, name)
            if field.serializer:
                result[name] = field.serializer(value)
            else:
                result[name] = value
        return result