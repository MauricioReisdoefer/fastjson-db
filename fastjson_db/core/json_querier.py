from typing import List, Any, Dict, Callable
from fastjson_db.core.json_model import JsonModel
from fastjson_db.types import Field
from fastjson_db.core.json_table import JsonTable
from fastjson_db.errors import OperationError

class JsonQuerier:
    """High-performance Querier for JsonTable with chained queries and automatic indices."""

    def __init__(self, table: JsonTable):
        self.table = table
        self._filters: List[Callable[[JsonModel], bool]] = []
        self._cache = table.cache
        self._fields_map: Dict[str, Field] = table.model._fields

        # ------------------ Build indices ------------------ #
        # unique or primary_key → HashMap
        # others → (future) B-Tree for range queries
        self._indices: Dict[str, Dict[Any, JsonModel]] = {}
        for field_name, field in self._fields_map.items():
            if getattr(field, "primary_key", False) or getattr(field, "unique", False):
                index = {}
                for obj in self._cache.values():
                    val = getattr(obj, field_name)
                    if val is not None:
                        # Use serializer if exists
                        if field.serializer:
                            key = field.serializer(val)
                        else:
                            key = val
                        index[key] = obj
                self._indices[field_name] = index

    def filter(self, **conditions):
        """Add a filter condition. Supports chained calls."""
        def condition_fn(item: JsonModel):
            for key, value in conditions.items():
                if key not in self._fields_map:
                    raise OperationError("Filter Error", f"Field '{key}' does not exist in model")
                field = self._fields_map[key]
                obj_val = getattr(item, key)
                # Apply serializer if exists
                if field.serializer:
                    obj_val = field.serializer(obj_val)
                    value = field.serializer(value)
                if obj_val != value:
                    return False
            return True

        self._filters.append(condition_fn)
        return self
    
    def _get_candidates(self, conditions: Dict[str, Any]) -> List[JsonModel]:
        """Return a reduced set of objects using hash indices if possible."""
        candidates = None

        # Try to use a hash index
        for key, value in conditions.items():
            if key in self._indices:
                field = self._fields_map[key]
                if field.serializer:
                    value = field.serializer(value)
                obj = self._indices[key].get(value)
                if obj:
                    candidates = [obj]
                else:
                    return []  # no match
                break

        if candidates is None:
            candidates = list(self._cache.values())

        return candidates

    def get(self, **conditions) -> List[JsonModel]:
        """Get all objects matching the conditions, supporting chained filters."""
        if conditions:
            self.filter(**conditions)

        merged_filters = self._filters.copy()
        self._filters.clear()

        # Use indices if possible
        index_conditions = {k: v for k, v in conditions.items() if k in self._indices}
        candidates = self._get_candidates(index_conditions)

        # Apply remaining filters
        return [obj for obj in candidates if all(f(obj) for f in merged_filters)]

    def first(self, **conditions) -> JsonModel | None:
        """Return the first object matching the conditions (or None)."""
        if conditions:
            self.filter(**conditions)

        merged_filters = self._filters.copy()
        self._filters.clear()

        index_conditions = {k: v for k, v in conditions.items() if k in self._indices}
        candidates = self._get_candidates(index_conditions)

        for obj in candidates:
            if all(f(obj) for f in merged_filters):
                return obj
        return None

    def count(self, **conditions) -> int:
        """Count all objects matching the conditions."""
        return len(self.get(**conditions))
