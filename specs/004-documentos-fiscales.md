# SPEC-004 — Documentos fiscales

**Estado:** Actualización pendiente
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md)

## Propósito y alcance

Incorporar XML manualmente, de uno en uno o en lote; extraer y conservar únicamente datos fiscales normalizados, detectar duplicados y consultar los documentos de la empresa y periodo. Mostrar emitidos/recibidos e información fiscal extraída, distinguiendo PUE/PPD.

Incluye la bandeja de documentos y su situación contable derivada de pólizas. No incluye SAT real, tratamiento de cancelaciones/sustituciones, nómina ni automatización fiscal avanzada.

## Fuentes

- [Alcance §6](../docs/planeacion/003%20-%20MVP-Scope.md#6-importaci%C3%B3n-y-obtenci%C3%B3n-de-xml), [Alcance §7](../docs/planeacion/003%20-%20MVP-Scope.md#7-consulta-de-documentos-fiscales), [Alcance §14](../docs/planeacion/003%20-%20MVP-Scope.md#14-pue), [Alcance §15](../docs/planeacion/003%20-%20MVP-Scope.md#15-ppd-y-complementos-de-pago) (importación, consulta y distinción PUE/PPD).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-010](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#12-br-010--el-mismo-cfdi-no-debe-importarse-dos-veces), [BR-011](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#13-br-011--el-xml-original-no-se-conserva), [BR-012](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#14-br-012--pue-y-ppd-se-tratan-como-escenarios-diferentes); BR-010 es SUPUESTO MVP, las demás están confirmadas en su alcance.
- [AC-015](../docs/planeacion/004%20-%20Escenarios%20contables.md#17-escenario-ac-015--documento-duplicado) (duplicado por empresa, SUPUESTO MVP); [OQ-003](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#5-oq-003--momento-en-que-un-cfdi-se-considera-contabilizado), [OQ-009](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#11-oq-009--estados-de-fiscaldocument), [OQ-019](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#21-oq-019--moneda-extranjera) (estado derivado provisional y moneda avanzada posterior).
- [Análisis §33: versiones de CFDI pendientes](../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#33-preguntas-abiertas).

## Contexto de ejecución

**Modo actual:** Actualización pendiente. Esta entrega modifica CA-004-01 y el contrato de recuperación: los XML nuevos se procesan sin almacenamiento durable y la descarga del original deja de existir. Trabajar la persistencia, migración y pruebas backend; no requiere cambio interactivo de frontend porque éste no consume la descarga.

**Paquete funcional:** esta spec contiene el alcance autoritativo de importación, conservación, duplicados, consulta, filtros, estados, contratos y criterios. Consultar SPEC-001 para autorización y SPEC-002 para contexto explícito; consultar SPEC-006 sólo para el contrato de relación ya definido.

**Fuentes consolidadas:** las fuentes enlazadas arriba, los supuestos expresamente etiquetados y las decisiones/contratos de esta spec ya fueron consolidados para esta actualización. No recargar Planeación durante la ejecución normal.

**Reabrir fuentes cuando:** cambie el contrato de documentos o una dependencia, un supuesto deje de ser válido, aparezca contradicción, la fecha/estado fiscal pendiente afecte el criterio trabajado o el usuario solicite nuevo comportamiento.

## Comportamiento y criterios de aceptación

Tras seleccionar el contexto, el usuario operativo carga XML, revisa el resultado y localiza documentos. El administrador accede a cualquier empresa y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. Se extraen UUID, RFC emisor/receptor, fecha, serie, folio, subtotal, impuestos, total, método/forma de pago, moneda y tipo de comprobante según alcance §7. Se conservan datos de moneda/tipo de cambio cuando existan, sin cálculo cambiario avanzado.

La importación es responsable de la incorporación que reutiliza SPEC-005. El indicador «contabilizado» se deriva de al menos una póliza POSTED (OQ-003); no implica liquidación. Ese indicador consume la relación definida en SPEC-006 y se completa al integrar ambas funcionalidades.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-004-01 | Se carga un XML válido y admitido para la empresa. | Queda disponible con sus datos extraídos; el XML original se descarta y no puede descargarse desde el sistema. |
| CA-004-02 | Se carga un lote de XML válidos, admitidos y no duplicados. | Los documentos quedan consultables; el usuario conoce el resultado de incorporación. |
| CA-004-03 | Se vuelve a cargar un CFDI cuyo UUID ya existe en la misma empresa. | Se informa el duplicado y no se crea otro documento equivalente (BR-010/AC-015, supuesto MVP). |
| CA-004-04 | Se consulta la bandeja dentro del contexto empresa/periodo. | Se pueden localizar documentos y distinguir emitidos/recibidos, PUE/PPD y los campos del alcance §7; la fecha de filtrado se debe concretar. |
| CA-004-05 | Se consulta un documento relacionado únicamente con pólizas DRAFT y luego con al menos una POSTED. | Se deriva «contabilizado» únicamente en el segundo caso, según OQ-003; no se afirma que esté liquidado. |
| CA-004-06 | Se intenta consultar documentos de una empresa no asignada. | No se exponen datos de esa empresa. |
| CA-004-07 | Un archivo no puede incorporarse según las validaciones acordadas. | El usuario identifica el problema por archivo y no se presenta como importado correctamente; los demás archivos válidos del lote sí pueden incorporarse conforme a la política parcial. |
| CA-004-08 | El XML contiene moneda y tipo de cambio. | Se conservan los datos existentes; no se ejecuta lógica contable avanzada de moneda extranjera. |
| CA-004-09 | Termina un intento de importación, incluido un lote con archivos importados y rechazados. | El resultado por archivo permanece visible para revisión, pero la selección nativa de archivos queda vacía y permite iniciar otro intento —incluso seleccionando nuevamente el mismo archivo— sin conservar adjuntos anteriores. Al cerrar y reabrir el diálogo inicia una sesión limpia. |
| CA-004-10 | Ya existe un CFDI y se vuelve a importar junto con otro nuevo de la misma empresa. | El existente se informa como duplicado una sola vez, el nuevo se incorpora una sola vez y la bandeja se reconcilia con la consulta autoritativa. Si el nuevo corresponde al periodo y filtros visibles queda localizable sin recargar manualmente; si queda fuera, el resultado explica qué periodo o filtro impide verlo. Crear una póliza y reintentar la importación reflejan la misma existencia del documento. |

## Decisiones cerradas

- Se admiten exclusivamente XML CFDI 4.0 de tipo `I`, `E` y `P`. El RFC de la empresa debe coincidir con emisor o receptor; se clasifica como emitido cuando coincide el emisor y como recibido cuando coincide el receptor.
- Los XML nuevos se procesan desde el temporal de carga y se descartan después de extraer y validar sus datos; no se conservan como archivo o BLOB y no existe descarga del original. Los archivos históricos permanecen sin acceso desde el producto y sin purga automática.
- La bandeja del contexto filtra por mes y ejercicio de la fecha de emisión. Los documentos se pueden relacionar con pólizas de otros periodos de la misma empresa.
- Los lotes se procesan por archivo: los válidos se incorporan y cada archivo inválido o duplicado se devuelve con su error. El UUID es único por empresa.
- Después de una respuesta completa del lote se limpia el control de archivos, no el resultado que el usuario todavía está revisando. Cerrar el diálogo descarta resultado, errores y selección de esa sesión.
- La confirmación de importación y la bandeja no pueden divergir silenciosamente. Tras un lote se vuelve a consultar el periodo activo; los documentos importados que no pertenezcan al periodo o queden ocultos por filtros/paginación se identifican en el resultado, sin reclasificarlos como rechazados ni alterar su fecha fiscal.
- Subtotal, impuestos, total y tipo de cambio se conservan con seis decimales y se representan por API como texto. No se calcula conversión monetaria.

## Pendientes y decisiones

- **Resuelto para esta entrega:** versiones/tipos, pertenencia al RFC, fecha de filtro, importación parcial, descarte del original y representación decimal.
- **Supuestos para validar:** duplicados por UUID dentro de la empresa (BR-010/AC-015); «contabilizado» derivado de POSTED y distinto de «liquidado» (OQ-003). No crear una máquina de estados compleja (OQ-009).
- **Posterior:** excepciones por sustitución/corrección, consulta SAT de cancelaciones y conversión contable de moneda. El mismo UUID en empresas distintas no se decide como duplicado global.

## Plan técnico y contratos

- Backend: extracción en la solicitud y consulta aislada por empresa; persiste sólo datos normalizados, expone incorporación parcial, listado por periodo y el indicador derivado de pólizas `POSTED`. `original_path` permanece opcional sólo para inventariar archivos históricos; no se expone mediante API.
- Contrato de consulta: `GET /api/companies/{companyId}/fiscal-documents?period_id={periodId}` entrega la bandeja filtrada por mes y ejercicio de `issued_at`; cada elemento conserva el resumen y los campos fiscales extraídos. `GET /api/companies/{companyId}/fiscal-documents/{fiscalDocumentId}` entrega el mismo documento completo para consultar UUID, RFC emisor/receptor, fecha, serie, folio, subtotal, impuestos, total, método/forma de pago, moneda, tipo de cambio, tipo de comprobante, dirección y `accounted`.
- Frontend: carga múltiple, resultado por archivo, limpieza real del selector después de cada respuesta, reconciliación de la bandeja vigente y explicación de documentos importados fuera de la vista actual. Conserva filtros y página compatibles conforme a SPEC-002, con detalle seleccionable del CFDI, sin añadir descarga SAT ni automatizaciones fiscales. El detalle presenta los campos del contrato existente, sin recalcular importes ni convertir moneda.
- Ejemplos de archivos compatibles para desarrollo: [ejemplos de XML CFDI](../docs/ejemplos/README.md).
- La política de lote se cerró como parcial. No requiere workers ni infraestructura adicional (DT-005).

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). El contrato de consulta de esta brecha queda cerrado; cualquier ampliación posterior debe actualizar esta spec antes de modificar consumidores.

## Verificación

**Evidencia de producto:** implementación backend y frontend realizada el 2026-09-08. `./vendor/bin/sail artisan test --compact` pasó con 31 pruebas y 263 aserciones; SPEC-004 cubre lote mixto, UUID duplicado, RFC ajeno, filtro por periodo, aislamiento, descarga autorizada e indicador contabilizado derivado. `pnpm lint`, `pnpm typecheck` y `pnpm build` pasaron en frontend.

**Evidencia de continuidad 2026-09-08:** el detalle de la bandeja consulta `GET /api/companies/{companyId}/fiscal-documents/{fiscalDocumentId}` y presenta los campos fiscales del contrato, sin recalcular importes. La prueba `Spec004Test::test_document_detail_exposes_the_complete_fiscal_contract` verifica el contrato completo; la prueba focalizada pasó con 4 pruebas y 41 aserciones y la suite backend completa pasó con 36 pruebas y 321 aserciones. En frontend, `pnpm lint`, `pnpm exec tsc --noEmit` y `pnpm run build` pasaron.

**Continuidad de contexto 2026-09-08:** la bandeja ya no emite consultas sin `period_id`: sólo se monta después de validar explícitamente el periodo contra la empresa y limpia documentos/detalle al perderlo. `pnpm lint`, `pnpm build` y `pnpm typecheck` pasan.

**Revisiones de implementación:** backend `23ddf6dd05ea08472fa48e7134beea0953f40377` ([PR #1](https://github.com/eduvzb/sistema-contable-back/pull/1), fusionado); frontend `4b43488718611e0b9e5088c2f1a7acacc6e3a24c` ([PR #2](https://github.com/eduvzb/sistema-contable-front/pull/2), fusionado). Las revisiones anteriores permanecen en la evidencia histórica de producto.

**Evidencia técnica de CA-004-09/10 — 2026-09-10:** CA-004-09 quedó cubierto en `src/components/fiscal-document-inbox.tsx`: el valor nativo del selector se limpia tras una respuesta completa y al cerrar/reabrir la sesión; la bandeja protege la reconciliación contra respuestas obsoletas y muestra documentos importados fuera del periodo o filtros visibles. CA-004-10 quedó cubierto por `Spec004Test::test_mixed_batch_reports_each_duplicate_once_and_reconciles_the_new_document`: el lote informa un duplicado y una incorporación, conserva exactamente dos documentos y ambos aparecen en la consulta autoritativa del periodo. `./vendor/bin/sail artisan test --compact tests/Feature/Spec004Test.php` pasó con 5 pruebas y 52 aserciones; la suite completa pasó con 73 pruebas y 661 aserciones; `vendor/bin/pint --dirty --format agent`, `pnpm lint`, `pnpm typecheck` y `pnpm build` pasaron.

**Evidencia técnica de DT-013 — 2026-09-14:** `Spec004Test::test_authorized_user_imports_a_batch_partially_without_persisting_the_original` comprueba que una importación persiste sus datos extraídos con `original_path = null` y que la ruta histórica `/original` responde `404`. `Spec005Test` comprueba la misma condición para la descarga simulada; `Spec007Test` y `CompleteFlowSeederTest` confirman continuidad PPD y datos demo sin archivos. `./vendor/bin/sail artisan test --compact tests/Feature/Spec004Test.php tests/Feature/Spec005Test.php tests/Feature/Spec007Test.php tests/Feature/CompleteFlowSeederTest.php` pasó con 19 pruebas y 170 aserciones; la suite completa pasó con 86 pruebas y 846 aserciones. `vendor/bin/pint --dirty --format agent` y `git diff --check` pasaron. Backend: rama `codex/refactor/SPEC-004/no-durable-xml`, commit [`a7a5aaa`](https://github.com/eduvzb/sistema-contable-back/commit/a7a5aaafd667ee506d18b8dbf79539d3c82913b3), [PR #6](https://github.com/eduvzb/sistema-contable-back/pull/6) abierto.

No se ejecutó una comprobación integral de interfaz por navegador, conforme a DP-004. QA humana debe recorrer la selección limpia, el resultado mixto, la bandeja reconciliada, los mensajes de periodo/filtros y la disponibilidad coherente al relacionar el CFDI en una póliza.

**Incidencia histórica documentada 2026-09-10:** en una prueba manual, un lote con un CFDI previamente registrado y otro nuevo informó un rechazo y una incorporación; el nuevo no apareció en la bandeja, aunque sí estaba disponible al crear una póliza y un nuevo intento lo reconoció como duplicado para el RFC. Esto evidenció una divergencia de presentación o reconciliación, no autorizó duplicar el registro ni cambiar BR-010. La regresión quedó corregida y comprobada en la evidencia de cierre técnico anterior.

**QA humana:** pendiente. Validar visualmente selección limpia, resultado del lote, bandeja y disponibilidad coherente al relacionar el CFDI; sólo la aprobación humana registrada permite marcar la spec Implementada.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance de documentos.

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-08:** se prepara la implementación conjunta con SPEC-006: CFDI 4.0 `I`/`E`/`P`, carga parcial, original privado, filtro por emisión y decimales de seis posiciones. Pasa a Lista; la evidencia se registra después de implementar.
- **2026-09-08:** se implementaron contrato API, almacenamiento privado, lote parcial y bandeja de CFDI; se registró la evidencia automatizada aplicable.
- **2026-09-08:** se concretó la consulta de detalle del CFDI en la bandeja mediante el contrato `GET` existente y se añadió cobertura automatizada de sus campos fiscales.
- **2026-09-08:** se eliminó la variante de carga de bandeja sin periodo y se condicionó su montaje a un contexto empresa/periodo validado por backend.
- **2026-09-10:** por observaciones explícitas del usuario se prepararon CA-004-09/10: limpieza del selector de XML y regresión del lote mixto duplicado+nuevo con reconciliación visible. Se reclasificó como Actualización pendiente y se registró la incidencia observada sin modificar código ni atribuirle todavía una causa.
- **2026-09-10:** conforme a DP-004, el cierre técnico de CA-004-09/10 llevará la spec a QA; la validación visual será responsabilidad humana.
- **2026-09-10:** se implementaron y comprobaron técnicamente CA-004-09/10; se publicaron y fusionaron backend `23ddf6d` en [PR #1](https://github.com/eduvzb/sistema-contable-back/pull/1) y frontend `4b43488` en [PR #2](https://github.com/eduvzb/sistema-contable-front/pull/2). La spec pasa a QA; la aprobación visual humana sigue pendiente.
- **2026-09-14:** por instrucción explícita del usuario y DT-013, CA-004-01 cambia: los XML nuevos no se almacenan de forma durable ni se descargan. Los archivos históricos se conservan sin exposición ni purga. La spec vuelve a Actualización pendiente hasta registrar la evidencia técnica de backend.
