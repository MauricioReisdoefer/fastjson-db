from fastjson_db import JsonModel, JsonTable
from dataclasses import dataclass

@dataclass
class User(JsonModel):
    _id: int | None = None
    name: str = ""
    age: int = 0

user_table = JsonTable("users.json", User)

new_user = User(
    _id = 0,
    name = "Allan",
    age = 17
)

new_user2 = User(
    _id = 0,
    name = "Jorge",
    age = 18
)

user_table.insert(new_user)
user_table.insert(new_user2)

user_table.update(1, User(_id=0,name="OtherName",age=15))
print(user_table.get_all())
print(user_table.get_by("name", "OtherName"))
user_table.flush()