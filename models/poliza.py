"""Modelo de póliza."""

import uuid
from datetime import date, datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Poliza(SQLModel, table=True):
    id_poliza: int = SqlModelField(default=None, primary_key=True)
    id_asegurado: str = SqlModelField(foreign_key="asegurado.id_asegurado", max_length=36)
    numero_poliza: str = SqlModelField(unique=True, max_length=100)
    tipo_seguro: str = SqlModelField(max_length=100)
    fecha_inicio: date
    fecha_vencimiento: date
    estatus: str = SqlModelField(max_length=20)
    prima_mensual: float = SqlModelField(default=0.0)
    created_at: datetime | None = SqlModelField(default_factory=datetime.utcnow)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.utcnow)
    deleted_at: datetime | None = SqlModelField(default=None)
