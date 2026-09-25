# Tareas de frontend — SPEC-001

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

- [ ] **FE-001-01 — Actualizar el alta y la consulta de empresa para mostrar nombre comercial como dato secundario y tipo de persona derivado del RFC.**
  - CA: CA-001-18/19.
  - Depende de: BE-001-01 (contrato disponible).
  - Hecho cuando: La interfaz permite el alta válida y presenta los dos campos sin sustituir la razón social.

- [ ] **FE-001-02 — Agregar pruebas de componentes y comportamiento para el alta, las validaciones visibles y la jerarquía de datos.**
  - CA: CA-001-18/19.
  - Depende de: FE-001-01.
  - Hecho cuando: `pnpm test`, lint, typecheck y build pasan; los resultados se registran en verificacion.md.
