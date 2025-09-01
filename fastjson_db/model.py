from dataclasses import dataclass, field
from typing import Optional, TypeVar, Dict
from fastjson_db import JsonTable

T = TypeVar("T", bound="JsonModel")
TABLE_REGISTRY: Dict[type, "JsonTable"] = {}

@dataclass
class JsonModel:
    _id: Optional[int] = field(default=None, init=False, repr=False)
    _table: Optional["JsonTable"] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Liga a instância à tabela correta usando o registry."""
        cls = type(self)
        if self._table is None and cls in TABLE_REGISTRY:
            self._table = TABLE_REGISTRY[cls]