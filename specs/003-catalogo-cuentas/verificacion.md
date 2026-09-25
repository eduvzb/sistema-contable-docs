# Verificación — SPEC-003

La entrega vigente y su estado se consultan en [spec.md](spec.md). Las pruebas, cierres y estados de entrega fechados a continuación son evidencia de su revisión histórica; no acreditan automáticamente criterios añadidos o modificados después.

## Entrega vigente

No hay tareas técnicas abiertas. La validación visual humana de búsqueda, limpieza, recuento y jerarquía permanece pendiente.

## Evidencia histórica y QA

**Revisión implementada:** `dfec655a56741b34257a80841dc9fd6933f698e2`.

**Referencias de implementación:**

- Backend, rama `codex/spec-003`: `601c75e1aa15092a8e3d7c24684f89d91f42e5bb`.
- Frontend, rama `codex/spec-003`: `552a1e64ef966684abc8b4a81dec9a65f4a02086`.

**2026-09-07 — Comprobaciones ejecutadas:**

| Cobertura | Evidencia y resultado |
|---|---|
| CA-003-01/02/04/05/07/08/09; persistencia de estado de CA-003-03; código por empresa, jerarquía, aislamiento e importación atómica | `./vendor/bin/sail artisan test --compact tests/Feature/Spec003Test.php`: 12 pruebas, 77 aserciones, aprobadas sobre PostgreSQL `testing`. |
| Regresión de SPEC-001 a SPEC-003 | `./vendor/bin/sail artisan test --compact`: 24 pruebas, 212 aserciones, aprobadas. |
| Formato, sintaxis y rutas backend | `./vendor/bin/sail pint --dirty --format agent`, revisión de sintaxis PHP y `php artisan route:list --path=api/companies --except-vendor`: aprobados; las cuatro rutas del catálogo quedaron registradas. |
| Dependencias backend | `./vendor/bin/sail composer validate --strict --no-check-publish`: válido. `./vendor/bin/sail composer audit`: sin avisos de vulnerabilidad. |
| Compilación de la interfaz | `pnpm lint`, `pnpm typecheck` y `pnpm build`: aprobados con Next.js 16.3.4; la compilación incluye `/companies/[id]/accounts`. |
| CA-003-06/10; aislamiento de partidas y protección posterior al primer uso | `./vendor/bin/sail artisan test --compact tests/Feature/Spec003Test.php`: 16 pruebas y 112 aserciones aprobadas. Rechaza con `422` cambios de código, naturaleza o padre sin alterar los datos originales; permite nombre y estado. La cobertura de pólizas rechaza cuentas ajenas y confirma rollback completo. |
| Regresión completa posterior a la integración | `./vendor/bin/sail artisan test --compact`: 72 pruebas y 650 aserciones aprobadas. |

El rechazo de cuentas inactivas/agrupadoras en nuevas partidas (parte de CA-003-03), el aislamiento al registrar partidas (CA-003-06) y el bloqueo estructural después del primer uso (CA-003-10) están comprobados en backend. La spec está en **QA** porque CA-003-11/12 ya cuentan con implementación y comprobación técnica; sólo resta la validación visual humana.

CA-003-03/06/10 ya cuentan con cobertura de integración automatizada mediante SPEC-006. CA-003-11/12 fueron implementados en frontend y comprobados técnicamente el 2026-09-10.

**2026-09-10 — Cierre técnico de CA-003-11/12:** el frontend normaliza código, nombre y término con Unicode NFD para ignorar mayúsculas y acentos; cuenta sólo las coincidencias directas, conserva los ancestros necesarios al renderizar la jerarquía, muestra el recuento contextual y ofrece estados vacíos con acciones para limpiar la búsqueda o restablecer filtros. La limpieza actualiza la continuidad de URL con `router.replace`, conserva la vista y devuelve el foco al campo de búsqueda. No cambió el contrato API ni el backend.

| CA-003-11/12 | `pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check` en `sistema-contable-frontend`: aprobados. Implementación en `src/components/company-workspace.tsx`; rama `codex/SPEC-003`, commit `f9f30d6fbacba0ef1db090532530f07d5a43f390`, publicada en `origin/codex/SPEC-003`. |

Con este cierre técnico, la spec pasa a **QA**. No se ejecutó una comprobación integral por navegador; la validación visual humana debe confirmar búsqueda por código/nombre con diferencias de mayúsculas y acentos, recuento, ancestros visibles, estado sin resultados, limpieza y recuperación del foco.

**QA humana:** no iniciada. Sólo la aprobación humana registrada permite marcar la spec Implementada.


## Historial documental

- **2026-09-24:** se migró la documentación a `spec.md`, `plan.md`, tareas por repositorio y `verificacion.md` sin cambiar código del producto ni ejecutar pruebas de producto; el estado vigente permanece en `spec.md`.
- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance del catálogo.
- **2026-09-07:** preparación para implementación por autorización explícita del usuario. Se fijaron campos, naturaleza, selección de movimientos, edición de cuentas utilizadas, integridad jerárquica y CSV atómico; SPEC-003 pasa a Lista.
- **2026-09-07:** se implementaron catálogo, jerarquía, estado e importación CSV en backend/frontend; se registraron las comprobaciones técnicas y la integración pendiente con SPEC-006.
- **2026-09-08:** se hizo autoritativo el bloqueo de código, naturaleza y padre después de la primera partida, conservando editables nombre y estado; se añadió cobertura de aislamiento y atomicidad.
- **2026-09-10:** por observación explícita del usuario se prepararon CA-003-11/12 para mejorar la búsqueda del catálogo, su limpieza, recuento y comprensión jerárquica. Se reclasificó como Actualización pendiente; no se modificó código ni se registró evidencia de implementación.
- **2026-09-10:** conforme a DP-004, el cierre técnico de CA-003-11/12 llevará la spec a QA; la validación visual será responsabilidad humana.
- **2026-09-10:** se implementaron y comprobaron técnicamente CA-003-11/12 en frontend; la rama `codex/SPEC-003` se publicó con el commit `f9f30d6fbacba0ef1db090532530f07d5a43f390`. La spec pasa a QA y conserva pendiente la aprobación visual humana.
