# SPEC-006 — Pólizas y trazabilidad

**Estado:** Lista
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md), [SPEC-003](003-catalogo-cuentas.md), [SPEC-004](004-documentos-fiscales.md)

## Propósito y alcance

Crear, consultar y modificar pólizas con partidas manuales; guardarlas como borrador y contabilizarlas balanceadas. Conservar documentos relacionados, cuentas, empresa, periodo y autoría básica.

Incluye tipos INGRESO/EGRESO/DIARIO, estados DRAFT/POSTED, relaciones XML opcionales y múltiples, trazabilidad bidireccional, ingresos/egresos PUE y representación manual del registro inicial PPD. No incluye selección automática de cuentas, tratamientos fiscales prescritos, estados adicionales, cierre/reversión ni auditoría histórica completa. La edición posterior a contabilización requiere una decisión antes de Lista.

## Fuentes

- [Alcance §9](../docs/planeacion/003%20-%20MVP-Scope.md#9-p%C3%B3lizas-contables), [Alcance §10](../docs/planeacion/003%20-%20MVP-Scope.md#10-partidas-contables), [Alcance §11](../docs/planeacion/003%20-%20MVP-Scope.md#11-relaci%C3%B3n-xml--p%C3%B3liza), [Alcance §12](../docs/planeacion/003%20-%20MVP-Scope.md#12-ingresos), [Alcance §13](../docs/planeacion/003%20-%20MVP-Scope.md#13-egresos), [Alcance §14](../docs/planeacion/003%20-%20MVP-Scope.md#14-pue), [Alcance §17](../docs/planeacion/003%20-%20MVP-Scope.md#17-auditor%C3%ADa-m%C3%ADnima) (pólizas, partidas, relaciones, captura manual y auditoría).
- [BR-002](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#4-br-002--el-contador-trabaja-dentro-de-un-periodo), [BR-003](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#5-br-003--cada-empresa-tiene-su-propio-cat%C3%A1logo-de-cuentas), [BR-004](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#6-br-004--cada-partida-utiliza-una-cuenta-contable), [BR-005](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#7-br-005--una-p%C3%B3liza-contabilizada-debe-estar-balanceada), [BR-006](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#8-br-006--una-p%C3%B3liza-incompleta-puede-guardarse-como-borrador), [BR-007](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#9-br-007--una-p%C3%B3liza-puede-relacionarse-con-varios-xml), [BR-008](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#10-br-008--un-xml-puede-relacionarse-con-varias-p%C3%B3lizas), [BR-009](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#11-br-009--una-p%C3%B3liza-puede-existir-sin-xml), [BR-016](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#18-br-016--el-contador-selecciona-manualmente-las-cuentas-contables), [BR-018](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#20-br-018--debe-existir-trazabilidad-desde-el-xml), [BR-019](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#21-br-019--debe-existir-trazabilidad-desde-la-p%C3%B3liza). BR-006 es SUPUESTO MVP; las demás están confirmadas en su alcance.
- [AC-001](../docs/planeacion/004%20-%20Escenarios%20contables.md#3-escenario-ac-001--ingreso-pue), [AC-002](../docs/planeacion/004%20-%20Escenarios%20contables.md#4-escenario-ac-002--egreso-pue), [AC-006](../docs/planeacion/004%20-%20Escenarios%20contables.md#8-escenario-ac-006--varios-xml-en-una-misma-p%C3%B3liza), [AC-007](../docs/planeacion/004%20-%20Escenarios%20contables.md#9-escenario-ac-007--un-xml-relacionado-con-varias-p%C3%B3lizas), [AC-008](../docs/planeacion/004%20-%20Escenarios%20contables.md#10-escenario-ac-008--p%C3%B3liza-sin-cfdi), [AC-011](../docs/planeacion/004%20-%20Escenarios%20contables.md#13-escenario-ac-011--p%C3%B3liza-descuadrada-en-borrador), [AC-012](../docs/planeacion/004%20-%20Escenarios%20contables.md#14-escenario-ac-012--consulta-de-trazabilidad-desde-un-cfdi), [AC-013](../docs/planeacion/004%20-%20Escenarios%20contables.md#15-escenario-ac-013--consulta-de-trazabilidad-desde-una-p%C3%B3liza). AC-001/002/008 tienen detalles pendientes; AC-011 es supuesto.
- [OQ-002](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#4-oq-002--borradores-de-p%C3%B3lizas-descuadradas), [OQ-008](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#10-oq-008--estados-adicionales-de-accountingpolicy), [OQ-010](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#12-oq-010--tipos-adicionales-de-p%C3%B3liza), [OQ-013](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#15-oq-013--supplier-y-customer-como-entidades); [Análisis §10: numeración todavía abierta](../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#10-p%C3%B3lizas-contables).

## Comportamiento y criterios de aceptación

El usuario operativo crea una póliza con o sin XML, selecciona cuentas y registra partidas. El administrador accede a cualquier empresa y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. La póliza contiene fecha, tipo, número, concepto, partidas, documentos y estado; las partidas contienen cuenta, cargo, abono, concepto y referencia según alcance §9/10. Empresa/periodo vienen de SPEC-002. Se permite guardar incompleta como DRAFT (supuesto); la contabilización exige cargos = abonos.

Las relaciones permiten varios XML por póliza y varias pólizas por XML, incluso entre periodos. Desde cada lado se puede consultar el otro y recorrer las partidas/cuentas de la póliza. No se infiere una asignación por partida a cada XML: esa granularidad debe aclararse si se necesita. Proveedor/cliente no requieren entidades propias en el MVP (OQ-013).

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
| CA-006-13 | El contador modifica manualmente cuentas o partidas de una póliza cuya edición está permitida. | Los cambios válidos se conservan y pueden consultarse, manteniendo las validaciones y auditoría aplicables. La política de edición de POSTED debe resolverse antes de Lista. |

## Decisiones cerradas

- La póliza obtiene un número consecutivo automático, único por empresa, periodo y tipo. La fecha debe pertenecer al periodo seleccionado.
- Un borrador exige tipo, fecha y concepto, y puede no tener partidas. Una póliza `POSTED` exige al menos dos partidas, cuentas activas que acepten movimientos, un único cargo o abono positivo por partida, total positivo y cargos iguales a abonos usando seis decimales.
- `POSTED` puede editarse, pero cualquier actualización debe continuar balanceada y conserva su estado. La creación y actualización conservan creador, último editor y marcas de tiempo.
- Las relaciones de CFDI son opcionales, solo pueden usar documentos de la misma empresa y pueden cruzar periodos. La relación es con la póliza, no con cada partida.
- La columna Día del editor es la fecha de la póliza derivada para cada renglón; no se almacena como atributo de partida.

## Pendientes y decisiones

- **Resuelto para esta entrega:** numeración, fecha/periodo, mínimos DRAFT/POSTED, precisión decimal, cuentas operables, edición POSTED y relación de CFDI por póliza.
- **Supuesto para validar:** DRAFT puede estar incompleta/descuadrada (BR-006/OQ-002/AC-011). Se mantiene la exigencia de balance para POSTED.
- **Posterior:** estados CANCELLED/REVERSED, tipos adicionales, cierre, provisiones automáticas y auditoría histórica de campos. No inventar bloqueo ni permiso de edición POSTED para resolver su pendiente.

## Plan técnico y contratos

- Backend: contratos de póliza/partidas, contabilización y relaciones con CFDI, dentro de una transacción; valida contexto, cuentas y empresa mediante SPEC-002/003/004.
- Frontend: modal ancho con encabezado, tabla de partidas, relaciones CFDI, totales y acciones separadas para borrador/contabilización. Las reglas vienen del backend.
- SPEC-004 consume las relaciones `POSTED` para su indicador; SPEC-007 agrega pagos y SPEC-008 consume las partidas contabilizadas sin duplicar contratos.

### Contrato de trazabilidad inversa CFDI → pólizas → partidas → cuentas → periodos

El detalle existente `GET /api/companies/{companyId}/fiscal-documents/{fiscalDocumentId}` conserva los campos fiscales definidos por SPEC-004 y agrega `accounting_policies`. El listado de CFDI no expone esta colección para evitar cargar la trazabilidad completa en la bandeja.

Cada elemento de `accounting_policies` incluye `id`, `company_id`, `accounting_period_id`, `type`, `number`, `display_number`, `entry_date`, `concept`, `status`, un objeto `period` con `id`, `year`, `month` y `status`, y `entries`. Cada elemento de `entries` incluye `id`, `position`, `account_id`, un objeto `account` con `id`, `code` y `name`, `concept`, `reference`, `debit` y `credit`. Los importes conservan seis decimales como texto.

La colección contiene todas las pólizas relacionadas con el CFDI, incluidas relaciones entre periodos, ordenadas por `entry_date` descendente y después `id` descendente; las partidas se ordenan por `position` ascendente. Un CFDI sin relaciones devuelve `accounting_policies: []`. Una póliza sin CFDI no se incluye desde ningún detalle de CFDI. La relación no asigna partidas individuales a CFDI.

El contrato se autoriza con el acceso a la empresa del CFDI. Un usuario sin acceso o una empresa distinta recibe el mismo `404` que el detalle actual; no se exponen pólizas, partidas, cuentas ni periodos fuera de la empresa visible. La consulta utiliza carga anticipada de las relaciones necesarias y no cambia las reglas de contabilización ni el cálculo de SPEC-008.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). El contrato de trazabilidad inversa de esta brecha queda cerrado; cualquier ampliación posterior debe actualizar esta spec antes de modificar consumidores.

## Verificación

**Evidencia de producto:** implementación backend y frontend realizada el 2026-09-08. `./vendor/bin/sail artisan test --compact` pasó con 42 pruebas y 350 aserciones; la suite incluye 10 pruebas y 58 aserciones focalizadas en SPEC-006, con CFDI sin pólizas, una y varias pólizas entre periodos, partidas/cuentas, pólizas sin CFDI, aislamiento entre empresas y usuario sin acceso. `pnpm lint`, `pnpm typecheck` y `pnpm build` pasaron. No se ejecutó navegador, Playwright ni E2E por la restricción vigente.

**Evidencia de continuidad 2026-09-08:** `./vendor/bin/sail artisan test --compact tests/Feature/Spec006Test.php` pasó con 15 pruebas y 114 aserciones. Cubre rechazo y rollback de cuenta o CFDI de otra empresa, `404` al consultar/modificar/contabilizar sin autorización, conservación de `created_by`, cambio correcto de `updated_by`, marcas de tiempo, edición balanceada de `POSTED` y serialización exacta de `999999999999.999999` a seis decimales tanto desde póliza como desde detalle fiscal. La regresión completa pasó con 72 pruebas y 650 aserciones.

**Revisiones de implementación:** backend parte de `868b20eaaa24c387e7e80f97a5798f024a4582e4` y frontend de `597bdc5f71c2ee071ce173ddc81167f2a7461bd7`; estas correcciones permanecen como cambios locales posteriores a esos commits. La documentación parte de `4e38ac5cc0b7dd2cd6900f49cb8b7ed48b127410` con cambios locales conservados. Al confirmar esta revisión documental, su hash real debe registrarse en `SPEC_REVISION` de ambos consumidores.

La suite cubre DRAFT desbalanceada, rechazo de POSTED desbalanceada, póliza balanceada, ausencia y multiplicidad de XML, cuentas/XML de otra empresa, autorización, auditoría mínima y edición válida de POSTED. Permanecen pendientes los recorridos interactivos y los escenarios manuales de ingreso/egreso que exigen navegador.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar reglas de pólizas.

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-08:** se prepara la implementación con editor tabular: numeración por empresa–periodo–tipo, fecha dentro del periodo, DRAFT sin partidas, POSTED balanceada editable y relaciones CFDI por póliza. Pasa a Lista; la evidencia se registra después de implementar.
- **2026-09-08:** se implementaron pólizas, partidas y relaciones con CFDI, junto con la evidencia automatizada aplicable.
- **2026-09-08:** se cerró el contrato de trazabilidad inversa CFDI → pólizas → partidas → cuentas → periodos; se implementó en el detalle del CFDI con aislamiento por empresa y cobertura automatizada. Permanece pendiente la comprobación interactiva por la restricción de no usar navegador.
- **2026-09-08:** se eliminó el uso de `float` en recursos de importes y totales, y se amplió la cobertura de aislamiento, atomicidad, autorización, auditoría y edición balanceada de pólizas contabilizadas.
