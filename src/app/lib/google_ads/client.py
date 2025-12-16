import os
import yaml
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from app.lib.db.client import ArangoClient
from app.lib.auth.security import TokenEncryptor
from app.domain.auth.models import UserCredentials, CredentialStatus
import msgspec

class GoogleAdsClientFactory:
    """
    Factory for creating authenticated GoogleAdsClient instances.
    Handles strict security requirements:
    1. Retrieval of encrypted credentials.
    2. Decryption of Refresh Token using Envelope Encryption.
    3. Construction of the client config.
    """
    def __init__(self, db: ArangoClient):
        self.db = db.get_db()
        self.encryptor = TokenEncryptor()
        
        # Load static config (Developer Token, Client ID/Secret)
        # In prod these come from env, but the lib expects a dict or file
        self.base_config = {
            "developer_token": os.getenv("GOOGLE_DEVELOPER_TOKEN"),
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "use_proto_plus": True
        }

    def create_client(self, user_id: str) -> GoogleAdsClient:
        """
        Creates a client for a specific user context.
        """
        # 1. Fetch Credentials
        col = self.db.collection("UserCredentials")
        if not col.has(user_id):
            raise ValueError(f"No credentials found for user {user_id}")
            
        doc = col.get(user_id)
        creds = msgspec.convert(doc, type=UserCredentials)
        
        if creds.status != CredentialStatus.ACTIVE:
            raise ValueError(f"Credentials for {user_id} are not ACTIVE (Status: {creds.status})")

        # 2. Decrypt Refresh Token
        try:
            refresh_token = self.encryptor.decrypt({
                "encrypted_refresh_token": creds.encrypted_refresh_token,
                "iv": creds.iv,
                "auth_tag": creds.auth_tag
            })
        except Exception as e:
            # SECURITY ALERT: Decryption failed. Potential tampering or key mismatch.
            print(f"CRITICAL SECURITY ALERT: Decryption failed for user {user_id}: {e}")
            raise e

        # 3. Construct Final Config
        config = self.base_config.copy()
        config["refresh_token"] = refresh_token
        
        # 4. Initialize Client
        # We assume v17 or latest stable
        return GoogleAdsClient.load_from_dict(config, version="v17")

async def get_google_ads_factory() -> GoogleAdsClientFactory:
    db = ArangoClient()
    return GoogleAdsClientFactory(db)
