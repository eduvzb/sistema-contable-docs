# Verificación — SPEC-001

La entrega vigente y su estado se consultan en [spec.md](spec.md). Las pruebas, cierres y estados de entrega fechados a continuación son evidencia de su revisión histórica; no acreditan automáticamente criterios añadidos o modificados después.

## Entrega vigente

CA-001-18/19 y el contrato ampliado de empresa siguen sin implementación ni comprobación de esta entrega. Las pruebas anteriores acreditan sólo CA-001-01 a CA-001-17.

## Evidencia histórica y QA

La implementación se registró contra la revisión documental `0e576cbd80b74e03ae6ecb994968d6880aa28912` en dos repositorios hermanos, ambos en la rama `codex/spec-001`:

- Backend: `a6395058e7d6f82bf33f61f63fff0459c68fce6d`.
- Frontend: `353e18c0ead71ceae0c1b848c3058d59d45e249b`.

Comprobaciones ejecutadas el 2026-09-07:

- `./vendor/bin/sail artisan test`: 7 pruebas y 94 aserciones aprobadas sobre PostgreSQL 18, base `testing`. Cubren acceso válido/inválido, salida, límite de intentos, cambio obligatorio, Argon2id, restablecimiento e invalidación de sesiones, normalización y duplicados de correo/RFC, validación, aislamiento, acceso global, asignaciones atómicas y comando administrativo.
- `./vendor/bin/pint --test`: aprobado.
- `composer validate --strict --no-check-publish`: aprobado; análisis sintáctico de todos los archivos PHP propios: aprobado.
- `pnpm lint`: aprobado.
- `pnpm typecheck`: aprobado.
- `pnpm build`: build de producción aprobado con Next.js 16.3.4.
- Revisión de diff y `git diff --check`: aprobados para el cambio de CA-001-17.
- No se ejecutaron ni se exigieron pruebas integrales de interfaz por navegador para este cierre; su configuración existente no forma parte de la evidencia. La validación visual queda a cargo de QA humana.

**Ejecución 2026-09-12:** CA-001-17 quedó implementado en el frontend. `src/app/page.tsx` consulta `GET /api/me` y realiza una sola navegación de reemplazo hacia `/login`, `/password` o `/companies`; durante la consulta sólo muestra un estado neutral. La evidencia anterior permanece vigente. La comprobación visual de los destinos corresponde a QA humana.

**Entrega a QA:** disponible. QA humana debe validar la entrada por `/` en los tres estados de acceso, la ausencia de paso por `/companies` para usuarios no autenticados, el comportamiento del botón atrás y el recorrido administrador → empresa → contador → asignación → cambio de contraseña → consulta → retirada.

**Estado de entrega 2026-09-12:** el MR [front #4](https://github.com/eduvzb/sistema-contable-front/pull/4) quedó fusionado en `main` como `d2b7e06`. La restauración del comando de pruebas está publicada para revisión en el MR [front #6](https://github.com/eduvzb/sistema-contable-front/pull/6), commit `98283d5`.

**Preparación documental 2026-09-12:** CA-001-18/19 y los contratos ampliados quedan pendientes de implementación. En esta tarea no se modificaron backend/frontend ni se ejecutaron pruebas de producto; toda la evidencia anterior se conserva y no acredita estos criterios nuevos.

## Historial documental

- **2026-09-24:** se migró la documentación a `spec.md`, `plan.md`, tareas por repositorio y `verificacion.md` sin cambiar código del producto ni ejecutar pruebas de producto; el estado vigente permanece en `spec.md`.
- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado.
- **2026-09-07:** alcance, contratos, entorno y criterios completados por instrucción explícita del usuario; SPEC-001 pasa a Lista. Se preservan los criterios CA-001-01 a CA-001-07 y se agregan CA-001-08 a CA-001-16.
- **2026-09-07:** backend y frontend implementados en `codex/spec-001`; comprobaciones técnicas registradas.
- **2026-09-10:** se reclasificó como QA conforme a DP-004; sólo resta validación visual humana del recorrido preparado.
- **2026-09-12:** se preparó CA-001-17 para que la ruta raíz resuelva directamente el destino según la sesión, sin transición intermedia por `/companies`; vuelve a Actualización pendiente. No se modificó código ni se registró evidencia técnica nueva.
- **2026-09-12:** se implementó CA-001-17 en el frontend con resolución por `GET /api/me` y navegación de reemplazo. Se ejecutaron lint, typecheck, build y revisión de diff. No se ejecutaron ni exigieron pruebas integrales de interfaz por navegador para ese cierre; DT-012 aplica prospectivamente y no invalida esta evidencia histórica.
- **2026-09-12:** revisión documental de SPEC-001: criterios, contexto de ejecución, dependencias, contratos y recorrido de QA coherentes; se entrega a QA mediante el MR [front #4](https://github.com/eduvzb/sistema-contable-front/pull/4).
- **2026-09-12:** tras revisar la integración de #4 sobre `main` con #5 ya fusionado, se restablece el script `pnpm test` mediante el PR correctivo [front #6](https://github.com/eduvzb/sistema-contable-front/pull/6), para conservar la ejecución reproducible de Vitest. Pasaron `pnpm test` (1 archivo, 3 pruebas), `pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check`. No modifica el comportamiento de CA-001-17 ni incorpora pruebas integrales por navegador.
- **2026-09-12:** se prepararon CA-001-18/19 para nombre comercial obligatorio, tipo de persona derivado y ampliación del recurso de empresa; la integración atómica de `GENERAL_V1` se remite a SPEC-003. La spec vuelve a Actualización pendiente sin cambios de código ni pruebas de producto nuevas.
