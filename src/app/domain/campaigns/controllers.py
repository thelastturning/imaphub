from litestar import Controller, get, post
from litestar.di import Provide
from app.lib.ai.client import GeminiService
from app.domain.campaigns.models import GenerateAssetsRequest, RSAAsset
import msgspec


# Dependency provider for GeminiService
async def provide_gemini_service() -> GeminiService:
    return GeminiService()


class CampaignController(Controller):
    path = "/campaigns"
    dependencies = {"gemini_service": Provide(provide_gemini_service)}

    @get("/")
    async def list_campaigns(self) -> dict:
        return {"message": "Campaigns logic here"}
    
    @post("/generate-assets")
    async def generate_assets(
        self,
        data: GenerateAssetsRequest,
        gemini_service: GeminiService
    ) -> dict:
        """
        Generate RSA assets using Gemini 1.5 Flash.
        
        Request body:
        {
            "landing_page_url": "https://example.com",
            "target_keywords": ["keyword1", "keyword2"],
            "brand_voice": "professional",  // optional
            "language": "de"  // optional, defaults to "de"
        }
        """
        try:
            assets = await gemini_service.generate_rsa_assets(
                landing_page_url=data.landing_page_url,
                target_keywords=data.target_keywords,
                brand_voice=data.brand_voice,
                language=data.language
            )
            return assets
        except Exception as e:
            # Log full error for debugging
            import traceback
            print(f"ERROR in generate_assets: {type(e).__name__}: {str(e)}")
            traceback.print_exc()
            return {
                "error": str(e),
                "message": "Failed to generate assets"
            }

    @get("/test-gemini")
    async def test_gemini(self, gemini_service: GeminiService) -> dict:
        """
        Simple connectivity test for Gemini API.
        Sends "Respond with 'OK'" to the model.
        """
        return await gemini_service.health_check()



