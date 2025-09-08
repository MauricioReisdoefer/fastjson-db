from .fastjsondb_error import FastJsonError

class BadTypingError(FastJsonError):
    """Describes a typing error"""
    
    def __init__(self, specific_message:str, field_error:str):
        full_message = f"{specific_message} | BadTypingError: {field_error}"
        super().__init__(full_message)