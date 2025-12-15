import msgspec

class Asset(msgspec.Struct):
    """
    Domain model representing a marketing asset.
    """
    id: str
    name: str
    type: str
