# FastJson-db - Objective and Roadmap #

## Mission ##

FastJson-db aims to provide a lightweight JSON-based database for Python projects. It is designed for small projects, prototypes, and educational purposes, where using SQLite or other relational databases might be overkill.

## Current Goals (v1.0.0) ##

These are the adjustments we aim before oficial 1.0.0 release (leaving beta and maintaining more stable strucutre).

### API Improvements ###

- Cleaner integration with JsonModel subclasses

### File Handling & Backend ###

- Ensure safe read/write operations (atomic writes)

### Query Enhancements ###

- Support for complex queries (AND, OR, NOT logic)
- Ability to chain queries (e.g., filter().exclude().order_by())

### Documentation & Examples ###

- Expand README with clear examples for JsonQuerier and ForeignKey
- Provide a “cheat sheet” for common operations
- Include migration guide from beta to stable

### Testing & Stability ###

- Full unit tests for all operations
- Tests for edge cases (missing keys, empty tables, invalid foreign keys)
- Benchmark basic CRUD and query performance

### New Types ###

- Dataclasses

## Philosophy ##

- Keep it lightweight and simple
- Make it extensible
- Prioritize readability and ease of use

Futurely we will prioritize speed and performance improvements, including optional support for faster JSON parsing with `orjson` or other optimized backends with C implementations.
