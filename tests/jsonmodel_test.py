import os
import tempfile
import pytest
from dataclasses import dataclass
from fastjson_db import JsonTable
from fastjson_db import JsonModel, TABLE_REGISTRY

# Classe de exemplo
@dataclass
class User(JsonModel):
    _id: int = 0
    name: str = ""
    email: str = ""


def test_jsonmodel_inheritance_and_registry():
    # cria arquivo temporário para a tabela
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "users.json")

        # registra a tabela no registry
        user_table = JsonTable(db_path, User)
        TABLE_REGISTRY[User] = user_table

        # instancia o modelo
        u = User(name="Alice", email="alice@example.com")

        # verifica os atributos internos
        assert u._id is not None, "Novo objeto deve começar com _id"
        assert u._table is user_table, "_table deve ser ligado automaticamente pelo registry"
