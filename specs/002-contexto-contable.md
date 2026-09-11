# SPEC-002 — Contexto contable

**Estado:** QA
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-001](001-acceso-usuarios-empresas.md)

## Propósito y alcance

Permitir seleccionar empresa, ejercicio y mes para operar y consultar información contable en un contexto identificable. Toda póliza pertenece a empresa, ejercicio y periodo; cuentas, documentos y saldos mantienen el aislamiento de su empresa. El cambio de contexto conserva la continuidad de navegación y comunica la carga sin saltos que hagan parecer vacío o mezclado el espacio de trabajo.

No incluye el flujo formal de cierre/reapertura ni reglas inventadas para periodos cerrados. El catálogo pertenece a la empresa, no se duplica por mes.

## Fuentes

- [Alcance §4: empresas](../docs/planeacion/003%20-%20MVP-Scope.md#4-empresas); [§5: periodos](../docs/planeacion/003%20-%20MVP-Scope.md#5-periodos-contables).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-002](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#4-br-002--el-contador-trabaja-dentro-de-un-periodo), [BR-003](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#5-br-003--cada-empresa-tiene-su-propio-cat%C3%A1logo-de-cuentas) (confirmadas).
- [OQ-016](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#18-oq-016--reglas-de-cierre-y-reapertura) (cierre formal posterior); [Análisis §7: periodos](../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#7-periodos-contables).

## Contexto de ejecución

**Modo actual:** QA. La implementación y las comprobaciones técnicas están completas; usar esta spec para validar visualmente selección, transición y recuperación de contexto según `Verificación`.

**Paquete funcional:** esta spec contiene el alcance autoritativo de empresa, ejercicio, mes, aislamiento, contexto explícito, continuidad de navegación, decisiones, contratos y criterios CA-002-01 a CA-002-08. En una actualización futura, trabajar sólo criterios nuevos o modificados.

**Dependencias y fuentes consolidadas:** consultar SPEC-001 sólo para el contrato vigente de autenticación, roles y acceso a empresas. Las fuentes enlazadas arriba y DT-008/DT-010 ya están consolidadas en este documento; no recargarlas durante una ejecución normal si no cambiaron.

**Reabrir fuentes cuando:** cambie una regla de acceso o contexto, cambie SPEC-001 o su contrato, aparezca una contradicción, se active un pendiente sobre cierre/fechas que afecte este alcance o el usuario solicite nuevo comportamiento.

## Comportamiento y criterios de aceptación

El usuario operativo elige una empresa accesible y un ejercicio/mes. El administrador puede elegir cualquiera; el contador, solo una asignada, conforme a DT-008/SPEC-001. Cualquier usuario con acceso a la empresa puede habilitar explícitamente un ejercicio; se crean sus doce meses en estado `OPEN`. No se crean periodos por la fecha actual ni al registrar una empresa.

El contexto se identifica por empresa y periodo en la URL y en los contratos API conforme a DT-010. El frontend puede recordar el último contexto válido en almacenamiento local, pero siempre lo comprueba de nuevo contra el backend. Las operaciones posteriores reciben el contexto explícito; seleccionar otro no reasigna información histórica y cada funcionalidad conserva su autorización.

El estado de navegación no autoritativo —como la pestaña activa, la página actual de una lista y sus filtros— se conserva mientras siga siendo válido para la misma empresa y vista. No sustituye la validación del contexto ni permite reutilizar datos de una empresa o periodo anterior como si pertenecieran al nuevo contexto.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-002-01 | Un usuario selecciona una empresa accesible, ejercicio y mes. | La interfaz identifica el contexto seleccionado para continuar el trabajo. |
| CA-002-02 | Se consulta la información de otra empresa sin tener acceso. | No se exponen ni mezclan sus datos, aunque la petición manipule identificadores de contexto. |
| CA-002-03 | Se registra una póliza mediante SPEC-006 dentro del contexto seleccionado. | Conserva empresa, ejercicio y periodo según BR-002. |
| CA-002-04 | Se cambia el contexto de empresa A a empresa B. | La consulta y acciones siguientes utilizan B; los registros históricos de A permanecen asociados a A. |
| CA-002-05 | Se consulta una póliza de un periodo y luego se selecciona otro. | El periodo propio de la póliza se conserva; no se reasigna por el cambio de selección. |
| CA-002-06 | Se opera en agosto sobre información contable de julio, como en el análisis §7. | Se puede seleccionar julio como contexto; el mes de la sesión no lo reemplaza automáticamente. Las reglas adicionales de fecha siguen pendientes. |
| CA-002-07 | Desde una vista con datos se cambia a otro periodo. | La región de contenido mantiene una estructura estable y muestra una transición de carga identificable; no presenta por un instante datos, estados vacíos ni acciones del periodo anterior como si correspondieran al nuevo, y evita saltos de disposición perceptibles. |
| CA-002-08 | El usuario cambia de periodo, recarga o navega hacia atrás/adelante dentro de la misma empresa. | Se recuperan la pestaña activa y el estado de consulta compatible, incluida la página actual cuando continúa existiendo. Si una página deja de ser válida, se ajusta a una página existente y se muestra el resultado sin perder silenciosamente el contexto. |

## Decisiones y pendientes

- Un ejercicio es un entero de cuatro dígitos. Habilitarlo crea atómicamente y una sola vez los meses `1` a `12`, todos `OPEN`, con unicidad por empresa, ejercicio y mes. Repetir el alta devuelve un error de validación y no cambia datos.
- `OPEN` y `CLOSED` se representan y muestran. En esta spec ambos son seleccionables y el estado no bloquea acciones; no existe operación para cambiarlo. Cierre, reapertura, permisos, bloqueos y auditoría permanecen posteriores conforme a OQ-016.
- Sin contexto, la interfaz solicita seleccionar empresa, ejercicio y mes y no supone el mes actual. Un contexto inexistente, de otra empresa o ya no accesible se trata como no encontrado; una memoria local nunca concede acceso.
- Durante un cambio de periodo, la selección de destino se hace visible de inmediato, las acciones dependientes permanecen inhabilitadas hasta validar y cargar el contexto, y la superficie reservada para cada vista conserva dimensiones suficientes para no colapsar y expandirse durante la transición.
- La continuidad de interfaz conserva como mínimo pestaña activa, página y filtros de la vista. Se limita a identificadores y preferencias de presentación: los datos contables se vuelven a obtener de los contratos autoritativos. Al cambiar de empresa se descarta cualquier estado incompatible o no autorizado.
- La fecha en que el usuario trabaja no cambia el periodo seleccionado. SPEC-004, SPEC-006 y SPEC-007 decidirán las reglas entre sus fechas de dominio y el periodo sin duplicarlas aquí.
- **Validación durante MVP:** utilidad de la presentación de empresa/periodo al cambiar de tarea.
- **Integración comprobada:** CA-002-03/05 se verifican mediante las rutas explícitas de pólizas de SPEC-006; la pertenencia de una póliza al periodo seleccionado permanece estable al cambiar de contexto.

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

El frontend conserva la pestaña y los parámetros de consulta de cada vista mediante estado de navegación recuperable, compatible con recarga e historial del navegador. Al cambiar de periodo mantiene la estructura de la vista activa, marca el destino como pendiente y reemplaza el contenido sólo cuando la validación y la consulta correspondientes terminan. No se agrega persistencia backend ni se reutilizan respuestas de otro contexto.

Separar pertenencia empresarial de filtrado por periodo: los criterios temporales de XML se concretan en SPEC-004, los de pólizas en SPEC-006 y los de pagos en SPEC-007. Aplican las [decisiones técnicas compartidas](../docs/decisiones.md).

## Verificación

**Revisión implementada:** `2dc868a2484772db6c5fc881ff7eadab63ea059f`.

**Referencias de implementación:**

- Backend, rama `codex/spec-002`: `098ec630fdbe41ee393dd04ccd4e6505dc8ceb5d`.
- Frontend, rama `codex/spec-002`: `7f59d6c86dc3a3bb61f314d16032df21b316f593`.
- Actualización frontend de CA-002-07/08 en el árbol de trabajo, principalmente `src/components/companies-dashboard.tsx`, `src/components/company-workspace.tsx` y `src/components/fiscal-document-inbox.tsx`; aún sin commit y, por tanto, sin nueva revisión Git.

**2026-09-07 — Comprobaciones ejecutadas:**

| Cobertura | Evidencia y resultado |
|---|---|
| CA-002-02; alta y consulta de periodos; errores de autenticación, contraseña temporal, año inválido/duplicado, cruce de empresa y periodo; `CLOSED` informativo | `./vendor/bin/sail artisan test --compact tests/Feature/Spec002Test.php`: 5 pruebas, 41 aserciones, aprobadas sobre PostgreSQL `testing`. |
| Regresión de SPEC-001 y SPEC-002 | `./vendor/bin/sail artisan test --compact`: 12 pruebas, 135 aserciones, aprobadas. |
| Formato y carga del backend | `./vendor/bin/sail pint --dirty --format agent`, revisión de sintaxis PHP y `php artisan route:list --path=api --except-vendor`: aprobados; las tres rutas del contrato quedaron registradas. |
| Dependencias backend | `./vendor/bin/sail composer validate --strict --no-check-publish`: válido. `./vendor/bin/sail composer audit`: sin avisos de vulnerabilidad. |
| Compilación de CA-002-01/04/06 y ruta de contexto | `pnpm lint`, `pnpm typecheck` y `pnpm build`: aprobados con Next.js 16.3.4; la compilación incluye `/companies/[id]` y `/companies/[id]/periods/[periodId]`. |
| CA-002-03/05; pertenencia estable de póliza al contexto explícito y aislamiento al cambiar de periodo | `tests/Feature/Spec002Test.php::test_policy_creation_keeps_its_explicit_period_when_the_context_changes`: pasa; creación DRAFT por empresa/periodo, consulta en el periodo original y ausencia en el periodo siguiente. |
| Regresión backend posterior a la integración | `./vendor/bin/sail artisan test --compact`: pasa el 2026-09-08 con 62 pruebas y 544 aserciones. |
| CA-002-01/02/04; validación autoritativa del contexto en frontend | La carga protegida queda suspendida hasta validar `GET /api/companies/{companyId}/accounting-periods/{periodId}`; un `periodId` malformado, ajeno, inexistente o revocado se retira de la URL y de la memoria local, y se vuelve al selector. `pnpm lint`, `pnpm build` y `pnpm typecheck` pasan. |
| Regresión completa posterior a la corrección de continuidad | `./vendor/bin/sail artisan test --compact`: 72 pruebas y 650 aserciones aprobadas; las 31 rutas API se listaron correctamente. |

La evidencia técnica anterior conserva validez y CA-002-03/05 están comprobados por backend.

CA-002-06 se cubre estructuralmente al no derivar el contexto de la fecha actual. CA-002-07/08 fueron preparados documentalmente el 2026-09-10 y su cierre técnico se documenta a continuación.

**2026-09-10 — Cierre técnico de la actualización:**

| Cobertura | Evidencia y resultado |
|---|---|
| CA-002-07 | La interfaz muestra el periodo destino desde el listado de la empresa, conserva una región de contenido con altura mínima y presenta `Validando periodo contable…`; las acciones de pólizas quedan inhabilitadas y no se montan datos del periodo anterior mientras la validación autoritativa está pendiente. Cambios en `src/components/company-workspace.tsx`. |
| CA-002-08 | `tab`, `year`, `catalogSearch`, `catalogStatus`, `documentSearch` y `documentDirection` se leen y escriben en la URL. La navegación entre periodos conserva esos valores dentro de la misma empresa, el cambio de empresa los descarta y `push` permite recuperación con historial. Cambios en `src/components/companies-dashboard.tsx`, `src/components/company-workspace.tsx` y `src/components/fiscal-document-inbox.tsx`. |
| Regresión y compilación frontend | `pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check`: aprobados. La compilación terminó correctamente con Next.js 16.3.4. |

No se modificó el backend; la evidencia histórica de sus contratos, autorización, aislamiento y pertenencia explícita de pólizas conserva validez. No se ejecutó una comprobación integral de interfaz por navegador conforme a DP-004.

La spec pasa a **QA**: validar visualmente selección y transición de periodo, ausencia de datos/acciones del contexto anterior, recuperación de tab y filtros tras recarga e historial, y ajuste de la vista al regresar a una página válida. Sólo la aprobación humana registrada permite marcarla como Implementada.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance contable.
- **2026-09-07:** preparación para implementación. Se resolvieron alta de ejercicios por cualquier usuario con acceso, doce meses persistidos, estado informativo, contexto explícito en URL, memoria local no autoritativa, contratos API y errores observables. SPEC-002 pasa a Lista por instrucción explícita del usuario.
- **2026-09-07:** se implementaron persistencia, API, autorización, selector y contexto visible; se registraron las comprobaciones técnicas y los pendientes de integración.
- **2026-09-08:** se comprobó la integración con las pólizas ya implementadas: la creación conserva empresa/periodo explícitos y el cambio de contexto no reasigna ni mezcla pólizas.
- **2026-09-08:** se reforzó el frontend para validar el periodo contra el backend antes de montar pólizas, balanza o documentos; los contextos inválidos se olvidan y regresan al selector sin usar el almacenamiento local como autorización.
- **2026-09-10:** por observación explícita del usuario se prepararon CA-002-07/08: transición estable al cambiar periodo y conservación recuperable de pestaña, página y filtros compatibles. Se reclasificó como Actualización pendiente; no se modificó código ni se registró evidencia de implementación.
- **2026-09-10:** se implementaron CA-002-07/08 en el frontend: transición estable con contexto destino pendiente, acciones dependientes bloqueadas y estado de navegación recuperable en URL; `pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check` pasaron. Conforme a DP-004, la spec pasa a QA y la validación visual queda a cargo de una persona.
