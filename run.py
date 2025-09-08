from fastjson_db import JsonTable, JsonModel, Field

class User(JsonModel):
    id = Field(field_name="id", type=int, primary_key=True, unique=True)
    username = Field(field_name="username", type=str)

new_table = JsonTable(User, "users.json")
new_table._load_cache()

print(new_table.cache)