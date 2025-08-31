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
    usuario_id: int  # Simulates a foreign key to Usuario._id
    _id: Optional[int] = None

# Tables
user_table = JsonTable("examples/users.json", Usuario)
post_table = JsonTable("examples/posts.json", Post)

# Create data if the table is empty
if not user_table.get_all():
    u1 = Usuario("Antonio", "antonio@example.com")
    u2 = Usuario("Maria", "maria@example.com")
    user_table.insert_many([u1, u2])

if not post_table.get_all():
    users = user_table.get_all()
    p1 = Post("First post", "Content of the first post", users[0]._id)
    p2 = Post("Second post", "Content of the second post", users[1]._id)
    post_table.insert_many([p1, p2])

# Show posts with their authors (relationship)
print("Posts with their authors:")
for post in post_table.get_all():
    author = user_table.get_by("_id", post.usuario_id)[0]
    print(f"{author.nome} wrote '{post.titulo}': {post.conteudo}")

# Optional: clean up JSON files after testing
if os.path.exists("examples/users.json"):
    os.remove("examples/users.json")
if os.path.exists("examples/posts.json"):
    os.remove("examples/posts.json")
