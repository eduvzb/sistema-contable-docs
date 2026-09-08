# SPEC-003 — Catálogo de cuentas

**Estado:** Lista
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md)

## Propósito y alcance

Administrar el catálogo propio de cada empresa: consultar, crear, editar, activar/desactivar cuentas e importar un catálogo inicial. Representar jerarquía conforme a OQ-001, sin fijar un máximo de niveles no documentado.

No incluye mapeo automático al catálogo SAT, patrones ni migración histórica. La importación inicial del catálogo sí está dentro del alcance.

## Fuentes

- [Alcance §8: catálogo](../docs/planeacion/003%20-%20MVP-Scope.md#8-cat%C3%A1logo-de-cuentas).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-003](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#5-br-003--cada-empresa-tiene-su-propio-cat%C3%A1logo-de-cuentas), [BR-004](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#6-br-004--cada-partida-utiliza-una-cuenta-contable) (confirmadas).
- [OQ-001](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#3-oq-001--jerarqu%C3%ADa-de-cuentas-contables) (jerarquía provisional); [OQ-017](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#19-oq-017--migraci%C3%B3n) (migración completa posterior).

## Comportamiento y criterios de aceptación

El usuario operativo administra las cuentas de una empresa accesible y las deja disponibles para captura manual de partidas en SPEC-006. El administrador accede a cualquiera y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. La jerarquía no define por sí sola qué niveles pueden recibir movimientos.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-003-01 | Se crea una cuenta con los datos que defina el contrato. | Queda en el catálogo de la empresa seleccionada y puede consultarse. |
| CA-003-02 | Se edita una cuenta existente de la empresa. | Se muestran los datos actualizados; la cuenta conserva su pertenencia empresarial. |
| CA-003-03 | Se activa o desactiva una cuenta. | Su condición se conserva y es consultable; una cuenta inactiva no puede elegirse para nuevas partidas, sin alterar movimientos históricos. |
| CA-003-04 | Se importan cuentas válidas según el formato que se concrete. | Quedan disponibles en el catálogo de la empresa, incluyendo las relaciones jerárquicas representadas en el formato. |
| CA-003-05 | Se relaciona una cuenta hija con una cuenta padre conforme a OQ-001. | La jerarquía se conserva y puede consultarse sin un máximo de niveles inventado. |
| CA-003-06 | Se intenta usar en una partida de A una cuenta que pertenece a B. | La operación no permite contabilizar con la cuenta ajena, conforme a BR-003. |
| CA-003-07 | Se intenta consultar o editar el catálogo de una empresa no asignada. | El backend impide el acceso y conserva los datos. |
| CA-003-08 | Se propone como padre una cuenta ajena, inexistente, la propia cuenta o una descendiente. | Se rechaza el cambio sin crear referencias cruzadas ni ciclos. |
| CA-003-09 | Una fila del archivo de importación es inválida, duplicada o referencia un padre inexistente. | Se informa el error por fila y no se importa ninguna cuenta del lote. |
| CA-003-10 | Se edita una cuenta que ya tiene partidas. | Puede cambiar nombre y estado; código, naturaleza y padre permanecen sin cambios. |

## Decisiones y pendientes

- Una cuenta conserva código de hasta 64 caracteres, nombre, naturaleza `DEBIT|CREDIT`, padre opcional, `accepts_entries` y estado activo. El código se recorta y es único dentro de la empresa; no se impone una máscara contable no documentada.
- La jerarquía usa una referencia padre de la misma empresa, sin máximo de niveles. Se rechazan cuenta propia, padre ajeno y ciclos. `accepts_entries` distingue cuentas agrupadoras de cuentas seleccionables sin deducirlo de su nivel.
- Las cuentas inactivas o con `accepts_entries=false` permanecen consultables, pero SPEC-006 debe rechazarlas en nuevas partidas. Las relaciones y movimientos históricos se conservan.
- Una cuenta sin partidas puede editar todos sus campos. Cuando SPEC-006 registre la primera partida, código, naturaleza y padre quedan protegidos; nombre y estado siguen editables. CA-003-06/10 se integran y verifican allí.
- La importación inicial usa CSV UTF-8 con encabezado exacto `code,name,nature,parent_code,accepts_entries,active`. Naturaleza acepta `DEBIT|CREDIT`; booleanos aceptan `true|false`. El padre puede existir previamente o estar en el mismo archivo, sin depender del orden de filas.
- La importación es síncrona y atómica. Rechaza encabezados, filas, códigos repetidos dentro del archivo o ya existentes, padres inexistentes y ciclos; devuelve errores identificados por fila y no escribe parcialmente.
- **Supuesto para validar:** jerarquía sin máximo de niveles fijado, OQ-001. La observación del catálogo real puede ajustar estos campos mediante esta misma spec.
- **Posterior:** catálogo SAT automático, migración de pólizas/saldos históricos y reglas de selección automática.

## Plan técnico y contratos

### Persistencia

`accounts` conserva `company_id`, `parent_id`, `code`, `name`, `nature`, `accepts_entries`, `active` y marcas de tiempo. La base garantiza código único por empresa y padre de la misma empresa. No existe eliminación en esta spec.

### API autenticada

Todas las rutas aplican la sesión Sanctum, el cambio obligatorio de contraseña y el acceso vigente a la empresa de SPEC-001.

| Operación | Resultado |
|---|---|
| `GET /api/companies/{companyId}/accounts` | `200` con el catálogo plano ordenado por código; cada fila incluye su `parent_id` para reconstruir el árbol. |
| `POST /api/companies/{companyId}/accounts` | `201` con la cuenta creada. Requiere código, nombre y naturaleza; padre es opcional y los booleanos predeterminan `true`. |
| `PUT /api/companies/{companyId}/accounts/{accountId}` | `200` con la cuenta actualizada, conservando empresa e integridad jerárquica. |
| `POST /api/companies/{companyId}/account-imports` | `201` con `{ imported_count, accounts }` para un archivo multipart `file`; falla atómicamente con `422`. |

La representación es `{ id, company_id, parent_id, code, name, nature, accepts_entries, active }`. Peticiones no autenticadas devuelven `401`; empresa/cuenta ajena o inexistente devuelve `404`; datos, jerarquía o importación inválidos devuelven `422` sin cambios.

### Interfaz

La empresa enlaza a `/companies/{companyId}/accounts`. La pantalla muestra la jerarquía, naturaleza, capacidad de recibir movimientos y estado; permite crear, editar, activar/desactivar e importar CSV, con errores de campos o filas. El catálogo pertenece a la empresa y no cambia al seleccionar otro periodo.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). SPEC-006 consume cuentas activas que aceptan movimientos y aplica el bloqueo de estructura cuando existan partidas; SPEC-008 consume `nature` para la balanza.

## Verificación

**Revisión implementada:** `dfec655a56741b34257a80841dc9fd6933f698e2`.

**Referencias de implementación:**

- Backend, rama `codex/spec-003`: `601c75e1aa15092a8e3d7c24684f89d91f42e5bb`.
- Frontend, rama `codex/spec-003`: `552a1e64ef966684abc8b4a81dec9a65f4a02086`.

**2026-09-07 — Comprobaciones ejecutadas:**

| Cobertura | Evidencia y resultado |
|---|---|
| CA-003-01/02/04/05/07/08/09; persistencia de estado de CA-003-03; código por empresa, jerarquía, aislamiento e importación atómica | `./vendor/bin/sail artisan test --compact tests/Feature/Spec003Test.php`: 12 pruebas, 77 aserciones, aprobadas sobre PostgreSQL `testing`. |
| Regresión de SPEC-001 a SPEC-003 | `./vendor/bin/sail artisan test --compact`: 24 pruebas, 212 aserciones, aprobadas. |
| Formato, sintaxis y rutas backend | `./vendor/bin/sail pint --dirty --format agent`, revisión de sintaxis PHP y `php artisan route:list --path=api/companies --except-vendor`: aprobados; las cuatro rutas del catálogo quedaron registradas. |
| Dependencias backend | `./vendor/bin/sail composer validate --strict --no-check-publish`: válido. `./vendor/bin/sail composer audit`: sin avisos de vulnerabilidad. |
| Compilación de la interfaz | `pnpm lint`, `pnpm typecheck` y `pnpm build`: aprobados con Next.js 16.3.4; la compilación incluye `/companies/[id]/accounts`. |

No se escribieron ni ejecutaron pruebas de SPEC-003 en navegador por instrucción explícita del usuario. La jerarquía, formularios, cambio de estado e importación no cuentan todavía con evidencia interactiva. El rechazo de cuentas inactivas/agrupadoras en nuevas partidas (parte de CA-003-03), el aislamiento al registrar partidas (CA-003-06) y el bloqueo estructural después del primer uso (CA-003-10) permanecen pendientes hasta SPEC-006. Por esos pendientes, el estado continúa **Lista** y no **Implementada**.

Pendiente: comprobar interactivamente el catálogo y completar CA-003-03/06/10 con las partidas de SPEC-006.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance del catálogo.
- **2026-09-07:** preparación para implementación por autorización explícita del usuario. Se fijaron campos, naturaleza, selección de movimientos, edición de cuentas utilizadas, integridad jerárquica y CSV atómico; SPEC-003 pasa a Lista.
- **2026-09-07:** se implementaron catálogo, jerarquía, estado e importación CSV en backend/frontend; se registraron las comprobaciones sin navegador y la integración pendiente con SPEC-006.
