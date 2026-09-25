# SPEC-006 — Pólizas y trazabilidad

- **Estado:** Actualización pendiente
- **Actualizado:** 2026-09-24 (migración documental; sin cambio de estado)
- **Criterios de esta entrega:** CA-006-19 revisado y CA-006-20 a CA-006-24; depende de CA-004-11.
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-001](../001-acceso-usuarios-empresas/spec.md), [SPEC-002](../002-contexto-contable/spec.md), [SPEC-003](../003-catalogo-cuentas/spec.md), [SPEC-004](../004-documentos-fiscales/spec.md)

## Contexto y objetivo

Crear, consultar y modificar pólizas con partidas manuales o propuestas desde CFDI; guardarlas como borrador y contabilizarlas balanceadas. Conservar documentos relacionados, cuentas, empresa, periodo y autoría básica.

Incluye tipos INGRESO/EGRESO/DIARIO, estados DRAFT/POSTED, relaciones XML opcionales y múltiples, trazabilidad bidireccional, ingresos/egresos PUE, representación manual del registro inicial PPD y una propuesta editable de partidas desde datos fiscales.

La edición posterior a contabilización se limita por las decisiones cerradas de esta spec.

## Historias de usuario

- H-006-01: Como contador quiero crear y modificar pólizas con partidas manuales, para registrar operaciones balanceadas y trazables.
- H-006-02: Como contador quiero seleccionar CFDI de mi periodo y revisar partidas propuestas, para completar una póliza editable sin contabilizarla automáticamente.
- H-006-03: Como contador quiero reutilizar las cuentas que asigné a componentes equivalentes, para agilizar la captura posterior.

## Requisitos funcionales y criterios de aceptación

El usuario operativo crea una póliza con o sin XML, selecciona cuentas y registra partidas. El administrador accede a cualquier empresa y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. La póliza contiene fecha, tipo, número, concepto, partidas, documentos y estado; las partidas contienen cuenta, cargo, abono, concepto y referencia según alcance §9/10. Empresa/periodo vienen de SPEC-002. Se permite guardar incompleta como DRAFT (supuesto); la contabilización exige cargos = abonos.

Las relaciones permiten varios XML por póliza y varias pólizas por XML, incluso entre periodos. Desde cada lado se puede consultar el otro y recorrer las partidas/cuentas de la póliza. La relación contable permanece a nivel de póliza: el origen opcional de una partida generada identifica el CFDI y componente usados para proponerla, sin convertirla en una relación contable por partida. Otra granularidad de relación requiere una decisión posterior. Proveedor/cliente no requieren entidades propias en el MVP (OQ-013).

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-006-01 | El contador crea una póliza con partidas manuales y cuentas de su empresa. | Se conserva como póliza consultable con fecha, tipo, número, concepto, partidas, empresa y periodo según el contrato preparado; cada partida indica la cuenta afectada conforme a BR-004. |
| CA-006-02 | Una póliza todavía tiene cargos distintos de abonos y se guarda como DRAFT. | Puede conservarse como borrador incompleto, sin considerarse contabilizada (BR-006/OQ-002, supuesto). |
| CA-006-03 | Se intenta contabilizar una póliza cuyos cargos no igualan sus abonos. | Se rechaza la contabilización y no se presenta como POSTED (BR-005). |
| CA-006-04 | Una póliza cumple las validaciones preparadas y sus cargos igualan sus abonos. | Puede contabilizarse como POSTED; sus partidas quedan disponibles para la balanza de SPEC-008. |
| CA-006-05 | Se crea una póliza sin XML. | La ausencia de documento fiscal no impide la póliza; solo aplican las validaciones correspondientes a sus datos/partidas. |
| CA-006-06 | Se relacionan varios XML de la empresa con una póliza. | Se conservan y se pueden consultar todos los documentos relacionados. |
| CA-006-07 | Se relaciona un XML con varias pólizas de la misma empresa. | Se pueden consultar todas las pólizas y sus periodos desde el documento, y regresar al XML desde cada póliza. |
| CA-006-08 | Una partida usa una cuenta de otra empresa o se intenta vincular un XML ajeno a la empresa de la póliza. | La operación impide mezclar información entre empresas. |
| CA-006-09 | Se crea o modifica una póliza mediante una operación permitida. | Se conserva quién la creó/modificó, fechas de creación/modificación, empresa y periodo; no se exige historial completo de cada campo. |
| CA-006-10 | Se registra un ingreso/egreso PUE con cuentas y partidas elegidas por el contador. | El XML queda trazable a la póliza y sus cuentas; no se deciden automáticamente asientos ni tratamiento fiscal. |
| CA-006-11 | Se consulta la trazabilidad desde una póliza o un XML con permisos suficientes. | Se muestran documentos, pólizas, partidas/cuentas y periodos asociados; complementos y pagos se integran según SPEC-007. |
| CA-006-12 | Un usuario sin acceso intenta consultar, modificar o contabilizar una póliza de otra empresa. | No puede realizar la operación ni obtener sus datos. |
| CA-006-13 | El contador modifica manualmente cuentas o partidas de una póliza cuya edición está permitida. | Los cambios válidos se conservan y pueden consultarse, manteniendo las validaciones y auditoría aplicables, incluida la exigencia de que una póliza POSTED continúe balanceada. |
| CA-006-14 | El usuario selecciona la fecha al crear o editar una póliza. | El control hace visibles el día, mes y año en español y permite elegir o escribir la fecha con teclado. El calendario muestra únicamente el periodo contable aplicable y no permite elegir días fuera de él; si se introduce manualmente una fecha inválida, el error aparece junto al control sin perder el resto de la captura. No se muestra el copy permanente “Periodo contable: … Solo puedes elegir fechas de este periodo. Usa Tab y Enter para elegir una fecha”. |
| CA-006-15 | El usuario abre el calendario de fecha durante la creación o edición. | El calendario aparece superpuesto sobre los demás elementos, permanece visible y operable dentro del área disponible, y abrirlo o cerrarlo no desplaza contenido, cambia las dimensiones del editor ni agrega scroll horizontal o vertical. |
| CA-006-16 | El usuario abre la creación de una póliza nueva. | El editor inicia con exactamente una partida vacía lista para capturar. Al editar una póliza se muestran sus partidas conservadas y no se agrega una partida vacía implícita. |
| CA-006-17 | En una partida capturada, el usuario termina un cargo o abono y presiona `Enter`. | Si la partida tiene una cuenta operable y exactamente uno de cargo o abono contiene un importe positivo válido, queda disponible una sola partida vacía posterior: se agrega al final cuando no existe y el foco pasa a su control de cuenta. `Enter` no guarda ni contabiliza la póliza. Si la partida no es válida, no se agrega otra y la captura actual se conserva para corregirla. |
| CA-006-18 | El usuario captura una póliza en un viewport de escritorio de al menos 1280 píxeles CSS de ancho. | Puede ver y operar los campos, totales y acciones del editor sin scroll horizontal en el diálogo ni en la tabla de partidas. En anchos menores, el contenido sigue siendo operable y puede recurrir a desplazamiento horizontal sin quedar cortado. |
| CA-006-19 | CUANDO el usuario busca CFDI al crear o editar una póliza. | EL SISTEMA filtra localmente los CFDI ya cargados para el periodo elegido por coincidencia parcial en UUID, RFC, razón social, serie o folio, sin distinguir mayúsculas, minúsculas ni acentos. La lista muestra fecha, tipo, UUID, contraparte y vínculos existentes; permite seleccionar varios CFDI mediante casillas, conserva selecciones ocultas temporalmente por la búsqueda y muestra recuento o estado sin resultados. Los CFDI relacionados con otras pólizas siguen disponibles; los vínculos preexistentes de otros periodos se conservan al editar. |
| CA-006-20 | CUANDO se abre «CFDI relacionados» en una póliza del periodo. | EL SISTEMA presenta en una ventana los CFDI emitidos en ese periodo, con búsqueda y selección múltiple; conserva el orden de selección y muestra relaciones anteriores aunque correspondan a otro periodo. «Continuar» no guarda la póliza. La búsqueda y selección previa de CA-006-19 se mantienen dentro de la ventana para los CFDI del periodo. |
| CA-006-21 | CUANDO se continúa con uno o varios CFDI `I` o `E` en MXN cuyos datos fiscales cuadran. | EL SISTEMA prellena bloques consecutivos de partidas por CFDI en el orden elegido: total, subtotal, descuento e impuestos presentes por tipo y naturaleza, con importes y lado cargo/abono según dirección y tipo. Las cuentas no conocidas quedan vacías y cada importe puede corregirse antes de guardar. |
| CA-006-22 | SI un CFDI seleccionado no cuadra con su total, es tipo `P` o usa otra moneda. | EL SISTEMA muestra su UUID y motivo. Un descuadre detiene la generación de ese CFDI sin ajuste ficticio; `P` y moneda distinta de MXN permiten relación y captura manual, sin generación. Los demás CFDI válidos pueden continuar. |
| CA-006-23 | CUANDO el contador asigna cuentas a partidas generadas y guarda una póliza válida DRAFT o POSTED. | EL SISTEMA conserva el origen opcional de cada partida y una sugerencia por empresa, emisor, dirección, tipo, PUE/PPD y componente; al volver a seleccionar un CFDI equivalente propone esas cuentas con sus propios importes. En conflictos de una misma póliza prevalece la última partida. |
| CA-006-24 | CUANDO varios CFDI del mismo emisor están en la misma captura y el contador asigna una cuenta al primer bloque. | EL SISTEMA aplica esa cuenta a las partidas equivalentes posteriores aún vacías sin alterar importes ni elecciones manuales. Una póliza contabilizada sigue exigiendo cuentas válidas y balance autoritativo. |

## Requisitos no funcionales aplicables

- Aislamiento, integridad y precisión: CA-006-03/04/08/12 y DT-011; accesibilidad y layout del editor: CA-006-14/15/18.

## Casos límite

- Póliza descuadrada, cuenta o CFDI ajeno, fecha inválida, CFDI sin propuesta y error parcial por CFDI: CA-006-02/03/08/14/22.

## Fuera de alcance

No incluye contabilización directa al continuar, tratamientos fiscales prescritos, estados adicionales, cierre/reversión ni auditoría histórica completa.

## Decisiones, supuestos y dudas

### Decisiones cerradas

- La póliza obtiene un número consecutivo automático, único por empresa, periodo y tipo. La fecha debe pertenecer al periodo seleccionado.
- Un borrador exige tipo, fecha y concepto, y puede no tener partidas. Una póliza `POSTED` exige al menos dos partidas, cuentas activas que acepten movimientos, un único cargo o abono positivo por partida, total positivo y cargos iguales a abonos usando seis decimales.
- `POSTED` puede editarse, pero cualquier actualización debe continuar balanceada y conserva su estado. La creación y actualización conservan creador, último editor y marcas de tiempo.
- Las relaciones de CFDI son opcionales, solo pueden usar documentos de la misma empresa y pueden cruzar periodos. La relación es con la póliza, no con cada partida.
- La columna Día del editor es la fecha de la póliza derivada para cada renglón; no se almacena como atributo de partida.
- La fecha de la póliza usa un control de calendario accesible y legible en español, limitado visualmente al periodo seleccionado y presentado como una capa que no altera el layout. El periodo se comunica dentro del calendario, por su contenido y etiquetas accesibles, y mediante errores cuando corresponda; no se conserva un texto instructivo permanente. La validación autoritativa de pertenencia al periodo permanece en backend.
- Una póliza nueva presenta una partida vacía inicial. La creación automática de la siguiente partida es sólo una ayuda de captura: exige cuenta operable y un único importe positivo válido, evita duplicar renglones vacíos y no sustituye la validación al guardar.
- El editor aprovecha el ancho disponible en escritorio para mantener visible una fila completa durante la captura normal; la adaptación a pantallas menores no elimina campos ni acciones.
- La relación de CFDI se localiza en frontend sobre la colección ya autorizada y cargada del periodo. La búsqueda es parcial e insensible a mayúsculas, minúsculas y acentos en UUID, RFC, razón social, serie y folio; no busca por fecha o importe, no pagina ni genera solicitudes adicionales. Las casillas no excluyen CFDI ya relacionados y una selección permanece al cambiar temporalmente el filtro.
- La nueva selección usa exclusivamente CFDI emitidos en el periodo elegido; los vínculos previos de otros periodos se conservan y muestran al editar. El orden de selección define los bloques generados. La memoria de cuentas no aplica automáticamente tratamiento fiscal ni contabiliza la póliza.
- Para `I` emitido se propone cargo a total y descuento, abono a subtotal y traslados, y cargo a retenciones; recibido invierte los lados y `E` invierte la orientación de `I`. Cada impuesto y naturaleza presente forma partida propia; los importes cero no la crean. La reconciliación usa seis decimales exactos y rechaza sólo el CFDI descuadrado.

### Pendientes y decisiones

- **Resuelto para esta entrega:** numeración, fecha/periodo, mínimos DRAFT/POSTED, precisión decimal, cuentas operables, edición POSTED y relación de CFDI por póliza.
- **Supuesto para validar:** DRAFT puede estar incompleta/descuadrada (BR-006/OQ-002/AC-011). Se mantiene la exigencia de balance para POSTED.
- **Posterior:** estados CANCELLED/REVERSED, tipos adicionales, cierre, provisiones automáticas y auditoría histórica de campos. No inventar bloqueo ni permiso de edición POSTED para resolver su pendiente.
- **Reinicio autorizado de datos de prueba:** en todos los entornos, mediante operación única con respaldo y recuento previos, eliminar los CFDI existentes y las pólizas de prueba que los referencian con sus partidas; conservar empresas, periodos, cuentas y pólizas no vinculadas. No ejecutar este borrado desde una migración repetible.

## Criterios de finalización

- Los criterios de esta entrega deben tener implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §9](../../docs/planeacion/003%20-%20MVP-Scope.md#9-p%C3%B3lizas-contables), [Alcance §10](../../docs/planeacion/003%20-%20MVP-Scope.md#10-partidas-contables), [Alcance §11](../../docs/planeacion/003%20-%20MVP-Scope.md#11-relaci%C3%B3n-xml--p%C3%B3liza), [Alcance §12](../../docs/planeacion/003%20-%20MVP-Scope.md#12-ingresos), [Alcance §13](../../docs/planeacion/003%20-%20MVP-Scope.md#13-egresos), [Alcance §14](../../docs/planeacion/003%20-%20MVP-Scope.md#14-pue), [Alcance §17](../../docs/planeacion/003%20-%20MVP-Scope.md#17-auditor%C3%ADa-m%C3%ADnima) (pólizas, partidas, relaciones, captura manual y auditoría).
- [BR-002](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#4-br-002--el-contador-trabaja-dentro-de-un-periodo), [BR-003](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#5-br-003--cada-empresa-tiene-su-propio-cat%C3%A1logo-de-cuentas), [BR-004](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#6-br-004--cada-partida-utiliza-una-cuenta-contable), [BR-005](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#7-br-005--una-p%C3%B3liza-contabilizada-debe-estar-balanceada), [BR-006](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#8-br-006--una-p%C3%B3liza-incompleta-puede-guardarse-como-borrador), [BR-007](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#9-br-007--una-p%C3%B3liza-puede-relacionarse-con-varios-xml), [BR-008](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#10-br-008--un-xml-puede-relacionarse-con-varias-p%C3%B3lizas), [BR-009](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#11-br-009--una-p%C3%B3liza-puede-existir-sin-xml), [BR-016](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#18-br-016--el-contador-selecciona-manualmente-las-cuentas-contables), [BR-018](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#20-br-018--debe-existir-trazabilidad-desde-el-xml), [BR-019](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#21-br-019--debe-existir-trazabilidad-desde-la-p%C3%B3liza). BR-006 es SUPUESTO MVP; las demás están confirmadas en su alcance.
- [AC-001](../../docs/planeacion/004%20-%20Escenarios%20contables.md#3-escenario-ac-001--ingreso-pue), [AC-002](../../docs/planeacion/004%20-%20Escenarios%20contables.md#4-escenario-ac-002--egreso-pue), [AC-006](../../docs/planeacion/004%20-%20Escenarios%20contables.md#8-escenario-ac-006--varios-xml-en-una-misma-p%C3%B3liza), [AC-007](../../docs/planeacion/004%20-%20Escenarios%20contables.md#9-escenario-ac-007--un-xml-relacionado-con-varias-p%C3%B3lizas), [AC-008](../../docs/planeacion/004%20-%20Escenarios%20contables.md#10-escenario-ac-008--p%C3%B3liza-sin-cfdi), [AC-011](../../docs/planeacion/004%20-%20Escenarios%20contables.md#13-escenario-ac-011--p%C3%B3liza-descuadrada-en-borrador), [AC-012](../../docs/planeacion/004%20-%20Escenarios%20contables.md#14-escenario-ac-012--consulta-de-trazabilidad-desde-un-cfdi), [AC-013](../../docs/planeacion/004%20-%20Escenarios%20contables.md#15-escenario-ac-013--consulta-de-trazabilidad-desde-una-p%C3%B3liza). AC-001/002/008 tienen detalles pendientes; AC-011 es supuesto.
- [OQ-002](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#4-oq-002--borradores-de-p%C3%B3lizas-descuadradas), [OQ-008](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#10-oq-008--estados-adicionales-de-accountingpolicy), [OQ-010](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#12-oq-010--tipos-adicionales-de-p%C3%B3liza), [OQ-013](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#15-oq-013--supplier-y-customer-como-entidades); [Análisis §10: numeración todavía abierta](../../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#10-p%C3%B3lizas-contables).
