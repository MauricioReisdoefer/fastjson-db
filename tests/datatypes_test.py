# test_serializers.py
import datetime
import decimal
import pytest
from fastjson_db.datatypes.serializer import serialize_value, deserialize_value
from fastjson_db.datatypes.hashed import Hashed

def test_datetime():
    original = datetime.datetime(2025, 9, 4, 21, 30, 0)
    serialized = serialize_value(original)
    deserialized = deserialize_value(serialized, datetime.datetime)
    assert deserialized == original

def test_date():
    original = datetime.date(2025, 9, 4)
    serialized = serialize_value(original)
    deserialized = deserialize_value(serialized, datetime.date)
    assert deserialized == original

def test_decimal():
    original = decimal.Decimal("1234.5678")
    serialized = serialize_value(original)
    deserialized = deserialize_value(serialized, decimal.Decimal)
    assert deserialized == original

def test_list():
    original = [1, 2, 3, "a", "b"]
    serialized = serialize_value(original)
    deserialized = deserialize_value(serialized, list)
    assert deserialized == original

def test_dict():
    original = {"a": 1, "b": 2, "c": "text"}
    serialized = serialize_value(original)
    deserialized = deserialize_value(serialized, dict)
    assert deserialized == original

def test_text():
    original = "Hello, World!"
    serialized = serialize_value(original)
    deserialized = deserialize_value(serialized, str)
    assert deserialized == original

def test_hashed():
    original = Hashed("password", False)
    serialized = serialize_value(original)
    deserialized = deserialize_value(serialized, Hashed)
    assert str(deserialized) == str(original)
    assert deserialized.check("password")