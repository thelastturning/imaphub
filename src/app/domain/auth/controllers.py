from litestar import Controller, get, Response
from litestar.params import Parameter
from litestar.response import Redirect
from litestar.di import Provide

from app.lib.db.client import ArangoClient
from app.lib.auth.service import AuthService

# Dependency Factory
async def provide_auth_service() -> AuthService:
    return AuthService(ArangoClient())

class AuthController(Controller):
    path = "/auth"
    dependencies = {"auth_service": Provide(provide_auth_service)}

    @get("/login")
    async def login(self, auth_service: AuthService) -> Redirect:
        # In a real app, generate a secure random state tied to session
        state = "random_nonce_to_prevent_csrf" 
        url = auth_service.get_authorization_url(state)
        return Redirect(url)

    @get("/callback")
    async def callback(self, code: str, auth_service: AuthService, oauth_state: str = Parameter(query="state")) -> dict:
        # Verify state here
        if oauth_state != "random_nonce_to_prevent_csrf":
            return {"error": "Invalid State - CSRF detected"}
            
        # Hardcoded user_id for demo/prototype -> Should come from Session
        user_id = "default_user"
        
        return await auth_service.exchange_code(code, user_id)
