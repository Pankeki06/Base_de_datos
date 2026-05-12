"""Modelo de asegurado."""

from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Asegurado(SQLModel, table=True):
    id_asegurado: int | None = SqlModelField(default=None, primary_key=True)
    nombre: str = SqlModelField(max_length=100)
    apellido_paterno: str = SqlModelField(max_length=100)
    apellido_materno: str = SqlModelField(max_length=100)
    rfc: str = SqlModelField(unique=True, max_length=20)
    correo: str | None = SqlModelField(default=None, max_length=255)
    celular: str | None = SqlModelField(default=None, max_length=15)
    calle: str = SqlModelField(max_length=255)
    numero_exterior: str = SqlModelField(max_length=50)
    numero_interior: str | None = SqlModelField(default=None, max_length=50)
    colonia: str = SqlModelField(max_length=100)
    municipio: str = SqlModelField(max_length=100)
    estado: str = SqlModelField(max_length=100)
    codigo_postal: str = SqlModelField(max_length=20)
    tipo_asegurado: str = SqlModelField(
        default="titular",
        max_length=20,
        description="titular, conyuge, hijo, dependiente"
    )
    id_poliza: int | None = SqlModelField(
        default=None,
        foreign_key="poliza.id_poliza",
        index=True,
        description="NULL si es titular, NOT NULL si es dependiente de otra póliza"
    )
    id_agente_responsable: int | None = SqlModelField(default=None, foreign_key="agente.id_agente", index=True)
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
