# Plan técnico — SPEC-009

Este archivo describe la ejecución técnica de [SPEC-009](spec.md); los criterios funcionales vigentes y el estado sólo se definen allí.

## Contexto para ejecución

El alcance y los criterios de esta entrega están en [spec.md](spec.md); las tareas abiertas por repositorio identifican el trabajo pendiente. Consulta los contratos de las specs dependientes que esta ejecución consume. Las fuentes ya citadas en `spec.md` se reabren sólo ante una contradicción, un cambio posterior de regla o contrato, un supuesto que afecte el resultado, o una solicitud explícita de cambiar comportamiento.

## Plan técnico y contratos

- Backend: consume los contratos de SPEC-004/006/008 y expone `GET /api/companies/{companyId}/accounting-periods/{periodId}/reports/{report}.xlsx`, donde `report` es `fiscal-documents`, `accounting-policies` o `trial-balance`.
- El contrato de filas usa columnas estables y este orden: XML `issued_at`, `document_type`, `direction`, `issuer_rfc`, `issuer_name`, `recipient_rfc`, `recipient_name`, `uuid`, `series`, `folio`, `payment_method`, `payment_form`, `currency`, `exchange_rate`, `subtotal`, `tax_total`, `total`, `accounted`; pólizas `entry_date`, `type`, `display_number`, `status`, `policy_concept`, `position`, `account_code`, `account_name`, `entry_concept`, `reference`, `debit`, `credit`; balanza `code`, `name`, `nature`, `opening_balance`, `debit_total`, `credit_total`, `closing_balance`.
- Las filas XML se ordenan por `issued_at` descendente e `id` descendente; las pólizas por `entry_date` descendente e `id` descendente y sus partidas por `position` ascendente; la balanza conserva el orden de SPEC-008. Una póliza sin partidas genera una fila con campos de partida vacíos.
- Todos los importes se escriben como texto con seis decimales; fechas e identificadores se escriben como texto; los valores booleanos usan `true`/`false`. La exportación no recalcula saldos ni agrega fórmulas.
- Frontend: añade una acción de exportar a cada vista existente, usando el periodo visible y mostrando errores sin abandonar el contexto.
- El XLSX se genera con las extensiones nativas disponibles, sin añadir dependencias ni migraciones.

Aplican las [decisiones técnicas compartidas](../../docs/decisiones.md). El contrato de exportación queda cerrado para el alcance MVP; cualquier filtro, formato adicional o procesamiento asíncrono posterior debe actualizar esta spec antes de modificar consumidores.

## Orden y coordinación

Las tareas pendientes se registran por repositorio en [backend](tasks-backend.md) y [frontend](tasks-frontend.md). El contrato responsable se prepara antes de implementarlo en un consumidor; las comprobaciones reales se registran en [verificación](verificacion.md).
