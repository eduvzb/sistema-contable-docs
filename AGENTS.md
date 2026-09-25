# Instrucciones para agentes

Este repositorio contiene documentación y specs compartidas del sistema contable. No contiene todavía la implementación de backend ni frontend.

## Antes de cambiar comportamiento

1. Localiza la funcionalidad en el [índice de specs](specs/README.md).
2. Respeta la [constitución](docs/constitution.md) y las [decisiones vigentes](docs/decisiones.md).
3. Lee primero `specs/NNN-nombre/spec.md`: es la única autoridad de estado y comportamiento. Para preparar o implementar, abre su `plan.md` y las tareas pendientes de backend o frontend según el repositorio afectado; para comprobar o retomar evidencia, abre `verificacion.md`. Durante ideación, preparación o cambio de comportamiento, consulta las fuentes concretas de la spec; durante implementación reábrela sólo según los disparadores del [flujo](docs/flujo-spec.md). El [mapa de fuentes](docs/fuentes.md) indica su autoridad. No es necesario leer toda Planeación.
4. Sigue el [flujo SDD](docs/flujo-spec.md): aclara los bloqueantes de esa spec y registra el comportamiento esperado antes de implementar. No inventes reglas de negocio.

## Durante el trabajo

- Realiza el cambio coherente más pequeño que cumpla la spec, usando las convenciones del framework.
- Reutiliza la spec al corregir un incumplimiento; actualízala antes de cambiar comportamiento. Documentación y refactors sin efecto observable no requieren otra spec.
- Las instrucciones explícitas del usuario cuentan como decisiones: regístralas donde correspondan, sin pedir confirmaciones repetidas.
- Preserva integridad, aislamiento, trazabilidad e historial necesario. Consulta las decisiones técnicas para responsabilidades y precisión monetaria.
- Para comportamiento interactivo nuevo o modificado en Next/React, agrega pruebas de componentes y comportamiento con Vitest y React Testing Library conforme a DT-012. No sustituyas esa cobertura con snapshots ni con pruebas integrales por navegador.
- Registra problemas ajenos al alcance sin resolverlos dentro del mismo cambio.

## Al terminar

- Verifica los criterios de aceptación y las regresiones relevantes. Las reglas de negocio requieren pruebas de comportamiento esperado y errores, no de detalles internos.
- Actualiza la evidencia real y las referencias a implementación en `verificacion.md`; conserva en `spec.md` los criterios y el único estado vigente. Marca tareas completadas sólo tras comprobar su «Hecho cuando». No declares comprobaciones que no se ejecutaron.
- Cuando implementación y comprobaciones técnicas estén completas, marca la spec como QA. No realices ni exijas una comprobación integral de interfaz por navegador: la validación visual corresponde a una persona.
- Marca la spec como Implementada únicamente cuando la aprobación de QA humana esté registrada conforme al flujo.
- Regenera el índice con `python3 scripts/spec_index.py --write` si cambia un estado y ejecuta `python3 scripts/spec_index.py --check` al cerrar el trabajo documental.
