# Verificación — SPEC-002

## Entrega actual: CA-002-10/11/12

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
