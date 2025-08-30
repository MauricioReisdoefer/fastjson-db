import sys
import os
sys.path.append(os.path.abspath("../jsonlite"))  # Adjustment to find jsonlite package

# -- Example -- #

from dataclasses import dataclass
from typing import Optional
from jsonlite import JsonTable

@dataclass
class Usuario:
    nome: str
    email: str
    idade: int
    _id: Optional[int] = None  # Only used to store the user ID after insertion
    
    def __repr__(self):
        return f'User {self.nome} | ID: {self._id} | Email: {self.email} | Age: {self.idade}'
    
user_table = JsonTable("examples/users.json", Usuario)

# If user table is empty, insert 2 new users
if not user_table.get_all():
    user_table.insert(Usuario("Antonio", "antonio@example.com", 50))
    user_table.insert(Usuario("Maria", "maria@example.com", 30))

# Find an user by name (Returns a List)
users = user_table.get_by("nome", "Antonio")
if users:
    user = users[0]
    print("Before update: ", user)

    # Update user's age
    user.idade = 51
    user_table.update(user._id, user)

    # Show updated user
    updated_user = user_table.get_by("_id", user._id)[0]
    print("After update:", updated_user)

# Delete user by name
users_to_delete = user_table.get_by("nome", "Maria")
if users_to_delete:
    user_table.delete(users_to_delete[0]._id)
    print("Table after deleting Maria: ")
    for u in user_table.get_all():
        print(u)

# (Opcional) limpar arquivo após teste
if os.path.exists("examples/users.json"):
    os.remove("examples/users.json")