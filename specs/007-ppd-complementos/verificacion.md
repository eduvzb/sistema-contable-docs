# Verificación — SPEC-007

La entrega vigente y su estado se consultan en [spec.md](spec.md). Las pruebas, cierres y estados de entrega fechados a continuación son evidencia de su revisión histórica; no acreditan automáticamente criterios añadidos o modificados después.

## Entrega vigente

No hay tareas técnicas abiertas. La validación visual humana de relaciones PPD y navegación permanece pendiente.

## Evidencia histórica y QA

**Evidencia de producto:** implementación backend y frontend realizada el 2026-09-08 en los árboles de trabajo; las comprobaciones técnicas están completas. La spec está en QA para validación visual humana.

| Criterios | Prueba/comprobación | Resultado |
| --- | --- | --- |
| CA-007-01/02/03/05/07/09 | `tests/Feature/Spec007Test.php::test_payment_complement_preserves_a_same_company_allocation_in_both_document_details`, `test_payment_complement_preserves_multiple_invoice_allocations`, `test_pending_invoice_reference_is_resolved_when_the_invoice_is_imported_later`, `test_payment_reference_to_another_company_remains_unresolved_and_is_not_exposed` | Pasa: extracción, importes de seis decimales, múltiples facturas, referencias pendientes, resolución posterior y aislamiento. |
| CA-007-04/06/08 | `tests/Feature/Spec007Test.php::test_payment_and_invoice_policies_keep_their_own_periods_in_the_trace` | Pasa: complementos y pólizas conservan sus periodos y el detalle mantiene `accounted` separado de la relación documental. |
| Autorización | `tests/Feature/Spec007Test.php::test_user_without_company_access_cannot_read_payment_trace` | Pasa: el usuario sin acceso recibe `404`. |
| Backend | `./vendor/bin/sail artisan test --compact tests/Feature/Spec007Test.php` | Pasa: 6 pruebas, 43 aserciones. |
| Regresión backend | `./vendor/bin/sail artisan test --compact` | Pasa: 54 pruebas, 440 aserciones. |
| Frontend | `pnpm lint`, `pnpm typecheck`, `pnpm build` | Pasa con Next.js 16.3.4. |

Las pruebas verifican extracción, persistencia, trazabilidad bidireccional y aislamiento. No se prueba cálculo de saldo porque está fuera de este alcance.

**QA humana:** pendiente. Validar visualmente la trazabilidad factura PPD ↔ complemento, los importes aplicados, las referencias pendientes/resueltas y la navegación hacia pólizas y periodos. Sólo su aprobación registrada permite marcar la spec Implementada.


## Historial documental

- **2026-09-24:** se migró la documentación a `spec.md`, `plan.md`, tareas por repositorio y `verificacion.md` sin cambiar código del producto ni ejecutar pruebas de producto; el estado vigente permanece en `spec.md`.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar reglas de PPD.

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-08:** por decisión de continuidad se reduce el alcance implementable a trazabilidad documental: relaciones CFDI `P`–factura, importes `ImpPagado`, referencias pendientes y navegación hacia pólizas/periodos. El saldo PPD y los tratamientos fiscales permanecen diferidos; la spec pasa a Lista.
- **2026-09-08:** se implementaron parser CFDI 4.0 tipo `P`, persistencia de asignaciones, resolución posterior de referencias, detalle fiscal bidireccional, interfaz y cobertura automatizada.
- **2026-09-10:** se reclasificó como QA conforme a DP-004; sólo resta validación visual humana del recorrido preparado.
