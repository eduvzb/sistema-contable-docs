# Verificación — SPEC-008

La entrega vigente y su estado se consultan en [spec.md](spec.md). Las pruebas, cierres y estados de entrega fechados a continuación son evidencia de su revisión histórica; no acreditan automáticamente criterios añadidos o modificados después.

## Entrega vigente

No hay tareas técnicas abiertas. La validación visual humana de lectura, importes y estados de la balanza permanece pendiente.

## Evidencia histórica y QA

**Evidencia de producto:** la implementación está vinculada en el árbol de trabajo y las comprobaciones técnicas están completas. La spec está en QA para validación visual humana.

| Criterios | Prueba/comprobación | Resultado |
|---|---|---|
| CA-008-01/02/03/05/06/08 | `tests/Feature/Spec008Test.php::test_trial_balance_returns_nature_aware_balances_and_excludes_drafts_and_future_periods` | Pasa: verifica naturaleza, arrastre entre julio/agosto, `POSTED`, exclusión de `DRAFT` y futuro, decimales y cuenta sin movimiento. |
| CA-008-04 | `tests/Feature/Spec008Test.php::test_posting_a_draft_is_reflected_once_when_the_trial_balance_is_queried_repeatedly` | Pasa: el cambio a `POSTED` aparece una vez en consultas repetidas. |
| CA-008-07 | `tests/Feature/Spec008Test.php::test_trial_balance_returns_not_found_for_unauthenticated_or_foreign_contexts` | Pasa: `401` sin sesión y `404` para empresa o periodo ajenos. |
| CA-008-05 | `tests/Feature/Spec008Test.php::test_trial_balance_does_not_mix_companies_or_periods` | Pasa: solo se devuelve el catálogo y movimiento de la empresa consultada. |
| Backend | `./vendor/bin/sail artisan test --compact` | Pasa: 35 pruebas, 302 assertions. |
| Frontend | `pnpm lint`, `pnpm typecheck`, `pnpm build` | Pasa. |

Las pruebas cubren valores decimales conocidos, `POSTED`/`DRAFT`, dos empresas y varios periodos.

**QA humana:** pendiente. Validar visualmente encabezados, importes, estados vacíos y lectura de la balanza en el periodo seleccionado; sólo su aprobación registrada permite marcar la spec Implementada.

La revisión documental de esta entrega está en el [índice](../README.md#verificaci%C3%B3n-documental); la implementación queda en los árboles backend y frontend indicados por el estado de continuidad.

## Historial documental

- **2026-09-24:** se migró la documentación a `spec.md`, `plan.md`, tareas por repositorio y `verificacion.md` sin cambiar código del producto ni ejecutar pruebas de producto; el estado vigente permanece en `spec.md`.
- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el cálculo pendiente de balanza.
- **2026-09-08:** se cerró el alcance mínimo: saldo inicial derivado de periodos anteriores, saldo por naturaleza, filas sin movimiento sin agregados jerárquicos, seis decimales como texto y contrato `trial-balance`. La spec queda Lista y su implementación mínima está añadida; `OpeningBalance` y migración permanecen fuera del MVP.
- **2026-09-10:** se reclasificó como QA conforme a DP-004; sólo resta validación visual humana del recorrido preparado.
