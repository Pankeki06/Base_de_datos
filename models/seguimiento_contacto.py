from datetime import datetime

from sqlmodel import SQLModel, Field as SqlModelField


class SeguimientoContacto(SQLModel, table=True):
    __tablename__ = "seguimiento_contacto"

    id_contacto: int | None = SqlModelField(default=None, primary_key=True)
    id_seguimiento: int = SqlModelField(foreign_key="seguimiento.id_seguimiento", index=True)
    iniciado_por: str = SqlModelField(max_length=10)
    tipo_contacto: str = SqlModelField(max_length=20)
    observaciones: str = SqlModelField(max_length=1000)
    resultado: str = SqlModelField(max_length=20)
    fecha_hora: datetime
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
