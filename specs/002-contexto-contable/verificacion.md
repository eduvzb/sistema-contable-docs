# Verificación — SPEC-002

La entrega vigente y su estado se consultan en [spec.md](spec.md). Las pruebas, cierres y estados de entrega fechados a continuación son evidencia de su revisión histórica; no acreditan automáticamente criterios añadidos o modificados después.

## Entrega vigente

No hay tareas técnicas abiertas. La validación visual humana del selector y la continuidad de contexto permanece pendiente.

## Evidencia histórica y QA

**Revisión implementada:** `2dc868a2484772db6c5fc881ff7eadab63ea059f`.

**Referencias de implementación:**

- Backend, rama `codex/spec-002`: `098ec630fdbe41ee393dd04ccd4e6505dc8ceb5d`.
- Frontend, rama `codex/spec-002`: `7f59d6c86dc3a3bb61f314d16032df21b316f593`.
- Actualización frontend de CA-002-07/08 en el árbol de trabajo, principalmente `src/components/companies-dashboard.tsx`, `src/components/company-workspace.tsx` y `src/components/fiscal-document-inbox.tsx`; aún sin commit y, por tanto, sin nueva revisión Git.

**2026-09-07 — Comprobaciones ejecutadas:**

| Cobertura | Evidencia y resultado |
|---|---|
| CA-002-02; alta y consulta de periodos; errores de autenticación, contraseña temporal, año inválido/duplicado, cruce de empresa y periodo; `CLOSED` informativo | `./vendor/bin/sail artisan test --compact tests/Feature/Spec002Test.php`: 5 pruebas, 41 aserciones, aprobadas sobre PostgreSQL `testing`. |
| Regresión de SPEC-001 y SPEC-002 | `./vendor/bin/sail artisan test --compact`: 12 pruebas, 135 aserciones, aprobadas. |
| Formato y carga del backend | `./vendor/bin/sail pint --dirty --format agent`, revisión de sintaxis PHP y `php artisan route:list --path=api --except-vendor`: aprobados; las tres rutas del contrato quedaron registradas. |
| Dependencias backend | `./vendor/bin/sail composer validate --strict --no-check-publish`: válido. `./vendor/bin/sail composer audit`: sin avisos de vulnerabilidad. |
| Compilación de CA-002-01/04/06 y ruta de contexto | `pnpm lint`, `pnpm typecheck` y `pnpm build`: aprobados con Next.js 16.3.4; la compilación incluye `/companies/[id]` y `/companies/[id]/periods/[periodId]`. |
| CA-002-03/05; pertenencia estable de póliza al contexto explícito y aislamiento al cambiar de periodo | `tests/Feature/Spec002Test.php::test_policy_creation_keeps_its_explicit_period_when_the_context_changes`: pasa; creación DRAFT por empresa/periodo, consulta en el periodo original y ausencia en el periodo siguiente. |
| Regresión backend posterior a la integración | `./vendor/bin/sail artisan test --compact`: pasa el 2026-09-08 con 62 pruebas y 544 aserciones. |
| CA-002-01/02/04; validación autoritativa del contexto en frontend | La carga protegida queda suspendida hasta validar `GET /api/companies/{companyId}/accounting-periods/{periodId}`; un `periodId` malformado, ajeno, inexistente o revocado se retira de la URL y de la memoria local, y se vuelve al selector. `pnpm lint`, `pnpm build` y `pnpm typecheck` pasan. |
| Regresión completa posterior a la corrección de continuidad | `./vendor/bin/sail artisan test --compact`: 72 pruebas y 650 aserciones aprobadas; las 31 rutas API se listaron correctamente. |

La evidencia técnica anterior conserva validez y CA-002-03/05 están comprobados por backend.

CA-002-06 se cubre estructuralmente al no derivar el contexto de la fecha actual. CA-002-07/08 fueron preparados documentalmente el 2026-09-10 y su cierre técnico se documenta a continuación.

**2026-09-10 — Cierre técnico de la actualización:**

| Cobertura | Evidencia y resultado |
|---|---|
| CA-002-07 | La interfaz muestra el periodo destino desde el listado de la empresa, conserva una región de contenido con altura mínima y presenta `Validando periodo contable…`; las acciones de pólizas quedan inhabilitadas y no se montan datos del periodo anterior mientras la validación autoritativa está pendiente. Cambios en `src/components/company-workspace.tsx`. |
| CA-002-08 | `tab`, `year`, `catalogSearch`, `catalogStatus`, `documentSearch` y `documentDirection` se leen y escriben en la URL. La navegación entre periodos conserva esos valores dentro de la misma empresa, el cambio de empresa los descarta y `push` permite recuperación con historial. Cambios en `src/components/companies-dashboard.tsx`, `src/components/company-workspace.tsx` y `src/components/fiscal-document-inbox.tsx`. |
| Regresión y compilación frontend | `pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check`: aprobados. La compilación terminó correctamente con Next.js 16.3.4. |

No se modificó el backend; la evidencia histórica de sus contratos, autorización, aislamiento y pertenencia explícita de pólizas conserva validez. No se ejecutó una comprobación integral de interfaz por navegador conforme a DP-004.

CA-002-09 quedó implementado en el frontend y su cobertura automatizada verifica coincidencias por razón social y RFC, normalización de mayúsculas/acentos, estado sin resultados, limpieza, teclado, puntero y ausencia de cambio de contexto antes de seleccionar. Después del cierre técnico, validar visualmente búsqueda y selección de empresa, transición de periodo, ausencia de datos/acciones del contexto anterior, recuperación de tab y filtros tras recarga e historial, y ajuste de la vista al regresar a una página válida.

| Criterio | Pruebas de componentes y comportamiento previstas |
|---|---|
| CA-002-09 | `src/components/company-selector.test.tsx`: 3 pruebas con Vitest, jsdom, React Testing Library y user-event; cubren búsqueda normalizada, RFC, estado vacío, limpieza, puntero, teclado y efecto `onSelect` únicamente al elegir. `pnpm test`, `pnpm typecheck`, `pnpm lint`, `pnpm build` y `git diff --check` aprobados. |

No se exige Playwright ni una prueba integral por navegador. La apariencia, superposición y ajuste visual del selector permanecen en el recorrido de QA humana.

**2026-09-12 — Cierre técnico de CA-002-09:** frontend en rama `codex/SPEC-002`, commit `022f28801a082e1656453ed733d93fee8ad2b28d`, publicado en `origin` mediante el PR [front #5](https://github.com/eduvzb/sistema-contable-front/pull/5) contra `main`. No se modificó backend. GitHub confirmó la solicitud de revisión a `alavazarez`; no mantuvo una solicitud adicional al autor `eduvzb`. La spec pasa a **QA**; queda exclusivamente validación visual humana.


## Historial documental

- **2026-09-24:** se migró la documentación a `spec.md`, `plan.md`, tareas por repositorio y `verificacion.md` sin cambiar código del producto ni ejecutar pruebas de producto; el estado vigente permanece en `spec.md`.
- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance contable.
- **2026-09-07:** preparación para implementación. Se resolvieron alta de ejercicios por cualquier usuario con acceso, doce meses persistidos, estado informativo, contexto explícito en URL, memoria local no autoritativa, contratos API y errores observables. SPEC-002 pasa a Lista por instrucción explícita del usuario.
- **2026-09-07:** se implementaron persistencia, API, autorización, selector y contexto visible; se registraron las comprobaciones técnicas y los pendientes de integración.
- **2026-09-08:** se comprobó la integración con las pólizas ya implementadas: la creación conserva empresa/periodo explícitos y el cambio de contexto no reasigna ni mezcla pólizas.
- **2026-09-08:** se reforzó el frontend para validar el periodo contra el backend antes de montar pólizas, balanza o documentos; los contextos inválidos se olvidan y regresan al selector sin usar el almacenamiento local como autorización.
- **2026-09-10:** por observación explícita del usuario se prepararon CA-002-07/08: transición estable al cambiar periodo y conservación recuperable de pestaña, página y filtros compatibles. Se reclasificó como Actualización pendiente; no se modificó código ni se registró evidencia de implementación.
- **2026-09-10:** se implementaron CA-002-07/08 en el frontend: transición estable con contexto destino pendiente, acciones dependientes bloqueadas y estado de navegación recuperable en URL; `pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check` pasaron. Conforme a DP-004, la spec pasa a QA y la validación visual queda a cargo de una persona.
- **2026-09-12:** se preparó CA-002-09 para sustituir el selector simple por una búsqueda y selección accesible de empresas por razón social o RFC; vuelve a Actualización pendiente. No se modificó código ni se registró evidencia técnica nueva.
- **2026-09-12:** se aplicó DT-012 a CA-002-09: su cierre técnico requiere pruebas de componentes y comportamiento con Vitest y React Testing Library; el layout real queda para QA visual humana.
- **2026-09-12:** se implementó CA-002-09 en frontend mediante un selector con búsqueda local normalizada, resultados operables con puntero/teclado y selección explícita. Pasaron `pnpm test` (3 pruebas), typecheck, lint, build y revisión de espacios; se publicó el PR [front #5](https://github.com/eduvzb/sistema-contable-front/pull/5). La spec pasa a QA y espera validación visual humana.
