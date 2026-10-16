# Verificación — SPEC-006

## Resumen de la entrega

- [x] CA-006-30/34/35: opción global persistente y restringida a administradores; las pólizas consultan su valor vigente al guardar.
- [x] CA-006-07/31/32/33: CFDI usados siguen visibles; los vínculos nuevos se validan en el servidor, sin escrituras parciales y conservando relaciones previas.
- [x] CA-006-32/34: dos solicitudes concurrentes a periodos distintos compiten por el mismo CFDI en PostgreSQL; solo una lo vincula. También se comprueba la serialización entre el cambio de configuración y el guardado.
- [x] CA-006-36/37: las propuestas incluyen el componente, serie-folio y emisor propios de cada XML, con sustitutos para datos ausentes o en blanco.
- [x] CA-006-38/39: conceptos editables y persistidos sin recálculo al abrir; el texto largo no se trunca y su error puede corregirse al crear o editar sin perder la captura.
- [x] Pruebas backend/frontend, tipos, formato y revisión de diferencias ejecutados según los comandos y resultados indicados abajo.
- [x] QA humana de los conceptos de partidas (tarea 018; CA-006-36/39): revisados el uso visible y la lectura/edición de conceptos en la interfaz.
  - Aprobado el 2026-10-15 por el usuario solicitante, según confirmación recibida en esta sesión. No se reportaron observaciones.
- [x] QA humana de la vista previa de conceptos CFDI (tarea 023; CA-006-25/29), integrada con la conservación y consulta descritas en SPEC-004.
  - Aprobado el 2026-10-15 por el usuario solicitante, según confirmación recibida en esta sesión. No se reportaron observaciones.
- [ ] QA humana pendiente: revisar que la opción global sea clara, que el bloqueo de CFDI usados se distinga de «contabilizado» y que los vínculos históricos sigan consultables. La revisión de teclado y anchos estrechos de estos flujos sigue pendiente.

## Evidencia técnica

### Backend

- Rama `codex/feature/SPEC-006/reutilizacion-cfdi-entrega`; commit `8d4997c`.
- PR [#11](https://github.com/eduvzb/sistema-contable-back/pull/11), fusionada a `main` el 2026-10-15; merge commit `2253855`. CI sin checks reportados.
- `./vendor/bin/sail artisan test --compact`: **114 pruebas aprobadas, 1,057 aserciones**. Incluye endpoints reales en procesos/conexiones PostgreSQL independientes para competencia por un CFDI y actualización concurrente de la opción global.
- `./vendor/bin/sail pint --dirty --format agent`: aprobado.
- `git diff --check`: aprobado.

El PR #10 se cerró como reemplazado para mantener fuera de esta entrega el commit ajeno `c89aa7f`; su rama y contenido se conservaron.

### Frontend

- Rama `codex/feature/SPEC-006/reutilizacion-cfdi`; commit `6d250cf`.
- PR [#19](https://github.com/eduvzb/sistema-contable-front/pull/19), fusionada a `main` el 2026-10-15; merge commit `23c845a`. CI sin checks reportados.
- `pnpm test`: **58 pruebas aprobadas** en 10 archivos.
- `pnpm typecheck`: aprobado.
- `pnpm lint`: cero errores; 94 warnings en scripts existentes de `.agents/skills/impeccable`.
- Prettier en los archivos frontend modificados: aprobado.
- `git diff --check`: aprobado.

### Documentación

- Rama `codex/docs/SPEC-006/cierre-tecnico`; commits `56763a1` y `62cdc69`.
- PR [#1](https://github.com/eduvzb/sistema-contable-docs/pull/1), abierta hacia `main`; reviewer `alavazarez` solicitado. CI sin checks reportados.
- `python3 scripts/spec_index.py --write` y `python3 scripts/spec_index.py --check`: 9 specs y enlaces locales validados.
- `git diff --check`: aprobado.

## QA humana pendiente

- [ ] Confirmar que la opción global en Administración sea clara y que un guardado fallido no se presente como exitoso.
- [ ] Confirmar que «Ya usado en otra póliza» se distingue de «contabilizado» y que los vínculos anteriores siguen consultables.
- [x] Tarea 018: revisar con teclado y en anchos estrechos la lectura y edición de conceptos largos y el error de longitud.
  - Aprobado el 2026-10-15 por el usuario solicitante, según confirmación recibida en esta sesión. No se reportaron observaciones.
- [x] Tarea 023: revisar la vista previa de descripciones y su integración con los conceptos conservados en SPEC-004.
  - Aprobado el 2026-10-15 por el usuario solicitante, según confirmación recibida en esta sesión. No se reportaron observaciones.
- [ ] Revisar con teclado y en anchos estrechos el selector y los vínculos históricos.
- La aprobación de las tareas 018 y 023 no cierra el QA completo de SPEC-006; los puntos pendientes anteriores deben aprobarse antes de cambiar la spec a Implementada.

## Observación fuera del alcance

Se mantiene el contraste previo: CA-006-19/20 describen una tabla con filtros, mientras el selector existente presenta una lista con búsqueda. Esta entrega no reconstruye el selector ni acredita esa discrepancia preexistente.
