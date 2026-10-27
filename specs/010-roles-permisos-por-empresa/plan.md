# Plan técnico — SPEC-010

El plan de implementación queda pendiente hasta resolver las preguntas bloqueantes de [spec.md](spec.md). No se definen todavía modelos, migraciones, endpoints ni contratos de permisos.

## Contratos y datos

Pendiente: la matriz de roles y permisos y las reglas del administrador global determinan el modelo de asignación por empresa, las respuestas de identidad y los permisos que deberá exponer el backend.

## Responsabilidades y orden de integración

- Backend: pendiente de acordar roles, permisos, administración de asignaciones y migración segura de usuarios actuales.
- Frontend: pendiente de acordar la matriz y los datos de autorización que recibirá la interfaz.
- Orden: definir primero perfiles y reglas de acceso; después acordar contratos backend y reflejarlos en frontend.

## Estrategia de pruebas

Pendiente de los criterios bloqueados. La entrega deberá comprobar autorización permitida y denegada por empresa, peticiones directas y regresiones de aislamiento; cualquier interacción nueva de interfaz requerirá pruebas de componentes y comportamiento.

## Bloqueantes técnicos

- No es posible fijar contratos ni cobertura por acción hasta aprobar la matriz de roles y permisos.
