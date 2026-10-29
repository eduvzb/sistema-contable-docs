# SPEC-005 — Descarga simulada

- **Estado:** Actualización pendiente
- **Actualizado:** 2026-10-28
- **Criterios de esta entrega:** CA-005-01/02/04 revisados y CA-005-07 añadido, coordinados con la implementación parcial controlada de SPEC-012. Cierre técnico y QA de la actualización pendientes; la QA previa no acredita estas restricciones nuevas.
- **Usuario:** Administrador para ejecutar la simulación; administrador o contador con acceso para consultar documentos ya incorporados.
- **Dependencias:** [SPEC-001](../001-acceso-usuarios-empresas/spec.md), [SPEC-002](../002-contexto-contable/spec.md), [SPEC-004](../004-documentos-fiscales/spec.md)

## Contexto y objetivo

Representar la obtención de XML mediante un servicio ficticio o controlado de pruebas internas, que el administrador inicia con advertencia y confirmación, separado de la descarga real de SPEC-012.

Incluye documentos preparados/de prueba, estados básicos del proceso e incorporación a la bandeja.

## Historias de usuario

- H-005-01: Como administrador quiero confirmar una descarga simulada y conocer el resultado, para incorporar documentos de prueba.
- H-005-02: Como contador quiero usar un documento incorporado por la simulación en el flujo de pólizas, para continuar el registro contable.

## Requisitos funcionales y criterios de aceptación

El administrador podrá iniciar la simulación en cualquier empresa con advertencia y confirmación, sin marca de empresa de pruebas. Un servicio simulado devuelve documentos preparados; la interfaz muestra el avance o resultado y los XML incorporados aparecen en la bandeja normal. La simulación reutiliza el importador de SPEC-004 sin una regla propia de duplicados o descarte de originales. Las nuevas restricciones son trabajo pendiente coordinado con SPEC-012; la versión anterior permite iniciarla también al contador asignado.

La solicitud síncrona exige un periodo de la empresa. `COMPLETED` indica que la respuesta se procesó, incluso con cero documentos o rechazos parciales; `FAILED` indica un fallo controlado antes de incorporar documentos, informa el motivo y permite reintentar. Los documentos válidos del resultado parcial permanecen incorporados.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-005-01 | El administrador elige la descarga simulada en cualquier empresa. | Se aplica CA-012-15 de SPEC-012: herramienta de pruebas internas identificada, advertencia de documentos ficticios y confirmación previa; cancelar no incorpora documentos. Al confirmar se representa la solicitud y se muestra su estado o resultado. |
| CA-005-02 | El servicio simulado devuelve XML admitidos y no existentes. | Se informa cuáles se encontraron y los incorporados aparecen en la consulta de SPEC-004, reutilizando su importador y política de originales sin una excepción de descarte para la simulación. |
| CA-005-03 | La simulación devuelve un documento que ya está en la empresa. | Se aplica el criterio CA-004-03, sin generar una segunda definición ni excepción de duplicado. |
| CA-005-04 | El contador con acceso selecciona un documento incorporado por la simulación. | Puede continuar por el mismo flujo de pólizas de SPEC-006 que con uno cargado manualmente, para los tipos permitidos por SPEC-004. No se eliminan documentos ficticios anteriores ni se altera su contabilidad por restringir quién inicia la simulación. |
| CA-005-05 | Se intenta iniciar o consultar el resultado para una empresa sin acceso. | No se incorporan ni exponen documentos de esa empresa. |
| CA-005-06 | Se ejecuta el recorrido de simulación. | No requiere credenciales fiscales ni conexión a SAT; los documentos provienen del servicio controlado. |
| CA-005-07 | Un contador accede a la bandeja o intenta ejecutar directamente la simulación, o falla la descarga real. | Se aplica CA-012-16 de SPEC-012: el contador no ve la opción y el backend impide ejecutarla. La simulación nunca sustituye automáticamente una descarga real fallida. |

## Requisitos no funcionales aplicables

- Aislamiento y reutilización de la incorporación fiscal: CA-005-02/03/05/06.

## Casos límite

- Duplicado, resultado vacío, fallo controlado, reintento y empresa ajena: CA-005-02/03/05.

## Fuera de alcance

Quedan fuera conexión SAT, certificados, credenciales fiscales, programación de sincronizaciones y errores oficiales.

## Criterios de finalización

- Los CA pendientes requieren implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

Las referencias de Planeación describen el alcance original simulado. SPEC-012 incorpora la conexión real por separado y limita la simulación a administradores; estas fuentes no sustituyen los criterios revisados ni acreditan su implementación.

- [Alcance §6: simulación y exclusiones](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#6-importaci%C3%B3n-y-obtenci%C3%B3n-de-xml).
- [BR-020](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#22-br-020--la-descarga-autom%C3%A1tica-se-simula-en-el-alcance-actual) (CONFIRMADA PARA EL ALCANCE ACTUAL); [AC-016](../../docs/planeacion/004%20-%20Escenarios%20contables.md#18-escenario-ac-016--descarga-simulada-de-xml) (DEFINIDO PARA EL ALCANCE ACTUAL).
- [Alcance §21: integración SAT fuera del alcance actual](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#21-fuera-del-alcance-actual).
