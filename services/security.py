"""Utilidades de seguridad para autenticación."""

import hashlib
import os

from dotenv import load_dotenv

load_dotenv(override=True)

PASSWORD_SALT = os.getenv("PASSWORD_SALT", "seguros_salt")


def hash_password(password: str) -> str:
    salted = f"{PASSWORD_SALT}:{password}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash
