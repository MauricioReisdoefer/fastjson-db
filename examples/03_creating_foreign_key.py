import sys
import os
sys.path.append(os.path.abspath("../jsonlite"))

from dataclasses import dataclass
from typing import Optional
from jsonlite import JsonTable

@dataclass
class Usuario:
    nome: str
    email: str
    _id: Optional[int] = None  # Only used to store the user ID after insertion

@dataclass
class Post:
    titulo: str
    conteudo: str
    usuario_id: int  # Simulate a foreign key
    _id: Optional[int] = None

# Creating tables
user_table = JsonTable("examples/users.json", Usuario)
post_table = JsonTable("examples/posts.json", Post)

# Creating fake users
if not user_table.get_all():
    u1 = Usuario("Antonio", "antonio@example.com")
    u2 = Usuario("Maria", "maria@example.com")
    user_table.insert_many([u1, u2])

# Creating posts with user id keys
users = user_table.get_all()
p1 = Post("Primeiro post", "Conteúdo do primeiro post", users[0]._id)
p2 = Post("Segundo post", "Conteúdo do segundo post", users[1]._id)
post_table.insert_many([p1, p2])

print("Posts criados com referência ao usuário (_id):")
for post in post_table.get_all():
    print(post)

# (Optional, but for tests) Destroying table users.json and table posts.json
if os.path.exists("examples/users.json"):
    os.remove("examples/users.json")
if os.path.exists("examples/posts.json"):
    os.remove("examples/posts.json")
