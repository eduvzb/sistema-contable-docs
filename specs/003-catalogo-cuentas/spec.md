# SPEC-003 — Catálogo de cuentas

- **Estado:** QA
- **Actualizado:** 2026-09-24 (migración documental; sin cambio de estado)
- **Criterios de esta entrega:** Sin tareas técnicas abiertas; resta QA humana.
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-001](../001-acceso-usuarios-empresas/spec.md), [SPEC-002](../002-contexto-contable/spec.md)

## Contexto y objetivo

Administrar el catálogo propio de cada empresa: consultar, localizar eficientemente, crear, editar, activar/desactivar cuentas e importar un catálogo inicial. Representar jerarquía conforme a OQ-001, sin fijar un máximo de niveles no documentado.

La importación inicial del catálogo sí está dentro del alcance.

## Historias de usuario

- H-003-01: Como usuario operativo quiero mantener el catálogo de mi empresa, para disponer de cuentas válidas al registrar partidas.
- H-003-02: Como usuario operativo quiero buscar cuentas y entender su jerarquía, para localizar la cuenta adecuada.

## Requisitos funcionales y criterios de aceptación

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
| CA-003-11 | El usuario busca una cuenta por una parte de su código o nombre. | El catálogo muestra las coincidencias sin distinguir mayúsculas ni acentos, informa cuántas encontró y conserva los ancestros necesarios para entender la jerarquía de cada resultado. |
| CA-003-12 | La búsqueda no tiene coincidencias o el usuario la limpia. | Se muestra un estado vacío específico con una acción clara para limpiar; al limpiar se restaura el catálogo y el foco permite continuar la búsqueda sin navegación innecesaria. |

## Requisitos no funcionales aplicables

- Aislamiento y consistencia de jerarquía: CA-003-06/07/08/09/10; búsqueda operable: CA-003-11/12.

## Casos límite

- Cuentas duplicadas, ciclos, padres ajenos, importaciones inválidas y búsqueda vacía: CA-003-06/07/08/09/12.

## Fuera de alcance

No incluye mapeo automático al catálogo SAT, patrones ni migración histórica.

## Decisiones, supuestos y dudas

### Decisiones y pendientes

- Una cuenta conserva código de hasta 64 caracteres, nombre, naturaleza `DEBIT|CREDIT`, padre opcional, `accepts_entries` y estado activo. El código se recorta y es único dentro de la empresa; no se impone una máscara contable no documentada.
- La jerarquía usa una referencia padre de la misma empresa, sin máximo de niveles. Se rechazan cuenta propia, padre ajeno y ciclos. `accepts_entries` distingue cuentas agrupadoras de cuentas seleccionables sin deducirlo de su nivel.
- Las cuentas inactivas o con `accepts_entries=false` permanecen consultables, pero SPEC-006 debe rechazarlas en nuevas partidas. Las relaciones y movimientos históricos se conservan.
- Una cuenta sin partidas puede editar todos sus campos. Cuando SPEC-006 registre la primera partida, código, naturaleza y padre quedan protegidos; nombre y estado siguen editables. CA-003-06/10 se integran y verifican allí.
- La importación inicial usa CSV UTF-8 con encabezado exacto `code,name,nature,parent_code,accepts_entries,active`. Naturaleza acepta `DEBIT|CREDIT`; booleanos aceptan `true|false`. El padre puede existir previamente o estar en el mismo archivo, sin depender del orden de filas.
- La importación es síncrona y atómica. Rechaza encabezados, filas, códigos repetidos dentro del archivo o ya existentes, padres inexistentes y ciclos; devuelve errores identificados por fila y no escribe parcialmente.
- La búsqueda del catálogo opera sobre código y nombre del catálogo ya autorizado, tolera diferencias de mayúsculas y acentos, conserva la estructura jerárquica de los resultados y puede limpiarse con una acción explícita. No modifica cuentas ni requiere seleccionar un periodo.
- El término de búsqueda y el filtro de estado forman parte de la continuidad de interfaz definida en SPEC-002. Cambiar de periodo no los elimina porque el catálogo pertenece a la empresa; cambiar de empresa no reutiliza resultados de la anterior.
- **Supuesto para validar:** jerarquía sin máximo de niveles fijado, OQ-001. La observación del catálogo real puede ajustar estos campos mediante esta misma spec.
- **Posterior:** catálogo SAT automático, migración de pólizas/saldos históricos y reglas de selección automática.

## Criterios de finalización

- Los criterios de esta entrega deben tener implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §8: catálogo](../../docs/planeacion/003%20-%20MVP-Scope.md#8-cat%C3%A1logo-de-cuentas).
- [BR-001](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-003](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#5-br-003--cada-empresa-tiene-su-propio-cat%C3%A1logo-de-cuentas), [BR-004](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#6-br-004--cada-partida-utiliza-una-cuenta-contable) (confirmadas).
- [OQ-001](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#3-oq-001--jerarqu%C3%ADa-de-cuentas-contables) (jerarquía provisional); [OQ-017](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#19-oq-017--migraci%C3%B3n) (migración completa posterior).
