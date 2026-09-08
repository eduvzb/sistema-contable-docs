# Estado de implementación y continuidad

**Actualizado:** 2026-09-08  
**Propósito:** punto de relevo entre sesiones para el MVP. Este archivo no sustituye las specs ni declara criterios satisfechos sin su evidencia.

## Estado observado

| Spec | Estado de la spec | Implementación observada | Situación para continuar |
| --- | --- | --- | --- |
| SPEC-001 | Lista | Backend y frontend existentes; la evidencia registrada cubre la suite sin navegador. | Falta comprobación integral de interfaz por la restricción de no usar navegador. |
| SPEC-002 | Lista | Contexto explícito por empresa y periodo existente; integración con pólizas comprobada sin navegador. | Falta únicamente la comprobación interactiva, que permanece bloqueada por la restricción vigente. |
| SPEC-003 | Lista | Catálogo, uso aislado de cuentas en partidas y protección de código/naturaleza/padre después del primer uso existentes. | CA-003-03/06/10 tienen evidencia backend; falta la comprobación interactiva del catálogo. |
| SPEC-004 | Lista | Importación parcial CFDI 4.0, original privado, aislamiento, filtro por periodo, indicador `accounted` y detalle fiscal seleccionable existentes. | Backend y frontend verificados sin navegador; falta comprobación interactiva del detalle antes de promoverla a Implementada. |
| SPEC-005 | Lista | Endpoint de descarga simulada, fixtures deterministas por empresa/periodo, incorporación compartida con SPEC-004 y acción de frontend para iniciar/reintentar. | Backend y frontend verificados sin navegador; falta comprobación interactiva de la acción y continuidad hacia póliza antes de promoverla a Implementada. |
| SPEC-006 | Lista | Pólizas, partidas, relación muchos-a-muchos con CFDI, balance de `POSTED` y auditoría mínima existentes. El detalle del CFDI ahora expone pólizas, periodos, partidas y cuentas relacionadas. | CA-006-07/11 verificados en backend y frontend sin navegador; falta comprobación interactiva antes de promoverla a Implementada. |
| SPEC-007 | Lista | Trazabilidad documental CFDI `P` → facturas, importes `ImpPagado`, referencias pendientes y detalle bidireccional hacia pólizas/periodos. No calcula saldo PPD. | Backend y frontend verificados sin navegador; falta comprobación interactiva. El saldo, sobrepagos, diferencias, moneda avanzada y liquidación siguen fuera de alcance. |
| SPEC-008 | Lista | API `trial-balance`, cálculo por cuenta con partidas `POSTED` y pestaña de balanza integrados en los árboles de trabajo. El saldo inicial deriva de periodos anteriores; no se creó `OpeningBalance` ni migración histórica. | Backend verificado; frontend pasa lint/typecheck/build. Falta comprobación interactiva por la restricción vigente de no usar navegador ni Playwright antes de promoverla a Implementada. |
| SPEC-009 | Lista | Tres exportaciones XLSX contextuales, generación nativa sin dependencias, botones en documentos/pólizas/balanza y pruebas de contrato implementados en los árboles de trabajo. | Backend y frontend verificados sin navegador; falta comprobación interactiva de los botones y apertura manual en Excel antes de promoverla a Implementada. |

La palabra **Lista** conserva su significado SDD: contrato preparado, no necesariamente terminado. No se promovieron specs a **Implementada** en esta revisión porque las verificaciones sin navegador y los criterios señalados arriba aún no cubren el alcance completo.

## Evidencia disponible

- En esta continuidad, SPEC-005 quedó implementada en los árboles de trabajo; el backend pasó la suite completa con 48 pruebas y 397 aserciones dentro de Sail; el frontend pasó `pnpm lint`, `pnpm typecheck` y `pnpm run build`.
- SPEC-005 cubre endpoint protegido, periodo explícito, dos fixtures deterministas, duplicados, lote parcial, resultado vacío, fallo/reintento controlados y persistencia privada mediante `tests/Feature/Spec005Test.php` (6 pruebas, 47 aserciones focalizadas).
- SPEC-004 añade el detalle fiscal mediante `GET /api/companies/{companyId}/fiscal-documents/{fiscalDocumentId}`; su prueba focalizada pasó con 4 pruebas y 41 aserciones antes de la regresión completa.
- SPEC-006 añade al detalle del CFDI la colección `accounting_policies` con `period` y `entries.account`; su prueba focalizada pasó con 10 pruebas y 58 aserciones, cubriendo ausencia, multiplicidad, orden, aislamiento, autorización y exclusión de pólizas sin relación.
- SPEC-007 añade extracción de `DoctoRelacionado`/`ImpPagado`, persistencia de asignaciones documentales y trazabilidad bidireccional; `tests/Feature/Spec007Test.php` pasó con 6 pruebas y 43 aserciones focalizadas.
- Las pruebas Playwright de SPEC-004/006 existen en frontend, pero no se ejecutaron por la instrucción vigente de no usar navegador ni Playwright.
- En SPEC-008, el backend pasó `./vendor/bin/sail artisan test --compact` con 35 pruebas y 302 assertions; el frontend pasó `pnpm lint`, `pnpm typecheck` y `pnpm build`. No se ejecutó `pnpm test:e2e` por la restricción vigente de no usar navegador ni Playwright. `git diff --check` no reportó errores de espacios.
- Tras SPEC-007, la suite backend completa pasó con 54 pruebas y 440 aserciones; el frontend pasó `pnpm lint`, `pnpm typecheck` y `pnpm build`. No se ejecutó `pnpm test:e2e`.
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

1. Completar la evidencia visual de SPEC-004, SPEC-006 y SPEC-008 cuando se autorice navegador; los contratos y verificaciones automatizadas están preparados.
2. Completar la evidencia visual de SPEC-005 cuando se autorice navegador; el contrato y las verificaciones automatizadas están preparados.
3. Completar la comprobación visual de SPEC-007 cuando se autorice navegador; no promoverla a Implementada mientras falte esa evidencia.
4. Completar la evidencia interactiva de SPEC-009 cuando se autorice navegador y apertura manual en Excel; después promoverla a Implementada si todos los criterios quedan cubiertos.

## Continuidad de esta sesión — 2026-09-08

- **Brechas cerradas:** protección estructural de cuentas usadas (CA-003-10), aislamiento y atomicidad de cuentas/CFDI en pólizas (CA-003-06 y CA-006-08), contexto frontend no autoritativo (SPEC-002/004), precisión DT-011, autorización/auditoría/edición POSTED de SPEC-006 y continuidad descarga simulada → póliza de SPEC-005.
- **Cambios realizados:** backend aplica el bloqueo estructural dentro de transacción y bloquea las cuentas consultadas al validar partidas; los recursos suman y serializan decimales como texto. Frontend valida el periodo antes de montar datos protegidos, olvida contextos inválidos y exige `period_id` para la bandeja fiscal. No se añadieron reglas contables, migraciones ni dependencias.
- **Pruebas ejecutadas:** regresión backend 72 pruebas/650 aserciones; SPEC-003 16/112; SPEC-005 7/62; SPEC-006 15/114; 31 rutas API; Pint; lint, build y typecheck frontend; `git diff --check` en los tres repositorios.
- **Pruebas no ejecutadas:** navegador, Playwright y E2E por prohibición explícita. Tampoco se ejecutó Pint en modo `--test`, porque las instrucciones del backend ordenan ejecutar el formateador y prohíben expresamente ese modo; `./vendor/bin/sail pint --dirty --format agent` pasó.
- **Bloqueos restantes:** evidencia visual/interactiva de las nueve specs; apertura manual de XLSX para SPEC-009. BR-015, OQ-004, saldos/liquidación PPD, migración histórica y cierre de periodos permanecen sin resolver y fuera de este cambio.
- **Siguiente paso recomendado:** conservar todas las specs en Lista y, cuando se autorice navegador, ejecutar la evidencia interactiva en el orden SPEC-002 → SPEC-003 → SPEC-004/005 → SPEC-006/007 → SPEC-008/009.

## Estado de los repositorios al relevo

Los tres árboles contienen cambios locales que se deben conservar. No usar `git reset --hard` ni `git checkout --`.

| Repositorio | Rama / `HEAD` revisado | Cambios locales relevantes |
| --- | --- | --- |
| `sistema-contable` | `codex/spec-003` / `4e38ac5cc0b7dd2cd6900f49cb8b7ed48b127410` + cambios locales | Se conservaron las ediciones previas de SPEC-002/004/005/006/007/008/009, índice y ejemplos; esta continuidad actualiza la evidencia existente. |
| `sistema-contable-backend` | `codex/spec-003` / `868b20eaaa24c387e7e80f97a5798f024a4582e4` + cambios locales | Protección de cuentas, precisión de recursos y pruebas de SPEC-003/005/006. |
| `sistema-contable-frontend` | `codex/spec-003` / `597bdc5f71c2ee071ce173ddc81167f2a7461bd7` + cambios locales | Validación autoritativa de contexto y bandeja CFDI limitada a periodo explícito. |

## Cómo retomar o compartir

En una nueva sesión, indicar: “Lee `docs/estado-implementacion.md`, conserva los cambios locales y continúa con la evidencia pendiente de SPEC-004/006/008” (o con la spec elegida). Antes de cambiar archivos, revisar el estado actual de cada repositorio:

```sh
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable status --short --branch
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable-backend status --short --branch
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable-frontend status --short --branch
```

Para que otra persona o clon reciba el mismo punto, confirmar primero los cambios coherentes de los tres repositorios y compartir los commits junto con este archivo. Mientras los cambios sigan sin commit, este archivo permite retomar en el mismo espacio de trabajo, pero no transporta por sí solo los árboles de trabajo.
