import sys
import os
sys.path.append(os.path.abspath("../jsonlite")) # Adjustment to find jsonlite package

# -- Example -- #

from dataclasses import dataclass
from typing import Optional
from jsonlite import JsonTable
import os

@dataclass
class Usuario:
    nome: str
    email: str
    idade: int
    _id: Optional[int] = None # Only used to store the user ID after insertion, not needed (and not used) when creating a new user

    def __repr__(self):
        return f'User {self.nome} | ID: {self._id} | Email: {self.email} | Age: {self.idade}'

# Create user table (with .json)
user_table = JsonTable("examples/users.json", Usuario)

# Create an user in user table
user = Usuario(nome="Antonio", email="antonio@example.com", idade=50)
user_table.insert(user)

# Shows every user in this table
for u in user_table.get_all():
    print(u)

# (Optional, but for tests) Destroying table users.json
if os.path.exists("examples/users.json"):
        os.remove("examples/users.json")