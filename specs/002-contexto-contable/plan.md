# Plan técnico — SPEC-002

Este archivo describe la ejecución técnica de [SPEC-002](spec.md); los criterios funcionales vigentes y el estado sólo se definen allí.

## Contexto para ejecución

El alcance y los criterios de esta entrega están en [spec.md](spec.md); las tareas abiertas por repositorio identifican el trabajo pendiente. Consulta los contratos de las specs dependientes que esta ejecución consume. Las fuentes ya citadas en `spec.md` se reabren sólo ante una contradicción, un cambio posterior de regla o contrato, un supuesto que afecte el resultado, o una solicitud explícita de cambiar comportamiento.

## Antecedentes de diseño

### Análisis de hallazgo 2026-09-12

| Hallazgo | Comportamiento actual mejorable | Comportamiento esperado | Impacto documental | Componentes |
|---|---|---|---|---|
| El selector de empresa es un `select` simple. | La lista completa se recorre sin búsqueda, lo que dificulta localizar una empresa cuando el volumen crece. | Un único control permite buscar y seleccionar conforme a CA-002-09, conservando la empresa elegida y el flujo de contexto existente. | Se agrega CA-002-09 y se concreta una decisión local de interacción; no cambia la política de acceso ni el contrato de empresas. | Frontend. El backend conserva el listado autorizado vigente. |

## Plan técnico y contratos

### Persistencia

`accounting_periods` conserva `company_id`, `year`, `month`, `status` y marcas de tiempo. Una restricción única cubre `(company_id, year, month)`; las restricciones de base de datos limitan el año a cuatro dígitos y el mes a `1..12`. El periodo pertenece a una empresa y es la referencia estable que usarán las entidades consumidoras.

### API JSON autenticada

Todas las rutas aplican la sesión Sanctum, el cambio obligatorio de contraseña y el acceso vigente a la empresa de SPEC-001.

| Operación | Resultado |
|---|---|
| `GET /api/companies/{companyId}/accounting-periods` | `200` con periodos accesibles, ordenados por ejercicio descendente y mes ascendente. |
| `GET /api/companies/{companyId}/accounting-periods/{periodId}` | `200` con el periodo cuando pertenece a la empresa accesible. |
| `POST /api/companies/{companyId}/accounting-years` con `{ "year": 2026 }` | `201` con los doce periodos creados; cualquier usuario con acceso a la empresa puede ejecutarlo. |

Cada periodo se representa como `{ id, company_id, year, month, month_name, status }`, con `status` en `OPEN|CLOSED` y nombre de mes en español. Una petición no autenticada devuelve `401`; una empresa/periodo inexistente, ajeno o no asignado devuelve `404`; año ausente, no entero o no de cuatro dígitos y ejercicio ya habilitado devuelven `422` sin escritura parcial.

### Interfaz

La empresa presenta ejercicios disponibles, sus meses y una acción para habilitar ejercicio. El selector de empresa permite buscar por razón social o RFC y elegir entre los resultados autorizados sin cambiar el contexto mientras sólo se busca. Elegir un periodo navega a `/companies/{companyId}/periods/{periodId}`. Esa ruta valida empresa y periodo mediante la API antes de guardar `{ company_id, period_id }` como último contexto. Una barra visible muestra razón social, ejercicio, mes y estado y permite cambiar de contexto. Un valor local inválido o revocado se elimina y regresa al selector sin mostrar datos protegidos.

El frontend conserva la pestaña y los parámetros de consulta de cada vista mediante estado de navegación recuperable, compatible con recarga e historial del navegador. Al cambiar de periodo mantiene la estructura de la vista activa, marca el destino como pendiente y reemplaza el contenido sólo cuando la validación y la consulta correspondientes terminan. No se agrega persistencia backend ni se reutilizan respuestas de otro contexto.

Separar pertenencia empresarial de filtrado por periodo: los criterios temporales de XML se concretan en SPEC-004, los de pólizas en SPEC-006 y los de pagos en SPEC-007. Aplican las [decisiones técnicas compartidas](../../docs/decisiones.md).

### Pruebas frontend de CA-002-09

Incorporar la configuración compartida de Vitest con `jsdom`, React Testing Library, `@testing-library/user-event` y matchers de `@testing-library/jest-dom` si todavía no existe. La suite debe ejecutarse mediante `pnpm test` y comprobar el selector en su frontera de componente, sustituyendo la API y la navegación externas necesarias sin levantar backend ni navegador.

## Orden y coordinación

Las tareas pendientes se registran por repositorio en [backend](tasks-backend.md) y [frontend](tasks-frontend.md). El contrato responsable se prepara antes de implementarlo en un consumidor; las comprobaciones reales se registran en [verificación](verificacion.md).
