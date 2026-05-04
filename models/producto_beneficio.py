"""Modelo de beneficio base de un producto de póliza."""

from datetime import datetime

from sqlmodel import SQLModel, Field as SqlModelField


class ProductoBeneficio(SQLModel, table=True):
    __tablename__ = "producto_beneficio"

    id_producto_beneficio: int | None = SqlModelField(default=None, primary_key=True)
    id_producto: int = SqlModelField(foreign_key="producto_poliza.id_producto", index=True)
    nombre_beneficio: str = SqlModelField(max_length=255)
    descripcion: str = SqlModelField(max_length=500)
    monto_cobertura: float = SqlModelField(default=0.0)
    costo_extra: float | None = SqlModelField(default=None)
    incluido_base: bool = SqlModelField(default=True)
    activo: bool = SqlModelField(default=True)
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
