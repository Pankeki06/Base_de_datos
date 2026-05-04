"""Modelo de relacion asegurado-poliza."""

from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class AseguradoPoliza(SQLModel, table=True):
    __tablename__ = "asegurado_poliza"

    id_asegurado_poliza: int | None = SqlModelField(default=None, primary_key=True)
    id_poliza: int = SqlModelField(foreign_key="poliza.id_poliza", index=True)
    id_asegurado: int = SqlModelField(foreign_key="asegurado.id_asegurado", index=True)
    tipo_participante: str = SqlModelField(max_length=20)
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
