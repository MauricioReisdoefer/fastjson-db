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
