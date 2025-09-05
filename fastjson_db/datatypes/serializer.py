# serializers.py
import datetime
import decimal
from typing import Any, Type, Dict, Callable, get_origin, get_args, Union
from fastjson_db.foreignkey import ForeignKey
from fastjson_db.errors.datatype_error import DataTypeError
from fastjson_db.datatypes.hashed import Hashed

# Registry global de tipos
SERIALIZERS: Dict[Type, Callable[[Any], Any]] = {}
DESERIALIZERS: Dict[Type, Callable[[Any], Any]] = {}

# Registrando tipos básicos

# Str e int não precisam de transformação
SERIALIZERS[str] = lambda v: v
DESERIALIZERS[str] = lambda v: v

SERIALIZERS[int] = lambda v: v
DESERIALIZERS[int] = lambda v: v

SERIALIZERS[float] = lambda v: v
DESERIALIZERS[float] = lambda v: v

# Decimal
SERIALIZERS[decimal.Decimal] = lambda v: str(v)
DESERIALIZERS[decimal.Decimal] = lambda v: decimal.Decimal(v)

# Datetime
SERIALIZERS[datetime.datetime] = lambda v: v.isoformat()
DESERIALIZERS[datetime.datetime] = lambda v: datetime.datetime.fromisoformat(v)

# Date
SERIALIZERS[datetime.date] = lambda v: v.isoformat()
DESERIALIZERS[datetime.date] = lambda v: datetime.date.fromisoformat(v)

# List genérica
SERIALIZERS[list] = lambda v: [serialize_value(i) for i in v]
DESERIALIZERS[list] = lambda v: [deserialize_value(i) for i in v]

# Dict genérico
SERIALIZERS[dict] = lambda v: {k: serialize_value(val) for k, val in v.items()}
DESERIALIZERS[dict] = lambda v: {k: deserialize_value(val) for k, val in v.items()}

SERIALIZERS[type(None)] = lambda v: None
DESERIALIZERS[type(None)] = lambda v: None

SERIALIZERS[ForeignKey] = lambda fk: fk._id
DESERIALIZERS[ForeignKey] = lambda v: ForeignKey(None, id=v)

SERIALIZERS[Hashed] = lambda v: str(v)
DESERIALIZERS[Hashed] = lambda v: Hashed(v, already_hashed=True)

def serialize_value(value):
    t = type(value)
    if t in SERIALIZERS:
        return SERIALIZERS[t](value)
    raise DataTypeError(f"Unsupported datatype for serialization: {t.__name__}")

def deserialize_value(value, target_type=None):
    import types
    if target_type:
        origin = get_origin(target_type)
        if origin is Union or isinstance(target_type, types.UnionType):
            args = get_args(target_type)
            for arg in args:
                if arg is type(None) and value is None:
                    return None
                if arg in DESERIALIZERS:
                    return DESERIALIZERS[arg](value)
            return value
        if target_type in DESERIALIZERS:
            return DESERIALIZERS[target_type](value)
        raise DataTypeError(f"Unsupported datatype for deserialization: {target_type}")
    return value