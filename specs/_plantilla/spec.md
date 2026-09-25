# SPEC-NNN — Nombre de la funcionalidad

- **Estado:** Borrador
- **Actualizado:** AAAA-MM-DD
- **Criterios de esta entrega:** CA-NNN-01; indicar criterios nuevos o revisados, o «Sin tareas técnicas abiertas; resta QA humana».
- **Usuario:** actor beneficiado
- **Dependencias:** IDs de specs enlazadas o ninguna

## Contexto y objetivo

Problema, resultado esperado y alcance incluido. Definir el comportamiento, no su implementación.

## Historias de usuario

- H-NNN-01: Como <actor> quiero <acción> para <beneficio>.

## Requisitos funcionales y criterios de aceptación

Conservar los IDs `CA-NNN-XX` al cambiar un criterio. Redactar cada criterio nuevo o revisado como respuesta observable a un evento, condición o estado; incluir errores relevantes.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-NNN-01 | CUANDO ocurre un evento observable. | EL SISTEMA produce un resultado verificable. |
| CA-NNN-02 | SI se presenta una condición no deseada. | EL SISTEMA informa el error y conserva la integridad aplicable. |

## Requisitos no funcionales aplicables

Seguridad, aislamiento, precisión, accesibilidad o rendimiento sólo cuando apliquen; enlazar la decisión o el CA responsable. No inventar umbrales.

## Casos límite

Vacíos, duplicados, datos inválidos, concurrencia y otros límites aplicables, enlazados a criterios; no duplicar sus resultados.

## Fuera de alcance

Exclusiones explícitas de esta entrega.

## Decisiones, supuestos y dudas

- **Decidido:** decisión funcional local y fuente.
- **Supuesto para validar:** comportamiento provisional con fuente.
- **Duda bloqueante:** sólo si impide definir o verificar un criterio. Una spec con dudas bloqueantes permanece en Borrador.
- **Posterior:** asunto excluido que no bloquea esta entrega.

## Criterios de finalización

- Los CA de esta entrega tienen implementación y comprobación técnica real en [verificacion.md](verificacion.md) antes de pasar a QA.
- Sólo una aprobación humana de QA registrada permite pasar a Implementada.

## Fuentes

Enlaces concretos al alcance, reglas BR, escenarios AC, preguntas OQ y decisiones pertinentes. Conservar su grado de certeza conforme al [mapa de fuentes](../../docs/fuentes.md).
