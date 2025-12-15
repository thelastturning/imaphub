from litestar import Controller, get

class ReportingController(Controller):
    path = "/reports"

    @get("/")
    async def get_dashboard_report(self) -> dict:
        return {"metrics": []}
