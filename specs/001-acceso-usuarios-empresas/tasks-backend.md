# Tareas de backend — SPEC-001

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

- [ ] **BE-001-01 — Ampliar el contrato de empresa y la transición de datos para nombre comercial, tipo derivado y versión de plantilla. Coordinar el alta atómica con SPEC-003.**
  - CA: CA-001-18/19.
  - Depende de: ninguna.
  - Hecho cuando: Las respuestas y validaciones de empresas nuevas y existentes satisfacen CA-001-18/19 sin dejar empresa ni catálogo parcial; pasan las pruebas backend previstas en plan.md.

- [ ] **BE-001-02 — Comprobar regresiones de RFC, régimen, autorización y asignación en el contrato ampliado.**
  - CA: CA-001-18/19.
  - Depende de: BE-001-01.
  - Hecho cuando: Las pruebas backend de casos válidos, inválidos y regresiones pasan y sus resultados reales quedan en verificacion.md.
