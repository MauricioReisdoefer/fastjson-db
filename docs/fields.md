# FastJson-DB - Fields #

## Introduction ##

FastJson-DB use the `Field` class to define every field in the Tables. So it represents how it should be serializated, deserializated, how the values should be validated, datatypes and other important definitions for FastJson-DB, like primary keys, uniques and foreign keys.

## How to Use Fields ##

### Quick Start ###

To use, import from FastJson-DB the Field class:

```py
from fastjson_db import Field
```

Then, create a new Field like this:

```py
from fastjson_db import Field

new_field = Field()
```

### Arguments ###

- **field_name** (`str`, required)  
  The name of the field. Must be a non-empty string. It's how the FastJson-DB will save your field in the database.

- **type** (`Any`, required)  
  The Python type of the field. Can be a native type (`int`, `str`, `float`), or a typing generic (`List[T]`, `Dict[K, V]`).  
  Custom types are allowed, but they require a **serializer** and **deserializer**.

- **foreign_key** (`Optional[str]`, default=`None`)  
  Defines a relation to another table’s primary key. Must be a string with the reference.

- **unique** (`bool`, default=`False`)  
  If `True`, ensures that all values in this field are unique across the table.

- **primary_key** (`bool`, default=`False`)  
  If `True`, marks this field as the primary identifier for the table.  
  ⚠ A primary key **must** also be unique (`unique=True`).

- **validator** (`Optional[Callable[[Any], Any]]`, default=`None`)  
  A callable that validates the field value before saving.  
  For native types (`int`, `str`, `float`, `List`, `Dict`), this is optional.  
  For custom types, this is **required** along with serializer/deserializer.

- **serializer** (`Optional[Callable[[Any], Any]]`, default=`None`)  
  Function to transform a custom Python object into a JSON-compatible format.  
  Required for custom types.

- **deserializer** (`Optional[Callable[[Any], Any]]`, default=`None`)  
  Function to reconstruct a custom Python object from a serialized (JSON) value.  
  Required for custom types.

### Creating a Complete Field ###

You can use all the arguments like this (for example, creating and ID field):

```py
id = Field(field_name="id", type=int, unique=True, primary_key=True)
```
