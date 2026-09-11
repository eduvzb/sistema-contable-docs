# Prompt maestro para trabajar una spec

Usa este prompt para preparar, implementar, verificar y actualizar una spec del sistema contable. Sustituye los valores entre corchetes; si omites un dato opcional, el agente debe obtenerlo del repositorio y avanzar con el alcance vigente.

## Variables

- `SPEC_ID`: identificador, por ejemplo `SPEC-004`.
- `OBJETIVO`: resultado adicional solicitado; opcional si se trabajará todo lo pendiente de la spec.
- `COMPONENTES`: `documentación`, `backend`, `frontend` o `todos`.
- `RESTRICCIONES`: límites explícitos, por ejemplo «solo documental» o «no crear commits».

## Prompt

```text
Trabaja [SPEC_ID] del sistema contable hasta dejar resuelto todo lo autorizado y verificable en esta sesión.

Objetivo adicional: [OBJETIVO o "ninguno; usa el alcance vigente de la spec"]
Componentes autorizados: [COMPONENTES o "todos"]
Restricciones: [RESTRICCIONES o "ninguna adicional"]

Los repositorios son independientes:
- `sistema-contable`: fuente canónica de specs y documentación compartida.
- `sistema-contable-backend`: implementación backend.
- `sistema-contable-frontend`: implementación frontend.

Sigue estas reglas durante todo el trabajo:

1. Antes de cambiar archivos, lee el `AGENTS.md` aplicable de cada repositorio que vayas a tocar y revisa su estado Git. Conserva cambios locales existentes y no mezcles trabajo ajeno.
2. Localiza [SPEC_ID] en `specs/README.md`. Lee siempre completamente la spec objetivo, su sección `Contexto de ejecución`, `docs/constitution.md`, `docs/decisiones.md`, `docs/flujo-spec.md` y `docs/fuentes.md`. Lee `AGENTS.md` completo en cada repositorio que vayas a tocar. Consulta `docs/estado-implementacion.md` como relevo operativo, sin tratarlo como sustituto de la spec.
   - En `Borrador`, lee además las fuentes de dominio necesarias para resolver el alcance, las decisiones y los bloqueantes.
   - En `Lista` o `Actualización pendiente`, lee sólo las dependencias y contratos directamente relacionados con los criterios que se van a implementar. No recargues automáticamente toda Planeación ni vuelvas a procesar fuentes ya consolidadas en la spec.
   - En `QA`, concentra la revisión en la evidencia de la spec y en los recorridos visuales pendientes; no reabras Planeación salvo que exista una observación que cambie el comportamiento.
3. Inspecciona la implementación y las pruebas reales antes de proponer contratos, comandos o archivos. Identifica qué criterios ya tienen evidencia, cuáles están pendientes y si existe una divergencia entre documentación, backend y frontend.
4. No inventes reglas contables, fiscales, de autorización ni de negocio. Si una decisión sustantiva no está respaldada y cambia el resultado esperado, registra el bloqueante y pregunta sólo por esa decisión. Las instrucciones explícitas del usuario son decisiones y deben registrarse en la fuente correspondiente.
5. Reutiliza la spec para corregir incumplimientos. No crees otra spec para un bug o una mejora perteneciente a la misma funcionalidad. Si el cambio modifica comportamiento esperado, actualiza primero la spec y luego la implementación.
6. Realiza el cambio coherente más pequeño que satisfaga los criterios autorizados. Mantén las responsabilidades vigentes: backend para negocio, autorización, validación autoritativa, persistencia y contratos; frontend para presentación, interacción y estado de interfaz.
7. Preserva aislamiento por empresa, contexto contable explícito, integridad transaccional, trazabilidad, historial requerido y precisión decimal. No amplíes el alcance a funcionalidades posteriores.
8. No inventes revisiones Git, resultados de pruebas ni evidencia. No actualices `SPEC_REVISION` con un hash inexistente. No crees commits, ramas, PR ni despliegues salvo solicitud explícita.

Actúa según el estado actual de la spec:

- `Borrador`: aclara y documenta los bloqueantes. Prepara alcance, criterios, contratos, riesgos y verificación. No implementes el comportamiento bloqueado. Cuando quede completamente preparado, cambia a `Lista` si es la primera implementación o a `Actualización pendiente` si modifica una funcionalidad existente.
- `Lista`: implementa los criterios pendientes que estén preparados y verifica las regresiones pertinentes. Cuando todos los componentes y comprobaciones técnicas estén completos, cambia a `QA`.
- `Actualización pendiente`: conserva la evidencia histórica y trabaja específicamente los criterios nuevos o modificados, además de sus regresiones. Al completar implementación y comprobaciones técnicas, cambia a `QA`.
- `QA`: no suplantes al responsable humano ni declares aprobación visual. Si no hay observaciones humanas, conserva el estado y entrega los recorridos que QA debe validar. Si el usuario proporciona una aprobación humana, regístrala y cambia a `Implementada`; si proporciona observaciones, reclasifica según `docs/flujo-spec.md` y trabaja únicamente lo autorizado.
- `Implementada`: si sólo se pide inspección, no cambies su estado. Si se solicita comportamiento nuevo, actualiza primero la misma spec y reclasifícala como `Borrador` o `Actualización pendiente`, según esté o no preparada la modificación.

Regla de reutilización de contexto:

- La spec es la fuente funcional de ejecución cuando está en `Lista` o `Actualización pendiente`: sus criterios, decisiones, contratos, pendientes no bloqueantes y Contexto de ejecución forman el paquete que se implementa.
- Reabre una fuente de Planeación sólo si el Contexto de ejecución identifica un pendiente o supuesto relevante, la spec contradice la fuente, la fuente cambió después de la preparación, cambió una dependencia o su contrato, o el usuario solicita cambiar el comportamiento.
- Si una fuente se reabre y modifica lo esperado, actualiza primero la spec y registra la decisión; no implementes una interpretación nueva sólo porque encontraste un párrafo antiguo o ambiguo.

Ejecuta el trabajo en este orden:

A. Diagnóstico
- Resume el propósito de [SPEC_ID], su estado, dependencias y criterios pendientes.
- Usa el `Contexto de ejecución` como límite inicial del diagnóstico. No repitas el análisis histórico ya consolidado; registra únicamente contradicciones, cambios o datos faltantes que afecten la ejecución.
- Revisa el código y pruebas relacionados en los componentes autorizados.
- Separa incumplimientos de la spec, cambios de comportamiento y problemas fuera de alcance.

B. Preparación SDD
- Confirma que cada cambio tenga un criterio observable con ID estable.
- Define entradas, resultados, autorización, errores y efectos de integridad necesarios.
- Registra decisiones locales en la spec y decisiones compartidas en `docs/decisiones.md`.
- Actualiza el índice o el estado de continuidad cuando cambie la clasificación.

C. Implementación
- Implementa sólo el alcance preparado en backend y/o frontend autorizados.
- Coordina cualquier contrato compartido entre ambos consumidores.
- Mantén compatibilidad con el comportamiento no modificado y evita refactors ajenos.

D. Verificación
- Comprueba cada criterio trabajado con pruebas de comportamiento esperado, errores relevantes y regresiones.
- Incluye autorización, aislamiento, atomicidad y precisión cuando apliquen.
- Ejecuta las comprobaciones convencionales de cada repositorio afectado. Si una comprobación no puede ejecutarse, explica exactamente por qué y déjala pendiente; no la sustituyas por una afirmación.
- No realices ni uses una comprobación integral de interfaz por navegador como criterio de cierre. Prepara recorridos visuales claros y entrégalos a QA humana.
- Revisa el diff final y confirma que no contiene cambios accidentales.

E. Cierre documental
- Actualiza la sección `Verificación` de [SPEC_ID] con criterio → prueba o comprobación → resultado real → referencia de implementación disponible.
- Conserva por separado la evidencia histórica y la generada para esta actualización.
- Actualiza `Cambios`, pendientes, `specs/README.md` y `docs/estado-implementacion.md` cuando corresponda.
- Reclasifica la spec aplicando literalmente `docs/flujo-spec.md`: el cierre técnico llega a `QA`; sólo una aprobación humana registrada permite `Implementada`.

No te detengas en un plan si puedes continuar de forma segura dentro del alcance. Al terminar, responde con:

1. Resultado alcanzado y estado final de la spec.
2. Cambios realizados por repositorio.
3. Criterios cubiertos y comprobaciones ejecutadas con sus resultados.
4. Recorridos entregados a QA humana, o aprobación/observaciones recibidas.
5. Comprobaciones técnicas no ejecutadas y motivo.
6. Pendientes o problemas fuera de alcance.
7. Enlaces a los archivos principales modificados.
```

## Ejemplo mínimo

```text
Trabaja SPEC-004 usando el prompt maestro de `docs/prompt-master-spec.md`.
Objetivo adicional: corregir y verificar CA-004-09/10.
Componentes autorizados: todos.
Restricciones: no crear commits ni desplegar.
```
