import os
import tempfile
import pytest
from dataclasses import dataclass
from fastjson_db import JsonModel, JsonTable
from fastjson_db.datatypes.unique import Unique
from fastjson_db.jsonuniquer import JsonUniquer


# ---- Modelo com Unique ----
@dataclass
class UserUnique(JsonModel):
    _id: int | None = None
    username: Unique[str] = None
    age: int = 0

@pytest.fixture(autouse=True)
def reset_juniquers(monkeypatch):
    """
    Limpa todos os JsonUniquer para evitar conflito de Unique entre testes.
    Essa fixture é automática para todos os testes (autouse=True).
    """
    original_init = JsonUniquer.__init__

    def patched_init(self, base_path: str, table_name: str, field_name: str):
        original_init(self, base_path, table_name, field_name)
        self._values.clear()
        self._flush()

    monkeypatch.setattr(JsonUniquer, "__init__", patched_init)

@pytest.fixture
def temp_unique_table():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    table = JsonTable(path, UserUnique)
    yield table
    os.remove(path)


# ---- TESTES ----

def test_insert_unique_success(temp_unique_table):
    user1 = UserUnique(username=Unique("alice"), age=20)
    user2 = UserUnique(username=Unique("bob"), age=25)

    id1 = temp_unique_table.insert(user1)
    id2 = temp_unique_table.insert(user2)

    assert id1 == 1
    assert id2 == 2
    users = temp_unique_table.get_all()
    assert [u.username.value for u in users] == ["alice", "bob"]


def test_insert_unique_violation(temp_unique_table):
    user1 = UserUnique(username=Unique("charlie"), age=30)
    temp_unique_table.insert(user1)

    user2 = UserUnique(username=Unique("charlie"), age=35)
    with pytest.raises(ValueError, match="Unique constraint violated"):
        temp_unique_table.insert(user2)


def test_delete_releases_unique(temp_unique_table):
    user1 = UserUnique(username=Unique("diana"), age=40)
    _id = temp_unique_table.insert(user1)

    assert temp_unique_table.delete(_id)
    user2 = UserUnique(username=Unique("diana"), age=45)
    new_id = temp_unique_table.insert(user2)
    assert new_id == 1 
