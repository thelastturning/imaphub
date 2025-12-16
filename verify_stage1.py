import sys
from unittest.mock import MagicMock

# Mock arango for import test
sys.modules['arango'] = MagicMock()
sys.modules['arango.database'] = MagicMock()

try:
    from app.lib.db.client import ArangoClient
    from app.lib.auth.security import TokenEncryptor
    from app.domain.auth.models import UserCredentials, CredentialStatus
    from app.lib.auth.service import AuthService
    from app.domain.auth.controllers import AuthController
    
    print("SUCCESS: ALL AUTH & DB MODULES IMPORTED")
except ImportError as e:
    print(f"ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
