"""Compatibilidad para acceso a conexión compartida de base de datos."""

from config.database import DATABASE_URL, create_session, engine

__all__ = ["DATABASE_URL", "engine", "create_session"]
