"""Modelo de beneficiario."""

import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Beneficiario(SQLModel, table=True):
    id_beneficiario: int = SqlModelField(default=None, primary_key=True)
    id_asegurado: str = SqlModelField(foreign_key="asegurado.id_asegurado", max_length=36)
    nombre_completo: str = SqlModelField(max_length=255)
    parentesco: str = SqlModelField(max_length=50)
    porcentaje_participacion: float = SqlModelField(default=0.0)
    telefono: str | None = SqlModelField(default=None, max_length=20)
    activo: bool = SqlModelField(default=True)
    created_at: datetime | None = SqlModelField(default_factory=datetime.utcnow)
    deleted_at: datetime | None = SqlModelField(default=None)
