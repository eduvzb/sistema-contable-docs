# Plan técnico — SPEC-006

Esta entrega cubre CA-006-25 a CA-006-29 de [spec.md](spec.md). Consume la conservación y consulta de conceptos de [SPEC-004](../004-documentos-fiscales/plan.md), sin cambiar selección, propuestas, guardado ni contabilización.

## Contratos y datos

Al abrir la vista, consultar `GET /api/companies/{companyId}/fiscal-documents/{documentId}` mediante el servicio de detalle existente. El campo `concepts` y su compatibilidad se definen exclusivamente en SPEC-004. La identificación usa UUID, Serie/Folio y contraparte según dirección; si no hay nombre, usa el RFC disponible.

Mantener separados el estado de consulta y el estado editable de la póliza. Identificar cada petición por empresa y documento. Cancelar o ignorar respuestas obsoletas al cambiar de CFDI, empresa, periodo, póliza o cerrar el diálogo; borrar contenido anterior antes de mostrar el nuevo. No reutilizar datos de otra empresa ni modificar el payload de propuestas o guardado.

## Interfaz

Agregar una acción de ojo independiente de la casilla o etiqueta de selección en el selector, incluida la sección de vínculos históricos. En el editor, colocarla junto al encabezado documental del bloque existente y exponer los documentos relacionados sin bloque generado en un área identificada. Usar `type="button"` para evitar enviar el formulario; no anidar el botón en una etiqueta que active la casilla. No sustituir el selector ni reconstruir su filtrado en esta entrega.

Componer un panel de lectura dentro del diálogo desde el que se abre, no otro modal apilado. El encabezado documental precede una lista numerada de conceptos, con separación entre elementos, ajuste de texto y desplazamiento interno cuando haga falta. Renderizar texto con React sin HTML interpretado. Mantener la acción cercana al CFDI y a la asignación de cuentas, sin confundir la descripción comercial con el concepto editable de una partida.

El panel tiene una acción de cierre propia. Al abrirlo, el foco pasa a su título o control inicial; al cerrar, vuelve al disparador. Si se usa Escape, cierra primero el panel, sin cerrar el editor ni descartar la captura. Usar la gestión de foco del diálogo vigente sin agregar una segunda trampa de foco.

## Responsabilidades y orden de integración

- Backend: el trabajo nuevo pertenece a SPEC-004; no hay cambios propios en pólizas ni propuestas.
- Frontend: contrato/servicio en `src/features/fiscal-documents` y `src/shared/contracts`; hook de consulta y panel en `src/features/policies`, consumiendo exports públicos. Los componentes no importan módulos API; el único `fetch` permanece en `src/shared/api/client.ts`.
- Integración: primero el contrato y la consulta de SPEC-004; después hook/panel y disparadores en selector/editor. Reutilizar primitivas existentes sin convertir el panel específico en un componente global.

## Errores e integridad

El panel distingue carga, error con reintento y datos no disponibles. Una lista vacía, `null` o campo ausente presenta el aviso acordado; una lista con elementos sin descripción mantiene cada posición. Un fallo de autorización tampoco muestra contenido anterior. Abrir/cerrar el panel no invoca selección, generación, sugerencias, guardado ni contabilización.

## Estrategia de pruebas

Pruebas con Vitest y React Testing Library para panel y hook: documento correcto, orden, repetidos, texto completo/seguro, datos parciales, `null`, lista vacía, campo ausente, carga, error, reintento y respuestas fuera de orden. En `accounting-policy-editor.test.tsx`, cubrir selector sin selección, bloque generado, captura manual, vínculos históricos, edición, varios CFDI, conservación de captura y ausencia de llamadas de generación/guardado al consultar. Cubrir teclado, nombre accesible, cierre, retorno de foco y Escape sin cerrar el editor. Ejecutar regresiones de selección, propuesta y sugerencias, tipos, lint y formato. Legibilidad y disposición real quedan para QA humana, sin exigir prueba integral por navegador.

## Riesgos y bloqueantes técnicos

No hay decisiones bloqueantes. La consulta diferida evita añadir todas las descripciones a los listados. No introduce paginación, búsqueda, truncamiento de texto ni cambios al volumen de documentos del selector.
