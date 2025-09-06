from typing import Generic, TypeVar

T = TypeVar("T")

class Unique(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Unique):
            return self.value == other.value
        return False

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Unique({self.value!r})"
