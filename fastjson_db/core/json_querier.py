from typing import List, Any, Dict, Callable
from fastjson_db.core.json_model import JsonModel
from fastjson_db.types import Field
from fastjson_db.core.json_table import JsonTable
from fastjson_db.errors import OperationError


class JsonQuerier:
    """High-performance Querier for JsonTable with support for chained queries and automatic indices."""

    def __init__(self, table: JsonTable):
        self.table = table
        self._filters: List[Callable[[JsonModel], bool]] = []
        self._cache = table.cache
        self._fields_map: Dict[str, Field] = table.model._fields

        # Only for fields that are primary_key or unique
        self._indices: Dict[str, Dict[Any, JsonModel]] = {}
        for field_name, field in self._fields_map.items():
            if getattr(field, "primary_key", False) or getattr(field, "unique", False):
                index = {}
                for obj in self._cache.values():
                    key = getattr(obj, field_name)
                    if key is not None:
                        index[key] = obj
                self._indices[field_name] = index

    def filter(self, **conditions):
        """
        Add a filter condition. Supports chained calls.
        Example: .filter(name="John", age=30)
        """
        def condition_fn(item: JsonModel):
            for key, value in conditions.items():
                if key not in self._fields_map:
                    raise OperationError("Filter Error", f"Field '{key}' does not exist in model")
                if getattr(item, key) != value:
                    return False
            return True

        self._filters.append(condition_fn)
        return self

    def _get_candidates(self, conditions: Dict[str, Any]) -> List[JsonModel]:
        """Return a reduced set of objects using indices if possible."""
        candidates = None

        # Check if any condition can use an index
        for key, value in conditions.items():
            if key in self._indices:
                obj = self._indices[key].get(value)
                if obj:
                    candidates = [obj]
                else:
                    return []  # indexed field not found
                break

        # If no index used, start with all objects
        if candidates is None:
            candidates = list(self._cache.values())

        return candidates

    def get(self, **conditions) -> List[JsonModel]:
        """
        Get all objects matching the conditions.
        Supports chained filters.
        """
        if conditions:
            self.filter(**conditions)

        # Merge all filters as one for efficiency
        merged_filters = self._filters.copy()
        self._filters.clear()

        # Attempt to use indexed fields first
        index_conditions = {k: v for k, v in conditions.items() if k in self._indices}
        candidates = self._get_candidates(index_conditions)

        # Apply remaining filters
        result = [obj for obj in candidates if all(f(obj) for f in merged_filters)]
        return result

    def first(self, **conditions) -> JsonModel | None:
        """
        Return the first object matching the conditions (or None)
        """
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
        """
        Count all objects matching the conditions
        """
        return len(self.get(**conditions))
