"""Modelo de beneficio."""

from datetime import datetime

from sqlmodel import SQLModel, Field as SqlModelField
from models.asegurado_poliza import AseguradoPoliza  # noqa: F401
from models.producto_beneficio import ProductoBeneficio  # noqa: F401


class Beneficio(SQLModel, table=True):
    id_beneficio: int | None = SqlModelField(default=None, primary_key=True)
    id_poliza: int = SqlModelField(foreign_key="poliza.id_poliza")
    id_producto_beneficio: int | None = SqlModelField(
        default=None,
        foreign_key="producto_beneficio.id_producto_beneficio",
    )
    id_asegurado_poliza: int | None = SqlModelField(
        default=None,
        foreign_key="asegurado_poliza.id_asegurado_poliza",
    )
    nombre_beneficio: str = SqlModelField(max_length=255)
    descripcion: str = SqlModelField(max_length=500)
    monto_cobertura: float = SqlModelField(default=0.0)
    costo_aplicado: float = SqlModelField(default=0.0)
    monto_override: float | None = SqlModelField(default=None)
    vigente: bool = SqlModelField(default=True)
    deleted_at: datetime | None = SqlModelField(default=None)
