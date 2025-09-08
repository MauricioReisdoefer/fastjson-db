from typing import Optional, Any, Callable, get_args, get_origin, List, Dict, TypeVar
from dataclasses import dataclass
from fastjson_db.errors import FieldDatatypeError
from .valid_field_type import check_return_type

T = TypeVar("TypeVar")

@dataclass
class Field():
    """Create a new personalized field in the Table"""
    
    # Obrigatory Fields #
    field_name : str
    type: Any
    
    # Optional Fields #
    foreign_key : int = None
    unique : bool = False
    primary_key : bool = False
    validator: Optional[Callable[[Any], Any]] = None
    serializer: Optional[Callable[[Any], Any]] = None
    deserializer: Optional[Callable[[Any], Any]] = None
    
    def __post_init__(self):
        """Makes various validations for every field"""
        # Validate field_name
        if not isinstance(self.field_name, str) or not self.field_name:
            raise FieldDatatypeError("Field creation error", "'field_name' MUST be a 'str'")
        
        # Validate type
        if not isinstance(self.type, type) and get_origin(self.type) is None:
            raise FieldDatatypeError("Field creation error", "'type' MUST be a 'type' or a typing generic (List[], Dict[])")
        
        # Validate booleans
        if not isinstance(self.unique, bool):
            raise FieldDatatypeError("Field creation error", "'unique' MUST be a 'bool'")
        if not isinstance(self.primary_key, bool):
            raise FieldDatatypeError("Field creation error", "'primary_key' MUST be a 'bool'")
        
        # Validate foreign_key
        if self.foreign_key is not None and not isinstance(self.foreign_key, str):
            raise FieldDatatypeError("Field creation error", "'foreign_key' MUST be a 'str'")
        
        # Make sure primary_key is unique
        if self.primary_key and self.unique is False:
            raise FieldDatatypeError("Field creation error", "if field is primary_key it MUST be 'unique=True'")
        
        # Checks if it's not List[T] or Dict[T, T] (Typed)
        if self.type in [list, dict]:
            origin = get_origin(self.type)
            args = get_args(self.type)
            if origin is None or not args:
                raise FieldDatatypeError(
                    "Field creation error",
                    f"{self.field_name} of type {self.type} must be typed (List[...] or Dict[...])"
                )
        
        origin = get_origin(self.type)
        if self.type in [int, str] or origin in [list, dict]:
            atributes = ['validator']
        else:
            # For native types, they are not, and validator is optional
            atributes = ['serializer', 'deserializer', 'validator']
        
        # Tests if attributes are correctly initializated
        for attr_name in atributes:
            attr = getattr(self, attr_name)
            if attr is None:
                if attr_name in ['serializer', 'deserializer']:
                    raise FieldDatatypeError("Field creation error", f"{attr_name} is obligatory in personalized types")
            elif not callable(attr):
                raise FieldDatatypeError("Field creation error", f"{attr_name} should be callable")
            else:
                check_return_type(attr, attr_name)