from litestar import Litestar, get
from app.domain.assets.controllers import AssetController
from app.domain.campaigns.controllers import CampaignController
from app.domain.reporting.controllers import ReportingController

@get("/")
async def hello_world() -> str:
    return "Hello World"

app = Litestar(route_handlers=[
    hello_world,
    AssetController,
    CampaignController,
    ReportingController
])
