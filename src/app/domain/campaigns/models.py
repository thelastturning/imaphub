import msgspec
from typing import Optional, List
from app.domain.shared.models import ArangoDocument, EntityStatus, AdType

class Campaign(ArangoDocument):
    """
    Campaign Vertex.
    """
    customer_id: str
    name: str
    status: EntityStatus
    advertising_channel_type: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    # Local/Sync Fields
    sync_status: str = "synced"
    is_dirty: bool = False
    internal_notes: Optional[str] = None

class AdAssetLink(msgspec.Struct):
    """
    Edge representation for Ad -> Asset.
    """
    asset_text: str  # Denormalized
    asset_id: str
    field_type: str  # HEADLINE, DESCRIPTION
    pinned_field: Optional[str] = None
    performance_label: Optional[str] = None

class AdResponse(ArangoDocument):
    """
    Ad Vertex (augmented with nested assets for API).
    """
    ad_group_id: str
    final_urls: List[str]
    type: AdType
    headlines: List[AdAssetLink] = []
    descriptions: List[AdAssetLink] = []
