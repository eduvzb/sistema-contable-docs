# SPEC-008 — Balanza básica

- **Estado:** QA
- **Actualizado:** 2026-09-24 (migración documental; sin cambio de estado)
- **Criterios de esta entrega:** Sin tareas técnicas abiertas; resta QA humana.
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-002](../002-contexto-contable/spec.md), [SPEC-003](../003-catalogo-cuentas/spec.md), [SPEC-006](../006-polizas-trazabilidad/spec.md)

## Contexto y objetivo

Consultar por cuenta saldo inicial, cargos, abonos y saldo final del contexto contable. Las partidas de pólizas contabilizadas afectan movimientos y saldos; los borradores quedan fuera de la balanza definitiva.

## Historias de usuario

- H-008-01: Como contador quiero consultar saldos y movimientos por cuenta en el periodo seleccionado, para revisar la balanza básica.

## Requisitos funcionales y criterios de aceptación

El usuario operativo consulta la balanza de una empresa accesible y periodo; el administrador accede a cualquiera y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. La consulta recorre las cuentas afectadas por pólizas POSTED. La presentación debe mostrar los cuatro componentes definidos en alcance §16. AC-014 usa saldo inicial + cargos − abonos como esquema conceptual y advierte que la presentación depende de la naturaleza de las cuentas; no se convierte ese ejemplo en una fórmula universal.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-008-01 | Se consulta la balanza del contexto con datos válidos preparados. | Se muestran cuenta, saldo inicial, cargos, abonos y saldo final conforme a la definición pendiente de presentación. |
| CA-008-02 | Existen pólizas POSTED del contexto. | Sus partidas se reflejan en los movimientos de las cuentas correspondientes. |
| CA-008-03 | Existe una póliza DRAFT con partidas, balanceadas o desbalanceadas. | Sus partidas no afectan la balanza definitiva. |
| CA-008-04 | Una póliza pasa de DRAFT a POSTED conforme a SPEC-006. | La balanza refleja el efecto de sus partidas contabilizadas al volver a consultarla, sin duplicar ese efecto por consultas repetidas. |
| CA-008-05 | Se consulta empresa A teniendo también acceso a B. | La balanza de A no mezcla cuentas ni movimientos de B; un usuario sin acceso a A tampoco puede consultarla. |
| CA-008-06 | Una factura origina pólizas en julio y agosto. | Cada póliza conserva su periodo; los movimientos de cada consulta respetan ese periodo. El saldo inicial de agosto incluye el efecto `POSTED` de julio, pero el movimiento de agosto solo incluye sus propias partidas. |
| CA-008-07 | Un usuario consulta una empresa no asignada o un periodo de otra empresa. | La respuesta es `404` y no revela cuentas ni movimientos del contexto ajeno. |
| CA-008-08 | Una cuenta no tiene movimientos `POSTED` en ningún periodo o en el periodo consultado. | La cuenta aparece una sola vez con importes en cero, sin crear agregados de cuentas padre. |

## Requisitos no funcionales aplicables

- Aislamiento y consistencia de saldos: CA-008-02/03/04/05/06/07/08.

## Casos límite

- Sin movimientos, borradores, periodos anteriores y contextos no autorizados: CA-008-02/03/04/05/06/07/08.

## Fuera de alcance

No incluye balanza electrónica SAT, cierre/reapertura, migración histórica ni cálculo fiscal. Mostrar saldo inicial no autoriza a inventar su procedencia ni a implementar una migración.

## Decisiones, supuestos y dudas

### Pendientes y decisiones

- **Resuelto para este alcance:** el saldo inicial no proviene de `OpeningBalance`: es el saldo acumulado de las partidas de pólizas `POSTED` pertenecientes a periodos anteriores de la misma empresa, ordenados por `(year, month)`. En el primer periodo sin historial, el resultado observable es cero, sin persistir un saldo inicial inventado.
- **Resuelto para este alcance:** cada cuenta se presenta como una fila independiente; no se agregan cuentas padre ni se muestran subtotales jerárquicos. Se incluyen todas las cuentas del catálogo de la empresa, incluso sin movimiento, para que una consulta no oculte cuentas existentes.
- **Resuelto para este alcance:** el saldo usa la naturaleza de la cuenta. Para `DEBIT`, `saldo = cargos - abonos`; para `CREDIT`, `saldo = abonos - cargos`. El saldo inicial y final pueden ser negativos cuando el movimiento neto queda del lado contrario. El saldo final es el saldo inicial más el movimiento neto del periodo.
- **Resuelto para este alcance:** los importes usan seis decimales, se calculan como `numeric` en PostgreSQL y se serializan como texto con exactamente seis decimales; no se redondean con punto flotante.
- **Fuera de este alcance:** `OpeningBalance`, migración histórica, cierres, reaperturas, balanza electrónica SAT y conversión monetaria.
- **Validación durante MVP:** lectura de saldos por cuenta y correspondencia con las pólizas que el contador registró.
- **Posterior:** carga/migración histórica y diseño completo de saldos iniciales, balanza fiscal, cierre y reapertura. La definición mínima para una balanza verificable sí debe quedar preparada.

## Criterios de finalización

- Los criterios de esta entrega deben tener implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §16: balanza básica](../../docs/planeacion/003%20-%20MVP-Scope.md#16-reportes-incluidos); [§20: éxito del MVP](../../docs/planeacion/003%20-%20MVP-Scope.md#20-criterios-de-%C3%A9xito-del-mvp).
- [BR-001](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-017](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#19-br-017--las-p%C3%B3lizas-contabilizadas-afectan-la-balanza) (confirmadas); [AC-014](../../docs/planeacion/004%20-%20Escenarios%20contables.md#16-escenario-ac-014--balanza-despu%C3%A9s-de-contabilizar) (necesidad confirmada; presentación según naturaleza pendiente).
- [OQ-012](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#14-oq-012--openingbalance), [OQ-017](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#19-oq-017--migraci%C3%B3n) (saldos iniciales/migración pendientes y posteriores al primer recorrido).
