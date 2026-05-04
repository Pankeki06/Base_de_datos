"""Utilidades de seguridad para autenticación."""

import base64
import hashlib
import hmac
import os
import string
import warnings

from dotenv import load_dotenv

load_dotenv(override=True)

_DEFAULT_SALT = "seguros_salt"
PASSWORD_SALT = os.getenv("PASSWORD_SALT", _DEFAULT_SALT)
if PASSWORD_SALT == _DEFAULT_SALT:
    warnings.warn(
        "PASSWORD_SALT no está configurado en las variables de entorno. "
        "Usando el valor por defecto inseguro. Defina PASSWORD_SALT en .env para producción.",
        stacklevel=1,
    )
PASSWORD_SCRYPT_N = int(os.getenv("PASSWORD_SCRYPT_N", "16384"))
PASSWORD_SCRYPT_R = int(os.getenv("PASSWORD_SCRYPT_R", "8"))
PASSWORD_SCRYPT_P = int(os.getenv("PASSWORD_SCRYPT_P", "1"))
PASSWORD_SCRYPT_DKLEN = int(os.getenv("PASSWORD_SCRYPT_DKLEN", "32"))
PASSWORD_SCRYPT_SALT_BYTES = int(os.getenv("PASSWORD_SCRYPT_SALT_BYTES", "16"))
_HASH_PREFIX = "scrypt"


def _legacy_hash_password(password: str) -> str:
    salted = f"{PASSWORD_SALT}:{password}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


def _encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def _decode_bytes(value: str) -> bytes:
    return base64.b64decode(value.encode("ascii"))


def is_legacy_password_hash(password_hash: str | None) -> bool:
    if not password_hash or len(password_hash) != 64:
        return False
    return all(character in string.hexdigits for character in password_hash)


def hash_password(password: str) -> str:
    salt = os.urandom(PASSWORD_SCRYPT_SALT_BYTES)
    derived_key = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=PASSWORD_SCRYPT_N,
        r=PASSWORD_SCRYPT_R,
        p=PASSWORD_SCRYPT_P,
        dklen=PASSWORD_SCRYPT_DKLEN,
    )
    return (
        f"{_HASH_PREFIX}${PASSWORD_SCRYPT_N}${PASSWORD_SCRYPT_R}${PASSWORD_SCRYPT_P}"
        f"${_encode_bytes(salt)}${_encode_bytes(derived_key)}"
    )


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash:
        return False

    if is_legacy_password_hash(password_hash):
        return hmac.compare_digest(_legacy_hash_password(password), password_hash)

    try:
        algorithm, n, r, p, salt_encoded, key_encoded = password_hash.split("$", 5)
        if algorithm != _HASH_PREFIX:
            return False

        salt = _decode_bytes(salt_encoded)
        expected_key = _decode_bytes(key_encoded)
        derived_key = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(expected_key),
        )
    except (TypeError, ValueError):
        return False

    return hmac.compare_digest(derived_key, expected_key)
