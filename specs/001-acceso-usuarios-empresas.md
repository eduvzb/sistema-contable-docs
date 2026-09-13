# SPEC-001 — Acceso, usuarios y empresas

**Estado:** Actualización pendiente
**Usuario:** Administrador y contador  
**Dependencias:** Ninguna funcionalidad previa; decisiones compartidas DT-001 a DT-009.

## Propósito y alcance

Permitir que un administrador inicial creado desde consola gestione empresas, contadores y sus asignaciones; permitir que ambos roles inicien sesión y consulten únicamente el alcance autorizado. El administrador tiene acceso operativo a todas las empresas. El contador accede solo a las asignadas.

Incluye autenticación, cambio obligatorio de contraseña temporal, alta y consulta de empresas, alta y consulta de contadores, restablecimiento de contraseñas y reemplazo de asignaciones. Los datos de empresa incluyen RFC, razón social, nombre comercial, tipo de persona derivado, régimen fiscal y versión de plantilla de cuentas. Empresa/ejercicio/periodo, XML y operaciones contables corresponden a las specs siguientes; la copia del catálogo inicial se concreta en SPEC-003.

Quedan fuera registro público, invitaciones por correo, edición de perfiles, bajas, creación de otros administradores desde la interfaz, roles adicionales, límites comerciales y administración de múltiples despachos.

## Fuentes

- [Alcance §3: actores](../docs/planeacion/003%20-%20MVP-Scope.md#3-usuarios-incluidos); [§4: empresas](../docs/planeacion/003%20-%20MVP-Scope.md#4-empresas); [§18: inicio del recorrido](../docs/planeacion/003%20-%20MVP-Scope.md#18-flujo-completo-que-debe-demostrar-el-mvp).
- [Análisis §5: administrador y contador](../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#5-actores-del-sistema) y [OQ-011](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#13-oq-011--organization-expl%C3%ADcita) (un despacho como supuesto provisional; Organization no es obligatoria).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa) (aislamiento confirmado).
- [BR-021](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#23-br-021--la-empresa-conserva-nombre-comercial-y-tipo-de-persona-derivado) y [BR-022](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#24-br-022--cada-empresa-nueva-recibe-una-copia-independiente-de-la-plantilla-general) (identidad comercial, derivación del tipo e integración con el catálogo inicial).
- [Análisis §6: datos de empresa](../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#6-empresas), limitado a los datos fiscales incluidos por el alcance del MVP.
- [Catálogo CFDI 4.0 del SAT](https://www.sat.gob.mx/minisitio/Factura/emite_quenecesitoparafacturar.htm), del que se conserva una copia versionada de `c_RegimenFiscal` en el backend.

## Contexto de ejecución

**Modo actual:** Actualización pendiente. CA-001-01 a CA-001-17 conservan su implementación y evidencia histórica; CA-001-18/19 y la ampliación del contrato de empresa están preparados documentalmente, todavía sin implementación ni comprobación de producto.

**Paquete funcional:** esta spec contiene el alcance autoritativo de acceso, roles, empresas, contadores, asignaciones, autenticación, contratos, errores y criterios CA-001-01 a CA-001-19. En la siguiente implementación trabajar CA-001-18/19, coordinar la atomicidad de creación con SPEC-003 y conservar la evidencia existente.

**Dependencias y fuentes consolidadas:** no depende de otra spec funcional; las decisiones compartidas y las fuentes enlazadas arriba ya están reflejadas en el comportamiento, decisiones locales y contratos de este documento. No recargar esas fuentes durante una ejecución normal si no cambiaron.

**Reabrir fuentes cuando:** una fuente cambie después de esta preparación, aparezca una contradicción, se modifique una política de acceso compartida, exista un pendiente que afecte el resultado o el usuario solicite cambiar el comportamiento.

## Comportamiento y criterios de aceptación

El acceso usa correo y contraseña. Nombre y correo son obligatorios; el correo se normaliza a minúsculas sin espacios exteriores y es único. Hay dos roles fijos: `admin` y `accountant`.

El comando interactivo `app:admin` crea el primer administrador con contraseña oculta. Si existe un administrador, no crea otro; `--reset-password` permite restablecer su contraseña. Desde la interfaz, el administrador crea exclusivamente contadores. El backend genera las contraseñas temporales aleatorias y solo las devuelve en la respuesta de creación o restablecimiento; nunca se conservan en texto plano.

Un contador con contraseña temporal debe cambiarla antes de consultar empresas u operar. Mientras tanto solo puede consultar su identidad, cambiar su contraseña y cerrar sesión. El cambio exige contraseña actual, nueva contraseña y confirmación; la nueva contraseña tiene entre 12 y 128 caracteres. Las contraseñas se almacenan con Argon2id. El restablecimiento invalida sesiones existentes y vuelve a exigir el cambio inicial.

Una empresa tiene RFC único, razón social, nombre comercial y un régimen fiscal. El RFC se normaliza a mayúsculas sin espacios exteriores y debe cumplir una comprobación estructural básica de 12 o 13 caracteres; no se consulta su situación ante SAT. La razón social y el nombre comercial son obligatorios, se recortan y admiten hasta 255 caracteres; sólo el RFC es único. La razón social se presenta como nombre principal y el nombre comercial como dato secundario.

`taxpayer_type` se calcula siempre a partir del RFC normalizado: 12 caracteres producen `PERSONA_MORAL` y 13, `PERSONA_FISICA`. No se captura ni se persiste y no filtra el catálogo de regímenes. El régimen se elige por código y nombre desde la copia versionada de `c_RegimenFiscal`; el backend valida que exista en ella y conserva procedencia y fecha del catálogo. `account_template_version` identifica la plantilla copiada conforme a SPEC-003. Para empresas existentes, la transición de datos establece `commercial_name = legal_name` y `account_template_version = null` sin generar cuentas.

Las asignaciones se reemplazan como conjunto dentro de una transacción, sin duplicados. Retirar una asignación surte efecto desde la siguiente petición. Un contador sin asignaciones recibe una lista vacía. Consultar una empresa inexistente o no autorizada produce el mismo `404`.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-001-01 | Un usuario registrado presenta credenciales válidas. | Inicia sesión, la sesión se regenera y obtiene su identidad; se dirige al cambio obligatorio o a empresas según corresponda. |
| CA-001-02 | Se intenta acceder sin autenticación, con credenciales inválidas o excediendo cinco intentos por minuto para el mismo correo normalizado e IP. | No se obtiene información protegida; se responde respectivamente `401` o `429`, sin revelar si la cuenta existe. |
| CA-001-03 | El administrador registra una empresa con RFC, razón social y código de régimen válidos. | Los valores normalizados se conservan y la empresa queda disponible para consulta y asignación con `201`. |
| CA-001-04 | El administrador registra un contador y le asigna una empresa. | Recibe una sola vez la contraseña temporal; el contador puede autenticarse, cambiarla y consultar la empresa. |
| CA-001-05 | Un contador tiene asignada la empresa A, pero no B; intenta consultar B por interfaz o petición directa. | B no aparece como accesible y su detalle responde `404`, igual que una empresa inexistente. |
| CA-001-06 | Un contador intenta realizar acciones reservadas al administrador. | Recibe `403`; no puede registrar usuarios o empresas, restablecer contraseñas ni cambiar asignaciones. |
| CA-001-07 | El administrador consulta las empresas existentes. | Consulta todas las empresas y puede acceder operativamente a cada una sin asignación explícita. |
| CA-001-08 | Un contador autenticado conserva la contraseña temporal e intenta consultar empresas. | Recibe `403`; solo puede consultar identidad, cambiar contraseña y cerrar sesión. |
| CA-001-09 | Se cambia la contraseña con contraseña actual correcta, confirmación coincidente y longitud válida. | La contraseña queda protegida con Argon2id, cesa el cambio obligatorio y la sesión se regenera; datos incorrectos reciben `422`. |
| CA-001-10 | El administrador restablece la contraseña de un contador. | Las sesiones anteriores se invalidan, se exige otro cambio inicial y la nueva contraseña temporal aparece únicamente en esa respuesta. |
| CA-001-11 | Se crea o restablece una credencial temporal y después se consultan identidad o usuarios. | Ningún hash ni contraseña temporal aparece en esas respuestas ni se guarda en texto plano. |
| CA-001-12 | Se intenta crear un correo o RFC equivalente tras normalizarlo, o usar datos/régimen inválidos. | Se responde `422` y no se crea un duplicado ni un registro parcial. |
| CA-001-13 | Se reemplazan asignaciones con IDs repetidos o inválidos. | Los repetidos se rechazan; un ID inexistente o ajeno al contrato invalida toda la operación y el conjunto anterior permanece intacto. |
| CA-001-14 | Se retira una empresa a un contador que mantiene sesión abierta. | Su siguiente petición deja de listar y no puede consultar la empresa retirada. |
| CA-001-15 | Se ejecuta `app:admin` sin administrador y luego cuando ya existe; o se usa `--reset-password`. | Se crea solo el primero; ejecuciones posteriores no crean otro y el modo de recuperación restablece únicamente al administrador existente. |
| CA-001-16 | El usuario cierra sesión. | La sesión actual se invalida y la respuesta es `204`; las peticiones protegidas posteriores responden `401`. |
| CA-001-17 | Un usuario abre la ruta raíz `/`. | La interfaz resuelve su estado de acceso y realiza una sola navegación de reemplazo al destino aplicable: `/login` si no está autenticado, `/password` si debe cambiar su contraseña o `/companies` si puede operar. No muestra una pantalla protegida intermedia ni agrega `/companies` al historial antes de enviar a un usuario no autenticado a `/login`. |
| CA-001-18 | El administrador crea una empresa con nombre comercial válido o intenta omitirlo, enviarlo sólo con espacios o superar 255 caracteres. | El valor válido se recorta y se conserva sin exigir unicidad; los casos inválidos reciben `422` y no dejan empresa ni catálogo parcial. La interfaz presenta la razón social como nombre principal y el nombre comercial como dato secundario. |
| CA-001-19 | Se captura un RFC estructuralmente válido de 12 o 13 caracteres durante el alta o se consulta una empresa nueva o existente. | La interfaz y el recurso muestran respectivamente `PERSONA_MORAL` o `PERSONA_FISICA`, calculado a partir del RFC normalizado y sin persistirlo ni filtrar regímenes. El recurso incluye `commercial_name` y `account_template_version`; las empresas existentes exponen nombre comercial igual a razón social y versión `null`. |

### Análisis de hallazgo 2026-09-12

| Hallazgo | Comportamiento actual que falla | Comportamiento esperado | Impacto documental | Componentes |
|---|---|---|---|---|
| La ruta raíz pasa por `/companies` antes de `/login`. | `/` envía incondicionalmente a `/companies`; esa pantalla consulta la sesión y sólo después redirige a `/login`, produciendo una transición protegida innecesaria. | La ruta raíz decide el destino a partir del estado de acceso y reemplaza la navegación una sola vez según CA-001-17. | Se agrega CA-001-17 y una decisión local; no cambia el contrato de autenticación ni requiere una decisión compartida. | Frontend. El backend conserva `GET /api/me` y sus respuestas vigentes. |

## Decisiones locales

- El volumen inicial usa listas completas, ordenadas por nombre y después ID, sin paginación.
- `users` conserva nombre, correo único, hash, rol y `must_change_password`; `companies`, RFC único, razón social, nombre comercial, código de régimen y versión nullable de plantilla; `company_user`, claves foráneas y unicidad usuario–empresa. `taxpayer_type` no se persiste.
- Se usan Eloquent, Form Requests, Policies y API Resources, sin paquetes de roles ni capa de repositorios.
- Sesiones y limitación de intentos se respaldan en PostgreSQL mediante capacidades de Laravel. El guardado de asignaciones y la invalidación de sesiones son transaccionales.
- La interfaz es en español, semántica y accesible, con estados de carga, vacío y error, validación junto a campos, paleta neutra y acento índigo. No incluye dashboard contable.
- La comprobación de RFC es estructural, no prueba existencia, vigencia ni situación fiscal. El régimen almacenado debe pertenecer al catálogo versionado, pero no se limita por tipo de persona en esta spec.
- La razón social es el identificador visible principal de la empresa. El nombre comercial es obligatorio, secundario y no único. El tipo de persona se muestra como dato calculado y nunca como campo editable.
- La compatibilidad de datos existentes fija nombre comercial igual a razón social y versión de plantilla `null`; no ejecuta una carga retroactiva del catálogo. SPEC-003 define la copia `GENERAL_V1` para altas nuevas y su transacción compartida.
- La ruta raíz es un punto de entrada neutral: su destino depende del estado de acceso y se resuelve sin encadenar rutas protegidas. No se introduce una página inicial nueva.

## Entorno y arquitectura

- Backend: Laravel 13, PHP 8.4, Sanctum y PostgreSQL 18 en Docker mediante Sail. Servicios mínimos: aplicación y PostgreSQL.
- Frontend: Next.js 16, TypeScript, App Router, Tailwind CSS y pnpm sobre Node 22. Los bloqueos fijan las versiones instaladas.
- Bases: `sistema_contable` para desarrollo y `testing` para pruebas, con volumen persistente. La suite rechaza ejecutar pruebas destructivas si la base activa no es `testing`.
- Direcciones locales: frontend `http://localhost:3000`, API `http://localhost:8000` y PostgreSQL expuesto solo en `127.0.0.1:54329`.
- Los repositorios hermanos `sistema-contable-backend` y `sistema-contable-frontend` trabajan en `codex/spec-001` y registran la misma revisión de esta spec.

## Autenticación y autorización

Se usa Sanctum en modo SPA: cookie de sesión HttpOnly, CSRF y `localhost:3000` como origen stateful/permitido. El navegador envía credenciales; Laravel conserva la autoridad. La sesión se regenera al iniciar sesión y cambiar contraseña, y se invalida al salir. El ingreso se limita a cinco intentos por minuto por correo normalizado e IP.

Las rutas autenticadas usan `auth:sanctum`. Un middleware de cambio obligatorio restringe al contador a identidad, cambio de contraseña y salida. Policies resuelven administración y acceso a empresa en cada petición; no se confía en ocultar controles en el frontend.

## Contrato API

| Operación | Método y ruta | Autorización / resultado |
|---|---|---|
| Preparar CSRF | `GET /sanctum/csrf-cookie` | Pública; cookie CSRF. |
| Iniciar sesión | `POST /login` | Pública; `{email,password}`; `204`. |
| Cerrar sesión | `POST /logout` | Autenticada; `204`. |
| Consultar identidad | `GET /api/me` | Autenticada; `{data:{id,name,email,role,must_change_password}}`. |
| Cambiar contraseña | `PUT /api/me/password` | Autenticada; `{current_password,password,password_confirmation}`; `204`. |
| Listar/crear contadores | `GET /api/users`, `POST /api/users` | Admin; creación `{name,email}`; `200`/`201`. |
| Restablecer contraseña | `POST /api/users/{user}/temporary-password` | Admin y destino contador; `200` con contraseña temporal. |
| Consultar/reemplazar asignaciones | `GET /api/users/{user}/companies`, `PUT /api/users/{user}/companies` | Admin y destino contador; `{company_ids:[]}`; `200`/`204`. |
| Listar/crear empresas | `GET /api/companies`, `POST /api/companies` | Usuario habilitado para listar; solo admin crea con `{rfc,legal_name,commercial_name,tax_regime_code}`; `200`/`201`. El alta nueva integra la copia atómica de SPEC-003. |
| Consultar empresa | `GET /api/companies/{company}` | Admin o contador asignado; `200`/`404`. El recurso de empresa incluye `commercial_name`, `taxpayer_type` y `account_template_version`. |
| Consultar regímenes | `GET /api/tax-regimes` | Usuario habilitado; `200`. |

Recursos y listas se envuelven en `data`. Las listas se ordenan por nombre y luego ID. Errores observables: `401` sin autenticación o credenciales incorrectas, `403` sin permiso o con cambio pendiente, `404` para empresa inaccesible/inexistente, `419` para CSRF, `422` para validación y `429` para límite de ingreso. Asignaciones y restablecimientos dirigidos a un administrador se rechazan en backend.

## Plan de implementación

- Preparar una revisión Git de esta documentación antes del código y referenciarla desde ambos repositorios.
- Crear migraciones, modelos, enum de roles, catálogo fiscal, requests, resources, policies, middleware, controladores, rutas y comando `app:admin` en el backend. Para CA-001-18/19, agregar la transición compatible de nombre comercial, derivar el tipo desde el RFC normalizado y coordinar la transacción de alta con SPEC-003.
- Crear cliente HTTP con credenciales/CSRF, guardas de navegación y pantallas de acceso, cambio de contraseña, empresas y administración de contadores en el frontend. Para CA-001-17, reutilizar el estado de sesión vigente al decidir el destino de `/`; para CA-001-18/19, mostrar tipo de persona durante el alta y nombre comercial como información secundaria.
- Mantener secretos fuera de Git e incluir `.env.example`, Docker/Sail e instrucciones reproducibles.

### Pruebas previstas para la actualización

- Backend: validar obligatoriedad, recorte, longitud y ausencia de unicidad del nombre comercial; comprobar normalización del RFC, derivación de `taxpayer_type`, recursos nuevos y transición compatible de empresas existentes. La copia exacta y atómica del catálogo se prueba con SPEC-003.
- Frontend: con Vitest y React Testing Library, comprobar el tipo de persona durante el alta y la presentación secundaria del nombre comercial sin sustituir la razón social.
- QA humana: validar jerarquía visual de razón social/nombre comercial y legibilidad del tipo derivado.

## Verificación

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

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado.
- **2026-09-07:** alcance, contratos, entorno y criterios completados por instrucción explícita del usuario; SPEC-001 pasa a Lista. Se preservan los criterios CA-001-01 a CA-001-07 y se agregan CA-001-08 a CA-001-16.
- **2026-09-07:** backend y frontend implementados en `codex/spec-001`; comprobaciones técnicas registradas.
- **2026-09-10:** se reclasificó como QA conforme a DP-004; sólo resta validación visual humana del recorrido preparado.
- **2026-09-12:** se preparó CA-001-17 para que la ruta raíz resuelva directamente el destino según la sesión, sin transición intermedia por `/companies`; vuelve a Actualización pendiente. No se modificó código ni se registró evidencia técnica nueva.
- **2026-09-12:** se implementó CA-001-17 en el frontend con resolución por `GET /api/me` y navegación de reemplazo. Se ejecutaron lint, typecheck, build y revisión de diff. No se ejecutaron ni exigieron pruebas integrales de interfaz por navegador para ese cierre; DT-012 aplica prospectivamente y no invalida esta evidencia histórica.
- **2026-09-12:** revisión documental de SPEC-001: criterios, contexto de ejecución, dependencias, contratos y recorrido de QA coherentes; se entrega a QA mediante el MR [front #4](https://github.com/eduvzb/sistema-contable-front/pull/4).
- **2026-09-12:** tras revisar la integración de #4 sobre `main` con #5 ya fusionado, se restablece el script `pnpm test` mediante el PR correctivo [front #6](https://github.com/eduvzb/sistema-contable-front/pull/6), para conservar la ejecución reproducible de Vitest. Pasaron `pnpm test` (1 archivo, 3 pruebas), `pnpm lint`, `pnpm typecheck`, `pnpm build` y `git diff --check`. No modifica el comportamiento de CA-001-17 ni incorpora pruebas integrales por navegador.
- **2026-09-12:** se prepararon CA-001-18/19 para nombre comercial obligatorio, tipo de persona derivado y ampliación del recurso de empresa; la integración atómica de `GENERAL_V1` se remite a SPEC-003. La spec vuelve a Actualización pendiente sin cambios de código ni pruebas de producto nuevas.
