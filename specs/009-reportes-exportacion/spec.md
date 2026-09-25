# SPEC-009 — Reportes y exportación

- **Estado:** QA
- **Actualizado:** 2026-09-24 (migración documental; sin cambio de estado)
- **Criterios de esta entrega:** Sin tareas técnicas abiertas; resta QA humana.
- **Usuario:** Administrador o contador con empresa accesible
- **Dependencias:** [SPEC-002](../002-contexto-contable/spec.md), [SPEC-004](../004-documentos-fiscales/spec.md), [SPEC-006](../006-polizas-trazabilidad/spec.md), [SPEC-008](../008-balanza-basica/spec.md)

## Contexto y objetivo

Consultar reportes básicos de XML, pólizas con partidas y balanza; exportar los reportes principales a Excel para revisar y compartir información. Cubrir los tres reportes del alcance §16.

## Historias de usuario

- H-009-01: Como usuario operativo quiero consultar los reportes básicos de mi contexto, para revisar la información contable.
- H-009-02: Como usuario operativo quiero exportar los reportes a Excel, para compartirlos y revisarlos fuera del sistema.

## Requisitos funcionales y criterios de aceptación

El usuario operativo selecciona el contexto, consulta el reporte y solicita exportación a Excel; el administrador accede a cualquier empresa y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. Documentos, pólizas y balanza provienen de sus contratos responsables; la exportación no redefine el cálculo ni las reglas de consulta.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-009-01 | El contador consulta el reporte de XML de su contexto. | Ve el listado y datos principales definidos en SPEC-004. |
| CA-009-02 | El contador consulta el reporte de pólizas. | Ve las pólizas DRAFT y POSTED y sus partidas según SPEC-006, dentro del periodo seleccionado. |
| CA-009-03 | El contador consulta el reporte de balanza. | Ve los mismos datos y cálculo definidos en SPEC-008, excluyendo efectos de borradores. |
| CA-009-04 | Se exporta cada uno de los tres reportes principales. | Se obtiene un archivo utilizable en Excel con los datos del contexto y filtros acordados, consistente con la consulta correspondiente. |
| CA-009-05 | Se intenta consultar o exportar datos de una empresa sin acceso. | No se entrega información ni un archivo con datos de esa empresa. |
| CA-009-06 | Se exportan importes y referencias del reporte preparado. | Los valores conservan la precisión y representación acordadas; la exportación no recalcula saldos mediante reglas independientes. |

## Requisitos no funcionales aplicables

- Aislamiento y exportación contextual: CA-009-01/02/03/04/05/06.

## Casos límite

- Periodos sin datos, acceso ajeno y exportaciones de las tres vistas: CA-009-01/02/03/04/05/06.

## Fuera de alcance

No incluye diseñador de reportes, dashboards, comparaciones entre empresas, DIOT ni archivos de contabilidad electrónica.

## Decisiones, supuestos y dudas

### Pendientes y decisiones

- **Resuelto para esta entrega:** tres archivos XLSX separados, una hoja por archivo, periodo obligatorio en la ruta, consulta completa del periodo sin filtros adicionales, pólizas DRAFT/POSTED y balanza únicamente con movimientos POSTED.
- **Resuelto para esta entrega:** el límite es de 10,000 filas de datos por archivo; una consulta vacía devuelve un XLSX válido con encabezados y sin datos; superar el límite devuelve `422` JSON sin archivo.
- **Resuelto para esta entrega:** los archivos son síncronos, usan MIME `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, nombres `xml-{year}-{month}.xlsx`, `polizas-{year}-{month}.xlsx` y `balanza-{year}-{month}.xlsx`, y no contienen fórmulas.
- **Validación durante MVP:** que los tres reportes y archivos permiten revisar el flujo principal con los contadores.
- **Posterior:** formatos fiscales oficiales, personalización avanzada, dashboards y comparación entre empresas.

## Criterios de finalización

- Los criterios de esta entrega deben tener implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §16: reportes y exportación](../../docs/planeacion/003%20-%20MVP-Scope.md#16-reportes-incluidos); [§18: recorrido completo](../../docs/planeacion/003%20-%20MVP-Scope.md#18-flujo-completo-que-debe-demostrar-el-mvp); [§21: reportería avanzada excluida](../../docs/planeacion/003%20-%20MVP-Scope.md#21-fuera-del-mvp).
- [BR-001](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-017](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#19-br-017--las-p%C3%B3lizas-contabilizadas-afectan-la-balanza) (aislamiento y fuente de movimientos contabilizados).
