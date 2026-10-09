# Verificación — SPEC-006

El [estado de trabajo y los criterios](spec.md) se contrastarán con el código y las pruebas de frontend cuando se implemente la entrega. Git conserva la evidencia de entregas anteriores.

## Estado de validación

### Validación técnica completada

- [x] **CA-006-19 — Tabla de CFDI del periodo:** columnas Fecha, Tipo, RFC y Nombre de la contraparte, Monto y moneda, Folio fiscal, Folio interno y Vínculos; incluye selección por casilla, sin paginación ni selección masiva.
- [x] **CA-006-20 — Filtros y conservación de selección:** filtros locales combinables; extremos inclusivos; validación de rangos; limpieza, coincidencias, selección total y selección que permanece al ocultar filas.
- [x] **Vínculos históricos:** se cargan desde la póliza al editar, se muestran sin permitir selección y se conservan mientras se filtran CFDI del periodo.
- [x] **Estados y accesibilidad:** se distinguen carga, error, periodo vacío y cero coincidencias; etiquetas y errores asociados; casillas operables por teclado; tabla con desplazamiento interno.
- [x] **Continuidad del flujo:** «Continuar» conserva la propuesta actual, no guarda ni contabiliza; CFDI `P` se puede relacionar y seguir capturando manualmente.
- [x] **Pruebas y comprobaciones frontend:** `pnpm test -- src/features/policies/components/accounting-policy-editor.test.tsx` — 6 archivos, 28 pruebas aprobadas; `pnpm exec tsc --noEmit`; ESLint sobre los archivos modificados; Prettier `--check` sobre ambos archivos.

### QA humana pendiente

- [ ] Confirmar que la jerarquía de filtros y tabla facilita localizar un CFDI durante Nueva/Editar póliza.
- [ ] Confirmar que Fecha, Tipo, RFC, Nombre, Monto y folios se distinguen y comparan con facilidad.
- [ ] Confirmar que selección, vínculos y recuentos son claros aun cuando los filtros oculten filas seleccionadas.
- [ ] Confirmar que la tabla se mantiene operable en los viewports previstos mediante desplazamiento interno, sin cortar acciones.
- [ ] Registrar fecha, resultado y observaciones de QA; una aprobación permite cambiar el estado a Implementada.

## Evidencia técnica

Implementación frontend de CA-006-19/20 completada. El contrato backend vigente se reutilizó sin cambios. La revisión visual humana de filtros, tabla y desplazamiento interno sigue pendiente; hasta su aprobación, la spec permanece en QA.
