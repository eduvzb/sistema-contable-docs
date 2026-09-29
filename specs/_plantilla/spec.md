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

Seguridad, aislamiento, precisión, accesibilidad o rendimiento sólo cuando apliquen; enlazar el CA o contrato responsable. No inventar umbrales.

## Casos límite

Vacíos, duplicados, datos inválidos, concurrencia y otros límites aplicables, enlazados a criterios; no duplicar sus resultados.

## Fuera de alcance

Exclusiones explícitas de esta entrega.

## Preguntas abiertas

- **Bloqueante:** decisión sin la cual no puede definirse o comprobarse un criterio. Mantener la spec en Borrador.
- **Para una ampliación futura:** cuestión que no cambia los criterios de esta entrega. No registrar aquí decisiones ya reflejadas por el código o los CA.

## Criterios de finalización

- Los CA de esta entrega tienen implementación y comprobación técnica real en [verificacion.md](verificacion.md) antes de pasar a QA.
- Sólo una aprobación humana de QA registrada permite pasar a Implementada.

## Fuentes

Enlaces concretos a fuentes de dominio pertinentes. Contrastar siempre las afirmaciones sobre comportamiento implementado con código y pruebas.
