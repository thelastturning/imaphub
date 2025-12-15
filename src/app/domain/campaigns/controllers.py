from litestar import Controller, get

class CampaignController(Controller):
    path = "/campaigns"

    @get("/")
    async def list_campaigns(self) -> dict:
        return {"message": "Campaigns logic here"}
