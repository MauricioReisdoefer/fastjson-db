from fastjson_db import JsonModel, Field
from fastjson_db.core.json_table import JsonTable

class User(JsonModel):
    id = Field(field_name="id", type=int, primary_key=True, unique=True)
    username = Field(field_name="username", type=str)
    
new_user = User(id=1, username="lixo")
print(new_user.to_json())

table = JsonTable(User, "users.json")