# Flujo de Spec Driven Development

**Seleccionar spec → aclarar lo necesario → preparar implementación → implementar → verificar y actualizar.**

`spec.md` es el acuerdo verificable de una funcionalidad y la única autoridad de su estado. No es una descripción retrospectiva del código.

Cada funcionalidad vive en `specs/NNN-nombre/`: `spec.md` define qué y por qué; `plan.md` define contratos y enfoque técnico; `tasks-backend.md` y `tasks-frontend.md` contienen únicamente trabajo técnico pendiente; `verificacion.md` conserva resultados reales, PR y QA por entrega. No se reconstruyen tareas completadas a partir del historial. La tabla del índice se genera desde `spec.md` con `python3 scripts/spec_index.py --write` y se comprueba con `--check`; ningún resumen manual cambia el estado de una spec.

## Política de contexto por fase

La carga de contexto se adapta al estado de la spec. El objetivo es entender el dominio durante la ideación y la preparación, y reutilizar esa decisión consolidada durante la ejecución sin reconstruirla en cada sesión.

- **Ideación, análisis y `Borrador`:** consultar el contexto amplio necesario: alcance, reglas, escenarios, preguntas abiertas, glosario y análisis aplicables. Registrar en la spec las decisiones, supuestos, bloqueantes y criterios que resulten de esa revisión.
- **`Lista` y `Actualización pendiente`:** leer `spec.md` primero; después el `plan.md`, las tareas del repositorio afectado, los contratos de dependencias y el código/pruebas reales. Abrir `verificacion.md` sólo para distinguir evidencia previa de criterios pendientes. No recargar automáticamente toda Planeación ni repetir el análisis ya consolidado.
- **`QA`:** usar `spec.md` y `verificacion.md` como paquete de validación. No volver a planear ni implementar; la revisión visual corresponde a la persona responsable.

En cualquier fase siguen siendo obligatorios `AGENTS.md` de los repositorios afectados, `docs/constitution.md`, `docs/decisiones.md`, este flujo y `docs/fuentes.md`. Las fuentes de dominio citadas por una spec se consultan cuando la fase o un disparador de revalidación lo exige; no se cargan por rutina si el comportamiento ya está consolidado en la spec.

## 0. Preflight Git por tarea

Cada tarea de código se trabaja en ramas aisladas únicamente en los repositorios de implementación que realmente tendrán cambios. El repositorio de specs es la fuente documental compartida: puede actualizarse en su rama de trabajo actual para conservar la evidencia, pero esta tarea no crea allí una rama `codex/...`, no exige commit ni publica cambios.

Antes de tomarla:

1. Identifica si la tarea modifica documentación, backend, frontend o una combinación de ellos.
2. En backend y frontend, exige un árbol de trabajo limpio. Los cambios locales previos bloquean el inicio; no se mezclan, guardan ni absorben dentro de la tarea.
3. En el repositorio de specs, revisa el estado y protege los cambios locales existentes; no crees una rama ni trates la documentación como un consumidor de código.
4. Define el tipo predominante (`feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `build` o `ci`) y un `slug` descriptivo no vacío en kebab-case (`[a-z0-9]+(?:-[a-z0-9]+)*`). Forma el candidato `codex/<tipo>/SPEC-NNN/<slug>`.
5. Para cada repositorio de implementación afectado, verifica que exista la rama base `main`, que esté disponible el remoto de publicación `origin`, que `gh` esté instalado y autenticado con acceso al repositorio, y consulta si el candidato existe localmente o en remoto. Si está ocupado en cualquiera de los repositorios afectados, incrementa el sufijo común (`-2`, `-3`, etc.) hasta elegir una única `RAMA_TRABAJO` disponible en todos ellos.
6. Crea `RAMA_TRABAJO` desde `main` sólo en los repositorios de implementación afectados, usando exactamente el mismo nombre en todos ellos.

Si falla cualquiera de estas comprobaciones de un repositorio de implementación, no modifiques ese repositorio ni crees una rama parcial: reporta el repositorio, la comprobación fallida y la acción necesaria. No reutilices una rama ocupada ni sustituyas el remoto ausente por un commit local. Un cambio local en el repositorio de specs sólo impide editar los archivos que se solapen; no obliga a crear una rama ni a publicarlo. Si una carrera concurrente hace que el `push` detecte una colisión después de elegir `RAMA_TRABAJO`, aplica el fallo de publicación: no elijas otro sufijo ni reintentes automáticamente.

## 1. Seleccionar y aclarar

Busca la spec en el [índice](../specs/README.md). Si la funcionalidad es nueva, usa las [cinco plantillas](../specs/_plantilla/spec.md), asigna el siguiente ID libre, crea su carpeta y regenera el índice. No crees otra spec para corregir un incumplimiento de una existente.

Lee sus fuentes concretas según el [mapa](fuentes.md) cuando prepares o cambies el comportamiento. Define propósito, alcance, comportamiento y criterios observables, incluyendo errores relevantes. Conserva las reglas por referencia; los criterios expresan cómo comprobarlas, no crean una segunda regla independiente.

Distingue **bloqueantes de preparación**, **supuestos existentes para validar durante el MVP** y **asuntos posteriores**. Una duda bloquea solo el comportamiento afectado; se puede avanzar con otras specs. No inventes reglas para cerrar huecos. Si es necesario reducir una spec para hacerla implementable, documenta el alcance y conserva el trabajo retirado en el índice.

Una instrucción explícita del usuario cuenta como decisión, sin confirmaciones repetidas. Registra decisiones locales en la spec y compartidas en [decisiones](decisiones.md). Para cambiar una regla del dominio, actualiza también la fuente responsable y las specs afectadas, dejando motivo y referencia a lo reemplazado.

## 2. Preparar

En `spec.md`, define objetivo, historias, criterios estables en lenguaje observable, casos límite, exclusiones y dudas. Conserva los IDs `CA-NNN-XX`; redacta criterios nuevos o revisados como «CUANDO/SI/MIENTRAS… EL SISTEMA…» sin cambiar su sentido. En `plan.md`, describe el cambio técnico mínimo, dependencias, riesgos de integridad y contratos necesarios: operaciones, entradas, resultados, autorización y errores observables. En las dos listas de tareas, registra sólo trabajo pendiente por repositorio, cada tarea con CA, dependencia y «Hecho cuando». No son obligatorios un OpenAPI separado ni un ADR.

Cuando el alcance agregue o modifique comportamiento interactivo en Next/React, prepara la cobertura de componentes y comportamiento exigida por DT-012. Identifica qué efectos observables se comprobarán con Vitest/React Testing Library y qué propiedades de layout real quedarán para QA visual humana. No uses snapshots ni una prueba integral por navegador como sustituto de esa cobertura.

Los detalles técnicos todavía desconocidos deben resolverse antes de marcar Lista o Actualización pendiente, consultando los repositorios reales al existir. El stack y la separación de responsabilidades ya están en decisiones; no se vuelven a decidir por spec.

| Estado | Condición |
|---|---|
| Borrador | Comportamiento en preparación; puede contener decisiones bloqueantes. |
| Lista | Alcance y criterios verificables; plan y contratos necesarios definidos; dependencias compatibles; ningún bloqueante para implementar ese alcance. Los supuestos existentes siguen etiquetados. |
| Actualización pendiente | La funcionalidad ya tenía implementación o evidencia y recibió un cambio de comportamiento aprobado y preparado. El comportamiento anterior continúa trazado, pero los criterios nuevos o modificados todavía no cuentan con implementación y comprobaciones técnicas completas. |
| QA | Implementación y comprobaciones técnicas completas. Sólo resta la validación visual humana; no hay contratos, código, pruebas automatizadas ni regresiones técnicas pendientes dentro del alcance. |
| Implementada | QA humana aprobada y registrada; todos los criterios del alcance están satisfechos. |

La primera colección se entrega en Borrador. Redactar una spec no equivale a aprobar cada detalle ni a implementar el producto. Una spec Lista puede estar en su primera implementación. Un cambio todavía no preparado lleva la spec a Borrador; cuando el cambio de una funcionalidad existente ya tiene alcance, criterios y plan suficientes, se clasifica como Actualización pendiente para hacer visible el retrabajo sin borrar la evidencia anterior.

Una spec en `Lista` o `Actualización pendiente` debe declarar en el encabezado de `spec.md` los criterios de esta entrega y sus dependencias. `plan.md` identifica contratos consumidos y disparadores para reabrir una fuente. Ninguno duplica Planeación: ambos indican qué conocimiento ya fue consolidado.

Al completar la implementación y las comprobaciones técnicas de una spec Lista o en Actualización pendiente, prepara la entrega a QA. Una dependencia en Actualización pendiente conserva su contrato previo vigente; los consumidores afectados por los criterios nuevos deben coordinarse con esa actualización antes de declarar su propio cierre técnico. Una dependencia en QA ya es consumible técnicamente y no bloquea implementación; su aprobación visual permanece a cargo de la persona responsable.

QA es responsabilidad de una persona. El agente no realiza ni usa una comprobación integral de interfaz por navegador como requisito de cierre. La persona valida visualmente los recorridos preparados y registra aprobación u observaciones. Una aprobación mueve la spec a Implementada; una observación que contradice criterios ya definidos la devuelve a Actualización pendiente, y una observación que exige decidir comportamiento nuevo la devuelve a Borrador hasta aclararlo.

## 3. Implementar

Backend y frontend usan el mismo ID y revisión Git de este repositorio. Referencian esa revisión desde su tarea o PR; no copian specs para mantener variantes. Antes del primer commit de documentación puede usarse el archivo local para preparar trabajo, pero no inventar un hash.

La rama de trabajo `codex/<tipo>/SPEC-NNN/<slug>` existe sólo en cada repositorio de implementación afectado. `RAMA_TRABAJO` identifica una tarea concreta y permite varias tareas paralelas de la misma spec; el repositorio de specs conserva su rama actual y sus cambios documentales quedan separados del ciclo de publicación de backend/frontend. Los cambios de cada repositorio permanecen separados y no se atribuyen a repositorios sin modificaciones.

Define cada contrato compartido en el `plan.md` de la funcionalidad responsable y enlázalo desde los planes consumidores. Coordina cambios de contrato actualizando el plan, los CA de `spec.md` cuando cambie el comportamiento y ambos consumidores afectados. `verificacion.md` guarda enlaces a las revisiones/PR de implementación cuando existan.

Implementa solo el alcance preparado. Si el código contradice la spec, corrígelo; si debe cambiar lo esperado, cambia primero la spec y sus fuentes pertinentes. Documentación y refactors sin efecto observable no requieren una spec nueva, aunque sí la comprobación apropiada al cambio.

Durante la implementación, reabre una fuente de Planeación sólo si `spec.md` o `plan.md` identifica un pendiente o supuesto que afecta el comportamiento, si aparece una contradicción, si la fuente o el contrato de una dependencia cambió después de preparar la spec, o si el usuario solicita modificar la regla. Una fuente reabierta puede cambiar el resultado esperado únicamente después de actualizar `spec.md` y registrar la decisión correspondiente.

## 4. Verificar y mantener

Comprueba cada criterio de aceptación con evidencia suficiente. Para reglas de negocio, incluye pruebas del caso esperado, errores relevantes y regresiones; verifica autorización e integridad cuando correspondan. Una prueba de detalle interno no sustituye un criterio funcional.

En frontend Next/React, todo comportamiento interactivo nuevo o modificado debe contar con pruebas de componentes y comportamiento en Vitest con `jsdom`, React Testing Library, `user-event` y `jest-dom`; ejecútalas mediante `pnpm test` junto con la regresión aplicable. Consulta por roles y etiquetas y verifica contenido, foco, eventos y efectos públicos. `jsdom` no demuestra superposición, dimensiones, scroll ni respuesta visual reales: registra esas comprobaciones como recorridos de QA humana. Las pruebas integrales por navegador existentes pueden conservarse, pero no son obligatorias ni sustituyen esta cobertura. Esta política no cambia las pruebas backend/API ni las comprobaciones de integración entre módulos.

En `verificacion.md` registra criterio → prueba o comprobación, resultado, revisión y referencia a la evidencia. Se permite agrupar criterios cubiertos por la misma prueba. La evidencia histórica no acredita criterios añadidos o revisados después. No inventes comandos de pruebas antes de conocer el repositorio ni resultados antes de ejecutarlos.

**Cierre técnico del agente:** satisface el alcance preparado; las comprobaciones automatizadas y técnicas pasan; se preservan autorización e integridad aplicables; no se introducen reglas o funcionalidades ajenas; documentación, contratos y referencias están actualizados. Si falta backend, frontend u otra parte incluida, la spec no puede pasar a QA.

**Terminado:** además del cierre técnico, la QA visual humana está aprobada y registrada. Sólo entonces la spec pasa a Implementada.

El cierre Git forma parte de la entrega técnica de backend y frontend:

- Cada repositorio de implementación afectado termina con un único commit final que contiene sólo los cambios de la tarea.
- El mensaje sigue el formato `SPEC-NNN: verbo en imperativo`, por ejemplo `SPEC-004: evita importar CFDI duplicados`.
- Publica la rama con `git push -u origin "$RAMA_TRABAJO"`.
- Después del `push`, crea o reutiliza un PR normal por cada repositorio de implementación afectado con `gh`, usando `main` como base y `RAMA_TRABAJO` como head. La invocación debe ser equivalente a `gh pr create --base main --head "$RAMA_TRABAJO"` y proporcionar el título del commit y un cuerpo con la spec, criterios cubiertos, comprobaciones ejecutadas, pasos reproducibles para validar la spec y recorridos pendientes de QA; se pueden usar `--title` y `--body-file` para evitar prompts interactivos. Los pasos deben indicar preparación o datos de prueba, recorrido de validación, resultado esperado y cualquier comprobación técnica o visual que siga pendiente.
- Antes de crear, consulta los PR abiertos para esa combinación exacta de base y head, por ejemplo con `gh pr list --state open --base main --head "$RAMA_TRABAJO" --json number,url,headRefName,baseRefName`. Si existe uno, reutilízalo y no dupliques la entrega. Un PR cerrado, una colisión o un PR cuya base/head no coincidan no satisface este requisito.
- Antes de crear o reutilizar el PR/MR, consulta todos los colaboradores del repositorio con acceso mediante `gh api repos/{owner}/{repo}/collaborators --paginate` y solicita revisión a cada login devuelto: usa `--reviewer` al crear el PR o `gh pr edit <numero> --add-reviewer <login,...>` si se reutiliza. No omitas colaboradores silenciosamente; si GitHub no permite solicitar a alguno, reporta el login y el error. Una solicitud de revisión no equivale a aprobación de QA.
- En `verificacion.md` registra, para backend y frontend cuando estén afectados, su rama, hash del commit, remoto publicado y URL/estado del PR.

**Fallo de publicación o PR:** cada operación de rama remota, `push`, creación/identificación de PR o asignación de reviewers se intenta una sola vez. Si el primer intento falla, agota el tiempo, queda colgado o requiere cambiar de protocolo/autenticación, detén la ejecución inmediatamente: no reintentes, no esperes indefinidamente, no cambies SSH por HTTPS ni ejecutes una vía alternativa. Reporta en la respuesta y, si la spec se está actualizando, en `verificacion.md`, el repositorio, la operación, el comando o herramienta usada, el error observado, el estado local/remoto conocido y la acción manual necesaria. Una consulta de estado de sólo lectura puede hacerse una vez para distinguir éxito parcial de fallo, pero no abre un nuevo intento ni retrasa el cierre.

La tarea de código no está cerrada ni la spec puede pasar a QA hasta que todos los repositorios de implementación afectados tienen su commit, rama publicada y PR creado o reutilizado. La documentación puede quedar modificada en el repositorio de specs sin commit ni push de esta tarea, y las tareas documentales no crean PR de implementación. Un cambio previo detectado, una colisión de rama, un remoto ausente, falta de autenticación/acceso de `gh` o un fallo de commit, push o PR bloquea el cierre y debe reportarse con el repositorio y la causa. Este flujo no realiza merge ni despliegue automáticamente.

Sólo después de crear o reutilizar todos los PR y registrar sus URLs en `verificacion.md`, clasifica `spec.md` como QA y entrega al responsable humano los recorridos visuales que debe validar. Si la creación o identificación de cualquier PR falla, conserva el estado anterior y reporta el bloqueo. Para un cambio posterior, actualiza la misma `spec.md` sin renumerar criterios existentes; agrega nuevos IDs y registra los criterios retirados y su motivo. Actualiza `plan.md` y tareas si cambia la ejecución, conserva evidencia anterior con su revisión en `verificacion.md` y usa Actualización pendiente cuando el cambio ya esté preparado pero aún no tenga cierre técnico. Regenera el índice y ejecuta `python3 scripts/spec_index.py --check`. Las specs que ya estaban en QA no requieren PR retroactivo.
