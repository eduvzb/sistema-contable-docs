# Verificación — SPEC-004

El [estado de trabajo y los criterios](spec.md) se contrastan con el código y las pruebas de backend y frontend. Git conserva las entregas anteriores.

## Entrega actual

CA-004-11 y la importación/consulta fiscal están integrados. No hay tareas técnicas abiertas.

La regresión ejecutada el 2026-09-24 en los repositorios actuales pasó: `./vendor/bin/sail artisan test --compact` (88 pruebas, 870 aserciones), `pnpm test` (6 archivos, 26 pruebas), `pnpm lint`, `pnpm typecheck` y `pnpm build`. Las pruebas backend por funcionalidad están en `tests/Feature/Spec004Test.php` del repositorio de backend cuando aplica. Estos resultados acreditan el estado de código comprobado; no sustituyen la revisión visual.

## QA humana pendiente

Lote mixto, mensajes por archivo, bandeja reconciliada y desglose de descuento e impuestos en el detalle. Registrar aquí fecha, resultado y observaciones. Sólo una aprobación humana registrada permite cambiar el estado a Implementada.
