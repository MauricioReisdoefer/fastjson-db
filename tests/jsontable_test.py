import os
import pytest
from dataclasses import dataclass
from typing import Optional
from jsonlite import JsonTable  # substitua pelo nome do arquivo onde está o JsonTable

TEST_FILE = "test_db.json"

@dataclass
class Usuario:
    nome: str
    senha: str
    email: str
    idade: int
    cidade: str
    _id: Optional[int] = None

@pytest.fixture
def limpa_tabela():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_insert_get_all(limpa_tabela):
    tabela = JsonTable(TEST_FILE, Usuario)
    user = Usuario("someone", "123", "someemail@something.com", 50, "somecity")
    tabela.insert(user)

    todos = tabela.get_all()
    assert len(todos) == 1
    assert todos[0].nome == "someone"

def test_get_by(limpa_tabela):
    tabela = JsonTable(TEST_FILE, Usuario)
    user = Usuario("someone", "123", "someemail@something.com", 50, "somecity")
    tabela.insert(user)

    encontrados = tabela.get_by("nome", "someone")
    assert len(encontrados) == 1
    assert encontrados[0].email == "someemail@something.com"

def test_update(limpa_tabela):
    tabela = JsonTable(TEST_FILE, Usuario)
    user = Usuario("someone", "123", "someemail@something.com", 50, "somecity")
    user_id = tabela.insert(user)

    novo_user = Usuario("someone", "456", "novo_email@teste.com", 51, "São Paulo")
    updated = tabela.update(user_id, novo_user)
    assert updated

    atualizado = tabela.get_by("_id", user_id)[0]
    assert atualizado.senha == "456"
    assert atualizado.email == "novo_email@teste.com"

def test_delete(limpa_tabela):
    tabela = JsonTable(TEST_FILE, Usuario)
    user = Usuario("someone", "123", "someemail@something.com", 50, "somecity")
    user_id = tabela.insert(user)

    deletado = tabela.delete(user_id)
    assert deletado

    todos = tabela.get_all()
    assert len(todos) == 0
