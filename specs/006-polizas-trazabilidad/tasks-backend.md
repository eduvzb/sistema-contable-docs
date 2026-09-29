# Tareas de backend — SPEC-006

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

- [x] **BE-006-01 — Implementar el endpoint de propuestas por CFDI con reconciliación exacta, errores por UUID y continuación parcial.**
  - CA: CA-006-21/22.
  - Depende de: desglose fiscal de CA-004-11 ya disponible en backend.
  - Hecho cuando: CFDI válidos I/E en MXN generan bloques ordenados; descuadres, tipo P y otras monedas producen el resultado previsto sin persistir una póliza; pruebas backend pasan.

- [x] **BE-006-02 — Conservar origen opcional de partidas y memoria de cuentas por la clave definida en la spec, validando empresa y documentos relacionados.**
  - CA: CA-006-23/24.
  - Depende de: BE-006-01.
  - Hecho cuando: Guardar DRAFT/POSTED actualiza sugerencias atómicamente y rechaza orígenes ajenos; pruebas de autorización, balance y regresión pasan.

- [x] **BE-006-03 — Comprobar integración entre desglose fiscal, propuesta, guardado y trazabilidad.**
  - CA: CA-006-21/22/23/24.
  - Depende de: BE-006-01 y BE-006-02.
  - Hecho cuando: Las pruebas backend focalizadas y relevantes de regresión pasan y se documentan con revisión y PR.

- [x] **BE-006-04 — Validar propuestas y memoria de cuentas con datos de prueba aislados, sin reiniciar bases compartidas.**
  - CA: CA-006-21/22/23/24.
  - Depende de: BE-006-01 y BE-006-02.
  - Hecho cuando: las pruebas aisladas verifican que previsualizar no persiste pólizas, que guardar conserva origen y sugerencias, que los errores no dejan escrituras parciales y que la regresión backend pasa.
