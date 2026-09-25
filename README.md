# Sistema contable — Specs y documentación

Fuente compartida de comportamiento para los repositorios independientes de backend y frontend. La documentación de Planeación incorporada aquí es la base versionada vigente; su carpeta original se conserva como procedencia.

## Empezar una tarea

1. Encuentra la funcionalidad en el [índice de specs del MVP](specs/README.md).
2. Lee primero su `spec.md` para conocer estado, comportamiento y criterios. Abre `plan.md`, las tareas del repositorio afectado y `verificacion.md` según la fase.
3. Aplica el [flujo SDD](docs/flujo-spec.md) para preparar, implementar y verificar esa spec.

| Necesidad | Documento |
|---|---|
| Instrucciones del agente | [AGENTS.md](AGENTS.md) |
| Principios que deben conservarse | [Constitución](docs/constitution.md) |
| Stack, responsabilidades y decisiones compartidas | [Decisiones](docs/decisiones.md) |
| Saber qué documento tiene autoridad y de dónde proviene | [Mapa de fuentes](docs/fuentes.md) |
| Crear o actualizar una spec | [Flujo](docs/flujo-spec.md) y [cinco plantillas](specs/_plantilla/spec.md) |
| Trabajar una spec de principio a fin | [Prompt maestro](docs/prompt-master-spec.md) |
| Entender el negocio desde el inicio | [Planeación](docs/planeacion/00%20-%20Inicio.md) |

El [índice de specs](specs/README.md) muestra los estados generados desde cada `spec.md`. Este repositorio contiene la fuente compartida; backend y frontend viven en repositorios independientes. La evidencia de cada revisión se registra en `verificacion.md` dentro de la carpeta correspondiente.
