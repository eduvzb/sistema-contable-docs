# REQ — Ampliación de propuestas de partidas y vista previa de conceptos del CFDI

- **Estado:** Borrador funcional; decisiones pendientes antes de preparar la implementación.
- **Fecha:** 2026-10-08
- **Actor:** Administrador o contador con acceso a la empresa y al contexto contable.
- **Specs relacionadas:** [SPEC-004 — Documentos fiscales](../../specs/004-documentos-fiscales/spec.md), [SPEC-006 — Pólizas y trazabilidad](../../specs/006-polizas-trazabilidad/spec.md), [SPEC-007 — PPD y complementos](../../specs/007-ppd-complementos/spec.md).

## 1. Objetivo

Ampliar la propuesta editable de partidas a partir de uno o varios CFDI, conservando más detalle fiscal y haciendo identificable el origen de cada partida. Incorporar la consulta de las descripciones del comprobante durante la selección de documentos y la revisión de partidas, para que el contador tenga información de la operación al elegir las cuentas.

El contador continúa siendo responsable de revisar, completar y corregir la póliza antes de contabilizar. Consultar descripciones o generar una propuesta no registra automáticamente un asiento definitivo.

## 2. Capacidades actuales que se conservan

Este requerimiento amplía el flujo existente de selección, generación, revisión, guardado y contabilización. Se conservan:

- Propuestas para CFDI `I` y `E` en MXN, emitidos o recibidos, cuyos datos fiscales sean verificables según SPEC-006.
- Partidas de total, subtotal, descuento e impuestos presentes, sin imponer una cantidad fija por CFDI.
- Reglas actuales de orientación cargo/abono y precisión decimal; no se definen tratamientos fiscales nuevos a partir de las descripciones.
- Sugerencias de cuentas y propagación entre componentes equivalentes conforme a CA-006-23/24. Toda cuenta sugerida sigue siendo revisable y corregible.
- Captura manual, edición de partidas y pólizas sin CFDI.
- Varios CFDI por póliza y varias pólizas por CFDI, incluso entre periodos conforme a los permisos y reglas actuales.
- Separación entre DRAFT y POSTED y validaciones autoritativas para contabilizar.
- Conservación de datos normalizados y descarte del XML original.

La exclusión del tratamiento integral de notas de crédito no elimina la propuesta básica vigente para CFDI `E`. Conservar las sugerencias actuales tampoco incorpora clasificación automática de cuentas a partir de las descripciones.

## 3. Información fiscal normalizada

Para nuevas importaciones admitidas, el sistema conservará la información disponible de UUID, serie, folio, emisor, receptor, subtotal, descuento, total, moneda, tipo de cambio, tipo de comprobante y método de pago.

El desglose de impuestos conservará clave o nombre, naturaleza —traslado o retención—, ámbito —federal o local—, importe y, cuando existan en el documento, base, tasa/cuota y tipo de factor.

Se mantendrá la distinción entre impuestos, tasas y factores diferentes. Un dato ausente no se completará mediante una suposición. El detalle fiscal debe evitar contabilizar dos veces el mismo importe por aparecer tanto en los conceptos como en el resumen del comprobante.

Los datos de moneda y tipo de cambio permanecen consultables. Su conservación no habilita propuestas en moneda extranjera ni diferencias cambiarias.

## 4. Descripciones de los conceptos del XML

El sistema incorporará como datos normalizados las descripciones de los conceptos del comprobante. La fuente es el atributo `Descripcion` de cada elemento `cfdi:Concepto` dentro de `cfdi:Conceptos`:

```xml
<cfdi:Conceptos>
  <cfdi:Concepto Descripcion="Servicio de consultoría" ... />
  <cfdi:Concepto Descripcion="Licencia de software" ... />
</cfdi:Conceptos>
```

El ejemplo es ilustrativo; los puntos suspensivos representan otros atributos del XML.

- Se conservarán todas las descripciones disponibles, su orden y su pertenencia al CFDI.
- No se eliminarán conceptos por repetir una descripción.
- El texto completo será consultable y seleccionable; se presentará como texto, sin interpretar etiquetas como contenido activo.
- Cuando un concepto no tenga descripción disponible, la vista lo identificará sin inventar un texto comercial.
- La falta de descripciones no impedirá por sí sola generar partidas si los datos fiscales permiten una propuesta verificable.
- Las descripciones son información de consulta; no se editan desde la póliza ni determinan automáticamente una cuenta.

La descripción del comprobante y el concepto de una partida son datos distintos. Abrir esta consulta no sustituye el concepto contable ni concatena automáticamente todas las descripciones en las partidas.

## 5. Vista previa mediante botón de ojo

### 5.1 Durante la revisión de partidas

En la vista **Pólizas**, dentro del modal **Nueva póliza / Editar póliza**, cada bloque identificado por CFDI tendrá un botón con icono de ojo junto a su encabezado documental.

Al activarlo, se mostrará un panel de lectura dentro del modal actual con:

- Título «Conceptos del CFDI».
- Serie y folio cuando existan, UUID y contraparte para identificar el documento.
- Lista de todas las descripciones, una por concepto, en el orden del XML.

El botón estará disponible también para los CFDI relacionados que requieran captura manual y no tengan un bloque de partidas generadas; se ubicará junto a la identificación del documento en el área de CFDI relacionados.

El contador podrá leer las descripciones, cerrar la vista y continuar asignando cuentas sin perder partidas, importes, selecciones ni otras correcciones. Se usará un botón por documento en el bloque, sin repetirlo en cada partida de ese mismo bloque.

### 5.2 Antes de generar la propuesta

Dentro del modal **CFDI relacionados**, cada documento dispondrá del mismo botón para consultar sus conceptos antes de seleccionarlo o continuar.

Activar el ojo no seleccionará ni deseleccionará el documento, no generará partidas y no ejecutará «Continuar». La vista previa identificará siempre el CFDI consultado, aunque se estén trabajando varios documentos.

### 5.3 En el detalle del documento fiscal

En **Documentos fiscales → Detalle del CFDI**, se incorporará la sección **Conceptos del comprobante**, con la misma información normalizada. La sección existente **Detalle de impuestos** se ampliará para mostrar los datos fiscales nuevos disponibles.

### 5.4 Estados y accesibilidad

- El ojo será un botón operable con teclado, con nombre accesible «Ver conceptos del CFDI …», identificado por folio o UUID.
- La función no dependerá únicamente de un tooltip ni de pasar el cursor.
- Si se consulta información de forma diferida, se distinguirán carga, error recuperable y ausencia de datos.
- Cuando no haya descripciones conservadas, se mostrará «No hay descripciones disponibles para este CFDI»; no se afirmará que el XML original carecía de conceptos.
- Una descripción larga podrá leerse completa, con texto ajustado al ancho y sin limitarse a una sola línea truncada.
- Cerrar la vista devolverá el foco al botón que la abrió y conservará la captura. El contenido seguirá siendo operable en escritorio y en anchos estrechos.
- La consulta respetará el acceso a la empresa y al documento; no expondrá descripciones de empresas ajenas.

## 6. Generación e identificación de partidas

Al continuar con uno o varios CFDI, el sistema analizará por separado cada documento y presentará las propuestas válidas en bloques identificables. «Continuar» no guardará ni contabilizará la póliza.

Cada partida generada conservará su CFDI de origen y su componente fiscal. La referencia se prellenará con el UUID correspondiente. La trazabilidad estructurada continuará identificando el origen aunque el contador corrija los campos editables.

El concepto de la partida identificará el componente y el documento utilizando los datos disponibles. Se propone el formato `{componente} · {serie-folio o UUID} · {contraparte}`; para impuestos incluirá además la información necesaria para distinguirlos. Este formato exacto permanece pendiente de aprobación.

La vista de descripciones aporta contexto para seleccionar cuentas, pero no obliga a generar una partida por cada concepto del XML. La propuesta continúa organizada por componentes fiscales, conforme a SPEC-006.

## 7. Edición y regeneración

El contador podrá cambiar cuentas, cargo/abono, importes, concepto y referencia, así como agregar o eliminar partidas, conservando las validaciones aplicables y el origen de las partidas generadas que permanezcan.

Antes de reemplazar una propuesta que contenga correcciones manuales, el sistema advertirá cuáles documentos se regenerarán y solicitará una decisión explícita. Cancelar conservará la captura. Aceptar no deberá modificar partidas manuales independientes ni bloques de otros documentos.

Un fallo de generación no deberá eliminar correcciones existentes ni reemplazarlas silenciosamente por un bloque vacío.

## 8. Información insuficiente y documentos anteriores

Si no puede generarse una propuesta verificable, el sistema informará el documento y el motivo, conservará su relación y permitirá captura manual. Los demás CFDI válidos podrán continuar. No se crearán importes ni ajustes ficticios.

Se distinguirán la ausencia legítima de impuestos, la falta de desglose conservado y un desglose inconsistente. Ver descripciones no convierte por sí mismo un documento insuficiente en elegible para generación.

No se reconstruirán automáticamente impuestos ni descripciones de CFDI importados anteriormente. Volver a importar un UUID existente mantendrá el comportamiento de duplicados; una actualización del documento desde el XML queda fuera de esta entrega.

## 9. Borrador, contabilización y PPD

La propuesta puede mantenerse en revisión y guardarse como DRAFT conforme a las validaciones actuales. DRAFT no significa contabilizada y no afecta la balanza.

Guardar partidas sin cuenta es una ampliación pendiente de decisión: este documento no la presenta como capacidad actual ni como condición aprobada para la entrega.

Sólo podrá contabilizarse una póliza que cumpla las validaciones del sistema, incluyendo cuentas operables de la empresa, importes válidos y balance entre cargos y abonos. Consultar las descripciones, aceptar cuentas sugeridas o generar una propuesta no sustituye esa validación.

La identificación como PPD no generará por sí sola movimientos bancarios, liquidaciones, saldos pendientes ni tratamiento completo de IVA. Los CFDI `P` mantendrán sus relaciones documentales y captura manual conforme a SPEC-007, sin propuesta automática de partidas. Sus descripciones podrán consultarse cuando estén conservadas.

## 10. Relación con los specs existentes

| Spec | Ampliación que deberá incorporarse al preparar la entrega |
|---|---|
| [SPEC-004](../../specs/004-documentos-fiscales/spec.md) | Ampliar CA-004-11 con base, tasa/cuota y factor disponibles; agregar conservación y consulta de descripciones de conceptos, estados sin información y compatibilidad con documentos anteriores. |
| [SPEC-006](../../specs/006-polizas-trazabilidad/spec.md) | Ampliar CA-006-19/20/21/22 y CA-006-13 con vista previa mediante ojo, conceptos/referencias identificables, revisión, mensajes y protección al regenerar. Preservar CA-006-23/24 sobre sugerencias de cuentas. |
| [SPEC-007](../../specs/007-ppd-complementos/spec.md) | Explicitar que la consulta de descripciones y la propuesta inicial no automatizan pagos, liquidación, saldos ni IVA. |

SPEC-003 continúa proporcionando las cuentas válidas y SPEC-008 continúa excluyendo borradores de la balanza. La preparación de contratos, tareas y estados de entrega se hará mediante el [flujo SDD](../flujo-spec.md), sin crear otra spec para el mismo flujo.

## 11. Casos de aceptación del requerimiento

Estos casos describen el resultado esperado de la ampliación; no acreditan implementación ni sustituyen los CA vigentes de cada spec.

| ID | Situación | Resultado esperado |
|---|---|---|
| REQ-CA-01 | Se importa un CFDI con dos conceptos y descripciones diferentes. | Se conservan y consultan ambas descripciones en su orden, sin almacenar el XML original. |
| REQ-CA-02 | Dos conceptos contienen la misma descripción. | Se muestran ambos conceptos; no se deduplican por texto. |
| REQ-CA-03 | En Nueva/Editar póliza se activa el ojo de un CFDI. | Se muestran únicamente sus conceptos y su identificación; cuentas, importes y captura permanecen sin cambios. |
| REQ-CA-04 | En el selector se consulta un CFDI sin seleccionarlo. | La vista previa no cambia las casillas ni genera partidas. |
| REQ-CA-05 | Hay varios CFDI relacionados y uno requiere captura manual. | Cada documento puede identificarse y consultar sus descripciones disponibles, aunque no tenga partidas generadas. |
| REQ-CA-06 | Un documento antiguo no conserva descripciones. | Se informa que no están disponibles, sin reconstruirlas ni atribuir esa ausencia al XML original. |
| REQ-CA-07 | Existe una descripción larga o un concepto sin descripción. | El texto existente puede leerse completo y la ausencia se identifica; no se inventa información. |
| REQ-CA-08 | La carga diferida de descripciones falla. | Se informa el error y se permite reintentar o cerrar, sin perder la captura. |
| REQ-CA-09 | Se generan partidas desde un CFDI elegible. | Se conserva origen y componente; la referencia se prellena con UUID y el concepto identifica el documento conforme al formato que se apruebe. |
| REQ-CA-10 | El CFDI contiene tasas o factores diferentes. | La información normalizada y su consulta conservan las diferencias; la regla de separación de partidas requiere la decisión indicada en §13. |
| REQ-CA-11 | Un CFDI no permite una propuesta verificable y otro sí. | Se informa el motivo del primero y se permite su captura manual; el segundo conserva su propuesta, sin ajustes ficticios. |
| REQ-CA-12 | Se intenta regenerar una propuesta corregida. | Se requiere una decisión antes de reemplazarla; cancelar o fallar no elimina la captura existente. |
| REQ-CA-13 | Existe una sugerencia válida de cuenta según CA-006-23/24. | La ayuda actual se conserva y el contador puede corregirla; consultar conceptos no cambia automáticamente la cuenta. |
| REQ-CA-14 | Se opera el ojo con teclado y se cierra la vista. | El contenido es legible, el foco vuelve al disparador y las selecciones y partidas se conservan. |
| REQ-CA-15 | Un usuario intenta consultar conceptos de otra empresa sin acceso. | No se entregan ni se muestran sus datos. |
| REQ-CA-16 | Se revisa una factura PPD o un CFDI `P`. | La vista previa no genera movimientos bancarios, saldos ni liquidación; se mantienen las restricciones de generación y las relaciones actuales. |

## 12. Fuera del alcance

- Contabilización automática completa o selección definitiva de cuentas sin revisión.
- Nuevas reglas que clasifiquen cuentas leyendo las descripciones, inteligencia artificial o patrones semánticos por producto/servicio.
- Una partida automática por cada concepto comercial del XML o una nueva relación contable por concepto.
- Reconstrucción o enriquecimiento automático de documentos anteriores y actualización mediante reimportación.
- Conservación, descarga o visualización del archivo XML original.
- Tratamiento integral de cancelaciones, sustituciones, notas de crédito, retenciones complejas y complementos de pago avanzados.
- Cálculo de saldos pendientes, diferencias cambiarias y automatización de pagos o IVA.

Estas exclusiones no retiran las sugerencias actuales de cuentas, las propuestas básicas para CFDI `E` ni las relaciones documentales implementadas.

## 13. Decisiones pendientes antes de preparar la implementación

1. **Separación de impuestos en partidas:** confirmar si cada combinación distinguible de impuesto, naturaleza, ámbito, tasa/cuota y factor genera siempre una partida independiente; definir los casos sin importe y de importe cero, conservando la información fiscal aunque no produzca movimiento.
2. **Formato del concepto y referencia:** aprobar el formato propuesto de identificación, qué hacer al superar la longitud admitida y si el UUID prellenado puede corregirse libremente o debe conservarse en el campo referencia además del vínculo de origen.
3. **Borradores sin cuenta:** decidir si esta entrega amplía DRAFT para conservar partidas sin cuenta o mantiene las validaciones actuales. No bloquea la definición de la vista previa de conceptos.

La conservación de cuentas sugeridas, la propuesta básica para `I`/`E`, la consulta de todas las descripciones mediante el ojo y la ausencia de reconstrucción automática de documentos antiguos forman parte del alcance de este requerimiento.
