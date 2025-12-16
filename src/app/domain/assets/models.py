import msgspec
from typing import Optional
from enum import Enum
from app.domain.shared.models import ArangoDocument

class AssetType(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"

class Asset(ArangoDocument):
    """
    Domain model representing a marketing asset.
    Vertices in 'Assets' collection.
    """
    type: AssetType
    asset_text: Optional[str] = None
    image_data: Optional[dict] = None # {url, file_size}
    name: Optional[str] = None # Optional name for management
