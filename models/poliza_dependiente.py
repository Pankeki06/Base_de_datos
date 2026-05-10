from datetime import datetime

from sqlmodel import SQLModel, Field as SqlModelField


class PolizaDependiente(SQLModel, table=True):
    __tablename__ = "poliza_dependiente"

    id_poliza_dependiente: int | None = SqlModelField(default=None, primary_key=True)
    id_poliza: int = SqlModelField(foreign_key="poliza.id_poliza", index=True)
    id_asegurado: int = SqlModelField(foreign_key="asegurado.id_asegurado", index=True)
    parentesco: str = SqlModelField(max_length=20)
    created_at: datetime | None = SqlModelField(default_factory=datetime.now)
    updated_at: datetime | None = SqlModelField(default_factory=datetime.now)
    deleted_at: datetime | None = SqlModelField(default=None)
