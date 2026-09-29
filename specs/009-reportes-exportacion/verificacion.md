# Verificación — SPEC-009

El [estado de trabajo y los criterios](spec.md) se contrastan con el código y las pruebas de backend y frontend. Git conserva las entregas anteriores.

## Entrega actual

Los reportes y exportaciones XLSX están integrados. No hay tareas técnicas abiertas.

La regresión ejecutada el 2026-09-24 en los repositorios actuales pasó: `./vendor/bin/sail artisan test --compact` (88 pruebas, 870 aserciones), `pnpm test` (6 archivos, 26 pruebas), `pnpm lint`, `pnpm typecheck` y `pnpm build`. Las pruebas backend por funcionalidad están en `tests/Feature/Spec009Test.php` del repositorio de backend cuando aplica. Estos resultados acreditan el estado de código comprobado; no sustituyen la revisión visual.

## QA humana pendiente

Consulta y descarga de XML, pólizas y balanza; comparar datos visibles con cada archivo abierto en una herramienta compatible. Registrar aquí fecha, resultado y observaciones. Sólo una aprobación humana registrada permite cambiar el estado a Implementada.
