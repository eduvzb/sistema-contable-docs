# Verificación — SPEC-006

## Entrega actual: CA-006-19/20/40/41/42/43/44

- [x] Catálogo global administrado sólo por administrador: alta/edición/activación/desactivación, códigos usados protegidos y tipo histórico inactivo conservado. El editor sólo permite tipos activos para nuevas asignaciones; errores de catálogo bloquean guardar y ofrecen reintento.
- [x] Tabla CFDI con Disponibles/Todos/Contabilizados y filtros de fecha, tipo, RFC/nombre contraparte, monto exacto, UUID/serie-folio y búsqueda general. POSTED define contabilización; selección y vínculos previos se conservan al filtrar. Documentos históricos siguen consultables.
- [x] POST/PUT exige reserva propia y devuelve 409 sin escrituras parciales. La interfaz refresca dueño por foco/polling, deshabilita cambios de terceros sin borrar captura y descarta respuestas tardías al cerrar/cambiar contexto, incluido el guardado en conflicto.
- [x] Backend final `6d3cd78cc750ce587b1576db33b4e31ea8a2a313`, frontend final `6a445f7bebbdef742dc298f0d0889bbc5146aa8c`, rama en ambos `codex/feature/SPEC-006/tipos-filtros-reserva`.
- [x] [PR backend #14](https://github.com/eduvzb/sistema-contable-back/pull/14) y [PR frontend #23](https://github.com/eduvzb/sistema-contable-front/pull/23) hacia main, SHA verificados, revisor `alavazarez` solicitado. No hay checks remotos disponibles. Integrar primero [SPEC-002 backend #13](https://github.com/eduvzb/sistema-contable-back/pull/13) y su [frontend #22](https://github.com/eduvzb/sistema-contable-front/pull/22); backend006 antes de frontend006. No se mezclaron commits de002 en estas ramas.

## Pruebas y revisión

- [x] Sail aislado: 121 pruebas/1,105 aserciones antes del caso histórico adicional; prueba final de tipos 7 pruebas/50 aserciones. Ensayo final conjunto002/003/006 con `./vendor/bin/sail exec -T -w /var/www/html/.orchestrator-worktrees/integration laravel.test php artisan test --compact`: 131 pruebas/1,217 aserciones, 13.30s, aprobado. Sólo DB testing; ejecuciones secuenciales del orquestador.
- [x] Autor frontend ejecutó `pnpm --config.verify-deps-before-run=false test`: 73/73. Orquestador comprobó el conjunto002/003/006/007: 87/87 pruebas en13 archivos. Tipos, lint, formato y build pasan en frontend006 final y en el conjunto: mismos comandos pnpm con `typecheck`, `lint`, `format:check`, `build`.
- [x] Pint, PHP lint y `git diff --check` aprobados. Sin cambios de dependencias. Dos migraciones aditivas del conjunto: plantilla versionada y catálogo de tipos; no ejecutadas sobre datos operativos.
- [x] Revisión independiente backend `audit_007_009` y frontend `audit_001_003`, gpt-6-luna/high: sin hallazgos pendientes sobre SHA finales. Se corrigieron autorización DELETE, fallo de catálogo y respuestas tardías antes de publicar. El orquestador resolvió en el ensayo conjunto sólo adiciones de rutas/paneles que coexisten con003.

## Corrección incremental: tipo tras conflicto de reserva

- [x] CA-006-44: recuperar la captura conserva el tipo seleccionado si continúa activo, o si es el tipo histórico propio. Recargar el catálogo no lo restablece silenciosamente. Si dejó de ser válido, se aplica la selección permitida existente.
- [x] Parche aportado por el usuario contrastado con el diff local: idénticos. Commit `e34a8bda387623587f8862314ac6f7a2b3376019`, mismo PR frontend #23. Cuatro regresiones cubren alta/edición con PERIOD_RESERVED y WORK_RESERVATION_REQUIRED y comprueban el payload del segundo guardado.
- [x] Orquestador: `pnpm --config.verify-deps-before-run=false test` — 77/77; `typecheck`, `lint`, `format:check`, `build` y `git diff --check` aprobados. Revisión independiente `review_reservation_type`, gpt-6-luna/high, sin bloqueantes. Ensayo conjunto actualizado: 91/91 pruebas, tipos, lint, formato y build aprobados; commit de ensayo `12548bb`. No cambia backend, contratos ni dependencias.

- [x] Base frontend actualizada a `origin/main` e5da561 tras integración externa de002/003/007. Conflictos aditivos de dashboard e índice resueltos conservando ambos paneles y revisados independientemente. Commit final `6a445f7bebbdef742dc298f0d0889bbc5146aa8c`; árbol idéntico al ensayo12548bb. En la rama final: 91/91, tipos, lint, formato y build aprobados. No se integró este PR en main.

## QA humana pendiente

- [ ] Revisar CRUD y selección de tipos activos, incluida lectura de tipos desactivados.
- [ ] Revisar filtros, estados CFDI, teclado y selección al cambiar filtros.
- [ ] Revisar toma/liberación de reserva, responsable visible y acciones deshabilitadas para terceros.
- [ ] Registrar persona, fecha, resultado y observaciones. La spec pasa a QA; no se acredita aprobación nueva ni estado Implementada.

## QA humana del alcance anterior (conservada)

- [x] Opción global de reutilización, indicación de uso, conservación de vínculos anteriores, lectura/edición de conceptos largos y error de longitud (tarea 018), y vista previa de descripciones integrada con SPEC-004 (tarea 023).
- [x] Aprobación general del alcance anterior confirmada el 2026-10-15 por el usuario solicitante, registrada previamente en el PR documental #1; fecha de ejecución y observaciones generales no especificadas. Tarea 023 sin observaciones reportadas.

La aprobación anterior se conserva para ese alcance. Tabla y filtros nuevos, tipos globales y reserva explícita requieren la QA humana pendiente indicada arriba.
