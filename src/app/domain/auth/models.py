import msgspec
from typing import Optional
from enum import Enum
import time

class CredentialStatus(str, Enum):
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    NEEDS_REAUTH = "NEEDS_REAUTH"

class UserCredentials(msgspec.Struct):
    """
    Schema for secure credential storage in ArangoDB.
    Strictly follows BACKEND-SPEC.md Table 1.
    """
    _key: str  # User ID
    google_account_id: str
    encrypted_refresh_token: str
    iv: str
    auth_tag: str
    key_version: int
    status: CredentialStatus
    updated_at: float = msgspec.field(default_factory=time.time)
