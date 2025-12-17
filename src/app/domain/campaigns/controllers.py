from litestar import Controller, get, post
from litestar.di import Provide
from app.lib.ai.client import GeminiService
from app.domain.campaigns.services import CampaignService
from app.domain.campaigns.models import GenerateAssetsRequest, CampaignStructure, ImportReportRequest
from app.lib.db.client import get_arango_db
from arango.database import StandardDatabase

# Dependency providers
async def provide_campaign_service(db: StandardDatabase) -> CampaignService:
    return CampaignService(db)

async def provide_gemini_service() -> GeminiService:
    return GeminiService()

class CampaignController(Controller):
    path = "/api/v1/campaigns" # Matched frontend prefix
    dependencies = {
        "db": Provide(get_arango_db),
        "campaign_service": Provide(provide_campaign_service),
        "gemini_service": Provide(provide_gemini_service)
    }

    @post("/generate")
    async def generate_assets(
        self,
        data: GenerateAssetsRequest,
        campaign_service: CampaignService
    ) -> CampaignStructure:
        """
        Generate Campaign Structure (AdGroups, Assets) using Gemini and persist to DB.
        """
        try:
            structure = await campaign_service.generate_campaign_structure_from_inputs(
                landing_page_url=data.landing_page_url,
                keywords=data.target_keywords
            )
            return structure
        except Exception as e:
            import traceback
            traceback.print_exc()
            # Return error structure or raise
            raise e

    @post("/import-report")
    async def import_report(
        self,
        data: ImportReportRequest,
        campaign_service: CampaignService
    ) -> CampaignStructure:
        """
        Parse Deep Research Report and generate Campaign Structure.
        """
        # === DEBUG LOGGING (commented out - uncomment to enable) ===
        # import logging
        # import os
        # from datetime import datetime
        # 
        # log_dir = "/app/logs"
        # os.makedirs(log_dir, exist_ok=True)
        # log_file = os.path.join(log_dir, "import_report.log")
        # 
        # logging.basicConfig(
        #     filename=log_file,
        #     level=logging.DEBUG,
        #     format='%(asctime)s - %(levelname)s - %(message)s',
        #     force=True
        # )
        # logger = logging.getLogger("import_report")
        # 
        # logger.info(f"=== NEW IMPORT REQUEST at {datetime.now().isoformat()} ===")
        # logger.info(f"Report text length: {len(data.report_text)} chars")
        # logger.info(f"Customer ID: {data.customer_id}")
        # logger.debug(f"Report preview (first 500 chars): {data.report_text[:500]}...")
        # === END DEBUG LOGGING ===
        
        try:
            structure = await campaign_service.generate_campaign_from_report(
                report_text=data.report_text,
                customer_id=data.customer_id
            )
            return structure
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e

    @get("/test-gemini")
    async def test_gemini(self, gemini_service: GeminiService) -> dict:
        return await gemini_service.health_check()



