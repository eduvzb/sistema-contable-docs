# Flujo de Spec Driven Development

**Seleccionar spec → aclarar lo necesario → preparar implementación → implementar → verificar y actualizar.**

La spec es el acuerdo verificable de una funcionalidad y se mantiene con sus cambios. No es una descripción retrospectiva del código.

## Política de contexto por fase

La carga de contexto se adapta al estado de la spec. El objetivo es entender el dominio durante la ideación y la preparación, y reutilizar esa decisión consolidada durante la ejecución sin reconstruirla en cada sesión.

- **Ideación, análisis y `Borrador`:** consultar el contexto amplio necesario: alcance, reglas, escenarios, preguntas abiertas, glosario y análisis aplicables. Registrar en la spec las decisiones, supuestos, bloqueantes y criterios que resulten de esa revisión.
- **`Lista` y `Actualización pendiente`:** la spec completa es el paquete funcional principal. Leer las instrucciones transversales obligatorias, la spec, sus dependencias y contratos directamente relacionados, y el código/pruebas reales. No recargar automáticamente toda Planeación ni repetir el análisis ya consolidado.
- **`QA`:** usar la spec, su evidencia de verificación y sus recorridos pendientes como paquete de validación. No volver a planear ni implementar; la revisión visual corresponde a la persona responsable.

En cualquier fase siguen siendo obligatorios `AGENTS.md` de los repositorios afectados, `docs/constitution.md`, `docs/decisiones.md`, este flujo y `docs/fuentes.md`. Las fuentes de dominio citadas por una spec se consultan cuando la fase o un disparador de revalidación lo exige; no se cargan por rutina si el comportamiento ya está consolidado en la spec.

## 0. Preflight Git por tarea

Cada tarea se trabaja en una rama aislada y se aplica sólo en los repositorios que realmente tendrán cambios. Antes de tomarla:

1. Identifica si la tarea modifica el repositorio de specs, backend, frontend o una combinación de ellos.
2. En cada repositorio afectado, exige un árbol de trabajo limpio. Los cambios locales previos bloquean el inicio; no se mezclan, guardan ni absorben dentro de la tarea.
3. Verifica que exista la rama base `main`, que esté disponible el remoto de publicación `origin` y que no exista `codex/SPEC-NNN` ni localmente ni en el remoto.
4. Crea `codex/SPEC-NNN` desde `main` en cada repositorio afectado, usando exactamente el mismo nombre y el ID de la spec.

Si falla cualquiera de estas comprobaciones, no modifiques el repositorio ni crees una rama parcial: reporta el repositorio, la comprobación fallida y la acción necesaria. No reutilices una rama existente ni sustituyas el remoto ausente por un commit local.

## 1. Seleccionar y aclarar

Busca la spec en el [índice](../specs/README.md). Si la funcionalidad es nueva, usa la [plantilla](../specs/_plantilla.md), asigna el siguiente ID libre y agrégala al índice. No crees otra spec para corregir un incumplimiento de una existente.

Lee sus fuentes concretas según el [mapa](fuentes.md) cuando prepares o cambies el comportamiento. Define propósito, alcance, comportamiento y criterios observables, incluyendo errores relevantes. Conserva las reglas por referencia; los criterios expresan cómo comprobarlas, no crean una segunda regla independiente.

Distingue **bloqueantes de preparación**, **supuestos existentes para validar durante el MVP** y **asuntos posteriores**. Una duda bloquea solo el comportamiento afectado; se puede avanzar con otras specs. No inventes reglas para cerrar huecos. Si es necesario reducir una spec para hacerla implementable, documenta el alcance y conserva el trabajo retirado en el índice.

Una instrucción explícita del usuario cuenta como decisión, sin confirmaciones repetidas. Registra decisiones locales en la spec y compartidas en [decisiones](decisiones.md). Para cambiar una regla del dominio, actualiza también la fuente responsable y las specs afectadas, dejando motivo y referencia a lo reemplazado.

## 2. Preparar

En la misma spec, describe el cambio técnico mínimo, dependencias, riesgos de integridad y verificación. Concreta únicamente los contratos que la funcionalidad necesita: operaciones, entradas, resultados, autorización y errores observables. No son obligatorios un OpenAPI separado, un ADR ni un archivo de tareas.

Los detalles técnicos todavía desconocidos deben resolverse antes de marcar Lista o Actualización pendiente, consultando los repositorios reales al existir. El stack y la separación de responsabilidades ya están en decisiones; no se vuelven a decidir por spec.

| Estado | Condición |
|---|---|
| Borrador | Comportamiento en preparación; puede contener decisiones bloqueantes. |
| Lista | Alcance y criterios verificables; plan y contratos necesarios definidos; dependencias compatibles; ningún bloqueante para implementar ese alcance. Los supuestos existentes siguen etiquetados. |
| Actualización pendiente | La funcionalidad ya tenía implementación o evidencia y recibió un cambio de comportamiento aprobado y preparado. El comportamiento anterior continúa trazado, pero los criterios nuevos o modificados todavía no cuentan con implementación y comprobaciones técnicas completas. |
| QA | Implementación y comprobaciones técnicas completas. Sólo resta la validación visual humana; no hay contratos, código, pruebas automatizadas ni regresiones técnicas pendientes dentro del alcance. |
| Implementada | QA humana aprobada y registrada; todos los criterios del alcance están satisfechos. |

La primera colección se entrega en Borrador. Redactar una spec no equivale a aprobar cada detalle ni a implementar el producto. Una spec Lista puede estar en su primera implementación. Un cambio todavía no preparado lleva la spec a Borrador; cuando el cambio de una funcionalidad existente ya tiene alcance, criterios y plan suficientes, se clasifica como Actualización pendiente para hacer visible el retrabajo sin borrar la evidencia anterior.

Una spec en `Lista` o `Actualización pendiente` debe incluir un **Contexto de ejecución** que identifique el alcance autoritativo, los criterios que se deben trabajar, las dependencias y los disparadores que obligan a reabrir una fuente. Ese bloque no duplica Planeación: funciona como índice de relevo y declara qué conocimiento ya fue consolidado en la spec.

Al completar la implementación y las comprobaciones técnicas de una spec Lista o en Actualización pendiente, pasa a QA. Una dependencia en Actualización pendiente conserva su contrato previo vigente; los consumidores afectados por los criterios nuevos deben coordinarse con esa actualización antes de declarar su propio cierre técnico. Una dependencia en QA ya es consumible técnicamente y no bloquea implementación; su aprobación visual permanece a cargo de la persona responsable.

QA es responsabilidad de una persona. El agente no realiza ni usa una comprobación integral de interfaz por navegador como requisito de cierre. La persona valida visualmente los recorridos preparados y registra aprobación u observaciones. Una aprobación mueve la spec a Implementada; una observación que contradice criterios ya definidos la devuelve a Actualización pendiente, y una observación que exige decidir comportamiento nuevo la devuelve a Borrador hasta aclararlo.

## 3. Implementar

Backend y frontend usan el mismo ID y revisión Git de este repositorio. Referencian esa revisión desde su tarea o PR; no copian specs para mantener variantes. Antes del primer commit de documentación puede usarse el archivo local para preparar trabajo, pero no inventar un hash.

La rama de trabajo es `codex/SPEC-NNN` en cada repositorio afectado. Si la tarea modifica la spec y consumidores, la misma rama se crea en los tres repositorios antes de editar; si sólo modifica uno, sólo se crea allí. Los cambios de cada repositorio permanecen separados y no se atribuyen a repositorios sin modificaciones.

Define cada contrato compartido en la spec responsable y enlázalo desde las consumidoras. Coordina cambios de contrato actualizando la spec y ambos consumidores afectados. La spec guarda enlaces a las revisiones/PR de implementación cuando existan.

Implementa solo el alcance preparado. Si el código contradice la spec, corrígelo; si debe cambiar lo esperado, cambia primero la spec y sus fuentes pertinentes. Documentación y refactors sin efecto observable no requieren una spec nueva, aunque sí la comprobación apropiada al cambio.

Durante la implementación, reabre una fuente de Planeación sólo si el Contexto de ejecución identifica un pendiente o supuesto que afecta el comportamiento, si aparece una contradicción, si la fuente o el contrato de una dependencia cambió después de preparar la spec, o si el usuario solicita modificar la regla. Una fuente reabierta puede cambiar el resultado esperado únicamente después de actualizar la spec y registrar la decisión correspondiente.

## 4. Verificar y mantener

Comprueba cada criterio de aceptación con evidencia suficiente. Para reglas de negocio, incluye pruebas del caso esperado, errores relevantes y regresiones; verifica autorización e integridad cuando correspondan. Una prueba de detalle interno no sustituye un criterio funcional.

En la spec registra criterio → prueba o comprobación, resultado, revisión y referencia a la evidencia. Se permite agrupar criterios cubiertos por la misma prueba. No inventes comandos de pruebas antes de conocer el repositorio ni resultados antes de ejecutarlos.

**Cierre técnico del agente:** satisface el alcance preparado; las comprobaciones automatizadas y técnicas pasan; se preservan autorización e integridad aplicables; no se introducen reglas o funcionalidades ajenas; documentación, contratos y referencias están actualizados. Si falta backend, frontend u otra parte incluida, la spec no puede pasar a QA.

**Terminado:** además del cierre técnico, la QA visual humana está aprobada y registrada. Sólo entonces la spec pasa a Implementada.

El cierre Git forma parte de la entrega técnica:

- Cada repositorio afectado termina con un único commit final que contiene sólo los cambios de la tarea.
- El mensaje sigue el formato `SPEC-NNN: verbo en imperativo`, por ejemplo `SPEC-004: evita importar CFDI duplicados`.
- Publica la rama con `git push -u origin codex/SPEC-NNN`.
- En la spec registra, por cada repositorio, su rama, hash del commit y remoto publicado.

La tarea no está cerrada hasta que todos los repositorios afectados tienen su commit y rama publicados. Un cambio previo detectado, una colisión de rama, un remoto ausente o un fallo de commit/push bloquea el cierre y debe reportarse con el repositorio y la causa. Este flujo no crea PR ni realiza merge automáticamente.

Para un cambio posterior, actualiza la misma spec sin renumerar criterios existentes; agrega nuevos IDs y registra los criterios retirados y su motivo. Conserva evidencia anterior con su revisión, distinguiéndola de lo todavía pendiente de verificar, y usa Actualización pendiente cuando el cambio ya esté preparado pero aún no tenga cierre técnico. Al alcanzarlo, clasifica la spec como QA y entrega al responsable humano los recorridos visuales que debe validar.
