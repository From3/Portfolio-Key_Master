import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

backend = default_backend()
salt = b"0147"


def get_key_derivation_function() -> PBKDF2HMAC:
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=backend)


def encrypt_data(message: str, key: bytes) -> str:
    return Fernet(key).encrypt(message.encode()).decode()


def decrypt_data(message: str, key: bytes) -> str:
    return Fernet(key).decrypt(message.encode()).decode()


def encrypt_master_password(master_password: str) -> bytes:
    encrypted_master = base64.urlsafe_b64encode(get_key_derivation_function().derive(master_password.encode()))
    return encrypted_master
