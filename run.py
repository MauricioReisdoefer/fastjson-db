import time
from random import randint
from fastjson_db import JsonModel, Field, JsonTable
from fastjson_db.core.json_querier import JsonQuerier

print("-/ FASTJSON-DB /-")

# ------------------ MODEL ------------------ #
class User(JsonModel):
    id = Field(field_name="id", type=int, primary_key=True, unique=True)
    username = Field(field_name="username", type=str)

# ------------------ HELPER ------------------ #
def create_users(n: int):
    return [User(id=i, username=f"User{i}") for i in range(n)]

# ------------------ BENCHMARK ------------------ #
def benchmark(n):
    print(f"\n--- Benchmark with {n} users ---")

    # Cria a tabela
    table = JsonTable(User, f"user_table_{n}.json")
    users = create_users(n)
    for u in users:
        table.insert(u)

    querier = JsonQuerier(table)

    # Escolhe um ID aleatório
    random_id = randint(0, n - 1)

    # ------------------ Test .first() ------------------ #
    start = time.perf_counter()
    user_first = querier.filter(id=random_id).first()
    end = time.perf_counter()
    print(f"Query first() by id={random_id}: {end - start:.6f} seconds")

    # ------------------ Test .get() ------------------ #
    start = time.perf_counter()
    user_list = querier.filter(id=random_id).get()
    end = time.perf_counter()
    print(f"Query get() by id={random_id}: {end - start:.6f} seconds")

    # ------------------ Test .count() ------------------ #
    start = time.perf_counter()
    count = querier.count(id=random_id)
    end = time.perf_counter()
    print(f"Query count() by id={random_id}: {end - start:.6f} seconds")

# ------------------ RUN BENCHMARK ------------------ #
for size in [1000, 10_000, 100_000]:
    benchmark(size)

print("\n\n-/ SQLITE /-")

import sqlite3
import time
from random import randint

# ------------------ HELPER ------------------ #
def create_users(n):
    return [(i, f"User{i}") for i in range(n)]

# ------------------ BENCHMARK ------------------ #
def benchmark_sqlite(n):
    print(f"\n--- SQLite Benchmark with {n} users ---")
    
    conn = sqlite3.connect(":memory:")  # memória para ser rápido
    c = conn.cursor()
    
    # Cria tabela
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
    
    # Insere dados
    users = create_users(n)
    start_insert = time.perf_counter()
    c.executemany("INSERT INTO users (id, username) VALUES (?, ?)", users)
    conn.commit()
    end_insert = time.perf_counter()
    print(f"Inserted {n} users in {end_insert - start_insert:.6f} seconds")
    
    # Escolhe ID aleatório
    random_id = randint(0, n - 1)
    
    # Test SELECT first
    start = time.perf_counter()
    c.execute("SELECT * FROM users WHERE id=?", (random_id,))
    row = c.fetchone()
    end = time.perf_counter()
    print(f"Query first() by id={random_id}: {end - start:.6f} seconds")
    
    # Test SELECT get (same as first here, because id is PK)
    start = time.perf_counter()
    c.execute("SELECT * FROM users WHERE id=?", (random_id,))
    rows = c.fetchall()
    end = time.perf_counter()
    print(f"Query get() by id={random_id}: {end - start:.6f} seconds")
    
    # Test COUNT
    start = time.perf_counter()
    c.execute("SELECT COUNT(*) FROM users WHERE id=?", (random_id,))
    count = c.fetchone()[0]
    end = time.perf_counter()
    print(f"Query count() by id={random_id}: {end - start:.6f} seconds")
    
    conn.close()

# ------------------ RUN BENCHMARK ------------------ #
for size in [1000, 10_000, 100_000]:
    benchmark_sqlite(size)
