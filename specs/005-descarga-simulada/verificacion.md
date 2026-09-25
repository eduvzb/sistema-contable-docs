# Verificación — SPEC-005

La entrega vigente y su estado se consultan en [spec.md](spec.md). Las pruebas, cierres y estados de entrega fechados a continuación son evidencia de su revisión histórica; no acreditan automáticamente criterios añadidos o modificados después.

## Entrega vigente

La tarea BE-005-01 debe reconciliar el cierre técnico de la actualización DT-013 con la evidencia backend ya registrada. La clasificación vigente se decide desde spec.md, no desde los párrafos históricos de QA.

## Evidencia histórica y QA

**Evidencia histórica de producto:** implementación backend y frontend realizada el 2026-09-08; las comprobaciones técnicas de esa entrega están completas. Su clasificación QA fue anterior a la actualización DT-013; el estado vigente se consulta en `spec.md`.

| Criterios | Prueba/comprobación | Resultado |
|---|---|---|
| CA-005-01/02/03/05/06 | `tests/Feature/Spec005Test.php::test_authorized_user_can_run_simulated_download_and_repeated_results_are_deduplicated` y `test_simulated_download_returns_not_found_for_unauthenticated_or_foreign_contexts` | Evidencia histórica: solicita por empresa/periodo, incorpora dos fixtures deterministas, repite sin duplicar y aísla autenticación/empresas/periodos. El descarte del original se comprueba en la actualización DT-013. |
| CA-005-02 | `tests/Feature/Spec005Test.php::test_simulated_download_reports_partial_imports_and_keeps_valid_documents` | Pasa: informa tres encontrados, dos incorporados y un rechazo sin deshacer los válidos. |
| CA-005-04 | `tests/Feature/Spec005Test.php::test_simulated_download_document_can_be_used_in_a_policy_without_losing_company_or_period_context` | Pasa: descarga, incorporación, póliza `POSTED`, pivote y trazabilidad inversa conservan empresa y periodo. |
| Vacío | `tests/Feature/Spec005Test.php::test_empty_simulated_download_returns_completed_without_creating_documents` | Pasa: `COMPLETED`, cero encontrados y cero documentos persistidos. |
| Fallo/reintento | `tests/Feature/Spec005Test.php::test_failed_simulated_download_does_not_import_and_can_be_retried` | Pasa: `FAILED` no persiste y un segundo intento controlado incorpora los documentos. |
| Backend focalizado | `./vendor/bin/sail artisan test --compact tests/Feature/Spec005Test.php` | Pasa: 7 pruebas y 62 aserciones. |
| Backend completo | `./vendor/bin/sail artisan test --compact` | Pasa: 72 pruebas y 650 aserciones. |
| Frontend | `pnpm lint`, `pnpm typecheck`, `pnpm run build` | Pasa. |

**Evidencia técnica de DT-013 — 2026-09-14:** la descarga simulada reutiliza el importador sin escribir el contenido XML; `Spec005Test::test_authorized_user_can_run_simulated_download_and_repeated_results_are_deduplicated` confirma que los documentos creados tienen `original_path = null`. Las pruebas focalizadas de SPEC-004/005/007 y seeder pasaron con 19 pruebas y 170 aserciones, y `./vendor/bin/sail artisan test --compact` pasó con 86 pruebas y 846 aserciones. `vendor/bin/pint --dirty --format agent` y `git diff --check` pasaron. Backend: rama `codex/refactor/SPEC-004/no-durable-xml`, commit [`a7a5aaa`](https://github.com/eduvzb/sistema-contable-back/commit/a7a5aaafd667ee506d18b8dbf79539d3c82913b3), [PR #6](https://github.com/eduvzb/sistema-contable-back/pull/6) abierto.

Revisiones de implementación: backend sobre `868b20eaaa24c387e7e80f97a5798f024a4582e4` con cambios locales; frontend sobre `597bdc5f71c2ee071ce173ddc81167f2a7461bd7` con cambios locales.

**QA humana:** pendiente. Validar visualmente inicio, resultado/reintento y continuidad hacia la bandeja y una póliza; sólo la aprobación humana registrada permite marcar la spec Implementada.


## Historial documental

- **2026-09-24:** se migró la documentación a `spec.md`, `plan.md`, tareas por repositorio y `verificacion.md` sin cambiar código del producto ni ejecutar pruebas de producto; el estado vigente permanece en `spec.md`.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance de la simulación.

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-08:** se cerró el contrato mínimo de simulación síncrona, fixtures deterministas por empresa/periodo, incorporación parcial reutilizando SPEC-004 y estados `COMPLETED`/`FAILED` con vacío y reintento controlados en pruebas. Pasa a Lista; la implementación y su evidencia quedan pendientes.
- **2026-09-08:** se implementaron el endpoint, el servicio controlado, la incorporación compartida y la acción de frontend; las verificaciones automatizadas pasan.
- **2026-09-08:** se añadió la prueba integrada descarga simulada → CFDI incorporado → póliza balanceada → consulta inversa, conservando empresa y periodo.
- **2026-09-10:** se reclasificó como QA conforme a DP-004; sólo resta validación visual humana del recorrido preparado.
- **2026-09-14:** por instrucción explícita del usuario y DT-013, la descarga simulada deja de persistir XML originales y reutiliza el descarte definido por SPEC-004. La spec vuelve a Actualización pendiente hasta registrar la evidencia técnica de backend.
