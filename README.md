# Sistema contable — Specs y documentación

Fuente compartida de comportamiento para los repositorios independientes de backend y frontend. La documentación de Planeación incorporada aquí es la base versionada vigente; su carpeta original se conserva como procedencia.

## Empezar una tarea

1. Encuentra la funcionalidad en el [índice de specs del MVP](specs/README.md).
2. Lee su comportamiento, criterios, pendientes y únicamente las fuentes que cita.
3. Aplica el [flujo SDD](docs/flujo-spec.md) para preparar, implementar y verificar esa spec.

| Necesidad | Documento |
|---|---|
| Instrucciones del agente | [AGENTS.md](AGENTS.md) |
| Principios que deben conservarse | [Constitución](docs/constitution.md) |
| Stack, responsabilidades y decisiones compartidas | [Decisiones](docs/decisiones.md) |
| Saber qué documento tiene autoridad y de dónde proviene | [Mapa de fuentes](docs/fuentes.md) |
| Crear o actualizar una spec | [Flujo](docs/flujo-spec.md) y [plantilla](specs/_plantilla.md) |
| Trabajar una spec de principio a fin | [Prompt maestro](docs/prompt-master-spec.md) |
| Entender el negocio desde el inicio | [Planeación](docs/planeacion/00%20-%20Inicio.md) |

SPEC-001, SPEC-005 y SPEC-007 a SPEC-009 están en **QA**, pendientes únicamente de validación visual humana. SPEC-002, SPEC-003, SPEC-004 y SPEC-006 están en **Actualización pendiente** por cambios preparados el 2026-09-10 que todavía requieren implementación y comprobación técnica. Este repositorio contiene la fuente compartida, no el código del producto; la evidencia de cada revisión se registra en su spec.
