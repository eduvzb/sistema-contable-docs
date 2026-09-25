# Plan técnico — SPEC-008

Este archivo describe la ejecución técnica de [SPEC-008](spec.md); los criterios funcionales vigentes y el estado sólo se definen allí.

## Contexto para ejecución

El alcance y los criterios de esta entrega están en [spec.md](spec.md); las tareas abiertas por repositorio identifican el trabajo pendiente. Consulta los contratos de las specs dependientes que esta ejecución consume. Las fuentes ya citadas en `spec.md` se reabren sólo ante una contradicción, un cambio posterior de regla o contrato, un supuesto que afecte el resultado, o una solicitud explícita de cambiar comportamiento.

## Plan técnico y contratos

- Backend: `GET /api/companies/{companyId}/accounting-periods/{periodId}/trial-balance`, protegido por Sanctum y la misma visibilidad de empresa de las demás funciones. Devuelve `{ data, meta }`; `data` contiene una fila por cuenta con `account_id`, `code`, `name`, `nature`, `accepts_entries`, `active`, `opening_balance`, `debit_total`, `credit_total` y `closing_balance`. Todos los importes son textos de seis decimales. `meta` identifica `company_id`, `accounting_period_id`, `year`, `month` y `decimal_scale: 6`.
- El cálculo consulta únicamente partidas de pólizas `POSTED` de la empresa y periodo correspondiente. Las partidas de `DRAFT`, otras empresas y periodos posteriores quedan fuera. La consulta es agregada por cuenta y no duplica partidas por relaciones con CFDI.
- Frontend: el espacio de trabajo consulta este endpoint cuando existe un periodo seleccionado y presenta la balanza en una vista propia; el contexto de empresa y periodo sigue siendo explícito.
- SPEC-009 consumirá este mismo contrato, sin repetir el cálculo ni crear otra fuente de saldos.

Aplican las [decisiones técnicas compartidas](../../docs/decisiones.md). Los contratos de este alcance quedan cerrados para la implementación descrita; cualquier ampliación de saldos iniciales o agregación deberá actualizar esta spec antes de implementarse.

## Orden y coordinación

Las tareas pendientes se registran por repositorio en [backend](tasks-backend.md) y [frontend](tasks-frontend.md). El contrato responsable se prepara antes de implementarlo en un consumidor; las comprobaciones reales se registran en [verificación](verificacion.md).
