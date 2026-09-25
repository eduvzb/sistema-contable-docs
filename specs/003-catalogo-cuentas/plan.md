# Plan técnico — SPEC-003

Este archivo describe la ejecución técnica de [SPEC-003](spec.md); los criterios funcionales vigentes y el estado sólo se definen allí.

## Contexto para ejecución

El alcance y los criterios de esta entrega están en [spec.md](spec.md); las tareas abiertas por repositorio identifican el trabajo pendiente. Consulta los contratos de las specs dependientes que esta ejecución consume. Las fuentes ya citadas en `spec.md` se reabren sólo ante una contradicción, un cambio posterior de regla o contrato, un supuesto que afecte el resultado, o una solicitud explícita de cambiar comportamiento.

## Plan técnico y contratos

### Persistencia

`accounts` conserva `company_id`, `parent_id`, `code`, `name`, `nature`, `accepts_entries`, `active` y marcas de tiempo. La base garantiza código único por empresa y padre de la misma empresa. No existe eliminación en esta spec.

### API autenticada

Todas las rutas aplican la sesión Sanctum, el cambio obligatorio de contraseña y el acceso vigente a la empresa de SPEC-001.

| Operación | Resultado |
|---|---|
| `GET /api/companies/{companyId}/accounts` | `200` con el catálogo plano ordenado por código; cada fila incluye su `parent_id` para reconstruir el árbol. |
| `POST /api/companies/{companyId}/accounts` | `201` con la cuenta creada. Requiere código, nombre y naturaleza; padre es opcional y los booleanos predeterminan `true`. |
| `PUT /api/companies/{companyId}/accounts/{accountId}` | `200` con la cuenta actualizada, conservando empresa e integridad jerárquica. |
| `POST /api/companies/{companyId}/account-imports` | `201` con `{ imported_count, accounts }` para un archivo multipart `file`; falla atómicamente con `422`. |

La representación es `{ id, company_id, parent_id, code, name, nature, accepts_entries, active }`. Peticiones no autenticadas devuelven `401`; empresa/cuenta ajena o inexistente devuelve `404`; datos, jerarquía o importación inválidos devuelven `422` sin cambios.

### Interfaz

La empresa enlaza a `/companies/{companyId}/accounts`. La pantalla muestra la jerarquía, naturaleza, capacidad de recibir movimientos y estado; permite crear, editar, activar/desactivar e importar CSV, con errores de campos o filas. El componente de búsqueda presenta campo etiquetado, acción de limpieza, recuento de coincidencias y estado sin resultados; filtra el catálogo cargado sin introducir un contrato API adicional. El catálogo pertenece a la empresa y no cambia al seleccionar otro periodo.

Aplican las [decisiones técnicas compartidas](../../docs/decisiones.md). SPEC-006 consume cuentas activas que aceptan movimientos y aplica el bloqueo de estructura cuando existan partidas; SPEC-008 consume `nature` para la balanza.

## Orden y coordinación

Las tareas pendientes se registran por repositorio en [backend](tasks-backend.md) y [frontend](tasks-frontend.md). El contrato responsable se prepara antes de implementarlo en un consumidor; las comprobaciones reales se registran en [verificación](verificacion.md).
