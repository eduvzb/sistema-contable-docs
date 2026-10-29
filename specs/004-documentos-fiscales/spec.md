# SPEC-004 — Documentos fiscales

- **Estado:** Actualización pendiente
- **Actualizado:** 2026-10-28
- **Criterios de esta entrega:** CA-004-01/03/10/11/12/13 revisados y CA-004-14 añadido, coordinados con la implementación parcial controlada de SPEC-012. Cierre técnico y QA de la actualización pendientes; la aprobación anterior de conceptos no acredita estos cambios.
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-001](../001-acceso-usuarios-empresas/spec.md), [SPEC-002](../002-contexto-contable/spec.md)

## Contexto y objetivo

Incorporar XML manualmente, de uno en uno o en lote; conservar datos fiscales normalizados y originales privados, detectar duplicados y consultar los documentos de la empresa y periodo. Mostrar emitidos/recibidos e información fiscal extraída, distinguiendo PUE/PPD.

Incluye la bandeja de documentos y su situación contable derivada de pólizas.

La conservación de descripciones de conceptos para [SPEC-006](../006-polizas-trazabilidad/spec.md) sigue vigente. La actualización pendiente amplía tipos y conservación de originales conforme a [SPEC-012](../012-descarga-masiva-sat/spec.md), sin implementar la conexión SAT en esta spec ni ampliar la interfaz del detalle fiscal.

## Historias de usuario

- H-004-01: Como usuario operativo quiero importar CFDI de forma individual o en lote, para conservar sus datos fiscales normalizados.
- H-004-02: Como usuario operativo quiero consultar y localizar documentos de mi contexto, para relacionarlos con la contabilidad.

## Requisitos funcionales y criterios de aceptación

Tras seleccionar el contexto, el usuario operativo carga XML, revisa el resultado y localiza documentos. El administrador accede a cualquier empresa y el contador solo a sus asignadas, conforme a SPEC-001. Se extraen UUID, RFC emisor/receptor, fecha, serie, folio, subtotal, impuestos, total, método/forma de pago, moneda y tipo de comprobante según alcance §7. Se conservan datos de moneda/tipo de cambio cuando existan, sin cálculo cambiario avanzado.

La importación es responsable de la incorporación que reutiliza SPEC-005. El indicador «contabilizado» se deriva de al menos una póliza POSTED (OQ-003); no implica liquidación. Ese indicador consume la relación definida en SPEC-006 y se completa al integrar ambas funcionalidades.

La carga admitirá XML CFDI 4.0 de tipo `I`, `E`, `P`, `N` y `T` cuando el RFC de la empresa coincida con emisor o receptor. Procesa cada archivo del lote de forma independiente. La conservación privada del original y la ampliación a `N`/`T` son cambios pendientes coordinados con SPEC-012; el código anterior sólo admite `I`/`E`/`P` y descarta el original. La bandeja filtra por mes y ejercicio de emisión; la relación con pólizas de los tipos permitidos puede cruzar periodos de la misma empresa. Los importes se representan como texto decimal de seis posiciones, sin conversión monetaria automática.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-004-01 | Se carga por primera vez un XML válido y admitido para la empresa. | Queda disponible con sus datos extraídos y se conserva su original conforme a CA-012-09 de SPEC-012: privado, protegido por permisos y respaldado, sin descarga al equipo. No se recuperan automáticamente originales históricos. |
| CA-004-02 | Se carga un lote de XML válidos, admitidos y no duplicados. | Los documentos quedan consultables; el usuario conoce el resultado de incorporación. |
| CA-004-03 | Se vuelve a cargar un CFDI cuyo UUID ya existe en la misma empresa. | No se crea otro documento equivalente. Si ya tiene original, se informa el duplicado sin reemplazarlo; si falta, se aplica la comparación y el resultado de CA-012-10/11 de SPEC-012, sin modificar datos fiscales, relaciones ni contabilidad. |
| CA-004-04 | Se consulta la bandeja dentro del contexto empresa/periodo. | Se pueden localizar documentos emitidos/recibidos y PUE/PPD por mes y ejercicio de emisión, con los campos fiscales de consulta. |
| CA-004-05 | Se consulta un documento relacionado únicamente con pólizas DRAFT y luego con al menos una POSTED. | Se deriva «contabilizado» únicamente en el segundo caso, según OQ-003; no se afirma que esté liquidado. |
| CA-004-06 | Se intenta consultar documentos de una empresa no asignada. | No se exponen datos de esa empresa. |
| CA-004-07 | Un archivo no puede incorporarse según las validaciones acordadas. | El usuario identifica el problema por archivo y no se presenta como importado correctamente; los demás archivos válidos del lote sí pueden incorporarse conforme a la política parcial. |
| CA-004-08 | El XML contiene moneda y tipo de cambio. | Se conservan los datos existentes; no se ejecuta lógica contable avanzada de moneda extranjera. |
| CA-004-09 | Termina un intento de importación, incluido un lote con archivos importados y rechazados. | El resultado por archivo permanece visible para revisión, pero la selección nativa de archivos queda vacía y permite iniciar otro intento —incluso seleccionando nuevamente el mismo archivo— sin conservar adjuntos anteriores. Al cerrar y reabrir el diálogo inicia una sesión limpia. |
| CA-004-10 | Ya existe un CFDI y se vuelve a importar junto con otro nuevo de la misma empresa. | El existente tiene un único resultado conforme a CA-004-03 —duplicado, original completado o rechazo explicado—, el nuevo se incorpora una sola vez y la bandeja se reconcilia con la consulta autoritativa. Si el nuevo corresponde al periodo y filtros visibles queda localizable sin recargar manualmente; si queda fuera, el resultado explica qué periodo o filtro impide verlo. Crear una póliza y reintentar la importación reflejan la misma existencia del documento. |
| CA-004-11 | CUANDO se importa por primera vez un CFDI 4.0 admitido con descuento, impuestos federales trasladados o retenidos, o impuestos locales en complemento. | EL SISTEMA conserva subtotal, descuento, total y cada impuesto con clave o nombre, naturaleza e importe decimal de seis posiciones, además del original conforme a CA-004-01. La consulta entrega ese desglose a SPEC-006 sin volver a cargar el archivo, respetando la restricción de tipos de CA-004-14. |
| CA-004-12 | Se importa por primera vez un CFDI admitido con elementos `cfdi:Concepto` dentro de `cfdi:Conceptos`. | Se conserva el atributo `Descripcion` de cada concepto y su pertenencia al CFDI, en el orden del XML y sin eliminar descripciones repetidas. Un concepto sin descripción conserva su posición sin inventar texto. Las descripciones completas quedan consultables por el usuario con acceso a la empresa y al documento, además del original conforme a CA-004-01 y sin cambiar los datos fiscales extraídos. |
| CA-004-13 | Se consulta un documento anterior sin conceptos conservados, un documento nuevo sin conceptos o se reimporta un UUID existente. | La consulta permite distinguir datos no conservados de una lista de conceptos vacía. No reconstruye descripciones ni actualiza datos fiscales por reimportación; sólo puede completar el original conforme a CA-004-03, sin rellenar conceptos históricos. La ausencia de descripciones no impide por sí sola continuar la captura contable de los tipos permitidos. |
| CA-004-14 | Se importa o consulta un CFDI 4.0 de nómina o traslado. | Se aplica CA-012-06 de SPEC-012 también a la carga manual: consulta general, sin extracción especializada de complementos, nuevas relaciones con pólizas, propuestas de partidas ni inclusión automática en DIOT. |

## Requisitos no funcionales aplicables

- Aislamiento, precisión decimal y conservación privada del original: CA-004-01/06/08/11.

## Casos límite

- Lote mixto, UUID duplicado, archivo inválido, filtro que oculta incorporaciones y desglose fiscal: CA-004-03/07/09/10/11.

## Fuera de alcance

La conexión SAT real pertenece a SPEC-012. No incluye tratamiento de cancelaciones/sustituciones, cálculo o tratamiento contable especializado de nómina/traslado ni automatización fiscal avanzada.

Esta entrega tampoco incluye recuperar conceptos de documentos anteriores, conservar otros atributos de los conceptos, ampliar impuestos, mostrar el XML original ni añadir una sección de conceptos en Documentos fiscales.

## Criterios de finalización

- Los CA pendientes requieren implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

Las fuentes de Planeación describen el alcance original. La regla histórica BR-011 de descarte queda sustituida para las nuevas incorporaciones por CA-004-01 y SPEC-012; no acredita implementación de la conservación pendiente.

- [Alcance §6](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#6-importaci%C3%B3n-y-obtenci%C3%B3n-de-xml), [Alcance §7](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#7-consulta-de-documentos-fiscales), [Alcance §14](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#14-pue), [Alcance §15](../../docs/planeacion/003%20-%20Alcance%20del%20producto.md#15-ppd-y-complementos-de-pago) (importación, consulta y distinción PUE/PPD).
- [BR-001](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-010](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#12-br-010--el-mismo-cfdi-no-debe-importarse-dos-veces), [BR-011](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#13-br-011--el-xml-original-no-se-conserva), [BR-012](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#14-br-012--pue-y-ppd-se-tratan-como-escenarios-diferentes).
- [AC-015](../../docs/planeacion/004%20-%20Escenarios%20contables.md#17-escenario-ac-015--documento-duplicado) (duplicado por empresa); [OQ-003](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#5-oq-003--momento-en-que-un-cfdi-se-considera-contabilizado), [OQ-009](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#11-oq-009--estados-de-fiscaldocument), [OQ-019](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#21-oq-019--moneda-extranjera) (estado derivado y moneda avanzada por evaluar).
