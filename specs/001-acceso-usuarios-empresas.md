# SPEC-001 — Acceso, usuarios y empresas

**Estado:** Lista  
**Usuario:** Administrador y contador  
**Dependencias:** Ninguna funcionalidad previa; decisiones compartidas DT-001 a DT-009.

## Propósito y alcance

Permitir que un administrador inicial creado desde consola gestione empresas, contadores y sus asignaciones; permitir que ambos roles inicien sesión y consulten únicamente el alcance autorizado. El administrador tiene acceso operativo a todas las empresas. El contador accede solo a las asignadas.

Incluye autenticación, cambio obligatorio de contraseña temporal, alta y consulta de empresas, alta y consulta de contadores, restablecimiento de contraseñas y reemplazo de asignaciones. Los datos fiscales de empresa se limitan a RFC, razón social y un régimen fiscal. Empresa/ejercicio/periodo, XML y operaciones contables corresponden a las specs siguientes.

Quedan fuera registro público, invitaciones por correo, edición de perfiles, bajas, creación de otros administradores desde la interfaz, roles adicionales, límites comerciales y administración de múltiples despachos.

## Fuentes

- [Alcance §3: actores](../docs/planeacion/003%20-%20MVP-Scope.md#3-usuarios-incluidos); [§4: empresas](../docs/planeacion/003%20-%20MVP-Scope.md#4-empresas); [§18: inicio del recorrido](../docs/planeacion/003%20-%20MVP-Scope.md#18-flujo-completo-que-debe-demostrar-el-mvp).
- [Análisis §5: administrador y contador](../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#5-actores-del-sistema) y [OQ-011](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#13-oq-011--organization-expl%C3%ADcita) (un despacho como supuesto provisional; Organization no es obligatoria).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa) (aislamiento confirmado).
- [Análisis §6: datos de empresa](../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#6-empresas), limitado a los datos fiscales incluidos por el alcance del MVP.
- [Catálogo CFDI 4.0 del SAT](https://www.sat.gob.mx/minisitio/Factura/emite_quenecesitoparafacturar.htm), del que se conserva una copia versionada de `c_RegimenFiscal` en el backend.

## Comportamiento y criterios de aceptación

El acceso usa correo y contraseña. Nombre y correo son obligatorios; el correo se normaliza a minúsculas sin espacios exteriores y es único. Hay dos roles fijos: `admin` y `accountant`.

El comando interactivo `app:admin` crea el primer administrador con contraseña oculta. Si existe un administrador, no crea otro; `--reset-password` permite restablecer su contraseña. Desde la interfaz, el administrador crea exclusivamente contadores. El backend genera las contraseñas temporales aleatorias y solo las devuelve en la respuesta de creación o restablecimiento; nunca se conservan en texto plano.

Un contador con contraseña temporal debe cambiarla antes de consultar empresas u operar. Mientras tanto solo puede consultar su identidad, cambiar su contraseña y cerrar sesión. El cambio exige contraseña actual, nueva contraseña y confirmación; la nueva contraseña tiene entre 12 y 128 caracteres. Las contraseñas se almacenan con Argon2id. El restablecimiento invalida sesiones existentes y vuelve a exigir el cambio inicial.

Una empresa tiene RFC único, razón social y un régimen fiscal. El RFC se normaliza a mayúsculas sin espacios exteriores y debe cumplir una comprobación estructural básica de 12 o 13 caracteres; no se consulta su situación ante SAT. La razón social es obligatoria y admite hasta 255 caracteres. El régimen se elige por código y nombre desde la copia versionada del catálogo `c_RegimenFiscal`; el backend valida que exista en ella y conserva procedencia y fecha del catálogo.

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

## Decisiones locales

- El volumen inicial usa listas completas, ordenadas por nombre y después ID, sin paginación.
- `users` conserva nombre, correo único, hash, rol y `must_change_password`; `companies`, RFC único, razón social y código de régimen; `company_user`, claves foráneas y unicidad usuario–empresa.
- Se usan Eloquent, Form Requests, Policies y API Resources, sin paquetes de roles ni capa de repositorios.
- Sesiones y limitación de intentos se respaldan en PostgreSQL mediante capacidades de Laravel. El guardado de asignaciones y la invalidación de sesiones son transaccionales.
- La interfaz es en español, semántica y accesible, con estados de carga, vacío y error, validación junto a campos, paleta neutra y acento índigo. No incluye dashboard contable.
- La comprobación de RFC es estructural, no prueba existencia, vigencia ni situación fiscal. El régimen almacenado debe pertenecer al catálogo versionado, pero no se limita por tipo de persona en esta spec.

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
| Listar/crear empresas | `GET /api/companies`, `POST /api/companies` | Usuario habilitado para listar; solo admin crea con `{rfc,legal_name,tax_regime_code}`; `200`/`201`. |
| Consultar empresa | `GET /api/companies/{company}` | Admin o contador asignado; `200`/`404`. |
| Consultar regímenes | `GET /api/tax-regimes` | Usuario habilitado; `200`. |

Recursos y listas se envuelven en `data`. Las listas se ordenan por nombre y luego ID. Errores observables: `401` sin autenticación o credenciales incorrectas, `403` sin permiso o con cambio pendiente, `404` para empresa inaccesible/inexistente, `419` para CSRF, `422` para validación y `429` para límite de ingreso. Asignaciones y restablecimientos dirigidos a un administrador se rechazan en backend.

## Plan de implementación

- Preparar una revisión Git de esta documentación antes del código y referenciarla desde ambos repositorios.
- Crear migraciones, modelos, enum de roles, catálogo fiscal, requests, resources, policies, middleware, controladores, rutas y comando `app:admin` en el backend.
- Crear cliente HTTP con credenciales/CSRF, guardas de navegación y pantallas de acceso, cambio de contraseña, empresas y administración de contadores en el frontend.
- Mantener secretos fuera de Git e incluir `.env.example`, Docker/Sail e instrucciones reproducibles.

## Verificación prevista

Pruebas Laravel sobre PostgreSQL `testing`:

- acceso válido/inválido, salida, CSRF y limitación;
- cambio obligatorio, contraseña actual incorrecta y restablecimiento con invalidación de sesiones;
- normalización y duplicados de correo/RFC, campos inválidos y régimen inexistente;
- acceso global del administrador y aislamiento del contador mediante listados y peticiones directas;
- duplicados, retirada y atomicidad de asignaciones; contador sin empresas;
- ausencia de hashes y contraseñas temporales en consultas posteriores;
- creación/recuperación del primer administrador mediante comando.

Playwright cubre administrador → empresa → contador → asignación → cambio de contraseña → consulta → retirada de acceso, usando datos y base de pruebas. Además se ejecutan formato y pruebas del backend, lint, comprobación TypeScript, pruebas y build de producción del frontend.

**Evidencia de producto:** pendiente hasta completar los dos repositorios y ejecutar las comprobaciones. No cambiar a Implementada antes de registrar aquí comandos, resultados, revisión de spec y revisiones de backend/frontend.

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado.
- **2026-09-07:** alcance, contratos, entorno y criterios completados por instrucción explícita del usuario; SPEC-001 pasa a Lista. Se preservan los criterios CA-001-01 a CA-001-07 y se agregan CA-001-08 a CA-001-16.
