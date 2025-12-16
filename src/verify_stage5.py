import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    print("Verifying Stage 5 Imports...")
    from app.domain.campaigns.mutations import GoogleAdsMutator
    from worker import WorkerSettings, startup, shutdown
    
    # Verify Settings
    if not hasattr(WorkerSettings, 'redis_settings'):
         raise ValueError("WorkerSettings missing redis_settings")

    print("SUCCESS: STAGE 5 MODULES VERIFIED")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"LOGIC ERROR: {e}")
    sys.exit(1)
