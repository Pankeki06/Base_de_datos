"""Modelo de beneficiario."""

from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Beneficiario(SQLModel, table=True):
    id_beneficiario: int = SqlModelField(default=None, primary_key=True)
    id_asegurado: int = SqlModelField(foreign_key="asegurado.id_asegurado")
    nombre_completo: str = SqlModelField(max_length=255)
    parentesco: str = SqlModelField(max_length=50)
    porcentaje_participacion: float = SqlModelField(default=0.0)
    telefono: str | None = SqlModelField(default=None, max_length=20)
    activo: bool = SqlModelField(default=True)
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
