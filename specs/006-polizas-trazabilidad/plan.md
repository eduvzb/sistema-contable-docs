# Plan técnico — SPEC-006

Este archivo describe la ejecución técnica de [SPEC-006](spec.md); los criterios funcionales vigentes y el estado sólo se definen allí.

## Contexto para ejecución

El alcance y los criterios de esta entrega están en [spec.md](spec.md); las tareas abiertas por repositorio identifican el trabajo pendiente. Consulta los contratos de las specs dependientes que esta ejecución consume. Las fuentes ya citadas en `spec.md` se reabren sólo ante una contradicción, un cambio posterior de regla o contrato, un supuesto que afecte el resultado, o una solicitud explícita de cambiar comportamiento.

## Antecedentes de diseño

### Análisis de hallazgos 2026-09-12

| Hallazgo | Comportamiento actual que falla o puede mejorar | Comportamiento esperado | Impacto documental | Componentes |
|---|---|---|---|---|
| El calendario expande el editor y genera scroll; además muestra un copy que debe retirarse. | El calendario vive dentro de un contenedor desplazable y el texto de ayuda ocupa espacio permanente, por lo que abrirlo puede alterar el layout. | El calendario se superpone sin cambiar dimensiones ni scroll según CA-006-14/15; se elimina el copy indicado sin retirar los errores localizados ni las etiquetas accesibles. | Se modifica CA-006-14 y se agrega CA-006-15; se ajusta la decisión local del calendario. | Frontend. La validación autoritativa de fecha del backend no cambia. |
| La creación inicia sin partidas. | El usuario debe accionar “Agregar partida” antes de comenzar la captura. | Una póliza nueva abre con una partida vacía; la edición no altera las partidas persistidas, según CA-006-16. | Se agrega CA-006-16 y una decisión local. | Frontend. El payload y las reglas DRAFT/POSTED no cambian. |
| `Enter` en cargo o abono no continúa la captura. | Terminar un importe no crea ni enfoca el siguiente renglón. | Una partida válida al final crea exactamente un renglón vacío y mueve el foco según CA-006-17, sin disparar el guardado. | Se agrega CA-006-17 y se define qué significa “partida válida” para esta interacción. | Frontend. El backend sigue validando autoritativamente al guardar. |
| El editor requiere scroll horizontal durante la captura normal. | El diálogo disponible es menor que el ancho mínimo de la tabla, por lo que campos y acciones quedan fuera de vista. | En escritorio desde 1280 px se ve la captura completa sin scroll horizontal; en anchos menores se preserva operabilidad según CA-006-18. | Se agrega CA-006-18 y una decisión local de presentación. | Frontend. |
| El selector múltiple nativo no permite encontrar rápidamente un CFDI relacionado. | Todos los CFDI de la empresa se concentran en un único control, sin filtrar por sus identificadores o contraparte y con información difícil de recorrer. | Una lista filtrable y seleccionable muestra los datos necesarios y conserva las relaciones elegidas según CA-006-19. | Se agrega CA-006-19 y una decisión local de búsqueda; no cambia el contrato ni la autorización. | Frontend. |

## Plan técnico y contratos

- Backend: contratos de póliza/partidas, contabilización y relaciones con CFDI, dentro de una transacción; valida contexto, cuentas y empresa mediante SPEC-002/003/004.
- Frontend: editor ancho con encabezado, calendario de fecha superpuesto y error próximo al control, tabla de partidas, relaciones CFDI, totales y acciones separadas para borrador/contabilización. La relación CFDI usa la colección ya cargada, un filtro local accesible y casillas que preservan sus IDs al cambiar la búsqueda. El calendario debe ser operable con puntero y teclado y conservar el resto del formulario ante un error. La creación inicia con una partida vacía; `Enter` en el importe de una última partida válida prepara y enfoca la siguiente sin enviar el formulario. Las reglas vienen del backend.
- Pruebas frontend: incorporar la configuración mínima de Vitest con `jsdom`, React Testing Library, `@testing-library/user-event` y matchers de `@testing-library/jest-dom`, ejecutable mediante `pnpm test`. Cubrir `AccountingPolicyEditor` en su frontera de componente, sustituyendo la API y demás dependencias externas necesarias para observar el comportamiento sin levantar backend ni navegador.
- SPEC-004 consume las relaciones `POSTED` para su indicador; SPEC-007 agrega pagos y SPEC-008 consume las partidas contabilizadas sin duplicar contratos.
- `POST /api/companies/{companyId}/accounting-periods/{periodId}/accounting-policy-entry-previews` recibe `fiscal_document_ids` ordenados y devuelve partidas propuestas por CFDI, componentes de origen, cuentas sugeridas y errores identificados por UUID. No persiste pólizas. Los contratos de guardar póliza agregan origen opcional por partida (`source_fiscal_document_id`, `source_component_key`), validado contra los documentos relacionados y la empresa; el origen se devuelve al consultar. Guardar actualiza la memoria de cuentas en la misma transacción.

### Contrato de trazabilidad inversa CFDI → pólizas → partidas → cuentas → periodos

El detalle existente `GET /api/companies/{companyId}/fiscal-documents/{fiscalDocumentId}` conserva los campos fiscales definidos por SPEC-004 y agrega `accounting_policies`. El listado de CFDI no expone esta colección para evitar cargar la trazabilidad completa en la bandeja.

Cada elemento de `accounting_policies` incluye `id`, `company_id`, `accounting_period_id`, `type`, `number`, `display_number`, `entry_date`, `concept`, `status`, un objeto `period` con `id`, `year`, `month` y `status`, y `entries`. Cada elemento de `entries` incluye `id`, `position`, `account_id`, un objeto `account` con `id`, `code` y `name`, `concept`, `reference`, `debit` y `credit`. Los importes conservan seis decimales como texto.

La colección contiene todas las pólizas relacionadas con el CFDI, incluidas relaciones entre periodos, ordenadas por `entry_date` descendente y después `id` descendente; las partidas se ordenan por `position` ascendente. Un CFDI sin relaciones devuelve `accounting_policies: []`. Una póliza sin CFDI no se incluye desde ningún detalle de CFDI. La relación contable no asigna partidas individuales a CFDI; el origen opcional de una partida generada sólo conserva la procedencia de su propuesta.

El contrato se autoriza con el acceso a la empresa del CFDI. Un usuario sin acceso o una empresa distinta recibe el mismo `404` que el detalle actual; no se exponen pólizas, partidas, cuentas ni periodos fuera de la empresa visible. La consulta utiliza carga anticipada de las relaciones necesarias y no cambia las reglas de contabilización ni el cálculo de SPEC-008.

Aplican las [decisiones técnicas compartidas](../../docs/decisiones.md). El contrato de trazabilidad inversa de esta brecha queda cerrado; cualquier ampliación posterior debe actualizar esta spec antes de modificar consumidores.

## Decisiones técnicas conservadas

- La actualización frontend se verifica conforme a DT-012 con Vitest, entorno `jsdom`, React Testing Library y simulación de interacción de usuario. Las pruebas se expresan mediante roles, etiquetas, foco, contenido y efectos observables; no acoplan la cobertura a estado interno ni sustituyen con snapshots los criterios de comportamiento. Playwright y las pruebas integrales por navegador no son requisito de cierre de esta actualización.

## Orden y coordinación

Las tareas pendientes se registran por repositorio en [backend](tasks-backend.md) y [frontend](tasks-frontend.md). El contrato responsable se prepara antes de implementarlo en un consumidor; las comprobaciones reales se registran en [verificación](verificacion.md).
