# Plan técnico — SPEC-006

Entrega: CA-006-07/20 revisados y CA-006-30 a CA-006-35 de [spec.md](spec.md). No cambia importes, propuestas ni el significado de POSTED.

## Contratos

- `GET /api/accounting-settings`: autenticación y contraseña actualizada, para administradores y contadores. Respuesta `200`: `{ "data": { "allow_cfdi_reuse": false } }`. Solo expone esta opción global, sin datos de empresas.
- `PUT /api/accounting-settings`: solo administrador. Recibe `{ "allow_cfdi_reuse": true }` o `false` como booleano JSON obligatorio y responde `200` con el valor persistido en el mismo formato de GET. Campo ausente, nulo o no booleano: `422`, error en `allow_cfdi_reuse`. Contador: `403`; sin sesión: `401`. No hay modificación por empresa ni caché que mantenga un valor anterior tras guardar.
- Se conserva `GET /api/companies/{companyId}/fiscal-documents?include=policy-links`. `policy_links` ya contiene todas las pólizas de esa empresa con ID, estado y periodo, sin limitar los vínculos al periodo visible. El selector combina esos vínculos con la configuración y los IDs inicialmente relacionados a la póliza editada. No usar `accounted`: actualmente significa existencia de una póliza POSTED y no detecta uso exclusivo en borradores. No cambiar ese campo ni los listados de SPEC-004.
- POST/PUT de pólizas conservan su payload. Reutilización prohibida: `422` con `errors.fiscal_document_ids` como lista de mensajes que identifican los UUID en conflicto, por ejemplo «El CFDI {uuid} ya está usado en otra póliza». No exponer documentos o pólizas de empresas ajenas. La respuesta sigue el formato de validación actual.

## Persistencia y compatibilidad

Crear una tabla `accounting_settings` con una única fila global de ID fijo `1`, booleano `allow_cfdi_reuse` no nulo con valor inicial `false` y timestamps. La migración inserta esa fila también en instalaciones existentes. No modificar las relaciones históricas ni agregar unicidad por documento en la tabla de vínculos: se permiten relaciones múltiples cuando la opción está activa y deben conservarse las anteriores.

Una ausencia inesperada de configuración no equivale a permitir reutilización: fallar sin guardar y devolver error recuperable. La fila se crea en la migración, no mediante un seeder opcional. No requiere cambios monetarios ni migrar estados fiscales.

## Guardado, autorización e integridad

Integrar la comprobación compartida en creación y actualización de `AccountingPolicyController`, dentro de la transacción existente y antes de reemplazar partidas, vínculos o sugerencias. Mantener autorización por empresa, validación de cuentas, balance, fechas y reserva de trabajo.

Después de bloquear el periodo y, en edición, la póliza como hoy, bloquear la fila global de configuración con `lockForUpdate`. Todas las escrituras de pólizas, independientemente del periodo, usan ese mismo bloqueo; PUT de configuración lo usa también. Mantener ese orden sin adquirir periodos después de la configuración. Leer el valor y los vínculos con una lectura vigente bajo bloqueo, no desde la captura del cliente ni desde un snapshot anterior a adquirirlo. Así se serializan el cambio de opción y la comprobación/creación de vínculos, incluso entre periodos; la reserva de un periodo por sí sola no cubre este caso.

En edición, obtener del servidor los IDs ya relacionados con la póliza bloqueada. Calcular vínculos nuevos como IDs solicitados menos IDs persistidos; si la opción está desactivada, buscar para esos IDs cualquier vínculo a otra póliza de la misma empresa, sin filtrar estado o periodo. Rechazar todos los conflictos antes de escribir. Conservar los IDs anteriores no es una reutilización nueva, aunque estén compartidos. Retirar un vínculo y volver a agregarlo antes de guardar no lo convierte en nuevo; retirarlo mediante un guardado sí lo hace para una incorporación posterior. El rollback cubre póliza, partidas, vínculos y sugerencias. No imponer una restricción única incompatible con la opción activa.

La generación de vista previa continúa sin guardar ni reservar CFDI. La comprobación definitiva ocurre al guardar, aunque la vista previa o selección se hayan hecho antes del cambio de disponibilidad.

## Interfaz y responsabilidades

- Administración: agregar una sección «Configuración» en el área existente `src/features/admin`, con la opción y una explicación de su alcance global. Carga, guardado, error recuperable y confirmación de éxito diferenciados. No presentar un cambio fallido como persistido ni ofrecerlo al contador.
- Datos: contrato compartido de configuración, servicio y export público en la feature responsable; el editor consume el export mediante su hook de solicitudes. Mantener API → hook → componente; `fetch` permanece solo en el cliente compartido.
- Selector: al abrirlo, actualizar configuración y documentos con sus vínculos. Durante carga o error no aceptar vínculos nuevos ni continuar con ellos; conservar la captura y permitir reintentar. Ignorar respuestas de un contexto anterior.
- Con la opción desactivada, deshabilitar la casilla de documentos usados que no estuvieran vinculados originalmente a la póliza editada. Mostrar «Ya usado en otra póliza» junto al documento, asociado al control accesible, no solo mediante color o tooltip. Mantenerlos en búsqueda y conteo de coincidencias; no contarlos como seleccionados nuevos. «Ver conceptos» y la consulta de vínculos no se deshabilitan.
- Si una selección nueva previa queda bloqueada al refrescar, retirarla de la selección nueva e informar el motivo, sin borrar partidas ni correcciones existentes. Al recibir `422` de guardado, mostrar el error con UUID, conservar la captura y permitir revisar vínculos; no reenviar ni eliminar datos automáticamente. La protección definitiva es del servidor.
- Al editar, conservar los vínculos iniciales y el tratamiento histórico de otros periodos. No reconstruir tabla o filtros: la diferencia previamente documentada entre CA-006-19/20 y la lista actual sigue fuera de esta entrega.

## Orden y pruebas

Primero migración, permisos y contrato de configuración; después validación transaccional y pruebas backend; luego administración y selector frontend con el contrato disponible. No hay decisiones bloqueantes.

Backend: ampliar pruebas de SPEC-006 para valor inicial en instalaciones nuevas/existentes, persistencia, validación de booleanos, autorización, ambas posiciones de la opción, uso en DRAFT/POSTED y otros periodos, vínculos previos compartidos, retirada y posterior incorporación, payload manipulado, configuración cambiada con pantalla abierta y rollback incluyendo sugerencias. Probar dos conexiones/transacciones contra un motor con bloqueos reales para el mismo CFDI entre periodos y la serialización con el cambio de opción; SQLite en memoria no acredita concurrencia. Ejecutar regresiones de SPEC-001/002/004/006/007 según impacto; adaptar casos de reutilización existentes para activar explícitamente la opción.

Frontend: Vitest y React Testing Library para guardar configuración, errores, carga y reintento; selección bloqueada con ratón/teclado, búsqueda y consulta de conceptos accesibles, opción activa, borradores, vínculos de otros periodos, edición con relaciones anteriores compartidas, refresco de selecciones, respuestas obsoletas y rechazo del servidor conservando captura. Mantener regresiones de propuesta, sugerencias y vista de conceptos; comprobar tipos, lint y formato. QA humana revisa claridad de la opción, motivo del bloqueo y operación en anchos estrechos, sin exigir prueba integral por navegador.

## Evidencia de partida

`FiscalDocumentController::index` ya entrega `policy_links` sin recorte de periodos y calcula `accounted` solo con POSTED. `AccountingPolicyController::replaceDetails` valida empresa, pero no restringe reutilización. El editor actual filtra por periodo/búsqueda sin bloquear documentos usados; sus pruebas incluyen vínculos DRAFT y POSTED. No existe una ruta de configuración global en `routes/api.php`.
