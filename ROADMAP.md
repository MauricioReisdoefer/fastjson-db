# FastJson-db - Objective and Roadmap #

## Mission ##

FastJson-db aims to provide a lightweight JSON-based database for Python projects. It is designed for small projects, prototypes, and educational purposes, where using SQLite or other relational databases might be overkill.

## Current Goals (v0.4.0) ##

These are the adjustments we aim before oficial 0.4.0 release.

### JsonApp ###

- Create a JsonApp
- Hide .flush() functionality
- Atomicity with .log append

### Simplify ###

- Simplify what's not simple and what's redundant.

### Query Enhancements ###

- Support for complex queries (AND, OR, NOT logic)
- Ability to chain queries (e.g., filter().exclude().order_by())

## Philosophy ##

- Keep it lightweight and simple
- Make it extensible
- Prioritize readability and ease of use

Futurely we will prioritize speed and performance improvements, including optional support for faster JSON parsing with `orjson` or other optimized backends with C implementations.
