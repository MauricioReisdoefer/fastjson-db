# FastJson-db #

A lightweight JSON-based database for Python.  
`fastjson-db` allows you to store, retrieve, and manipulate data in a simple JSON file with a minimal and easy-to-use API.

## Features ##

- Lightweight and simple to use
- CRUD operations: insert, get, update, delete
- Automatic unique IDs for records
- Optional fast backend using `orjson` if installed
- Human-readable JSON file

## Installation ##

The currently newest version is [0.3.5].

```bash
pip install fastjson-db
```

## Examples ##

Some basic examples on how to user FastJson-db

### Creating a Class ###

To manipulate JsonTables, you need to create a JsonModel subclass (dataclass), so the JsonTable only accepts that especific JsonModel subclass.

```py
from fastjson_db import JsonModel
from dataclasses import dataclass

@dataclass
class User(JsonModel):
    _id: int
    name: str = ""
    password: str = ""
```

It's obrigatory using `_id` field or it will not result in error when quering.

### Creating a JsonTable ###

JsonTables are the ones inserting and updating your dataclasses in .json files. They will automaticly create and facilitate the usage of .json "tables", trying to simulate a simple database.

```py
from fastjson_db import JsonModel, JsonTable
from dataclasses import dataclass

@dataclass
class User(JsonModel):
    _id: int = 0
    name: str = ""
    password: str = ""
    
user = User(name="Allan", password="123")

user_table = JsonTable("users.json", User)
```

## Links ##

📚 [Complete Docs](https://github.com/MauricioReisdoefer/fastjson-db/tree/main/docs/index.md)  
📝 [Changelog](https://github.com/MauricioReisdoefer/fastjson-db/tree/main/CHANGELOG.md)  
🛣️ [Roadmap](https://github.com/MauricioReisdoefer/fastjson-db/tree/main/ROADMAP.md)  
🤝 [Contributing](https://github.com/MauricioReisdoefer/fastjson-db/tree/main/CONTRIBUTING.md)

![PyPI](https://img.shields.io/pypi/v/fastjson-db)
![License](https://img.shields.io/github/license/MauricioReisdoefer/fastjson-db)
