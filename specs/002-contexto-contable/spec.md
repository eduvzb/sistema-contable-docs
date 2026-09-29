# SPEC-002 — Contexto contable

- **Estado:** QA
- **Actualizado:** 2026-09-24
- **Criterios de esta entrega:** Sin tareas técnicas abiertas; resta QA humana.
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-001](../001-acceso-usuarios-empresas/spec.md)

## Contexto y objetivo

Permitir seleccionar empresa, ejercicio y mes para operar y consultar información contable en un contexto identificable. Toda póliza pertenece a empresa, ejercicio y periodo; cuentas, documentos y saldos mantienen el aislamiento de su empresa. El cambio de contexto conserva la continuidad de navegación y comunica la carga sin saltos que hagan parecer vacío o mezclado el espacio de trabajo.

El catálogo pertenece a la empresa y no se duplica por mes.

## Historias de usuario

- H-002-01: Como usuario operativo quiero elegir empresa, ejercicio y periodo, para trabajar en el contexto contable correcto.
- H-002-02: Como usuario operativo quiero cambiar de contexto sin perder la continuidad de navegación, para seguir la tarea que estaba realizando.

## Requisitos funcionales y criterios de aceptación

El usuario operativo elige una empresa accesible y un ejercicio/mes. El administrador puede elegir cualquiera; el contador, solo una asignada, conforme a SPEC-001. Cualquier usuario con acceso a la empresa puede habilitar explícitamente un ejercicio; se crean sus doce meses en estado `OPEN`. No se crean periodos por la fecha actual ni al registrar una empresa.

El contexto se identifica por empresa y periodo en la URL y en los contratos API. El frontend puede recordar el último contexto válido en almacenamiento local, pero siempre lo comprueba de nuevo contra el backend. Las operaciones posteriores reciben el contexto explícito; seleccionar otro no reasigna información histórica y cada funcionalidad conserva su autorización.

El estado de navegación no autoritativo —como la pestaña activa, la página actual de una lista y sus filtros— se conserva mientras siga siendo válido para la misma empresa y vista. No sustituye la validación del contexto ni permite reutilizar datos de una empresa o periodo anterior como si pertenecieran al nuevo contexto.

Habilitar un ejercicio de cuatro dígitos crea de forma atómica sus doce meses `OPEN`, una sola vez por empresa. `OPEN` y `CLOSED` pueden seleccionarse; este alcance no ofrece una operación de cierre o reapertura ni bloquea acciones por el estado. Un contexto inexistente, ajeno o revocado se trata como no encontrado.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-002-01 | Un usuario selecciona una empresa accesible, ejercicio y mes. | La interfaz identifica el contexto seleccionado para continuar el trabajo. |
| CA-002-02 | Se consulta la información de otra empresa sin tener acceso. | No se exponen ni mezclan sus datos, aunque la petición manipule identificadores de contexto. |
| CA-002-03 | Se registra una póliza mediante SPEC-006 dentro del contexto seleccionado. | Conserva empresa, ejercicio y periodo según BR-002. |
| CA-002-04 | Se cambia el contexto de empresa A a empresa B. | La consulta y acciones siguientes utilizan B; los registros históricos de A permanecen asociados a A. |
| CA-002-05 | Se consulta una póliza de un periodo y luego se selecciona otro. | El periodo propio de la póliza se conserva; no se reasigna por el cambio de selección. |
| CA-002-06 | Se opera en agosto sobre información contable de julio. | Se puede seleccionar julio como contexto; el mes de la sesión no lo reemplaza automáticamente. Cada funcionalidad aplica sus propias reglas sobre fechas de documentos y pólizas. |
| CA-002-07 | Desde una vista con datos se cambia a otro periodo. | La región de contenido mantiene una estructura estable y muestra una transición de carga identificable; no presenta por un instante datos, estados vacíos ni acciones del periodo anterior como si correspondieran al nuevo, y evita saltos de disposición perceptibles. |
| CA-002-08 | El usuario cambia de periodo, recarga o navega hacia atrás/adelante dentro de la misma empresa. | Se recuperan la pestaña activa y el estado de consulta compatible, incluida la página actual cuando continúa existiendo. Si una página deja de ser válida, se ajusta a una página existente y se muestra el resultado sin perder silenciosamente el contexto. |
| CA-002-09 | El usuario abre el selector de empresa y busca entre sus empresas accesibles. | Puede filtrar por razón social o RFC, sin distinguir mayúsculas/minúsculas ni acentos en el nombre, recorrer los resultados con teclado o puntero y seleccionar una empresa. La lista informa cuando no hay coincidencias; limpiar la búsqueda vuelve a mostrar todas las empresas accesibles. Buscar o abrir el control no cambia el contexto hasta que el usuario selecciona una empresa. |

## Requisitos no funcionales aplicables

- Aislamiento y contexto explícito: CA-002-02/03/04/05; continuidad y operación accesible del selector: CA-002-07/08/09.

## Casos límite

- Contexto ausente, inexistente, ajeno o retirado; cambios durante carga: CA-002-04/05/07/08/09.

## Fuera de alcance

No incluye el flujo formal de cierre/reapertura ni reglas inventadas para periodos cerrados.

## Criterios de finalización

- Los CA pendientes requieren implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §4: empresas](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#4-empresas); [§5: periodos](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#5-periodos-contables).
- [BR-001](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-002](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#4-br-002--el-contador-trabaja-dentro-de-un-periodo), [BR-003](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#5-br-003--cada-empresa-tiene-su-propio-cat%C3%A1logo-de-cuentas) (confirmadas).
- [OQ-016](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#18-oq-016--reglas-de-cierre-y-reapertura) (cierre formal posterior); [Análisis §7: periodos](../../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#7-periodos-contables).
