# FastJson-DB JsonModels #

## Introduction ##

FastJson-DB uses JsonModels to interpretate how the Tables should work. It's like the JsonTable "rule book", on how every field should be serializated, deserializated and returned.

## Using JsonModels ##

### Importing ###

To import `JsonModel`, simply use:

```py
from fastjson_db import JsonModel
```

### Using Class Heritage ###

JsonModel should be used as a "parent" class. So your Models MUST be a JsonModel subclass. So it initializates correctly with JsonModel Metaclass.

```py
from fastjson_db import JsonModel

class User(JsonModel):
    pass

```

### Creating fields ###

You can create your Model fields with the Field class. Find more in [Fields](fields.md)

```py
from fastjson_db import JsonModel, Field

class User(JsonModel):
    id = Field(field_name="id", type=int, primary_key=True, unique=True)
    username = Field(field_name="username", type=str)
```

### Using your Class ###

You can serializate your class and use the built-in function ".to_json" that turns everything in a `dict`. You don't need to use __init__ function because JsonModel MetaClass already takes care of everything.

```py
from fastjson_db import JsonModel, Field

class User(JsonModel):
    id = Field(field_name="id", type=int, primary_key=True, unique=True)
    username = Field(field_name="username", type=str)

new_user = User(id=0, username="new_name")
print(new_user.to_json())
```
