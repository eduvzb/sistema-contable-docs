# Verificación — SPEC-004

## Entrega actual

- [x] La regresión actual del árbol integrado pasa con Laravel Sail: `./vendor/bin/sail artisan test --compact`, 114 pruebas y 1,057 aserciones (2026-10-15; árbol equivalente a backend `2253855`).
- [x] La suite frontend pasa: `pnpm test`, 58 pruebas en 10 archivos; `pnpm typecheck` y `pnpm build` aprobados (árbol equivalente a `23c845a`).
- [x] `pnpm lint` termina sin errores; reporta 94 advertencias en herramientas locales excluidas de Git.
- [ ] `pnpm format:check` global: falla previamente en 87 archivos locales de `.agents`/`.impeccable`; no se considera aprobado ni se modifica ese trabajo ajeno. No hay cambios de código para esta spec.


CA-004-12/13: conservación de conceptos CFDI y consulta autorizada del detalle. Código y pruebas añadidos el 2026-10-14; la validación integrada se completó con Laravel Sail.

## Estado de validación

### Validación técnica comprobada

- [x] El parser conserva orden, repetidos, descripción completa, entidades XML, prefijo alternativo y posiciones sin descripción; CFDI sin conceptos produce una lista vacía.
  - `./vendor/bin/sail artisan test --compact tests/Unit/CfdiXmlParserTest.php`: 2 pruebas aprobadas.
- [x] CA-004-12/13: las pruebas de importación, duplicados, lotes, lista vacía, documentos anteriores, detalle autorizado, aislamiento y ausencia de conceptos en listado/importación pasan.
  - `./vendor/bin/sail artisan test --compact tests/Feature/Spec004Test.php`: 11 pruebas y 99 aserciones aprobadas.
  - `./vendor/bin/sail artisan test --compact`: 100 pruebas y 951 aserciones aprobadas.
- [x] El contrato y servicio de detalle frontend aceptan lista, `null`, campo ausente y errores; la suite de comportamiento, tipos, lint de archivos modificados y formato pasan.
  - `pnpm test`: 8 archivos y 42 pruebas aprobadas.
  - `pnpm typecheck`: aprobado.
  - `pnpm exec eslint <archivos modificados>`: aprobado.
  - `pnpm exec prettier --check <archivos modificados>`: aprobado.
  - `pnpm build`: aprobado.
- [x] Pint y revisión de whitespace del backend pasan.
  - `vendor/bin/pint --dirty --format agent` y `git diff --check`: aprobados.
- [x] Ramas publicadas, PR integrados previamente en `main` y revisión solicitada a colaborador con acceso.
  - Backend: commit `d841b59`, integrado, [PR #9](https://github.com/eduvzb/sistema-contable-back/pull/9).
  - Frontend: commit `c032007`, integrado, [PR #18](https://github.com/eduvzb/sistema-contable-front/pull/18).

### QA humana

- [x] Revisar el resultado integrado con la vista previa de [SPEC-006](../006-polizas-trazabilidad/verificacion.md), incluidos conceptos de nuevas importaciones y el aviso de documentos anteriores (tarea 023).
  - Aprobado el 2026-10-15 por el usuario solicitante, según confirmación recibida en esta sesión. No se reportaron observaciones.

## Contraste de implementación

El cambio agrega una columna JSON nullable, extracción por espacio de nombres CFDI, persistencia en la importación existente y conceptos sólo en el recurso de detalle. Las pruebas de integración se ejecutaron con PostgreSQL dentro de Laravel Sail.
