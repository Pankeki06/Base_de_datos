"""Modelo de póliza."""

from datetime import date, datetime
from sqlmodel import SQLModel, Field as SqlModelField
from models.producto_poliza import ProductoPoliza  # noqa: F401


class Poliza(SQLModel, table=True):
    id_poliza: int | None = SqlModelField(default=None, primary_key=True)
    id_asegurado: int = SqlModelField(foreign_key="asegurado.id_asegurado")
    id_producto: int = SqlModelField(foreign_key="producto_poliza.id_producto")
    numero_poliza: str = SqlModelField(unique=True, max_length=100)
    fecha_inicio: date
    fecha_vencimiento: date
    estatus: str = SqlModelField(max_length=20)
    prima_mensual: float = SqlModelField(default=0.0)
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
