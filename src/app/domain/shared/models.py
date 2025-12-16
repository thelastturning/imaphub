import msgspec
from typing import Optional
from enum import Enum

class EntityStatus(str, Enum):
    ENABLED = "ENABLED"
    PAUSED = "PAUSED"
    REMOVED = "REMOVED"
    UNKNOWN = "UNKNOWN"

class AdType(str, Enum):
    RESPONSIVE_SEARCH_AD = "RESPONSIVE_SEARCH_AD"
    EXPANDED_TEXT_AD = "EXPANDED_TEXT_AD"  # Legacy

class ArangoDocument(msgspec.Struct, kw_only=True):
    """
    Base Struct for all ArangoDB Documents.
    """
    _key: str
    _id: Optional[str] = None
    _rev: Optional[str] = None
