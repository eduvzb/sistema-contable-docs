# SPEC-004 — Documentos fiscales

**Estado:** Lista
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md)

## Propósito y alcance

Incorporar XML manualmente, de uno en uno o en lote; conservar originales, detectar duplicados y consultar los documentos de la empresa y periodo. Mostrar emitidos/recibidos e información fiscal extraída, distinguiendo PUE/PPD.

Incluye la bandeja de documentos y su situación contable derivada de pólizas. No incluye SAT real, tratamiento de cancelaciones/sustituciones, nómina ni automatización fiscal avanzada.

## Fuentes

- [Alcance §6](../docs/planeacion/003%20-%20MVP-Scope.md#6-importaci%C3%B3n-y-obtenci%C3%B3n-de-xml), [Alcance §7](../docs/planeacion/003%20-%20MVP-Scope.md#7-consulta-de-documentos-fiscales), [Alcance §14](../docs/planeacion/003%20-%20MVP-Scope.md#14-pue), [Alcance §15](../docs/planeacion/003%20-%20MVP-Scope.md#15-ppd-y-complementos-de-pago) (importación, consulta y distinción PUE/PPD).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-010](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#12-br-010--el-mismo-cfdi-no-debe-importarse-dos-veces), [BR-011](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#13-br-011--el-xml-original-debe-conservarse), [BR-012](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#14-br-012--pue-y-ppd-se-tratan-como-escenarios-diferentes); BR-010 es SUPUESTO MVP, las demás están confirmadas en su alcance.
- [AC-015](../docs/planeacion/004%20-%20Escenarios%20contables.md#17-escenario-ac-015--documento-duplicado) (duplicado por empresa, SUPUESTO MVP); [OQ-003](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#5-oq-003--momento-en-que-un-cfdi-se-considera-contabilizado), [OQ-009](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#11-oq-009--estados-de-fiscaldocument), [OQ-019](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#21-oq-019--moneda-extranjera) (estado derivado provisional y moneda avanzada posterior).
- [Análisis §33: versiones de CFDI pendientes](../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#33-preguntas-abiertas).

## Comportamiento y criterios de aceptación

Tras seleccionar el contexto, el usuario operativo carga XML, revisa el resultado y localiza documentos. El administrador accede a cualquier empresa y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. Se extraen UUID, RFC emisor/receptor, fecha, serie, folio, subtotal, impuestos, total, método/forma de pago, moneda y tipo de comprobante según alcance §7. Se conservan datos de moneda/tipo de cambio cuando existan, sin cálculo cambiario avanzado.

La importación es responsable de la incorporación que reutiliza SPEC-005. El indicador «contabilizado» se deriva de al menos una póliza POSTED (OQ-003); no implica liquidación. Ese indicador consume la relación definida en SPEC-006 y se completa al integrar ambas funcionalidades.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-004-01 | Se carga un XML válido y admitido para la empresa. | Queda disponible con sus datos extraídos y se conserva el XML original. |
| CA-004-02 | Se carga un lote de XML válidos, admitidos y no duplicados. | Los documentos quedan consultables; el usuario conoce el resultado de incorporación. |
| CA-004-03 | Se vuelve a cargar un CFDI cuyo UUID ya existe en la misma empresa. | Se informa el duplicado y no se crea otro documento equivalente (BR-010/AC-015, supuesto MVP). |
| CA-004-04 | Se consulta la bandeja dentro del contexto empresa/periodo. | Se pueden localizar documentos y distinguir emitidos/recibidos, PUE/PPD y los campos del alcance §7; la fecha de filtrado se debe concretar. |
| CA-004-05 | Se consulta un documento relacionado únicamente con pólizas DRAFT y luego con al menos una POSTED. | Se deriva «contabilizado» únicamente en el segundo caso, según OQ-003; no se afirma que esté liquidado. |
| CA-004-06 | Se intenta consultar documentos de una empresa no asignada. | No se exponen datos ni archivos originales de esa empresa. |
| CA-004-07 | Un archivo no puede incorporarse según las validaciones acordadas. | El usuario identifica el problema; no se presenta ese archivo como importado correctamente. El efecto sobre el resto del lote sigue pendiente. |
| CA-004-08 | El XML contiene moneda y tipo de cambio. | Se conservan los datos existentes; no se ejecuta lógica contable avanzada de moneda extranjera. |

## Decisiones cerradas

- Se admiten exclusivamente XML CFDI 4.0 de tipo `I`, `E` y `P`. El RFC de la empresa debe coincidir con emisor o receptor; se clasifica como emitido cuando coincide el emisor y como recibido cuando coincide el receptor.
- Se conservan los XML originales en almacenamiento privado y solo un usuario con acceso vigente a la empresa puede descargarlos.
- La bandeja del contexto filtra por mes y ejercicio de la fecha de emisión. Los documentos se pueden relacionar con pólizas de otros periodos de la misma empresa.
- Los lotes se procesan por archivo: los válidos se incorporan y cada archivo inválido o duplicado se devuelve con su error. El UUID es único por empresa.
- Subtotal, impuestos, total y tipo de cambio se conservan con seis decimales y se representan por API como texto. No se calcula conversión monetaria.

## Pendientes y decisiones

- **Resuelto para esta entrega:** versiones/tipos, pertenencia al RFC, fecha de filtro, importación parcial, recuperación autorizada del original y representación decimal.
- **Supuestos para validar:** duplicados por UUID dentro de la empresa (BR-010/AC-015); «contabilizado» derivado de POSTED y distinto de «liquidado» (OQ-003). No crear una máquina de estados compleja (OQ-009).
- **Posterior:** excepciones por sustitución/corrección, consulta SAT de cancelaciones y conversión contable de moneda. El mismo UUID en empresas distintas no se decide como duplicado global.

## Plan técnico y contratos

- Backend: conservación privada del archivo, extracción y consulta aislada por empresa; expone incorporación parcial, listado por periodo, descarga autorizada y el indicador derivado de pólizas `POSTED`.
- Frontend: carga múltiple, resultado por archivo y bandeja local con filtros básicos, sin añadir descarga SAT ni automatizaciones fiscales.
- La política de lote se cerró como parcial. No requiere workers ni infraestructura adicional (DT-005).

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). Los contratos aún no están cerrados: resolver los detalles necesarios antes de Lista, sin introducir reglas para completar huecos.

## Verificación

**Evidencia de producto:** implementación backend y frontend realizada el 2026-09-08. `./vendor/bin/sail artisan test --compact` pasó con 31 pruebas y 263 aserciones; SPEC-004 cubre lote mixto, UUID duplicado, RFC ajeno, filtro por periodo, aislamiento, descarga autorizada e indicador contabilizado derivado. `pnpm lint`, `pnpm typecheck` y `pnpm build` pasaron en frontend. Se añadió cobertura Playwright para el flujo integrado, sin ejecutarla por la restricción vigente de no abrir navegador.

**Revisiones de implementación:** backend `7427840516423bb59f122e6db33eb890ba3bcbb8`; frontend `2020e0194c3ba998aa29a412005019ca8734bd15`.

Prever pruebas de conservación del original, extracción, duplicado reintentado dentro de la misma empresa, lote mixto según contrato, aislamiento de archivos y regresión DRAFT/POSTED. El cálculo del indicador debe probarse al integrar SPEC-006.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance de documentos.

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-08:** se prepara la implementación conjunta con SPEC-006: CFDI 4.0 `I`/`E`/`P`, carga parcial, original privado, filtro por emisión y decimales de seis posiciones. Pasa a Lista; la evidencia se registra después de implementar.
- **2026-09-08:** se implementaron contrato API, almacenamiento privado, lote parcial y bandeja de CFDI; se registró la evidencia automatizada aplicable.
