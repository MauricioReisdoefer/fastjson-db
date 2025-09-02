from typing import Generic, TypeVar, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from fastjson_db.model import JsonModel

T = TypeVar("T", bound="JsonModel")

class ForeignKey(Generic[T]):
    def __init__(self, model_cls: Type[T], default: Optional[int] = None):
        self.model_cls = model_cls
        self._id = default

    def set(self, obj: T):
        """Seta a foreign key a partir de uma instância"""
        if not isinstance(obj, self.model_cls):
            raise TypeError(f"Expected {self.model_cls.__name__}, got {type(obj).__name__}")
        self._id = obj._id

    def get(self) -> Optional[T]:
        """Retorna a instância referenciada se existir"""
        from fastjson_db.model import TABLE_REGISTRY
        if self._id is None:
            return None
        table = TABLE_REGISTRY.get(self.model_cls)
        if table is None:
            raise ValueError(f"No table registered for {self.model_cls.__name__}")
        result = table.get_by("_id", self._id)
        return result[0] if result else None

    def __repr__(self):
        return f"ForeignKey({self.model_cls.__name__}, id={self._id})"
