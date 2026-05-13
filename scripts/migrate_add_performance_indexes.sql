-- ============================================================
--  MIGRACIÓN: Índices de rendimiento para listado de asegurados
--  Ejecutar en bases de datos existentes de aseguradora
-- ============================================================
USE aseguradora;

CREATE INDEX IF NOT EXISTS idx_asegurado_agente_deleted
    ON asegurado(id_agente_responsable, deleted_at);

CREATE INDEX IF NOT EXISTS idx_asegurado_poliza_tipo
    ON asegurado(id_poliza, tipo_asegurado);

CREATE INDEX IF NOT EXISTS idx_poliza_asegurado_deleted
    ON poliza(id_asegurado, deleted_at);

CREATE INDEX IF NOT EXISTS idx_beneficiario_asegurado_deleted
    ON beneficiario(id_asegurado, deleted_at);
