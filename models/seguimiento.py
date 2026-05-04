"""Modelo de seguimiento."""

from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Seguimiento(SQLModel, table=True):
    id_seguimiento: int | None = SqlModelField(default=None, primary_key=True)
    id_asegurado: int = SqlModelField(foreign_key="asegurado.id_asegurado", index=True)
    id_agente: int = SqlModelField(foreign_key="agente.id_agente", index=True)
    tipo_contacto: str = SqlModelField(max_length=20)
    observaciones: str = SqlModelField(max_length=1000)
    resultado: str = SqlModelField(max_length=20)
    fecha_hora: datetime
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
