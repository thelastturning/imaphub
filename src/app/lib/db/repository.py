from typing import List, Dict, Any
from arango.database import StandardDatabase

class CampaignRepository:
    def __init__(self, db: StandardDatabase):
        self.db = db

    async def batch_upsert_assets(self, assets: List[Dict[str, Any]], links: List[Dict[str, Any]]) -> None:
        """
        Persists assets and edges using AQL atomic transactions.
        
        Per Architecture Spec (Section 4.2):
        - The hash becomes the _key for the Asset vertex
        - Uses UPSERT for deduplication
        
        Args:
            assets: List of dicts with keys: hash, text, type
            links: List of dicts with keys: from_id, to_id, field_type, pinned_field
        """
        
        # Skip if no assets to persist
        if not assets:
            # DEBUG: print("No assets to persist, skipping.")
            return
        
        # DEBUG: print(f"Upserting {len(assets)} assets...")
        
        # 1. Upsert Assets (Vertices)
        # Per architecture: hash IS the _key, no separate hash field stored
        aql_assets = """
        FOR asset IN @assets
            UPSERT { _key: asset.hash }
            INSERT {
                _key: asset.hash,
                text: asset.text,
                type: asset.type,
                created_at: DATE_NOW()
            }
            UPDATE {
                last_seen: DATE_NOW()
            }
            IN Assets
        """
        
        try:
            # Execute Asset Upsert
            self.db.aql.execute(aql_assets, bind_vars={"assets": assets})
            # DEBUG: print("Asset upsert successful.")
        except Exception as e:
            print(f"ERROR: Asset upsert failed: {e}")
            raise

        # Skip if no links to persist
        if not links:
            # DEBUG: print("No links to persist, skipping edge creation.")
            return
            
        aql_links = """
        FOR link IN @links
            UPSERT { _from: link.from_id, _to: link.to_id, field_type: link.field_type }
            INSERT {
                _from: link.from_id,
                _to: link.to_id,
                field_type: link.field_type,
                pinned_field: link.pinned_field
            }
            UPDATE {
                pinned_field: link.pinned_field
            }
            IN uses_asset
        """
        
        try:
            self.db.aql.execute(aql_links, bind_vars={"links": links})
            # DEBUG: print("Edge upsert successful.")
        except Exception as e:
            print(f"ERROR: Edge upsert failed: {e}")
            raise
