# SPEC-NNN — Nombre de la funcionalidad

**Estado:** Borrador  
**Usuario:** actor beneficiado  
**Dependencias:** IDs enlazados o ninguna

## Propósito y alcance

Problema, resultado que necesita el usuario, qué incluye y qué queda fuera.

## Fuentes

Enlaces a secciones concretas de alcance, BR, AC, OQ y decisiones aplicables. Conservar el estado de certeza de las fuentes. Omitir categorías que no apliquen.

## Contexto de ejecución

Esta spec es el paquete funcional principal para implementar su alcance cuando está en `Lista` o `Actualización pendiente`.

- **Alcance autoritativo para ejecución:** esta spec, sus criterios de aceptación, decisiones, contratos y pendientes no bloqueantes.
- **Criterios a trabajar en esta ejecución:** IDs de criterios pendientes o modificados; no reabrir criterios ya satisfechos salvo regresión.
- **Dependencias y contratos a consultar:** specs y contratos directamente relacionados, con sus estados actuales.
- **Decisiones y supuestos relevantes:** resumir sólo los que puedan cambiar la implementación o la verificación.
- **Fuentes ya consolidadas:** las fuentes citadas en `Fuentes` no se recargan normalmente durante implementación si no cambiaron y no contienen pendientes que afecten este alcance.
- **Reabrir una fuente cuando:** exista una decisión bloqueante, contradicción con la spec, cambio posterior de la fuente o de una dependencia, o una solicitud explícita de cambiar comportamiento.

En `Borrador`, completar este bloque al preparar la spec. En `QA`, convertirlo en un paquete de validación con la evidencia y los recorridos humanos pendientes.

## Comportamiento y criterios de aceptación

Describir el flujo mínimo y resultados observables; no duplicar reglas compartidas.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-NNN-01 | Contexto y acción | Resultado comprobable. |

Incluir errores relevantes y regresiones; agregar autorización/integridad donde corresponda.

## Pendientes y decisiones

- **Antes de Lista:** decisiones que impiden implementar o verificar el alcance.
- **Supuestos para validar durante el MVP:** comportamiento provisional ya sustentado, con su fuente.
- **Posterior:** asuntos excluidos que no bloquean esta spec.

## Plan técnico y contratos

Cambio mínimo por componente, contratos que define/consume y comprobaciones previstas. Resolver operaciones, datos, autorización y errores necesarios antes de Lista. No inventar esquemas para completar el documento.

## Verificación

**Evidencia de producto:** pendiente; no ejecutada.

**Entrega Git:**

| Repositorio | Rama | Commit | Remoto |
|---|---|---|---|
| Pendiente | `codex/SPEC-NNN` | Pendiente | `origin` |

Al verificar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencia a implementación. No rellenar resultados por anticipado.

**QA humana:** no iniciada. Cuando implementación y comprobaciones técnicas estén completas, cambiar el estado a QA y describir aquí los recorridos visuales entregados a la persona responsable. Registrar su aprobación u observaciones; no sustituirla con una comprobación integral por navegador realizada por el agente.

## Cambios

- Fecha — motivo, decisión/fuente y criterios afectados. Git conserva las revisiones anteriores.
