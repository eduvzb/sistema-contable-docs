# SPEC-011 — DIOT

- **Estado:** Actualización pendiente
- **Actualizado:** 2026-10-28
- **Criterios de esta entrega:** CA-011-10/11 revisados y CA-011-14 a CA-011-16 nuevos. CA-011-01 a CA-011-09 y CA-011-12/13 se conservan como regresión.
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-002](../002-contexto-contable/spec.md), [SPEC-004](../004-documentos-fiscales/spec.md), [SPEC-006](../006-polizas-trazabilidad/spec.md), [SPEC-009](../009-reportes-exportacion/spec.md)

## Contexto y objetivo

Actualizar la pestaña DIOT para revisar el IVA total del periodo, identificar la póliza de cada resultado y recorrer la tabla en páginas de 25 filas. La consulta y el Excel tendrán el mismo desglose por póliza, proveedor, factor y tasa, sin cambiar la selección ni el cálculo fiscal al contabilizar.

## Historias de usuario

- H-011-01: Como contador quiero elegir los subtotales que participan en DIOT para conservar su cálculo al contabilizar.
- H-011-02: Como usuario operativo quiero consultar y exportar bases e IVA por proveedor y mes para revisar la información.

## Requisitos funcionales y criterios de aceptación

La captura contable continúa regida por SPEC-006; esta capacidad agrega información DIOT, no asientos ni tratamiento automático de pagos. Cada subtotal generado representa el subtotal de un XML completo, no sus conceptos individuales. Seleccionarlo incluye todas sus bases de IVA elegibles, separadas por tasa y tipo de factor.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-011-01 | CUANDO se abre una póliza nueva o borrador con subtotales elegibles. | Cada subtotal tiene un botón DIOT inicialmente inactivo. Un clic lo activa, resalta el botón y sombrea sólo esa fila; otro clic revierte los tres efectos. Las filas se seleccionan independientemente, también mediante teclado, con estado anunciable y sin depender sólo del color. |
| CA-011-02 | CUANDO se evalúa si una fila puede seleccionarse. | Sólo se habilita DIOT para el subtotal con origen verificable en un CFDI I recibido por la empresa, PUE, MXN, con IVA trasladado 002 calculable, a tasa cero o exento. Las partidas manuales, otros componentes, documentos no elegibles o sin datos fiscales suficientes no permiten activación e indican el motivo. |
| CA-011-03 | CUANDO se guarda un borrador y se vuelve a abrir. | No se conserva selección ni se generan resultados DIOT. Quitar una fila o desvincular su XML antes de contabilizar elimina su selección transitoria; las demás selecciones no cambian. |
| CA-011-04 | CUANDO se contabiliza válidamente con subtotales seleccionados. | Se conserva para cada XML su proveedor, póliza, periodo contable y desglose fiscal: por cada traslado 002 con factor Tasa se calcula Base × TasaOCuota del XML, redondeado a seis decimales con mitades hacia arriba; luego se suman bases e IVA por tasa. Base 1,000 y tasa 0.16 producen IVA 160.000000. No intervienen otros impuestos, retenciones ni el importe editado de la partida; no se resta nuevamente el descuento de la base fiscal. |
| CA-011-05 | SI un XML seleccionado contiene varias tasas, tasa cero y/o exento. | Se conservan grupos independientes por tasa y factor; tasa cero y exento conservan sus bases e IVA 0.000000, sin confundirse entre sí. Cada base se cuenta una vez desde un único nivel fiscal del XML, sin sumar simultáneamente conceptos y totales. |
| CA-011-06 | SI falla la contabilización o una selección contiene un origen inválido, datos incompletos o importes fuera de capacidad. | Se informa el motivo y no se guarda parcialmente ni la contabilización ni la DIOT; la captura permanece disponible para corregir. No se infieren tasas a partir de subtotal o importe de impuesto. |
| CA-011-07 | SI se intenta incluir el mismo XML de una empresa en otra póliza, repetirlo en varias filas o contabilizarlo concurrentemente. | Sólo se admite una inclusión DIOT por XML y empresa, sin importar el periodo; la segunda inclusión se rechaza sin efectos parciales. Reintentar el guardado de la misma póliza ya contabilizada no duplica resultados. |
| CA-011-08 | CUANDO se consulta o edita una póliza ya contabilizada. | La selección DIOT y su resultado se muestran en sólo lectura y no se agregan, eliminan ni recalculan. Las ediciones contables permitidas por SPEC-006 preservan la información DIOT y su trazabilidad; intentar alterar sus vínculos de origen o su periodo es rechazado. Las pólizas previamente contabilizadas sin DIOT no reciben selección retroactiva. |
| CA-011-09 | CUANDO se contabiliza sin subtotales seleccionados. | No se generan resultados DIOT y se mantienen las reglas contables existentes, incluida la posibilidad de pólizas sin XML. |
| CA-011-10 | CUANDO se consulta DIOT de una empresa y periodo mensual accesibles. | Se muestran sólo resultados conservados al contabilizar, asignados al periodo de la póliza, agrupados por póliza, RFC del proveedor, factor y tasa, con bases e IVA sumados a seis decimales. Pólizas distintas no se fusionan aunque compartan proveedor y tasa. Se distinguen cero y exento; un periodo sin resultados muestra un estado vacío. |
| CA-011-11 | CUANDO se exporta la consulta mensual. | Se descarga un XLSX de una hoja cuya primera columna se llama «# poliza» y muestra el mismo número de póliza que la pantalla; conserva después empresa, año, mes, RFC proveedor, factor, tasa, base e IVA. Incluye todas las filas del periodo, no sólo la página visible, con las mismas agrupaciones, orden e importes de la consulta completa. Un periodo vacío genera encabezados sin filas; aplica el límite vigente de exportación de 10,000 filas, rechazándose el exceso sin archivo. No es un formato de carga al SAT. |
| CA-011-12 | SI se intenta seleccionar, contabilizar, consultar o exportar información de una empresa sin acceso. | No se permite la operación ni se revelan sus datos; tampoco se aceptan XML ajenos o periodos de otra empresa. |
| CA-011-13 | CUANDO se importa un XML con IVA trasladado 002. | Se conservan base, factor y tasa cuando corresponda, incluyendo cero y exento sin exigir tasa o importe inexistentes en este último. El desglose permite el cálculo por tasa sin duplicar bases; las importaciones y propuestas contables existentes mantienen su comportamiento. |
| CA-011-14 | CUANDO termina correctamente la consulta mensual. | Una sección sobre la tabla muestra «Total IVA» con la suma exacta de IVA de todas las filas del periodo a seis decimales, sin duplicar ni perder importes. El total no cambia al navegar entre páginas. Si no hay resultados muestra 0.000000 junto al estado vacío; durante carga, sin periodo o ante un error no presenta un total anterior ni un cero como resultado válido. |
| CA-011-15 | CUANDO se muestran las filas de DIOT. | La primera columna tiene el encabezado «# poliza» y presenta como texto el número visible de la póliza relacionada, con el formato utilizado en el listado de pólizas, no el identificador interno. Las demás columnas permanecen en su orden actual. No se requiere enlace ni navegación a la póliza. |
| CA-011-16 | CUANDO se recorren los resultados. | La tabla muestra hasta 25 filas por página, controles «Anterior» y «Siguiente» e indicador «Página X de Y». Los controles están deshabilitados en sus límites y son operables por teclado con nombres accesibles; no se omiten ni repiten filas entre páginas. Al cambiar empresa o periodo se vuelve a la primera página y no se muestran datos anteriores ni respuestas tardías de otro contexto. Con 1 a 25 filas muestra página 1 de 1 y ambos controles deshabilitados; sin resultados no hay controles de paginación activos. |

## Requisitos no funcionales aplicables

- Accesibilidad: CA-011-01/02/08; precisión e integridad: CA-011-04/05/06/07; aislamiento: CA-011-12.

## Casos límite

- XML antiguos sin desglose suficiente, sin IVA y capturas manuales: CA-011-02/06.
- Tasas mixtas, descuentos, cero y exento: CA-011-04/05/13.
- Duplicados entre periodos, concurrencia y reintentos: CA-011-07/08.
- Borradores, ausencia de selección, consulta vacía y exceso de filas: CA-011-03/09/10/11.

## Fuera de alcance

Archivo oficial o envío al SAT, PPD/complementos y prorrateo de pagos, notas de crédito, emitidos, otras monedas, retenciones, selección por concepto individual del XML, corrección/reversión DIOT posterior a contabilización y reconstrucción automática de datos fiscales históricos faltantes. No se crean proveedores maestros ni se amplían los tres reportes de SPEC-009; DIOT es una consulta y exportación adicional bajo esta spec. Esta actualización no añade filtros, ordenación interactiva, selector de tamaño de página, enlaces a pólizas, una fila de total en Excel ni cambios al editor o al cálculo fiscal.

## Preguntas abiertas

Sin decisiones bloqueantes. El usuario confirmó el 2026-10-28 el total del periodo, el desglose por póliza, la paginación fija de 25 filas y la actualización del Excel. Se conserva la definición previa del origen verificable: referencia al CFDI vinculado y elegible y a su componente `subtotal`, validada en servidor, sin exigir acreditar una propuesta previa.

## Criterios de finalización

- El alcance está definido en [plan.md](plan.md), [tasks-backend.md](tasks-backend.md) y [tasks-frontend.md](tasks-frontend.md). La actualización está implementada y comprobada localmente conforme a [verificacion.md](verificacion.md). Se mantiene Actualización pendiente, no QA: el usuario autorizó continuar sobre la rama actual con los cambios previos, sin commits ni publicación, por lo que falta el cierre formal del flujo y la QA humana.
- Los CA de esta entrega requieren implementación, pruebas y cierre técnico registrados en [verificacion.md](verificacion.md) antes de pasar a QA.
- Sólo una aprobación humana registrada permite Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- Alcance confirmado por el usuario el 2026-10-26.
- [SPEC-004](../004-documentos-fiscales/spec.md): documentos e importación; [SPEC-006](../006-polizas-trazabilidad/spec.md): pólizas y origen del subtotal; [SPEC-009](../009-reportes-exportacion/spec.md): convenciones vigentes de Excel, sin ampliar sus criterios.
