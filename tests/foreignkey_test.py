import pytest
from dataclasses import dataclass

from fastjson_db.model import JsonModel, TABLE_REGISTRY
from fastjson_db.jsontable import JsonTable
from fastjson_db.foreignkey import ForeignKey


# -------- MODELOS --------
@dataclass
class User(JsonModel):
    _id: int = 0
    name: str = ""


@dataclass
class Restaurant(JsonModel):
    _id: int = 0
    name: str = ""
    owner: ForeignKey[User] = ForeignKey(User)


@dataclass
class Product(JsonModel):
    _id: int = 0
    name: str = ""


# -------- FIXTURES --------
@pytest.fixture(autouse=True)
def clean_registry(tmp_path):
    """Reseta TABLE_REGISTRY e usa arquivos temporários em cada teste"""
    TABLE_REGISTRY.clear()

    user_table = JsonTable(tmp_path / "users.json", User)
    TABLE_REGISTRY[User] = user_table

    rest_table = JsonTable(tmp_path / "restaurants.json", Restaurant)
    TABLE_REGISTRY[Restaurant] = rest_table

    prod_table = JsonTable(tmp_path / "products.json", Product)
    TABLE_REGISTRY[Product] = prod_table

    yield user_table, rest_table, prod_table

    TABLE_REGISTRY.clear()


# -------- TESTES --------
def test_foreignkey_rejects_invalid_model(clean_registry):
    """Deve rejeitar um objeto de classe errada"""
    _, rest_table, prod_table = clean_registry

    user = User(name="Allan")
    TABLE_REGISTRY[User].insert(user)

    restaurant = Restaurant(name="Sabor da Serra")

    product = Product(name="Pizza")
    TABLE_REGISTRY[Product].insert(product)

    with pytest.raises(TypeError):
        restaurant.owner.set(product)


def test_foreignkey_relationship_works(clean_registry):
    """Deve aceitar User e conseguir buscá-lo pelo FK"""
    user_table, rest_table, _ = clean_registry

    user = User(name="Maria")
    user_table.insert(user)

    restaurant = Restaurant(name="Delícia Mineira")
    restaurant.owner.set(user)
    rest_table.insert(restaurant)

    # Buscar via FK
    owner = restaurant.owner.get()
    assert owner is not None
    assert owner.name == "Maria"


def test_foreignkey_broken_after_delete(clean_registry):
    """Se o User for deletado, o restaurante não deve mais resolver o FK"""
    user_table, rest_table, _ = clean_registry

    user = User(name="Carlos")
    user_table.insert(user)

    restaurant = Restaurant(name="Churrascaria do Zé")
    restaurant.owner.set(user)
    rest_table.insert(restaurant)
    user_table.delete(user._id)

    assert restaurant.owner.get() is None
