# Flujo de Spec Driven Development

**Seleccionar spec → aclarar lo necesario → preparar implementación → implementar → verificar y actualizar.**

La spec es el acuerdo verificable de una funcionalidad y se mantiene con sus cambios. No es una descripción retrospectiva del código.

## 1. Seleccionar y aclarar

Busca la spec en el [índice](../specs/README.md). Si la funcionalidad es nueva, usa la [plantilla](../specs/_plantilla.md), asigna el siguiente ID libre y agrégala al índice. No crees otra spec para corregir un incumplimiento de una existente.

Lee sus fuentes concretas según el [mapa](fuentes.md). Define propósito, alcance, comportamiento y criterios observables, incluyendo errores relevantes. Conserva las reglas por referencia; los criterios expresan cómo comprobarlas, no crean una segunda regla independiente.

Distingue **bloqueantes de preparación**, **supuestos existentes para validar durante el MVP** y **asuntos posteriores**. Una duda bloquea solo el comportamiento afectado; se puede avanzar con otras specs. No inventes reglas para cerrar huecos. Si es necesario reducir una spec para hacerla implementable, documenta el alcance y conserva el trabajo retirado en el índice.

Una instrucción explícita del usuario cuenta como decisión, sin confirmaciones repetidas. Registra decisiones locales en la spec y compartidas en [decisiones](decisiones.md). Para cambiar una regla del dominio, actualiza también la fuente responsable y las specs afectadas, dejando motivo y referencia a lo reemplazado.

## 2. Preparar

En la misma spec, describe el cambio técnico mínimo, dependencias, riesgos de integridad y verificación. Concreta únicamente los contratos que la funcionalidad necesita: operaciones, entradas, resultados, autorización y errores observables. No son obligatorios un OpenAPI separado, un ADR ni un archivo de tareas.

Los detalles técnicos todavía desconocidos deben resolverse antes de marcar Lista, consultando los repositorios reales al existir. El stack y la separación de responsabilidades ya están en decisiones; no se vuelven a decidir por spec.

| Estado | Condición |
|---|---|
| Borrador | Comportamiento en preparación; puede contener decisiones bloqueantes. |
| Lista | Alcance y criterios verificables; plan y contratos necesarios definidos; dependencias compatibles; ningún bloqueante para implementar ese alcance. Los supuestos existentes siguen etiquetados. |
| Implementada | Criterios satisfechos y evidencia real registrada para todos los componentes del alcance. |

La primera colección se entrega en Borrador. Redactar una spec no equivale a aprobar cada detalle ni a implementar el producto. Una spec Lista puede estar en ejecución: no hace falta otro estado. Un cambio de alcance vuelve a Borrador hasta preparar lo nuevo.

## 3. Implementar

Backend y frontend usan el mismo ID y revisión Git de este repositorio. Referencian esa revisión desde su tarea o PR; no copian specs para mantener variantes. Antes del primer commit de documentación puede usarse el archivo local para preparar trabajo, pero no inventar un hash.

Define cada contrato compartido en la spec responsable y enlázalo desde las consumidoras. Coordina cambios de contrato actualizando la spec y ambos consumidores afectados. La spec guarda enlaces a las revisiones/PR de implementación cuando existan.

Implementa solo el alcance preparado. Si el código contradice la spec, corrígelo; si debe cambiar lo esperado, cambia primero la spec y sus fuentes pertinentes. Documentación y refactors sin efecto observable no requieren una spec nueva, aunque sí la comprobación apropiada al cambio.

## 4. Verificar y mantener

Comprueba cada criterio de aceptación con evidencia suficiente. Para reglas de negocio, incluye pruebas del caso esperado, errores relevantes y regresiones; verifica autorización e integridad cuando correspondan. Una prueba de detalle interno no sustituye un criterio funcional.

En la spec registra criterio → prueba o comprobación, resultado, revisión y referencia a la evidencia. Se permite agrupar criterios cubiertos por la misma prueba. No inventes comandos de pruebas antes de conocer el repositorio ni resultados antes de ejecutarlos.

**Terminado:** satisface el alcance y los criterios; las comprobaciones pasan; se preservan autorización e integridad aplicables; no se introducen reglas o funcionalidades ajenas; documentación, contratos y referencias están actualizados. Si falta frontend u otra parte incluida, la spec todavía no está Implementada.

Para un cambio posterior, actualiza la misma spec sin renumerar criterios existentes; agrega nuevos IDs y registra los criterios retirados y su motivo. Conserva evidencia anterior con su revisión, distinguiéndola de lo todavía pendiente de verificar.

## Dos recorridos de uso

- **Funcionalidad nueva — descarga simulada:** seleccionar SPEC-005, consultar BR-020/AC-016, cerrar datos de prueba y contrato de incorporación con SPEC-004, preparar criterios, marcar Lista, implementar y registrar evidencia. No se agrega SAT real ni un archivo separado de tareas.
- **Corrección — duplicado importado:** localizar SPEC-004 y su criterio CA-004-03; mantener el comportamiento vigente, reproducir el incumplimiento, corregirlo y comprobar la regresión. No se crea otra spec ni se cambia la definición de duplicado para aceptar el fallo. Si se solicita cambiar esa definición, primero se registra la decisión y se actualizan BR-010/AC-015 y la spec.
