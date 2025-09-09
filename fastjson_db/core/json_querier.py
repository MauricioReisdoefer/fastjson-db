from typing import List, Any, Dict, Callable
from fastjson_db.core.json_model import JsonModel
from fastjson_db.types import Field
from fastjson_db.core.json_table import JsonTable
from fastjson_db.errors import OperationError
from .b_tree import BTree

class JsonQuerier:
    """High-performance Querier for JsonTable with chained queries and automatic indices."""

    def __init__(self, table: JsonTable):
        self.table = table
        self._filters: List[Callable[[JsonModel], bool]] = []
        self._cache = table.cache
        self._fields_map: Dict[str, Field] = table.model._fields

        self._indices_hash: Dict[str, Dict[Any, JsonModel]] = {}
        self._indices_btree: Dict[str, BTree] = {}

    # ------------------ Load Cache / Build Indices ------------------ #
    def _load_cache(self):
        """Build hash maps and B-Trees for fast querying."""
        self._indices_hash.clear()
        self._indices_btree.clear()

        for field_name, field in self._fields_map.items():
            if getattr(field, "primary_key", False) or getattr(field, "unique", False):
                index = {}
                for obj in self._cache.values():
                    val = getattr(obj, field_name)
                    if val is not None:
                        key = field.serializer(val) if field.serializer else val
                        index[key] = obj
                self._indices_hash[field_name] = index
            else:
                btree = BTree()
                for obj in self._cache.values():
                    val = getattr(obj, field_name)
                    if val is not None:
                        key = field.serializer(val) if field.serializer else val
                        btree.insert(key, obj)
                self._indices_btree[field_name] = btree

    def filter(self, **conditions):
        """Add a filter condition. Supports chained calls."""
        def condition_fn(item: JsonModel):
            for key, value in conditions.items():
                if key not in self._fields_map:
                    raise OperationError("Filter Error", f"Field '{key}' does not exist in model")
                field = self._fields_map[key]
                obj_val = getattr(item, key)
                if field.serializer:
                    obj_val = field.serializer(obj_val)
                    value = field.serializer(value)
                if obj_val != value:
                    return False
            return True

        self._filters.append(condition_fn)
        return self

    def _get_candidates(self, conditions: Dict[str, Any]) -> List[JsonModel]:
        """Return a reduced set of objects using hash or B-Tree indices if possible."""
        candidates = None

        for key, value in conditions.items():
            if key in self._indices_hash:
                field = self._fields_map[key]
                if field.serializer:
                    value = field.serializer(value)
                obj = self._indices_hash[key].get(value)
                if obj:
                    candidates = [obj]
                else:
                    return []
                break

        # After B-Tree
        if candidates is None:
            for key, value in conditions.items():
                if key in self._indices_btree:
                    field = self._fields_map[key]
                    if field.serializer:
                        value = field.serializer(value)
                    candidates = self._indices_btree[key].search(value)
                    break

        if candidates is None:
            candidates = list(self._cache.values())

        return candidates

    # ------------------ Queries ------------------ #
    def get(self, **conditions) -> List[JsonModel]:
        if conditions:
            self.filter(**conditions)

        merged_filters = self._filters.copy()
        self._filters.clear()

        index_conditions = {k: v for k, v in conditions.items()
                            if k in self._indices_hash or k in self._indices_btree}
        candidates = self._get_candidates(index_conditions)

        return [obj for obj in candidates if all(f(obj) for f in merged_filters)]

    def first(self, **conditions) -> JsonModel | None:
        if conditions:
            self.filter(**conditions)

        merged_filters = self._filters.copy()
        self._filters.clear()

        index_conditions = {k: v for k, v in conditions.items()
                            if k in self._indices_hash or k in self._indices_btree}
        candidates = self._get_candidates(index_conditions)

        for obj in candidates:
            if all(f(obj) for f in merged_filters):
                return obj
        return None

    def count(self, **conditions) -> int:
        return len(self.get(**conditions))
