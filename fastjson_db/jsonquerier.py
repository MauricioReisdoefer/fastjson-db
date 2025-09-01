from typing import Any, Dict, List, Optional, Callable, TypeVar
from .jsontable import JsonTable
T = TypeVar("T")

class JsonQuerier:
    """
    Provides advanced querying capabilities over a JsonTable.
    """

    def __init__(self, table: JsonTable):
        self.table = table

    def filter(self, **conditions: Any) -> List[T]:
        """
        Returns all objects that match all conditions.

        Example:
            querier.filter(nome="Antonio", idade=50)
        """
        results = self.table.get_all()
        for key, value in conditions.items():
            results = [obj for obj in results if getattr(obj, key) == value]
        return results

    def exclude(self, **conditions: Any) -> List[T]:
        """
        Returns all objects that do NOT match the given conditions.
        """
        results = self.table.get_all()
        for key, value in conditions.items():
            results = [obj for obj in results if getattr(obj, key) != value]
        return results

    def custom(self, func: Callable[[T], bool]) -> List[T]:
        """
        Returns all objects that satisfy a custom function.
        Example:
            querier.custom(lambda u: u.idade > 30)
        """
        return [obj for obj in self.table.get_all() if func(obj)]

    def get_first(self, **conditions: Any) -> Optional[T]:
        """
        Returns the first object that matches the conditions, or None if not found.
        """
        filtered = self.filter(**conditions)
        return filtered[0] if filtered else None

    def order_by(self, key: str, reverse: bool = False) -> List[T]:
        """
        Returns all objects ordered by the given key.
        """
        return sorted(self.table.get_all(), key=lambda obj: getattr(obj, key), reverse=reverse)
