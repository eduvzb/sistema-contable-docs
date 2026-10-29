# Plan técnico — SPEC-004

## Actualización pendiente coordinada con SPEC-012

La entrega actual revisa CA-004-01/03/10/11/12/13 y añade CA-004-14 de [spec.md](spec.md). El [plan preliminar de SPEC-012](../012-descarga-masiva-sat/plan.md) concentra el diseño pendiente de tipos N/T, originales privados, comparación histórica y resultados del importador compartido. No se define aquí otro contrato ni otra migración.

La ejecución se concentra en BE-012-02/03 y FE-012-05, con BE-012-10 para almacenamiento y respaldos. Contratos, dimensionamiento y autorizaciones siguen pendientes; coordinar los criterios no autoriza implementar ni habilitar conexión real. Las regresiones deben conservar conceptos, impuestos, pagos, unicidad e integración contable de los tipos permitidos.

## Referencia de la entrega anterior: conceptos

El contenido siguiente describe el contrato anterior de CA-004-12/13 para [SPEC-006](../006-polizas-trazabilidad/plan.md), cuya evidencia se conserva en verificación. Sus menciones al descarte de XML y a la ausencia de conceptos describen la base de aquella entrega, no el nuevo resultado esperado ni trabajo pendiente que deba repetirse. La política de originales queda sustituida por la actualización anterior.

## Base comprobada

`app/CfdiXmlParser.php` extrae datos fiscales, pero no conceptos. `app/Support/FiscalDocumentImporter.php` persiste datos normalizados en una transacción por documento y rechaza UUID duplicados por empresa. `app/Models/FiscalDocument.php` y `app/Http/Resources/FiscalDocumentResource.php` aún no contienen conceptos. Existe la consulta autorizada de detalle en `FiscalDocumentController::show`.

## Datos y migración

Agregar a `fiscal_documents` una columna JSON nullable `concepts`, con conversión a array en el modelo:

- `null`: no se conservaron conceptos; valor para registros anteriores, sin reconstrucción ni relleno histórico.
- `[]`: la nueva importación no encontró elementos Concepto en Conceptos.
- Lista de objetos `{ "description": string | null }`: un objeto por elemento; la posición del array representa el orden del XML. Ausencia o texto compuesto sólo de espacios se representa con `null`; el texto disponible se conserva completo, sin deduplicar ni recortar a la longitud del concepto contable.

El parser obtiene los hijos Concepto de Conceptos en el espacio de nombres CFDI 4.0, sin depender del prefijo literal `cfdi`. Las entidades XML se decodifican como texto mediante el parser existente, sin habilitar resolución externa. No se conservan XML ni otros atributos de los conceptos.

Persistir el dato en la transacción vigente del documento. Conservar UUID único por empresa, política parcial de lotes y validaciones de importación. No hay cambios monetarios, fiscales ni de contabilización. La migración inversa retira únicamente la columna nueva.

## Contrato de consulta

Ampliar sólo `GET /api/companies/{companyId}/fiscal-documents/{documentId}` con `data.concepts`, usando los tres valores definidos arriba. Ejemplo del campo añadido:

```json
{
  "concepts": [
    { "description": "Servicio de consultoría contable" },
    { "description": "Licencia mensual de software" },
    { "description": "Soporte técnico" }
  ]
}
```

Conservar los campos actuales de identificación y detalle. El listado y las respuestas de pólizas e importación no necesitan incorporar este campo: el consumidor solicita el detalle al abrir la vista. No añadir parámetros ni rutas y no alterar `policy-links`.

Aplicar la autorización vigente de empresa visible y documento perteneciente a esa empresa. Una consulta no autorizada o inexistente conserva la respuesta de error actual; nunca devuelve conceptos de otra empresa. El dato no admite edición mediante pólizas ni un endpoint de escritura nuevo.

## Responsabilidades e integración

- Backend: migración, extracción, persistencia y exposición del campo en el detalle.
- Frontend: contrato compartido y servicio de detalle; sin cambios de presentación en la bandeja ni en el detalle fiscal. La interacción se prepara en SPEC-006.
- Orden: preparar backend y contrato de detalle antes de integrar el consumidor. El campo ausente durante un despliegue compatible se trata como información no disponible, no como fallo ni como prueba de que el XML no tenía conceptos.

## Pruebas previstas

Ampliar `tests/Feature/Spec004Test.php` con importación y consulta posterior de uno, varios y repetidos conceptos; descripción larga, Unicode, entidades XML, prefijo alternativo, posición sin descripción, lista vacía y documento anterior con `null`. Comprobar persistencia tras descartar el archivo, duplicados sin actualización, lotes y aislamiento de empresa/documento. Verificar que listado, impuestos e importación vigentes no cambian.

En frontend, probar el servicio de detalle y su contrato con los tres valores y compatibilidad con campo ausente. La representación y los errores interactivos se prueban en SPEC-006. No hay bloqueantes técnicos conocidos.
