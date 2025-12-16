from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from app.domain.assets.controllers import AssetController
from app.domain.campaigns.controllers import CampaignController
from app.domain.reporting.controllers import ReportingController
from app.domain.auth.controllers import AuthController

@get("/")
async def hello_world() -> str:
    return "Hello World"

# CORS Configuration for frontend
cors_config = CORSConfig(
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True
)

app = Litestar(
    route_handlers=[
        hello_world,
        AssetController,
        CampaignController,
        ReportingController,
        AuthController
    ],
    cors_config=cors_config
)
