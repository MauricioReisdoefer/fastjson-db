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

```bash
pip install fastjson-db
```

## Documentation ##

For further information, see the docs/ folder on github.

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

For easier table manipulation and avoid various JsonTables manipulating the same .json table, register the table in TABLE_REGISTRY.

```py
TABLE_REGISTRY[User] = user_table
```

### Creating a JsonQuerier ###

JsonQueriers will make queries and searchs in the .json files / tables.

```py
from fastjson_db import JsonModel, JsonTable, JsonQuerier
from dataclasses import dataclass

@dataclass
class User(JsonModel):
    _id: int = 0
    name: str = ""
    password: str = ""
    age: int = 0

user_table = JsonTable("users.json", User)
TABLE_REGISTRY[User] = user_table

user_table.insert(User(_id=1, name="Alice", password="abc", age=25))
user_table.insert(User(_id=2, name="Bob", password="123", age=30))
user_table.insert(User(_id=3, name="Charlie", password="xyz", age=35))

querier = JsonQuerier(user_table)

alice = querier.filter(name="Alice")
print("Filter:", alice)

not_30 = querier.exclude(age=30)
print("Exclude:", not_30)

older_than_30 = querier.custom(lambda u: u.age > 30)
print("Custom:", older_than_30)

bob = querier.get_first(name="Bob")
print("Get first:", bob)

ordered = querier.order_by("age")
print("Order by age:", ordered)
```

These are the main functions of JsonQuerier. You can have multiple queriers in the same table without generating Exceptions, but it's not recomended.

### Using a ForeignKey ###

FastJson-db tries to simulate ForeignKeys with a class called ForeignKey. You need to just create a ForeignKey field with the JsonModel it's related to.

```py
from fastjson_db import JsonModel, JsonTable, ForeignKey
from dataclasses import dataclass

@dataclass
class User(JsonModel):
    _id: int = 0
    name: str = ""

@dataclass
class Post(JsonModel):
    _id: int = 0
    title: str = ""
    author: ForeignKey[User] = ForeignKey(User)

user_table = JsonTable("users.json", User)
post_table = JsonTable("posts.json", Post)
TABLE_REGISTRY[User] = user_table
TABLE_REGISTRY[Post] = post_table

alice = User(_id=1, name="Alice")
user_table.insert(alice)

post = Post(_id=1, title="Meu primeiro post")
post.author.set(alice)
post_table.insert(post)

retrieved_post = post_table.get_first(_id=1)
author = retrieved_post.author.get()
print("Post:", retrieved_post.title)
print("Author:", author.name if author else "None")
```

So in this example we user a basic query to find a "Author" in the Post Table.

## Changelog ##

For a complete list of changes and updates, see the [CHANGELOG](CHANGELOG.md) file.

## Roadmap ##

For a complete list of future updates and how you can help, see [ROADMAP](ROADMAP.md) and [CONTRIBUTING](CONTRIBUTING.md) files.
