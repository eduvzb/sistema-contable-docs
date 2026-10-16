# Verificación — SPEC-007

## Entrega actual: CA-007-05

- [x] Facturas y complementos importados son consultables desde sus relaciones en el detalle, incluso si pertenecen a otro periodo de la misma empresa. Las referencias pendientes conservan UUID e importe sin acción de navegación.
- [x] Un fallo permite reintentar; las respuestas tardías tras cerrar o cambiar empresa/periodo no reemplazan el detalle actual.
- [x] `pnpm --config.verify-deps-before-run=false test`: 62 pruebas en 10 archivos, incluidas 7 de `fiscal-document-inbox.test.tsx`, ejecutadas sobre `5649b38`.
- [x] ESLint, TypeScript, `format:check`, `git diff --check` y build de producción aprobados. El flag de pnpm evita reinstalación en el worktree con dependencias enlazadas; no cambia paquetes ni lockfile.
- [x] Revisión independiente `audit_001_003`, gpt-6-luna/high: sin hallazgos bloqueantes. Límite: se prueba cambio de empresa/contexto y cierre; no hay caso aislado de cambio sólo de periodo. La implementación invalida ambos identificadores.
- [x] Rama publicada `codex/fix/SPEC-007/navegacion-relaciones`, SHA `5649b3803a51e3c4f7881a955916503ff4b395be`, [PR frontend #20](https://github.com/eduvzb/sistema-contable-front/pull/20) hacia `main`; revisión solicitada a `alavazarez`. No hay cambios backend para esta entrega.
- [ ] QA humana de la interacción nueva: navegar factura↔complemento, revisar teclado, carga y reintento. Registrar persona, fecha, resultado y observaciones.

## QA humana del alcance anterior (conservada)

Factura PPD ↔ complemento, importes aplicados, referencias pendientes/resueltas y navegación hacia pólizas y periodos. Aprobación confirmada el 2026-10-15 por el usuario solicitante en esta sesión; fecha de ejecución y observaciones no especificadas.
