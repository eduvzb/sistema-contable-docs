# Plan técnico — SPEC-006

Este plan cubre sólo CA-006-19 revisado y CA-006-20 a CA-006-24 de [spec.md](spec.md). Antes de implementar, contrastar los contratos propuestos con el código actual de backend y frontend. El desglose fiscal de SPEC-004 ya está disponible.

## Contrato de propuestas

`POST /api/companies/{companyId}/accounting-periods/{periodId}/accounting-policy-entry-previews` recibe `fiscal_document_ids` en orden y devuelve bloques de partidas por CFDI, su componente de origen, cuentas sugeridas y errores asociados al UUID. La operación no guarda pólizas. Sólo usa CFDI autorizados de la empresa y admite generación para `I`/`E` en MXN cuyos datos fiscales cuadran a seis decimales. Un CFDI inválido no impide generar los demás bloques válidos.

Los contratos de guardado y consulta de póliza incorporan `source_fiscal_document_id` y `source_component_key` opcionales por partida. El backend valida que cada origen pertenece a la empresa y a los documentos relacionados con la póliza. Al guardar DRAFT o POSTED actualiza la memoria de cuentas en la misma transacción; la clave es empresa, emisor, dirección, tipo, PUE/PPD y componente. Los importes siempre proceden del CFDI seleccionado, nunca de la memoria. Una póliza POSTED sigue exigiendo balance y cuentas operables.

## Interfaz e integración

La ventana «CFDI relacionados» utiliza CFDI del periodo cargados y autorizados, conserva selección ordenada y vínculos previos de otros periodos. «Continuar» solicita propuestas y abre bloques editables; no guarda la póliza. Los errores por UUID y los casos de captura manual permanecen visibles. Al asignar una cuenta, sólo se propaga a componentes equivalentes del mismo emisor que todavía estén vacíos; no altera importes ni cuentas elegidas manualmente.

Orden de trabajo: contrato de desglose SPEC-004 → [propuesta backend](tasks-backend.md) → [ventana y bloques frontend](tasks-frontend.md) → memoria y guardado → pruebas de integración y regresión. Backend valida autorización, exactitud decimal, integridad y atomicidad; frontend prueba interacción con Vitest y React Testing Library. La disposición visual real se revisa en QA humana.

## Datos de prueba

La validación de CA-006-21/22/23/24 usa datos aislados del entorno de pruebas (`RefreshDatabase` y fixtures). Se comprueba que previsualizar no cree pólizas, que los guardados válidos conserven el origen y actualicen la memoria de cuentas, y que errores de autorización/integridad no dejen escrituras parciales. No se requiere reiniciar datos de una base compartida ni ejecutar una operación destructiva. Los resultados se registran en [verificación](verificacion.md).
