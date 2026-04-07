"""Modelo de seguimiento."""

import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Seguimiento(SQLModel, table=True):
    id_seguimiento: int = SqlModelField(default=None, primary_key=True)
    id_asegurado: str = SqlModelField(foreign_key="asegurado.id_asegurado", max_length=36)
    id_agente: str = SqlModelField(foreign_key="agente.id_agente", max_length=36)
    tipo_contacto: str = SqlModelField(max_length=20)
    observaciones: str = SqlModelField(max_length=1000)
    resultado: str = SqlModelField(max_length=20)
    fecha_hora: datetime
    created_at: datetime | None = SqlModelField(default_factory=datetime.utcnow)
    deleted_at: datetime | None = SqlModelField(default=None)
