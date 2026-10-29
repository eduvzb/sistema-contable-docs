# Verificación — SPEC-001

El [estado de trabajo y los criterios](spec.md) se contrastan con el código y las pruebas de backend y frontend. Git conserva las entregas anteriores.

## Entrega actual

### Actualización pendiente: edición de empresa

- [ ] Backend: endpoint de actualización, validaciones y autorización vigente de administrador/contador asignado, con RFC inmutable.
- [ ] Frontend: formulario de edición accesible desde la empresa seleccionada, con errores y estados comprobados.
- [ ] Reemplazo de FIEL: criterio y controles coordinados en [SPEC-012](../012-descarga-masiva-sat/spec.md#ampliación-autorizada-edición-de-empresa-y-reemplazo-de-fiel-para-usuarios-reales); sin implementación ni prueba de producción acreditadas en esta actualización documental.
- No se ejecutaron pruebas de producto ni se modificó código en esta preparación documental.

- [x] La regresión actual del árbol integrado pasa con Laravel Sail: `./vendor/bin/sail artisan test --compact`, 114 pruebas y 1,057 aserciones (2026-10-15; árbol equivalente a backend `2253855`).
- [x] La suite frontend pasa: `pnpm test`, 58 pruebas en 10 archivos; `pnpm typecheck` y `pnpm build` aprobados (árbol equivalente a `23c845a`).
- [x] `pnpm lint` termina sin errores; reporta 94 advertencias en herramientas locales excluidas de Git.
- [ ] `pnpm format:check` global: falla previamente en 87 archivos locales de `.agents`/`.impeccable`; no se considera aprobado ni se modifica ese trabajo ajeno. No hay cambios de código para esta spec.


CA-001-18/19 y el acceso vigente están integrados en backend y frontend. No hay tareas técnicas abiertas.

La regresión ejecutada el 2026-09-24 en los repositorios actuales pasó: `./vendor/bin/sail artisan test --compact` (88 pruebas, 870 aserciones), `pnpm test` (6 archivos, 26 pruebas), `pnpm lint`, `pnpm typecheck` y `pnpm build`. Las pruebas backend por funcionalidad están en `tests/Feature/Spec001Test.php` del repositorio de backend cuando aplica. Estos resultados acreditan el estado de código comprobado; no sustituyen la revisión visual.

## QA humana aprobada

Alta y consulta de empresa: razón social principal, nombre comercial secundario, tipo de persona derivado; entrada y permisos de administrador/contador. Aprobación confirmada el 2026-10-15 por el usuario solicitante en esta sesión; fecha de ejecución y observaciones no especificadas.
