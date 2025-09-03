from .FastJsonDBerror import FastJsonDBError

class ForeignKeyError(FastJsonDBError):
    """Raised for invalid foreign key operations."""
    pass

class InvalidForeignKeyTypeError(ForeignKeyError, TypeError):
    """Raised when setting a foreign key with the wrong model type."""
    def __init__(self, expected, got):
        super().__init__(f"Expected {expected}, got {got}")
