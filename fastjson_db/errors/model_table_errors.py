from .FastJsonDBerror import FastJsonDBError

class NotDataclassModelError(FastJsonDBError):
    """Raised for issues related to JsonModel usage."""
    pass

class TableError(FastJsonDBError):
    """Raised for errors related to JsonTable operations."""
    pass

class TableNotRegisteredError(TableError):
    """Raised when trying to access a model/table not registered."""
    def __init__(self, model_cls):
        super().__init__(f"No table registered for model {model_cls.__name__}")

class InvalidModel(TableError):
    """Raised for errors related to invalid model in tables."""
    pass