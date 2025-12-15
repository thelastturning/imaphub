from litestar import Controller, get
from typing import List

from .models import Asset

class AssetController(Controller):
    path = "/assets"

    @get("/")
    async def list_assets(self) -> List[Asset]:
        """
        List all assets.
        """
        return []

    @get("/{asset_id:str}")
    async def get_asset(self, asset_id: str) -> Asset:
        """
        Get a specific asset by ID.
        """
        return Asset(id=asset_id, name="Placeholder Asset", type="image")
