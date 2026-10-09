# Plan técnico — SPEC-006

Este plan cubre únicamente CA-006-19 y CA-006-20 revisados de [spec.md](spec.md). La entrega reemplaza la lista de búsqueda del selector de CFDI por una tabla filtrable dentro de Nueva/Editar póliza, sin modificar la generación de partidas, el guardado ni la contabilización.

## Contratos y datos

El frontend reutiliza `GET /api/companies/{companyId}/fiscal-documents?period_id={periodId}&include=policy-links`. La respuesta vigente ya contiene fecha de emisión, tipo, dirección, RFC y nombre de emisor y receptor, UUID, Serie, Folio, total, moneda y vínculos con pólizas. No se agregan endpoints, campos, tipos públicos, migraciones ni reglas de autorización.

La consulta se limita al periodo contable activo. Al editar, los `fiscal_documents` ya relacionados incluidos en la póliza se combinan en presentación con la consulta del periodo para conservar y mostrar por separado vínculos históricos de otros periodos; esos documentos históricos no se vuelven seleccionables en esta ventana.

## Interfaz y filtrado

La ventana «CFDI relacionados» muestra una tabla con Selección, Fecha, Tipo, RFC, Nombre, Monto, Folio fiscal, Folio interno y Vínculos. RFC y Nombre se derivan de la contraparte según la dirección del CFDI; Folio fiscal corresponde al UUID; Folio interno usa Serie-Folio; Monto presenta el total y el código de moneda, sin conversión.

Los filtros se ejecutan localmente sobre los CFDI ya cargados del periodo y se combinan con lógica AND. Fecha y monto admiten extremos inclusivos desde/hasta; un extremo vacío no restringe. RFC, nombre, UUID y Serie-Folio usan coincidencia parcial normalizada, sin distinguir mayúsculas, minúsculas ni acentos. Tipo admite Todos, Ingreso (`I`), Egreso (`E`) y Pago (`P`). Un rango inválido o invertido muestra un error asociado y no se aplica hasta corregirse. «Limpiar filtros» restablece la tabla sin alterar la selección.

La selección permanece ordenada y se conserva aunque una fila quede oculta por los filtros. El recuento distingue coincidencias visibles de selección total. No hay paginación ni selección masiva. La tabla usa encabezado reconocible, casillas etiquetadas por CFDI, operación por teclado, región desplazable y estados explícitos de carga, error, periodo sin documentos y filtros sin coincidencias.

«Continuar» conserva su responsabilidad actual: solicita la propuesta para los CFDI seleccionados del periodo y cierra la ventana para presentar bloques editables; no guarda ni contabiliza la póliza. Los CFDI `P` permanecen seleccionables y siguen el flujo de captura manual ya definido por CA-006-22.

## Responsabilidades y orden de integración

- Backend: sin trabajo nuevo; conserva autorización, aislamiento, filtrado por periodo y exposición de `policy-links` mediante el contrato vigente.
- Frontend: consulta el periodo activo, compone los vínculos históricos, administra filtros y selección, renderiza la tabla y conserva las acciones actuales.
- Dependencias: FE-006-04 consume el contrato vigente de SPEC-004 y no requiere una tarea backend previa.

## Errores e integridad

Los errores de carga no se presentan como una tabla vacía. Los rangos inválidos conservan el resto de los filtros y la selección para que el usuario pueda corregirlos. Filtrar, limpiar, cerrar o reabrir la ventana durante la misma edición no elimina CFDI seleccionados ni modifica vínculos históricos. Cambiar de empresa, periodo o póliza reinicia el estado de filtros conforme al nuevo contexto.

## Estrategia de pruebas

Las pruebas de componente con Vitest y React Testing Library cubren columnas y valores derivados, cada filtro y sus combinaciones, límites inclusivos, errores de rango, limpieza, selección oculta, orden, vínculos históricos, tipo `P`, recuentos, estados de carga/error/vacío y que «Continuar» no guarda la póliza. También se ejecutan las comprobaciones frontend de tipos, lint y formato. La legibilidad, el desplazamiento interno y la jerarquía visual se reservan para QA humana.

## Riesgos y bloqueantes técnicos

No hay bloqueantes conocidos. El alcance supone un volumen mensual manejable en memoria; paginación o filtrado remoto requerirán una entrega posterior y un contrato backend explícito.
