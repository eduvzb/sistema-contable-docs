# Verificación — SPEC-006

El [estado de trabajo y los criterios](spec.md) se contrastan con el código y las pruebas de backend y frontend. Git conserva las entregas anteriores.

## Estado de validación

### Validado técnicamente

- [x] **CA-006-19/20 — Selección de CFDI:** búsqueda local sin distinguir acentos o mayúsculas, selección múltiple conservada al filtrar, orden de selección, estado vacío y vínculos previos entre periodos.
- [x] **CA-006-21 — Propuesta de partidas:** bloques consecutivos por CFDI con componentes, importes, orientación y precisión de seis decimales.
- [x] **CA-006-22 — Errores parciales:** el UUID y el motivo quedan visibles; un CFDI inválido no genera ajustes ficticios ni impide procesar los válidos.
- [x] **CA-006-23 — Origen y memoria de cuentas:** guardar DRAFT o POSTED conserva el origen, actualiza sugerencias de forma atómica y aplica la última asignación equivalente.
- [x] **CA-006-24 — Propagación de cuentas:** la cuenta se aplica sólo a componentes equivalentes posteriores que siguen vacíos, sin cambiar importes ni elecciones manuales.
- [x] **Regresión backend:** 95 pruebas y 932 aserciones aprobadas.
- [x] **Regresión frontend:** 27 pruebas, lint, tipos, build y formato aprobados.
- [x] **Integración:** PR backend #8 y PR frontend #17 fusionados a `main`.

### Pendiente de validación humana

- [ ] Confirmar visualmente la búsqueda, selección múltiple y orden de CFDI del periodo.
- [ ] Confirmar que los bloques propuestos sean fáciles de reconocer y editar antes de guardar.
- [ ] Confirmar que los errores por UUID y la continuidad de los CFDI válidos sean claras.
- [ ] Confirmar visualmente las sugerencias y la propagación de cuentas sin sobrescribir elecciones manuales.
- [ ] Registrar fecha, resultado y observaciones de QA; una aprobación permite cambiar el estado a Implementada.

## Evidencia técnica

La validación se hizo con datos aislados del entorno de pruebas; no se reinició ninguna base compartida ni se modificaron datos de usuario.

### Backend

- `vendor/bin/pint --dirty --format agent` — pasó; aplicó formato a la clase de propuesta.
- `DB_HOST=127.0.0.1 DB_PORT=54329 DB_USERNAME=sail DB_PASSWORD=password vendor/bin/phpunit tests/Feature/Spec006Test.php` — pasó: 26 pruebas, 216 aserciones.
- `APP_KEY=base64:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA= DB_HOST=127.0.0.1 DB_PORT=54329 DB_USERNAME=sail DB_PASSWORD=password vendor/bin/phpunit tests/Feature` — pasó: 95 pruebas, 932 aserciones.
- PR backend: [#8](https://github.com/eduvzb/sistema-contable-back/pull/8), fusionado a `main` el 2026-09-29 por `eduvzb`; se solicitó revisión a `alavazarez`, sin review registrado en GitHub.

### Frontend

- `pnpm test` — pasó: 6 archivos, 27 pruebas.
- `pnpm lint`, `pnpm typecheck`, `pnpm build` y `pnpm format:check` — pasaron.
- PR frontend: [#17](https://github.com/eduvzb/sistema-contable-front/pull/17), fusionado a `main` el 2026-09-29 por `eduvzb`; se solicitó revisión a `alavazarez`, sin review registrado en GitHub.

El estado de trabajo permanece en «QA» hasta completar y registrar la validación humana pendiente.
