# Estrategia de Borrado Logico

## Regla general

- `deleted_at`: indica eliminacion logica. El registro no debe salir en consultas operativas por defecto.
- `activo` / `vigente`: indican estado de negocio. No reemplazan al borrado logico.

## Recomendacion por tabla

| Tabla | deleted_at | activo | vigente | Recomendacion |
| --- | --- | --- | --- | --- |
| `agente` | Si | No | No | Mantener solo `deleted_at`. Un agente eliminado no debe autenticarse ni asignarse. |
| `asegurado` | Si | No | No | Mantener solo `deleted_at`. Preserva historial comercial y operativo. |
| `poliza` | Si | No | No | Mantener `deleted_at` y seguir usando `estatus` como estado funcional. |
| `asegurado_poliza` | Si | No | No | Mantener `deleted_at` para conservar el historial de participantes cubiertos. |
| `beneficiario` | Si | No | No | Mantener solo `deleted_at`. El porcentaje es regla de negocio, no estado. |
| `beneficio` | Si | No | Si | Usar ambos. `deleted_at` elimina logicamente; `vigente` indica si la cobertura sigue aplicando. |
| `producto_poliza` | Si | Si | No | Usar ambos. `activo` controla disponibilidad comercial; `deleted_at` audita retiro logico. |
| `producto_beneficio` | Si | Si | No | Usar ambos. `activo` controla si se copia a nuevas pólizas; `deleted_at` conserva trazabilidad. |
| `seguimiento` | Si | No | No | Mantener solo `deleted_at`. Es historial operativo. |
| `sesion` futura | Si | No | No | Recomendado si se quiere invalidacion o limpieza logica sin perder auditoria. |

## Criterios de implementacion

1. Las consultas operativas deben excluir `deleted_at IS NOT NULL`.
2. Las banderas `activo` y `vigente` deben seguir disponibles para reglas de negocio y reportes.
3. Un borrado logico no debe sustituir cambios de estado funcional.
4. Para `beneficio`, el delete operativo debe marcar `deleted_at` y dejar `vigente = FALSE` para compatibilidad transitoria.
5. Si se implementan vistas historicas o reportes de auditoria, deben consultar tambien registros con `deleted_at`.

## Migracion aplicada en esta fase

- `beneficio` ahora acepta `deleted_at` en schema y modelo.
- `BeneficioRepository` filtra por `deleted_at IS NULL` y `vigente = TRUE`.
- El delete logico de beneficios marca `deleted_at` y tambien `vigente = FALSE`.
- `producto_poliza` y `producto_beneficio` ahora usan `deleted_at` ademas de `activo`.
- Las consultas operativas de catalogo excluyen registros eliminados logicamente.

## Siguiente extension sugerida

1. Crear helpers compartidos para filtros `deleted_at` en repositorios.
2. Unificar pruebas de soft delete por entidad.
3. Agregar scripts de migracion para bases ya creadas fuera de `create_database.sql`.