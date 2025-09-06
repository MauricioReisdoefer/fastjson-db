import os
import json

class JsonUniquer:
    def __init__(self, base_path: str, table_name: str, field_name: str):
        self.path = os.path.join(
            os.path.dirname(base_path),
            f"{table_name}_{field_name}_unique.json"
        )
        self._values = set()

        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self._values = set(json.load(f))
        else:
            self._flush()

    def _flush(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(list(self._values), f)

    def add(self, value):
        if value in self._values:
            raise ValueError(f"Unique constraint violated: {value}")
        self._values.add(value)
        self._flush()

    def remove(self, value):
        if value in self._values:
            self._values.remove(value)
            self._flush()
