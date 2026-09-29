# SPEC-003 — Catálogo de cuentas

- **Estado:** QA
- **Actualizado:** 2026-09-24
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

El usuario operativo administra las cuentas de una empresa accesible y las deja disponibles para captura manual de partidas en SPEC-006. El administrador accede a cualquiera y el contador solo a sus asignadas, conforme a SPEC-001. La jerarquía no define por sí sola qué niveles pueden recibir movimientos.

Una cuenta contiene código único por empresa de hasta 64 caracteres, nombre, naturaleza `DEBIT|CREDIT`, padre opcional de la misma empresa, `accepts_entries` y estado activo. Una cuenta inactiva o agrupadora permanece consultable, pero no puede usarse en nuevas partidas. Tras la primera partida, código, naturaleza y padre no se editan; nombre y estado sí.

La importación acepta CSV UTF-8 con encabezado `code,name,nature,parent_code,accepts_entries,active`. Usa `DEBIT|CREDIT` y booleanos `true|false`; el padre puede aparecer antes o después de la fila hija. Un error de fila, duplicado, padre inexistente o ciclo rechaza todo el lote e informa las filas afectadas.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-003-01 | Se crea una cuenta con código, nombre, naturaleza, padre opcional, `accepts_entries` y estado válidos. | Queda en el catálogo de la empresa seleccionada y puede consultarse. |
| CA-003-02 | Se edita una cuenta existente de la empresa. | Se muestran los datos actualizados; la cuenta conserva su pertenencia empresarial. |
| CA-003-03 | Se activa o desactiva una cuenta. | Su condición se conserva y es consultable; una cuenta inactiva no puede elegirse para nuevas partidas, sin alterar movimientos históricos. |
| CA-003-04 | Se importa un CSV UTF-8 válido con el encabezado definido arriba. | Las cuentas quedan disponibles en el catálogo de la empresa, incluyendo padres e hijas sin depender del orden de las filas. |
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

## Criterios de finalización

- Los CA pendientes requieren implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §8: catálogo](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#8-cat%C3%A1logo-de-cuentas).
- [BR-001](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-003](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#5-br-003--cada-empresa-tiene-su-propio-cat%C3%A1logo-de-cuentas), [BR-004](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#6-br-004--cada-partida-utiliza-una-cuenta-contable) (confirmadas).
- [OQ-001](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#3-oq-001--jerarqu%C3%ADa-de-cuentas-contables) (jerarquía de cuentas); [OQ-017](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#19-oq-017--migraci%C3%B3n) (migración completa posterior).
