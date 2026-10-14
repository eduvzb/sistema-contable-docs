# Instrucciones para agentes

Este repositorio contiene documentación y specs compartidas del sistema contable. La implementación vive en los repositorios hermanos de backend y frontend.

## Antes de cambiar comportamiento

1. Localiza la funcionalidad en el [índice de specs](specs/README.md).
2. Respeta la [constitución](docs/constitution.md) y verifica el comportamiento actual en código y pruebas antes de proponer un cambio.
3. Lee `specs/NNN-nombre/spec.md` para conocer el alcance previsto y el estado de trabajo. Si hay implementación pendiente, abre su `plan.md` y las tareas del repositorio afectado; para cerrar la entrega, abre `verificacion.md`. Consulta las fuentes de dominio pertinentes según el [mapa](docs/fuentes.md), sin cargar toda Planeación por rutina.
4. Sigue el [flujo SDD](docs/flujo-spec.md): aclara los bloqueantes de esa spec y registra el comportamiento esperado antes de implementar. No inventes reglas de negocio.

## Durante el trabajo

- Para nuevas specs y próximas entregas, usa definiciones pequeñas y directas: objetivo breve, alcance acotado y criterios observables. No repitas los CA en historias, reglas o casos límite; integra errores y límites en los propios criterios. Mantén contratos en `plan.md`, trabajo en tareas y evidencia en `verificacion.md`. No reescribas specs existentes fuera del cambio solicitado ni elimines criterios vigentes para abreviar.
- Escribe las specs en lenguaje natural, como explicarías el cambio a otra persona. Usa frases cortas, sujetos y acciones claros, y palabras habituales; evita fórmulas rígidas, jerga innecesaria y siglas sin explicar. Conserva nombres técnicos exactos sólo cuando sean necesarios para implementar o comprobar el resultado. Claridad no significa sobreexplicar ni perder precisión.
- Realiza el cambio coherente más pequeño que cumpla la spec, usando las convenciones del framework.
- Reutiliza la spec al cambiar una funcionalidad existente. Si la documentación contradice el código, confirma primero qué hace el producto; registra el comportamiento deseado como cambio explícito antes de implementarlo.
- Las instrucciones explícitas del usuario definen el cambio solicitado; registra criterios o dudas pendientes sin mantener un diario de decisiones cerradas.
- Preserva integridad, aislamiento y trazabilidad. Confirma responsabilidades y precisión monetaria en los contratos y el código vigentes.
- Para comportamiento interactivo nuevo o modificado en Next/React, agrega pruebas de componentes y comportamiento con Vitest y React Testing Library. No sustituyas esa cobertura con snapshots ni con pruebas integrales por navegador.
- Registra problemas ajenos al alcance sin resolverlos dentro del mismo cambio.

## Al terminar

- Verifica los criterios de aceptación y las regresiones relevantes. Las reglas de negocio requieren pruebas de comportamiento esperado y errores, no de detalles internos.
- Registra en `verificacion.md` sólo la evidencia de la entrega en curso y su QA pendiente. Conserva en `spec.md` los criterios y el estado de trabajo; el código y las pruebas acreditan lo implementado. Retira las tareas cerradas tras comprobar su «Hecho cuando».
- Cuando implementación y comprobaciones técnicas estén completas, marca la spec como QA. No realices ni exijas una comprobación integral de interfaz por navegador: la validación visual corresponde a una persona.
- Marca la spec como Implementada únicamente cuando la aprobación de QA humana esté registrada conforme al flujo.
- Regenera el índice con `python3 scripts/spec_index.py --write` si cambia un estado y ejecuta `python3 scripts/spec_index.py --check` al cerrar el trabajo documental.
