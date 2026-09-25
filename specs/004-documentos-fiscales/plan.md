# Plan técnico — SPEC-004

Este archivo describe la ejecución técnica de [SPEC-004](spec.md); los criterios funcionales vigentes y el estado sólo se definen allí.

## Contexto para ejecución

El alcance y los criterios de esta entrega están en [spec.md](spec.md); las tareas abiertas por repositorio identifican el trabajo pendiente. Consulta los contratos de las specs dependientes que esta ejecución consume. Las fuentes ya citadas en `spec.md` se reabren sólo ante una contradicción, un cambio posterior de regla o contrato, un supuesto que afecte el resultado, o una solicitud explícita de cambiar comportamiento.

## Plan técnico y contratos

- Backend: extracción en la solicitud y consulta aislada por empresa; persiste sólo datos normalizados, expone incorporación parcial, listado por periodo y el indicador derivado de pólizas `POSTED`. `original_path` permanece opcional sólo para inventariar archivos históricos; no se expone mediante API.
- Contrato de consulta: `GET /api/companies/{companyId}/fiscal-documents?period_id={periodId}` entrega la bandeja filtrada por mes y ejercicio de `issued_at`; cada elemento conserva el resumen y los campos fiscales extraídos. `GET /api/companies/{companyId}/fiscal-documents/{fiscalDocumentId}` entrega el mismo documento completo para consultar UUID, RFC emisor/receptor, fecha, serie, folio, subtotal, impuestos, total, método/forma de pago, moneda, tipo de cambio, tipo de comprobante, dirección y `accounted`.
- El contrato agrega `discount` decimal y `tax_lines[]` con `code`, `name`, `nature` (`TRANSFER`/`WITHHOLDING`), `scope` (`FEDERAL`/`LOCAL`) y `amount`, todos los importes como texto con seis decimales. No expone XML crudo.
- Frontend: carga múltiple, resultado por archivo, limpieza real del selector después de cada respuesta, reconciliación de la bandeja vigente y explicación de documentos importados fuera de la vista actual. Conserva filtros y página compatibles conforme a SPEC-002, con detalle seleccionable del CFDI, sin añadir descarga SAT ni automatizaciones fiscales. El detalle presenta los campos del contrato existente, sin recalcular importes ni convertir moneda.
- Ejemplos de archivos compatibles para desarrollo: [ejemplos de XML CFDI](../../docs/ejemplos/README.md).
- La política de lote se cerró como parcial. No requiere workers ni infraestructura adicional (DT-005).

Aplican las [decisiones técnicas compartidas](../../docs/decisiones.md). El contrato de consulta de esta brecha queda cerrado; cualquier ampliación posterior debe actualizar esta spec antes de modificar consumidores.

## Orden y coordinación

Las tareas pendientes se registran por repositorio en [backend](tasks-backend.md) y [frontend](tasks-frontend.md). El contrato responsable se prepara antes de implementarlo en un consumidor; las comprobaciones reales se registran en [verificación](verificacion.md).
