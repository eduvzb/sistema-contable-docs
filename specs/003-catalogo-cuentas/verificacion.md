# Verificación — SPEC-003

## Entrega actual: CA-003-13/14/15

- [x] Sólo administradores consultan, descargan el layout e importan la plantilla global. CSV UTF-8 con encabezado exacto, jerarquía y valores inválidos se rechaza sin reemplazar la versión vigente.
- [x] Cada importación válida activa una versión única; la creación de empresas copia el snapshot vigente bajo un bloqueo común. Activar otra versión y editar una empresa no altera otros catálogos ni versiones anteriores.
- [x] El panel muestra la versión vigente y la guía del layout; descarga el CSV y conserva el archivo tras errores recuperables.
- [x] Sail ejecutado por orquestador: `./vendor/bin/sail exec -T -w /var/www/html/.orchestrator-worktrees/spec003 laravel.test php artisan test --compact` — 119 pruebas y 1,133 aserciones. Selección de plantilla/empresa/catálogo: 34 pruebas y 394 aserciones.
- [x] Frontend: `pnpm --config.verify-deps-before-run=false test` — 65 pruebas en 11 archivos; lint, tipos, build y format:check aprobados. Pint, PHP lint y `git diff --check` aprobados. No cambian dependencias.
- [x] Revisión independiente `audit_001_003`, gpt-6-luna/high: sin hallazgos bloqueantes. Los errores de pruebas iniciales quedaron corregidos antes de estos resultados.
- [x] Backend `134e497eebc0be78e8e06b101319ddf7424b1eb5`, rama `codex/feature/SPEC-003/plantilla-sat-global`, [PR #12](https://github.com/eduvzb/sistema-contable-back/pull/12) hacia main; revisor `alavazarez` solicitado.
- [x] Frontend `ec75d9c7e5620dd20bcf2a660a680f6b4252cf9e`, misma rama, [PR #21](https://github.com/eduvzb/sistema-contable-front/pull/21) hacia main; revisor `alavazarez` solicitado. No hay checks remotos disponibles. Integrar backend antes de frontend.
- [ ] QA humana: comprobar consulta de versión, guía/layout, carga y corrección del archivo en administración. La vigencia del contenido SAT debe comprobarla la persona administradora antes de activarlo. Registrar persona, fecha, resultado y observaciones.

## QA humana del alcance anterior (conservada)

Búsqueda, limpieza, recuento, jerarquía y selección de cuentas operables. Aprobación confirmada el 2026-10-15 por el usuario solicitante en esta sesión; fecha de ejecución y observaciones no especificadas.

La aprobación corresponde al alcance previo; la interacción nueva permanece en QA.
