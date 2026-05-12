from datetime import datetime

from sqlmodel import SQLModel, Field as SqlModelField


class Beneficio(SQLModel, table=True):
    id_beneficio: int | None = SqlModelField(default=None, primary_key=True)
    id_poliza: int = SqlModelField(foreign_key="poliza.id_poliza")
    id_producto_beneficio: int = SqlModelField(foreign_key="producto_beneficio.id_producto_beneficio")
    id_asegurado: int | None = SqlModelField(
        default=None,
        foreign_key="asegurado.id_asegurado",
        description="NULL = aplica a toda la póliza (titular), NOT NULL = aplica solo a este dependiente"
    )
    monto_override: float | None = SqlModelField(default=None)
    costo_aplicado: float = SqlModelField(default=0.0)
    vigente: bool = SqlModelField(default=True)
    deleted_at: datetime | None = SqlModelField(default=None)
