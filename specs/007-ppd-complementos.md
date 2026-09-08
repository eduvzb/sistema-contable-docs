# SPEC-007 — PPD y complementos

**Estado:** Borrador  
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-002](002-contexto-contable.md), [SPEC-004](004-documentos-fiscales.md), [SPEC-006](006-polizas-trazabilidad.md)

## Propósito y alcance

Representar facturas PPD pendientes de pago/cobro, complementos, pagos parciales y pagos en varios periodos. Conservar relaciones, importes y trazabilidad para consultar el saldo pendiente cuando su cálculo esté definido.

El complemento permanece como FiscalDocument con relaciones a las facturas conforme a OQ-005. No incluye provisiones automáticas, automatización de IVA, reglas por régimen ni moneda extranjera avanzada.

## Fuentes

- [Alcance §15: PPD](../docs/planeacion/003%20-%20MVP-Scope.md#15-ppd-y-complementos-de-pago).
- [BR-012](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#14-br-012--pue-y-ppd-se-tratan-como-escenarios-diferentes), [BR-013](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#15-br-013--una-factura-ppd-puede-tener-varios-pagos), [BR-014](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#16-br-014--los-pagos-pueden-ocurrir-en-distintos-periodos), [BR-015](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#17-br-015--los-complementos-deben-conservar-su-relaci%C3%B3n-con-la-factura). BR-012/013/014 están confirmadas; BR-015 conserva PENDIENTE DE VALIDACIÓN NORMATIVA aunque se utiliza para representar el escenario MVP.
- [AC-003](../docs/planeacion/004%20-%20Escenarios%20contables.md#5-escenario-ac-003--factura-ppd-pendiente-de-pago-o-cobro), [AC-004](../docs/planeacion/004%20-%20Escenarios%20contables.md#6-escenario-ac-004--pago-parcial-de-factura-ppd), [AC-005](../docs/planeacion/004%20-%20Escenarios%20contables.md#7-escenario-ac-005--m%C3%BAltiples-pagos-en-distintos-periodos), [AC-007](../docs/planeacion/004%20-%20Escenarios%20contables.md#9-escenario-ac-007--un-xml-relacionado-con-varias-p%C3%B3lizas) (necesidad funcional; cuentas/cálculos pendientes).
- [OQ-003](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#5-oq-003--momento-en-que-un-cfdi-se-considera-contabilizado), [OQ-004](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#6-oq-004--saldo-pendiente-en-ppd), [OQ-005](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#7-oq-005--complementos-que-pagan-m%C3%BAltiples-facturas), [OQ-006](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#8-oq-006--provisi%C3%B3n-en-operaciones-ppd), [OQ-007](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#9-oq-007--iva-pendiente-y-momento-de-pagocobro), [OQ-019](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#21-oq-019--moneda-extranjera).

## Comportamiento y criterios de aceptación

La factura PPD puede relacionarse con una póliza inicial y después con movimientos de pago/cobro. Un complemento mantiene su relación con cada factura e importe correspondiente; los pagos conservan su periodo. El usuario operativo registra manualmente las partidas mediante SPEC-006; el administrador accede a cualquier empresa y el contador solo a sus asignadas, conforme a DT-008/SPEC-001.

«Contabilizado» no significa «liquidado». OQ-004 propone importe de la operación menos pagos relacionados, pero no decide todos los componentes del cálculo; se debe cerrar esa definición antes de implementar el saldo.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-007-01 | Se registra una factura PPD sin pagos. | Puede representarse pendiente de liquidación y vincularse a una póliza inicial, sin asumir que ocurrió un cobro/pago. |
| CA-007-02 | Existe un complemento relacionado con una factura. | Se conserva como documento fiscal con relación a la factura y el pago puede trazarse a su póliza; BR-015 mantiene su estado de revisión normativa. |
| CA-007-03 | Una factura de 100,000 tiene un pago de 40,000 en el caso simple de AC-004, sin diferencias. | Se representan factura, pago y pendiente de 60,000 conforme al ejemplo provisional; este ejemplo no resuelve ajustes, monedas ni la base general del cálculo. |
| CA-007-04 | Una factura de 100,000 recibe 50,000 en julio y 50,000 en agosto, como en AC-005. | Cada pago/póliza conserva su periodo; la operación puede reconstruirse cronológicamente y consultarse su saldo bajo el cálculo que se prepare. |
| CA-007-05 | Un complemento se relaciona con más de una factura. | Se conserva cada relación con su importe correspondiente, según el modelo provisional OQ-005, sujeto a validación. |
| CA-007-06 | Una factura participa en una póliza POSTED pero tiene pagos pendientes. | Puede identificarse contabilizada sin presentarse por ello como liquidada. |
| CA-007-07 | Se intenta relacionar un pago/complemento con información de otra empresa. | No se crea una relación que mezcle información de empresas. |
| CA-007-08 | Se consulta una factura con pagos y pólizas en distintos periodos. | Se pueden reconstruir sus relaciones sin limitar artificialmente todos sus movimientos al periodo de la factura. |

## Pendientes y decisiones

- **Antes de Lista:** base del importe y pagos computables para saldo, fecha de corte y relación del cálculo con estados de pólizas; diferencias, sobrepagos, duplicidad de relaciones y monedas; campos del complemento en las versiones CFDI admitidas; tratamiento de referencias a facturas aún no importadas; contrato de relaciones e importes por factura. Estos puntos impiden cerrar el cálculo, no iniciar otras specs.
- **Supuestos para validar:** saldo conceptual de OQ-004 y representación de complemento para múltiples facturas de OQ-005. BR-015 conserva revisión normativa pendiente; la representación funcional no declara validez fiscal.
- **Posterior:** provisiones e IVA automáticos (OQ-006/OQ-007), diferencias cambiarias y tratamientos fiscales completos. Las cuentas las selecciona el contador.

## Plan técnico y contratos

- Backend: concretar datos extraídos con SPEC-004, definir aquí relaciones complemento-factura, importes de pago y saldo; reutilizar contratos de pólizas de SPEC-006. No crear una entidad PaymentComplement independiente por aparecer como candidata en el análisis.
- Frontend: detalle de factura con complementos, pagos, periodos, pólizas y saldo; distinguir estado contable de liquidación.
- Una vez decidido el cálculo, agregar criterios para diferencias, fechas de corte y errores relevantes antes de Lista. Aplicar DT-004 a importes y operaciones decimales.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). Los contratos aún no están cerrados: resolver los detalles necesarios antes de Lista, sin introducir reglas para completar huecos.

## Verificación

**Evidencia de producto:** pendiente; no ejecutada. No existe implementación vinculada todavía.

Prever fixtures de factura sin pago, parcial, pagos en dos periodos y complemento para múltiples facturas. Verificar trazabilidad y aislamiento. Los ejemplos simples no sustituyen las pruebas del cálculo definitivo ni una revisión normativa.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar reglas de PPD.

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
