# SPEC-002 — Contexto contable

**Estado:** Lista
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-001](001-acceso-usuarios-empresas.md)

## Propósito y alcance

Permitir seleccionar empresa, ejercicio y mes para operar y consultar información contable en un contexto identificable. Toda póliza pertenece a empresa, ejercicio y periodo; cuentas, documentos y saldos mantienen el aislamiento de su empresa.

No incluye el flujo formal de cierre/reapertura ni reglas inventadas para periodos cerrados. El catálogo pertenece a la empresa, no se duplica por mes.

## Fuentes

- [Alcance §4: empresas](../docs/planeacion/003%20-%20MVP-Scope.md#4-empresas); [§5: periodos](../docs/planeacion/003%20-%20MVP-Scope.md#5-periodos-contables).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-002](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#4-br-002--el-contador-trabaja-dentro-de-un-periodo), [BR-003](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#5-br-003--cada-empresa-tiene-su-propio-cat%C3%A1logo-de-cuentas) (confirmadas).
- [OQ-016](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#18-oq-016--reglas-de-cierre-y-reapertura) (cierre formal posterior); [Análisis §7: periodos](../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#7-periodos-contables).

## Comportamiento y criterios de aceptación

El usuario operativo elige una empresa accesible y un ejercicio/mes. El administrador puede elegir cualquiera; el contador, solo una asignada, conforme a DT-008/SPEC-001. Cualquier usuario con acceso a la empresa puede habilitar explícitamente un ejercicio; se crean sus doce meses en estado `OPEN`. No se crean periodos por la fecha actual ni al registrar una empresa.

El contexto se identifica por empresa y periodo en la URL y en los contratos API conforme a DT-010. El frontend puede recordar el último contexto válido en almacenamiento local, pero siempre lo comprueba de nuevo contra el backend. Las operaciones posteriores reciben el contexto explícito; seleccionar otro no reasigna información histórica y cada funcionalidad conserva su autorización.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-002-01 | Un usuario selecciona una empresa accesible, ejercicio y mes. | La interfaz identifica el contexto seleccionado para continuar el trabajo. |
| CA-002-02 | Se consulta la información de otra empresa sin tener acceso. | No se exponen ni mezclan sus datos, aunque la petición manipule identificadores de contexto. |
| CA-002-03 | Se registra una póliza mediante SPEC-006 dentro del contexto seleccionado. | Conserva empresa, ejercicio y periodo según BR-002. |
| CA-002-04 | Se cambia el contexto de empresa A a empresa B. | La consulta y acciones siguientes utilizan B; los registros históricos de A permanecen asociados a A. |
| CA-002-05 | Se consulta una póliza de un periodo y luego se selecciona otro. | El periodo propio de la póliza se conserva; no se reasigna por el cambio de selección. |
| CA-002-06 | Se opera en agosto sobre información contable de julio, como en el análisis §7. | Se puede seleccionar julio como contexto; el mes de la sesión no lo reemplaza automáticamente. Las reglas adicionales de fecha siguen pendientes. |

## Decisiones y pendientes

- Un ejercicio es un entero de cuatro dígitos. Habilitarlo crea atómicamente y una sola vez los meses `1` a `12`, todos `OPEN`, con unicidad por empresa, ejercicio y mes. Repetir el alta devuelve un error de validación y no cambia datos.
- `OPEN` y `CLOSED` se representan y muestran. En esta spec ambos son seleccionables y el estado no bloquea acciones; no existe operación para cambiarlo. Cierre, reapertura, permisos, bloqueos y auditoría permanecen posteriores conforme a OQ-016.
- Sin contexto, la interfaz solicita seleccionar empresa, ejercicio y mes y no supone el mes actual. Un contexto inexistente, de otra empresa o ya no accesible se trata como no encontrado; una memoria local nunca concede acceso.
- La fecha en que el usuario trabaja no cambia el periodo seleccionado. SPEC-004, SPEC-006 y SPEC-007 decidirán las reglas entre sus fechas de dominio y el periodo sin duplicarlas aquí.
- **Validación durante MVP:** utilidad de la presentación de empresa/periodo al cambiar de tarea.
- **Integración pendiente:** CA-002-03/05 se comprueban al implementar las pólizas de SPEC-006.

## Plan técnico y contratos

### Persistencia

`accounting_periods` conserva `company_id`, `year`, `month`, `status` y marcas de tiempo. Una restricción única cubre `(company_id, year, month)`; las restricciones de base de datos limitan el año a cuatro dígitos y el mes a `1..12`. El periodo pertenece a una empresa y es la referencia estable que usarán las entidades consumidoras.

### API JSON autenticada

Todas las rutas aplican la sesión Sanctum, el cambio obligatorio de contraseña y el acceso vigente a la empresa de SPEC-001.

| Operación | Resultado |
|---|---|
| `GET /api/companies/{companyId}/accounting-periods` | `200` con periodos accesibles, ordenados por ejercicio descendente y mes ascendente. |
| `GET /api/companies/{companyId}/accounting-periods/{periodId}` | `200` con el periodo cuando pertenece a la empresa accesible. |
| `POST /api/companies/{companyId}/accounting-years` con `{ "year": 2026 }` | `201` con los doce periodos creados; cualquier usuario con acceso a la empresa puede ejecutarlo. |

Cada periodo se representa como `{ id, company_id, year, month, month_name, status }`, con `status` en `OPEN|CLOSED` y nombre de mes en español. Una petición no autenticada devuelve `401`; una empresa/periodo inexistente, ajeno o no asignado devuelve `404`; año ausente, no entero o no de cuatro dígitos y ejercicio ya habilitado devuelven `422` sin escritura parcial.

### Interfaz

La empresa presenta ejercicios disponibles, sus meses y una acción para habilitar ejercicio. Elegir un periodo navega a `/companies/{companyId}/periods/{periodId}`. Esa ruta valida empresa y periodo mediante la API antes de guardar `{ company_id, period_id }` como último contexto. Una barra visible muestra razón social, ejercicio, mes y estado y permite cambiar de contexto. Un valor local inválido o revocado se elimina y regresa al selector sin mostrar datos protegidos.

Separar pertenencia empresarial de filtrado por periodo: los criterios temporales de XML se concretan en SPEC-004, los de pólizas en SPEC-006 y los de pagos en SPEC-007. Aplican las [decisiones técnicas compartidas](../docs/decisiones.md).

## Verificación

**Revisión implementada:** `2dc868a2484772db6c5fc881ff7eadab63ea059f`.

**Referencias de implementación:**

- Backend, rama `codex/spec-002`: `098ec630fdbe41ee393dd04ccd4e6505dc8ceb5d`.
- Frontend, rama `codex/spec-002`: `7f59d6c86dc3a3bb61f314d16032df21b316f593`.

**2026-09-07 — Comprobaciones ejecutadas:**

| Cobertura | Evidencia y resultado |
|---|---|
| CA-002-02; alta y consulta de periodos; errores de autenticación, contraseña temporal, año inválido/duplicado, cruce de empresa y periodo; `CLOSED` informativo | `./vendor/bin/sail artisan test --compact tests/Feature/Spec002Test.php`: 5 pruebas, 41 aserciones, aprobadas sobre PostgreSQL `testing`. |
| Regresión de SPEC-001 y SPEC-002 | `./vendor/bin/sail artisan test --compact`: 12 pruebas, 135 aserciones, aprobadas. |
| Formato y carga del backend | `./vendor/bin/sail pint --dirty --format agent`, revisión de sintaxis PHP y `php artisan route:list --path=api --except-vendor`: aprobados; las tres rutas del contrato quedaron registradas. |
| Dependencias backend | `./vendor/bin/sail composer validate --strict --no-check-publish`: válido. `./vendor/bin/sail composer audit`: sin avisos de vulnerabilidad. |
| Compilación de CA-002-01/04/06 y ruta de contexto | `pnpm lint`, `pnpm typecheck` y `pnpm build`: aprobados con Next.js 16.3.4; la compilación incluye `/companies/[id]` y `/companies/[id]/periods/[periodId]`. |

No se escribieron ni ejecutaron pruebas de SPEC-002 en navegador por instrucción explícita del usuario. La interfaz, su cambio de contexto y la memoria local no cuentan todavía con evidencia de ejecución interactiva. CA-002-03/05 permanecen pendientes hasta que SPEC-006 implemente pólizas y su pertenencia estable al periodo. Por esos pendientes, el estado continúa **Lista** y no **Implementada**.

Pendiente: comprobar interactivamente selección/cambio de contexto y verificar CA-002-03/05 con pólizas. CA-002-06 se cubre estructuralmente al no derivar el contexto de la fecha actual, pero su recorrido de usuario tampoco se declara ejecutado.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance contable.
- **2026-09-07:** preparación para implementación. Se resolvieron alta de ejercicios por cualquier usuario con acceso, doce meses persistidos, estado informativo, contexto explícito en URL, memoria local no autoritativa, contratos API y errores observables. SPEC-002 pasa a Lista por instrucción explícita del usuario.
- **2026-09-07:** se implementaron persistencia, API, autorización, selector y contexto visible; se registraron las comprobaciones sin navegador y los pendientes de integración que impiden marcar la spec como Implementada.
