import os
import tempfile
import pytest
from dataclasses import dataclass
from fastjson_db import JsonModel, JsonTable
from fastjson_db.jsonquerier import JsonQuerier


# ---- Modelo de exemplo ----
@dataclass
class User(JsonModel):
    _id: int | None = None
    name: str = ""
    age: int = 0


# ---- FIXTURE COM JsonQuerier ----
@pytest.fixture
def querier():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    with open(path, "wb") as f:
        f.write(b"[]")

    table = JsonTable(path, User)
    q = JsonQuerier(table)

    # insere alguns dados
    table.insert_many([
        User(name="Alice", age=30),
        User(name="Bob", age=25),
        User(name="Charlie", age=40),
        User(name="Diana", age=25),
    ])

    yield q

    os.remove(path)


# ---- TESTES ----

def test_filter_by_single_field(querier):
    result = querier.filter(age=25)
    assert len(result) == 2
    names = {u.name for u in result}
    assert names == {"Bob", "Diana"}


def test_filter_by_multiple_fields(querier):
    result = querier.filter(name="Alice", age=30)
    assert len(result) == 1
    assert result[0].name == "Alice"


def test_exclude(querier):
    result = querier.exclude(age=25)
    ages = {u.age for u in result}
    assert 25 not in ages
    assert len(result) == 2


def test_custom_function(querier):
    result = querier.custom(lambda u: u.age > 30)
    names = {u.name for u in result}
    assert names == {"Charlie"}


def test_get_first_found(querier):
    user = querier.get_first(age=25)
    assert user is not None
    assert user.age == 25


def test_get_first_not_found(querier):
    user = querier.get_first(name="Zoe")
    assert user is None


def test_order_by_ascending(querier):
    result = querier.order_by("age")
    ages = [u.age for u in result]
    assert ages == sorted(ages)


def test_order_by_descending(querier):
    result = querier.order_by("age", reverse=True)
    ages = [u.age for u in result]
    assert ages == sorted(ages, reverse=True)
