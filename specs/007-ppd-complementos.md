# SPEC-007 — PPD y complementos

**Estado:** QA
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-002](002-contexto-contable.md), [SPEC-004](004-documentos-fiscales.md), [SPEC-006](006-polizas-trazabilidad.md)

## Propósito y alcance

Representar facturas PPD, complementos de pago, asignaciones parciales y pagos en varios periodos. Conservar relaciones documentales, importes asignados y trazabilidad hacia las pólizas y periodos, sin calcular todavía saldos de liquidación.

El complemento permanece como `FiscalDocument` con relaciones a las facturas conforme a OQ-005. En este alcance se admiten CFDI 4.0 de tipo `P` y sus referencias `DoctoRelacionado`; no se crea una entidad `PaymentComplement` independiente. No incluye cálculo de saldo, sobrepagos, diferencias, provisiones automáticas, automatización de IVA, reglas por régimen ni moneda extranjera avanzada.

## Fuentes

- [Alcance §15: PPD](../docs/planeacion/003%20-%20MVP-Scope.md#15-ppd-y-complementos-de-pago).
- [BR-012](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#14-br-012--pue-y-ppd-se-tratan-como-escenarios-diferentes), [BR-013](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#15-br-013--una-factura-ppd-puede-tener-varios-pagos), [BR-014](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#16-br-014--los-pagos-pueden-ocurrir-en-distintos-periodos), [BR-015](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#17-br-015--los-complementos-deben-conservar-su-relaci%C3%B3n-con-la-factura). BR-012/013/014 están confirmadas; BR-015 conserva PENDIENTE DE VALIDACIÓN NORMATIVA aunque se utiliza para representar el escenario MVP.
- [AC-003](../docs/planeacion/004%20-%20Escenarios%20contables.md#5-escenario-ac-003--factura-ppd-pendiente-de-pago-o-cobro), [AC-004](../docs/planeacion/004%20-%20Escenarios%20contables.md#6-escenario-ac-004--pago-parcial-de-factura-ppd), [AC-005](../docs/planeacion/004%20-%20Escenarios%20contables.md#7-escenario-ac-005--m%C3%BAltiples-pagos-en-distintos-periodos), [AC-007](../docs/planeacion/004%20-%20Escenarios%20contables.md#9-escenario-ac-007--un-xml-relacionado-con-varias-p%C3%B3lizas) (necesidad funcional; cuentas/cálculos pendientes).
- [OQ-003](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#5-oq-003--momento-en-que-un-cfdi-se-considera-contabilizado), [OQ-004](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#6-oq-004--saldo-pendiente-en-ppd), [OQ-005](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#7-oq-005--complementos-que-pagan-m%C3%BAltiples-facturas), [OQ-006](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#8-oq-006--provisi%C3%B3n-en-operaciones-ppd), [OQ-007](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#9-oq-007--iva-pendiente-y-momento-de-pagocobro), [OQ-019](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#21-oq-019--moneda-extranjera).

## Contexto de ejecución

**Modo actual:** QA. La implementación y las comprobaciones técnicas están completas; usar esta spec para validar visualmente trazabilidad factura PPD ↔ complemento, importes, referencias y navegación.

**Paquete funcional:** esta spec contiene el alcance autoritativo de trazabilidad documental, relaciones, importes asignados, referencias pendientes y criterios CA-007-01 a CA-007-08. El saldo, la liquidación y los tratamientos fiscales diferidos no forman parte de una ejecución de este alcance.

**Dependencias y fuentes consolidadas:** consultar SPEC-002, SPEC-004 y SPEC-006 para los contratos vigentes de contexto, documentos y pólizas. Las fuentes enlazadas arriba y los límites explícitos de esta spec ya están consolidados; no recargarlos durante una ejecución normal si no cambiaron.

**Reabrir fuentes cuando:** cambie un contrato de dependencia, se resuelva normativamente BR-015 o un pendiente diferido afecte este alcance, aparezca una contradicción o el usuario solicite calcular saldo/liquidación.

## Comportamiento y criterios de aceptación

La factura PPD puede relacionarse con una póliza inicial y un complemento puede conservar una o varias asignaciones a facturas. Cada asignación conserva el UUID referido y `ImpPagado` con seis decimales como texto; cuando la factura ya está importada en la misma empresa también conserva su documento relacionado. Los complementos y sus pólizas conservan sus fechas y periodos mediante SPEC-006. El usuario operativo registra manualmente las partidas mediante SPEC-006; el administrador accede a cualquier empresa y el contador solo a sus asignadas, conforme a DT-008/SPEC-001.

«Contabilizado» no significa «liquidado». El detalle de este alcance no expone saldo, importe pagado acumulado ni estado de liquidación. OQ-004 permanece pendiente para una ampliación posterior.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-007-01 | Se registra una factura PPD sin pagos. | Puede representarse pendiente de liquidación y vincularse a una póliza inicial, sin asumir que ocurrió un cobro/pago. |
| CA-007-02 | Existe un complemento relacionado con una factura. | Se conserva como documento fiscal con relación a la factura y el pago puede trazarse a su póliza; BR-015 mantiene su estado de revisión normativa. |
| CA-007-03 | Una factura de 100,000 tiene un pago de 40,000 en el caso simple de AC-004, sin diferencias. | Se representan la factura, el complemento y la asignación documental `40.000000`; no se calcula ni se expone un saldo de `60,000`. |
| CA-007-04 | Una factura de 100,000 recibe 50,000 en julio y 50,000 en agosto, como en AC-005. | Cada complemento conserva su asignación y sus pólizas relacionadas conservan el periodo correspondiente; la operación puede reconstruirse cronológicamente sin calcular saldo. |
| CA-007-05 | Un complemento se relaciona con más de una factura. | Se conserva cada UUID referido y su importe `ImpPagado`; las facturas importadas en la misma empresa aparecen como relaciones navegables. |
| CA-007-06 | Una factura participa en una póliza POSTED y tiene complementos relacionados. | Puede identificarse contabilizada mediante SPEC-006 sin presentarse por ello como liquidada. |
| CA-007-07 | Se intenta relacionar un pago/complemento con información de otra empresa. | No se crea una relación que mezcle información de empresas. |
| CA-007-08 | Se consulta una factura con complementos y pólizas en distintos periodos. | Se pueden reconstruir sus relaciones documentales y contables sin limitar artificialmente todos sus movimientos al periodo de la factura. |
| CA-007-09 | Se importa un complemento cuya factura referida todavía no existe en la empresa. | Se conserva el UUID y el importe referido como relación pendiente, sin crear un documento ficticio ni exponer documentos de otra empresa. |

## Pendientes y decisiones

- **Resuelto para este alcance:** contrato de relaciones documentales CFDI `P` → facturas, importes `ImpPagado` con seis decimales, referencias pendientes y trazabilidad contable mediante las relaciones de SPEC-006. Las referencias de otra empresa permanecen sin vínculo navegable.
- **Fuera de este alcance y pendiente:** base del saldo, pagos computables, fecha de corte, diferencias, sobrepagos, duplicidad de relaciones, estados de liquidación, moneda avanzada y cualquier tratamiento fiscal o contable automático. Estos puntos requieren una decisión posterior antes de calcular saldos.
- **Supuestos para validar:** representación funcional de complementos para múltiples facturas conforme a OQ-005. BR-015 conserva revisión normativa pendiente; esta representación no declara validez fiscal.
- **Posterior:** provisiones e IVA automáticos (OQ-006/OQ-007), diferencias cambiarias y tratamientos fiscales completos. Las cuentas las selecciona el contador.

## Plan técnico y contratos

- Backend: extraer `DoctoRelacionado/@IdDocumento` e `ImpPagado` de CFDI 4.0 tipo `P`, persistir una asignación documental con UUID e importe, resolver el documento si pertenece a la misma empresa y extender el detalle fiscal en ambos sentidos. Reutilizar los contratos de pólizas de SPEC-006. No crear una entidad `PaymentComplement` independiente.
- Frontend: detalle fiscal con facturas relacionadas desde un complemento y complementos desde una factura, importes asignados y pólizas/periodos existentes. No mostrar saldo ni estado de liquidación.
- Ejemplo documental de factura PPD y complemento de pago: [ejemplos de XML CFDI](../docs/ejemplos/README.md).
- Los importes de asignación se almacenan con seis decimales y se representan como texto. El cálculo, las diferencias, los sobrepagos y los errores asociados quedan para una ampliación que deberá actualizar esta spec antes de modificar consumidores.

### Contrato de trazabilidad documental

La importación de un CFDI 4.0 tipo `P` conserva sus referencias `DoctoRelacionado` en una colección `payment_allocations`. Cada elemento contiene:

```json
{
  "related_uuid": "11111111-1111-4111-8111-111111111111",
  "invoice_id": 42,
  "allocated_amount": "40000.000000"
}
```

`invoice_id` es `null` cuando el UUID todavía no está importado en la misma empresa o pertenece a otra empresa. No se crea un `FiscalDocument` ficticio. Desde el detalle de una factura, `payment_complements` expone `id`, `uuid`, `issued_at` y `allocated_amount`; desde el detalle del complemento, `payment_allocations` expone los datos anteriores y, cuando existe, el resumen de la factura relacionada. Las colecciones conservan un orden estable por el identificador de asignación.

Las asignaciones se autorizan con el mismo acceso a la empresa del documento. Una referencia coincidente en otra empresa no se enlaza ni se serializan sus datos. Las pólizas y periodos se consultan mediante `accounting_policies` de SPEC-006; este contrato no añade saldo, liquidación ni cálculo contable.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). El contrato de trazabilidad de este alcance queda cerrado; cualquier ampliación de saldos o tratamiento de pagos debe actualizar esta spec antes de modificar consumidores.

## Verificación

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

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar reglas de PPD.

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-08:** por decisión de continuidad se reduce el alcance implementable a trazabilidad documental: relaciones CFDI `P`–factura, importes `ImpPagado`, referencias pendientes y navegación hacia pólizas/periodos. El saldo PPD y los tratamientos fiscales permanecen diferidos; la spec pasa a Lista.
- **2026-09-08:** se implementaron parser CFDI 4.0 tipo `P`, persistencia de asignaciones, resolución posterior de referencias, detalle fiscal bidireccional, interfaz y cobertura automatizada.
- **2026-09-10:** se reclasificó como QA conforme a DP-004; sólo resta validación visual humana del recorrido preparado.
