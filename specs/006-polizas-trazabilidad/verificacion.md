# Verificación — SPEC-006

La entrega vigente y su estado se consultan en [spec.md](spec.md). Las pruebas, cierres y estados de entrega fechados a continuación son evidencia de su revisión histórica; no acreditan automáticamente criterios añadidos o modificados después.

## Entrega vigente

CA-006-19 revisado y CA-006-20 a CA-006-24 no tienen implementación ni pruebas de esta entrega; dependen de CA-004-11. La prueba de CA-006-19 del 2026-09-14 acredita sólo su versión anterior.

## Evidencia histórica y QA

**Actualización CA-006-19 a CA-006-24 pendiente (2026-09-23):** únicamente se preparó la spec. No se modificó código de producto, no se ejecutaron pruebas de esta actualización y los recorridos de QA descritos siguen pendientes. La evidencia histórica siguiente corresponde a versiones anteriores del editor.

**Evidencia CA-006-19, 2026-09-14:** frontend en la rama `codex/feat/SPEC-006/cfdi-policy-search`, commit `b8d16a679bbd9c931caa50282ea12dd07657f3f3`, publicado en `origin` y entregado en el PR [front #15](https://github.com/eduvzb/sistema-contable-front/pull/15). `pnpm test` pasó con 6 archivos y 25 pruebas; `pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check` aprobaron. Las pruebas del editor cubren búsqueda por UUID, RFC, contraparte, serie y folio sin distinción de mayúsculas o acentos, recuento, estado vacío, vínculos existentes, conservación de selección al filtrar y envío de todos los IDs seleccionados al guardar.

**Evidencia de producto:** implementación backend y frontend realizada el 2026-09-08. `./vendor/bin/sail artisan test --compact` pasó con 42 pruebas y 350 aserciones; la suite incluye 10 pruebas y 58 aserciones focalizadas en SPEC-006, con CFDI sin pólizas, una y varias pólizas entre periodos, partidas/cuentas, pólizas sin CFDI, aislamiento entre empresas y usuario sin acceso. `pnpm lint`, `pnpm typecheck` y `pnpm build` pasaron.

**Evidencia de continuidad 2026-09-08:** `./vendor/bin/sail artisan test --compact tests/Feature/Spec006Test.php` pasó con 15 pruebas y 114 aserciones. Cubre rechazo y rollback de cuenta o CFDI de otra empresa, `404` al consultar/modificar/contabilizar sin autorización, conservación de `created_by`, cambio correcto de `updated_by`, marcas de tiempo, edición balanceada de `POSTED` y serialización exacta de `999999999999.999999` a seis decimales tanto desde póliza como desde detalle fiscal. La regresión completa pasó con 72 pruebas y 650 aserciones.

**Evidencia histórica de la versión de CA-006-14 preparada el 2026-09-10:** el frontend implementó un campo editable `DD/MM/AAAA`, calendario en español limitado al periodo seleccionado, operación por teclado, ayuda contextual del periodo, validación localizada junto al control y conservación del resto de la captura ante una fecha inválida. La fecha seleccionada se transforma al `AAAA-MM-DD` que ya consume el backend; no se modificó el contrato ni la validación autoritativa del backend. Comprobaciones frontend ejecutadas: `pnpm lint`, `pnpm typecheck` y `pnpm build`, todas aprobadas. Implementación: frontend, rama `codex/SPEC-006`, commit `d7287c1d50a9eaf9aa55968f1596aebfa9fda23c` (`SPEC-006: mejora el calendario de pólizas`), remoto `origin`, PR [#3](https://github.com/eduvzb/sistema-contable-front/pull/3), fusionado en `main` mediante el merge commit `80cf438eefdb517c41e27a9d394fbf9202e43ce6`. Backend no fue afectado.

**Cierre técnico 2026-09-12:** CA-006-14 modificado y CA-006-15 a CA-006-18 se implementaron en frontend. El calendario es una capa superpuesta y se retiró el copy permanente; la creación inicia con una partida vacía; `Enter` en un cargo o abono válido prepara y enfoca la siguiente partida sin guardar; y el editor aprovecha el ancho de escritorio. `pnpm test` aprobó 2 archivos y 9 pruebas; `pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check` aprobaron. Implementación: rama `codex/fix/SPEC-006/policy-editor-capture`, commit `c8837791fda157154436073f9a3890fea78a5eb3` (`SPEC-006: mejora la captura de pólizas`), actualizado con `main` en `7947c0044c775cb17050fe8f6b157e92dd85d9ee`, remoto `origin` y PR [front #7](https://github.com/eduvzb/sistema-contable-front/pull/7) abierto. Backend no fue afectado.

**Revisiones de implementación:** backend parte de `868b20eaaa24c387e7e80f97a5798f024a4582e4`; la actualización frontend está en `7947c0044c775cb17050fe8f6b157e92dd85d9ee`, publicada en `origin/codex/fix/SPEC-006/policy-editor-capture` mediante PR [#7](https://github.com/eduvzb/sistema-contable-front/pull/7) abierto. La documentación conserva cambios locales compartidos; su revisión real debe registrarse en `SPEC_REVISION` de ambos consumidores al confirmarla.

La suite cubre DRAFT desbalanceada, rechazo de POSTED desbalanceada, póliza balanceada, ausencia y multiplicidad de XML, cuentas/XML de otra empresa, autorización, auditoría mínima y edición válida de POSTED. La versión anterior de CA-006-14 cuenta con implementación y evidencia técnica frontend; no se ejecutó una comprobación integral de interfaz por navegador como criterio de cierre. Un intento puntual del recorrido existente no alcanzó el editor porque reutilizó un servidor preexistente sin el estado de prueba esperado; se conserva como incidencia de entorno, no como evidencia de producto.

**Cierre técnico:** CA-006-14 modificado y CA-006-15 a CA-006-18 cuentan con implementación y comprobaciones técnicas. La evidencia anterior permanece vigente para contratos, reglas contables y comportamiento no modificado.

La cobertura frontend ejecutada sustituye las pruebas de integración por navegador para esta actualización:

| Criterios | Pruebas de componentes y comportamiento ejecutadas |
|---|---|
| CA-006-14/15 | Renderizar creación y edición; abrir/cerrar el calendario por botón y teclado; comprobar mes/año y días disponibles; seleccionar y escribir fecha; mostrar el error localizado conservando el resto de la captura; verificar que el copy retirado no esté presente. La superposición real y la ausencia de cambios de layout se reservan a QA visual. |
| CA-006-16 | Comprobar que creación inicia con exactamente una partida vacía y que edición presenta únicamente las partidas recibidas, sin agregar otra implícita. |
| CA-006-17 | Simular `Enter` en cargo y abono para los casos válido, inválido y con renglón vacío posterior; comprobar que existe como máximo una nueva partida, que el foco pasa a su cuenta y que no se invocan guardado, contabilización ni API. |
| CA-006-18 | Comprobar a nivel de componente que todos los campos, totales y acciones continúan renderizados y accesibles. La ausencia efectiva de scroll horizontal a 1280 px y la operabilidad responsiva se validan visualmente porque `jsdom` no calcula layout. |
| CA-006-19 | Buscar por UUID, RFC, razón social, serie y folio; comprobar coincidencia sin mayúsculas ni acentos, recuento, estado vacío, etiquetas accesibles, visualización de vínculos existentes, conservación de una selección al filtrar y los IDs completos enviados al guardar. |

No se ejecutó ni se exige Playwright o una prueba integral de interfaz por navegador. QA humana debe validar calendario superpuesto y sin copy, captura por teclado, partida inicial y continuación con `Enter`, ancho sin scroll horizontal en escritorio, límites del periodo, conservación del formulario tras error y la densidad, legibilidad y operabilidad de la lista filtrable de CFDI, tanto al crear como al editar cuando aplique. Su aprobación registrada permitirá marcar la spec como Implementada.

**Evidencia histórica de bloqueo 2026-09-10:** el primer preflight SDD se detuvo antes de crear ramas o modificar backend/frontend. Ambos árboles estaban limpios en `main`; sin embargo, `git ls-remote --heads origin main refs/heads/codex/SPEC-006` no pudo resolver `github.com` en backend ni frontend, y `gh auth status` reportó inválido el token de `eduvzb`. Conforme a `docs/flujo-spec.md`, no se crearon ramas, commits, pushes ni PRs en ese intento. El diagnóstico del código confirmó que el backend ya validaba `entry_date` contra el periodo y que el editor frontend todavía usaba un `<input type="date">`; no se declaró implementación ni evidencia técnica nueva.


## Historial documental

- **2026-09-24:** se migró la documentación a `spec.md`, `plan.md`, tareas por repositorio y `verificacion.md` sin cambiar código del producto ni ejecutar pruebas de producto; el estado vigente permanece en `spec.md`.
- **2026-09-23:** por instrucción explícita del usuario se modifica CA-006-19 y se preparan CA-006-20 a CA-006-24 para la ventana de selección por periodo, la propuesta editable por CFDI, la memoria de cuentas y el reinicio único de datos de prueba. La implementación y las comprobaciones quedan pendientes.

- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar reglas de pólizas.

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-08:** se prepara la implementación con editor tabular: numeración por empresa–periodo–tipo, fecha dentro del periodo, DRAFT sin partidas, POSTED balanceada editable y relaciones CFDI por póliza. Pasa a Lista; la evidencia se registra después de implementar.
- **2026-09-08:** se implementaron pólizas, partidas y relaciones con CFDI, junto con la evidencia automatizada aplicable.
- **2026-09-08:** se cerró el contrato de trazabilidad inversa CFDI → pólizas → partidas → cuentas → periodos; se implementó en el detalle del CFDI con aislamiento por empresa y cobertura automatizada.
- **2026-09-08:** se eliminó el uso de `float` en recursos de importes y totales, y se amplió la cobertura de aislamiento, atomicidad, autorización, auditoría y edición balanceada de pólizas contabilizadas.
- **2026-09-10:** por observación explícita del usuario se preparó CA-006-14 para mejorar el calendario de fecha en nueva póliza y edición. Se reclasificó como Actualización pendiente; no se modificó código ni se registró evidencia de implementación.
- **2026-09-10:** conforme a DP-004, el cierre técnico de CA-006-14 llevará la spec a QA; la validación visual será responsabilidad humana.
- **2026-09-10:** el preflight para implementar CA-006-14 quedó bloqueado por resolución de `github.com` y autenticación inválida de `gh`; no se modificaron backend/frontend ni se alteró el estado de la spec.
- **2026-09-10:** se implementó CA-006-14 en frontend, se aprobaron lint, typecheck y build, y se publicó el PR [#3](https://github.com/eduvzb/sistema-contable-front/pull/3). SPEC-006 pasa a QA; la validación visual humana queda pendiente.
- **2026-09-12:** se verificó que el PR [#3](https://github.com/eduvzb/sistema-contable-front/pull/3) fue fusionado en `main` (`80cf438`); se actualiza únicamente el relevo documental y se conserva pendiente la validación visual humana.
- **2026-09-12:** se prepararon las observaciones posteriores de interfaz: CA-006-14 se modifica para retirar el copy permanente; CA-006-15 a CA-006-18 definen superposición del calendario, partida inicial, continuación con `Enter` y ancho de captura. La spec vuelve a Actualización pendiente; no se modificó código ni se registró evidencia técnica nueva.
- **2026-09-12:** por decisión explícita del usuario, la comprobación automatizada de CA-006-14 a CA-006-18 se prepara como pruebas de componentes y comportamiento con Vitest + React Testing Library en lugar de pruebas de integración por navegador. DT-012 generaliza esta política para el frontend y la validación de layout real permanece en QA humana.
- **2026-09-12:** se implementaron y comprobaron técnicamente CA-006-14 modificado y CA-006-15 a CA-006-18 en frontend. `pnpm test` (2 archivos, 9 pruebas), lint, typecheck, build y `git diff --check` aprobaron; se publicó el PR [front #7](https://github.com/eduvzb/sistema-contable-front/pull/7). La spec pasa a QA y queda pendiente exclusivamente la validación visual humana.
- **2026-09-14:** por instrucción explícita del usuario se prepara CA-006-19 para sustituir el selector múltiple de CFDI por búsqueda local y casillas. No modifica contratos, autorización ni reglas contables; la spec pasa a Actualización pendiente hasta registrar el cierre técnico de frontend.
- **2026-09-14:** se implementó y comprobó técnicamente CA-006-19 en frontend. `pnpm test` (6 archivos, 25 pruebas), lint, typecheck, build y `git diff --check` aprobaron; se publicó el PR [front #15](https://github.com/eduvzb/sistema-contable-front/pull/15). La spec vuelve a QA y queda pendiente exclusivamente la validación visual humana de la lista filtrable.
