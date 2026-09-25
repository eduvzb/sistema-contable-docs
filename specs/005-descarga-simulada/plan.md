# Plan técnico — SPEC-005

Este archivo describe la ejecución técnica de [SPEC-005](spec.md); los criterios funcionales vigentes y el estado sólo se definen allí.

## Contexto para ejecución

El alcance y los criterios de esta entrega están en [spec.md](spec.md); las tareas abiertas por repositorio identifican el trabajo pendiente. Consulta los contratos de las specs dependientes que esta ejecución consume. Las fuentes ya citadas en `spec.md` se reabren sólo ante una contradicción, un cambio posterior de regla o contrato, un supuesto que afecte el resultado, o una solicitud explícita de cambiar comportamiento.

## Plan técnico y contratos

- Backend: `POST /api/companies/{companyId}/fiscal-document-downloads/simulated` con cuerpo `{ "period_id": integer }`, protegido por Sanctum y la visibilidad de empresa vigente. El periodo se resuelve dentro de la empresa y un periodo ajeno devuelve `404`.
- La respuesta `200` tiene `{ data: { status, period_id, found_count, imported, rejected, message? } }`. `status` es `COMPLETED` o `FAILED`; `found_count` cuenta los XML entregados por el servicio; `imported` reutiliza los elementos de SPEC-004 y `rejected` contiene `{ name, errors }`. En `FAILED`, `imported` y `rejected` son colecciones vacías y `message` explica el fallo controlado.
- La implementación separa el servicio ficticio de la incorporación para que el mecanismo de SPEC-004 sea el único responsable de validación, duplicados, descarte del XML y resultado por archivo. No se persiste una entidad de descarga.
- Frontend: en la bandeja de SPEC-004, con periodo seleccionado, una acción `Descarga simulada` inicia la solicitud; mientras responde muestra estado de ejecución y luego muestra encontrados, incorporados y rechazados. En `FAILED` la misma acción permite `Reintentar descarga`. Los documentos incorporados aparecen al recargar la bandeja y pueden abrirse en el detalle y continuar hacia pólizas de SPEC-006.
- Acordar un mecanismo de ejecución suficiente para la demostración; la representación del proceso no implica por sí sola Redis, colas ni workers.

Aplican las [decisiones técnicas compartidas](../../docs/decisiones.md). El contrato de este alcance queda cerrado; cualquier ampliación del servicio o de los estados debe actualizar esta spec antes de modificar consumidores.

## Decisiones técnicas conservadas

- El servicio ficticio se sustituye en pruebas para demostrar resultado vacío y fallo/reintento; la interfaz de usuario solo expone iniciar o reintentar y muestra el resultado, sin controles de prueba ni conexión externa.

## Orden y coordinación

Las tareas pendientes se registran por repositorio en [backend](tasks-backend.md) y [frontend](tasks-frontend.md). El contrato responsable se prepara antes de implementarlo en un consumidor; las comprobaciones reales se registran en [verificación](verificacion.md).
