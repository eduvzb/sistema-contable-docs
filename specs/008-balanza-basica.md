# SPEC-008 — Balanza básica

**Estado:** QA
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-002](002-contexto-contable.md), [SPEC-003](003-catalogo-cuentas.md), [SPEC-006](006-polizas-trazabilidad.md)

## Propósito y alcance

Consultar por cuenta saldo inicial, cargos, abonos y saldo final del contexto contable. Las partidas de pólizas contabilizadas afectan movimientos y saldos; los borradores quedan fuera de la balanza definitiva.

No incluye balanza electrónica SAT, cierre/reapertura, migración histórica ni cálculo fiscal. Mostrar saldo inicial no autoriza a inventar su procedencia ni a implementar una migración.

## Fuentes

- [Alcance §16: balanza básica](../docs/planeacion/003%20-%20MVP-Scope.md#16-reportes-incluidos); [§20: éxito del MVP](../docs/planeacion/003%20-%20MVP-Scope.md#20-criterios-de-%C3%A9xito-del-mvp).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-017](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#19-br-017--las-p%C3%B3lizas-contabilizadas-afectan-la-balanza) (confirmadas); [AC-014](../docs/planeacion/004%20-%20Escenarios%20contables.md#16-escenario-ac-014--balanza-despu%C3%A9s-de-contabilizar) (necesidad confirmada; presentación según naturaleza pendiente).
- [OQ-012](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#14-oq-012--openingbalance), [OQ-017](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#19-oq-017--migraci%C3%B3n) (saldos iniciales/migración pendientes y posteriores al primer recorrido).

## Contexto de ejecución

**Modo actual:** QA. La implementación y las comprobaciones técnicas están completas; usar esta spec para validar visualmente lectura, importes, estados vacíos y correspondencia con el periodo seleccionado.

**Paquete funcional:** esta spec contiene el alcance autoritativo de saldo inicial, cargos, abonos, saldo final, inclusión de partidas POSTED, exclusión de borradores y criterios CA-008-01 a CA-008-05. No ampliar el alcance a balanza SAT, migración ni cierre.

**Dependencias y fuentes consolidadas:** consultar SPEC-002, SPEC-003 y SPEC-006 para contexto, cuentas y pólizas. Las fuentes enlazadas arriba y las decisiones/contratos de esta spec ya están consolidados; no recargarlos durante una ejecución normal si no cambiaron.

**Reabrir fuentes cuando:** cambie un contrato de dependencia, se defina la procedencia del saldo inicial, aparezca una contradicción o el usuario solicite migración, cierre o tratamiento fiscal.

## Comportamiento y criterios de aceptación

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

## Pendientes y decisiones

- **Resuelto para este alcance:** el saldo inicial no proviene de `OpeningBalance`: es el saldo acumulado de las partidas de pólizas `POSTED` pertenecientes a periodos anteriores de la misma empresa, ordenados por `(year, month)`. En el primer periodo sin historial, el resultado observable es cero, sin persistir un saldo inicial inventado.
- **Resuelto para este alcance:** cada cuenta se presenta como una fila independiente; no se agregan cuentas padre ni se muestran subtotales jerárquicos. Se incluyen todas las cuentas del catálogo de la empresa, incluso sin movimiento, para que una consulta no oculte cuentas existentes.
- **Resuelto para este alcance:** el saldo usa la naturaleza de la cuenta. Para `DEBIT`, `saldo = cargos - abonos`; para `CREDIT`, `saldo = abonos - cargos`. El saldo inicial y final pueden ser negativos cuando el movimiento neto queda del lado contrario. El saldo final es el saldo inicial más el movimiento neto del periodo.
- **Resuelto para este alcance:** los importes usan seis decimales, se calculan como `numeric` en PostgreSQL y se serializan como texto con exactamente seis decimales; no se redondean con punto flotante.
- **Fuera de este alcance:** `OpeningBalance`, migración histórica, cierres, reaperturas, balanza electrónica SAT y conversión monetaria.
- **Validación durante MVP:** lectura de saldos por cuenta y correspondencia con las pólizas que el contador registró.
- **Posterior:** carga/migración histórica y diseño completo de saldos iniciales, balanza fiscal, cierre y reapertura. La definición mínima para una balanza verificable sí debe quedar preparada.

## Plan técnico y contratos

- Backend: `GET /api/companies/{companyId}/accounting-periods/{periodId}/trial-balance`, protegido por Sanctum y la misma visibilidad de empresa de las demás funciones. Devuelve `{ data, meta }`; `data` contiene una fila por cuenta con `account_id`, `code`, `name`, `nature`, `accepts_entries`, `active`, `opening_balance`, `debit_total`, `credit_total` y `closing_balance`. Todos los importes son textos de seis decimales. `meta` identifica `company_id`, `accounting_period_id`, `year`, `month` y `decimal_scale: 6`.
- El cálculo consulta únicamente partidas de pólizas `POSTED` de la empresa y periodo correspondiente. Las partidas de `DRAFT`, otras empresas y periodos posteriores quedan fuera. La consulta es agregada por cuenta y no duplica partidas por relaciones con CFDI.
- Frontend: el espacio de trabajo consulta este endpoint cuando existe un periodo seleccionado y presenta la balanza en una vista propia; el contexto de empresa y periodo sigue siendo explícito.
- SPEC-009 consumirá este mismo contrato, sin repetir el cálculo ni crear otra fuente de saldos.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). Los contratos de este alcance quedan cerrados para la implementación descrita; cualquier ampliación de saldos iniciales o agregación deberá actualizar esta spec antes de implementarse.

## Verificación

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

La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental); la implementación queda en los árboles backend y frontend indicados por el estado de continuidad.

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el cálculo pendiente de balanza.
- **2026-09-08:** se cerró el alcance mínimo: saldo inicial derivado de periodos anteriores, saldo por naturaleza, filas sin movimiento sin agregados jerárquicos, seis decimales como texto y contrato `trial-balance`. La spec queda Lista y su implementación mínima está añadida; `OpeningBalance` y migración permanecen fuera del MVP.
- **2026-09-10:** se reclasificó como QA conforme a DP-004; sólo resta validación visual humana del recorrido preparado.
