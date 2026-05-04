"""Modelo de beneficio."""

from datetime import datetime

from sqlmodel import SQLModel, Field as SqlModelField


class Beneficio(SQLModel, table=True):
    id_beneficio: int | None = SqlModelField(default=None, primary_key=True)
    id_poliza: int = SqlModelField(foreign_key="poliza.id_poliza", index=True)
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
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
