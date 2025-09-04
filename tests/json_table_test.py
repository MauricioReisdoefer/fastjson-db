import os
import tempfile
import pytest
from dataclasses import dataclass
from fastjson_db import JsonModel, JsonTable
from fastjson_db.errors.model_table_errors import NotDataclassModelError, InvalidModel


# ---- Modelo de exemplo ----
@dataclass
class User(JsonModel):
    _id: int | None = None
    name: str = ""
    age: int = 0


# ---- FIXTURE PARA ARQUIVO TEMP ----
@pytest.fixture
def temp_table():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    table = JsonTable(path, User)
    yield table
    os.remove(path)


# ---- TESTES ----

def test_not_dataclass_error():
    class NotData:
        _id: int
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    with pytest.raises(NotDataclassModelError):
        JsonTable(path, NotData)
    os.remove(path)


def test_invalid_model_error():
    @dataclass
    class BadModel:
        _id: int | None
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    with pytest.raises(InvalidModel):
        JsonTable(path, BadModel)
    os.remove(path)


def test_insert_and_get_all(temp_table):
    user = User(name="Alice", age=30)
    _id = temp_table.insert(user)
    assert _id == 1
    all_users = temp_table.get_all()
    assert len(all_users) == 1
    assert all_users[0].name == "Alice"


def test_insert_many(temp_table):
    users = [User(name="Bob", age=25), User(name="Charlie", age=40)]
    ids = temp_table.insert_many(users)
    assert ids == [1, 2]
    all_users = temp_table.get_all()
    assert len(all_users) == 2


def test_get_by(temp_table):
    temp_table.insert(User(name="Diana", age=20))
    temp_table.insert(User(name="Eve", age=22))
    result = temp_table.get_by("name", "Eve")
    assert len(result) == 1
    assert result[0].name == "Eve"


def test_update(temp_table):
    user = User(name="Frank", age=35)
    _id = temp_table.insert(user)
    updated_user = User(name="Frank Updated", age=36)
    ok = temp_table.update(_id, updated_user)
    assert ok
    all_users = temp_table.get_all()
    assert all_users[0].name == "Frank Updated"


def test_update_many(temp_table):
    u1 = User(name="Gina", age=28)
    u2 = User(name="Hank", age=33)
    id1 = temp_table.insert(u1)
    id2 = temp_table.insert(u2)
    updates = {
        id1: User(name="Gina Updated", age=29),
        id2: User(name="Hank Updated", age=34),
    }
    count = temp_table.update_many(updates)
    assert count == 2
    all_users = temp_table.get_all()
    names = [u.name for u in all_users]
    assert "Gina Updated" in names
    assert "Hank Updated" in names


def test_delete(temp_table):
    user = User(name="Ivan", age=50)
    _id = temp_table.insert(user)
    deleted = temp_table.delete(_id)
    assert deleted
    assert temp_table.get_all() == []


def test_flush_and_reload(temp_table):
    user = User(name="Jack", age=27)
    temp_table.insert(user)
    temp_table.flush() 
    
    new_table = JsonTable(temp_table.path, User)
    all_users = new_table.get_all()
    assert len(all_users) == 1
    assert all_users[0].name == "Jack"
