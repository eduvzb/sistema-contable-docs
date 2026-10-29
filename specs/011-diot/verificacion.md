# Verificación — SPEC-011

## Estado de validación

### Actualización UI y Excel — 2026-10-28

- [x] Alcance confirmado por el usuario: IVA de todo el periodo, desglose por póliza, paginación fija de 25 filas y Excel alineado.
- [x] Punto de partida contrastado con `DiotReportService`, `DiotReportController`, `AccountingPolicyResource`, `diot-report.tsx`, su prueba y el contrato/servicio frontend: antes de esta actualización no había total, columna de póliza ni paginación.
- [x] Índice regenerado, 11 specs y enlaces locales validados; revisados los cinco documentos, IDs de criterios/tareas, dependencias sin ciclos y diferencias documentales. `git diff --check` sin errores de whitespace.
- [x] CA-011-10/15: desglose por póliza y número visible implementados y comprobados por HTTP y Vitest/RTL.
- [x] CA-011-14: total exacto de todo el periodo, incluso por encima de la capacidad monetaria individual, y estados sin periodo/carga/vacío/error comprobados.
- [x] CA-011-16: páginas de 25 filas, límites 0/1/25/26/50/51, teclado, navegación sin duplicados, reinicio por empresa/periodo y respuestas tardías comprobados con Vitest/RTL.
- [x] CA-011-11/12: Excel alineado con el periodo completo, primera columna textual, límite de 10,000 aceptado y 10,001 rechazado al separar pólizas, autenticación y aislamiento comprobados; regresiones backend/frontend ejecutadas.
- [ ] Cierre técnico de los repositorios afectados y QA visual humana registrados según el flujo.

Implementación autorizada tras la preparación documental. Ambos repositorios ya tenían cambios DIOT sin commit; el usuario eligió «Continuar en rama actual», autorizando preservarlos y trabajar en `codex/feat/SPEC-011/diot` sin commits ni publicación. Estado: **Actualización pendiente**, no QA ni Implementada, por faltar el cierre formal y la aprobación humana. No se realizaron commits, push ni PR.

#### Comprobaciones de producto de esta actualización

- Backend, desde Sail: `wsl -d Ubuntu --cd /mnt/c/proyecto-contable-corgor/sistema-contable-back -- bash ./vendor/bin/sail artisan test --compact --do-not-cache-result tests/Feature/Spec011Test.php tests/Unit/Support/ExactDecimalTest.php tests/Feature/Spec009Test.php`: **41 pruebas aprobadas, 320 aserciones**, 66.22 s. Incluye la nueva agrupación, suma dentro de póliza, total con acarreo y valores grandes, vacío, sólo POSTED, XLSX y aislamiento. La comprobación del límite usa dos pólizas con tasas coincidentes para detectar una fusión incorrecta. Primera ronda sin SPEC-009: 35 pruebas, 241 aserciones aprobadas.
- Frontend: `npm.cmd test -- --no-file-parallelism --maxWorkers=1 --pool=threads src/features/reports/components/diot-report.test.tsx src/features/reports/api/reports-api.test.ts src/features/policies/model/diot-eligibility.test.ts src/features/workspace/components/company-workspace.test.tsx src/features/policies/components/diot-policy-results.test.tsx`: **38 pruebas aprobadas** en 5 archivos, 37.95 s. Una ronda previa detectó el mock antiguo sin `meta` del workspace; se actualizó al contrato vigente y la repetición aprobó sin errores no manejados.
- `npm.cmd run lint` y `npm.cmd run typecheck`: aprobados después de los cambios finales.
- `npm.cmd exec prettier -- --check` sobre `src/shared/contracts/{index,reports}.ts`, `src/features/reports/api/reports-api{,.test}.ts`, `src/features/reports/hooks/use-diot-report.ts`, `src/features/reports/components/diot-report{,-table,-pagination}.tsx`, `src/features/reports/components/diot-report.test.tsx` y `src/features/workspace/components/company-workspace.test.tsx`: los diez archivos aprobados.
- Sail `exec -T laravel.test vendor/bin/pint --dirty --format agent`, y ejecución explícita sobre `ExactDecimal.php`, `DiotReportService.php`, `DiotReportController.php`, `ExactDecimalTest.php` y `Spec011Test.php`: aprobadas.
- `git diff --check` en backend y frontend: sin errores; frontend sólo advierte normalización LF/CRLF. Archivos nuevos/sin seguimiento revisados directamente, ya que no aparecen en el diff ordinario.
- No se ejecutaron build, suites completas, navegador ni integración interactiva real frontend/backend. Las pruebas frontend usan mocks; las pruebas backend ejercitan HTTP y leen el contenido generado del XLSX, no su apariencia en Excel. Los fallos ajenos del editor descritos abajo no se corrigen ni se consideran aprobados.

Comprobaciones documentales desde `sistema-contable-docs`:

- `wsl -d Ubuntu --cd /mnt/c/proyecto-contable-corgor/sistema-contable-docs -- python3 scripts/spec_index.py --write`: correcto, 11 specs y enlaces locales validados.
- Mismo comando con `--check`: correcto, 11 specs y enlaces locales validados.
- `git diff --check`: sin errores; sólo aviso de normalización LF/CRLF en el índice. La carpeta SPEC-011 ya estaba sin seguimiento al inicio, por lo que sus cinco documentos se revisaron directamente, además del diff del índice.
- El primer intento del generador rechazó las etiquetas en negrita de las tareas. Se ajustaron al formato `CA:`, `Depende de:` y `Hecho cuando:` admitido por el validador; las ejecuciones posteriores aprobaron.

QA humana de esta actualización: comprobar resumen sobre la tabla, legibilidad de «# poliza», controles y anchos pequeños, y ceros iniciales al abrir Excel. Pendiente, sin aprobación.

### Evidencia previa, no acredita la actualización del 2026-10-28

### Entrega local — 2026-10-27

- [x] Índice y enlaces locales de las 11 specs validados al iniciar mediante `docker run --rm --entrypoint python3 -v "C:\proyecto-contable-corgor\sistema-contable-docs:/workspace" -w /workspace sail-8.4/app scripts/spec_index.py --check`.
- [x] Validación documental repetida tras las aclaraciones mediante `wsl -d Ubuntu -- python3 /mnt/c/proyecto-contable-corgor/sistema-contable-docs/scripts/spec_index.py --check`: 11 specs y enlaces locales validados. El estado de la spec no cambió y el índice no requiere regeneración por esta ejecución.
- [x] Frontend: 27 pruebas de consulta, descarga, elegibilidad y workspace, más 5 pruebas DIOT del editor, aprobadas con Vitest/RTL en ejecución serial y aislamiento habilitado.
- [x] Frontend: lint, typecheck, Prettier de los 20 archivos de la entrega y `git diff --check` aprobados.
- [ ] Suite completa del editor no aprobada: los fallos varían entre ejecuciones; QA reprodujo fallos también en baseline y no confirmó una regresión DIOT.
- [x] Backend: cálculo exacto corregido, contabilización atómica, inmutabilidad, consulta y XLSX comprobados por 24 pruebas SPEC-011 (190 aserciones) y 6 unitarias de cálculo exacto (6 aserciones).
- [x] Concurrencia: 1 prueba y 9 aserciones aprobadas; una inclusión aceptada y la segunda rechazada sin efectos parciales bajo el bloqueo contable vigente.
- [x] Regresiones SPEC-004/005/006/009: 56 pruebas y 517 aserciones aprobadas mediante Sail literal desde WSL.
- [x] Contrato frontend corregido para consumir `diot_results[].groups[]`; 6 pruebas focalizadas del editor y del desglose anidado aprobadas, incluyendo un XML con tasa 16 %, cero y exento. La integración real con backend sigue pendiente.
- [x] QA independiente estático de backend y contratos, y pruebas frontend revisadas; sin defectos confirmados pendientes del alcance aclarado. No acredita las pruebas backend.
- [x] QA independiente final: 30 pruebas backend y 196 aserciones aprobadas; sin defectos confirmados pendientes en el alcance revisado.
- [ ] Integración interactiva real frontend/backend y validación visual humana no realizadas. No se exige recorrido integral por navegador para cerrar el trabajo del agente.

Desarrollo backend y frontend delegado a GPT-6 Luna `xhigh`; QA independiente a GPT-6 Luna `medium`, sin modificaciones de código. Por instrucción expresa del usuario no se hacen commits, publicaciones ni PR. Las comprobaciones locales no acreditan el cierre formal del flujo ni una aprobación humana.

#### Comandos frontend

- `npm.cmd run lint` y `npm.cmd run typecheck`: aprobados.
- `npm.cmd test -- --no-file-parallelism --maxWorkers=1 --pool=threads src/features/reports/components/diot-report.test.tsx src/features/reports/api/reports-api.test.ts src/features/policies/model/diot-eligibility.test.ts src/features/workspace/components/company-workspace.test.tsx`: 27 pruebas aprobadas.
- `npm.cmd test -- --no-file-parallelism --maxWorkers=1 --pool=threads -t "alterna selecciones|elegible|omite DIOT|sólo IDs|grupos POSTED" src/features/policies/components/accounting-policy-editor.test.tsx`: 5 aprobadas y 34 omitidas.
- `npm.cmd test -- --no-file-parallelism --maxWorkers=1 --pool=threads src/features/policies/components/accounting-policy-editor.test.tsx`: 33 aprobadas y 6 fallidas; afectan errores 422 con conceptos largos (2), consulta de conceptos CFDI (3) y conservación de captura tras `PERIOD_RESERVED` (1). Contraste con baseline y limitaciones descritos en QA frontend.
- `npm.cmd run format:check`: falla por 106 archivos; el chequeo específico de los 20 archivos modificados aprueba. No se reformatea el repositorio fuera del alcance.
- Primer intento con `--isolate=false`: 24 pruebas aprobadas y 3 fallidas por interferencia entre mocks; repetición con aislamiento habilitado: 27/27 aprobadas.
- No se ha ejecutado el build ni la suite completa del frontend. Las pruebas usan mocks, no acreditan integración real con backend ni lectura visual del Excel.
- Tras corregir el contrato: `npm.cmd test -- --no-file-parallelism --maxWorkers=1 --pool=threads -t "alterna selecciones|elegible|omite DIOT|sólo IDs|grupos POSTED|grupos anidados" src/features/policies/components/accounting-policy-editor.test.tsx src/features/policies/components/diot-policy-results.test.tsx`: 6 aprobadas y 34 omitidas. Typecheck, lint, Prettier de los cuatro archivos afectados y `git diff --check` aprobaron otra vez.
- Repetición por el coordinador sobre el contrato corregido: `npm.cmd test -- --no-file-parallelism --maxWorkers=1 --pool=threads src/features/reports/components/diot-report.test.tsx src/features/reports/api/reports-api.test.ts src/features/policies/model/diot-eligibility.test.ts src/features/workspace/components/company-workspace.test.tsx src/features/policies/components/diot-policy-results.test.tsx`: 28 aprobadas en 5 archivos. Repetición del comando focalizado del editor: 5 aprobadas y 34 omitidas. Total focalizado vigente: 33 pruebas aprobadas.

#### QA independiente frontend

- Luna `medium` confirmó 5 pruebas DIOT del editor y 27 de elegibilidad/reportes/workspace aprobadas, además de TypeScript, ESLint y Prettier de los archivos modificados. No modificó código ni documentación.
- La ejecución completa del editor revisada por QA tuvo 5 fallos. QA comparó contra una exportación temporal de `HEAD` sin cambiar el working tree: también fallaron en baseline las variantes de concepto largo, vínculo histórico y conservación ante `PERIOD_RESERVED`. Los fallos varían entre ejecuciones y pasan aisladamente; no hay regresión DIOT confirmada, pero la suite completa no está aprobada.
- Advertencia P2 de estabilidad: la prueba «muestra el botón para captura manual…» esperaba 4 llamadas a `api` y recibió 5 dentro de una suite completa; pasa aislada y en baseline. No se confirmó un fallo estable de producto atribuible a DIOT.

#### Backend: ejecución vigente y correcciones

Todos los comandos siguientes usan el prefijo `wsl -d Ubuntu --cd /mnt/c/proyecto-contable-corgor/sistema-contable-back -- bash ./vendor/bin/sail`:

- `artisan test --compact --do-not-cache-result tests/Unit/Support/ExactDecimalTest.php`: 6 aprobadas, 6 aserciones, 25.08 s.
- `artisan test --compact --do-not-cache-result tests/Feature/Spec011Test.php`: 24 aprobadas, 190 aserciones, 54.26 s.
- `artisan test --compact --do-not-cache-result tests/Feature/Spec011ConcurrencyTest.php`: 1 aprobada, 9 aserciones, 101.90 s.
- `artisan test --compact --do-not-cache-result tests/Feature/Spec004Test.php tests/Feature/Spec005Test.php tests/Feature/Spec006Test.php tests/Feature/Spec009Test.php`: 56 aprobadas, 517 aserciones, 100.55 s.
- `exec -T laravel.test vendor/bin/pint --dirty --format agent`: aprobado. También `exec -T laravel.test vendor/bin/pint --format agent tests/Unit/Support/ExactDecimalTest.php tests/Feature/Spec011Test.php`: aprobado.
- Coordinador: `exec -T laravel.test vendor/bin/pint --format agent app/Http/Controllers/DiotReportController.php app/Models/DiotInclusion.php app/Models/DiotInclusionLine.php app/Support/DiotInclusionService.php app/Support/DiotReportService.php database/migrations/2026_10_26_000000_add_diot_tax_lines_to_fiscal_documents_table.php database/migrations/2026_10_27_000000_create_diot_inclusions_and_lines_tables.php tests/Feature/Spec011Test.php tests/Feature/Spec011ConcurrencyTest.php tests/Unit/Support/ExactDecimalTest.php`: aprobado, incluidos todos los PHP nuevos sin seguimiento.

La primera ejecución completa de SPEC-011 obtuvo 22 aprobadas y 2 fallidas: IVA grande esperado `160000000000.000000`, recibido `153333333333.333333`; agregado esperado `20.019753`, recibido `19.719530`. Se corrigió el acarreo de `ExactDecimal::multiplyIntegers`: un recorrido indexado lee las posiciones actualizadas, en lugar de los valores copiados por `foreach`. Se añadieron seis casos unitarios y se mantuvieron las expectativas feature originales. La repetición de 24 pruebas aprobó.

El primer intento de regresiones tuvo 54 aprobadas y 2 errores porque Sail no podía escribir `storage/logs/laravel.log`. `ls -ln` confirmó UID/GID 0 y modo 644 en ese log y `.phpunit.result.cache`. Se ejecutó sólo `exec -T laravel.test chown sail:sail storage/logs/laravel.log .phpunit.result.cache`, sin borrar contenido ni ampliar permisos. La repetición aprobó las 56 pruebas.

Antes de recuperar el entorno hubo timeouts sin salida y procesos PHP en estado `D`; se reiniciaron contenedores, Docker Desktop y WSL con autorización del usuario, sin borrar volúmenes. Los timeouts no cuentan como pruebas aprobadas ni fallos de aserción. Las ejecuciones vigentes usan Sail literal desde WSL; no se atribuye una causa confirmada a los bloqueos anteriores.

#### QA independiente backend

- QA final Luna `medium` ejecutó independientemente `wsl -d Ubuntu --cd /mnt/c/proyecto-contable-corgor/sistema-contable-back -- bash ./vendor/bin/sail artisan test --compact --do-not-cache-result tests/Unit/Support/ExactDecimalTest.php tests/Feature/Spec011Test.php`: 30 pruebas aprobadas, 196 aserciones, 116.31 s. Confirmó la corrección del acarreo y el contrato anidado entre backend y frontend. No modificó código, pruebas ni documentación. Dictamen: sin defectos confirmados pendientes en el alcance revisado.
- El usuario confirmó que basta la referencia al CFDI vinculado y elegible y a la clave canónica `subtotal`, validadas por el servidor. QA retiró el P1 sobre acreditar una propuesta previa y no encontró otro fallo concreto del alcance confirmado en su revisión estática.
- Pasaron las pruebas de transición DRAFT → POSTED con DIOT, edición POSTED omitiendo IDs y cambiando importes contables, y conflicto específico de unicidad con rollback inducido mediante un trigger de prueba, incluidas en las 24 de SPEC-011.
- La prueba concurrente usa el bloqueo global contable vigente: comprueba serialización entre solicitudes, no una carrera aislada en la restricción única. El conflicto inducido mediante trigger tampoco equivale a dos escritores concurrentes. Se conserva esta limitación de evidencia.

### Evidencia de partida: BE-011-01 — 2026-10-26

- Se añadieron al importador la captura DIOT desde traslados 002 de conceptos, con fallback a globales sin mezclar niveles, normalización decimal a seis posiciones y motivo para desglose incompleto o factor no soportado. La migración conserva `diot_tax_lines` y `diot_unavailable_reason` como campos nuevos nullable; no reconstruye datos históricos.
- Las pruebas cubren prioridad conceptos/globales, tasas cero y exento sin importe, datos insuficientes, factor no soportado, ausencia de IVA identificable y exposición en detalle/lista.
- `docker compose up -d` — PostgreSQL y Laravel Sail iniciados; el contenedor ejecuta PHP 8.4.26.
- `docker compose exec -T laravel.test php artisan test --compact tests/Feature/Spec004Test.php` — 14 pruebas y 127 aserciones aprobadas.
- `docker compose exec -T laravel.test php artisan test --compact tests/Feature/Spec005Test.php` — 7 pruebas y 62 aserciones aprobadas.
- `docker compose exec -T laravel.test php artisan test --compact tests/Feature/Spec006Test.php` — 29 pruebas y 249 aserciones aprobadas.
- `php -l` para `CfdiXmlParser.php`, `FiscalDocumentResource.php`, `FiscalDocument.php`, la migración DIOT y `Spec004Test.php` — sin errores de sintaxis.
- `docker compose exec -T laravel.test vendor/bin/pint --dirty --format agent` — completado sin errores después de integrar el backend remoto.
- `git diff --check` — sin errores de whitespace.
- `python3 scripts/spec_index.py --check`, `python scripts/spec_index.py --check` y `py -3 scripts/spec_index.py --check` — no se pudieron ejecutar localmente porque Python no está disponible; la validación posterior en el contenedor está registrada arriba.

### Pendiente de validación humana

- [ ] Tras implementar: revisar highlight, sombreado independiente, contraste y operación visual del editor y la consulta DIOT; revisar lectura del XLSX.
- [ ] Registrar fecha, resultado y aprobación de QA humana después del cierre técnico real.

En la entrega anterior backend y frontend contenían cambios sin commit en `codex/feat/SPEC-011/diot`. No se acreditó cierre formal ni QA humana; se conservó Lista al no realizar la publicación requerida por el flujo. No se hicieron commits, publicaciones ni PR, conforme a la instrucción de aquella entrega. Para la actualización actual rige el estado indicado al inicio de este documento.
