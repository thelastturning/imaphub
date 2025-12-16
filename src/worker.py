import asyncio
import os
from arq.connections import RedisSettings

from app.lib.db.client import ArangoClient
from app.lib.google_ads.client import GoogleAdsClientFactory

async def startup(ctx):
    print("Worker starting up...")
    ctx['arango_client'] = ArangoClient()
    ctx['ads_factory'] = GoogleAdsClientFactory(ctx['arango_client'])
    print("Worker dependencies initialized.")

async def shutdown(ctx):
    print("Worker shutting down...")

async def sample_task(ctx, message: str):
    """
    Example task to verify worker execution.
    """
    print(f"Processing task: {message}")
    return f"Processed: {message}"

# Worker Settings
class WorkerSettings:
    redis_settings = RedisSettings(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", 6379))
    )
    functions = [sample_task]
    on_startup = startup
    on_shutdown = shutdown
    max_jobs = 10
