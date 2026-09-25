# Prompt maestro para trabajar una spec

Usa este prompt después de localizar la funcionalidad en el [índice](../specs/README.md). El [flujo SDD](flujo-spec.md) conserva las reglas completas de preparación, pruebas, Git y QA; este prompt no las sustituye.

## Variables

- `SPEC_ID`: por ejemplo, `SPEC-004`.
- `OBJETIVO`: resultado adicional solicitado; omitir para trabajar todo lo pendiente.
- `COMPONENTES`: `documentación`, `backend`, `frontend` o `todos`.
- `RESTRICCIONES`: límites explícitos del usuario.

## Prompt

```text
Trabaja [SPEC_ID] del sistema contable hasta resolver el alcance autorizado.
Objetivo adicional: [OBJETIVO o «criterios vigentes pendientes»].
Componentes autorizados: [COMPONENTES o «todos»].
Restricciones: [RESTRICCIONES o «ninguna adicional»].

1. Lee los AGENTS.md aplicables, la constitución, las decisiones vigentes, el flujo SDD y el mapa de fuentes. Revisa el estado Git antes de editar. Localiza la carpeta de [SPEC_ID] en specs/README.md.
2. Lee primero spec.md: su campo Estado es la única autoridad documental del estado vigente. Identifica los CA de esta entrega y sus fuentes. Durante implementación, reabre Planeación sólo según los disparadores del flujo.
3. Para preparar o implementar, lee plan.md y las tareas pendientes del repositorio afectado. Consulta contratos de specs dependientes cuando corresponda. Para distinguir trabajo previo y comprobar resultados, lee verificacion.md; su evidencia histórica no acredita CA revisados después.
4. Si cambia el comportamiento esperado, actualiza antes spec.md y sus fuentes responsables. Actualiza plan.md y tareas sólo si cambia la ejecución. No inventes reglas, resultados de pruebas, revisiones Git ni aprobaciones.
5. Implementa exclusivamente los CA autorizados en backend y/o frontend. Cumple la separación de responsabilidades y el preflight Git de docs/flujo-spec.md. Prueba casos válidos, errores y regresiones relevantes; para interacciones Next/React aplica DT-012.
6. Marca una tarea sólo después de comprobar su «Hecho cuando». Registra en verificacion.md CA, pruebas ejecutadas, resultados, revisión y PR de cada repositorio afectado. Reserva layout y recorridos visuales para QA humana.
7. Tras el cierre técnico y los PR requeridos, cambia Estado de spec.md a QA. Sólo una aprobación humana registrada permite Implementada. Regenera el índice con python3 scripts/spec_index.py --write y compruébalo con --check.
8. Informa cambios, CA cubiertos, pruebas reales, PR y recorridos de QA o bloqueantes. No hagas merge ni despliegue automáticamente.
```

Para una consulta o revisión sin cambios, basta con `spec.md` y los documentos que sustenten la respuesta; no se ejecuta el ciclo Git de implementación.
