# Verificación — SPEC-012

## Actualización documental: reemplazo de FIEL para usuarios reales

- [ ] Validar integración del reemplazo desde edición de empresa para administrador y contador asignado, sin permitir modificar RFC.
- [ ] Verificar autorización/evidencia del titular, almacenamiento productivo, control de claves, reemplazo atómico, coordinación con trabajos activos, respaldos y recuperación conforme a la política aprobada.
- [ ] Ejecutar pruebas automatizadas de roles, errores, integridad y secretos; revisar operación productiva por separado. No se ejecutaron pruebas de producto ni despliegue en esta actualización documental.
- El usuario confirma que existe aprobación fiscal/legal y autorización de titulares para la custodia de empresas cliente. Esta confirmación no acredita controles técnicos ni habilitación de producción.

## Entrega actual: FIEL guardada desde Crear empresa, sólo local

### Incidencia en primera ejecución de empresa propia

- La ejecución #3 de la empresa 2 quedó `INTERRUPTED/LOCAL_PROCESS` antes de la primera consulta. Inspección local de estados: las seis combinaciones permanecen `PENDING`, sin identificadores SAT, estado SAT ni trabajos pendientes. No se reanudó ni se envió otra solicitud.
- Causa: el worker de larga vida se inició antes de configurar `SAT_LOCAL_SAVED_ENABLED` y la clave local. Conservó la configuración anterior, `enabled()` falló antes de construir la FIEL o llamar al gateway, y el catch guardó sólo el mensaje genérico. La configuración actual y el worker recién iniciado ya tienen habilitado el piloto local.
- La pantalla seguía haciendo GET de historial cada dos segundos aunque el proceso estaba interrumpido. El hook ahora sólo sondea mientras algún proceso esté `QUEUED`, `RUNNING`, `WAITING_SAT` o `STOPPING`; se añadió prueba de regresión.
- La prueba que ya inició el usuario se puede reanudar manualmente desde el botón del proceso #3: sus consultas siguen `PENDING`, así que el runner no necesita reenviar ningún identificador conocido. La acción de reanudar sí puede iniciar comunicaciones SAT; el agente no la ejecutó. No hace falta crear otro proceso.
- Tras la segunda reanudación, #3 volvió a interrumpirse con las seis consultas `PENDING`, sin ID SAT ni jobs pendientes. Verificación local sin red con `tinker`: la clave local descifra los datos guardados y `Fiel::create` valida vigencia/RFC/llave (`gateway()`), por lo que el bloqueo ocurre después de cargar la FIEL, probablemente en autenticación SAT. No se inspeccionaron ni imprimieron secretos ni se repitió la comunicación.
- Se ajustó el error para distinguir fallo de autenticación y dejar explícito que la consulta no se envió; se conserva texto seguro sin excepción previa. El worker se reinició para cargar la mejora. Prueba feature añadida para asegurar mensaje seguro, estado `PENDING`, ningún ID y cero llamadas a `query`; resultado de la prueba acotada pendiente de registrar.

- [x] Carga opcional de certificado, llave y contraseña en el formulario existente, con aviso y confirmación de empresa propia; multipart sin persistencia de secretos en navegador. Crear sin FIEL sigue disponible.
- [x] Backend: validación criptográfica de FIEL/RFC/llave/contraseña y límite de 64 KiB; empresa/catálogo/credencial atómicos. Certificado, llave y contraseña cifrados con AES-256-GCM y clave dedicada local. API sólo informa presencia; cola sólo recibe identificadores/generación/paso.
- [x] Modo `REAL_SAVED` con seguimiento en cola local, inicio/reanudación explícitos e idempotentes, exclusión empresarial y recuperación sin repetir envíos inciertos. Retiro reservado al administrador, serializado con la unidad viva, invalida trabajos pendientes y conserva historial/XML. Eventos de carga/retiro registran actor/fecha/consentimiento sin secretos.
- [x] Tipos, ESLint de los archivos afectados, Prettier y `php vendor/bin/pint --dirty --format agent`, aprobados. Para formularios con archivos en jsdom se envía el evento submit tras seleccionar archivos/consentimiento; se comprueban el payload exacto y los errores de la aplicación, sin atribuir validación nativa de navegador.
- [x] Frontend completo sobre el árbol final: `node node_modules/vitest/vitest.mjs run --maxWorkers=1 --testTimeout=15000`: **122 pruebas aprobadas en 19 archivos**. `node node_modules/next/dist/bin/next build --webpack`: aprobado, Next.js 16.3.4, con tipos comprobados.
- [x] Backend completo sobre el árbol final, incluidos eventos de auditoría: `./vendor/bin/sail artisan test --compact` mediante Ubuntu, **176 pruebas y 1 583 aserciones aprobadas**. Base `testing` separada y pruebas de concurrencia en bases efímeras propias del conjunto de pruebas; no se vació la base de aplicación ni se usaron datos fiscales reales.
- [x] Migración `2026_10_28_234005_create_sat_local_credentials_table` aplicada sólo en `spec012_local`. Generada clave dedicada aleatoria sin imprimirla, guardada en `.env` local ignorado por Git, sin rotar claves existentes. `SAT_LOCAL_SAVED_ENABLED=true`, depuración deshabilitada y caché de configuración limpiada. No se habilita producción ni el VPS.
- [x] Nuevo build iniciado en el puerto 3012; `/login` y backend `/up` responden HTTP 200. Ruta `api/company-creation-capabilities` presente y `sat-downloads.saved_local.enabled=true` comprobados mediante Artisan sin imprimir la clave. Worker `sat-real-local` iniciado con un intento, timeout 240 s y memoria 256 MiB; conexión dedicada con reserva 300 s, proceso comprobado. La cola real local estaba vacía antes de iniciarlo. No se aportó ni leyó FIEL real, ni se inició comunicación SAT por parte del agente.
- [ ] Prueba humana del usuario con su empresa propia; no hay aprobación ni comunicación SAT real acreditadas. Publicación/PR y custodia de clientes siguen fuera de esta entrega local.
- [x] Validación documental: 12 specs y enlaces locales comprobados con `python3 scripts/spec_index.py --check`. Sin cambio del estado completo ni del índice. Los nuevos trabajos técnicos BE-012-12/FE-012-10 se retiran tras acreditar sus condiciones; se mantienen las tareas completas aún pendientes y los cambios ajenos de SPEC-011/004/005.

### Cómo probar desde la interfaz

1. Entrar en <http://localhost:3012/login> con el usuario administrador. Abrir **Nueva empresa** y capturar el RFC real, razón social, nombre comercial y régimen de la empresa propia. No cambiar la empresa ficticia existente.
2. Activar **Guardar FIEL de mi empresa en esta computadora (opcional)**. Elegir `.cer` y `.key` desde su carpeta privada externa e introducir la contraseña en el campo oculto. Leer y confirmar el aviso local. No adjuntar archivos o contraseña al chat. **Crear empresa** valida y guarda; no envía solicitudes al SAT. Un error de FIEL impide guardar la empresa para poder corregir el formulario.
3. Crear/seleccionar el ejercicio y un periodo no futuro. En **Documentos fiscales → Descarga SAT · piloto local**, dejar **Real SAT · FIEL guardada local**, elegir inicialmente un solo día con pocos documentos y un tipo/dirección. Confirmar la solicitud real y pulsar **Iniciar descarga real SAT**. No elegir el modo ficticio en la empresa real por accidente.
4. El seguimiento continúa mientras Docker y el worker estén funcionando, aunque se cierre la pantalla. SAT puede tardar; se verifica cada cinco minutos. Los XML, paquetes e historial quedan privados en el backend local, sin descarga de originales al equipo. Detener no cancela la solicitud SAT. Reanudar es manual y no reenvía solicitudes inciertas.
5. Para retirar la credencial, confirmar **Retirar FIEL local** en el panel. Si una unidad está viva, detener y repetir cuando termine. Se elimina la copia cifrada activa de certificado/llave/contraseña, no los archivos fuente, XML, historial, eventos ni posibles respaldos. Esta entrega no incorpora recarga/reemplazo en empresas ya creadas: no retirar sólo para probar si se necesita seguir descargando.

La clave dedicada reside en el `.env` local de este worktree: no se publica ni debe compartirse. Perderla impide descifrar la FIEL guardada. El cifrado no protege una computadora comprometida ni separa físicamente las claves de sus datos; proteger equipo y copias sigue siendo responsabilidad del titular. No hay prueba de respaldo/recuperación, dictamen jurídico de custodia de clientes ni seguridad de producción acreditados.

Si se reinicia la computadora, levantar Docker/Sail y frontend como se indica abajo; el worker de esta variante se inicia desde `spec012-back` en Ubuntu:

```sh
./vendor/bin/sail artisan queue:work sat-real-local --queue=sat-real-local --tries=1 --timeout=240 --memory=256
```

## Antecedente: piloto real local con FIEL temporal

- [x] Instalación autorizada de `phpcfdi/sat-ws-descarga-masiva` v1.1.4 y cuatro dependencias nuevas, sin actualizar/eliminar las existentes. Composer falló inicialmente por permisos del vendor copiado; el catálogo quedó instalado y `composer dump-autoload --no-scripts --no-interaction` terminó correctamente (7 432 clases). Sólo en `spec012-back`.
- [x] Comando `sat-downloads:local`: sólo local, bandera explícita y terminal interactiva; contraseñas ocultas, archivos bajo `/run/fiel`, comprobación de FIEL vigente/RFC, confirmación previa y credenciales fuera de base de datos/cola. No se ha ejecutado con FIEL del usuario.
- [x] Pruebas iniciales de transporte fijo sin reintentos/redirects, respuesta acotada y errores sin cadena con secretos; ZIP privado sin extracción, rutas peligrosas/enlaces/límites rechazados. Cola controlada ignora procesos reales incluso en callback de fallo.
- [x] Primera ejecución de las suites afectadas: 28 pruebas y 217 aserciones aprobadas; comprueba solicitud/identificador, importación parcial, recuperación manual, pérdida de permiso, exclusión del proceso vivo y respuesta tardía tras STOPPING. Se amplía cobertura de bloques/espacio/códigos SAT antes de la regresión final.
- [x] Regresiones finales: backend 164 pruebas y 1 474 aserciones; frontend 115 pruebas en 18 archivos. Formato, tipos, lint y build aprobados; migración local aplicada y comando/guía comprobados sin comunicaciones SAT reales.
- [ ] Prueba humana real a cargo del usuario. Sin comunicaciones SAT ni lectura de archivos FIEL reales por el agente. Aprobación anterior sólo cubre fixtures.
- [ ] Publicación/PR, custodia de clientes, capacidad/respaldo productivo y despliegue al VPS: fuera de esta entrega local y no acreditados.

### Comprobaciones al retomar

- Docker Desktop iniciado por petición del usuario. `./vendor/bin/sail up -d --no-build` mediante Ubuntu levanta únicamente el proyecto `spec012`: aplicación en loopback 8012 y PostgreSQL saludable en 54332. Frontend iniciado en loopback 3012; `/login` y backend `/up` responden HTTP 200. Worker `sat-controlled` y `schedule:work` iniciados para el modo ficticio; el piloto real no los utiliza.
- `./vendor/bin/sail artisan migrate:status --no-interaction`: la migración `2026_10_28_184317_create_sat_local_packages_tables` ya figuraba aplicada, batch 2. `./vendor/bin/sail artisan migrate --no-interaction`: «Nothing to migrate», sin reiniciar ni vaciar bases.
- `./vendor/bin/sail artisan test --compact tests/Feature/SatLocalRunnerTest.php tests/Feature/SatLocalSafetyTest.php tests/Feature/Spec012Test.php`: **33 pruebas y 252 aserciones aprobadas**. Incluye los bloques de 50, recuperación de entradas confirmadas, falta de espacio y código SAT de límite sin éxito vacío aparente.
- `./vendor/bin/sail artisan test --compact`: **164 pruebas y 1 474 aserciones aprobadas**, exclusivamente con Sail y la base `testing` separada. No se suman las pruebas acotadas como casos adicionales.
- `./vendor/bin/sail artisan sat-downloads:local --help --no-interaction`: comando y opciones disponibles. Ejecución sin interacción rechazada antes de pedir credenciales o comunicar con SAT; también con `docker compose run --rm --no-deps -T -e SAT_LOCAL_REAL_ENABLED=true laravel.test php artisan sat-downloads:local 1 --no-interaction`. La bandera real permanece limitada al contenedor interactivo que iniciará el usuario; no hay caché de configuración local que la sustituya.
- `php vendor/bin/pint --dirty --format agent`: aprobado; corrigió el orden de imports de `SatLocalSafetyTest.php`. Ese ajuste y las ampliaciones de cobertura siguen pendientes de ejecución con Sail.
- Frontend: `node node_modules/vitest/vitest.mjs run --maxWorkers=1 --testTimeout=15000`: **115 pruebas aprobadas en 18 archivos**, incluida la distinción del proceso real, envío incierto y STOPPING sin reanudación web. `node node_modules/typescript/bin/tsc --noEmit`, Prettier y ESLint sobre los tres archivos modificados, y `node node_modules/next/dist/bin/next build --webpack`, aprobados (Next.js 16.3.4). Esta ejecución corresponde al piloto actual, no a la etapa anterior.
- `python3 scripts/spec_index.py --check` mediante Ubuntu: 12 specs y enlaces locales validados. `git diff --check` de ambos worktrees sin errores de espacios.
- Bloqueos de ejecución excluidos de Git mediante `storage/framework/.gitignore`; `git check-ignore storage/framework/sat-local-locks/987654.lock` confirma la exclusión sin borrar ni reemplazar el archivo de bloqueo.

### Cómo iniciar la prueba propia (después de completar los checks anteriores)

1. Crear en la aplicación local **otra empresa con su RFC real** y un periodo no futuro. No cambiar el RFC de la empresa ficticia ni reutilizar sus documentos. Identificar los IDs de empresa/periodo en sus rutas de navegación. El usuario de la aplicación debe ser administrador o contador actualmente asignado, sin cambio de contraseña pendiente.
2. Mantener `.cer` y `.key` en una carpeta privada **fuera del repositorio**. No adjuntarlos al chat ni poner contraseña en comandos, `.env` o archivos auxiliares. Asegurar permisos de la carpeta; este piloto no evalúa swap, volcados de memoria ni respaldos de la computadora.
3. Abrir una terminal WSL Ubuntu en `/mnt/c/proyecto-contable-corgor/spec012-back`. Con `spec012` iniciado y migrado, ejecutar el ejemplo siguiente, sustituyendo ruta e IDs por los propios. No ejecutarlo literalmente con los marcadores.

```sh
docker compose run --rm --no-deps \
  -e SAT_LOCAL_REAL_ENABLED=true \
  --volume '/mnt/c/RUTA-PRIVADA-FIEL:/run/fiel:ro' \
  laravel.test php artisan sat-downloads:local EMPRESA_ID \
  --period=PERIODO_ID --from=2026-10-01 --to=2026-10-01 \
  --direction=RECEIVED --types=I
```

Elegir inicialmente un día con pocos CFDI, dentro del periodo seleccionado. La bandera sólo vale para ese contenedor interactivo; no habilita la carga web ni el VPS. No usar `-T`, redirecciones, `--no-interaction`, depuración HTTP ni grabación de terminal. El contenedor no publica puertos adicionales ni requiere worker para esta descarga real.

4. Introducir correo/contraseña **de la aplicación**, comprobar RFC/selección y confirmar. Indicar después `/run/fiel/archivo.cer` y `/run/fiel/archivo.key`, e introducir contraseña FIEL sin eco. No se requiere contraseña por argumento ni variable de entorno.
5. Conservar el ID impreso. Mantener esta terminal abierta mientras se verifica cada cinco minutos; consultar el historial en **Documentos fiscales → Descarga SAT · pruebas**. Detener desde la web no cancela SAT y conserva `STOPPING` hasta terminar la unidad en curso. Ctrl+C termina el seguimiento local de forma manual conservando avances.
6. Para continuar tras detener/reiniciar, repetir el montaje y autenticación con `sat-downloads:local EMPRESA_ID --resume=PROCESO_ID`. Se exige volver a aportar FIEL; se reutilizan solicitudes y paquetes confirmados. Si hay envío incierto/rechazado, no se reenvía: queda interrumpido para revisión. No iniciar otra selección a ciegas.

Presupuesto aprobado: SOAP 16 MiB, ZIP 8 MiB, 100 MiB descomprimidos, 1 000 entradas, XML 10 MiB y 512 MiB libres mínimos. El comando acota memoria PHP a 256 MiB. Un límite o error interrumpe sin reintento automático; no aumentar límites sin revisar capacidad. Los ZIP/XML se guardan privados en el backend, no se ofrecen para descarga al equipo. El montaje de FIEL es sólo lectura y no elimina sus archivos fuente.

## Antecedente: primera etapa controlada ya aprobada

La evidencia y guía que siguen corresponden a la etapa anterior, no acreditan el piloto real ni describen la disponibilidad actual del nuevo comando.

Autorizada por el usuario para pruebas humanas, en worktrees separados de SPEC-011. **No es la implementación completa de la conexión SAT.** La spec completa permanece en Borrador; SPEC-004/005 siguen en Actualización pendiente. Hay aprobación humana de la etapa controlada, no cierre técnico ni aprobación de la funcionalidad real completa.

- [x] Código de backend y frontend aislado en `spec012-back` / `spec012-front`, rama `codex/feat/SPEC-012/controlled-downloads`, desde `origin/main` actualizado. Bases: backend `9ef673f`, frontend `8faf8c3`. No se trasladaron, descartaron ni incluyeron cambios locales de DIOT.
- [x] Inicio explícito de documentos ficticios sólo por administrador, con confirmación; aislamiento por empresa, selección de periodo/fechas/direcciones/tipos, idempotencia y una descarga activa por empresa.
- [x] Trabajo local persistente, historial/resultados, fallo sin reintento automático, detención por otro contador asignado y reanudación manual. Los trabajos obsoletos no incorporan documentos tras detener el proceso.
- [x] Importación parcial, duplicados sin reemplazo y originales privados sin ruta de descarga; comparación limitada de históricos sin rellenar campos, rechazo de esencial faltante y rollback del documento si falla el almacenamiento.
- [x] Tipos N/T consultables pero rechazados para nuevas relaciones/propuestas de partidas. No se integró ni alteró la entrega DIOT pendiente.
- [x] Conexión real y carga de e.firma ausentes; el driver controlado exige configuración explícita y entorno local/testing, y se comprueba su rechazo en producción incluso con la bandera activa. Pruebas sin comunicaciones HTTP externas.
- [x] Frontend: 114 pruebas en 18 archivos; tipos, lint de archivos afectados, formato y build aprobados, con las condiciones de ejecución indicadas abajo.
- [x] Backend: regresión completa con 146 pruebas y 1 342 aserciones; tras el último ajuste del callback de fallo tardío, SPEC-012 pasa nuevamente con 16 pruebas y 123 aserciones. No se suman ambas ejecuciones como si fueran casos distintos.
- [x] Entorno local separado preparado: migraciones aplicadas y empresa/usuarios ficticios creados; frontend `/login` y backend `/up` responden HTTP 200. Worker de la cola `sat-controlled` y coordinador local iniciados.
- [x] Commits locales de código: backend `15fae0e` (implementación en `d0e5e32` y cobertura adicional), frontend `fb42426`, ambos en `codex/feat/SPEC-012/controlled-downloads`; los `.env`, dependencias y artefactos de ejecución están excluidos. Ambos worktrees quedan limpios.
- [ ] Publicación, PR y revisión. No se publican ramas por cuenta propia en esta entrega local; `gh` tampoco está disponible en Windows ni en el PATH de WSL para verificar autenticación/gestionar PR. No hay PR ni revisión solicitada acreditados; no se declara el cierre técnico formal ni el estado QA.
- [x] Aprobación humana de la etapa controlada registrada el 2026-10-28: el usuario indicó «Ya realice las pruebas y todo bien». No comunicó observaciones. No se infieren recorridos concretos, versiones distintas ni comprobación de cada CA completo a partir de esa confirmación; no sustituye publicación/PR ni pruebas SAT reales.

## Alcance del piloto solicitado

- El usuario confirmó que la empresa es suya y que probará primero en su computadora; una eventual subida al VPS se revisará después, sin autorización de despliegue actual.
- Eligió FIEL temporal: otra ejecución o reiniciar el proceso que la utiliza requerirá volver a aportarla. Decisión incorporada a CA-012-25, sin cambiar las reglas de custodia permanente para clientes.
- Diseño/contratos/tareas locales preparados y autorizados en el plan. Los archivos y contraseñas reales no se han solicitado, leído ni utilizado; no se ejecutaron solicitudes SAT.
- `SatDownloadController::capabilities()` mantiene `real_enabled=false` y `credentials_enabled=false` para la creación/carga **web**. El nuevo comando crea `REAL_LOCAL`; las creaciones HTTP permanecen `CONTROLLED` sin fallback.

## Pruebas y comprobaciones técnicas

### Backend

- Entorno: Laravel Sail, PHP 8.4 y PostgreSQL 18, proyecto Compose `spec012`, base de pruebas `testing` en un volumen nuevo. No se probaron ni migraron bases del VPS ni del trabajo DIOT. `phpunit.xml` separa además los archivos de prueba de los originales de la aplicación local.
- `./vendor/bin/sail artisan test --compact tests/Feature/Spec012Test.php tests/Feature/Spec004Test.php tests/Feature/Spec005Test.php`: 27 pruebas y 250 aserciones aprobadas antes de ampliar la cobertura final.
- `./vendor/bin/sail artisan test --compact`: **146 pruebas y 1 342 aserciones aprobadas** tras corregir/probar el seeder local. Después se añadió la protección frente a un callback de fallo de un paso ya superado; `./vendor/bin/sail artisan test --compact tests/Feature/Spec012Test.php` vuelve a pasar sobre el árbol final: **16 pruebas y 123 aserciones**. No se atribuye una ejecución completa de 147 casos al último comando acotado.
- Tras reforzar el caso histórico existente con diferencia de total, `./vendor/bin/sail artisan test --compact tests/Feature/Spec012Test.php --filter=legacy_original_can_be_completed`: **1 prueba y 14 aserciones aprobadas**, comprobando rechazo por campo sin cambiar total ni guardar original incompatible. Sólo se amplió esa prueba, no el código de producto; no se suma como caso nuevo a las 16 anteriores.
- `php vendor/bin/pint --dirty --format agent`: ejecutado sobre los archivos de esta rama; ajustes de formato aplicados. Pint se ejecuta con PHP local, **las pruebas de aplicación se ejecutan exclusivamente con Sail**.
- Las expectativas históricas de descarte/duplicado en Spec004/005 se actualizaron a los criterios coordinados: originales privados y resultados `DUPLICATE` separados de los rechazos reales. No se eliminaron esos casos ni se relajaron sus comprobaciones funcionales.

### Frontend

- Se reutilizaron las dependencias locales instaladas; no se añadieron paquetes. Comandos ejecutados mediante Node porque `pnpm` no está en el PATH de esta sesión.
- `node node_modules/vitest/vitest.mjs run --maxWorkers=1 --testTimeout=15000`: **114 pruebas aprobadas en 18 archivos**. Las ejecuciones iniciales con el límite de cinco segundos agotaron tiempo en casos existentes de escritura larga y produjeron efectos tardíos entre pruebas; con el límite de ejecución de 15 segundos y un worker pasan las mismas aserciones, sin editar esos casos ni cambiar configuración del producto.
- `node node_modules/typescript/bin/tsc --noEmit`: aprobado; el build volvió a comprobar tipos.
- `node node_modules/eslint/bin/eslint.js <rutas afectadas>`: aprobado sin advertencias después de ajustar referencias de limpieza del hook.
- `node node_modules/prettier/bin/prettier.cjs --check <13 archivos afectados>`: aprobado.
- `node node_modules/next/dist/bin/next build --webpack`: aprobado, Next.js 16.3.4. No se acredita CI ni recorrido integral por navegador.

## Entorno para pruebas humanas

Ya iniciado en esta máquina, separado de DIOT:

- Interfaz: <http://localhost:3012/login>.
- Backend: <http://localhost:8012>; `/up` respondió HTTP 200.
- Empresa: **EMPRESA FICTICIA SPEC-012**, RFC de prueba `QAQ010101AAA`, doce meses del ejercicio actual.
- Administrador: `admin012@example.test`.
- Contador asignado: `contador012@example.test`.
- Contraseña inicial de ambas cuentas ficticias: `Pruebas012-Local!`. El seeder no restablece contraseñas al repetirse. Son cuentas de laboratorio, no credenciales fiscales ni cuentas para producción.

Entra en la empresa, selecciona un mes no futuro, abre **Documentos fiscales → Descarga SAT · pruebas**. Confirma la incorporación ficticia antes de iniciar. El resultado puede tardar varios pasos de dos segundos por consulta; ambas direcciones y cinco tipos crean diez consultas secuenciales.

Pruebas humanas sugeridas, sin exigir un recorrido integral:

1. Iniciar un caso válido, cerrar y volver a abrir el panel; comprobar historial, resultado y consulta de documentos.
2. Repetir la misma selección para ver duplicados, sin nuevos documentos ni reemplazo del original.
3. Probar «Válidos y rechazados», «Sin documentos» y «Fallo y reanudación manual»; distinguir resultado parcial, vacío e interrupción.
4. En «Espera prolongada controlada», comprobar el aviso simulado, detener y reanudar explícitamente para continuar. No se han esperado 24 horas reales ni se ha contactado al SAT.
5. Con el contador, comprobar que no puede iniciar simulaciones y que sí puede consultar/detener el proceso de su empresa. Revisar legibilidad, mensajes y presentación; comunicar observaciones antes de aprobar QA.

Si se detienen los procesos locales, iniciar desde los worktrees correspondientes (WSL para Sail):

```sh
# spec012-back, proyecto Compose spec012 configurado en su .env local
./vendor/bin/sail up -d --no-build
./vendor/bin/sail artisan queue:work database --queue=sat-controlled --tries=1 --timeout=30
# En otra terminal del mismo worktree:
./vendor/bin/sail artisan schedule:work
```

```powershell
# spec012-front, con el build ya generado
node node_modules/next/dist/bin/next start --hostname 127.0.0.1 --port 3012
```

Migraciones y `SatControlledQaSeeder` ya se ejecutaron en la base local separada. No ejecutarlos sobre otro proyecto/base para repetir esta prueba. No se han cargado XML fiscales reales ni e.firmas.

## Límites de la evidencia y pendientes reales

- El driver no descarga SOAP/ZIP: no acredita límites de paquetes, control de descompresión, cuotas SAT, incertidumbre de envíos externos, disponibilidad de 72 horas ni continuidad tras renovar certificados. Sus referencias y estados SAT son null; no se inventan identificadores.
- La comparación usa columnas originales, no el recurso HTTP que transforma null en lista vacía. Los campos nullable conocidos se prueban en esta base; no se atribuye procedencia a datos de una base externa ni se completa DIOT.
- Almacenamiento privado local comprobado no equivale a respaldos comprobados, limpieza de huérfanos o conservación de producción. La capacidad del VPS sigue sin definirse y el volumen de CFDI sigue desconocido.
- Sigue sin asesoría/dictamen jurídico de custodia. Ficha de capacidad, encargo jurídico, matriz SAT y contratos completos permanecen en [plan.md](plan.md); las fuentes y acuerdos funcionales permanecen en [spec.md](spec.md).
- La lectura del código/recursos y migraciones base, commits `5a59938`/`d841b59` y productores de prueba sustentó el contrato histórico; no se inspeccionaron bases reales. Los manuales SAT y la discrepancia comunitaria sobre ventana histórica no son una conexión real probada.

## Validación documental

- `python3 scripts/spec_index.py --check` desde el repositorio documental mediante WSL (Python 3.12.3): **12 specs y enlaces locales validados**. El bloqueo de Python del PATH de Windows no impide esta vía; no se instala software ni se regeneran estados sin necesidad.
- No se cambió el estado completo de SPEC-012 ni se editó el índice en esta implementación parcial. Se preservan SPEC-011 y los cambios documentales anteriores de SPEC-004/005.
- `git diff --check` documental y de código, incluidos los diffs staged revisados: sin errores de espacios; avisos de conversión LF/CRLF en archivos Markdown/TypeScript. SPEC-012 sigue sin seguimiento en Git documental; se comprueban sus archivos/enlaces mediante el validador, no sólo con el diff rastreado. Documentación sin commit, preservando los cambios previos del índice y SPEC-011.
- La publicación técnica y la QA humana no se consideran cerradas por pasar el validador documental. No se fusionaron ramas, no hubo despliegue y no se usaron credenciales fiscales reales.
