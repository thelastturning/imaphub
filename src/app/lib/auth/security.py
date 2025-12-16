import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class TokenEncryptor:
    """
    Handles AES-256-GCM encryption for sensitive tokens.
    Uses APP_MASTER_KEY from environment variables.
    """
    def __init__(self):
        master_key_b64 = os.getenv("APP_MASTER_KEY")
        if not master_key_b64:
            # Fallback for dev/test only - NEVER use in prod
            # In a real environment, this should raise an error
            print("WARNING: APP_MASTER_KEY not set. Using insecure default for development.")
            self.kek = AESGCM.generate_key(bit_length=256)
        else:
            self.kek = base64.urlsafe_b64decode(master_key_b64)
            
        self.aesgcm = AESGCM(self.kek)

    def encrypt(self, plain_text: str) -> dict:
        """
        Encrypts a string using AES-GCM.
        Returns dict with 'ciphertext', 'iv', 'tag'.
        """
        iv = os.urandom(12)  # NIST recommended 96-bit IV
        data = plain_text.encode('utf-8')
        ciphertext_with_tag = self.aesgcm.encrypt(iv, data, None)
        
        # Split tag (last 16 bytes) and ciphertext
        tag = ciphertext_with_tag[-16:]
        ciphertext = ciphertext_with_tag[:-16]
        
        return {
            "encrypted_refresh_token": base64.b64encode(ciphertext).decode('utf-8'),
            "iv": base64.b64encode(iv).decode('utf-8'),
            "auth_tag": base64.b64encode(tag).decode('utf-8'),
            "key_version": 1
        }

    def decrypt(self, encrypted_data: dict) -> str:
        """
        Decrypts data using the stored IV and Tag.
        """
        iv = base64.b64decode(encrypted_data['iv'])
        tag = base64.b64decode(encrypted_data['auth_tag'])
        ciphertext = base64.b64decode(encrypted_data['encrypted_refresh_token'])
        
        # Reconstruct format expected by cryptography library (ciphertext + tag)
        data = ciphertext + tag
        
        plaintext = self.aesgcm.decrypt(iv, data, None)
        return plaintext.decode('utf-8')
