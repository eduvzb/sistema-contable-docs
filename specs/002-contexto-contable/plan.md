# Plan técnico — SPEC-002

## Contratos y responsabilidades

- Mantener el estado contable del periodo (`OPEN`/`CLOSED`) separado de la reserva de trabajo (`Disponible`/reservado por una persona). Habilitar un ejercicio sigue creando doce meses; la reserva no cambia el estado contable.
- Agregar una operación autenticada para tomar la reserva de un periodo disponible. La reserva debe obtenerse antes de empezar la captura de pólizas. Si otra persona ya la tiene, responder con el conflicto `PERIOD_RESERVED` y los datos del responsable; el servidor es la autoridad aunque la interfaz esté desactualizada.
- Reutilizar la liberación de reserva existente. El dueño puede liberar su periodo; un administrador puede liberar una reserva ajena. La acción visual solicitada se llama «Cerrar periodo», pero únicamente libera la reserva de trabajo.
- Las consultas siguen disponibles mientras otra persona tiene la reserva. Crear o modificar pólizas queda limitado al dueño de la reserva y se comprueba también en backend.

## Integración y pruebas

Primero agregar la toma explícita de reserva y ajustar la autorización de las escrituras de póliza; después integrar la acción y el estado visible en el selector de periodos y el espacio de trabajo. Conservar el bloqueo transaccional por periodo.

Backend: comprobar creación de los doce meses sin reserva, adquisición de un periodo disponible, conflicto ante una adquisición simultánea, acceso de lectura mientras existe reserva y liberación por el dueño o administrador. Reutilizar las pruebas de autorización de reserva; el rechazo de escrituras de póliza por terceros se especifica en SPEC-006. Probar concurrencia con el motor configurado para el proyecto.

Frontend: con Vitest y React Testing Library, comprobar abrir/cerrar, responsable visible, errores recuperables, acciones de póliza bloqueadas para terceros y actualización tras liberación. La revisión visual humana valida que «Disponible», «Trabajando por…» y «Cerrar periodo» no se confundan con el cierre contable.

## Bloqueantes

Ninguno de dominio para esta entrega. La reserva de trabajo no introduce el cierre/reapertura contable formal.

## Contrato de implementación acordado

`POST /api/companies/{companyId}/accounting-periods/{periodId}/work-reservation` devuelve `201` y `{data: WorkReservationResource}`. Repite la reserva del dueño sin duplicarla. La autorización de empresa y el bloqueo transaccional del periodo se mantienen. Una reserva ajena responde `409 PERIOD_RESERVED`; `DELETE` conserva `204`. La interfaz usa «Abrir periodo» y «Cerrar periodo». SPEC-006 aplica la propiedad obligatoria en guardados.
