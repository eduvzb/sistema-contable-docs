# Verificación — SPEC-006

## Entrega actual

CA-006-07/20 revisados y CA-006-30 a CA-006-35: reutilización configurable de CFDI. Preparación documental del 2026-10-14; no se ha implementado ni ejecutado pruebas de esta entrega. Estado: Actualización pendiente.

Nuevo requerimiento diferenciado: CA-006-36 a CA-006-39, concepto de partidas con componente, serie-folio y emisor al generar desde XML en creación y edición. Se añade a la misma spec sin reemplazar la entrega de reutilización; su implementación y sus pruebas también están pendientes.

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

## Nuevo requerimiento: conceptos de partidas — pendiente

### Comprobación técnica

- [ ] CA-006-36: vista previa y editor muestran componente más identificación del emisor correcto en cada partida de uno o varios XML, al crear y editar.
- [ ] CA-006-37: datos ausentes o blancos usan los sustitutos acordados sin separadores sobrantes; se conservan ceros iniciales.
- [ ] CA-006-38: conceptos editables y persistidos sin recálculo al guardar o abrir; selección sin «Continuar» y partidas manuales sin cambios. Importes, cuentas, referencias y sugerencias sin regresiones.
- [ ] CA-006-39: propuesta completa sin truncar; 255 caracteres válidos, rechazo de 256 en creación/edición, error junto a la partida y corrección sin pérdida de captura ni escritura parcial.
- [ ] Pruebas backend y Vitest/React Testing Library, regresiones, tipos, lint y formato ejecutados y registrados; cierre técnico conforme al flujo cuando se autorice.

### QA humana

- [ ] Lectura y edición de conceptos largos, identificación de cada XML y error de longitud con teclado y en los anchos vigentes.
- [ ] Registrar persona, fecha, resultado y observaciones; no hay aprobación para este nuevo requerimiento.

### Contraste de partida

Se revisaron `AccountingPolicyEntryPreviewService`, `StoreAccountingPolicyRequest`, la ruta de vista previa, `tests/Feature/Spec006Test.php`, el servicio de API y `accounting-policy-editor.tsx` con sus pruebas. La propuesta actual usa solo la etiqueta del componente; el editor la copia y el guardado admite hasta 255 caracteres. No se ejecutaron pruebas del producto ni se modificó código por esta preparación documental.

## Contraste de partida y límite ajeno

Se revisaron `AccountingPolicyController`, `FiscalDocumentController`, `FiscalDocumentResource`, las rutas de API, el área administrativa y el editor con sus pruebas de selección. La reutilización sigue permitida y no hay endpoint global de configuración. `accounted` solo refleja vínculos POSTED; `policy_links` también incluye borradores. Estas lecturas no acreditan los nuevos criterios.

Se conserva la observación ajena previa: CA-006-19/20 describen una tabla con filtros, mientras el código consultado presenta una lista con búsqueda. Esta entrega no reconstruye el selector ni acredita el cumplimiento de esos filtros.

La evidencia de la entrega anterior de conceptos permanece en Git; su QA humana no estaba aprobada y no queda aprobada por esta preparación. No se trasladan checks de aquella entrega como evidencia de la actual.

## Validación documental previa: reutilización de CFDI

- `python3 scripts/spec_index.py --write`: índice actualizado; 9 specs y sus enlaces locales validados.
- `python3 scripts/spec_index.py --check`: correcto.
- `git diff --check`: sin errores de espacios.
- Revisión de los cinco documentos y del diff: criterios enlazados con contratos y tareas, sin decisiones bloqueantes; se conservan los IDs y criterios previos salvo CA-006-07/20, ajustados al alcance confirmado.

Esta validación es documental; no sustituye pruebas del producto ni QA humana.

## Validación documental del nuevo requerimiento

- `python3 scripts/spec_index.py --check`: correcto; 9 specs y enlaces locales validados.
- `git diff --check`: sin errores de espacios.
- Revisión de los cinco documentos y del diff: CA-006-36 a CA-006-39 cubiertos por plan y tareas BE/FE-006-10/11, sin ciclos ni bloqueantes. Se conserva el trabajo previo de reutilización y sus IDs.
- No cambian filas del índice ni el estado; no se requiere regenerarlo. Estado: Actualización pendiente, con preparación documental completa y ejecución técnica pendiente.

La validación es solo documental; no acredita implementación, pruebas del producto ni QA humana.
