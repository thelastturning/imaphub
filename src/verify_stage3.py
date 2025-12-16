import sys
import os

# Set PYTHONPATH to verify we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    print("Verifying Imports...")
    from app.lib.google_ads.client import GoogleAdsClientFactory
    from app.domain.reporting.services import GAQLService
    from app.domain.reporting.models import SearchTermRow
    from app.domain.campaigns.services import CampaignService
    
    print("Verifying GAQL Logic...")
    # Simple Logic Test
    query = GAQLService.build_search_term_query(lookback_days=7)
    if "LAST_7_DAYS" not in query:
        raise ValueError("GAQL Builder Logic Failed")
        
    print("SUCCESS: STAGE 3 MODULES VERIFIED")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"LOGIC ERROR: {e}")
    sys.exit(1)
