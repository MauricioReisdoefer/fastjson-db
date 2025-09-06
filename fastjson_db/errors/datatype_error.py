from .FastJsonDBerror import FastJsonDBError

class DataTypeError(FastJsonDBError):
    """When a datatype is incorrectly used"""
    pass

class NotUniqueTypeError(DataTypeError):
    """When a unique value is not unique"""
    pass