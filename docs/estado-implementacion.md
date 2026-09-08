# Estado de implementación y continuidad

**Actualizado:** 2026-09-08  
**Propósito:** punto de relevo entre sesiones para el MVP. Este archivo no sustituye las specs ni declara criterios satisfechos sin su evidencia.

## Estado observado

| Spec | Estado de la spec | Implementación observada | Situación para continuar |
| --- | --- | --- | --- |
| SPEC-001 | Lista | Backend y frontend existentes; la evidencia registrada cubre la suite sin navegador. | Falta comprobación integral de interfaz por la restricción de no usar navegador. |
| SPEC-002 | Lista | Contexto explícito por empresa y periodo existente. | La pertenencia estable de pólizas ya existe; falta actualizar la evidencia de integración y la comprobación interactiva sigue sin ejecutar. |
| SPEC-003 | Lista | Catálogo y uso de cuentas por partidas existentes. | La integración con partidas ya está implementada; falta actualizar la evidencia y la comprobación interactiva sigue sin ejecutar. |
| SPEC-004 | Lista | Importación parcial CFDI 4.0, original privado, aislamiento, filtro por periodo e indicador `accounted` existentes. | El API entrega todos los campos fiscales, pero la bandeja no expone un detalle para consultar serie, folio, subtotal, impuestos, forma de pago y moneda. Revisar CA-004-04 antes de marcarla Implementada. |
| SPEC-005 | Borrador | Sin rutas, modelos ni interfaz de simulación. | Preparar contrato del simulador, fixtures, vacío/fallo/reintento y resultado de incorporación parcial. |
| SPEC-006 | Lista | Pólizas, partidas, relación muchos-a-muchos con CFDI, balance de `POSTED` y auditoría mínima existentes. | La relación póliza -> CFDI está expuesta; falta el recorrido inverso desde el CFDI hacia sus pólizas, partidas/cuentas y periodos (CA-006-07/11). |
| SPEC-007 | Borrador | Sin modelo ni contratos de complementos/pagos. | Bloqueada para Lista por el cálculo del saldo, fechas de corte, importes por factura, duplicidad/sobrepagos, moneda y representación de referencias no importadas. |
| SPEC-008 | Borrador | No existe API ni interfaz de balanza. Las partidas de pólizas `POSTED` ya son la fuente de movimientos. | Preparar origen del saldo inicial, relación entre periodos, signo/naturaleza, agregación sin doble conteo, cuentas sin movimiento y redondeo. |
| SPEC-009 | Borrador | No existen reportes ni exportaciones. | Depende del contrato de balanza y de definir formato Excel, columnas, filtros, límites y errores. |

La palabra **Lista** conserva su significado SDD: contrato preparado, no necesariamente terminado. No se promovieron specs a **Implementada** en esta revisión porque las verificaciones sin navegador y los criterios señalados arriba aún no cubren el alcance completo.

## Evidencia disponible

- El contexto de esta entrega reporta backend con 31 pruebas y 263 aserciones aprobadas, y frontend con `pnpm lint`, `pnpm typecheck` y `pnpm build` aprobados.
- Las pruebas Playwright de SPEC-004/006 existen en frontend, pero no se ejecutaron por la instrucción vigente de no usar navegador ni Playwright.
- En esta revisión no se volvieron a ejecutar pruebas. `git diff --check` no reportó errores de espacios en los tres repositorios.
- Las migraciones de CFDI, pólizas, partidas y la tabla pivote están presentes y el contexto confirma que están aplicadas.

## Orden recomendado

1. Corregir o delimitar explícitamente las dos brechas de consulta: detalle de CFDI (SPEC-004) y trazabilidad desde CFDI (SPEC-006).
2. Preparar SPEC-008. La fuente de movimientos está resuelta por las partidas de `POSTED`; el único bloque de diseño es definir la balanza mínima sin inventar `OpeningBalance` ni migración histórica.
3. Preparar/implementar SPEC-005 en paralelo funcional con la balanza si se desea demostrar la descarga simulada.
4. Preparar SPEC-007 tras acordar el cálculo de pagos y saldos PPD.
5. Preparar SPEC-009 después del contrato de SPEC-008.

## Estado de los repositorios al relevo

Los tres árboles contienen cambios locales que se deben conservar. No usar `git reset --hard` ni `git checkout --`.

| Repositorio | Rama / `HEAD` revisado | Cambios locales relevantes |
| --- | --- | --- |
| `sistema-contable` | `codex/spec-003` | DT-011, las actualizaciones de SPEC-004/006 y este relevo se confirman en el commit de documentación actual. |
| `sistema-contable-backend` | `codex/spec-003` / `7427840516423bb59f122e6db33eb890ba3bcbb8` | CFDI, pólizas, partidas, migraciones, pruebas y rutas confirmados. |
| `sistema-contable-frontend` | `codex/spec-003` / `2020e0194c3ba998aa29a412005019ca8734bd15` | Interfaz CFDI/pólizas, rediseño y pruebas E2E sin ejecutar, confirmados. |

## Cómo retomar o compartir

En una nueva sesión, indicar: “Lee `docs/estado-implementacion.md`, conserva los cambios locales y continúa con SPEC-008” (o con la spec elegida). Antes de cambiar archivos, revisar el estado actual de cada repositorio:

```sh
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable status --short --branch
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable-backend status --short --branch
git -C /Users/eduardovazquez/Documents/ChatGPT/sistema-contable-frontend status --short --branch
```

Para que otra persona o clon reciba el mismo punto, confirmar primero los cambios coherentes de los tres repositorios y compartir los commits junto con este archivo. Mientras los cambios sigan sin commit, este archivo permite retomar en el mismo espacio de trabajo, pero no transporta por sí solo los árboles de trabajo.
