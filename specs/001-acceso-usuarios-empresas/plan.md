# Plan técnico — SPEC-001

Este archivo describe la ejecución técnica de [SPEC-001](spec.md); los criterios funcionales vigentes y el estado sólo se definen allí.

## Contexto para ejecución

El alcance y los criterios de esta entrega están en [spec.md](spec.md); las tareas abiertas por repositorio identifican el trabajo pendiente. Consulta los contratos de las specs dependientes que esta ejecución consume. Las fuentes ya citadas en `spec.md` se reabren sólo ante una contradicción, un cambio posterior de regla o contrato, un supuesto que afecte el resultado, o una solicitud explícita de cambiar comportamiento.

## Antecedentes de diseño

### Análisis de hallazgo 2026-09-12

| Hallazgo | Comportamiento actual que falla | Comportamiento esperado | Impacto documental | Componentes |
|---|---|---|---|---|
| La ruta raíz pasa por `/companies` antes de `/login`. | `/` envía incondicionalmente a `/companies`; esa pantalla consulta la sesión y sólo después redirige a `/login`, produciendo una transición protegida innecesaria. | La ruta raíz decide el destino a partir del estado de acceso y reemplaza la navegación una sola vez según CA-001-17. | Se agrega CA-001-17 y una decisión local; no cambia el contrato de autenticación ni requiere una decisión compartida. | Frontend. El backend conserva `GET /api/me` y sus respuestas vigentes. |

## Entorno y arquitectura

- Backend: Laravel 13, PHP 8.4, Sanctum y PostgreSQL 18 en Docker mediante Sail. Servicios mínimos: aplicación y PostgreSQL.
- Frontend: Next.js 16, TypeScript, App Router, Tailwind CSS y pnpm sobre Node 22. Los bloqueos fijan las versiones instaladas.
- Bases: `sistema_contable` para desarrollo y `testing` para pruebas, con volumen persistente. La suite rechaza ejecutar pruebas destructivas si la base activa no es `testing`.
- Direcciones locales: frontend `http://localhost:3000`, API `http://localhost:8000` y PostgreSQL expuesto solo en `127.0.0.1:54329`.
- Backend y frontend usan el mismo ID y revisión real de la spec; cada tarea nueva sigue la convención de ramas vigente en DP-005. La rama `codex/spec-001` pertenece a la entrega histórica registrada en [verificación](verificacion.md).

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

## Arquitectura existente y actualización pendiente

- Referenciar desde ambos repositorios una revisión Git real de la documentación cuando exista; el repositorio de specs no requiere un commit de implementación propio.
- El backend existente comprende migraciones, modelos, enum de roles, catálogo fiscal, requests, resources, policies, middleware, controladores, rutas y comando `app:admin`. Para CA-001-18/19, agregar la transición compatible de nombre comercial, derivar el tipo desde el RFC normalizado y coordinar la transacción de alta con SPEC-003.
- El frontend existente comprende cliente HTTP con credenciales/CSRF, guardas de navegación y pantallas de acceso, cambio de contraseña, empresas y administración de contadores. CA-001-17 ya resolvió la ruta `/`; para CA-001-18/19, mostrar tipo de persona durante el alta y nombre comercial como información secundaria.
- Mantener secretos fuera de Git e incluir `.env.example`, Docker/Sail e instrucciones reproducibles.

### Pruebas previstas para la actualización

- Backend: validar obligatoriedad, recorte, longitud y ausencia de unicidad del nombre comercial; comprobar normalización del RFC, derivación de `taxpayer_type`, recursos nuevos y transición compatible de empresas existentes. La copia exacta y atómica del catálogo se prueba con SPEC-003.
- Frontend: con Vitest y React Testing Library, comprobar el tipo de persona durante el alta y la presentación secundaria del nombre comercial sin sustituir la razón social.
- QA humana: validar jerarquía visual de razón social/nombre comercial y legibilidad del tipo derivado.

## Decisiones técnicas conservadas

- `users` conserva nombre, correo único, hash, rol y `must_change_password`; `companies`, RFC único, razón social, nombre comercial, código de régimen y versión nullable de plantilla; `company_user`, claves foráneas y unicidad usuario–empresa. `taxpayer_type` no se persiste.
- Se usan Eloquent, Form Requests, Policies y API Resources, sin paquetes de roles ni capa de repositorios.
- Sesiones y limitación de intentos se respaldan en PostgreSQL mediante capacidades de Laravel. El guardado de asignaciones y la invalidación de sesiones son transaccionales.
- La interfaz es en español, semántica y accesible, con estados de carga, vacío y error, validación junto a campos, paleta neutra y acento índigo. No incluye dashboard contable.

## Orden y coordinación

Las tareas pendientes se registran por repositorio en [backend](tasks-backend.md) y [frontend](tasks-frontend.md). El contrato responsable se prepara antes de implementarlo en un consumidor; las comprobaciones reales se registran en [verificación](verificacion.md).
