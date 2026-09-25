# Verificación — SPEC-009

La entrega vigente y su estado se consultan en [spec.md](spec.md). Las pruebas, cierres y estados de entrega fechados a continuación son evidencia de su revisión histórica; no acreditan automáticamente criterios añadidos o modificados después.

## Entrega vigente

No hay tareas técnicas abiertas. La validación visual humana de los reportes y archivos XLSX permanece pendiente.

## Evidencia histórica y QA

**Evidencia de producto:** implementación realizada el 2026-09-08 en los árboles de trabajo. `tests/Feature/Spec009Test.php` pasó con 6 pruebas y 79 aserciones focalizadas; la suite backend completa pasó con 60 pruebas y 519 aserciones. `pnpm lint`, `pnpm typecheck` y `pnpm build` pasaron en frontend. `vendor/bin/pint --dirty --format agent` corrigió únicamente el formato de los archivos nuevos y `git diff --check` no reporta errores.

La cobertura verifica los tres MIME/nombres/contenidos XLSX, columnas y orden, precisión decimal, aislamiento por empresa y periodo, DRAFT/POSTED en pólizas, exclusión de DRAFT en balanza, archivos vacíos, autenticación/autorización y el límite de 10,000 filas.

**Revisiones de implementación:** backend parte de `829837d` y frontend de `ca15edd`; la implementación de SPEC-009 permanece como cambio local posterior a esas revisiones. La documentación parte de `4e38ac5` con cambios locales conservados.

**QA humana:** pendiente. Comparar visualmente los datos consultados/exportados en los tres reportes, accionar cada descarga y abrir el XLSX en una herramienta compatible. La autorización, precisión y contenido ya están cubiertos técnicamente; sólo la aprobación humana registrada permite marcar la spec Implementada.


## Historial documental

- **2026-09-24:** se migró la documentación a `spec.md`, `plan.md`, tareas por repositorio y `verificacion.md` sin cambiar código del producto ni ejecutar pruebas de producto; el estado vigente permanece en `spec.md`.
- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance de reportes.
- **2026-09-08:** se cerró el contrato MVP de tres exportaciones XLSX separadas, columnas estables, contexto por periodo, estados de pólizas, límite de filas y errores observables. SPEC-009 pasa a Lista.
- **2026-09-08:** se implementaron las tres rutas XLSX, generación nativa sin dependencias, botones de frontend y pruebas de contrato.
- **2026-09-10:** se reclasificó como QA conforme a DP-004; sólo resta validación visual humana de botones, descargas y apertura de archivos.
