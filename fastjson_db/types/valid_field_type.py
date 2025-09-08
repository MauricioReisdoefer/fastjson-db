from fastjson_db.errors import FieldDatatypeError

VALID_RETURN_TYPES = (int, str, list, dict, float)

def check_return_type(func, attr_name):
    """Checks if validator, serializer and deserializer are valid"""
    if func is None:
        return
    test_val = 0 if attr_name == "validator" else None
    try:
        result = func(test_val)
    except Exception as e:
        raise FieldDatatypeError("Field creation error", f"{attr_name} raised an exception: {e}")
    
    if attr_name == "serializer":
        if type(result) not in VALID_RETURN_TYPES:
            raise FieldDatatypeError(
                "Field creation error",
                f"{attr_name} must return one of {VALID_RETURN_TYPES}, got {type(result)}"
            )
    elif attr_name == "deserializer":
        # Returns anything
        pass
    elif attr_name == "validator":
        if type(result) is not bool:
            raise FieldDatatypeError(
                "Field creation error",
                f"{attr_name} must return bool, got {type(result)}"
            )