# Cuándo usar una spec

| Cambio | Trabajo suficiente |
|---|---|
| Pequeño, sin regla ni contrato nuevo | Investiga código y pruebas → cambia → verifica. Describe resultado y pruebas en la entrega; no crees spec. |
| Entre repositorios o con contrato existente | Aclara el resultado y el contrato; reutiliza una spec si ayuda a coordinar. Prueba cada lado. |
| Regla contable/fiscal, permiso, migración, concurrencia o contrato nuevo | Acuerda decisiones y límites antes de implementar. Escribe una spec breve y, si hace falta, un plan de integración. |

El código y las pruebas muestran qué existe; una spec expresa qué se quiere cambiar. Si difieren, comprueba el caso antes de editar. No conviertas Planeación antigua en requisito sin confirmación. [Fuentes](fuentes.md) · [Índice](../specs/README.md).

## Spec breve

Para una funcionalidad nueva, crea `specs/NNN-nombre/spec.md` desde la [plantilla](../specs/_plantilla/spec.md). Para una existente, añade sólo los criterios del cambio y conserva los anteriores. La primera pantalla debe responder: **qué cambia, qué no cambia y cómo sabremos que funciona**. Escribe cada decisión una vez; enlaza reglas ya definidas. Pregunta sólo por decisiones que bloqueen el cambio.

`plan.md` es opcional para contratos, migraciones, autorización, integridad u orden de integración no evidentes. Usa tareas separadas sólo si hay trabajo paralelo o dependencias difíciles de seguir. Evidencia separada sólo si es necesaria para retomar o registrar QA; resultados de pruebas también pueden quedar en la entrega o en Git. No crees archivos vacíos para satisfacer una plantilla.

Estados de specs existentes: **Borrador** (bloqueantes), **Lista** (criterios preparados), **Actualización pendiente** (cambio sobre funcionalidad existente), **QA** (comprobación técnica completa; falta revisión humana aplicable), **Implementada** (QA humana requerida aprobada). El estado organiza trabajo, no demuestra que el código lo cumpla. Si no hay QA visual o humana aplicable, registra la razón al cerrar el cambio sin inventar una aprobación.

## Comprobar y cerrar

- Verifica comportamiento y errores relevantes, permisos, aislamiento y regresiones según el cambio. Backend: pruebas con Sail sobre `testing`; frontend: `pnpm test`, lint, tipos y build cuando corresponda. Si un entorno falta, informa el bloqueo, no acredites pruebas no ejecutadas.
- Al entregar, indica resultado, comandos y resultados reales, y lo pendiente. Una revisión visual humana se registra sólo si ocurrió. No exijas navegador integral como sustituto de pruebas de componentes.
- No se exige rama, commit, push, PR ni revisión remota. Para publicar una entrega, usa la skill opcional únicamente si se solicita de forma expresa.
- Si cambiaste una spec, usa `python3 scripts/spec_index.py --check`. Actualiza el índice con `--write` sólo tras revisar cambios locales ajenos. El validador comprueba estructura y enlaces, no certifica implementación ni QA.
