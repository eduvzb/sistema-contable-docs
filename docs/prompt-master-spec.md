# Prompt para trabajar una spec

Úsalo cuando el requisito ya tenga un ID en el [índice](../specs/README.md). Para un requisito nuevo, primero decide si amplía una spec existente o requiere una carpeta nueva según el [flujo](flujo-spec.md).

```text
Trabaja SPEC-NNN del sistema contable para este objetivo: [resultado solicitado].
Alcance autorizado: [documentación, backend, frontend o todos].
Restricciones adicionales: [si existen].

Lee AGENTS.md y docs/flujo-spec.md. Revisa el estado Git y contrasta spec.md con el código y las pruebas actuales. El código muestra lo implementado; la spec define el resultado solicitado y los CA pendientes. Si hay una diferencia, explica cuál es y prepara el cambio antes de codificar.

Usa plan.md y las tareas sólo para trabajo pendiente. Implementa los CA autorizados, prueba comportamiento y errores relevantes, registra resultados reales y PR en verificacion.md, retira tareas cerradas y actualiza el estado de trabajo. Regenera y comprueba el índice. No inventes reglas, pruebas ni aprobación de QA humana.
```
