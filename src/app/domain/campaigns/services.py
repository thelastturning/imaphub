from typing import List
from litestar.exceptions import NotFoundException

from app.lib.db.client import ArangoClient
from app.domain.campaigns.models import Campaign, EntityStatus
import msgspec

class CampaignService:
    def __init__(self, db: ArangoClient):
        self.db = db.get_db()
        self.collection = self.db.collection("Campaigns")

    async def get_all(self) -> List[Campaign]:
        cursor = self.collection.all()
        return [msgspec.convert(doc, type=Campaign) for doc in cursor]

    async def sync_campaigns_batch(self, campaigns: List[dict]):
        """
        Implements the AQL Upsert-Merge pattern to sync from Google.
        Preserves local modifications (is_dirty=True).
        """
        aql = """
        FOR doc IN @batch
          UPSERT { _key: doc._key }
          INSERT MERGE(doc, {
              first_synced_at: DATE_NOW(),
              local_status: "clean",
              is_dirty: false,
              sync_status: "synced"
          })
          UPDATE MERGE(doc, {
              last_synced_at: DATE_NOW(),
              
              # 1. Preserve local metadata
              internal_notes: OLD.internal_notes,
              
              # 2. Protect Dirty Fields (Local Wins)
              name: OLD.is_dirty ? OLD.name : doc.name,
              status: OLD.is_dirty ? OLD.status : doc.status,
              
              # 3. Always update read-only fields
              serving_status: doc.serving_status,
              sync_status: "synced"
          })
          IN Campaigns
        """
        
        # Execute Batch Transaction
        self.db.aql.execute(aql, bind_vars={"batch": campaigns})
