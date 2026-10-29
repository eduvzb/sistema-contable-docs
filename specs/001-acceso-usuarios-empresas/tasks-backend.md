# Tareas de backend — SPEC-001

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

## Tareas pendientes

- [ ] **BE-001-01 — Actualizar datos de empresa con permiso vigente.**
  - CA: CA-001-20.
  - Depende de: contrato `PUT /api/companies/{companyId}` en [plan.md](plan.md); integración con permisos de empresa vigentes.
  - Hecho cuando: razón social, nombre comercial y régimen fiscal se validan y actualizan en una operación; RFC no se acepta en el payload ni cambia. Administrador y contador asignado pueden guardar; acceso inexistente/revocado y datos inválidos no producen cambios. Pruebas feature cubren persistencia, validación, aislamiento y actualización parcial inválida.
