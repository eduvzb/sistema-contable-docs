# Plan técnico — SPEC-003

## Contratos y persistencia

- Sustituir la plantilla general codificada en `GeneralAccountTemplate` por una plantilla SAT global administrable y versionada. El layout descargable es CSV UTF-8 con encabezado `code,name,nature,parent_code,accepts_entries,active,sat_grouping_code`; la importación se hace una vez en la plantilla y crea una versión activa. La creación de una empresa copia esa versión dentro de la transacción de creación.
- Cada catálogo de empresa permanece independiente. Una nueva versión global solo se usa para empresas creadas después de activarla; no actualiza cuentas de empresas existentes ni modifica sus movimientos.
- Conservar el significado vigente de `accepts_entries`: solo cuentas activas con esta marca pueden elegirse y usarse en partidas. Esta entrega no agrega una regla de hoja sin hijas.
- La importación por empresa existente continúa disponible conforme al contrato actual de SPEC-003. No se cambia su semántica como efecto lateral de importar la plantilla global.

## Integración y pruebas

Backend: persistir versiones de la plantilla global, autorizar su administración, validar el archivo antes de activarlo y mantener la versión previa si falla la importación. Reutilizar las reglas actuales del importador para códigos, naturaleza, jerarquía, banderas y código agrupador SAT. Probar copia en creación de empresa, aislamiento entre empresas, creación posterior a un cambio de plantilla y ausencia de cambios en empresas preexistentes.

Frontend: añadir el lugar de administración para consultar e importar la plantilla y mostrar el resultado de la versión activa. Añadir pruebas de comportamiento para carga, error y resultado; usar Vitest y React Testing Library si la interacción es Next/React.

## Bloqueantes

Ninguno para preparar la actualización. El archivo debe seguir el layout definido en CA-003-13; la revisión de vigencia de los datos SAT corresponde a la persona administradora antes de activar cada versión.

## Contrato de implementación acordado

Sólo administradores acceden a `GET /api/account-template`, que devuelve `{data: {version: string, accounts_count: number}}`, `GET /api/account-template/layout`, que descarga el encabezado CSV, y `POST /api/account-template/imports`, multipart `file`, que devuelve `201` con la versión activada y su cantidad de cuentas. Los errores conservan `422` y el detalle por fila. La guía breve vive junto a la descarga en administración. La versión inicial conserva `GENERAL_V1`; no se modifica ningún catálogo empresarial existente. Activación y copia de plantilla se serializan para no producir copias mezcladas.
