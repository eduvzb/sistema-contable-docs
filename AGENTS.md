# Instrucciones para agentes

Este repositorio contiene documentación y specs compartidas del sistema contable. No contiene todavía la implementación de backend ni frontend.

## Antes de cambiar comportamiento

1. Localiza la funcionalidad en el [índice de specs](specs/README.md).
2. Respeta la [constitución](docs/constitution.md) y las [decisiones vigentes](docs/decisiones.md).
3. Lee la spec y sus fuentes concretas; el [mapa de fuentes](docs/fuentes.md) indica su autoridad. No es necesario leer toda Planeación.
4. Sigue el [flujo SDD](docs/flujo-spec.md): aclara los bloqueantes de esa spec y registra el comportamiento esperado antes de implementar. No inventes reglas de negocio.

## Durante el trabajo

- Realiza el cambio coherente más pequeño que cumpla la spec, usando las convenciones del framework.
- Reutiliza la spec al corregir un incumplimiento; actualízala antes de cambiar comportamiento. Documentación y refactors sin efecto observable no requieren otra spec.
- Las instrucciones explícitas del usuario cuentan como decisiones: regístralas donde correspondan, sin pedir confirmaciones repetidas.
- Preserva integridad, aislamiento, trazabilidad e historial necesario. Consulta las decisiones técnicas para responsabilidades y precisión monetaria.
- Registra problemas ajenos al alcance sin resolverlos dentro del mismo cambio.

## Al terminar

- Verifica los criterios de aceptación y las regresiones relevantes. Las reglas de negocio requieren pruebas de comportamiento esperado y errores, no de detalles internos.
- Actualiza en la spec la evidencia real, las referencias a implementación y los pendientes. No declares comprobaciones que no se ejecutaron.
- Marca la spec como Implementada únicamente cuando cumpla la definición de terminado del flujo.
