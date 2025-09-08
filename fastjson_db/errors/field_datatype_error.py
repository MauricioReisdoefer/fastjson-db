from .fastjsondb_error import FastJsonError

class FieldDatatypeError(FastJsonError):
    """Describes an error of Field"""
    
    def __init__(self, specific_message:str, field_error:str):
        full_message = f"{specific_message} | FieldDataTypeError: {field_error}"
        super().__init__(full_message)