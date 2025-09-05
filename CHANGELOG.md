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

## [0.3.1] - 2025-09-04 ##

### Patch / Fixed ###

Removing `"_table_"` field from JsonTable insert. It could may cause many errors in serialization.

### Expected to Next Update [0.3.2] ###

Added support for using `@dataclass` objects for serialization within JsonTables.
