from typing import List
from litestar.exceptions import NotFoundException

from app.lib.db.client import ArangoClient
from app.domain.campaigns.models import Campaign, EntityStatus, CampaignStructure
from arango.database import StandardDatabase
import msgspec

class CampaignService:
    def __init__(self, db: StandardDatabase):
        self.db = db
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

    async def generate_campaign_structure_from_inputs(self, landing_page_url: str, keywords: List[str]) -> CampaignStructure:
        """
        Generates a Campaign Structure directly from inputs (Wizard Mode).
        """
        from app.lib.ai.client import GeminiService
        from app.domain.campaigns.models import CampaignStructure
        from app.lib.ai.schema_bridge import prepare_schema_for_gemini
        
        gemini = GeminiService()
        schema = prepare_schema_for_gemini(CampaignStructure)
        
        prompt = f"""
        You are a Google Ads Expert. Create a high-performing Campaign Structure
        for the following Landing Page and Keywords.
        
        Landing Page: {landing_page_url}
        Target Keywords: {", ".join(keywords)}
        
        Requirements:
        1. Create 1 optimized Ad Group.
        2. Generate 15 Headlines (max 30 chars).
        3. Generate 4 Descriptions (max 90 chars).
        4. Suggest a Campaign Name and Budget.
        """
        
        structure_dict = await gemini.generate_with_retry(prompt, schema)
        structure = msgspec.json.decode(msgspec.json.encode(structure_dict), type=CampaignStructure)
        
        # Persist
        await self._persist_structure(structure)
        
        return structure

    async def generate_campaign_from_report(self, report_text: str, customer_id: str) -> CampaignStructure:
        """
        Parses a Deep Research Report using Gemini and persists the resulting
        Campaign Structure (Campaign -> AdGroups -> Assets) to ArangoDB.
        """
        from app.lib.ai.client import GeminiService
        from app.domain.campaigns.models import CampaignStructure
        from app.lib.ai.schema_bridge import prepare_schema_for_gemini
        
        # 1. Call AI to parse report
        # DEBUG: print(f"Starting Campaign Generation from Report. Length: {len(report_text)} chars")
        gemini = GeminiService()
        schema = prepare_schema_for_gemini(CampaignStructure)
        
        prompt = f"""
        You are an expert Google Ads Strategist.
        
        TASK:
        Analyze the provided "Deep Research Report" and construct a complete Google Ads Campaign Structure.
        
        INSTRUCTIONS:
        1. Identify the logical segments in the report (e.g., Target Audiences, Product Angles) and create separate Ad Groups for each.
        2. For each Ad Group, extract or generate highly relevant Keywords (Broad/Phrase/Exact).
        3. For each Ad Group, extract or write 15 High-Quality Headlines (max 30 chars) and 4 Descriptions (max 90 chars).
        4. If the report suggests a budget, use it; otherwise estimate a recommended daily budget.
        
        REPORT CONTENT:
        {report_text}
        """
        
        # DEBUG: print("Sending request to Gemini...")
        structure_dict = await gemini.generate_with_retry(prompt, schema)
        # DEBUG: print("Received response from Gemini. Decoding...")
        structure = msgspec.json.decode(msgspec.json.encode(structure_dict), type=CampaignStructure)
        # DEBUG: print(f"Successfully decoded structure. Found {len(structure.ad_groups)} Ad Groups.")

        # 2. Persist
        # DEBUG: print("Persisting structure to ArangoDB...")
        await self._persist_structure(structure)
        # DEBUG: print("Persistence complete.")
        
        return structure

    async def _persist_structure(self, structure: CampaignStructure):
        """
        Helper to persist a CampaignStructure to ArangoDB using the Repository.
        """
        from app.domain.assets.services import AssetService
        from app.domain.assets.models import AssetType
        from app.lib.db.repository import CampaignRepository
        
        # DEBUG: print("Starting _persist_structure...")
        repo = CampaignRepository(self.db)
        
        # Use dict for deduplication (hash -> asset data)
        unique_assets = {}
        links_batch = []
        
        for ag in structure.ad_groups:
            # Headlines
            for hl in ag.assets.headlines:
                h_hash = AssetService.generate_asset_hash(hl, AssetType.TEXT)
                # Only add if not already seen (deduplication)
                if h_hash not in unique_assets:
                    unique_assets[h_hash] = {
                        "hash": h_hash,
                        "text": hl,
                        "type": AssetType.TEXT
                    }
                
            # Descriptions
            for desc in ag.assets.descriptions:
                d_hash = AssetService.generate_asset_hash(desc, AssetType.TEXT)
                if d_hash not in unique_assets:
                    unique_assets[d_hash] = {
                        "hash": d_hash,
                        "text": desc,
                        "type": AssetType.TEXT
                    }
        
        # Convert back to list
        assets_batch = list(unique_assets.values())
        # DEBUG: print(f"Deduplicated {len(assets_batch)} unique assets for persistence.")
        
        # Batch Upsert to ArangoDB
        await repo.batch_upsert_assets(assets_batch, links_batch)
        # DEBUG: print("Batch upsert complete.")
