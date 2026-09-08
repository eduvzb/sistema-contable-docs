# SPEC-002 — Contexto contable

**Estado:** Borrador  
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

El usuario operativo elige una empresa accesible y un ejercicio/mes. El administrador puede elegir cualquiera; el contador, solo una asignada, conforme a DT-008/SPEC-001. Las operaciones posteriores usan ese contexto; seleccionar otro no reasigna información histórica. Cada funcionalidad conserva su autorización en el backend.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-002-01 | Un usuario selecciona una empresa accesible, ejercicio y mes. | La interfaz identifica el contexto seleccionado para continuar el trabajo. |
| CA-002-02 | Se consulta la información de otra empresa sin tener acceso. | No se exponen ni mezclan sus datos, aunque la petición manipule identificadores de contexto. |
| CA-002-03 | Se registra una póliza mediante SPEC-006 dentro del contexto seleccionado. | Conserva empresa, ejercicio y periodo según BR-002. |
| CA-002-04 | Se cambia el contexto de empresa A a empresa B. | La consulta y acciones siguientes utilizan B; los registros históricos de A permanecen asociados a A. |
| CA-002-05 | Se consulta una póliza de un periodo y luego se selecciona otro. | El periodo propio de la póliza se conserva; no se reasigna por el cambio de selección. |
| CA-002-06 | Se opera en agosto sobre información contable de julio, como en el análisis §7. | Se puede seleccionar julio como contexto; el mes de la sesión no lo reemplaza automáticamente. Las reglas adicionales de fecha siguen pendientes. |

## Pendientes y decisiones

- **Antes de Lista:** creación/disponibilidad de ejercicios y periodos, datos del selector, tratamiento de contexto ausente o inválido y relación entre fecha de operación y periodo. Resolver si ABIERTO/CERRADO se muestran solo como información o qué comportamiento mínimo requieren; no derivar un cierre formal de esos nombres.
- **Validación durante MVP:** utilidad de la presentación de empresa/periodo al cambiar de tarea.
- **Posterior:** permisos de cierre, bloqueos, reapertura y auditoría del cierre (OQ-016). Estos flujos no son dependencias del MVP.

## Plan técnico y contratos

- Backend: definir el contrato para consultar/seleccionar el contexto y comprobar acceso usando SPEC-001. Las operaciones de las demás specs deben recibir o resolver inequívocamente ese contexto.
- Frontend: selector de empresa/ejercicio/mes y representación visible del contexto. Preparar la forma de actualizar consultas al cambiarlo sin datos de otra empresa.
- Separar pertenencia empresarial de filtrado por periodo: los criterios temporales de XML se concretan en SPEC-004 y los de pagos en SPEC-007.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). Los contratos aún no están cerrados: resolver los detalles necesarios antes de Lista, sin introducir reglas para completar huecos.

## Verificación

**Evidencia de producto:** pendiente; no ejecutada. No existe implementación vinculada todavía.

Prever pruebas de pertenencia persistida, consultas entre empresas y cambio de contexto. Verificar CA-002-03/05 con pólizas y CA-002-06 con fechas de trabajo distintas del periodo seleccionado.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance contable.
