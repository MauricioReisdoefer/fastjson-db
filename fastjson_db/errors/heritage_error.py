from .fastjsondb_error import FastJsonError

class HeritageError(FastJsonError):
    """Describes a Class Heritage Error"""
    
    def __init__(self, specific_message:str, field_error:str):
        full_message = f"{specific_message} | Heritage Error: {field_error}"
        super().__init__(full_message)