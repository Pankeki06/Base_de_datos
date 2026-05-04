"""Modelo de catálogo de productos de póliza."""

from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class ProductoPoliza(SQLModel, table=True):
    __tablename__ = "producto_poliza"

    id_producto: int | None = SqlModelField(default=None, primary_key=True)
    nombre: str = SqlModelField(unique=True, max_length=150)
    descripcion: str | None = SqlModelField(default=None)
    tipo_seguro: str = SqlModelField(max_length=100)
    prima_base: float = SqlModelField(default=0.0)
    activo: bool = SqlModelField(default=True)
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
