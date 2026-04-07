"""Modelo de beneficio."""

from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Beneficio(SQLModel, table=True):
    id_beneficio: int = SqlModelField(default=None, primary_key=True)
    id_poliza: int = SqlModelField(foreign_key="poliza.id_poliza")
    nombre_beneficio: str = SqlModelField(max_length=255)
    descripcion: str = SqlModelField(max_length=500)
    monto_cobertura: float = SqlModelField(default=0.0)
    vigente: bool = SqlModelField(default=True)
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
