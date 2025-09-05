# serializers.py
import datetime
import decimal
from typing import Any, Type, Dict, Callable

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

def serialize_value(value):
    t = type(value)
    if t in SERIALIZERS:
        return SERIALIZERS[t](value)
    return value

def deserialize_value(value, target_type=None):
    if target_type and target_type in DESERIALIZERS:
        return DESERIALIZERS[target_type](value)
    if isinstance(value, dict):
        return {k: deserialize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [deserialize_value(v) for v in value]
    return value
