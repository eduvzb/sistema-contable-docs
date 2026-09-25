# SPEC-007 — PPD y complementos

- **Estado:** QA
- **Actualizado:** 2026-09-24 (migración documental; sin cambio de estado)
- **Criterios de esta entrega:** Sin tareas técnicas abiertas; resta QA humana.
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-002](../002-contexto-contable/spec.md), [SPEC-004](../004-documentos-fiscales/spec.md), [SPEC-006](../006-polizas-trazabilidad/spec.md)

## Contexto y objetivo

Representar facturas PPD, complementos de pago, asignaciones parciales y pagos en varios periodos. Conservar relaciones documentales, importes asignados y trazabilidad hacia las pólizas y periodos, sin calcular todavía saldos de liquidación.

El complemento permanece como `FiscalDocument` con relaciones a las facturas conforme a OQ-005. En este alcance se admiten CFDI 4.0 de tipo `P` y sus referencias `DoctoRelacionado`; no se crea una entidad `PaymentComplement` independiente.

## Historias de usuario

- H-007-01: Como contador quiero consultar complementos y facturas PPD relacionadas, para reconstruir pagos documentales entre periodos.
- H-007-02: Como contador quiero seguir las referencias hacia pólizas y periodos, para revisar la trazabilidad de la operación.

## Requisitos funcionales y criterios de aceptación

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

## Requisitos no funcionales aplicables

- Aislamiento y precisión de importes: CA-007-05/07/08/09 y DT-011.

## Casos límite

- Factura aún no importada, complemento de múltiples facturas, otra empresa y distintos periodos: CA-007-05/07/08/09.

## Fuera de alcance

No incluye cálculo de saldo, sobrepagos, diferencias, provisiones automáticas, automatización de IVA, reglas por régimen ni moneda extranjera avanzada.

## Decisiones, supuestos y dudas

### Pendientes y decisiones

- **Resuelto para este alcance:** contrato de relaciones documentales CFDI `P` → facturas, importes `ImpPagado` con seis decimales, referencias pendientes y trazabilidad contable mediante las relaciones de SPEC-006. Las referencias de otra empresa permanecen sin vínculo navegable.
- **Fuera de este alcance y pendiente:** base del saldo, pagos computables, fecha de corte, diferencias, sobrepagos, duplicidad de relaciones, estados de liquidación, moneda avanzada y cualquier tratamiento fiscal o contable automático. Estos puntos requieren una decisión posterior antes de calcular saldos.
- **Supuestos para validar:** representación funcional de complementos para múltiples facturas conforme a OQ-005. BR-015 conserva revisión normativa pendiente; esta representación no declara validez fiscal.
- **Posterior:** provisiones e IVA automáticos (OQ-006/OQ-007), diferencias cambiarias y tratamientos fiscales completos. Las cuentas las selecciona el contador.

## Criterios de finalización

- Los criterios de esta entrega deben tener implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §15: PPD](../../docs/planeacion/003%20-%20MVP-Scope.md#15-ppd-y-complementos-de-pago).
- [BR-012](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#14-br-012--pue-y-ppd-se-tratan-como-escenarios-diferentes), [BR-013](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#15-br-013--una-factura-ppd-puede-tener-varios-pagos), [BR-014](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#16-br-014--los-pagos-pueden-ocurrir-en-distintos-periodos), [BR-015](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#17-br-015--los-complementos-deben-conservar-su-relaci%C3%B3n-con-la-factura). BR-012/013/014 están confirmadas; BR-015 conserva PENDIENTE DE VALIDACIÓN NORMATIVA aunque se utiliza para representar el escenario MVP.
- [AC-003](../../docs/planeacion/004%20-%20Escenarios%20contables.md#5-escenario-ac-003--factura-ppd-pendiente-de-pago-o-cobro), [AC-004](../../docs/planeacion/004%20-%20Escenarios%20contables.md#6-escenario-ac-004--pago-parcial-de-factura-ppd), [AC-005](../../docs/planeacion/004%20-%20Escenarios%20contables.md#7-escenario-ac-005--m%C3%BAltiples-pagos-en-distintos-periodos), [AC-007](../../docs/planeacion/004%20-%20Escenarios%20contables.md#9-escenario-ac-007--un-xml-relacionado-con-varias-p%C3%B3lizas) (necesidad funcional; cuentas/cálculos pendientes).
- [OQ-003](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#5-oq-003--momento-en-que-un-cfdi-se-considera-contabilizado), [OQ-004](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#6-oq-004--saldo-pendiente-en-ppd), [OQ-005](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#7-oq-005--complementos-que-pagan-m%C3%BAltiples-facturas), [OQ-006](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#8-oq-006--provisi%C3%B3n-en-operaciones-ppd), [OQ-007](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#9-oq-007--iva-pendiente-y-momento-de-pagocobro), [OQ-019](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#21-oq-019--moneda-extranjera).
