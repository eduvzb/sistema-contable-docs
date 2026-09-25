# SPEC-005 — Descarga simulada

- **Estado:** Actualización pendiente
- **Actualizado:** 2026-09-24 (migración documental; sin cambio de estado)
- **Criterios de esta entrega:** Continuidad de CA-005-02 y CA-005-04 con DT-013; revisar el cierre técnico indicado en la spec.
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-001](../001-acceso-usuarios-empresas/spec.md), [SPEC-002](../002-contexto-contable/spec.md), [SPEC-004](../004-documentos-fiscales/spec.md)

## Contexto y objetivo

Representar la obtención automática de XML mediante un servicio ficticio o controlado, para validar cómo el contador inicia el proceso, conoce el resultado y continúa contabilizando.

Incluye documentos preparados/de prueba, estados básicos del proceso e incorporación a la bandeja.

## Historias de usuario

- H-005-01: Como contador quiero iniciar una descarga simulada y conocer el resultado, para incorporar documentos de prueba.
- H-005-02: Como contador quiero usar un documento incorporado por la simulación en el flujo de pólizas, para continuar el registro contable.

## Requisitos funcionales y criterios de aceptación

El usuario operativo inicia una descarga para una empresa accesible; el administrador accede a cualquiera y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. Un servicio simulado devuelve documentos preparados; la interfaz muestra el avance o resultado y los XML incorporados aparecen en la bandeja normal. La simulación reutiliza SPEC-004, incluyendo descarte del original y detección de duplicados.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-005-01 | El contador inicia una descarga en una empresa accesible. | Se representa una solicitud al servicio simulado y se muestra el estado o resultado del proceso. |
| CA-005-02 | El servicio simulado devuelve XML admitidos y no existentes. | Se informa cuáles se encontraron y los incorporados aparecen en la consulta de SPEC-004. |
| CA-005-03 | La simulación devuelve un documento que ya está en la empresa. | Se aplica el criterio CA-004-03, sin generar una segunda definición ni excepción de duplicado. |
| CA-005-04 | El contador selecciona un XML incorporado por la simulación. | Puede continuar por el mismo flujo de pólizas de SPEC-006 que con un XML cargado manualmente. |
| CA-005-05 | Se intenta iniciar o consultar el resultado para una empresa sin acceso. | No se incorporan ni exponen documentos de esa empresa. |
| CA-005-06 | Se ejecuta el recorrido de simulación. | No requiere credenciales fiscales ni conexión a SAT; los documentos provienen del servicio controlado. |

## Requisitos no funcionales aplicables

- Aislamiento y reutilización de la incorporación fiscal: CA-005-02/03/05/06 y DT-013.

## Casos límite

- Duplicado, resultado vacío, fallo controlado, reintento y empresa ajena: CA-005-02/03/05 y decisiones cerradas.

## Fuera de alcance

Quedan fuera conexión SAT, certificados, credenciales fiscales, programación de sincronizaciones y errores oficiales.

## Decisiones, supuestos y dudas

### Decisiones cerradas

- La simulación es síncrona para el MVP: una solicitud devuelve el resultado final en la misma respuesta y no crea una descarga persistida ni requiere colas, Redis o workers.
- La solicitud requiere `period_id` y el periodo debe pertenecer a la empresa de la URL. El administrador puede usar cualquier empresa y el contador solo las asignadas.
- El servicio controlado prepara dos XML CFDI 4.0 deterministas por empresa/periodo: un ingreso emitido y un ingreso recibido, ambos con fecha dentro del periodo. Sus UUID se derivan de empresa, periodo y fixture, por lo que repetir la solicitud ejercita el duplicado de SPEC-004 sin contaminar otros contextos.
- La incorporación usa exactamente las reglas de SPEC-004: valida el XML y el RFC de la empresa, persiste únicamente sus datos normalizados, descarta el contenido original, procesa cada documento de forma independiente y reporta `imported`/`rejected` sin deshacer los documentos válidos.
- El contrato usa `COMPLETED` para una respuesta procesada, incluso si se encontraron cero documentos o hubo rechazos parciales, y `FAILED` para un fallo controlado del servicio antes de incorporar documentos. Un `FAILED` devuelve `message`, no incorpora documentos y permite reintentar la misma operación.

## Criterios de finalización

- Los criterios de esta entrega deben tener implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §6: simulación y exclusiones](../../docs/planeacion/003%20-%20MVP-Scope.md#6-importaci%C3%B3n-y-obtenci%C3%B3n-de-xml).
- [BR-020](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#22-br-020--la-descarga-autom%C3%A1tica-se-simula-en-el-mvp) (CONFIRMADA PARA MVP); [AC-016](../../docs/planeacion/004%20-%20Escenarios%20contables.md#18-escenario-ac-016--descarga-simulada-de-xml) (DEFINIDO PARA MVP).
- [Alcance §21: integración SAT fuera del MVP](../../docs/planeacion/003%20-%20MVP-Scope.md#21-fuera-del-mvp).
