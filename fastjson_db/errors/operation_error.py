from .fastjsondb_error import FastJsonError

class OperationError(FastJsonError):
    """Describes a Database Operation Error"""
    
    def __init__(self, specific_message:str, field_error:str):
        full_message = f"{specific_message} | Operation Error: {field_error}"
        super().__init__(full_message)