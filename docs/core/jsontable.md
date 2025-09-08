# FastJson-DB JsonTables #

## Introduction ##

JsonTables are the "engine" of a single Table in the database. So, each of them should control only ONE Table in the entire database.

They need also to receive a `JsonModel` to verify the pattern of the .json table. See more about JsonModels here: [JsonModels](jsonmodel.md).

## How to Use JsonTables ##

### Importing JsonTables ###

To import get it directly from the FastJson-DB.

```py
from fastjson_db import JsonTables
```

### Creating a JsonTable ###

You need to import and create a subclass of the JsonModel, and then pass a path and the model you created as parameter.

```py
from fastjson_db import JsonTable, JsonModel, Field

class User(JsonModel):
    id = Field(field_name="id", type=int, primary_key=True, unique=True)
    username = Field(field_name="username", type=str)

new_table = JsonTable(User, "users.json")
```

This creates a JsonTable that manipulates the file "users.json", and use the User model as a pattern to insertion and manipulation of the database.
