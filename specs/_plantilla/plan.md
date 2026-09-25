# Plan técnico — SPEC-NNN

La definición y el estado vigentes están en [spec.md](spec.md). Este plan referencia sus CA y no crea reglas de negocio.

## Contratos y datos

Operaciones, entradas, salidas, representación de importes, persistencia y compatibilidad necesarios para los CA de esta entrega. Registrar la spec responsable de cada contrato compartido.

## Responsabilidades y orden de integración

- Backend: validación autoritativa, autorización, persistencia y API aplicables.
- Frontend: presentación, interacción y estado de interfaz aplicables.
- Dependencias: contrato que debe estar disponible antes de una tarea consumidora; enlazar los IDs de las tareas afectadas.

## Errores e integridad

Errores observables, aislamiento por empresa, atomicidad y regresiones aplicables. Referenciar los CA.

## Estrategia de pruebas

Pruebas de comportamiento backend y regresiones pertinentes. Para interacción nueva o modificada en Next/React, usar Vitest y React Testing Library conforme a DT-012; reservar layout real para QA visual humana. No registrar resultados no ejecutados aquí.

## Decisiones técnicas y pendientes

Decisiones necesarias para implementar y cuestiones técnicas que bloquean el alcance. Las tareas se dividen entre [backend](tasks-backend.md) y [frontend](tasks-frontend.md); los resultados viven en [verificacion.md](verificacion.md).
