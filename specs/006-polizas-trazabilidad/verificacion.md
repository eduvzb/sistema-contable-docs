# Verificación — SPEC-006

El [estado de trabajo y los criterios](spec.md) se contrastan con el código y las pruebas de backend y frontend. Git conserva las entregas anteriores.

## Entrega actual

La implementación de CA-006-19 revisado y CA-006-20 a CA-006-24 quedó completada en los repositorios backend y frontend; las tareas técnicas BE-006-01/02/03 y FE-006-01/02/03 están cerradas. La tarea BE-006-04 permanece abierta: aunque se autoriza un reinicio único de datos de prueba, falta identificar el entorno/base de datos y los registros exactos. No se ejecutó respaldo ni reinicio.

### Backend

- `vendor/bin/pint --dirty --format agent` — pasó; aplicó formato a la clase de propuesta.
- `DB_HOST=127.0.0.1 DB_PORT=54329 DB_USERNAME=sail DB_PASSWORD=password vendor/bin/phpunit tests/Feature/Spec006Test.php` — pasó: 25 pruebas, 209 aserciones.
- `APP_KEY=base64:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA= DB_HOST=127.0.0.1 DB_PORT=54329 DB_USERNAME=sail DB_PASSWORD=password vendor/bin/phpunit tests/Feature` — pasó: 94 pruebas, 925 aserciones.
- PR backend: [#8](https://github.com/eduvzb/sistema-contable-back/pull/8), rama publicada hacia `main`; revisión solicitada a `alavazarez` (pendiente).

### Frontend

- `pnpm test` — pasó: 6 archivos, 27 pruebas.
- `pnpm lint`, `pnpm typecheck`, `pnpm build` y `pnpm format:check` — pasaron.
- PR frontend: [#17](https://github.com/eduvzb/sistema-contable-front/pull/17), rama publicada hacia `main`; revisión solicitada a `alavazarez` (pendiente).

## QA humana pendiente

Validar visualmente selección de CFDI por periodo, bloques editables, corrección de errores y sugerencias de cuentas; registrar fecha, resultado y observaciones. Sólo una aprobación humana registrada permite cambiar el estado a Implementada. El estado de trabajo sigue en «Actualización pendiente» mientras BE-006-04 no tenga destino definido y cierre técnico.
