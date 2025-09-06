import os
import pytest
from dataclasses import dataclass
from fastjson_db.model import JsonModel
from fastjson_db.jsontable import JsonTable

@dataclass
class Dummy(JsonModel):
    _id: int | None = None
    name: str = ""

def test_save_failure_keeps_original(tmp_path, monkeypatch):
    db_file = tmp_path / "dummy.json"

    table = JsonTable(str(db_file), Dummy)
    table.insert(Dummy(name="ok"))
    table.flush()
    
    with open(db_file, "rb") as f:
        original_content = f.read()

    def fake_replace(src, dst):
        raise IOError("Simulated write failure")

    monkeypatch.setattr(os, "replace", fake_replace)

    table.insert(Dummy(name="fail"))
    with pytest.raises(IOError, match="Simulated write failure"):
        table.flush()

    with open(db_file, "rb") as f:
        final_content = f.read()

    assert final_content == original_content
