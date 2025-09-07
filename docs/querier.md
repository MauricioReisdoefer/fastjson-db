# Queriers #

Just like in most databases or ORMs, `fastjson-db` provides the ability to perform custom and more complex queries. This is achieved through the `JsonQuerier`, a dedicated class designed to facilitate querying your `.json` tables efficiently. Each `JsonQuerier` instance is specifically associated with a `JsonTable`, allowing for targeted data retrieval and manipulation.

Find about it's intern functioning in [JsonQuerier](querier_internals.md)

```python
from typing import Any, Dict, List, Optional, Callable, TypeVar
from .jsontable import JsonTable
T = TypeVar("T")

class JsonQuerier:
    """
    Provides advanced querying capabilities over a JsonTable.
    """

    def __init__(self, table: JsonTable):
        self.table = table
```

## Initialization ##

To use `JsonQuerier`, you must first instantiate it, passing an existing `JsonTable` object to its constructor. This links the querier to a specific dataset, enabling it to perform operations on that table.

**Parameters**

* `table` (`JsonTable`): The `JsonTable` instance on which the queries will be performed.

**Example**

```python
from fastjson_db import JsonTable, JsonQuerier, JsonModel
from dataclasses import dataclass

@dataclass
class Product(JsonModel):
    _id: int | None = None
    name: str = ""
    price: float = 0.00

# Assuming 'products.json' exists and contains Product data
products_table = JsonTable("products.json", Product)
products_querier = JsonQuerier(products_table)
```

## `filter(**conditions: Any) -> List[T]` ##

This method returns all objects from the associated `JsonTable` that match **all** the provided conditions. It performs an exact match for each key-value pair specified.

**Parameters**

* `**conditions` (keyword arguments): One or more keyword arguments where the key is the attribute name of the object and the value is the desired value to match. All conditions must be met for an object to be included in the results.

**Returns**

* `List[T]`: A list of objects (of type `T`, which is the `JsonModel` type of the `JsonTable`) that satisfy all the specified conditions. If no objects match, an empty list is returned.

**Example**

```python
# Assuming products_querier is initialized with a JsonTable of Product objects
# Product objects have 'name' and 'price' attributes

# Find all products named "Laptop" with a price of 1200.00
laptops = products_querier.filter(name="Laptop", price=1200.00)
for product in laptops:
    print(f"Found: {product.name} - ${product.price}")

# Find all products with a specific ID
product_by_id = products_querier.filter(id=101)
if product_by_id:
    print(f"Product with ID 101: {product_by_id[0].name}")
```

## `exclude(**conditions: Any) -> List[T]` ##

This method returns all objects from the associated `JsonTable` that **do not** match any of the given conditions. It effectively filters out objects that satisfy the specified criteria.

**Parameters**

* `**conditions` (keyword arguments): One or more keyword arguments where the key is the attribute name of the object and the value is the value to exclude. Objects matching any of these conditions will be excluded from the results.

**Returns**

* `List[T]`: A list of objects (of type `T`) that do not satisfy any of the specified conditions. If all objects match the exclusion criteria, an empty list is returned.

**Example**

```python
# Assuming products_querier is initialized with a JsonTable of Product objects

# Exclude all products named "Book" or with a price of 10.00
non_book_or_expensive_items = products_querier.exclude(name="Book", price=10.00)
for product in non_book_or_expensive_items:
    print(f"Found: {product.name} - ${product.price}")

# Exclude products with a specific ID
products_without_id_101 = products_querier.exclude(id=101)
for product in products_without_id_101:
    print(f"Product: {product.name}")
```

## `custom(func: Callable[[T], bool]) -> List[T]` ##

This method allows for highly flexible querying by accepting a custom function. It returns all objects from the `JsonTable` for which the provided function returns `True`.

**Parameters**

* `func` (`Callable[[T], bool]`): A callable (such as a lambda function or a regular function) that takes a single argument (an object of type `T`) and returns a boolean value. The function should return `True` if the object meets the desired criteria, and `False` otherwise.

**Returns**

* `List[T]`: A list of objects that satisfy the custom function. If no objects satisfy the function, an empty list is returned.

**Example**

```python
# Assuming products_querier is initialized with a JsonTable of Product objects

# Find all products with a price greater than 50.00
expensive_products = products_querier.custom(lambda p: p.price > 50.00)
for product in expensive_products:
    print(f"Expensive product: {product.name} - ${product.price}")

# Find all products whose names start with "Smart"
def starts_with_smart(product):
    return product.name.startswith("Smart")

smart_products = products_querier.custom(starts_with_smart)
for product in smart_products:
    print(f"Smart device: {product.name}")
```

## `get_first(**conditions: Any) -> Optional[T]` ##

This method returns the first object from the associated `JsonTable` that matches the given conditions. It is useful when you expect only one result or are interested in the first match found.

**Parameters**

* `**conditions` (keyword arguments): One or more keyword arguments where the key is the attribute name of the object and the value is the desired value to match. Similar to `filter`, all conditions must be met.

**Returns**

* `Optional[T]`: The first object (of type `T`) that satisfies all the specified conditions. Returns `None` if no object matches the conditions.

**Example**

```python
# Assuming products_querier is initialized with a JsonTable of Product objects

# Find the first product named "Monitor"
monitor = products_querier.get_first(name="Monitor")
if monitor:
    print(f"First monitor found: {monitor.name} - ${monitor.price}")
else:
    print("No monitor found.")

# Find the first product with a price exactly 75.00
product_at_price = products_querier.get_first(price=75.00)
if product_at_price:
    print(f"Product at $75.00: {product_at_price.name}")
```

## `order_by(key: str, reverse: bool = False) -> List[T]` ##

This method returns all objects from the associated `JsonTable`, sorted by a specified key. You can control the sort order (ascending or descending).

**Parameters**

* `key` (`str`): The attribute name of the object to use for sorting.
* `reverse` (`bool`, optional): If `True`, the list is sorted in descending order. Defaults to `False` (ascending order).

**Returns**

* `List[T]`: A new list containing all objects from the `JsonTable`, sorted according to the specified key and order.

**Example**

```python
# Assuming products_querier is initialized with a JsonTable of Product objects

# Get all products sorted by price in ascending order
products_by_price_asc = products_querier.order_by("price")
print("Products sorted by price (ascending):")
for product in products_by_price_asc:
    print(f"- {product.name}: ${product.price}")

# Get all products sorted by name in descending order
products_by_name_desc = products_querier.order_by("name", reverse=True)
print("\nProducts sorted by name (descending):")
for product in products_by_name_desc:
    print(f"- {product.name}")
```

Complete working code to tests:

```py
# JsonQuerier initialization example
from fastjson_db import JsonTable, JsonQuerier, JsonModel
from dataclasses import dataclass

@dataclass
class Product(JsonModel):
    _id: int | None = None
    name: str = ""
    price: float = 0.00

# Assuming 'products.json' exists and contains Product data
products_table = JsonTable("products.json", Product)

products_table.insert(Product(name="Laptop", price=1200.00))
products_table.insert(Product(name="Laptop", price=1500.00))
products_table.insert(Product(name="Book", price=10.00))
products_table.insert(Product(name="Smartphone", price=800.00))
products_table.insert(Product(name="Smartwatch", price=250.00))
products_table.insert(Product(name="Monitor", price=300.00))
products_table.insert(Product(name="Keyboard", price=75.00))
products_table.insert(Product(name="Mouse", price=50.00))

products_table.flush()

products_querier = JsonQuerier(products_table)

# filter example
laptops = products_querier.filter(name="Laptop", price=1200.00)
for product in laptops:
    print(f"Found: {product.name} - ${product.price}")

product_by_id = products_querier.filter(_id=101)
if product_by_id:
    print(f"Product with ID 101: {product_by_id[0].name}")

# exclude example
non_book_or_expensive_items = products_querier.exclude(name="Book", price=10.00)
for product in non_book_or_expensive_items:
    print(f"Found: {product.name} - ${product.price}")

products_without_id_101 = products_querier.exclude(_id=101)
for product in products_without_id_101:
    print(f"Product: {product.name}")

# custom example
expensive_products = products_querier.custom(lambda p: p.price > 50.00)
for product in expensive_products:
    print(f"Expensive product: {product.name} - ${product.price}")

def starts_with_smart(product):
    return product.name.startswith("Smart")

smart_products = products_querier.custom(starts_with_smart)
for product in smart_products:
    print(f"Smart device: {product.name}")

# get_first example
monitor = products_querier.get_first(name="Monitor")
if monitor:
    print(f"First monitor found: {monitor.name} - ${monitor.price}")
else:
    print("No monitor found.")

product_at_price = products_querier.get_first(price=75.00)
if product_at_price:
    print(f"Product at $75.00: {product_at_price.name}")

# order_by example
products_by_price_asc = products_querier.order_by("price")
print("Products sorted by price (ascending):")
for product in products_by_price_asc:
    print(f"- {product.name}: ${product.price}")

products_by_name_desc = products_querier.order_by("name", reverse=True)
print("\nProducts sorted by name (descending):")
for product in products_by_name_desc:
    print(f"- {product.name}")
```
