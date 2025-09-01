from fastjson_db import JsonModel, TABLE_REGISTRY, JsonTable
from dataclasses import dataclass
from typing import Optional

@dataclass
class User(JsonModel):
    _id: Optional[int] = 0
    _table: Optional[JsonTable]
    name: str = ""
    password: str = ""
    
user = User(name="Allan", password="123")

user_table = JsonTable("users.json", User)
TABLE_REGISTRY[User] = user_table

user_table.insert(user) 
user_table.flush()

print(user_table.get_all())