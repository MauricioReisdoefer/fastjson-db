from dataclasses import dataclass, asdict

@dataclass
class JsonModel():
    """Base model for every JsonTable fields"""
    _id: int = None | None