"""Servicio de autenticación para el login básico."""

from sqlmodel import select
from services.database import create_session
from models.agente import Agente


def authenticate(clave_agente: str, password: str) -> bool:
    """Valida las credenciales de un agente contra la base de datos."""
    with create_session() as session:
        statement = (
            select(Agente)
            .where(Agente.clave_agente == clave_agente)
            .where(Agente.password == password)
            .where(Agente.activo == True)
        )
        return session.exec(statement).first() is not None
