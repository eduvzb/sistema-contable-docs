# Flujo de specs

Una spec describe un cambio deseado. Para saber qué hace el producto hoy, consulta el código, las pruebas y los contratos de los repositorios de backend y frontend. Si difieren de una spec, verifica la diferencia antes de editar: el comportamiento ya implementado se documenta como hecho y el nuevo resultado se redacta como trabajo pendiente.

Cada funcionalidad tiene `spec.md` (resultado esperado y estado de trabajo), `plan.md` (contratos de la entrega pendiente), `tasks-backend.md`, `tasks-frontend.md` y `verificacion.md` (comprobación de la entrega actual y QA). Las tareas terminadas y las cronologías se consultan en Git; no se mantienen como listas paralelas.

## Preparar un cambio

1. Localiza la funcionalidad en el [índice](../specs/README.md). Reutiliza su spec para cambios de una función existente. Para una capacidad nueva, toma el siguiente ID libre y usa las [plantillas](../specs/_plantilla/spec.md).
2. Lee el código y las pruebas de los repositorios afectados. Consulta las fuentes de dominio pertinentes sólo para aclarar el requisito o un conflicto; el [mapa de fuentes](fuentes.md) indica qué aporta cada una.
3. En `spec.md`, escribe objetivo, alcance, actores, criterios observables, errores, casos límite y exclusiones. Conserva los IDs de CA existentes; agrega otros sin renumerar. Distingue una duda que bloquea el cambio de una ampliación futura.
4. En `plan.md`, define únicamente contratos o migraciones nuevos, autorización, integridad y orden de integración. Crea tareas pendientes por repositorio con CA, dependencia y «Hecho cuando» comprobable. Evita copiar decisiones cerradas o describir de nuevo todo el producto.

| Estado de trabajo | Condición |
|---|---|
| Borrador | Falta definir un comportamiento necesario o resolver una duda bloqueante. |
| Lista | Cambio nuevo con criterios y plan preparados para implementar. |
| Actualización pendiente | Funcionalidad existente con criterios nuevos o revisados aún sin cierre técnico. |
| QA | Código y comprobaciones técnicas de la entrega completos; resta validación visual humana. |
| Implementada | QA humana aprobada y registrada. |

El estado de `spec.md` sirve para organizar trabajo. No demuestra por sí mismo qué está implementado. El [índice](../specs/README.md) lo genera `python3 scripts/spec_index.py --write`; `--check` valida consistencia y enlaces.

## Implementar y comprobar

- Antes de editar código, revisa `AGENTS.md` de cada repositorio afectado y su estado Git. Backend y frontend deben estar limpios. Protege cualquier cambio local previo en el repositorio documental.
- Trabaja en ramas aisladas desde `main` sólo en repositorios de implementación afectados, con nombre `codex/<tipo>/SPEC-NNN/<slug>` disponible en todos ellos. Mantén los contratos compartidos coordinados entre ambos repositorios.
- Implementa los CA pendientes y prueba comportamientos válidos, errores, autorización, integridad y regresiones relevantes. Para interacciones Next/React usa Vitest y React Testing Library; la disposición visual real queda para QA humana.
- Registra en `verificacion.md` únicamente CA de la entrega, comandos ejecutados, resultados, revisión y PR. Inicia con un resumen de lectura rápida: checks marcados (`[x]`) para cada comportamiento realmente comprobado y checks pendientes (`[ ]`) para cada validación que aún falte. Separa la validación técnica de la QA humana, redacta cada check como un resultado observable y conserva debajo la evidencia que lo respalda. No marques una comprobación por implementación asumida ni agrupes como aprobados recorridos que no se ejecutaron. Retira tareas completadas; no inventes pruebas, enlaces ni aprobaciones.
- Cada repositorio de código afectado termina con commit, rama publicada y PR hacia `main`. Solicita revisión a los colaboradores con acceso. Si falla publicación, PR o asignación de revisores, detén el cierre técnico y reporta la operación fallida; no sustituyas el paso por un estado documental.
- Cuando ambos repositorios afectados tengan cierre técnico y PR, pasa la spec a QA. Sólo la aprobación humana registrada en `verificacion.md` permite Implementada. No se exige una prueba integral por navegador para cerrar el trabajo del agente.

Para un cambio puramente documental no se crean ramas ni PR de implementación. Al terminar, regenera el índice si cambió un estado, ejecuta `python3 scripts/spec_index.py --check` y revisa enlaces y diff. Git conserva la historia de cambios.
