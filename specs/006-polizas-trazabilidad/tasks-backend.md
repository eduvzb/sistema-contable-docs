# Tareas de backend — SPEC-006

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

- [ ] **BE-006-01 — Implementar el endpoint de propuestas por CFDI con reconciliación exacta, errores por UUID y continuación parcial.**
  - CA: CA-006-21/22.
  - Depende de: BE-004-01 (CA-004-11 disponible).
  - Hecho cuando: CFDI válidos I/E en MXN generan bloques ordenados; descuadres, tipo P y otras monedas producen el resultado previsto sin persistir una póliza; pruebas backend pasan.

- [ ] **BE-006-02 — Conservar origen opcional de partidas y memoria de cuentas por la clave definida en la spec, validando empresa y documentos relacionados.**
  - CA: CA-006-23/24.
  - Depende de: BE-006-01.
  - Hecho cuando: Guardar DRAFT/POSTED actualiza sugerencias atómicamente y rechaza orígenes ajenos; pruebas de autorización, balance y regresión pasan.

- [ ] **BE-006-03 — Comprobar integración entre desglose fiscal, propuesta, guardado y trazabilidad.**
  - CA: CA-006-21/22/23/24.
  - Depende de: BE-006-01 y BE-006-02.
  - Hecho cuando: Las pruebas backend focalizadas y relevantes de regresión pasan y se documentan con revisión y PR.

- [ ] **BE-006-04 — Preparar y ejecutar únicamente la operación de reinicio de datos de prueba autorizada en la spec, fuera de migraciones repetibles.**
  - CA: CA-006-21/23 (preparación de datos); decisión de reinicio único en spec.md.
  - Depende de: respaldo y recuento previos.
  - Hecho cuando: Quedan registrados respaldo, recuentos antes/después y conservación de empresas, periodos, cuentas y pólizas no vinculadas.
