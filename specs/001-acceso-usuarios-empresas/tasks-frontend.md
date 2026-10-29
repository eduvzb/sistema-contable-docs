# Tareas de frontend — SPEC-001

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

## Tareas pendientes

- [ ] **FE-001-01 — Editar la empresa seleccionada.**
  - CA: CA-001-20.
  - Depende de: `PUT /api/companies/{companyId}`; reutilizar la API y campos de empresa existentes sin exponer ni duplicar credenciales FIEL.
  - Hecho cuando: administrador y contador asignado pueden abrir la edición desde la empresa, ver datos actuales con RFC no editable, guardar cambios o cancelar; errores de validación y pérdida de acceso se muestran sin presentar un guardado fallido como éxito. Vitest/React Testing Library comprueban permisos, precarga, edición, guardado, cancelación y errores.
