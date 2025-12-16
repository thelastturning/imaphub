import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    print("Verifying Stage 4 Imports...")
    from app.domain.campaigns.mutations import GoogleAdsMutator
    
    # Check method existence
    if not hasattr(GoogleAdsMutator, 'create_campaign'):
        raise ValueError("GoogleAdsMutator missing create_campaign method")

    print("SUCCESS: STAGE 4 MODULES VERIFIED")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"LOGIC ERROR: {e}")
    sys.exit(1)
