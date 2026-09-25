# Tareas de backend — SPEC-005

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

- [ ] **BE-005-01 — Revisar en el backend la reutilización del importador sin almacenamiento durable del XML y comprobar si queda alguna brecha técnica de la actualización.**
  - CA: CA-005-02/04, DT-013.
  - Depende de: SPEC-004: contrato de incorporación vigente.
  - Hecho cuando: Los casos de incorporación, duplicado, aislamiento y continuidad hacia póliza pasan; cualquier brecha se corrige y el resultado, revisión y PR se registran en verificacion.md.
