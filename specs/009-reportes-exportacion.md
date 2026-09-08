# SPEC-009 — Reportes y exportación

**Estado:** Lista
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-002](002-contexto-contable.md), [SPEC-004](004-documentos-fiscales.md), [SPEC-006](006-polizas-trazabilidad.md), [SPEC-008](008-balanza-basica.md)

## Propósito y alcance

Consultar reportes básicos de XML, pólizas con partidas y balanza; exportar los reportes principales a Excel para revisar y compartir información. Cubrir los tres reportes del alcance §16.

No incluye diseñador de reportes, dashboards, comparaciones entre empresas, DIOT ni archivos de contabilidad electrónica.

## Fuentes

- [Alcance §16: reportes y exportación](../docs/planeacion/003%20-%20MVP-Scope.md#16-reportes-incluidos); [§18: recorrido completo](../docs/planeacion/003%20-%20MVP-Scope.md#18-flujo-completo-que-debe-demostrar-el-mvp); [§21: reportería avanzada excluida](../docs/planeacion/003%20-%20MVP-Scope.md#21-fuera-del-mvp).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-017](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#19-br-017--las-p%C3%B3lizas-contabilizadas-afectan-la-balanza) (aislamiento y fuente de movimientos contabilizados).

## Comportamiento y criterios de aceptación

El usuario operativo selecciona el contexto, consulta el reporte y solicita exportación a Excel; el administrador accede a cualquier empresa y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. Documentos, pólizas y balanza provienen de sus contratos responsables; la exportación no redefine el cálculo ni las reglas de consulta.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-009-01 | El contador consulta el reporte de XML de su contexto. | Ve el listado y datos principales definidos en SPEC-004. |
| CA-009-02 | El contador consulta el reporte de pólizas. | Ve las pólizas DRAFT y POSTED y sus partidas según SPEC-006, dentro del periodo seleccionado. |
| CA-009-03 | El contador consulta el reporte de balanza. | Ve los mismos datos y cálculo definidos en SPEC-008, excluyendo efectos de borradores. |
| CA-009-04 | Se exporta cada uno de los tres reportes principales. | Se obtiene un archivo utilizable en Excel con los datos del contexto y filtros acordados, consistente con la consulta correspondiente. |
| CA-009-05 | Se intenta consultar o exportar datos de una empresa sin acceso. | No se entrega información ni un archivo con datos de esa empresa. |
| CA-009-06 | Se exportan importes y referencias del reporte preparado. | Los valores conservan la precisión y representación acordadas; la exportación no recalcula saldos mediante reglas independientes. |

## Pendientes y decisiones

- **Resuelto para esta entrega:** tres archivos XLSX separados, una hoja por archivo, periodo obligatorio en la ruta, consulta completa del periodo sin filtros adicionales, pólizas DRAFT/POSTED y balanza únicamente con movimientos POSTED.
- **Resuelto para esta entrega:** el límite es de 10,000 filas de datos por archivo; una consulta vacía devuelve un XLSX válido con encabezados y sin datos; superar el límite devuelve `422` JSON sin archivo.
- **Resuelto para esta entrega:** los archivos son síncronos, usan MIME `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, nombres `xml-{year}-{month}.xlsx`, `polizas-{year}-{month}.xlsx` y `balanza-{year}-{month}.xlsx`, y no contienen fórmulas.
- **Validación durante MVP:** que los tres reportes y archivos permiten revisar el flujo principal con los contadores.
- **Posterior:** formatos fiscales oficiales, personalización avanzada, dashboards y comparación entre empresas.

## Plan técnico y contratos

- Backend: consume los contratos de SPEC-004/006/008 y expone `GET /api/companies/{companyId}/accounting-periods/{periodId}/reports/{report}.xlsx`, donde `report` es `fiscal-documents`, `accounting-policies` o `trial-balance`.
- El contrato de filas usa columnas estables y este orden: XML `issued_at`, `document_type`, `direction`, `issuer_rfc`, `issuer_name`, `recipient_rfc`, `recipient_name`, `uuid`, `series`, `folio`, `payment_method`, `payment_form`, `currency`, `exchange_rate`, `subtotal`, `tax_total`, `total`, `accounted`; pólizas `entry_date`, `type`, `display_number`, `status`, `policy_concept`, `position`, `account_code`, `account_name`, `entry_concept`, `reference`, `debit`, `credit`; balanza `code`, `name`, `nature`, `opening_balance`, `debit_total`, `credit_total`, `closing_balance`.
- Las filas XML se ordenan por `issued_at` descendente e `id` descendente; las pólizas por `entry_date` descendente e `id` descendente y sus partidas por `position` ascendente; la balanza conserva el orden de SPEC-008. Una póliza sin partidas genera una fila con campos de partida vacíos.
- Todos los importes se escriben como texto con seis decimales; fechas e identificadores se escriben como texto; los valores booleanos usan `true`/`false`. La exportación no recalcula saldos ni agrega fórmulas.
- Frontend: añade una acción de exportar a cada vista existente, usando el periodo visible y mostrando errores sin abandonar el contexto.
- El XLSX se genera con las extensiones nativas disponibles, sin añadir dependencias ni migraciones.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). El contrato de exportación queda cerrado para el alcance MVP; cualquier filtro, formato adicional o procesamiento asíncrono posterior debe actualizar esta spec antes de modificar consumidores.

## Verificación

**Evidencia de producto:** implementación realizada el 2026-09-08 en los árboles de trabajo. `tests/Feature/Spec009Test.php` pasó con 6 pruebas y 79 aserciones focalizadas; la suite backend completa pasó con 60 pruebas y 519 aserciones. `pnpm lint`, `pnpm typecheck` y `pnpm build` pasaron en frontend. `vendor/bin/pint --dirty --format agent` corrigió únicamente el formato de los archivos nuevos y `git diff --check` no reporta errores.

La cobertura verifica los tres MIME/nombres/contenidos XLSX, columnas y orden, precisión decimal, aislamiento por empresa y periodo, DRAFT/POSTED en pólizas, exclusión de DRAFT en balanza, archivos vacíos, autenticación/autorización y el límite de 10,000 filas. La comprobación interactiva de los botones y la apertura manual en Excel siguen pendientes por la restricción vigente de no usar navegador ni Playwright.

**Revisiones de implementación:** backend parte de `829837d` y frontend de `ca15edd`; la implementación de SPEC-009 permanece como cambio local posterior a esas revisiones. La documentación parte de `4e38ac5` con cambios locales conservados.

Prever comparación de datos consultados/exportados en los tres reportes, apertura del formato elegido en una herramienta compatible, valores decimales e intento de exportación de una empresa no asignada. Completar el recorrido extremo a extremo descrito en el índice.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance de reportes.
- **2026-09-08:** se cerró el contrato MVP de tres exportaciones XLSX separadas, columnas estables, contexto por periodo, estados de pólizas, límite de filas y errores observables. SPEC-009 pasa a Lista.
- **2026-09-08:** se implementaron las tres rutas XLSX, generación nativa sin dependencias, botones de frontend y pruebas de contrato. Permanece pendiente la comprobación interactiva por la restricción de no usar navegador.
