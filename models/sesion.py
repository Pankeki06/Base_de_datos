"""Modelo de sesión de acceso."""

import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Sesion(SQLModel, table=True):
    id_sesion: str = SqlModelField(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    id_agente: str = SqlModelField(foreign_key="agente.id_agente", max_length=36)
    inicio_sesion: datetime
    fin_sesion: datetime | None = SqlModelField(default=None)
    ip_origen: str = SqlModelField(max_length=100)
    dispositivo: str = SqlModelField(max_length=100)
