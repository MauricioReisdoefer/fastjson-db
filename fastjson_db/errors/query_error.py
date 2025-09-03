from .FastJsonDBerror import FastJsonDBError

class StorageError(FastJsonDBError):
    """Raised when there are issues reading/writing JSON files."""
    pass
