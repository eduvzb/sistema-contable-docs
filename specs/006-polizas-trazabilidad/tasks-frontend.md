# Tareas de frontend — SPEC-006

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

## FE-006-07 — Opción en Administración

- [ ] Incorporar contrato, servicio, hook y sección de Configuración global en el área administrativa existente.
- **CA:** CA-006-30/34/35.
- **Depende de:** [BE-006-07](tasks-backend.md#be-006-07--configuración-global-de-reutilización).
- **Hecho cuando:** el administrador consulta y guarda la opción con estados de carga, éxito y error recuperable; el contador no dispone de su edición. Pruebas con Vitest y React Testing Library cubren ambas posiciones, persistencia al recargar, fallo de carga/guardado y reintento. Los componentes no llaman directamente a API y el contrato se exporta para uso del editor.

## FE-006-08 — Disponibilidad en el selector de CFDI

- [ ] Actualizar configuración y vínculos al abrir el selector, bloquear nuevas selecciones usadas sin ocultarlas y conservar relaciones previas al editar.
- **CA:** CA-006-07/20/31/33/34/35.
- **Depende de:** FE-006-07 y [BE-006-08](tasks-backend.md#be-006-08--validación-atómica-de-vínculos-nuevos).
- **Hecho cuando:** pruebas de componentes acreditan búsqueda y conteo con documentos bloqueados visibles, motivo accesible, bloqueo con ratón/teclado, conceptos consultables y selección permitida con la opción activa. Se cubren DRAFT/POSTED, otros periodos, vínculos previos compartidos, carga/error/reintento, selección invalidada al refrescar y respuestas tardías de otro contexto sin pérdida de captura.

## FE-006-09 — Rechazo de guardado y regresiones

- [ ] Integrar el error de vínculo nuevo en el editor sin descartar datos y comprobar regresiones del flujo contable.
- **CA:** CA-006-07/20/32/33/34/35.
- **Depende de:** FE-006-08.
- **Hecho cuando:** Vitest y React Testing Library comprueban que un `422` por reutilización muestra el UUID y conserva cuentas, partidas, conceptos, importes y relaciones para corregir; no reenvía ni borra información automáticamente. Pasan regresiones de selección, propuesta, sugerencias y consulta de conceptos, tipos, lint y formato. La disposición real se deja explícitamente pendiente de QA humana.
