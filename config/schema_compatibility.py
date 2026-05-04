"""Utilidades para aplicar compatibilidad de esquema en bases legadas."""

from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def ensure_schema_compatibility(engine: Engine) -> list[str]:
    """Aplica ajustes mínimos para bases legadas y devuelve las acciones ejecutadas."""
    if engine.dialect.name != "mysql":
        return []

    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    missing_tables = {"beneficiario", "poliza"} - table_names
    if missing_tables:
        return []

    column_names = {column["name"] for column in inspector.get_columns("beneficiario")}
    index_names = {index["name"] for index in inspector.get_indexes("beneficiario")}
    fk_names = {foreign_key["name"] for foreign_key in inspector.get_foreign_keys("beneficiario")}
    executed_actions: list[str] = []

    try:
        with engine.begin() as connection:
            if "id_poliza" not in column_names:
                connection.execute(text("ALTER TABLE beneficiario ADD COLUMN id_poliza INT NULL AFTER id_asegurado"))
                executed_actions.append("Added beneficiario.id_poliza")
            if "idx_beneficiario_id_poliza" not in index_names:
                connection.execute(text("CREATE INDEX idx_beneficiario_id_poliza ON beneficiario (id_poliza)"))
                executed_actions.append("Created idx_beneficiario_id_poliza")
            if "fk_beneficiario_poliza" not in fk_names:
                connection.execute(
                    text(
                        "ALTER TABLE beneficiario "
                        "ADD CONSTRAINT fk_beneficiario_poliza "
                        "FOREIGN KEY (id_poliza) REFERENCES poliza(id_poliza) ON DELETE CASCADE"
                    )
                )
                executed_actions.append("Created fk_beneficiario_poliza")
    except Exception as exc:  # noqa: BLE001
        import logging as _logging
        _logging.getLogger(__name__).error("schema_compatibility error: %s", exc)

    return executed_actions