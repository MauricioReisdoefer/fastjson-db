# FastJson-db Changelog #

All changes from 0.2.1 version or above will be documented here.

## [0.2.1] - 2025-09-03 ##

### Added ###

- Base exceptions `InvalidModel` and `NotDataclassModelError` for explicit model validation.
- `TableNotRegisteredError` when not registring a table in `TABLE_REGISTRY` to avoid duplication.
- `InvalidForeignKeyTypeError` when trying to use a invalid model / class in Foreign Keys
- Model validation in `JsonTable` to ensure `_id` field and inheritance from `JsonModel`.

### Fixed ###

- Order of checks in `JsonTable.__init__` to raise errors earlier.

### Changed ###

- Improved feedback when reconstructing models from JSON.

---

## [0.3.0] - 2025-09-04 ##

### Added ###

- Added the possibility to add other datatypes with Serializers
- New serializable types:
- - Generic Lists
- - Datatime
- - Date
- - Decimal
- - Generic Dicts

### Observation ###

This new version does not break the last version, only adds a new feature. You can upgrade without any problem.

---

## [0.3.1] - 2025-09-04 ##

### Patch / Fixed ###

Removing `"_table_"` field from JsonTable insert. It could may cause many errors in serialization.

---

## [0.3.2] - 2025-09-05 ##

### Added ###

- Deserialization now supports fields annotated with `Optional[T]` or `T | None`. (As in the ROADMAP)
- Improved compatibility with Python 3.10+ type hint syntax.

### IMPORTANT ###

This might break some codes if not being used properly.

---

## [0.3.3] - 2025-09-05 ##

### Added ###

- Added new datatype "Hashed", a wrapper to facilitate `Werkzeug.security` usage
- Serialization and Deserialization of `Hashed` type

---

## [0.3.4] - 2025-09-06 ##

### Patch ###

- Added new atomicity system to JsonTables

---

## [0.3.5] - 2025-09-06 ##

### Added ###

- Added new Unique type, so it doesn't permit non Unique entrys in determined fields.

### ### Expected to Next Update [0.4.0] ###

- Adding support for using `@dataclass` objects for serialization within JsonTables.
- Adding harsher datatype validation to ensure stronger guarantees when serializing and deserializing models.
- General performance improvements in serialization.
