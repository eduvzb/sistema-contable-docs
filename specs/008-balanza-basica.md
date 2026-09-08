# SPEC-008 — Balanza básica

**Estado:** Borrador  
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-002](002-contexto-contable.md), [SPEC-003](003-catalogo-cuentas.md), [SPEC-006](006-polizas-trazabilidad.md)

## Propósito y alcance

Consultar por cuenta saldo inicial, cargos, abonos y saldo final del contexto contable. Las partidas de pólizas contabilizadas afectan movimientos y saldos; los borradores quedan fuera de la balanza definitiva.

No incluye balanza electrónica SAT, cierre/reapertura, migración histórica ni cálculo fiscal. Mostrar saldo inicial no autoriza a inventar su procedencia ni a implementar una migración.

## Fuentes

- [Alcance §16: balanza básica](../docs/planeacion/003%20-%20MVP-Scope.md#16-reportes-incluidos); [§20: éxito del MVP](../docs/planeacion/003%20-%20MVP-Scope.md#20-criterios-de-%C3%A9xito-del-mvp).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-017](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#19-br-017--las-p%C3%B3lizas-contabilizadas-afectan-la-balanza) (confirmadas); [AC-014](../docs/planeacion/004%20-%20Escenarios%20contables.md#16-escenario-ac-014--balanza-despu%C3%A9s-de-contabilizar) (necesidad confirmada; presentación según naturaleza pendiente).
- [OQ-012](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#14-oq-012--openingbalance), [OQ-017](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#19-oq-017--migraci%C3%B3n) (saldos iniciales/migración pendientes y posteriores al primer recorrido).

## Comportamiento y criterios de aceptación

El usuario operativo consulta la balanza de una empresa accesible y periodo; el administrador accede a cualquiera y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. La consulta recorre las cuentas afectadas por pólizas POSTED. La presentación debe mostrar los cuatro componentes definidos en alcance §16. AC-014 usa saldo inicial + cargos − abonos como esquema conceptual y advierte que la presentación depende de la naturaleza de las cuentas; no se convierte ese ejemplo en una fórmula universal.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-008-01 | Se consulta la balanza del contexto con datos válidos preparados. | Se muestran cuenta, saldo inicial, cargos, abonos y saldo final conforme a la definición pendiente de presentación. |
| CA-008-02 | Existen pólizas POSTED del contexto. | Sus partidas se reflejan en los movimientos de las cuentas correspondientes. |
| CA-008-03 | Existe una póliza DRAFT con partidas, balanceadas o desbalanceadas. | Sus partidas no afectan la balanza definitiva. |
| CA-008-04 | Una póliza pasa de DRAFT a POSTED conforme a SPEC-006. | La balanza refleja el efecto de sus partidas contabilizadas al volver a consultarla, sin duplicar ese efecto por consultas repetidas. |
| CA-008-05 | Se consulta empresa A teniendo también acceso a B. | La balanza de A no mezcla cuentas ni movimientos de B; un usuario sin acceso a A tampoco puede consultarla. |
| CA-008-06 | Una factura origina pólizas en julio y agosto. | Cada póliza conserva su periodo; los movimientos de cada consulta respetan ese periodo. El arrastre del saldo inicial se concreta antes de Lista. |

## Pendientes y decisiones

- **Antes de Lista:** origen de saldo inicial para la demostración y relación entre periodos; naturaleza/signo de cuentas y fórmula/presentación de saldo final; jerarquía/agregación evitando doble conteo; inclusión de cuentas sin movimiento; precisión y redondeo; filtros y efecto de edición de POSTED acordado en SPEC-006. No asumir saldo inicial cero ni convertir OQ-012 en obligación de implementar OpeningBalance.
- **Validación durante MVP:** lectura de saldos por cuenta y correspondencia con las pólizas que el contador registró.
- **Posterior:** carga/migración histórica y diseño completo de saldos iniciales, balanza fiscal, cierre y reapertura. La definición mínima para una balanza verificable sí debe quedar preparada.

## Plan técnico y contratos

- Backend: define el único contrato y cálculo de balanza consumido por la pantalla y la exportación SPEC-009; usa cuentas de SPEC-003 y partidas contabilizadas de SPEC-006.
- Frontend: consulta por contexto y presentación de componentes conforme al contrato.
- Preparar ejemplos de cuentas de naturaleza distinta y movimientos entre periodos al resolver pendientes; no introducir tablas de saldos, cachés o consolidaciones por anticipación.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). Los contratos aún no están cerrados: resolver los detalles necesarios antes de Lista, sin introducir reglas para completar huecos.

## Verificación

**Evidencia de producto:** pendiente; no ejecutada. No existe implementación vinculada todavía.

Prever pruebas con valores decimales conocidos, POSTED/DRAFT, dos empresas y dos periodos. Agregar resultados numéricos definitivos al resolver saldo inicial, naturaleza y agregación; sin esos acuerdos no hay evidencia suficiente de correctitud de la balanza.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el cálculo pendiente de balanza.
