# Plan técnico — SPEC-NNN

Sólo cambios técnicos necesarios para los CA de [spec.md](spec.md). No repetir requisitos ni describir lo que no cambia.

Explica los cambios con frases directas. Usa nombres exactos de rutas, campos o estados cuando sean necesarios, sin añadir jerga para lo que puede decirse de forma sencilla.

## Contratos y datos

Operación, entradas/salidas y cambios de datos. Incluir precisión, autorización, integridad, errores o compatibilidad cuando cambien; referenciar los CA. Si no hay cambios, indicarlo.

## Responsabilidades y orden de integración

- Backend: cambio necesario, o ninguno.
- Frontend: cambio necesario, o ninguno.
- Orden: dependencia concreta, o trabajo independiente.

## Estrategia de pruebas

Qué comportamiento y regresión comprobar. Para interacción Next/React, Vitest y React Testing Library; la revisión visual es QA humana. Resultados en `verificacion.md`, no aquí.

## Bloqueantes técnicos

Ninguno, o decisión técnica pendiente. Omitir riesgos genéricos y decisiones cerradas.
