import hashlib
from app.domain.assets.models import AssetType

class AssetService:
    """
    Business logic for managing assets.
    """
    
    @staticmethod
    def generate_asset_hash(text: str, type: AssetType) -> str:
        """
        Generates a deterministic SHA-256 hash for an asset.
        This serves as the _key in ArangoDB to ensure deduplication.
        """
        # Normalize: strip whitespace, lowercase (optional but good for strict dedupe)
        # We stick to raw text for now to preserve casing if needed by the brand.
        payload = f"{type}:{text}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    async def get_all(self):
        pass

    async def get_by_id(self, id: str):
        pass
