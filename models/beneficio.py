from datetime import datetime

from sqlmodel import SQLModel, Field as SqlModelField
from models.producto_beneficio import ProductoBeneficio  # noqa: F401


class Beneficio(SQLModel, table=True):
    id_beneficio: int | None = SqlModelField(default=None, primary_key=True)
    id_poliza: int = SqlModelField(foreign_key="poliza.id_poliza")
    id_producto_beneficio: int | None = SqlModelField(
        default=None,
        foreign_key="producto_beneficio.id_producto_beneficio",
    )
    id_asegurado: int | None = SqlModelField(
        default=None,
        foreign_key="asegurado.id_asegurado",
    )
    nombre_beneficio_extra: str | None = SqlModelField(default=None, max_length=255)
    descripcion_extra: str | None = SqlModelField(default=None, max_length=500)
    monto_override: float | None = SqlModelField(default=None)
    costo_aplicado: float = SqlModelField(default=0.0)
    vigente: bool = SqlModelField(default=True)
    deleted_at: datetime | None = SqlModelField(default=None)

    @property
    def id_asegurado_poliza(self) -> int | None:
        return self.id_asegurado
