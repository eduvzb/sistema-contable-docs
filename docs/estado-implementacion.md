# Estado de implementación y continuidad

- **Actualizado:** 2026-09-24
- **Propósito:** punto de entrada entre sesiones. Este documento no mantiene otra tabla de estados ni sustituye las specs.

## Dónde está la información vigente

1. El [índice de specs](../specs/README.md) muestra una tabla generada desde el campo `Estado` de cada `spec.md`. Si difieren, ejecutar `python3 scripts/spec_index.py --check` y corregir la fuente responsable antes de continuar.
2. `specs/NNN-nombre/spec.md` define el estado, los criterios de la entrega y el comportamiento esperado. Es la única autoridad documental para esas preguntas.
3. `plan.md` contiene contratos, dependencias y enfoque técnico. `tasks-backend.md` y `tasks-frontend.md` enumeran únicamente trabajo técnico pendiente por repositorio.
4. `verificacion.md` conserva pruebas realmente ejecutadas, revisiones, PR y recorridos de QA. Cada entrega histórica queda separada de los criterios añadidos o modificados después.

Para retomar una tarea, abre primero `spec.md` y luego sólo los archivos pertinentes a la fase. Conserva cambios locales existentes; verifica el estado Git de los tres repositorios antes de editar o crear ramas de implementación. El [flujo SDD](flujo-spec.md) define las transiciones y el ciclo Git.

```sh
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable status --short --branch
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable-backend status --short --branch
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable-frontend status --short --branch
```

El repositorio de specs conserva su rama documental. Las ramas, commits y PR de implementación corresponden sólo a los repositorios de backend/frontend afectados; ningún resumen de relevo promociona una spec a QA o Implementada.
