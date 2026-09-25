# SPEC-001 — Acceso, usuarios y empresas

- **Estado:** Actualización pendiente
- **Actualizado:** 2026-09-24 (migración documental; sin cambio de estado)
- **Criterios de esta entrega:** CA-001-18 y CA-001-19 (ampliación del contrato de empresa)
- **Usuario:** Administrador y contador
- **Dependencias:** Ninguna funcionalidad previa; decisiones compartidas DT-001 a DT-009.

## Contexto y objetivo

Permitir que un administrador inicial creado desde consola gestione empresas, contadores y sus asignaciones; permitir que ambos roles inicien sesión y consulten únicamente el alcance autorizado. El administrador tiene acceso operativo a todas las empresas. El contador accede solo a las asignadas.

Incluye autenticación, cambio obligatorio de contraseña temporal, alta y consulta de empresas, alta y consulta de contadores, restablecimiento de contraseñas y reemplazo de asignaciones. Los datos de empresa incluyen RFC, razón social, nombre comercial, tipo de persona derivado, régimen fiscal y versión de plantilla de cuentas. Empresa/ejercicio/periodo, XML y operaciones contables corresponden a las specs siguientes; la copia del catálogo inicial se concreta en SPEC-003.

## Historias de usuario

- H-001-01: Como administrador quiero crear empresas y contadores y gestionar sus asignaciones, para habilitar el trabajo autorizado.
- H-001-02: Como contador quiero iniciar sesión y consultar únicamente mis empresas, para operar dentro de mis permisos.

## Requisitos funcionales y criterios de aceptación

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
| CA-001-18 | CUANDO el administrador crea una empresa con nombre comercial válido, o SI lo omite, envía sólo espacios o supera 255 caracteres. | EL SISTEMA recorta y conserva el valor válido sin exigir unicidad; para los casos inválidos responde `422` sin dejar empresa ni catálogo parcial. La interfaz presenta la razón social como nombre principal y el nombre comercial como dato secundario. |
| CA-001-19 | CUANDO se captura un RFC estructuralmente válido de 12 o 13 caracteres durante el alta, o se consulta una empresa nueva o existente. | EL SISTEMA muestra en interfaz y recurso `PERSONA_MORAL` o `PERSONA_FISICA`, respectivamente, calculado a partir del RFC normalizado, sin persistirlo ni filtrar regímenes. El recurso incluye `commercial_name` y `account_template_version`; las empresas existentes exponen nombre comercial igual a razón social y versión `null`. |

## Requisitos no funcionales aplicables

- Autenticación, autorización, aislamiento y protección de credenciales: CA-001-02/05/06/08/10/11/14 y DT-007/008/009.
- Interfaz en español, semántica y accesible, con estados de carga, vacío y error y validación junto a campos; la presentación concreta se describe en [plan.md](plan.md).

## Casos límite

- Credenciales inválidas, duplicados, datos incompletos, RFC y régimen inválidos, asignaciones ajenas o repetidas: CA-001-02/12/13/18/19.

## Fuera de alcance

Quedan fuera registro público, invitaciones por correo, edición de perfiles, bajas, creación de otros administradores desde la interfaz, roles adicionales, límites comerciales y administración de múltiples despachos.

No incluye dashboard contable.

## Decisiones, supuestos y dudas

### Decisiones locales

- El volumen inicial usa listas completas, ordenadas por nombre y después ID, sin paginación.
- La comprobación de RFC es estructural, no prueba existencia, vigencia ni situación fiscal. El régimen almacenado debe pertenecer al catálogo versionado, pero no se limita por tipo de persona en esta spec.
- La razón social es el identificador visible principal de la empresa. El nombre comercial es obligatorio, secundario y no único. El tipo de persona se muestra como dato calculado y nunca como campo editable.
- La compatibilidad de datos existentes fija nombre comercial igual a razón social y versión de plantilla `null`; no ejecuta una carga retroactiva del catálogo. SPEC-003 define la copia `GENERAL_V1` para altas nuevas y su transacción compartida.
- La ruta raíz es un punto de entrada neutral: su destino depende del estado de acceso y se resuelve sin encadenar rutas protegidas. No se introduce una página inicial nueva.

## Criterios de finalización

- Los criterios de esta entrega deben tener implementación y comprobación técnica registradas en [verificación](verificacion.md) antes de pasar a QA.
- Sólo la aprobación humana de QA registrada permite pasar a Implementada, conforme al [flujo SDD](../../docs/flujo-spec.md).

## Fuentes

- [Alcance §3: actores](../../docs/planeacion/003%20-%20MVP-Scope.md#3-usuarios-incluidos); [§4: empresas](../../docs/planeacion/003%20-%20MVP-Scope.md#4-empresas); [§18: inicio del recorrido](../../docs/planeacion/003%20-%20MVP-Scope.md#18-flujo-completo-que-debe-demostrar-el-mvp).
- [Análisis §5: administrador y contador](../../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#5-actores-del-sistema) y [OQ-011](../../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#13-oq-011--organization-expl%C3%ADcita) (un despacho como supuesto provisional; Organization no es obligatoria).
- [BR-001](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa) (aislamiento confirmado).
- [BR-021](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#23-br-021--la-empresa-conserva-nombre-comercial-y-tipo-de-persona-derivado) y [BR-022](../../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#24-br-022--cada-empresa-nueva-recibe-una-copia-independiente-de-la-plantilla-general) (identidad comercial, derivación del tipo e integración con el catálogo inicial).
- [Análisis §6: datos de empresa](../../docs/planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md#6-empresas), limitado a los datos fiscales incluidos por el alcance del MVP.
- [Catálogo CFDI 4.0 del SAT](https://www.sat.gob.mx/minisitio/Factura/emite_quenecesitoparafacturar.htm), del que se conserva una copia versionada de `c_RegimenFiscal` en el backend.
