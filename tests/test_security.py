import hashlib
from types import SimpleNamespace

import services.auth_service as auth_service
from services.security import PASSWORD_SALT, hash_password, is_legacy_password_hash, verify_password


def _legacy_hash(password: str) -> str:
    salted = f"{PASSWORD_SALT}:{password}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


def test_hash_password_generates_modern_hash_and_verifies():
    password_hash = hash_password("1234")

    assert password_hash.startswith("scrypt$")
    assert verify_password("1234", password_hash) is True
    assert verify_password("wrong", password_hash) is False


def test_verify_password_accepts_legacy_sha256_hash():
    legacy_hash = _legacy_hash("1234")

    assert is_legacy_password_hash(legacy_hash) is True
    assert verify_password("1234", legacy_hash) is True
    assert verify_password("wrong", legacy_hash) is False


def test_login_agente_rehashes_legacy_password(monkeypatch):
    legacy_hash = _legacy_hash("1234")
    agente = SimpleNamespace(id_agente=7, password=legacy_hash)
    update_calls = []

    monkeypatch.setattr(
        auth_service.AgenteRepository,
        "get_agente_by_clave",
        lambda clave_agente: agente,
    )

    def _update_agente(id_agente: int, updated_data: dict):
        update_calls.append((id_agente, updated_data))
        return SimpleNamespace(id_agente=id_agente, password=updated_data["password"])

    monkeypatch.setattr(
        auth_service.AgenteRepository,
        "update_agente",
        _update_agente,
    )

    result = auth_service.login_agente("admin1", "1234")

    assert result is not None
    assert result.password.startswith("scrypt$")
    assert len(update_calls) == 1
    assert update_calls[0][0] == 7
    assert verify_password("1234", update_calls[0][1]["password"]) is True