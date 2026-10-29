# Plan técnico — SPEC-011

La definición y el estado vigentes están en [spec.md](spec.md). La actualización del 2026-10-28 cubre CA-011-10/11 revisados y CA-011-14/15/16. Las secciones 1 a 3 conservan los contratos base, sin trabajo nuevo sobre importación o contabilización. Los contratos modificados están en las secciones 4 en adelante; su implementación local y las comprobaciones reales se acreditan únicamente en [verificacion.md](verificacion.md).

## Evidencia de partida

- `app/Support/DiotReportService.php::rows` agrupa actualmente por RFC/factor/tasa y devuelve cadenas a seis decimales. Ya relaciona inclusiones con pólizas POSTED y filtra empresa y periodo, pero no expone la póliza ni un total.
- `app/Http/Controllers/DiotReportController.php` comparte esas filas entre JSON y XLSX; limita sólo el XLSX a 10,000 filas. `AccountingPolicyResource` expone `display_number` con relleno mínimo de seis posiciones a la izquierda con ceros.
- `src/features/reports/components/diot-report.tsx` obtiene el array completo y muestra RFC, factor, tasa, base e IVA sin paginar ni totalizar. Su prueba cubre carga de datos, vacío, error, respuestas tardías y descarga. `reports-api.ts::getDiot` desenvuelve `data`; `DiotRow` vive actualmente en `src/shared/contracts/index.ts` y se reexporta en `reports.ts`.
- La evidencia de las pruebas de la entrega anterior se conserva en [verificacion.md](verificacion.md); no demuestra el cambio de agrupación ni la UI nueva.

## Contratos y datos

### 1. Captura fiscal adicional — CA-011-02/04/05/13

SPEC-004 sigue siendo responsable de importación; esta entrega añade a `fiscal_documents` un JSON nullable `diot_tax_lines`, expuesto aditivamente en lista y detalle. `null` significa desglose no disponible, no un IVA cero. `[]` significa desglose conocido sin IVA trasladado 002. Se preserva sin cambios la forma pública de `tax_lines` para no alterar propuestas, reportes o clientes existentes.

Cada línea contiene `source_key` (posición estable del nodo dentro del XML), `base` (cadena decimal a seis posiciones), `factor_type` (`Tasa` o `Exento`), `rate` (cadena de seis posiciones para Tasa, `null` para Exento). Sólo contiene IVA federal trasladado código 002; una línea exenta tiene IVA calculado cero, no necesita Importe ni TasaOCuota.

Fuente canónica: traslados 002 de los conceptos, si existen. Si no hay conceptos con esos traslados, pueden usarse los globales que incluyan Base y factor suficientes; nunca combinar ambos niveles. Una línea relevante incompleta o con factor no soportado deja el desglose DIOT no disponible y su motivo; no se reconstruye dividiendo importe entre subtotal. Los errores de importación fiscal ya existentes permanecen; la ausencia de datos nuevos no invalida por sí sola un documento antes aceptado. Ajustar el lector global para admitir Exento sin Importe como importe contable cero, conservando la omisión vigente de partidas de impuesto cero.

Agregar `diot_unavailable_reason: string|null` para explicar datos insuficientes o factor no soportado. Los motivos se derivan al importar y se conservan junto al desglose. Migración aditiva, sin backfill por estimación; los documentos existentes quedan `null`. El original no se almacena y reimportar un UUID sigue siendo duplicado: no prometer reparación de históricos con el flujo actual ni modificar esa política en esta entrega.

### 2. Selección al contabilizar — CA-011-01/02/03/06/07/08/09/12

Extender POST/PUT vigentes de `/api/companies/{companyId}/accounting-periods/{periodId}/accounting-policies[/{accountingPolicyId}]`, responsables de SPEC-006, con `diot_document_ids: integer[]` opcional:

- En creación POSTED o transición DRAFT → POSTED, omisión equivale a `[]`. Cada ID debe ser distinto y tener exactamente una partida de origen `source_fiscal_document_id = ID`, `source_component_key = subtotal`, además de estar en `fiscal_document_ids` y ser elegible. No aceptar una etiqueta «Subtotal» como prueba de origen.
- En DRAFT el frontend omite el campo; si se recibe, no se conserva ni produce resultados. La selección sólo vive en memoria del editor y se reinicia al reabrir, quitar la fila o desvincular su origen.
- En edición POSTED → POSTED, omisión conserva la selección guardada; enviar explícitamente otro conjunto responde `422`. No permite añadir DIOT a pólizas históricas ya POSTED. Una lista idéntica no recalcula.
- Respuesta de póliza: agregar `diot_document_ids` persistidos y `diot_results`, con `fiscal_document_id`, `uuid`, `supplier_rfc`, `accounting_period_id` y grupos `factor_type`, `rate`, `base`, `vat`. Ambos arrays están vacíos en DRAFT o POSTED sin DIOT. Las cadenas monetarias tienen seis decimales.
- Lista/detalle de CFDI: agregar `diot_inclusion: null|{accounting_policy_id, accounting_period_id}` para mostrar indisponibilidad por inclusión previa, incluso en otro periodo. Es informativo; backend vuelve a validar al contabilizar.

Elegibilidad autoritativa: tipo I, `recipient_rfc` igual al RFC de empresa, emisor distinto, método PUE, MXN, desglose DIOT disponible y no vacío. Ninguna información enviada por el cliente fija la base, tasa, proveedor o impuesto. Con varias tasas, una selección del subtotal incorpora el XML entero; no se desdobla la propuesta contable.

El origen verificable se acredita con la referencia al CFDI vinculado y elegible y la clave canónica `subtotal`, validadas por el servidor. No se exige demostrar que la fila salió de una propuesta previa ni se añade un token de propuesta. Una partida sin esa referencia fiscal sigue siendo manual y no elegible. Alcance confirmado por el usuario el 2026-10-27.

### 3. Instantánea inmutable y precisión — CA-011-04/05/06/07/08

Migraciones aditivas propuestas:

- `diot_inclusions`: empresa, documento fiscal, póliza, periodo contable, UUID y RFC de proveedor capturados, autor y fecha. Restricción única `(company_id, fiscal_document_id)` y referencias al contexto; sólo se crea al contabilizar. No vincular la instantánea a IDs de partidas que `replaceDetails` destruye.
- `diot_inclusion_lines`: referencia a inclusión, factor, tasa nullable, base e IVA agrupados. Tasas `decimal(12,6)`; base e IVA `decimal(18,6)` como importes vigentes. Exento usa tasa nula; cero usa `0.000000`.

Multiplicación decimal exacta sin `float`: calcular cada Base × TasaOCuota con hasta doce decimales, redondear a seis con mitades hacia arriba y después agrupar por factor/tasa. No redondear a centavos ni multiplicar una base agregada antes de redondear cada línea. Sumas de consulta también exactas; serializar como cadenas sin truncar y rechazar desbordamiento de persistencia con `422`. Reutilizar `ExactDecimal` para representación/sumas y ampliar su capacidad de multiplicación exacta sólo lo necesario.

En la misma transacción de contabilización: validar póliza/orígenes, bloquear documentos seleccionados en orden de ID, comprobar inclusión previa, crear inclusión y líneas. La restricción única cubre carreras entre periodos; traducir su conflicto específico a error de validación y revertir toda la operación. Conservar reservas y permisos vigentes.

Para actualizar una POSTED, bloquear póliza y validar antes de `replaceDetails` que cada XML incluido y su origen subtotal permanecen, y que no cambia el periodo de su instantánea. Se permiten otras ediciones contables válidas sin recalcular DIOT, incluso cambios de importe: el cálculo procede del XML. No prohibir por DIOT la edición del resto de la póliza. No introducir borrado en cascada de las instantáneas por recrear partidas ni un mecanismo de reversión.

### 4. Consulta, total y Excel — CA-011-10/11/12/14/15/16

Contratos modificados, responsabilidad de SPEC-011; no requieren migraciones ni cambios en las instantáneas:

- `GET /api/companies/{companyId}/accounting-periods/{periodId}/diot`: mantiene `data: DiotRow[]` completo y añade `meta: {total_vat: string}`. Cada fila conserva `company_id`, `year`, `month`, `supplier_rfc`, `factor_type`, `rate` nullable, `base`, `vat` y añade `accounting_policy_id: number` y `policy_display_number: string`. El número visible usa el mismo formato que `AccountingPolicyResource::display_number`; el ID sirve para identidad y agrupación, no para presentación.
- Una fila por ID de póliza/RFC/factor/tasa. Los XML con la misma combinación dentro de una póliza se suman, sin mezclar pólizas distintas. Orden estable: número de póliza ascendente, ID de póliza como desempate, RFC ascendente, Tasa antes de Exento y tasa ascendente. Conservar filtros por empresa, periodo de la instantánea y pólizas POSTED. No consultar el mes de emisión del XML ni recalcular desde partidas editadas.
- `meta.total_vat` es la suma decimal exacta de `vat` de todas las filas devueltas, calculada en backend con `ExactDecimal` y serializada a seis decimales; vacío devuelve `data: []` y `total_vat: "0.000000"`. No usar `float`, no redondear a centavos ni limitar el total a una página. Derivar filas y total de la misma colección obtenida, no de dos lecturas que puedan divergir.
- `GET /api/companies/{companyId}/accounting-periods/{periodId}/reports/diot.xlsx`: mismo servicio y orden que JSON; una hoja `DIOT`, archivo `diot-AAAA-MM.xlsx`, encabezados `# poliza`, `company_id`, `year`, `month`, `supplier_rfc`, `factor_type`, `rate`, `base`, `vat`, en ese orden. La primera celda de cada fila usa `policy_display_number` como texto; no se exporta el ID interno. Tasa exenta vacía. Celdas decimales como texto exacto. Reutilizar `XlsxReportExporter`; aplicar el límite de 10,000 a las filas ya desglosadas por póliza, sin truncar. Vacío conserva los nueve encabezados. La descarga no recibe página ni incorpora fila de total.
- Compatibilidad: permanecen las rutas y las columnas previas, pero cambia intencionalmente la granularidad en ambos formatos y se antepone una columna al Excel. Coordinar backend y frontend; el frontend no debe inferir pólizas ni sustituir un total ausente por cero. La consulta JSON no hereda el límite de exportación.

Ambas operaciones siguen autenticación, cambio de contraseña y contexto visible vigentes. `401` no autenticado; contexto ajeno responde según la convención vigente (`404` al resolver empresa/periodo no visible); `422` validación DIOT o exceso de filas, sin archivo. Los conflictos de reserva conservan el contrato actual. Los errores de guardado usan `errors.diot_document_ids` y, si procede, referencia al UUID accesible; no exponen XML ajenos.

## Responsabilidades y orden de integración

1. Backend: ampliar agregación y total en `DiotReportService`, respuesta y XLSX en `DiotReportController`; probar el contrato antes de integrar la UI.
2. Frontend: extender `DiotRow` y definir el resultado de consulta con filas y total en contratos compartidos; `reports-api.ts::getDiot` y `use-report-requests` deben conservar ambos. No modificar globalmente `DataResponse<T>` ni los contratos de otros reportes.
3. Extraer la consulta y el estado de página a un hook de reports; mantener `DiotReport` como composición de resumen, tabla y controles. El servicio sigue pasando por el cliente compartido; los componentes no importan API. No introducir lógica en rutas ni dependencias nuevas.
4. Paginación local sobre el array completo: tamaño constante 25, índice inicial 1, corte después del orden del backend y clave de fila por ID de póliza/RFC/factor/tasa. El total se toma de `meta`, no de las filas visibles. Cambiar de página no solicita datos ni afecta la descarga. Reiniciar página al cambiar empresa o periodo; descartar respuestas tardías y ocultar filas/total previos durante carga o error. En vacío mostrar el resumen cero y el estado vacío; ocultar o desactivar los controles. Sin periodo no mostrar resumen válido.
5. Integrar BE-011-06 antes de FE-011-04; BE-011-07 y FE-011-05 consumen el contrato y completan las regresiones de la entrega. Dependencias y condiciones de término en los archivos de tareas.

## Estrategia de pruebas

- Backend: adaptar `tests/Feature/Spec011Test.php` para dos pólizas con igual proveedor/tasa que ya no se fusionan; varios XML de una póliza que sí se suman; tasa cero y exento separados; orden determinista; número visible con ceros; total exacto con fracciones, acarreo y valores grandes; vacío, sólo POSTED, aislamiento por empresa/periodo y rechazo de contexto ajeno.
- XLSX: primera columna y valor textual, nueve encabezados, igualdad de todas las filas con JSON, vacío, exactamente 10,000 filas aceptadas y 10,001 rechazadas tras separar por póliza. Regresión de `Spec009Test` y de las pruebas vigentes de SPEC-011, sin cambiar sus reglas fiscales.
- Frontend: Vitest/RTL en `diot-report.test.tsx` y `reports-api.test.ts` para filas y total del contrato, primera columna, estados sin periodo/carga/vacío/error, total invariable al paginar, límites de 0/1/25/26/50/51 filas, navegación por teclado, páginas sin duplicados, cambio de empresa y de periodo por separado desde una página posterior y respuestas tardías. La descarga usa sólo empresa/periodo incluso desde la página 2.
- QA humana pendiente: posición y legibilidad del resumen, columna de póliza, controles, tabla en anchos pequeños y ceros iniciales al abrir Excel. No se requiere prueba integral por navegador ni se da esta revisión por realizada.

## Riesgos y bloqueantes técnicos

Sin bloqueantes para preparar esta actualización. La granularidad por póliza puede aumentar el número de filas y alcanzar antes el límite de Excel; es intencional, no autoriza truncar ni aumentar el límite. Se conserva la consulta completa y paginación local para no introducir un protocolo nuevo de paginación; no se promete una mejora de transferencia o escalabilidad. Hay trabajo local previo sin commit que debe protegerse antes de implementar; los fallos frontend ajenos descritos en verificación no se corrigen en esta entrega.

Situación de tareas en [tasks-backend.md](tasks-backend.md) y [tasks-frontend.md](tasks-frontend.md); evidencia local y cierre formal pendiente en [verificacion.md](verificacion.md).
