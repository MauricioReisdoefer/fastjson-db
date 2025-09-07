# Tables #

`JsonTables` are the primary mechanism through which `FastJson-DB` organizes data. Although it operates as a NoSQL database, it adopts a familiar "table" structure to streamline data organization and access. Each `JsonTable` serves as a logical container for JSON documents that share a common structure or purpose, akin to collections in other NoSQL databases or traditional tables in relational databases.

See more about the internal functioning of `JsonTables` here [JsonTables](jsontables_internals.md)

## Features ##

* **Indexing**: While not a relational database, `FastJson-DB` supports indexing of fields within `JsonTables` to optimize query performance. This feature is crucial for efficient data retrieval, especially with large datasets.

* **CRUD Operations**: `JsonTables` fully support the fundamental Create, Read, Update, and Delete (CRUD) operations, ensuring comprehensive data manipulation capabilities.

* **File Storage**: Each `JsonTable` is persistently stored as a separate JSON file within the file system. This design choice enhances backup procedures, data portability, and allows for direct inspection of the stored data.

* **Simplicity**: The `JsonTables` approach prioritizes simplicity in data organization, making `FastJson-DB` intuitive and easy to use. This is particularly beneficial for developers accustomed to file-based structures or traditional table concepts.

## How To Use ##

### Creating a JsonTable ###

To begin using `FastJson-DB`, the initial step involves creating a `JsonTable`. This process is performed programmatically via the database's API. By creating a `JsonTable`, you are essentially defining a new container for your JSON documents. `FastJson-DB` automatically handles the creation of the corresponding file in your specified file system directory.

**Note**: A `JsonTable` must be initialized with a `JsonModel` (typically a `@dataclass` inheriting from `JsonModel`) that defines the structure of the data it will store. For more details, refer to [Models](models.md).

```python
from fastjson_db import JsonModel, JsonTable
from dataclasses import dataclass
@dataclass
class User(JsonModel):
    _id: int | None = None
    name: str = ""
    age: int = 0

# Parameters:
# - "users.json": The filename (string) where the JsonTable data will be stored. This file will be created if it doesn't exist.
# - User: The JsonModel class (e.g., a @dataclass) that defines the structure of documents to be stored in this table.
user_table = JsonTable("users.json", User)
```

Executing the code above will create a file named `users.json` (or manipulate an existing one) and configure the `user_table` instance to exclusively manage `User` dataclass objects.

### Inserting Data ###

`JsonTables` provide direct support for CRUD operations, including insertion. To insert a new document, simply use the `.insert()` method and pass an instance of the `JsonModel` class associated with the `JsonTable`.

```python
new_user = User(
    _id = 0, # This _id will be ignored by the JsonTable, which automatically assigns a unique ID upon insertion.
    name = "Allan",
    age = 17
)

# Parameters:
# - new_user: An instance of the JsonModel (e.g., User, defined in the creation of the Table) to be inserted into the table.
user_table.insert(new_user)
```

**Important**: This operation does **not** immediately write the user data to the `users.json` file. Instead, it adds the user to the `JsonTable`'s internal cache memory. Data is only persisted to disk when the `.flush()` method is explicitly called.

### Flushing Data ###

To persist the cached data to the file, use the `.flush()` method of the `JsonTable`. It is generally inefficient to write every single insertion directly to the `.json` file. Therefore, the table first accumulates changes in its cache and only writes them to the file when `.flush()` is invoked.

**Note**: For optimal performance, invoke `.flush()` only when necessary, such as after a batch of insertions or updates, or when you need to ensure data persistence.

```python
# Parameters:
# - This method takes no parameters.
user_table.flush()
```

After calling `.flush()`, you can open the `users.json` file and verify that the new user data has been successfully written.

### Retrieving Data ###

To retrieve specific entries from a `JsonTable`, you can use the `.get_by()` method. This method allows you to query documents based on a specified field and its corresponding value.

```python
# Parameters:
# - "age": The name of the field (string) to search within.
# - 18: The value (any type) to match against the specified field.
users = user_table.get_by("age", 18)
```

This call will return a list of all users whose `age` field is equal to 18. To retrieve all documents from the `user_table`, use the `.get_all()` method.

```python
# Parameters:
# - This method takes no parameters.
users = user_table.get_all()
```

It's important to note that you do not need to call `.flush()` before using these retrieval methods, as they operate on the current state of the table, including cached data.

For more complex queries and advanced filtering, refer to the documentation on [JsonQuerier](querier.md).

### Updating Entries ###

To update an existing document, use the `.update()` method. This method updates a specific entry identified by its unique ID.

```python
# First, retrieve the user to be updated. Assuming we want to update the first user found with age 17.
user_to_update = user_table.get_by("age", 17)[0]

# Create a new User object with the updated fields. The _id must match the original document's _id.
updated_user_data = User(_id=user_to_update._id, name="NewName", age=18)

# Parameters:
# - user_to_update._id: The unique ID (integer) of the document to be updated.
# - updated_user_data: An instance of the JsonModel (e.g., User) containing the new data for the document.
#   All fields in this object will replace the corresponding fields in the existing document.
user_table.update(user_to_update._id, updated_user_data)
```

You need to provide both the ID of the object to be updated and a new `JsonModel` object that will completely replace the older one.

### Deleting Entries ###

To remove a document from a `JsonTable`, simply use the `.delete()` method. This method takes a document ID and removes the corresponding entry.

```python
# Parameters:
# - 5: The unique ID (integer) of the document to be deleted.
user_table.delete(5)
```

This code snippet will remove the user document with `_id = 5` from the `JsonTable`.
