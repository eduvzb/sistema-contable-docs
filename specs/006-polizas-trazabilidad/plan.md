# Plan técnico — SPEC-006

## Contratos y responsabilidades

- **Tipos de póliza:** sustituir la lista fija de enum por un catálogo global persistente, administrado solo por administradores, manteniendo los códigos INGRESO, EGRESO y DIARIO. Preservar los tipos históricos en las pólizas; tipos inactivos no se ofrecen para pólizas nuevas. Tipos en uso no se borran y pueden desactivarse.
- **Selector CFDI:** reutilizar `policy_links`, que ya entrega estado y periodo de todos los vínculos. Derivar los estados de esos vínculos: disponible = sin vínculos; contabilizado = al menos un vínculo con estado POSTED; Todos = sin filtro de estado. Un CFDI solo ligado a borradores pertenece a Todos, no a Disponibles ni a Contabilizados. Mantener la opción global de reutilización como autorización definitiva para vínculos nuevos; los filtros no la reemplazan. No se necesita un contrato backend nuevo para filtrar.
- **Filtros avanzados:** implementar CA-006-19/20 como tabla con filtros de fecha, tipo, RFC, nombre, monto, folio fiscal e interno según criterios ya definidos. Los filtros son locales a la consulta recibida y mantienen las selecciones vigentes al cambiar de filtro.
- **Reserva de periodo:** incorporar la adquisición explícita al abrir un periodo, reutilizando `WorkReservationService`. La operación de cierre visual libera la reserva con el endpoint existente; administrador puede liberar reservas ajenas. La adquisición se confirma antes de iniciar cambios y los guardados de póliza exigen ser dueño de la reserva. No alterar el estado contable del periodo.

## Persistencia y compatibilidad

- El catálogo de tipos será global, no por empresa. La migración debe conservar los valores existentes y la representación de pólizas históricas. La estructura final debe permitir desactivación sin borrar el tipo referenciado.
- Los vínculos CFDI existentes y su estado POSTED/DRAFT siguen siendo la fuente de la disponibilidad. No ocultar documentos de las consultas de SPEC-004.
- La reserva de periodo permanece separada de `AccountingPeriod.status`. El conflicto de reserva conserva el código y respuesta `PERIOD_RESERVED` existentes.

## Orden e integración

Primero definir el rol que administra los tipos y preparar la persistencia de ese catálogo; después exponer los contratos y conectar el formulario de póliza. En paralelo, construir los estados y filtros del selector desde `policy_links`, conservando la validación de reutilización ya implementada. Para la reserva, añadir la toma explícita desde el contexto de periodo, retirar la adquisición implícita al guardar y exigir una reserva propiedad del usuario en POST/PUT. Ajustar la interfaz de periodo y editor para mostrar responsable y «Cerrar periodo».

## Pruebas

Backend: preservar los tres tipos existentes e historial; probar creación, edición, activación/desactivación, borrado rechazado de tipos usados y autorización según el rol acordado. Probar CFDI sin vínculo, con vínculo DRAFT, con vínculo POSTED y con ambos estados; confirmar que cada filtro da el conjunto esperado y que la opción global sigue rechazando vínculos prohibidos. Probar reserva explícita, dos usuarios concurrentes, guardados sin reserva o por tercero, lectura, liberación por dueño y administrador.

Frontend: Vitest y React Testing Library para el CRUD de tipos, filtro inicial y cambios entre estados, preservación de selección, filtros avanzados, reserva al abrir, mensaje de responsable, consulta de solo lectura y liberación. Mantener regresiones de propuesta y trazabilidad. Revisar tipos, lint y formato; QA humana revisa claridad y operación de los selectores, sin exigir prueba integral por navegador.

## Bloqueantes

Ninguno de dominio para la preparación de esta entrega.

## Contrato de implementación acordado

`GET /api/accounting-policy-types` devuelve `{data: [{id, code, name, active}]}` a usuarios operativos. `POST`, `PUT /{id}` y `DELETE /{id}` requieren administrador. Los códigos únicos se normalizan a mayúsculas (máximo 64 caracteres), los nombres admiten 255. Un código usado se conserva, mientras nombre y activación pueden editarse. El campo `type` de póliza sigue siendo el código; los tres valores originales e historial permanecen. Un tipo inactivo ya asociado puede conservarse sin reasignación.

Los guardados exigen reserva propia bajo el mismo bloqueo del periodo: reserva ajena responde `409 PERIOD_RESERVED`; sin reserva, `409 WORK_RESERVATION_REQUIRED`. No adquieren implícitamente una reserva. Depende del endpoint y controles de SPEC-002. La integración conjunta se comprueba antes de publicar; cada PR explica la dependencia.
