# Sistema contable — Specs y documentación

Documentación de trabajo para los repositorios independientes de backend y frontend. El código y las pruebas muestran lo que el producto hace hoy; las specs describen cambios pendientes y comportamiento que se quiere desarrollar.

## Empezar una tarea

1. Encuentra la funcionalidad en el [índice de specs](specs/README.md).
2. Contrasta `spec.md` con el código y las pruebas del repositorio afectado. Abre `plan.md` y las tareas sólo si hay un cambio pendiente; usa `verificacion.md` para el cierre de la entrega actual.
3. Aplica el [flujo SDD](docs/flujo-spec.md) para preparar, implementar y verificar esa spec.

| Necesidad | Documento |
|---|---|
| Instrucciones del agente | [AGENTS.md](AGENTS.md) |
| Principios para cambios futuros | [Constitución](docs/constitution.md) |
| Contexto de dominio y alcance | [Mapa de fuentes](docs/fuentes.md) |
| Crear o actualizar una spec | [Flujo](docs/flujo-spec.md) y [cinco plantillas](specs/_plantilla/spec.md) |
| Trabajar una spec de principio a fin | [Prompt maestro](docs/prompt-master-spec.md) |
| Consultar el contexto del producto | [Planeación](docs/planeacion/00%20-%20Inicio.md) |

El [índice de specs](specs/README.md) muestra los estados de trabajo generados desde cada `spec.md`. Ante una diferencia sobre comportamiento implementado, verifica el código y sus pruebas antes de actualizar la documentación. Git conserva el historial de cambios.
