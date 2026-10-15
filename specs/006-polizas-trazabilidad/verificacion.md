# Verificación — SPEC-006

## Entrega actual

CA-006-07/20 revisados y CA-006-30 a CA-006-35: reutilización configurable de CFDI. Preparación documental del 2026-10-14; no se ha implementado ni ejecutado pruebas de esta entrega. Estado: Actualización pendiente.

## Validación técnica pendiente

- [ ] CA-006-30: opción global persistente, inicialmente desactivada, modificable solo por administrador, con validación y errores de guardado.
- [ ] CA-006-20/31/35: CFDI usados visibles en búsqueda, selección bloqueada con motivo accesible, consulta de conceptos y vínculos operable; carga, error y reintento sin habilitar vínculos por suposición.
- [ ] CA-006-32: servidor rechaza vínculos nuevos con UUID y sin guardado parcial, incluso con petición manipulada o pantalla desactualizada.
- [ ] CA-006-07/33: edición conserva relaciones anteriores compartidas y de otros periodos; retirar y guardar un vínculo cambia su tratamiento en una incorporación posterior.
- [ ] CA-006-34: ambos valores de la opción funcionan, la desactivación no elimina relaciones y se consulta el valor vigente al guardar.
- [ ] CA-006-32/34: dos transacciones entre periodos no reutilizan el mismo CFDI con la opción desactivada; el cambio global se serializa con el guardado, probado en un motor con bloqueos reales.
- [ ] CA-006-32/35: errores y respuestas obsoletas conservan la captura y no sustituyen el contexto actual.
- [ ] Regresiones backend/frontend, pruebas de componentes, tipos, lint y formato de los cambios.
- [ ] Cierre técnico y publicación de repositorios afectados conforme al flujo, solo cuando se autorice la implementación y entrega.

## QA humana pendiente

- [ ] Claridad del alcance global y del valor guardado en Configuración.
- [ ] Visibilidad de «Ya usado en otra póliza» y distinción entre un documento usado y uno contabilizado.
- [ ] Operación del selector, vínculos anteriores y conceptos con teclado y en anchos estrechos.
- [ ] Registrar persona, fecha, resultado y observaciones; no hay aprobación de esta entrega.

## Contraste de partida y límite ajeno

Se revisaron `AccountingPolicyController`, `FiscalDocumentController`, `FiscalDocumentResource`, las rutas de API, el área administrativa y el editor con sus pruebas de selección. La reutilización sigue permitida y no hay endpoint global de configuración. `accounted` solo refleja vínculos POSTED; `policy_links` también incluye borradores. Estas lecturas no acreditan los nuevos criterios.

Se conserva la observación ajena previa: CA-006-19/20 describen una tabla con filtros, mientras el código consultado presenta una lista con búsqueda. Esta entrega no reconstruye el selector ni acredita el cumplimiento de esos filtros.

La evidencia de la entrega anterior de conceptos permanece en Git; su QA humana no estaba aprobada y no queda aprobada por esta preparación. No se trasladan checks de aquella entrega como evidencia de la actual.

## Validación documental

- `python3 scripts/spec_index.py --write`: índice actualizado; 9 specs y sus enlaces locales validados.
- `python3 scripts/spec_index.py --check`: correcto.
- `git diff --check`: sin errores de espacios.
- Revisión de los cinco documentos y del diff: criterios enlazados con contratos y tareas, sin decisiones bloqueantes; se conservan los IDs y criterios previos salvo CA-006-07/20, ajustados al alcance confirmado.

Esta validación es documental; no sustituye pruebas del producto ni QA humana.
