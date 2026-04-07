"""Modelo de beneficio."""

import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field as SqlModelField


class Beneficio(SQLModel, table=True):
    id_beneficio: int = SqlModelField(default=None, primary_key=True)
    id_poliza: str = SqlModelField(foreign_key="poliza.id_poliza", max_length=36)
    nombre_beneficio: str = SqlModelField(max_length=255)
    descripcion: str = SqlModelField(max_length=500)
    monto_cobertura: float = SqlModelField(default=0.0)
    vigente: bool = SqlModelField(default=True)
