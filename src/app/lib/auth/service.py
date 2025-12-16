import os
import httpx
import msgspec
from litestar.exceptions import NotAuthorizedException

from app.lib.db.client import ArangoClient
from app.lib.auth.security import TokenEncryptor
from app.domain.auth.models import UserCredentials, CredentialStatus

class AuthService:
    def __init__(self, db: ArangoClient):
        self.db = db.get_db()
        self.encryptor = TokenEncryptor()
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")

    def get_authorization_url(self, state: str) -> str:
        """
        Constructs the Google OAuth2 URL with offline access.
        """
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        scope = "https://www.googleapis.com/auth/adwords"
        return (
            f"{base_url}?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&response_type=code"
            f"&scope={scope}"
            f"&access_type=offline"
            f"&prompt=consent"
            f"&state={state}"
        )

    async def exchange_code(self, code: str, user_id: str):
        """
        Exchanges code for tokens and securely stores the refresh token.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": self.redirect_uri,
                    }
                )
                
            if response.status_code != 200:
                raise NotAuthorizedException(detail=f"Google Auth Failed: {response.text}")
                
            token_data = response.json()
            refresh_token = token_data.get("refresh_token")
            
            if not refresh_token:
                 # This happens if the user didn't see the consent screen (prompt=consent missing)
                 raise NotAuthorizedException(detail="No Refresh Token returned. Please re-authorize.")
                 
            # Encrypt
            encrypted = self.encryptor.encrypt(refresh_token)
            
            # Store in DB
            creds = UserCredentials(
                _key=user_id,
                google_account_id="PENDING_FETCH", 
                encrypted_refresh_token=encrypted["encrypted_refresh_token"],
                iv=encrypted["iv"],
                auth_tag=encrypted["auth_tag"],
                key_version=encrypted["key_version"],
                status=CredentialStatus.ACTIVE
            )
            
            # Upsert into UserCredentials collection
            col = self.db.collection("UserCredentials")
            if not col.has(user_id):
                col.insert(msgspec.to_builtins(creds), overwrite=True)
            else:
                col.update({"_key": user_id}, msgspec.to_builtins(creds))
                
            return {"status": "success", "message": "Credentials stored securely."}
        except Exception as e:
            print(f"ERROR in exchange_code: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
