# Tareas de frontend — SPEC-006

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

Las tareas FE-006-07 a FE-006-09 corresponden a reutilización de CFDI; el nuevo requerimiento de conceptos se prepara por separado en FE-006-10/11.

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

## FE-006-10 — Integración de conceptos propuestos

- [ ] Actualizar las pruebas y los datos simulados del editor para consumir el concepto completo de la vista previa sin recomponerlo.
- **CA:** CA-006-36/37/38.
- **Depende de:** [BE-006-10](tasks-backend.md#be-006-10--concepto-propuesto-con-identificación-del-xml); no depende de las tareas de reutilización.
- **Hecho cuando:** Vitest y React Testing Library verifican creación y edición con varios XML, texto recibido sin mezcla ni duplicación, edición manual y payload enviado. Abrir una póliza y seleccionar XML sin «Continuar» no cambia conceptos existentes; las partidas manuales permanecen intactas. Pasan las regresiones de generación, sugerencias y consulta de conceptos.

## FE-006-11 — Corrección de conceptos largos

- [ ] Asociar a la partida el error de longitud del servidor y comprobar la corrección sin pérdida de datos, ajustando la presentación solo si falta.
- **CA:** CA-006-38/39.
- **Depende de:** FE-006-10 y [BE-006-11](tasks-backend.md#be-006-11--persistencia-y-límite-del-concepto).
- **Hecho cuando:** pruebas de componentes verifican propuesta larga sin truncar, rechazo `422` visible junto a su partida, conservación del resto de la captura y reenvío del concepto corregido al crear y editar. Pasan tipos, lint y formato; la legibilidad y el layout real quedan pendientes de QA humana.
