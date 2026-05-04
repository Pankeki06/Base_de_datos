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


def test_verify_password_falla_con_contrasena_incorrecta():
    from services.security import hash_password, verify_password
    hashed = hash_password("correcta")
    assert verify_password("incorrecta", hashed) is False


def test_verify_password_legacy_falla_con_contrasena_incorrecta():
    import hashlib
    from services.security import PASSWORD_SALT, verify_password
    salted = f"{PASSWORD_SALT}:buena".encode("utf-8")
    legacy_hash = hashlib.sha256(salted).hexdigest()
    assert verify_password("mala", legacy_hash) is False


def test_hash_password_contrasena_muy_larga():
    from services.security import hash_password, verify_password
    pw = "A" * 1000
    hashed = hash_password(pw)
    assert verify_password(pw, hashed) is True
    assert verify_password("A" * 999, hashed) is False


def test_login_agente_sin_contrasena_no_autenticado(monkeypatch):
    """Sin password, login_agente debe rechazar aunque el agente exista."""
    import pytest
    import services.auth_service as _auth
    with pytest.raises(ValueError):
        _auth.login_agente("clave", "")
