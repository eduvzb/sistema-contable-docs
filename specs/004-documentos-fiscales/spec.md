# SPEC-004 — Documentos fiscales

- **Estado:** Actualización pendiente
- **Actualizado:** 2026-09-24 (migración documental; sin cambio de estado)
- **Criterios de esta entrega:** CA-004-11 (desglose fiscal estructurado)
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-001](../001-acceso-usuarios-empresas/spec.md), [SPEC-002](../002-contexto-contable/spec.md)

## Contexto y objetivo

Incorporar XML manualmente, de uno en uno o en lote; extraer y conservar únicamente datos fiscales normalizados, detectar duplicados y consultar los documentos de la empresa y periodo. Mostrar emitidos/recibidos e información fiscal extraída, distinguiendo PUE/PPD.

Incluye la bandeja de documentos y su situación contable derivada de pólizas.

## Historias de usuario

- H-004-01: Como usuario operativo quiero importar CFDI de forma individual o en lote, para conservar sus datos fiscales normalizados.
- H-004-02: Como usuario operativo quiero consultar y localizar documentos de mi contexto, para relacionarlos con la contabilidad.

## Requisitos funcionales y criterios de aceptación

Tras seleccionar el contexto, el usuario operativo carga XML, revisa el resultado y localiza documentos. El administrador accede a cualquier empresa y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. Se extraen UUID, RFC emisor/receptor, fecha, serie, folio, subtotal, impuestos, total, método/forma de pago, moneda y tipo de comprobante según alcance §7. Se conservan datos de moneda/tipo de cambio cuando existan, sin cálculo cambiario avanzado.

La importación es responsable de la incorporación que reutiliza SPEC-005. El indicador «contabilizado» se deriva de al menos una póliza POSTED (OQ-003); no implica liquidación. Ese indicador consume la relación definida en SPEC-006 y se completa al integrar ambas funcionalidades.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-004-01 | Se carga un XML válido y admitido para la empresa. | Queda disponible con sus datos extraídos; el XML original se descarta y no puede descargarse desde el sistema. |
| CA-004-02 | Se carga un lote de XML válidos, admitidos y no duplicados. | Los documentos quedan consultables; el usuario conoce el resultado de incorporación. |
| CA-004-03 | Se vuelve a cargar un CFDI cuyo UUID ya existe en la misma empresa. | Se informa el duplicado y no se crea otro documento equivalente (BR-010/AC-015, supuesto MVP). |
| CA-004-04 | Se consulta la bandeja dentro del contexto empresa/periodo. | Se pueden localizar documentos y distinguir emitidos/recibidos, PUE/PPD y los campos del alcance §7; la fecha de filtrado se debe concretar. |
| CA-004-05 | Se consulta un documento relacionado únicamente con pólizas DRAFT y luego con al menos una POSTED. | Se deriva «contabilizado» únicamente en el segundo caso, según OQ-003; no se afirma que esté liquidado. |
| CA-004-06 | Se intenta consultar documentos de una empresa no asignada. | No se exponen datos de esa empresa. |
| CA-004-07 | Un archivo no puede incorporarse según las validaciones acordadas. | El usuario identifica el problema por archivo y no se presenta como importado correctamente; los demás archivos válidos del lote sí pueden incorporarse conforme a la política parcial. |
| CA-004-08 | El XML contiene moneda y tipo de cambio. | Se conservan los datos existentes; no se ejecuta lógica contable avanzada de moneda extranjera. |
| CA-004-09 | Termina un intento de importación, incluido un lote con archivos importados y rechazados. | El resultado por archivo permanece visible para revisión, pero la selección nativa de archivos queda vacía y permite iniciar otro intento —incluso seleccionando nuevamente el mismo archivo— sin conservar adjuntos anteriores. Al cerrar y reabrir el diálogo inicia una sesión limpia. |
| CA-004-10 | Ya existe un CFDI y se vuelve a importar junto con otro nuevo de la misma empresa. | El existente se informa como duplicado una sola vez, el nuevo se incorpora una sola vez y la bandeja se reconcilia con la consulta autoritativa. Si el nuevo corresponde al periodo y filtros visibles queda localizable sin recargar manualmente; si queda fuera, el resultado explica qué periodo o filtro impide verlo. Crear una póliza y reintentar la importación reflejan la misma existencia del documento. |
| CA-004-11 | CUANDO se importa por primera vez un CFDI 4.0 con descuento, impuestos federales trasladados o retenidos, o impuestos locales en complemento. | EL SISTEMA conserva subtotal, descuento, total y cada impuesto con clave o nombre, naturaleza e importe decimal de seis posiciones, sin conservar el XML original. La consulta entrega ese desglose a SPEC-006 sin volver a cargar el archivo. |

## Requisitos no funcionales aplicables

- Aislamiento, precisión decimal y descarte del original: CA-004-01/06/08/11 y DT-011/013.

## Casos límite

- Lote mixto, UUID duplicado, archivo inválido, filtro que oculta incorporaciones y desglose fiscal: CA-004-03/07/09/10/11.

## Fuera de alcance

No incluye SAT real, tratamiento de cancelaciones/sustituciones, nómina ni automatización fiscal avanzada.

## Decisiones, supuestos y dudas

### Decisiones cerradas

- Se admiten exclusivamente XML CFDI 4.0 de tipo `I`, `E` y `P`. El RFC de la empresa debe coincidir con emisor o receptor; se clasifica como emitido cuando coincide el emisor y como recibido cuando coincide el receptor.
- Los XML nuevos se procesan desde el temporal de carga y se descartan después de extraer y validar sus datos; no se conservan como archivo o BLOB y no existe descarga del original. Los archivos históricos permanecen sin acceso desde el producto y sin purga automática.
- La bandeja del contexto filtra por mes y ejercicio de la fecha de emisión. Los documentos se pueden relacionar con pólizas de otros periodos de la misma empresa.
- Los lotes se procesan por archivo: los válidos se incorporan y cada archivo inválido o duplicado se devuelve con su error. El UUID es único por empresa.
- Después de una respuesta completa del lote se limpia el control de archivos, no el resultado que el usuario todavía está revisando. Cerrar el diálogo descarta resultado, errores y selección de esa sesión.
- La confirmación de importación y la bandeja no pueden divergir silenciosamente. Tras un lote se vuelve a consultar el periodo activo; los documentos importados que no pertenezcan al periodo o queden ocultos por filtros/paginación se identifican en el resultado, sin reclasificarlos como rechazados ni alterar su fecha fiscal.
- Subtotal, impuestos, total y tipo de cambio se conservan con seis decimales y se representan por API como texto. No se calcula conversión monetaria.
- El desglose se extrae del XML durante su primera incorporación: cada impuesto federal o local conserva tipo, naturaleza e importe; `tax_total` permanece por compatibilidad, pero no alimenta propuestas de partidas. Los CFDI existentes son datos de prueba autorizados para reinicio conforme a SPEC-006.

### Pendientes y decisiones

- **Resuelto para esta entrega:** versiones/tipos, pertenencia al RFC, fecha de filtro, importación parcial, descarte del original y representación decimal.
- **Supuestos para validar:** duplicados por UUID dentro de la empresa (BR-010/AC-015); «contabilizado» derivado de POSTED y distinto de «liquidado» (OQ-003). No crear una máquina de estados compleja (OQ-009).
- **Posterior:** excepciones por sustitución/corrección, consulta SAT de cancelaciones y conversión contable de moneda. El mismo UUID en empresas distintas no se decide como duplicado global.

## Criterios de finalización

- Los criterios de esta entrega deben tener implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §6](../../docs/planeacion/003%20-%20MVP-Scope.md#6-importaci%C3%B3n-y-obtenci%C3%B3n-de-xml), [Alcance §7](../../docs/planeacion/003%20-%20MVP-Scope.md#7-consulta-de-documentos-fiscales), [Alcance §14](../../docs/planeacion/003%20-%20MVP-Scope.md#14-pue), [Alcance §15](../../docs/planeacion/003%20-%20MVP-Scope.md#15-ppd-y-complementos-de-pago) (importación, consulta y distinción PUE/PPD).
- [BR-001](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-010](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#12-br-010--el-mismo-cfdi-no-debe-importarse-dos-veces), [BR-011](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#13-br-011--el-xml-original-no-se-conserva), [BR-012](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#14-br-012--pue-y-ppd-se-tratan-como-escenarios-diferentes); BR-010 es SUPUESTO MVP, las demás están confirmadas en su alcance.
- [AC-015](../../docs/planeacion/004%20-%20Escenarios%20contables.md#17-escenario-ac-015--documento-duplicado) (duplicado por empresa, SUPUESTO MVP); [OQ-003](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#5-oq-003--momento-en-que-un-cfdi-se-considera-contabilizado), [OQ-009](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#11-oq-009--estados-de-fiscaldocument), [OQ-019](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#21-oq-019--moneda-extranjera) (estado derivado provisional y moneda avanzada posterior).
- [Análisis §33: versiones de CFDI pendientes](../../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#33-preguntas-abiertas).
