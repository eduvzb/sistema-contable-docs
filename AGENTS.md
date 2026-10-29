# Guía breve para trabajar en Braval

Este repositorio guarda decisiones de producto y specs; el código vive en los repositorios hermanos `sistema-contable-backend` y `sistema-contable-frontend`.

1. Antes de cambiar comportamiento, mira código y pruebas. Consulta [fuentes de dominio](docs/fuentes.md) sólo si aportan al caso. No inventes reglas contables o fiscales.
2. Para un cambio pequeño con resultado claro, implementa y prueba directamente. Usa una [spec](docs/flujo-spec.md) cuando haya decisiones de negocio, varios contratos, migraciones o riesgos que deban acordarse. Reutiliza la spec existente si corresponde.
3. Escribe lo mínimo que permita entender el cambio de un vistazo: objetivo, alcance y resultados observables; errores y límites sólo si afectan la decisión. Plan, tareas y evidencia separada sólo cuando aporten información nueva. No reduzcas criterios vigentes de specs anteriores para adaptar el formato.
4. Respeta aislamiento por empresa, contexto de periodo, integridad y precisión monetaria. Para cambios interactivos en Next/React, prueba comportamiento con Vitest y React Testing Library.
5. Ejecuta las pruebas relevantes y comunica resultados reales y pendientes. Backend: usa Sail y la base de pruebas aislada según su README; si no está disponible, indica el bloqueo. La validación visual humana no se atribuye al agente.

No se requieren ramas, commits, publicación ni PR para completar este flujo. Sólo se hacen por solicitud expresa; la skill de entrega del workspace es opcional. Se puede delegar investigación o trabajo independiente cuando ahorre contexto; el responsable de la tarea conserva las decisiones, integra resultados y comunica bloqueos. No se delegan decisiones de negocio pendientes ni se atribuyen pruebas ajenas sin evidencia. Protege cambios locales previos.

Si editas specs, ejecuta `python3 scripts/spec_index.py --check` desde este repositorio; regenera el índice sólo cuando corresponda y sin sobrescribir cambios ajenos.
