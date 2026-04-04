"""Modelo de agente."""

import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Agente(SQLModel, table=True):
    id_agente: str = SqlModelField(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    clave_agente: str = SqlModelField(index=True, unique=True, max_length=100)
    nombre: str = SqlModelField(max_length=100)
    apellido_paterno: str = SqlModelField(max_length=100)
    apellido_materno: str = SqlModelField(max_length=100)
    correo: str = SqlModelField(unique=True, max_length=255)
    telefono: str | None = SqlModelField(default=None, max_length=20)
    rol: str = SqlModelField(max_length=10)
    activo: bool = SqlModelField(default=True)
    password: str = SqlModelField(max_length=255)
    created_at: datetime | None = SqlModelField(default_factory=datetime.utcnow)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.utcnow)
