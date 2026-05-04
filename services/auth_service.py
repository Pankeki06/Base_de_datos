"""Servicio de autenticación de agentes."""

from repositories.agente_repository import AgenteRepository
from services.security import hash_password, is_legacy_password_hash, verify_password
from services.validators import validar_requerido


def login_agente(clave_agente: str, password: str):
    validar_requerido(clave_agente, "clave_agente")
    validar_requerido(password, "password")

    agente = AgenteRepository.get_agente_by_clave(clave_agente)
    if not agente:
        return None

    if not verify_password(password, agente.password):
        return None

    if is_legacy_password_hash(agente.password):
        updated_agente = AgenteRepository.update_agente(
            agente.id_agente,
            {"password": hash_password(password)},
        )
        if updated_agente is not None:
            agente = updated_agente
    return agente


def authenticate(clave_agente: str, password: str) -> bool:
    """Compatibilidad con el flujo actual de login en Flet."""
    return login_agente(clave_agente, password) is not None
