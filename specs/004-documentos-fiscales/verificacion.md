# Verificación — SPEC-004

La entrega vigente y su estado se consultan en [spec.md](spec.md). Las pruebas, cierres y estados de entrega fechados a continuación son evidencia de su revisión histórica; no acreditan automáticamente criterios añadidos o modificados después.

## Entrega vigente

CA-004-11 aún no tiene implementación ni prueba de extracción y consulta del desglose fiscal. La evidencia anterior de importación no acredita ese criterio.

## Evidencia histórica y QA

**Actualización CA-004-11 pendiente (2026-09-23):** únicamente se preparó la spec. No se modificó código, no se ejecutaron pruebas de esta actualización y no se ha comprobado la extracción detallada de impuestos y descuentos.

**Evidencia de producto:** implementación backend y frontend realizada el 2026-09-08. `./vendor/bin/sail artisan test --compact` pasó con 31 pruebas y 263 aserciones; SPEC-004 cubre lote mixto, UUID duplicado, RFC ajeno, filtro por periodo, aislamiento, descarga autorizada e indicador contabilizado derivado. `pnpm lint`, `pnpm typecheck` y `pnpm build` pasaron en frontend.

**Evidencia de continuidad 2026-09-08:** el detalle de la bandeja consulta `GET /api/companies/{companyId}/fiscal-documents/{fiscalDocumentId}` y presenta los campos fiscales del contrato, sin recalcular importes. La prueba `Spec004Test::test_document_detail_exposes_the_complete_fiscal_contract` verifica el contrato completo; la prueba focalizada pasó con 4 pruebas y 41 aserciones y la suite backend completa pasó con 36 pruebas y 321 aserciones. En frontend, `pnpm lint`, `pnpm exec tsc --noEmit` y `pnpm run build` pasaron.

**Continuidad de contexto 2026-09-08:** la bandeja ya no emite consultas sin `period_id`: sólo se monta después de validar explícitamente el periodo contra la empresa y limpia documentos/detalle al perderlo. `pnpm lint`, `pnpm build` y `pnpm typecheck` pasan.

**Revisiones de implementación:** backend `23ddf6dd05ea08472fa48e7134beea0953f40377` ([PR #1](https://github.com/eduvzb/sistema-contable-back/pull/1), fusionado); frontend `4b43488718611e0b9e5088c2f1a7acacc6e3a24c` ([PR #2](https://github.com/eduvzb/sistema-contable-front/pull/2), fusionado). Las revisiones anteriores permanecen en la evidencia histórica de producto.

**Evidencia técnica de CA-004-09/10 — 2026-09-10:** CA-004-09 quedó cubierto en `src/components/fiscal-document-inbox.tsx`: el valor nativo del selector se limpia tras una respuesta completa y al cerrar/reabrir la sesión; la bandeja protege la reconciliación contra respuestas obsoletas y muestra documentos importados fuera del periodo o filtros visibles. CA-004-10 quedó cubierto por `Spec004Test::test_mixed_batch_reports_each_duplicate_once_and_reconciles_the_new_document`: el lote informa un duplicado y una incorporación, conserva exactamente dos documentos y ambos aparecen en la consulta autoritativa del periodo. `./vendor/bin/sail artisan test --compact tests/Feature/Spec004Test.php` pasó con 5 pruebas y 52 aserciones; la suite completa pasó con 73 pruebas y 661 aserciones; `vendor/bin/pint --dirty --format agent`, `pnpm lint`, `pnpm typecheck` y `pnpm build` pasaron.

**Evidencia técnica de DT-013 — 2026-09-14:** `Spec004Test::test_authorized_user_imports_a_batch_partially_without_persisting_the_original` comprueba que una importación persiste sus datos extraídos con `original_path = null` y que la ruta histórica `/original` responde `404`. `Spec005Test` comprueba la misma condición para la descarga simulada; `Spec007Test` y `CompleteFlowSeederTest` confirman continuidad PPD y datos demo sin archivos. `./vendor/bin/sail artisan test --compact tests/Feature/Spec004Test.php tests/Feature/Spec005Test.php tests/Feature/Spec007Test.php tests/Feature/CompleteFlowSeederTest.php` pasó con 19 pruebas y 170 aserciones; la suite completa pasó con 86 pruebas y 846 aserciones. `vendor/bin/pint --dirty --format agent` y `git diff --check` pasaron. Backend: rama `codex/refactor/SPEC-004/no-durable-xml`, commit [`a7a5aaa`](https://github.com/eduvzb/sistema-contable-back/commit/a7a5aaafd667ee506d18b8dbf79539d3c82913b3), [PR #6](https://github.com/eduvzb/sistema-contable-back/pull/6) abierto.

No se ejecutó una comprobación integral de interfaz por navegador, conforme a DP-004. QA humana debe recorrer la selección limpia, el resultado mixto, la bandeja reconciliada, los mensajes de periodo/filtros y la disponibilidad coherente al relacionar el CFDI en una póliza.

**Incidencia histórica documentada 2026-09-10:** en una prueba manual, un lote con un CFDI previamente registrado y otro nuevo informó un rechazo y una incorporación; el nuevo no apareció en la bandeja, aunque sí estaba disponible al crear una póliza y un nuevo intento lo reconoció como duplicado para el RFC. Esto evidenció una divergencia de presentación o reconciliación, no autorizó duplicar el registro ni cambiar BR-010. La regresión quedó corregida y comprobada en la evidencia de cierre técnico anterior.

**QA humana:** pendiente. Validar visualmente selección limpia, resultado del lote, bandeja y disponibilidad coherente al relacionar el CFDI; sólo la aprobación humana registrada permite marcar la spec Implementada.


## Historial documental

- **2026-09-24:** se migró la documentación a `spec.md`, `plan.md`, tareas por repositorio y `verificacion.md` sin cambiar código del producto ni ejecutar pruebas de producto; el estado vigente permanece en `spec.md`.
- **2026-09-23:** por instrucción explícita del usuario se prepara CA-004-11 para conservar datos fiscales estructurados desde la primera importación, sin conservar el XML original. La implementación y su comprobación quedan pendientes.

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
