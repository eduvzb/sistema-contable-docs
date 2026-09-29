# SPEC-008 — Balanza básica

- **Estado:** QA
- **Actualizado:** 2026-09-24
- **Criterios de esta entrega:** Sin tareas técnicas abiertas; resta QA humana.
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-002](../002-contexto-contable/spec.md), [SPEC-003](../003-catalogo-cuentas/spec.md), [SPEC-006](../006-polizas-trazabilidad/spec.md)

## Contexto y objetivo

Consultar por cuenta saldo inicial, cargos, abonos y saldo final del contexto contable. Las partidas de pólizas contabilizadas afectan movimientos y saldos; los borradores quedan fuera de la balanza definitiva.

## Historias de usuario

- H-008-01: Como contador quiero consultar saldos y movimientos por cuenta en el periodo seleccionado, para revisar la balanza básica.

## Requisitos funcionales y criterios de aceptación

El usuario operativo consulta la balanza de una empresa accesible y periodo; el administrador accede a cualquiera y el contador solo a sus asignadas, conforme a SPEC-001. La consulta incluye todas las cuentas de la empresa como filas independientes, sin agregar saldos de cuentas padre.

El saldo inicial acumula partidas de pólizas `POSTED` de periodos anteriores de la misma empresa; si no existen, es cero. El movimiento del periodo incluye sólo sus propias partidas `POSTED`. Para naturaleza `DEBIT`, el saldo es cargos menos abonos; para `CREDIT`, abonos menos cargos. El saldo final suma el movimiento neto al inicial y puede ser negativo. Los cálculos usan decimal exacto y la API entrega importes como texto con seis posiciones.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-008-01 | Se consulta la balanza del contexto con datos válidos preparados. | Se muestran cuenta, saldo inicial, cargos, abonos y saldo final según la naturaleza de cada cuenta y el periodo seleccionado. |
| CA-008-02 | Existen pólizas POSTED del contexto. | Sus partidas se reflejan en los movimientos de las cuentas correspondientes. |
| CA-008-03 | Existe una póliza DRAFT con partidas, balanceadas o desbalanceadas. | Sus partidas no afectan la balanza definitiva. |
| CA-008-04 | Una póliza pasa de DRAFT a POSTED conforme a SPEC-006. | La balanza refleja el efecto de sus partidas contabilizadas al volver a consultarla, sin duplicar ese efecto por consultas repetidas. |
| CA-008-05 | Se consulta empresa A teniendo también acceso a B. | La balanza de A no mezcla cuentas ni movimientos de B; un usuario sin acceso a A tampoco puede consultarla. |
| CA-008-06 | Una factura origina pólizas en julio y agosto. | Cada póliza conserva su periodo; los movimientos de cada consulta respetan ese periodo. El saldo inicial de agosto incluye el efecto `POSTED` de julio, pero el movimiento de agosto solo incluye sus propias partidas. |
| CA-008-07 | Un usuario consulta una empresa no asignada o un periodo de otra empresa. | La respuesta es `404` y no revela cuentas ni movimientos del contexto ajeno. |
| CA-008-08 | Una cuenta no tiene movimientos `POSTED` en ningún periodo o no tiene movimientos en el periodo consultado. | La cuenta aparece una sola vez. Sin historial, todos sus importes son cero; si existen movimientos anteriores, cargos y abonos del periodo son cero y el saldo inicial y final conservan ese historial, sin agregados de cuentas padre. |

## Requisitos no funcionales aplicables

- Aislamiento y consistencia de saldos: CA-008-02/03/04/05/06/07/08.

## Casos límite

- Sin movimientos, borradores, periodos anteriores y contextos no autorizados: CA-008-02/03/04/05/06/07/08.

## Fuera de alcance

No incluye balanza electrónica SAT, cierre/reapertura, migración histórica ni cálculo fiscal. Mostrar saldo inicial no autoriza a inventar su procedencia ni a implementar una migración.

## Criterios de finalización

- Los CA pendientes requieren implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §16: balanza básica](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#16-reportes-incluidos); [§20: éxito del producto](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#20-resultados-esperados-del-producto).
- [BR-001](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-017](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#19-br-017--las-p%C3%B3lizas-contabilizadas-afectan-la-balanza) (confirmadas); [AC-014](../../docs/planeacion/004%20-%20Escenarios%20contables.md#16-escenario-ac-014--balanza-despu%C3%A9s-de-contabilizar).
- [OQ-012](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#14-oq-012--openingbalance), [OQ-017](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#19-oq-017--migraci%C3%B3n) (saldos externos y migración por evaluar; el saldo derivado de pólizas anteriores ya está definido arriba).
