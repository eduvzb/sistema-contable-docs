# Plan técnico — SPEC-002

## Actualización pendiente: CA-002-13/14/15/16

### Responsabilidades y compatibilidad

- Cambio sólo de frontend. `company-workspace.tsx` retira los accesos duplicados del encabezado y sus filas vacías; conserva los controles de las pestañas y «Habilitar ejercicio». Componer una franja de periodo y reserva con el estilo compacto existente, sin rediseñar la identidad visual.
- `PeriodSelector` deriva la ocupación de `AccountingPeriod.work_reservation`: reserva presente significa ocupado; `null` significa disponible. No deducir ocupación de `OPEN`/`CLOSED`. El campo opcional ausente no acredita disponibilidad: conservar la validación o recargar el periodo antes de presentar ese dato como confirmado. La franja conserva la identificación del responsable; el selector sólo muestra ocupación.
- Reutilizar las consultas y operaciones de reserva existentes. Tras tomar o liberar, sincronizar el periodo de la franja y la lista del selector; ante `PERIOD_RESERVED`, recuperar el estado autorizado del servidor. No añadir sondeo ni tiempo real. Mantener separación por empresa y descartar respuestas de un contexto anterior.
- Crear una notificación reutilizable en `src/shared/ui/` y alojar su proveedor/cola en el espacio de empresa. Las funcionalidades emiten texto y tono mediante un hook de presentación, sin introducir llamadas API en componentes. Usar identificadores y temporizadores independientes; limpiar temporizadores al cerrar o desmontar y descartar avisos de la empresa anterior al cambiar de empresa.
- Renderizar la región de avisos fuera del flujo, con ancho limitado al viewport y cierre accesible; los éxitos usan anuncio de estado y los errores generales anuncio de alerta. No mover el foco. Integrar los avisos de acciones de las pestañas, incluidos los originados en diálogos; conservar errores de campo y estados persistentes en su lugar. No migrar indiscriminadamente todos los componentes `Notice`.
- No hay endpoints, migraciones, cambios monetarios ni cambios de autorización nuevos. Los contratos de reserva que siguen abajo se conservan como referencia vigente, no como trabajo backend pendiente.

### Orden y comprobación

1. Incorporar la infraestructura de avisos y sus pruebas de cierre, temporización, mensajes sucesivos y desmontaje.
2. Ajustar encabezado, franja y selector; integrar la sincronización de reservas sin cambiar selección, navegación o permisos.
3. Migrar avisos de acciones del espacio de empresa y sus pestañas, comprobando éxitos y errores generales sin duplicados en flujo.

Vitest y React Testing Library: ausencia de botones sólo en encabezado, permanencia en pestañas; meses libres, propios y ajenos, cambio de ejercicio sin selección, consulta de ocupados y actualización tras reserva/liberación/conflicto; regresiones de permisos y carga. Con temporizadores controlados comprobar los 5 segundos, cierre manual, cola, anuncios accesibles y limpieza al cambiar de empresa. Cubrir acciones de cada pestaña migrada y la permanencia de errores de campos. Ejecutar formato, lint, TypeScript, pruebas y build según los scripts del frontend.

QA humana pendiente: franja y avisos a 320/390 px y escritorio, nombres largos, varios avisos y diálogos abiertos; comprobar que no hay espacio vacío ni saltos de layout y que controles y cierres son utilizables. No se exige un recorrido integral automatizado por navegador.

Sin bloqueantes para preparar esta actualización.

## Contratos vigentes de selección y reserva

## Contratos y responsabilidades

- Mantener el estado contable del periodo (`OPEN`/`CLOSED`) separado de la reserva de trabajo (`Disponible`/reservado por una persona). Habilitar un ejercicio sigue creando doce meses; la reserva no cambia el estado contable.
- Agregar una operación autenticada para tomar la reserva de un periodo disponible. La reserva debe obtenerse antes de empezar la captura de pólizas. Si otra persona ya la tiene, responder con el conflicto `PERIOD_RESERVED` y los datos del responsable; el servidor es la autoridad aunque la interfaz esté desactualizada.
- Reutilizar la liberación de reserva existente. El dueño puede liberar su periodo; un administrador puede liberar una reserva ajena. La acción visual se llama «Liberar reserva» para distinguirla del cierre contable.
- Las consultas siguen disponibles mientras otra persona tiene la reserva. Crear o modificar pólizas queda limitado al dueño de la reserva y se comprueba también en backend.

## Integración y pruebas

Primero agregar la toma explícita de reserva y ajustar la autorización de las escrituras de póliza; después integrar la acción y el estado visible en el selector de periodos y el espacio de trabajo. Conservar el bloqueo transaccional por periodo.

Backend: comprobar creación de los doce meses sin reserva, adquisición de un periodo disponible, conflicto ante una adquisición simultánea, acceso de lectura mientras existe reserva y liberación por el dueño o administrador. Reutilizar las pruebas de autorización de reserva; el rechazo de escrituras de póliza por terceros se especifica en SPEC-006. Probar concurrencia con el motor configurado para el proyecto.

Frontend: con Vitest y React Testing Library, comprobar selección de ejercicio y mes, toma y liberación de reserva, responsable visible, errores recuperables, acciones de póliza bloqueadas para terceros y actualización tras liberación. La revisión visual humana valida que el panel flotante y los avisos no desplacen los controles, y que el estado contable se distinga de la reserva.

## Bloqueantes

Ninguno de dominio para esta entrega. La reserva de trabajo no introduce el cierre/reapertura contable formal.

## Contrato de implementación acordado

`POST /api/companies/{companyId}/accounting-periods/{periodId}/work-reservation` devuelve `201` y `{data: WorkReservationResource}`. Repite la reserva del dueño sin duplicarla. La autorización de empresa y el bloqueo transaccional del periodo se mantienen. Una reserva ajena responde `409 PERIOD_RESERVED`; `DELETE` conserva `204`. La interfaz usa «Tomar para trabajar» y «Liberar reserva». SPEC-006 aplica la propiedad obligatoria en guardados.
