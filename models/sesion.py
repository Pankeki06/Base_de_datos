"""Modelo de sesión de acceso."""

from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Sesion(SQLModel, table=True):
    id_sesion: int = SqlModelField(default=None, primary_key=True)
    id_agente: str = SqlModelField(foreign_key="agente.id_agente", max_length=36)
    inicio_sesion: datetime
    fin_sesion: datetime | None = SqlModelField(default=None)
