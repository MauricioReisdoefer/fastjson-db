# Models

FastJson-db works with "Models". Models are like a blueprint for how tables will be generated and how they should be read. These Models must contain all the fields that should be included in the tables. For Models to function correctly, they must inherit from the `JsonModel` class, created by FastJson-db. This facilitates their use and integration with the rest of the application.

## Data Types

JsonModels accept various data types. However, it is necessary to define the data type when creating the model.

Example:

```python
integer: int = 5
string: str = ""
```

In Python, we use a colon (`:`) followed by the variable type to define it.

Currently, in version [0.3.2], the FastJson-db supports the following variable types:

- Integer (`int`)
- String (`str`)
- Float (`float`)
- Decimal (`decimal.Decimal`)
- Datetime (`datetime.datetime`)
- Date (`datetime.date`)
- List (`list`)
- Dictionary (`dict`)
- Null (`type(None)`)
- ForeignKey\[Type] (`ForeignKey(Type)`)
- Hashed (`Hashed`)

## Creating a Basic Model

To create a model, we need to import `JsonModel` from our library. Then, we inherit from it in our class:

```python
from fastjson_db import JsonModel
from dataclasses import dataclass

@dataclass
class User(JsonModel):
    pass
```

Models in FastJson-db are created as `@dataclass` to also simplify their use in tables.

Now, we create the table fields in the model.

```python
from fastjson_db import JsonModel
from dataclasses import dataclass

@dataclass
class User(JsonModel):
    _id: int = 0
    name: str = ""
    password: str = ""
```

In summary, FastJson-db uses dataclass-based Models that inherit from `JsonModel` to define the structure and data types of your database tables, providing a clear and organized way to manage your data schema directly within your Python code.
