# SPEC-005 — Descarga simulada

**Estado:** Lista
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

## Decisiones cerradas

- La simulación es síncrona para el MVP: una solicitud devuelve el resultado final en la misma respuesta y no crea una descarga persistida ni requiere colas, Redis o workers.
- La solicitud requiere `period_id` y el periodo debe pertenecer a la empresa de la URL. El administrador puede usar cualquier empresa y el contador solo las asignadas.
- El servicio controlado prepara dos XML CFDI 4.0 deterministas por empresa/periodo: un ingreso emitido y un ingreso recibido, ambos con fecha dentro del periodo. Sus UUID se derivan de empresa, periodo y fixture, por lo que repetir la solicitud ejercita el duplicado de SPEC-004 sin contaminar otros contextos.
- La incorporación usa exactamente las reglas de SPEC-004: conserva el original privado, valida el XML y el RFC de la empresa, procesa cada documento de forma independiente y reporta `imported`/`rejected` sin deshacer los archivos válidos.
- El contrato usa `COMPLETED` para una respuesta procesada, incluso si se encontraron cero documentos o hubo rechazos parciales, y `FAILED` para un fallo controlado del servicio antes de incorporar documentos. Un `FAILED` devuelve `message`, no incorpora documentos y permite reintentar la misma operación.
- El servicio ficticio se sustituye en pruebas para demostrar resultado vacío y fallo/reintento; la interfaz de usuario solo expone iniciar o reintentar y muestra el resultado, sin controles de prueba ni conexión externa.

## Plan técnico y contratos

- Backend: `POST /api/companies/{companyId}/fiscal-document-downloads/simulated` con cuerpo `{ "period_id": integer }`, protegido por Sanctum y la visibilidad de empresa vigente. El periodo se resuelve dentro de la empresa y un periodo ajeno devuelve `404`.
- La respuesta `200` tiene `{ data: { status, period_id, found_count, imported, rejected, message? } }`. `status` es `COMPLETED` o `FAILED`; `found_count` cuenta los XML entregados por el servicio; `imported` reutiliza los elementos de SPEC-004 y `rejected` contiene `{ name, errors }`. En `FAILED`, `imported` y `rejected` son colecciones vacías y `message` explica el fallo controlado.
- La implementación separa el servicio ficticio de la incorporación para que el mecanismo de SPEC-004 sea el único responsable de validación, duplicados, almacenamiento privado y resultado por archivo. No se persiste una entidad de descarga.
- Frontend: en la bandeja de SPEC-004, con periodo seleccionado, una acción `Descarga simulada` inicia la solicitud; mientras responde muestra estado de ejecución y luego muestra encontrados, incorporados y rechazados. En `FAILED` la misma acción permite `Reintentar descarga`. Los documentos incorporados aparecen al recargar la bandeja y pueden abrirse en el detalle y continuar hacia pólizas de SPEC-006.
- Acordar un mecanismo de ejecución suficiente para la demostración; la representación del proceso no implica por sí sola Redis, colas ni workers.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). El contrato de este alcance queda cerrado; cualquier ampliación del servicio o de los estados debe actualizar esta spec antes de modificar consumidores.

## Verificación

**Evidencia de producto:** implementación backend y frontend realizada el 2026-09-08. La comprobación visual queda pendiente porque la instrucción vigente prohíbe navegador y Playwright.

| Criterios | Prueba/comprobación | Resultado |
|---|---|---|
| CA-005-01/02/03/05/06 | `tests/Feature/Spec005Test.php::test_authorized_user_can_run_simulated_download_and_repeated_results_are_deduplicated` y `test_simulated_download_returns_not_found_for_unauthenticated_or_foreign_contexts` | Pasa: solicita por empresa/periodo, incorpora dos fixtures deterministas, repite sin duplicar, conserva originales y aísla autenticación/empresas/periodos. |
| CA-005-02 | `tests/Feature/Spec005Test.php::test_simulated_download_reports_partial_imports_and_keeps_valid_documents` | Pasa: informa tres encontrados, dos incorporados y un rechazo sin deshacer los válidos. |
| CA-005-04 | `tests/Feature/Spec005Test.php::test_simulated_download_document_can_be_used_in_a_policy_without_losing_company_or_period_context` | Pasa: descarga, incorporación, póliza `POSTED`, pivote y trazabilidad inversa conservan empresa y periodo. La interacción visual sigue pendiente. |
| Vacío | `tests/Feature/Spec005Test.php::test_empty_simulated_download_returns_completed_without_creating_documents` | Pasa: `COMPLETED`, cero encontrados y cero documentos persistidos. |
| Fallo/reintento | `tests/Feature/Spec005Test.php::test_failed_simulated_download_does_not_import_and_can_be_retried` | Pasa: `FAILED` no persiste y un segundo intento controlado incorpora los documentos. |
| Backend focalizado | `./vendor/bin/sail artisan test --compact tests/Feature/Spec005Test.php` | Pasa: 7 pruebas y 62 aserciones. |
| Backend completo | `./vendor/bin/sail artisan test --compact` | Pasa: 72 pruebas y 650 aserciones. |
| Frontend | `pnpm lint`, `pnpm typecheck`, `pnpm run build` | Pasa; no se ejecutó `pnpm test:e2e`, navegador ni Playwright. |

Revisiones de implementación: backend sobre `868b20eaaa24c387e7e80f97a5798f024a4582e4` con cambios locales; frontend sobre `597bdc5f71c2ee071ce173ddc81167f2a7461bd7` con cambios locales. La spec permanece Lista hasta contar con evidencia interactiva de la acción y la continuidad XML → póliza, aunque esa continuidad ya está cubierta por backend.

La evidencia de implementación registra criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance de la simulación.

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-08:** se cerró el contrato mínimo de simulación síncrona, fixtures deterministas por empresa/periodo, incorporación parcial reutilizando SPEC-004 y estados `COMPLETED`/`FAILED` con vacío y reintento controlados en pruebas. Pasa a Lista; la implementación y su evidencia quedan pendientes.
- **2026-09-08:** se implementaron el endpoint, el servicio controlado, la incorporación compartida y la acción de frontend; las verificaciones automatizadas pasan. Permanece pendiente únicamente la comprobación interactiva no autorizada.
- **2026-09-08:** se añadió la prueba integrada descarga simulada → CFDI incorporado → póliza balanceada → consulta inversa, conservando empresa y periodo.
