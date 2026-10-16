# Verificación — SPEC-002

## Entrega actual: CA-002-13/14/15/16

- [x] Encabezado sin los tres accesos duplicados, con acciones de pestaña conservadas; pruebas de workspace aprobadas.
- [x] Franja compacta de periodo, estado y reserva, con autorización y carga conservadas; slot de acción estable comprobado por componente, disposición visual real pendiente.
- [x] Meses identificados por ocupación; se conserva la sincronización existente tras reserva, liberación y conflicto, con pruebas de selector y workspace aprobadas.
- [x] Avisos de acciones del workspace, pólizas, CFDI y exportaciones flotantes, con cierre manual o a los 5 segundos; pruebas de accesibilidad semántica, sucesión, limpieza por empresa y errores de campos aprobadas.
- [x] Pruebas de componentes y comportamiento, formato y lint de archivos modificados, TypeScript y build del frontend.
- [ ] QA visual humana de franja y avisos en móvil y escritorio.

### Evidencia técnica de esta entrega

- Frontend: rama `codex/feat/SPEC-002/header-period-toasts`, commit `6bee152`, publicado en origin. [PR #24 hacia main](https://github.com/eduvzb/sistema-contable-front/pull/24), revisión solicitada a `alavazarez`, colaborador con acceso. No fusionado; no se afirma CI aprobado.
- `pnpm test --reporter=dot`: 107 pruebas aprobadas en 16 archivos; resultado final repetido por el agente coordinador sobre el contenido entregado.
- Agente frontend GPT-6 Luna medium: `pnpm build`, `pnpm typecheck`, ESLint y Prettier `--check` sobre archivos modificados aprobados. `pnpm lint` global sin errores, con 94 advertencias de skills locales; `pnpm format:check` global no aprueba por 87 archivos preexistentes de skills fuera de esta entrega. No se modificaron esos archivos.
- `git diff --check` y `git diff --cached --check`: aprobados antes del commit. Sólo se incluyeron los 15 archivos frontend de la entrega.
- Backend sin cambios. Tareas FE-002-13/14/15/16 retiradas tras acreditar implementación, pruebas y publicación. QA humana pendiente en 320/390 px y escritorio, nombres largos, avisos sucesivos y diálogos abiertos.
- Documentación actualizada localmente; no se publica ni se incluye en el commit frontend, para conservar los cambios documentales previos del usuario.

La evidencia previa que sigue no sustituye las comprobaciones de esta entrega.

## Evidencia previa: mejora de selección y reserva de periodos

- [x] Selector flotante con ejercicio y mes; cambiar de ejercicio no cambia el contexto hasta elegir un mes. Escape devuelve el foco y el clic fuera cierra el panel.
- [x] La franja distingue estado contable y reserva. Las acciones «Tomar para trabajar» y «Liberar reserva» conservan la autorización y los contratos existentes.
- [x] Frontend: 95 pruebas en 14 archivos, TypeScript, build, formato y ESLint de archivos modificados aprobados. Detector Impeccable sin hallazgos.
- [x] Revisión visual local con datos de prueba a 1440, 390 y 320 px: los meses caben en el panel; en 320 px la acción de reserva y la pestaña conservaron sus coordenadas antes y después de tomar la reserva. La vista temporal se retiró.
- [ ] QA humana sobre la vista autenticada completa: comprobar selección, reserva ajena y avisos en condiciones reales. No se pudo acceder con las cuentas públicas de los seeders; esta entrega no afirma esa validación.

## Entrega anterior: CA-002-10/11/12

- [x] Habilitar ejercicio conserva doce meses sin reserva; abrir adquiere inmediatamente la reserva propia y repetir no la duplica. Dos usuarios concurrentes obtienen 201 y 409 respectivamente.
- [x] El dueño o administrador libera sin alterar OPEN/CLOSED; terceros conservan consulta y ven el responsable. La interfaz usa «Disponible», «Abrir periodo» y «Cerrar periodo».
- [x] Respuestas tardías de adquisición o refresco no sustituyen el contexto nuevo; un refresco fallido informa error sin anunciar éxito.
- [x] Sail directo sobre los commits finales: `./vendor/bin/sail exec -T -w /var/www/html/.orchestrator-worktrees/spec002 laravel.test php artisan test --compact tests/Feature/Spec002Test.php tests/Feature/Spec002ConcurrencyTest.php` — 13 pruebas y 113 aserciones, incluidas dos conexiones PostgreSQL reales. La configuración y la base temporal se limpian también si falla su preparación.
- [x] Suite backend completa anterior al ajuste de limpieza: 118 pruebas/1,083 aserciones. Ensayo conjunto final002/003/006: 131 pruebas/1,217 aserciones.
- [x] Frontend final: `pnpm --config.verify-deps-before-run=false test` — 61 pruebas/10 archivos; lint, tipos, format:check, build y diff-check aprobados. Pint/PHP lint/backend diff-check aprobados. No cambian dependencias.
- [x] Revisión independiente `audit_007_009`, gpt-6-luna/high: tres hallazgos P2 corregidos y revalidados (contexto tardío, éxito falso y limpieza de DB de prueba).
- [x] Backend final `0e3dda21657498313caf7981a60ff5384ceaee1f`, rama `codex/feature/SPEC-002/reserva-explicita`, [PR #13](https://github.com/eduvzb/sistema-contable-back/pull/13) hacia main; revisor `alavazarez` solicitado.
- [x] Frontend final `3e5b00a0486f1b21efebbca3cbb721e0234848d8`, misma rama, [PR #22](https://github.com/eduvzb/sistema-contable-front/pull/22) hacia main; revisor `alavazarez` solicitado. Sin checks remotos disponibles. Integrar backend antes de frontend; SPEC-006 añade el enforcement del guardado como entrega dependiente.
- [ ] QA humana: comprobar adquisición, responsable, conflicto y liberación; confirmar que «Cerrar periodo» comunica liberar una reserva y no cierre contable. Registrar persona, fecha, resultado y observaciones.

## QA humana del alcance anterior (conservada)

Cambio de empresa y periodo, búsqueda del selector, conservación de la vista y ausencia de datos de otro contexto. Aprobación confirmada el 2026-10-15 por el usuario solicitante en esta sesión; fecha de ejecución y observaciones no especificadas.

La aprobación corresponde al alcance previo; la interacción nueva permanece en QA.
