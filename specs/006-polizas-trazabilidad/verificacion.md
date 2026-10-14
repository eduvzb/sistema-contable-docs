# Verificación — SPEC-006

## Entrega actual

CA-006-25 a CA-006-29: vista previa de conceptos CFDI. Implementación frontend y pruebas completadas el 2026-10-14. El endpoint real requerido está cubierto por las pruebas de backend de [SPEC-004](../004-documentos-fiscales/verificacion.md); quedan pendientes publicación y QA humana.

## Estado de validación

### Validación técnica comprobada

- [x] CA-006-25: la acción aparece en el selector antes de seleccionar, en bloques generados, documentos de captura manual y vínculos históricos.
- [x] CA-006-26/27: el panel identifica el CFDI, respeta orden y repetidos, presenta texto largo sin interpretarlo como HTML y distingue posiciones sin descripción y datos no disponibles.
- [x] CA-006-28: carga, error, reintento y respuestas tardías de otro documento o empresa no alteran la captura ni activan generación o guardado.
- [x] CA-006-29: nombre accesible, foco inicial, cierre, retorno al disparador y Escape sin cerrar la póliza se comprueban con pruebas de componentes.
- [x] El endpoint real de detalle entrega conceptos a un usuario autorizado y distingue lista vacía, `null` de documentos anteriores y acceso a otra empresa.
  - `./vendor/bin/sail artisan test --compact tests/Feature/Spec004Test.php`: 11 pruebas y 99 aserciones aprobadas.
- [x] Regresiones frontend, tipos, lint de archivos modificados, formato y build pasan.
  - `pnpm test`: 8 archivos y 42 pruebas aprobadas.
  - `pnpm typecheck`: aprobado.
  - `pnpm exec eslint <archivos modificados>`: aprobado.
  - `pnpm exec prettier --check <archivos modificados>`: aprobado.
  - `pnpm build`: aprobado.
  - El detector de interfaz de Impeccable no reportó hallazgos (`[]`).
- [x] Ramas publicadas, PR abiertos hacia `main` y revisión solicitada a colaborador con acceso.
  - Backend: commit `d841b59`, [PR #9](https://github.com/eduvzb/sistema-contable-back/pull/9).
  - Frontend: commit `c032007`, [PR #18](https://github.com/eduvzb/sistema-contable-front/pull/18).

### QA humana pendiente

- [ ] Confirmar que el ojo se identifica fácilmente junto al CFDI y aporta contexto al asignar cuentas.
- [ ] Revisar separación de conceptos, descripciones extensas y operación en escritorio y anchos estrechos.
- [ ] Confirmar que el panel no oculta acciones necesarias ni interrumpe la captura.
- [ ] Registrar fecha, resultado y observaciones. No hay aprobación humana registrada.

## Contraste de implementación y observación ajena

El editor consulta el detalle fiscal de forma diferida y presenta un panel dentro del diálogo actual. Los disparadores no cambian selección, propuestas, sugerencias, guardado ni contabilización. Las pruebas frontend usan el cliente API simulado; las pruebas backend ejercitan el endpoint real, pero no se ejecutó una prueba integral entre frontend y backend.

Existe una discrepancia previa fuera de esta entrega: CA-006-19/20 y la verificación anterior describen una tabla con filtros, mientras el código actual consultado presenta una lista con búsqueda. Esta preparación no reconstruye el selector ni modifica esos criterios; requiere revisión separada y no acredita su cumplimiento.
