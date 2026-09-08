# SPEC-005 — Descarga simulada

**Estado:** Borrador  
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md), [SPEC-004](004-documentos-fiscales.md)

## Propósito y alcance

Representar la obtención automática de XML mediante un servicio ficticio o controlado, para validar cómo el contador inicia el proceso, conoce el resultado y continúa contabilizando.

Incluye documentos preparados/de prueba, estados básicos del proceso e incorporación a la bandeja. Quedan fuera conexión SAT, certificados, credenciales fiscales, programación de sincronizaciones y errores oficiales.

## Fuentes

- [Alcance §6: simulación y exclusiones](../docs/planeacion/003%20-%20MVP-Scope.md#6-importaci%C3%B3n-y-obtenci%C3%B3n-de-xml).
- [BR-020](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#22-br-020--la-descarga-autom%C3%A1tica-se-simula-en-el-mvp) (CONFIRMADA PARA MVP); [AC-016](../docs/planeacion/004%20-%20Escenarios%20contables.md#18-escenario-ac-016--descarga-simulada-de-xml) (DEFINIDO PARA MVP).
- [Alcance §21: integración SAT fuera del MVP](../docs/planeacion/003%20-%20MVP-Scope.md#21-fuera-del-mvp).

## Comportamiento y criterios de aceptación

El usuario operativo inicia una descarga para una empresa accesible; el administrador accede a cualquiera y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. Un servicio simulado devuelve documentos preparados; la interfaz muestra el avance o resultado y los XML incorporados aparecen en la bandeja normal. La simulación reutiliza SPEC-004, incluyendo conservación del original y detección de duplicados.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-005-01 | El contador inicia una descarga en una empresa accesible. | Se representa una solicitud al servicio simulado y se muestra el estado o resultado del proceso. |
| CA-005-02 | El servicio simulado devuelve XML admitidos y no existentes. | Se informa cuáles se encontraron y los incorporados aparecen en la consulta de SPEC-004. |
| CA-005-03 | La simulación devuelve un documento que ya está en la empresa. | Se aplica el criterio CA-004-03, sin generar una segunda definición ni excepción de duplicado. |
| CA-005-04 | El contador selecciona un XML incorporado por la simulación. | Puede continuar por el mismo flujo de pólizas de SPEC-006 que con un XML cargado manualmente. |
| CA-005-05 | Se intenta iniciar o consultar el resultado para una empresa sin acceso. | No se incorporan ni exponen documentos de esa empresa. |
| CA-005-06 | Se ejecuta el recorrido de simulación. | No requiere credenciales fiscales ni conexión a SAT; los documentos provienen del servicio controlado. |

## Pendientes y decisiones

- **Antes de Lista:** conjunto de documentos de prueba y su asignación a empresa/periodo; contrato del servicio ficticio; representación de estados y resultado vacío; fallo controlado y reintento; forma de mostrar resultados de incorporación parcial conforme a SPEC-004.
- **Validación durante MVP:** que el inicio, la espera/resultado y la continuidad hacia contabilización representen el proceso esperado por el contador.
- **Posterior:** autenticación SAT, certificados, sincronización periódica y catálogo de errores externos oficiales.

## Plan técnico y contratos

- Backend: servicio simulado mínimo que entrega documentos al mecanismo de incorporación definido en SPEC-004; definir aquí únicamente solicitud y resultado de la simulación.
- Frontend: acción de inicio, estado/resultado y navegación hacia la bandeja existente.
- Acordar un mecanismo de ejecución suficiente para la demostración; la representación del proceso no implica por sí sola Redis, colas ni workers.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). Los contratos aún no están cerrados: resolver los detalles necesarios antes de Lista, sin introducir reglas para completar huecos.

## Verificación

**Evidencia de producto:** pendiente; no ejecutada. No existe implementación vinculada todavía.

Prever una demostración con documentos nuevos y repetidos, controles de acceso y continuidad XML → póliza. Agregar vacío/fallo/reintento al cerrar el contrato del simulador.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance de la simulación.

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
