# Tareas de backend — SPEC-004

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

- [ ] **BE-004-01 — Extraer y persistir descuento y líneas fiscales estructuradas en la primera importación CFDI 4.0, sin conservar el XML.**
  - CA: CA-004-11.
  - Depende de: ninguna.
  - Hecho cuando: La consulta devuelve descuento y cada impuesto con naturaleza, alcance e importe decimal conforme al contrato de plan.md.

- [ ] **BE-004-02 — Probar traslados, retenciones, impuestos locales, valores ausentes y conservación del resultado anterior del lote.**
  - CA: CA-004-11.
  - Depende de: BE-004-01.
  - Hecho cuando: Las pruebas backend focalizadas y regresiones pasan; la evidencia real se registra en verificacion.md.
