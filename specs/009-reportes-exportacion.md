# SPEC-009 — Reportes y exportación

**Estado:** Borrador  
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
| CA-009-02 | El contador consulta el reporte de pólizas. | Ve las pólizas y sus partidas según SPEC-006; el alcance de estados/filtros se debe concretar. |
| CA-009-03 | El contador consulta el reporte de balanza. | Ve los mismos datos y cálculo definidos en SPEC-008, excluyendo efectos de borradores. |
| CA-009-04 | Se exporta cada uno de los tres reportes principales. | Se obtiene un archivo utilizable en Excel con los datos del contexto y filtros acordados, consistente con la consulta correspondiente. |
| CA-009-05 | Se intenta consultar o exportar datos de una empresa sin acceso. | No se entrega información ni un archivo con datos de esa empresa. |
| CA-009-06 | Se exportan importes y referencias del reporte preparado. | Los valores conservan la precisión y representación acordadas; la exportación no recalcula saldos mediante reglas independientes. |

## Pendientes y decisiones

- **Antes de Lista:** formato Excel concreto, columnas/orden, filtros y estados incluidos para cada listado, consulta vacía, volumen admitido y resultado de errores de exportación; representación de importes/fechas/identificadores para conservar su significado. Preparar estos contratos tras definir los reportes fuente.
- **Validación durante MVP:** que los tres reportes y archivos permiten revisar el flujo principal con los contadores.
- **Posterior:** formatos fiscales oficiales, personalización avanzada, dashboards y comparación entre empresas.

## Plan técnico y contratos

- Backend: consume contratos de SPEC-004/006/008 y define aquí las operaciones de exportación, sus opciones y errores. Elegir biblioteca solo si las capacidades disponibles no resuelven la necesidad, conforme a DT-005.
- Frontend: consulta de reportes y acción de exportar, con contexto claro y resultado visible.
- Evitar fórmulas/cálculos de negocio independientes en archivos exportados. La decisión de ejecución síncrona/asíncrona depende del volumen acordado, no se presupone infraestructura.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). Los contratos aún no están cerrados: resolver los detalles necesarios antes de Lista, sin introducir reglas para completar huecos.

## Verificación

**Evidencia de producto:** pendiente; no ejecutada. No existe implementación vinculada todavía.

Prever comparación de datos consultados/exportados en los tres reportes, apertura del formato elegido en una herramienta compatible, valores decimales e intento de exportación de una empresa no asignada. Completar el recorrido extremo a extremo descrito en el índice.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance de reportes.
