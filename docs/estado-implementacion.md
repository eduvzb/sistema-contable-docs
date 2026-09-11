# Estado de implementación y continuidad

**Actualizado:** 2026-09-10
**Propósito:** punto de relevo entre sesiones para el MVP. Este archivo no sustituye las specs ni declara criterios satisfechos sin su evidencia.

## Estado observado

| Spec     | Estado de la spec       | Implementación observada                                                                                                                                                                                                                 | Situación para continuar                                                                                                                             |
| -------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| SPEC-001 | QA                      | Backend, frontend y comprobaciones técnicas existentes.                                                                                                                                                                                  | QA humana debe validar visualmente acceso, administración, asignaciones y cambio de contraseña.                                                      |
| SPEC-002 | QA                      | Contexto explícito por empresa y periodo, transición estable y continuidad de pestaña/año/filtros en URL implementados; integración con pólizas comprobada.                                                                              | QA humana debe validar visualmente selección, transición, recuperación por recarga/historial y filtros; después puede pasar a Implementada.          |
| SPEC-003 | Actualización pendiente | Catálogo, uso aislado de cuentas en partidas y protección de código/naturaleza/padre después del primer uso existentes. CA-003-11/12 preparan la mejora del buscador.                                                                    | Implementar y comprobar técnicamente búsqueda tolerante, limpieza, recuento y jerarquía; después pasa a QA.                                          |
| SPEC-004 | Actualización pendiente | Importación parcial CFDI 4.0, original privado, aislamiento, filtro por periodo, indicador `accounted` y detalle fiscal seleccionable existentes. CA-004-09/10 documentan limpieza del selector y la incidencia de lote duplicado+nuevo. | Reproducir, corregir y comprobar técnicamente el lote mixto y la limpieza; después pasa a QA.                                                        |
| SPEC-005 | QA                      | Endpoint, servicio simulado, incorporación compartida, continuidad hacia póliza y acción frontend verificados técnicamente.                                                                                                              | QA humana debe validar visualmente inicio, resultado, reintento y continuidad.                                                                       |
| SPEC-006 | Actualización pendiente | Pólizas, partidas, relación muchos-a-muchos con CFDI, balance de `POSTED` y auditoría mínima existentes. CA-006-14 prepara la mejora del calendario de fecha.                                                                            | Implementar y comprobar técnicamente el calendario accesible dentro del periodo; después pasa a QA.                                                  |
| SPEC-007 | QA                      | Trazabilidad documental CFDI `P` → facturas, importes `ImpPagado`, referencias pendientes y detalle bidireccional verificados técnicamente.                                                                                              | QA humana debe validar visualmente trazabilidad y navegación; saldo, sobrepagos, diferencias, moneda avanzada y liquidación siguen fuera de alcance. |
| SPEC-008 | QA                      | API `trial-balance`, cálculo por cuenta con partidas `POSTED` y pestaña de balanza verificados técnicamente. El saldo inicial deriva de periodos anteriores.                                                                             | QA humana debe validar visualmente lectura, importes y estados de la balanza.                                                                        |
| SPEC-009 | QA                      | Tres exportaciones XLSX contextuales, generación nativa, botones y pruebas de contrato verificados técnicamente.                                                                                                                         | QA humana debe validar visualmente botones, descargas y apertura de XLSX.                                                                            |

**Actualización pendiente** identifica una funcionalidad existente con cambios preparados que aún no tienen cierre técnico. **QA** identifica implementación y comprobaciones técnicas completas, con sólo validación visual humana pendiente. Ninguna spec pasa a Implementada sin aprobación humana registrada.

## Uso como relevo operativo

Este archivo sirve para localizar el estado, los repositorios, las revisiones y los pendientes de continuidad. No es una segunda fuente de comportamiento ni debe usarse para reconstruir el análisis de Planeación.

Al retomar una implementación, el agente debe abrir primero la spec objetivo y su sección **Contexto de ejecución**. Después consulta aquí únicamente la situación de los árboles, la evidencia disponible y el siguiente criterio pendiente. La spec, sus contratos y sus decisiones vigentes determinan el comportamiento; la documentación histórica de este archivo sólo se reabre cuando es necesaria para verificar una discrepancia o recuperar un dato no registrado en la spec.

## Preparación documental — 2026-09-10

Esta actualización registra observaciones de uso como extensiones de las specs responsables; no crea una spec transversal ni modifica reglas de negocio. No se cambió código de backend o frontend y no se ejecutaron pruebas de producto.

| Observación | Spec y criterio preparado |
| --- | --- |
| Mejorar búsqueda del catálogo | SPEC-003, CA-003-11/12: código/nombre, mayúsculas/acentos, jerarquía, recuento, vacío y limpieza. |
| Evitar saltos al cambiar periodo | SPEC-002, CA-002-07: transición estable sin datos o vacíos del contexto anterior. |
| Limpiar después de importar XML | SPEC-004, CA-004-09: control de archivos limpio, resultado visible y nueva sesión limpia. |
| Mantener tabs, página y estado de consulta | SPEC-002, CA-002-08, consumido por las vistas: continuidad recuperable y ajuste sólo si la página deja de existir. |
| Mejorar calendario de nueva póliza | SPEC-006, CA-006-14: fecha clara en español, teclado, periodo visible y error localizado. |
| CFDI nuevo no visible tras lote mixto | SPEC-004, CA-004-10: regresión duplicado+nuevo y coherencia entre importación, bandeja y relación en póliza. |

## Cierre técnico de SPEC-002 — 2026-09-10

Se implementaron CA-002-07/08 en el frontend. El cambio conserva el periodo destino visible durante la validación, reserva una superficie estable, deshabilita acciones dependientes y mantiene pestaña, año y filtros de catálogo/CFDI en la URL. El cambio de empresa descarta estado incompatible; la navegación por historial y la recarga lo recuperan dentro de la misma empresa. No se modificó backend.

`pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check` pasaron en `sistema-contable-frontend`. No se ejecutó navegador como criterio de cierre; la spec queda en QA para validación visual humana.

## Reclasificación QA — 2026-09-10

DP-004 retira la comprobación integral de interfaz por navegador del cierre del agente. SPEC-001, SPEC-005 y SPEC-007 a SPEC-009 pasan a QA porque su implementación y comprobaciones técnicas ya están completas. SPEC-003/004/006 permanecen en Actualización pendiente hasta cerrar sus criterios nuevos; SPEC-002 se suma a QA tras cerrar técnicamente CA-002-07/08. La validación visual y la aprobación para llegar a Implementada corresponden a una persona.

## Evidencia disponible

- En esta continuidad, SPEC-005 quedó implementada en los árboles de trabajo; el backend pasó la suite completa con 48 pruebas y 397 aserciones dentro de Sail; el frontend pasó `pnpm lint`, `pnpm typecheck` y `pnpm run build`.
- SPEC-005 cubre endpoint protegido, periodo explícito, dos fixtures deterministas, duplicados, lote parcial, resultado vacío, fallo/reintento controlados y persistencia privada mediante `tests/Feature/Spec005Test.php` (6 pruebas, 47 aserciones focalizadas).
- SPEC-004 añade el detalle fiscal mediante `GET /api/companies/{companyId}/fiscal-documents/{fiscalDocumentId}`; su prueba focalizada pasó con 4 pruebas y 41 aserciones antes de la regresión completa.
- SPEC-006 añade al detalle del CFDI la colección `accounting_policies` con `period` y `entries.account`; su prueba focalizada pasó con 10 pruebas y 58 aserciones, cubriendo ausencia, multiplicidad, orden, aislamiento, autorización y exclusión de pólizas sin relación.
- SPEC-007 añade extracción de `DoctoRelacionado`/`ImpPagado`, persistencia de asignaciones documentales y trazabilidad bidireccional; `tests/Feature/Spec007Test.php` pasó con 6 pruebas y 43 aserciones focalizadas.
- La validación visual de SPEC-004/006 queda reservada para QA humana después de cerrar sus criterios nuevos; no forma parte del cierre técnico del agente.
- En SPEC-008, el backend pasó `./vendor/bin/sail artisan test --compact` con 35 pruebas y 302 assertions; el frontend pasó `pnpm lint`, `pnpm typecheck` y `pnpm build`. `git diff --check` no reportó errores de espacios.
- Tras SPEC-007, la suite backend completa pasó con 54 pruebas y 440 aserciones; el frontend pasó `pnpm lint`, `pnpm typecheck` y `pnpm build`.
- Las migraciones de CFDI, pólizas, partidas y la tabla pivote están presentes y el contexto confirma que están aplicadas.
- SPEC-009 implementa `GET .../reports/fiscal-documents.xlsx`, `GET .../reports/accounting-policies.xlsx` y `GET .../reports/trial-balance.xlsx`, con una hoja, encabezados estables, importes textuales a seis decimales, consulta vacía válida y límite de 10,000 filas.
- SPEC-009 pasó `./vendor/bin/sail artisan test --compact tests/Feature/Spec009Test.php` con 6 pruebas y 79 aserciones; la suite backend completa pasó con 60 pruebas y 519 aserciones. `vendor/bin/pint --dirty --format agent`, `pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check` pasaron.
- SPEC-002 cerró su brecha de integración con `tests/Feature/Spec002Test.php::test_policy_creation_keeps_its_explicit_period_when_the_context_changes`: la prueba focalizada pasó con 6 pruebas y 51 aserciones; verifica creación en el contexto explícito, pertenencia estable y ausencia al consultar otro periodo.
- La implementación de SPEC-009 parte de backend `829837d`, frontend `ca15edd` y documentación `4e38ac5`, con todos los cambios nuevos conservados como cambios locales sin commit.
- La auditoría de continuidad del 2026-09-08 pasó la suite backend completa con 72 pruebas y 650 aserciones, la cobertura focalizada de SPEC-003 con 16/112, SPEC-005 con 7/62 y SPEC-006 con 15/114. También pasaron las 31 rutas API, Pint, `pnpm lint`, `pnpm build`, `pnpm typecheck` y `git diff --check` en los tres repositorios.
- SPEC-002/004 ahora suspenden toda carga de pólizas, balanza y CFDI hasta que el backend valide empresa/periodo; un contexto inválido se elimina de URL y almacenamiento local. SPEC-004 nunca consulta la bandeja sin `period_id`.
- SPEC-006 serializa importes y totales a seis decimales sin conversión a `float`; la prueba extrema conserva exactamente `999999999999.999999` en póliza y trazabilidad fiscal.
- `SPEC_REVISION` de backend/frontend se sincroniza únicamente después de confirmar esta revisión documental, usando el hash real resultante y sin inventar referencias.

## Orden recomendado

1. Implementar y comprobar técnicamente CA-003-11/12, CA-004-09/10 y CA-006-14; mover cada spec a QA al alcanzar su cierre técnico.
2. Entregar a QA humana los recorridos visuales de SPEC-001, SPEC-005 y SPEC-007 a SPEC-009.
3. Registrar aprobación u observaciones humanas en cada spec. Sólo las aprobadas pasan a Implementada.

## Continuidad de esta sesión — 2026-09-08

- **Brechas cerradas:** protección estructural de cuentas usadas (CA-003-10), aislamiento y atomicidad de cuentas/CFDI en pólizas (CA-003-06 y CA-006-08), contexto frontend no autoritativo (SPEC-002/004), precisión DT-011, autorización/auditoría/edición POSTED de SPEC-006 y continuidad descarga simulada → póliza de SPEC-005.
- **Cambios realizados:** backend aplica el bloqueo estructural dentro de transacción y bloquea las cuentas consultadas al validar partidas; los recursos suman y serializan decimales como texto. Frontend valida el periodo antes de montar datos protegidos, olvida contextos inválidos y exige `period_id` para la bandeja fiscal. No se añadieron reglas contables, migraciones ni dependencias.
- **Pruebas ejecutadas:** regresión backend 72 pruebas/650 aserciones; SPEC-003 16/112; SPEC-005 7/62; SPEC-006 15/114; 31 rutas API; Pint; lint, build y typecheck frontend; `git diff --check` en los tres repositorios.
- **Comprobación técnica omitida:** no se ejecutó Pint en modo `--test`, porque las instrucciones del backend ordenan ejecutar el formateador y prohíben expresamente ese modo; `./vendor/bin/sail pint --dirty --format agent` pasó.
- **QA humana pendiente o por programar:** recorridos visuales de las nueve specs y apertura manual de XLSX para SPEC-009. SPEC-003/004/006 deben alcanzar primero su cierre técnico; SPEC-002 ya está preparada para QA. BR-015, OQ-004, saldos/liquidación PPD, migración histórica y cierre de periodos permanecen sin resolver y fuera de este cambio.
- **Siguiente paso recomendado:** mantener SPEC-003/004/006 en Actualización pendiente hasta su cierre técnico; ejecutar QA humana sobre SPEC-001/002/005/007/008/009 y sobre las demás conforme lleguen a QA.

## Estado de los repositorios al relevo

Los tres árboles contienen cambios locales que se deben conservar. No usar `git reset --hard` ni `git checkout --`.

| Repositorio | Rama / `HEAD` revisado | Cambios locales relevantes |
| --- | --- | --- |
| `sistema-contable` | `codex/spec-003` / `4e38ac5cc0b7dd2cd6900f49cb8b7ed48b127410` + cambios locales | Se conservaron las ediciones previas de SPEC-002/004/005/006/007/008/009, índice y ejemplos; esta continuidad actualiza la evidencia existente. |
| `sistema-contable-backend` | `codex/spec-003` / `868b20eaaa24c387e7e80f97a5798f024a4582e4` + cambios locales | Protección de cuentas, precisión de recursos y pruebas de SPEC-003/005/006. |
| `sistema-contable-frontend` | `codex/spec-003` / `597bdc5f71c2ee071ce173ddc81167f2a7461bd7` + cambios locales | Validación autoritativa de contexto y bandeja CFDI limitada a periodo explícito. |

## Cómo retomar o compartir

En una nueva sesión, indicar: “Lee `docs/estado-implementacion.md`, conserva los cambios locales y continúa con la actualización pendiente elegida; al cierre técnico muévela a QA” (o proporcionar observaciones de QA humana). Antes de cambiar archivos, revisar el estado actual de cada repositorio:

```sh
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable status --short --branch
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable-backend status --short --branch
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable-frontend status --short --branch
```

Para que otra persona o clon reciba el mismo punto, confirmar primero los cambios coherentes de los tres repositorios y compartir los commits junto con este archivo. Mientras los cambios sigan sin commit, este archivo permite retomar en el mismo espacio de trabajo, pero no transporta por sí solo los árboles de trabajo.
