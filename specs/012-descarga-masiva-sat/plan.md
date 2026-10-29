# Plan técnico — SPEC-012

Plan para los criterios de [spec.md](spec.md). El usuario autorizó la etapa controlada y los pilotos locales para su empresa propia, incluida la FIEL guardada desde Crear empresa y la descarga web explícita, aislados de DIOT. La primera comunicación SAT real la inicia el usuario; no se autoriza al agente a utilizar su FIEL ni intervenir en el VPS.

El usuario autorizó preparar los puntos pendientes, incluidos los contratos técnicos. Las secciones «Contrato HTTP», «Persistencia y coordinación» y «Contrato del importador» definen la propuesta; no describen endpoints o tablas ya implementados. El usuario confirma aprobación fiscal/legal y autorización de titulares. Los archivos FIEL se guardarán cifrados en la carpeta privada de aplicación indicada en el contrato, con clave fuera del código; su implementación y pruebas siguen pendientes. Dimensionamiento y comprobaciones SAT de la funcionalidad completa siguen abiertos.

## Primera etapa controlada autorizada

- Worktrees separados `spec012-back` y `spec012-front`, rama `codex/feat/SPEC-012/controlled-downloads`, desde la base remota `main` comprobada mediante fetch y fast-forward. Los árboles originales de SPEC-011 permanecen intactos.
- El cliente ofrece «Descarga SAT · pruebas», con aviso y confirmación de documentos ficticios. Inicio y reanudación del driver controlado sólo por administrador, como corresponde a la simulación; acceso y detención por administrador/contador asignado. No se habilita el permiso de crear solicitudes **reales** del contador por fingir credenciales.
- `SAT_CONTROLLED_TESTS_ENABLED=false` por defecto. El driver requiere además `APP_ENV=local/testing`; incluso con la bandera activa no funciona en producción. `capabilities` expone `real_enabled=false` y `credentials_enabled=false`. No hay adaptador HTTP SAT ni endpoints para subir e.firmas en esta etapa.
- POST de prueba exige `mode=CONTROLLED`, `confirmed=true` y `scenario=SUCCESS/EMPTY/PARTIAL/ERROR/PROLONGED`, además de la selección e idempotencia del contrato. No hay fallback automático. Una petición `mode=REAL` se rechaza por validación, sin enviarla.
- Una consulta por dirección/tipo, persistida como JSON acotado a diez consultas en `sat_downloads`, sin identificadores ni estados SAT inventados (`sat_request_id`/`sat_status` son null). No se generan ZIP ni se acredita descarga/descompresión de paquetes reales. El driver prepara XML sintéticos y usa el importador común.
- Exclusión local: todas las creaciones, reanudaciones y pasos bloquean primero la misma fila de empresa y luego el proceso; se comprueba una única descarga activa. Los trabajos incluyen id/generación/paso y son descartados si quedaron obsoletos. Al no haber comunicación externa, el paso local corto se confirma bajo esa transacción; detener espera su final y devuelve STOPPED, sin fingir cancelación SAT. El contrato de slots/STOPPING y comunicaciones externas sigue siendo requisito de la etapa real, no algo probado con estos fixtures.
- Cola persistente `database`, cola nombrada `sat-controlled`, un intento por job, timeout local de 30 segundos y `retry_after` predeterminado superior. Los pasos de prueba usan dos segundos para observación humana; no sustituyen la cadencia SAT aprobada de cinco minutos. `sat-downloads:tick`, programado cada minuto, recupera trabajo local pendiente; nunca consulta SAT. La generación/paso y el bloqueo empresarial impiden reaplicar una unidad repetida.
- ERROR falla una vez sin reintento automático; reanudar explícitamente continúa. PROLONGED mantiene una espera marcada como **simulada** sin falsear timestamps; detener y reanudar libera esa espera del fixture. Esto no acredita el umbral de 24 horas ni la renovación de certificados del servicio real.
- Persistencia de esta etapa: `sat_downloads`, `sat_download_commands` y `sat_download_results`, más hash/tamaño del original en `fiscal_documents`. Historial de 25 y resultados de 50 por página. No crear aún tablas de paquetes, secretos o evidencia legal. El resumen controlado incluye `pending_query_count`, no una cantidad inventada de paquetes.
- Importador común: originales exactos en disco privado no servido por HTTP, resultados canónicos y duplicados sin reemplazo. La comparación histórica de los campos nullable conocidos se prueba contra esta base; no acredita procedencia de una base externa ni los campos de DIOT aún pendientes en SPEC-011. Una escritura de archivo no referenciada tras rollback queda como huérfana para limpieza futura; no se promete política de temporales/respaldos de producción.
- N/T admitidos para consulta general, bloqueados en nuevas relaciones/propuestas; la integración DIOT se mantiene fuera de estos worktrees. La simulación síncrona anterior también exige administrador y `confirmed=true`.
- Entorno local de QA separado: proyecto Compose `spec012`, nueva base/volumen, backend 8012 y frontend 3012 en loopback. No usar la base ni los contenedores del trabajo DIOT para probar o migrar esta etapa. El seeder de QA tiene guardia local y crea sólo identidades/empresa ficticias; no se ejecuta en producción.

Los contratos siguientes describen la funcionalidad completa. Las diferencias explícitas de esta sección sólo corresponden a la entrega parcial autorizada y no cierran los bloqueos reales.

## Piloto local temporal autorizado (CA-012-25)

El usuario autorizó diseño e implementación local, la dependencia `phpcfdi/sat-ws-descarga-masiva:1.1.4` y el presupuesto acotado siguiente. No autorizó al agente a ejecutar comunicaciones SAT reales ni intervenir en el VPS. Los contratos permanentes posteriores siguen fuera de este piloto.

- Entrada: comando interactivo local en Sail, con empresa, periodo, fechas, direcciones/tipos o identificador para reanudar. Autentica usuario de la aplicación mediante contraseña oculta y comprueba acceso actual a la empresa. La contraseña FIEL se solicita sin eco, nunca por argumento, variable de entorno, HTTP, tabla o cola. La carpeta fuente externa se monta sólo lectura; no se copian certificados ni llaves al repositorio. Sólo el proceso interactivo conserva la FIEL y token en memoria; terminar exige volver a aportarla. No se promete borrado físico de memoria, swap ni archivos fuente.
- Confirmación visible de empresa/RFC/selección antes de autenticar ante SAT. El comando no se ejecuta con secretos ni comunicaciones reales durante desarrollo. `APP_ENV=local` y bandera explícita separada; producción y carga web siguen bloqueadas.
- Exclusión: bloqueo de archivo por empresa durante toda la ejecución (sin caducidad), además de transacciones cortas que bloquean empresa y proceso. No se mantiene una transacción abierta durante comunicaciones SAT. Un proceso vivo impide reanudación/relevo; tras caída se exige recuperación manual. `STOPPING` conserva la reserva hasta finalizar la unidad en curso; perder permisos impide nuevas comunicaciones/importaciones.
- Intención de solicitud persistida antes de enviar. Si falta respuesta confirmada, queda incierta; nunca se reenvía automáticamente ni se sustituye por una simulación. Autenticación renovada al expirar token no reintenta la operación fallida. Verificación cada 300 segundos; conexión 10 segundos, autenticación/solicitud/verificación 60 segundos y descarga 180 segundos, TLS verificado, sin redirects ni reintentos HTTP, endpoints CFDI fijos. Hooks sin SOAP, tokens o registros de secretos.
- Presupuesto aprobado del piloto: respuesta SOAP hasta 16 MiB, ZIP hasta 8 MiB, total descomprimido hasta 100 MiB, hasta 1 000 entradas por paquete, XML hasta 10 MiB y mínimo 512 MiB libres en disco. Se comprueba tamaño anunciado y real; lectura limitada, sin `extractTo`, rutas relativas seguras, sin enlaces, entradas repetidas/cifradas ni archivos no XML. Un exceso interrumpe y no cuenta como éxito. No acredita capacidad VPS.
- Paquetes reales y resultados por entrada separados de los fixtures: identidad `(proceso, consulta, paquete)` y `(paquete, posición)`, hash y ruta privados; originales mediante importador común. Importar secuencialmente hasta 50 XML por bloque y persistir resultado junto con importación para no duplicar avances al reiniciar. Verificar RFC/dirección/tipo/fecha antes de incorporar; no afirmar vigencia por inspeccionar XML, sólo conservar el filtro de solicitud SAT.
- El coordinador y jobs controlados deben ignorar REAL_LOCAL incluso en callbacks de error. API de historial/resultados mantiene autorización vigente y distingue modo, estado SAT, incertidumbre y necesidad de proceso/FIEL local; no expone rutas/credenciales. La web observa y detiene; reanudación real únicamente en terminal aportando FIEL de nuevo. Pruebas con transporte falso, llaves ficticias, ZIP peligrosos, límites, autorización, bloqueo, caída y respuesta tardía; no usar secretos del usuario.

## Base comprobada y cambios necesarios

### Ampliación local autorizada: formulario Crear empresa y FIEL persistente

- Carga multipart opcional en `POST /api/companies`: `fiel_certificate`, `fiel_key`, `fiel_password`, `fiel_consent=1`. Máximo 64 KiB por archivo, contraseña hasta 1 024 caracteres; sin alteración por TrimStrings. Validación criptográfica local antes de persistir; empresa, catálogo y credenciales en una transacción. No se llama al SAT para guardar.
- `SAT_LOCAL_SAVED_ENABLED` explícita y `APP_ENV=local`; clave dedicada `SAT_LOCAL_CREDENTIAL_KEY` de 32 bytes, sin valor versionado. Payload cifrado autenticado AES-256-GCM en `sat_local_credentials`, único por empresa; eventos de carga/retiro con actor, consentimiento versionado y fecha en `sat_local_credential_events`, sin secretos y conservados tras retirar la copia activa. No se serializa el ciphertext ni los secretos por API. No se usa la clave productiva ni se exportan archivos fuente. El piloto local no promete separación física de claves de la misma computadora.
- En la entrega local implementada, la capacidad se informa en `GET /api/company-creation-capabilities`; estado y retiro están en `GET/DELETE /api/companies/{id}/local-fiel`. El retiro sólo lo realiza el administrador y se serializa con el runner. Esa ruta no ofrece reemplazo; el contrato nuevo de producción está en «Credenciales: superficie técnica condicionada» y no se implementa en esta etapa local.
- Descarga `REAL_SAVED`, escenario `REAL_SAVED`, misma ruta HTTP de creación y reanudación con idempotencia. El runner conserva `REAL_LOCAL` para terminal. Se reutilizan paquetes/resultados privados. Jobs sólo id, generación y paso; conexión de cola `sat-real-local` con `retry_after=300`, un intento y timeout 240 s. El siguiente paso legítimo se programa tras confirmar avances; fallos quedan interrumpidos sin reintento. Trabajos obsoletos no comunican ni importan.
- UI: carga opcional en formulario existente, aviso/consentimiento sin premarcar y contraseña oculta. FormData sólo si hay FIEL. Panel fiscal permite selección real diferenciada de fixtures, estado de credencial y retiro con confirmación. No se conserva formulario sensible tras éxito/cancelación ni se guarda en almacenamiento del navegador.
- Pruebas: creación sin FIEL, trío incompleto, contraseña/RFC/llave inválidos, rollback, cifrado y ausencia de secretos, límites, producción, permisos, retiro y aislamiento; jobs obsoletos/errores/reanudación sin reenvío; componentes del formulario y descarga real con React Testing Library. Todas las comunicaciones usan dobles ficticios, nunca FIEL del usuario.

- `FiscalDocumentController::simulate()` ejecuta la simulación y la importación dentro de la misma petición. La conexión real necesita un proceso persistente, independiente de la pantalla y separado de esa operación ficticia.
- `FiscalDocumentImporter` es compartido por carga manual y simulación. Debe ser el punto común de incorporación del SAT para evitar otra definición de duplicados o extracción fiscal.
- `FiscalDocumentType` y `CfdiXmlParser` admiten sólo `I`, `E` y `P`, en versión 4.0. La ampliación a `N` y `T` debe coordinar extracción, consulta, filtros y consumidores contables; no basta con cambiar el selector de descarga.
- Las migraciones ya definen `fiscal_documents.original_path` nullable y unicidad por empresa/UUID; la importación actual no guarda originales. No se presupone que deba crearse otra columna equivalente ni rellenar documentos históricos automáticamente.
- Las pruebas `tests/Feature/Spec004Test.php`, `Spec005Test.php` y `CompleteFlowSeederTest.php` contienen expectativas de ausencia de original que tendrán que distinguir datos históricos de nuevas incorporaciones. No se han ejecutado para esta preparación.
- `config/queue.php` contempla una cola persistente de base de datos como valor predeterminado. Esto no demuestra qué conexión, procesos de trabajo o servicios están activos en el VPS.
- Frontend: reutilizar `src/features/fiscal-documents/`, manteniendo acceso a datos en `api/`, coordinación en hooks y presentación en componentes. Las rutas sólo compondrán pantallas. No agregar llamadas directas a `fetch` fuera del cliente compartido.

## Flujo y estados propuestos

Referencias: CA-012-01 a CA-012-08, CA-012-12 a CA-012-14 y CA-012-20.

| Etapa visible propuesta | Responsabilidad del proceso | Salida o interrupción |
|---|---|---|
| Validación previa | Revisar acceso, periodo, fechas, tipos y dirección, habilitación jurídica, autorización de custodia, disponibilidad de e.firma válida y ausencia de otra solicitud activa. | Un rechazo previo no se envía al SAT ni se presenta como solicitud aceptada. |
| Pendiente de envío | Conservar la intención aceptada localmente y reservar el único proceso activo de esa empresa antes de comunicar con SAT. | Enviar sólo el trabajo pendiente; evitar duplicar envíos por doble clic o ejecución repetida. |
| Solicitud al SAT | Autenticar y presentar las consultas necesarias, conservando cada identificador que SAT confirme. | Si falta certeza sobre la recepción, registrar la incertidumbre: no afirmar que no existe una solicitud ni reenviar a ciegas. |
| Esperando al SAT | Consultar periódicamente los identificadores aceptados, mediante ejecuciones cortas y persistentes. | «Aceptada» o «En proceso» mantiene el seguimiento normal; no es un reintento tras fallo. Un error detiene el intento afectado. |
| Espera prolongada | Mostrar el aviso definido por CA-012-22 sin cambiar el estado reportado por SAT. | Mantener el seguimiento y la reserva activa; no terminar ni reenviar por cumplir el umbral. |
| Descargando paquetes | Registrar los paquetes informados y guardar cada paquete obtenido de forma privada antes de importarlo. | Un paquete ya disponible e íntegro se reutiliza; no vuelve a solicitarse sólo porque falló la importación. |
| Importando documentos | Leer los XML de cada paquete y utilizar el importador compartido, conservando originales y resultados por documento. | Mantener avances entre ejecuciones. Distinguir rechazo individual de XML de fallo que impide procesar el resto de un paquete. |
| Finalizada | Consolidar todas las consultas y paquetes previstos. | Distinguir resultado completo, completo con rechazos y sin documentos. Tener algunos XML importados no acredita haber terminado toda la solicitud. |
| Interrumpida | Conservar etapa, motivo seguro y avances ante fallo de comunicación, autenticación, almacenamiento o procesamiento. | Liberar la reserva activa del proceso y esperar una acción manual, sin perder documentos incorporados ni volver a empezar indiscriminadamente. |
| Detenida por credenciales | Detener nuevas comunicaciones cuando se retiran o dejan de ser utilizables las credenciales. | Liberar la reserva activa y conservar historial y archivos. La reanudación manual depende de una credencial válida, ausencia de otra activa y de que SAT aún permita continuar. |
| Seguimiento detenido por usuario | Registrar la detención por administrador o contador actualmente asignado, aunque no sea el solicitante original. | Liberar la reserva, conservar avances y no ejecutar nuevos pasos ni reanudar automáticamente. No afirmar que se canceló en SAT. |
| Rechazada o vencida por SAT | Registrar el estado informado por el servicio y su motivo disponible. | No confundirlo con un tiempo de espera local ni prometer recuperación de paquetes ya vencidos. |

Las etapas visibles anteriores se proyectan sobre el estado y la etapa técnicos definidos en «Persistencia y coordinación»; no constituyen otro enum. Los estados SAT `Aceptada=1`, `En Proceso=2`, `Terminada=3`, `Error=4`, `Rechazada=5` y `Vencida=6` se conservan separados del resultado de incorporación local: «Terminada» en SAT no significa «importada» en el sistema.

### Una solicitud del usuario y varias consultas SAT

El SAT separa emitidos y recibidos y permite filtrar un tipo de CFDI por consulta. Crear una consulta por cada combinación seleccionada de dirección y tipo, incluso si se eligen los cinco tipos: entre una y diez consultas bajo un mismo proceso local, sin omitir el filtro de tipo ni ampliar fechas. Orden estable: emitidos antes que recibidos y tipos I/E/P/N/T. Envíos y procesamiento secuenciales dentro de la empresa; la concurrencia global queda sujeta al dimensionamiento. Un fallo interrumpe el proceso completo, incluidas sus consultas hermanas, conservando las ya aceptadas para reanudación manual.

Todas las consultas y paquetes del proceso se vincularán a la misma empresa, periodo y selección original. La regla de una solicitud activa por empresa se aplica al proceso local completo, no sólo a una consulta SAT. No se habilitan programaciones periódicas de nuevas descargas: el seguimiento automático sólo atiende solicitudes iniciadas manualmente.

## Reintentos, espera y liberación

Referencias: CA-012-03/04/07/08/20/22/23/24.

- Reintento manual por etapa: verificar de nuevo los identificadores conocidos, obtener sólo paquetes faltantes y reprocesar archivos locales pendientes sin crear documentos repetidos.
- Si SAT confirma rechazo, vencimiento, límite de resultados o agotamiento de solicitudes repetidas, mostrar una explicación y conservar el historial. Dividir rangos, cambiar filtros o crear otra petición requiere diseño explícito; no modificar fechas para eludir límites ni crear consultas adicionales como recuperación automática.
- Una ejecución repetida por caída del proceso de trabajo no equivale a autorización para repetir una operación externa de resultado desconocido. Registrar la intención y la respuesta conocida para poder distinguir recuperación local de nuevo envío.
- Separar espera de preparación SAT, tiempo máximo de una comunicación, duración de ejecución local y disponibilidad de paquetes. Las 72 horas del manual se cuentan desde la generación del paquete; no son un tiempo máximo garantizado de respuesta del SAT ni una razón para declarar vencida una solicitud aún en proceso.
- El umbral acordado de espera prolongada se calcula por consulta SAT desde su aceptación; mostrar qué consulta del proceso lo alcanzó y conservar la espera como etapa operativa, no como error SAT. Una selección con varias consultas puede tener aceptaciones en distintos momentos.
- Aplicar los parámetros iniciales aprobados de la sección siguiente, sin confundirlos con el umbral funcional de espera prolongada. La duración máxima de cada ejecución local y su coordinación con la reserva de trabajo siguen pendientes de contrato técnico.
- La interrupción por fallo, el retiro de credenciales sin reemplazo y la detención manual dejan el proceso local sin reserva activa. La reanudación manual vuelve a validar credenciales, permiso y ausencia de otra activa, y adquiere la reserva de forma atómica antes de ejecutar trabajo. Una credencial restaurada no dispara reanudación por sí sola.
- Administrador o contador actualmente asignado pueden detener seguimiento de cualquier solicitud de la empresa. Registrar quién lo hizo; no restringirlo por autoría ni extender ese permiso al retiro de e.firma o a la simulación, que siguen reservados al administrador.
- El trabajo previamente encolado debe volver a comprobar que el proceso puede continuar. Coordinar ejecución en curso y liberación de reserva según «Persistencia y coordinación»; una petición ya enviada al SAT no puede deshacerse.
- La liberación no borra historial, archivos o identificadores conocidos ni cancela la solicitud remota. Antes de presentar otra consulta con los mismos criterios, revisar antecedentes y respuestas SAT: permitir otro proceso local no autoriza duplicar envíos externos de resultado desconocido.
- La exclusión de descargas simultáneas usa el slot persistente y control atómico definidos en «Persistencia y coordinación», no depende de deshabilitar un botón. Su comprobación ante caídas sigue pendiente.

### Parámetros iniciales aprobados

Son valores configurables del sistema, no exigencias ni tiempos garantizados del SAT. Su aprobación no acredita capacidad del VPS ni habilita cambios en él.

| Parámetro | Valor inicial | Aplicación |
|---|---|---|
| Intervalo de verificación | 5 minutos por consulta pendiente | Distribuir las ejecuciones entre consultas para evitar ráfagas. El seguimiento sólo continúa mientras SAT responda normalmente que aún procesa la consulta. |
| Tiempo para establecer conexión | Hasta 10 segundos | Dentro del tiempo total de la comunicación, no sumado a éste. |
| Tiempo total de autenticación, solicitud o verificación | Hasta 60 segundos por comunicación | Un timeout interrumpe el intento afectado y requiere reintento manual. No iniciar otra solicitud automáticamente si se desconoce si SAT recibió el envío. |
| Tiempo total de descarga de paquete | Hasta 180 segundos por intento | Incluye establecimiento de conexión y lectura de la respuesta. No renovar indefinidamente el plazo por recibir datos parciales ni reintentar automáticamente al agotarlo. |
| Bloque interno de importación | Hasta 50 XML, procesados secuencialmente | Conservar avance entre bloques; no cargar todos los XML a memoria ni limitar la solicitud completa a 50 documentos. Un bloque tampoco autoriza mantener simultáneamente 50 archivos completos en memoria. |
| Tamaño individual de XML | Hasta 10 MiB (10 485 760 bytes) | Conservar el límite equivalente vigente de carga manual y aplicarlo inicialmente a los XML de paquetes SAT. Un XML mayor se informa como rechazado; los demás válidos pueden continuar. |

- La cadencia de cinco minutos no promete que el proceso completo termine cinco minutos después de que SAT prepare los archivos: intervienen la cola, cantidad de consultas, descarga y procesamiento.
- Procesar bloques no implica una transacción global por bloque. Conservar incorporación y resultado por archivo, sin perder los válidos ante un rechazo individual.
- Antes y durante el procesamiento, controlar bytes reales de respuesta y de contenido descomprimido, cantidad de entradas, tamaño individual y espacio disponible. No confiar sólo en los tamaños declarados por el ZIP o sus cabeceras; contemplar además el envoltorio de transporte del SAT al calcular recursos.
- Impedir rutas de salida del área privada, enlaces o entradas peligrosas y expansión desproporcionada de ZIP/XML. No ejecutar contenido de los paquetes ni permitir que su extracción o análisis agote memoria/disco.
- Si un paquete completo o el recurso disponible excede un límite seguro, interrumpir con motivo explícito y conservar los avances válidos; no marcar completado ni omitir silenciosamente documentos. Un rechazo individual no obliga por sí solo a descartar todo el paquete.
- **Dimensionamiento pendiente:** el usuario desconoce el volumen de CFDI de la empresa mayor y no se ha confirmado RAM, CPU o disco del VPS. No fijar por suposición máximos de paquete comprimido/descomprimido, número de entradas, memoria, espacio temporal o concurrencia global entre empresas. Deben definirse y probarse antes de ejecutar descargas reales; esta pendiente no se resuelve con el bloque de 50 ni con el límite individual de 10 MiB.
- Referencia de seguridad: [OWASP, límites de archivos y descompresión](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html#upload-and-download-limits). La guía fundamenta controlar recursos antes y después de descomprimir; no prescribe los valores numéricos aprobados aquí.

## Fechas e históricos

- Traducir los días seleccionados a límites inclusivos `AAAA-MM-DDT00:00:00` y `AAAA-MM-DDT23:59:59`, sin desplazarlos por UTC o por la zona del navegador. El filtro corresponde a emisión, no a timbrado, fecha de pago del complemento ni fecha de recepción.
- Determinar «hoy» en backend con `America/Mexico_City` y mostrar la misma referencia en el selector frontend. Aplicar esta regla a la función, sin cambiar globalmente `config/app.php`, actualmente en UTC, ni agregar configuración de zona por empresa.
- Conservar las fechas del formulario como días de calendario, evitando que su conversión a un instante UTC cambie el día. Consultas recibidas pueden contener CFDI expedidos en distintas zonas; no reinterpretar su fecha escrita como hora de Ciudad de México.
- Permitir rango que incluya hoy y conservar el límite de día completo solicitado. No garantizar que SAT entregue documentos emitidos después de iniciar o procesar la consulta ni prometer que toda fecha seleccionada esté completa. No ampliar el rango ni consultar de nuevo automáticamente para completarlo.
- Mantener el mes/ejercicio activo y la validación de fechas futuras. Para históricos, no introducir un corte artificial en abril de 2023: validar versión 4.0 de cada XML, informar otras versiones como no admitidas y respetar la ventana y respuestas del SAT.
- El manual v1.5 describe cinco ejercicios anteriores más el actual. Su aplicación efectiva requiere contraste frente a reportes comunitarios de límite móvil; no imponer un corte local distinto sin acreditarlo y conservar errores del servicio sin atribuir ausencia de documentos a una descarga completa. Véase «Matriz de contraste SAT». La ventana de recuperación SAT no determina el plazo de conservación de XML u originales ya guardados.

## Información que deberá persistir

Resumen de datos del diseño propuesto; las tablas y reglas de coordinación se concretan más adelante. Las migraciones se escribirán sólo al autorizar implementación.

| Agrupación | Información necesaria | CA |
|---|---|---|
| Proceso local | Empresa, periodo capturado al inicio, usuario solicitante, fechas de emisión, dirección, tipos, fechas de ejecución, etapa y resultado. | 01–05, 14 |
| Consultas SAT | Pertenencia al proceso, selección enviada, identificadores aceptados, estados y códigos del SAT, última verificación y próxima consulta prevista. Registrar incertidumbre si un envío no tiene respuesta concluyente. | 03–05, 08 |
| Paquetes | Consulta de origen, identificador SAT, referencia privada al paquete, integridad, progreso local y resultados. No atribuir una fecha exacta de generación o expiración si SAT no la proporciona. | 03, 07–08 |
| Resultados por XML | Documento asociado cuando corresponda, tipo de resultado, motivo de rechazo seguro y avance de incorporación. Separar completar un original de crear un documento nuevo. | 06–11 |
| Original fiscal | Asociación por empresa/documento, referencia privada e integridad. Conservar ausencia de original en registros históricos hasta que llegue uno compatible. | 09–11 |
| Credenciales y autorización | Referencias al almacén protegido, metadatos no secretos de certificado, estado de disponibilidad, aceptación versionada y evidencia de autorización del cliente. No duplicar secretos en procesos, colas, resultados o auditoría. | 12–14, 17–21 |

### Integridad y compatibilidad

- Mantener la unicidad empresa/UUID existente. Vincular cada resultado sólo con documentos y archivos de la misma empresa, incluso ante ejecuciones repetidas o simultáneas de carga manual y descarga SAT.
- Coordinar guardado privado del XML y registro en base de datos según «Atomicidad de documentos y originales»: no informar éxito completo si el original obligatorio no quedó disponible. Un fallo no debe dejar una referencia rota ni permitir que otro usuario consulte un archivo sin autorización. El calendario de limpieza de temporales sigue sujeto al presupuesto de disco y política de retención pendientes.
- Completar un original faltante exige comprobar correspondencia con el documento existente, no sólo encontrar su UUID. Comparar UUID, RFC emisor/receptor, tipo, fecha, moneda e importes conservados y los demás datos fiscales disponibles. No actualizar importes, relaciones o pólizas; ante incompatibilidad, rechazar completar el original e identificar los campos distintos, sin guardar el archivo como original ni abrir una revisión humana pendiente no acordada. No exigir conceptos o desgloses que nunca se conservaron para ese documento.
- Para esa comparación, utilizar la precisión decimal vigente sin comparar representaciones textuales equivalentes como si fueran importes distintos. La fecha histórica sólo conserva día, no hora: no exigir una hora inexistente en el registro. La comparación no constituye verificación criptográfica ni consulta de vigencia ante SAT.
- CA-012-10 establece como esenciales UUID, RFC emisor/receptor, tipo, día de emisión, moneda, subtotal y total. Si falta cualquiera en el registro existente, rechazar completar el original con motivo por campo, sin corregirlo automáticamente ni iniciar revisión humana. No confundir valores válidos como total cero o moneda `XXX` con ausencia de datos.
- Diferenciar ausencia histórica demostrable de dato opcional realmente ausente en el CFDI y de valor conservado vacío o cero. Las migraciones de descuento/desglose y conceptos los agregaron nullable; el parser actual produce descuento cero cuando no viene en XML y conceptos vacíos cuando no hay nodos. No usar `null`, cero o lista vacía como equivalentes universales ni basarse únicamente en la fecha del documento para inferir lo que se guardó.
- Cuando coincidan esenciales y demás valores conservados, la falta histórica de descuento, desglose o conceptos no impide guardar sólo el archivo: mantener esos campos sin completar e informar que se compararon datos disponibles, sin verificación integral. Un valor efectivamente conservado sí se compara, aunque sea cero o lista vacía; una diferencia se rechaza e identifica. El contrato del importador concreta la normalización; acreditar los productores históricos sigue pendiente, sin cambiar esta política aprobada.
- Conservar importes con la precisión decimal vigente de seis posiciones y sin conversiones a números de coma flotante. Mantener reglas de pagos, impuestos, conceptos y aislamiento del importador existente.
- Revisar consumidores de nómina/traslado antes de ampliar el enum. No permitir que un nuevo tipo caiga por defecto en tratamiento de ingreso/egreso o genere datos contables inventados. Mantenerlos en consulta general y rechazar nuevas relaciones con pólizas y propuestas de partidas tanto en interfaz como en backend, independientemente de que provengan del SAT o de carga manual; no incluirlos automáticamente en DIOT. No modificar ni borrar relaciones históricas por esta nueva restricción.
- Los límites HTTP actuales de carga manual son 50 archivos de hasta 10 MiB por archivo. Se mantienen; el bloque de procesamiento SAT y los límites técnicos de paquetes se tratan en «Parámetros iniciales aprobados», sin imponer 50 documentos como máximo de la descarga completa.
- Las actualizaciones de esquema no deben exigir originales para datos históricos ni eliminar documentos, pólizas o evidencia existentes. La limpieza de datos de simulación previos no forma parte del plan.

## Custodia y autorización: controles por implementar

Referencias: CA-012-12 a CA-012-14 y CA-012-17 a CA-012-21.

- Mantener separados tres permisos: carga inicial y reemplazo por administrador o contador con asignación vigente; retiro y simulación sólo por administrador. La autorización se verifica de nuevo en cada operación.
- Mostrar aviso y exigir aceptación antes de transmitir archivos o contraseña. No guardar secretos en almacenamiento del navegador ni devolverlos mediante consultas. La autorización del cliente y su evidencia no se sustituyen por un rol de usuario.
- Contemplar un componente de credenciales/firma separado del importador. Este último sólo necesita XML, nunca acceso a la llave privada. El proceso de descarga debe referenciar la credencial vigente, sin conservar una copia de la anterior para terminar tras su retiro.
- La restricción de finalidad debe aplicarse al componente de firma y a sus operaciones admitidas, no sólo a una leyenda de interfaz. No habilitar firma arbitraria de documentos.
- El retiro impide nuevas comunicaciones; una comunicación ya enviada no se deshace. El diseño deberá tratar explícitamente operaciones en curso y cambios de credenciales sin prometer revocación del certificado ni cancelación en SAT.
- El usuario confirma aprobación fiscal/legal y autorización de titulares, y elige persistir archivos FIEL cifrados en una carpeta privada de la aplicación. Esa carpeta queda fuera de Git y de rutas públicas; la clave de cifrado se configura fuera del código. La operación productiva sigue pendiente de implementación y comprobación; no se asume que el despliegue ya esté configurado.

## Responsabilidades y orden de integración

- Backend: acceso por empresa y permisos por acción; persistencia del proceso y reserva activa; coordinación de consultas/paquetes; reintentos manuales; integración con importador y originales; compatibilidad fiscal y auditoría. La simulación exige `confirmed=true` también en backend, conforme al contrato HTTP.
- Operación del VPS: comprobar procesos de trabajo persistentes, recuperación tras reinicios, almacenamiento y respaldos privados, supervisión de fallos y custodia separada de claves. No asumir que la configuración del repositorio acredita estos controles en Hostinger.
- Frontend: formulario de rango y selección, consulta del proceso activo y del historial, resultado por etapa/documento, acción de reintento y bandeja reconciliada tras importar. Mostrar claramente que la consulta SAT solicita sólo vigentes y no actualiza cancelaciones posteriores.
- Interfaz de credenciales: carga inicial/reemplazo para administrador o contador asignado; retiro sólo para administrador; aceptación y referencia a autorización de cliente; mostrar metadatos necesarios, nunca credenciales recuperables. El reemplazo se integra en la edición de empresa sin permitir cambiar RFC.
- Simulación: mantenerla identificada, sólo para administrador, con advertencia y confirmación previa. No llamar SAT ni usar e.firma; no utilizarla como sustitución automática ante un error real.
- Se preparó el desglose preliminar por repositorio y se coordinaron los documentos de SPEC-004/005. Antes de implementar: completar contratos y precisiones de la parte afectada → revisar las dependencias de tareas → implementar y probar únicamente tras autorización expresa. La revisión jurídica y de custodia es requisito adicional para habilitar la parte afectada, no una tarea que pueda darse por resuelta implementando cifrado.
- [Tareas de backend](tasks-backend.md) y [frontend](tasks-frontend.md) contienen acciones pendientes con CA y condiciones de cierre; sus dependencias remiten a los contratos preparados y a sus puntos aún condicionados. No constituyen autorización de ejecución.

## Estrategia de pruebas

La evidencia futura corresponde a [verificacion.md](verificacion.md). No se ejecutan pruebas de producto en esta fase documental.

| Cobertura prevista | Comprobaciones |
|---|---|
| CA-012-01/02/06 | Cada tipo 4.0, combinaciones de dirección/tipos, fechas inclusivas, fin de mes/ejercicio, fuera de periodo, rango invertido, versión no admitida, XML fuera del filtro y RFC ajeno. Probar hoy/futuro con reloj controlado cerca de medianoche en UTC y Ciudad de México, navegador en otra zona y emisión local sin desplazamiento de día; históricos 4.0 anteriores a abril de 2023 y rechazo SAT por antigüedad, sin confundirlo con cero resultados. Nómina/traslado consultables por ambas vías, sin nuevas relaciones con pólizas ni propuestas incluso por petición directa; sin inclusión automática en DIOT. |
| CA-012-03/04/05 | Cierre de pantalla/sesión, persistencia y recuperación del proceso; competencia de dos solicitudes en una empresa; independencia entre empresas; varios identificadores SAT agrupados en un historial. |
| CA-012-07/08 | Lote mixto, cero resultados, error en una consulta o paquete después de avances, incertidumbre tras envío, vencimiento, límite de consultas, reanudación desde paquete guardado y ausencia de reintentos automáticos tras fallo. |
| CA-012-09/10/11/21 | Conservación exacta de originales de carga manual/SAT, fallo de almacenamiento, duplicado con original, recuperación de original faltante compatible, rechazo de diferencias y de esenciales ausentes con identificación de campos sin modificar el registro. Histórico sin conceptos/descuento/desglose guarda sólo original e informa comparación limitada; esos campos siguen ausentes. Distinguir cero/lista vacía conservados de ausencia histórica, aceptar decimales equivalentes y moneda XXX cuando corresponda. Comprobar aislamiento y ausencia de URL pública o descarga al equipo. |
| CA-012-12/13/14/17/18/19/20/29 | Matriz de roles/empresa, reemplazo de la credencial por contador asignado, aceptación previa al envío, versión y evidencia de autorización, credenciales inválidas, retiro/reemplazo concurrente, fallo atómico, ausencia de contacto SAT durante el reemplazo, secretos ausentes de respuestas/registros/colas y operaciones de firma no autorizadas. Comprobar controles de producción sin usar credenciales reales en pruebas automatizadas. |
| CA-012-15/16 | Simulación visible sólo para administrador; cancelación de la confirmación sin incorporaciones; petición directa de contador rechazada; simulación sin conexión real ni fallback automático. |
| CA-012-22/23/24 | Reloj controlado antes, al cumplir y después de 24 horas; aviso sin detener ni liberar; liberación tras fallo/retiro/detención; detener por otro contador asignado; rechazo tras perder acceso; ausencia de reanudación automática; reanudación manual frente a otra activa y trabajo antiguo encolado sin reactivar un proceso detenido. |
| Regresiones | Importación manual, unicidad por empresa, datos históricos sin original, pagos y conceptos, pólizas, reportes y DIOT; no dar nómina/traslado un tratamiento contable no definido. |

- Backend: pruebas de comportamiento con respuestas SAT controladas para aceptación, espera, múltiples paquetes, límites y fallos. Evitar usar e.firmas reales o consumir cuotas SAT en pruebas automatizadas. Ejecutar las pruebas futuras con Sail conforme al flujo del proyecto.
- Parámetros y recursos: reloj controlado para intervalo de cinco minutos sin ráfagas; límites de conexión y tiempo total por operación; fallo de comunicación sin reintento automático; más de 50 XML conservando avances entre bloques; archivo justo en 10 MiB y otro superior; ZIP con tamaños falsos, rutas peligrosas, expansión excesiva y espacio insuficiente. Los casos de capacidad total requieren primero fijar el dimensionamiento pendiente; no se dan por cubiertos por validar el tamaño de un XML.
- Frontend: Vitest y React Testing Library para selección, validaciones, permisos, seguimiento, historial, resultados parciales, cambio de empresa/periodo sin mezclar respuestas y confirmaciones. Simular el cliente compartido y comprobar que secretos no se mantienen tras cerrar el formulario. No sustituir estos casos por snapshots.
- QA humana: disposición y claridad visual de formularios, estados, resultados y textos de advertencia cuando exista implementación. No exigir un recorrido integral por navegador para acreditar las pruebas técnicas.
- Contratos nuevos: idempotencia con entrada igual/diferente, secuencia de una a diez consultas, paginación aislada, errores 403/404/409/422, `STOPPING` frente a worker vivo y mensajes tardíos de una generación anterior. Probar caída antes y después de persistir intención/respuesta sin reenviar `UNKNOWN`, discrepancias de entrada ZIP con nombre repetido y resultado canónico sin doble conteo. La autenticación renovada normalmente no debe convertirse en reintento automático tras fallo.

## Contrato HTTP

Propuesta nueva bajo `/api/companies/{companyId}`, dentro de la autenticación Sanctum y control de cambio de contraseña existentes. No introducir otra versión de API. Fechas de calendario: `YYYY-MM-DD`; instantes de auditoría: ISO 8601 UTC. Los identificadores locales son enteros y los SAT son cadenas opacas, nunca nombres de archivo. Los permisos se comprueban en cada acción y los recursos se buscan siempre dentro de la empresa visible; empresa/recurso ajenos responden 404 como las rutas fiscales actuales, y una acción no permitida dentro de una empresa visible responde 403.

### Solicitudes reales e historial

| Operación nueva | Entrada | Salida |
|---|---|---|
| `POST /fiscal-document-downloads` | JSON: `period_id`, `date_from`, `date_to`, `directions` (lista sin repetidos de `ISSUED`/`RECEIVED`), `document_types` (lista sin repetidos de I/E/P/N/T). Cabecera `Idempotency-Key`: UUID generado para esa intención del usuario. | 202 con `{data: Download}` tras persistir intención y reserva; aún no significa aceptación SAT. La misma clave y contenido devuelve el mismo recurso sin nuevo envío. |
| `GET /fiscal-document-downloads?period_id=&page=` | Periodo opcional perteneciente a la empresa; página positiva. Sin periodo incluye todo el historial de la empresa. | `{data: Download[], links, meta}` paginado de 25, orden `created_at DESC, id DESC`. |
| `GET /fiscal-document-downloads/{id}` | Sin cuerpo. | `{data: Download}` con selección original, consultas y resumen, aunque cambió el periodo de pantalla. |
| `GET /fiscal-document-downloads/{id}/results?page=` | Página positiva. | Resultados por entrada paginados de 50; no incluir XML ni descargar archivos desde esta ruta. |
| `POST /fiscal-document-downloads/{id}/stop` | Sin cuerpo. | 202 con el recurso en detención o ya detenido; repetir la acción no produce efectos extra. |
| `POST /fiscal-document-downloads/{id}/resume` | Sin cuerpo y nueva `Idempotency-Key`. | 202 con el recurso reservado para revisión de avances; no crea otro proceso ni cambia su selección. |

`Download` contiene `id`, `company_id`, `period_id`, `requested_by` (id), `date_from`, `date_to`, `directions`, `document_types`, `status`, `stage`, `stop_reason`, `created_at`, `updated_at`, `completed_at` nullable, `has_prolonged_wait`, `submission_uncertain`, `can_stop`, `can_resume`, `blocking_code` nullable, `summary` y `queries`. Las acciones permitidas son orientativas para la interfaz; el servidor las vuelve a comprobar. No devolver referencias internas al almacén, tokens o credenciales.

- `summary`: `imported_count`, `duplicate_count`, `original_completed_count`, `rejected_count`, `pending_package_count`, `processed_entry_count` y `is_complete`. Todos son enteros no negativos. No usar el número SAT de CFDI como si fuera el número local importado ni prometer documentos únicos sumando consultas: un mismo UUID puede aparecer en varias.
- `queries[]`: `id`, `direction`, `document_type`, `submission_status`, `sat_request_id` nullable, `sat_status` nullable (1–6), `sat_code` nullable (cadena), `accepted_at`, `last_checked_at`, `next_check_at`, `has_prolonged_wait`, `reported_document_count` nullable y paquetes conocidos (`id` local, `status`). No incluir en el detalle todas las entradas XML; usar la ruta paginada de resultados.
- Validar pertenencia del periodo, rango inclusivo dentro de su mes/ejercicio, hoy en America/Mexico_City y listas no vacías. Capturar el contexto al crear: cambiar el periodo activo después no retargetea el trabajo. No exigir una nueva reserva contable ni convertir esta descarga fiscal en escritura de pólizas.
- Doble clic/reenvío HTTP: clave única por empresa, usuario y operación; guardar hash de la entrada normalizada y referencia al recurso en la misma transacción. Misma clave con otra entrada: 409 `IDEMPOTENCY_CONFLICT`. Conservar la vinculación en el historial, sin caducar la clave mientras pueda reaparecer un envío incierto. Un reenvío no permite saltar la autorización vigente.
- Una nueva clave no elude la reserva ni autoriza repetir consultas SAT de recepción desconocida. Si hay antecedentes inciertos con los mismos criterios, responder 409 `SAT_SUBMISSION_UNCERTAIN`; no resolverlo alterando fechas, buscando por UUID o inventando un identificador SAT.

### Validación y errores

Conservar el formato Laravel `{message, errors}`; añadir `code` estable para conflictos/precondiciones, sin cuerpos SOAP ni mensajes con secretos. 401 y protección CSRF conservan el comportamiento existente; 422 para campos inválidos; 409 para otra descarga activa (`DOWNLOAD_ACTIVE`), estado incompatible (`INVALID_DOWNLOAD_STATE`), falta de credenciales válidas (`CREDENTIAL_UNAVAILABLE`) o custodia no habilitada (`CUSTODY_NOT_ENABLED`). El conflicto activo incluye su id sólo dentro de la empresa autorizada; basta con `code`/`message` si el cliente actual no conserva propiedades adicionales del error.

Fallos externos posteriores al 202 se consultan como estado del recurso, no como si el POST nunca hubiese existido. Una indisponibilidad del sistema antes de guardar la intención puede devolver 503 sin crear recurso. No devolver éxito ante transacción o almacenamiento fallidos.

### Credenciales: superficie técnica condicionada

La autorización fiscal/legal para custodia de clientes y la autorización de sus titulares han sido confirmadas por el usuario. Las rutas reales no se consideran habilitadas hasta implementar y verificar controles de credenciales, evidencia, infraestructura y operación definidos en este plan.

| Operación nueva | Contrato previsto |
|---|---|
| `GET /sat-credentials` | Sólo metadatos: `configured`, `status`, RFC, número/vigencia del certificado, versión de credencial y acciones permitidas; nunca `.cer`, `.key`, contraseña, token o referencia de secreto. |
| `GET /sat-credential-notice` | Aviso vigente versionado, requisitos y disponibilidad de la custodia. El texto y sus requisitos son insumos jurídicos pendientes, no textos inventados por implementación. |
| `POST /sat-credentials` | Carga inicial multipart: `certificate`, `private_key`, `password`, `notice_version`, `accepted=true`, `authorization_id`. Administrador o contador asignado; si existe una credencial no se convierte en reemplazo. |
| `POST /sat-credentials/replacement` | Mismos campos y `expected_credential_version`; administrador o contador con acceso vigente. Validar par certificado/llave, contraseña, e.firma (no CSD), vigencia y mismo RFC antes de sustituir atómicamente. Guardar archivos y contraseña cifrados bajo `storage/app/private/fiel/{companyId}`, fuera de Git y webroot; la clave no se guarda en esa carpeta ni se versiona. Si falla la validación o la coordinación con un trabajo activo, mantener la credencial anterior y sus avances. No contactar al SAT durante el reemplazo. |
| `DELETE /sat-credentials` | Sólo administrador, versión esperada como precondición `If-Match`. Retiro idempotente, 204; conflicto de versión 409. Impide usos nuevos e invalida tokens, no promete borrar todas las copias. |

`authorization_id` referencia evidencia aprobada del titular/representante; nunca basta con una cadena proporcionada por el contador. El usuario confirma que existe aprobación fiscal/legal y autorización; el contrato de implementación debe resolver cómo verificar y vincular la evidencia a empresa y credencial conforme a la política aprobada. El aviso debe aceptarse antes de transmitir cualquier archivo o contraseña; una versión obsoleta produce 409 `NOTICE_VERSION_CHANGED`, sin guardar secretos. No registrar cuerpos multipart ni mantener secretos en almacenamiento del navegador. Tamaños permitidos de CER/KEY y límites de carga se fijarán con el proveedor de custodia y antes de habilitar cargas; no aceptar cargas sin esos límites.

La versión publicada por `GET /sat-credentials` se devuelve también como `ETag` para la precondición de retiro. Carga y reemplazo responden 201/200 con sólo esos metadatos; no devuelven los archivos subidos. Conservar la existencia/versiones de una credencial retirada para impedir que una segunda carga del contador se presente como carga inicial.

### Simulación y documentos existentes

- Mantener `POST /fiscal-document-downloads/simulated` síncrono, añadiendo `confirmed: true` al `period_id` existente; contador 403, confirmación ausente/falsa 422. No crear trabajo SAT, usar credenciales ni aplicar reintentos de red automáticos. Preservar `COMPLETED`/`FAILED`, resultado vacío/parcial y mensajes seguros.
- Mantener las rutas de importación manual/listado/detalle. Ampliar el tipo fiscal a I/E/P/N/T en el contrato compartido; detalle añade `original_available: boolean`, sin URL ni ruta de almacenamiento. Los datos contables y de conceptos siguen sus contratos vigentes. Prohibir N/T también en los endpoints de relación y propuesta, no sólo en selectores.

## Persistencia y coordinación

Esquema lógico nuevo para implementación; migraciones aditivas, índices y claves foráneas compatibles con el motor del proyecto. No modificar tablas de reservas contables: su alcance es empresa/periodo y no coincide con una descarga activa por empresa.

| Tabla propuesta | Campos y restricciones principales |
|---|---|
| `sat_downloads` | Empresa, periodo y solicitante; selección inmutable; estado/etapa; motivo seguro, fechas y contadores. Índice empresa/fecha/id. El periodo se valida contra la misma empresa antes de insertar; toda relación se resuelve con ese ámbito. |
| `sat_download_slots` | `company_id` como PK única, `download_id` nullable, `generation` creciente. Una fila por empresa, bloqueo transaccional para adquirir/liberar y comprobar estado. No usar un índice único sobre un booleano activo. |
| `sat_download_queries` | FK al proceso, dirección/tipo, hash de selección, `submission_status`, id SAT nullable, estados/códigos, aceptación y próxima verificación. Única combinación proceso/dirección/tipo. Guardar intención antes del envío. |
| `sat_download_packages` | FK a consulta, id SAT, ubicación privada generada por servidor, hash SHA-256, bytes, estado y avance. Único consulta/id SAT. Fecha de generación/expiración nullable cuando SAT no las informe. |
| `sat_download_items` | FK a paquete, posición de entrada ZIP, nombre seguro, hash del contenido, UUID/documento nullable, resultado, campos discrepantes, alcance de comparación y campos no comparados. Única paquete/posición: repetir el mismo nombre en un ZIP no sobrescribe resultados. |
| `sat_download_operations` | Proceso/consulta/paquete, tipo de operación, generación, intención, inicio/fin y resultado `CONFIRMED`/`FAILED`/`UNKNOWN`; sin datos de firma ni XML. Un envío iniciado sin respuesta confirmada permanece incierto tras reinicio. |
| `sat_download_commands` | Empresa, usuario, tipo de comando, clave idempotente, hash de entrada y referencia al proceso. Única empresa/usuario/operación/clave. |
| `sat_company_credentials` y auditoría | Empresa única, versión, RFC/vigencia, estado y referencias internas a archivos cifrados bajo `storage/app/private/fiel/{companyId}`; aceptación versionada y referencia a autorización aprobada. No guardar llave/contraseña en claro, respuestas o trabajos. |

En `fiscal_documents`, reutilizar `original_path` nullable, añadiendo `original_sha256` y `original_size` nullable. No crear otra columna de ruta equivalente ni rellenar originales/datos fiscales históricos. El rollback de la ampliación no borra archivos ni documentos existentes; retirar infraestructura con trabajo pendiente exige un procedimiento autorizado, no una migración destructiva automática.

### Estados y transiciones

- `status`: `QUEUED`, `RUNNING`, `WAITING_SAT`, `STOPPING`, `COMPLETED`, `INTERRUPTED`, `STOPPED`. `stage`: `SUBMIT`, `VERIFY`, `DOWNLOAD`, `IMPORT`, `FINALIZE`. El aviso de 24 horas es una propiedad derivada por consulta, no otro estado terminal.
- `submission_status` por consulta: `NOT_SENT`, `SENDING`, `ACCEPTED`, `REJECTED`, `UNKNOWN`. `SENDING` sin respuesta confirmada tras una caída se reconcilia como `UNKNOWN`, no `NOT_SENT`. Paquetes: `PENDING`, `DOWNLOADING`, `STORED`, `PROCESSING`, `PROCESSED`, `FAILED`; `STORED` exige bytes/hash verificados. El estado de un paquete no sobrescribe el estado SAT de su consulta.
- Crear o reanudar adquiere slot y entra en `QUEUED`; ejecutar pasa a `RUNNING`. Respuestas SAT 1/2 pasan a `WAITING_SAT`, conservando slot y próxima verificación. Una consulta pendiente de envío o paquete pendiente sigue en la etapa correspondiente; no crear otra intención externa por saltar entre trabajos.
- `COMPLETED` exige todas las consultas terminadas y todos los paquetes procesados o ningún resultado confirmado por SAT. `is_complete=true` no significa ausencia de rechazos individuales; éstos permanecen contados. SAT rechazado/vencido o error de infraestructura produce `INTERRUPTED`, con motivo y `is_complete=false`, no «completa con cero».
- Detener, retirar credenciales o fallar impide programar nuevos pasos. Si hay trabajo ejecutándose, usar `STOPPING` y `stop_reason` (`USER`, `CREDENTIAL`, `FAILURE`); pasar a `STOPPED` para usuario o `INTERRUPTED` para credenciales/fallo cuando termine el paso en curso y liberar slot. No responder que ya quedó libre si aún ejecuta una operación local. Una operación remota ya enviada no se puede deshacer.
- Reanudar sólo desde `INTERRUPTED`/`STOPPED` y sin otro slot ocupado; credencial válida y permisos actuales. No reanudar `COMPLETED`, no volver a enviar una consulta con `submission_status=UNKNOWN`, ni recrear una vencida como parte de la reanudación. Informar que ese punto no admite recuperación segura; una nueva selección manual sigue sujeta a antecedentes y límites SAT.

### Exclusión, caídas y trabajo en curso

Cada unidad de trabajo incluye sólo id local y generación de ejecución. Antes de tomarla y antes de toda comunicación, comprobar estado, slot y versión vigente de credencial; un trabajo viejo termina sin efectos. Mantener una sola unidad ejecutándose por empresa mediante exclusión de ejecución, además del slot persistente. La espera de cinco minutos no mantiene una transacción SQL abierta.

Crear la fila vacía de slot de forma idempotente para cada empresa antes de bloquearla; una fila ausente no puede protegerse sólo con un bloqueo de lectura. Guardar en el registro de operación id de unidad/worker, generación y heartbeat sin secretos para reconciliar trabajo vivo y terminado; esos metadatos no autorizan por sí mismos el relevo.

Persistir intención externa en una transacción corta, ejecutar fuera de ella y guardar respuesta en otra. No envolver SOAP/descarga en una transacción que retenga bloqueos. Los bloqueos del proceso y de la versión de credencial serializan el permiso para iniciar comunicación con stop/retiro: lo autorizado antes del retiro se registra como ya en curso; lo posterior se rechaza. Guardar respuestas de operaciones ya iniciadas aunque se haya pedido detener, sin encadenar el paso siguiente.

Al caer un worker, el vencimiento de un bloqueo o heartbeat **no autoriza** tomar el slot y enviar de nuevo. Primero impedir que el worker antiguo continúe y verificar terminación del trabajo; después registrar interrupción, conservar el resultado incierto y liberar slot. No reintentar excepciones automáticamente mediante la cola. Recuperar trabajo local interrumpido sólo permite reconciliar escrituras/respuestas ya persistidas; nuevos contactos externos requieren reanudación manual tras un fallo.

Cada unidad realiza como máximo una comunicación externa, un bloque de hasta 50 XML o la consolidación local. Duración total local, TTL del bloqueo y plazo de recuperación del supervisor se fijarán juntos tras medición: el bloqueo debe cubrir el límite total del worker y el supervisor debe terminarlo antes de cualquier reasignación. Los 180 segundos de descarga no incluyen permiso para importar indefinidamente. La cola no debe redespachar el mismo trabajo mientras pueda seguir vivo; se comprobará con pruebas de caída reales del entorno controlado.

Despachar trabajo sólo después de persistir la intención. Un coordinador persistente recupera intenciones comprometidas no despachadas comprobando generación/estado y ausencia de una unidad ya iniciada; eso no permite repetir operaciones `UNKNOWN`. No usar el logout o cerrar una pantalla como causa de detención. La pérdida de acceso de un usuario invalida sus nuevas acciones, no borra la solicitud empresarial ya aceptada.

## Contrato del importador

El importador común debe aceptar una entrada XML cada vez o un iterable acotado; no construir un array con todos los contenidos de un ZIP. La carga manual conserva sus límites HTTP y la importación SAT aplica adicionalmente dirección/tipo/rango de la consulta que originó el paquete.

Resultado canónico por entrada: `{name, uuid, document_id, outcome, code, errors, comparison_scope, unverified_fields}`. Identificadores nullable si no se pudo analizar. `outcome` es `IMPORTED`, `DUPLICATE`, `ORIGINAL_COMPLETED` o `REJECTED`; `errors` es mapa de campo a lista de mensajes, vacío fuera de rechazo; `comparison_scope` es `AVAILABLE_FIELDS` o null y `unverified_fields` lista los secundarios históricos no comparados. No llamarlo comprobación integral ni guardar valores secretos en mensajes. Los resultados de XML no contienen rutas privadas.

Para compatibilidad, conservar `imported` y `rejected` en la respuesta HTTP actual y añadir `outcomes`. `imported` contiene sólo documentos nuevos; `rejected` proyecta sólo rechazos reales y `outcomes` incluye todos los resultados, también duplicados y originales completados. El cliente nuevo usa `outcomes` como fuente autoritativa, sin sumar dos veces sus proyecciones. El cambio de clasificación de duplicados exige despliegue coordinado y pruebas del cliente; no se presume compatible con una interfaz antigua que sólo lee `rejected`. La simulación conserva sus campos actuales y añade el mismo resultado canónico.

### Comparación con registros históricos

Comparar el registro almacenado directamente, no el Resource HTTP: actualmente `tax_lines()` convierte null en lista vacía y perdería la distinción necesaria.

| Datos | Normalización/comparación |
|---|---|
| Esenciales | `uuid`, `issuer_rfc`, `recipient_rfc`, `document_type`, `issued_at`, `currency`, `subtotal`, `total`. UUID/RFC/códigos con normalización vigente de parser; día literal del XML, no instante UTC. Ausencia esencial es rechazo por campo; cero y XXX no son ausencia. |
| Decimales conservados | También `exchange_rate`, `discount`, `tax_total` e importes de estructuras. Canonizar como texto de seis posiciones, sin float ni tolerancias monetarias añadidas. Rechazar valores no representables en la precisión vigente, sin redondear diferencias para completar original. |
| Textos y opcionales | `issuer_name`, `recipient_name`, `series`, `folio`, `payment_method`, `payment_form`: misma extracción del parser y comparación exacta del texto conservado. Null por atributo opcional ausente no es permiso general de omitir ese campo si el XML ahora lo incluye. No uniformar nombres/acentos ni recortar diferencias silenciosamente. |
| Estructuras | `taxes` por claves sin depender del orden de atributos; valores fiscales decimales canonizados. `tax_lines` y `concepts` según campos persistidos, preservando posición y repetidos. Cambiar orden de conceptos conservados es diferencia; no ordenar ni deduplicar para hacer coincidir. |
| Pagos y DIOT | Comparar datos fiscales guardados del pago (`related_uuid`, `allocated_amount`) sin usar ids de facturas que pudieron resolverse después. Comparar líneas fiscales DIOT conservadas, no inclusión manual/estado de póliza ni motivos derivados de interfaz. No escribir relaciones, inclusiones o campos fiscales al completar original. |

La exclusión por ausencia histórica sólo aplica a campos demostrablemente no conservados por una versión anterior del importador. Para `discount`, `tax_lines`, `concepts` y líneas fiscales añadidas posteriormente, registrar la cobertura por versión del importador en nuevas incorporaciones. Para históricos, comprobar migraciones y productores anteriores: null es candidato a ausencia histórica, no prueba universal; si se sabe que el productor siempre generaba cero/lista, esos valores se comparan. Un null con semántica de dato fiscal no extraíble (por ejemplo DIOT incompleto) no equivale automáticamente a ausencia histórica.

Cuando la evidencia de procedencia no permita clasificar una ausencia, rechazar con `HISTORICAL_COMPARISON_UNAVAILABLE` y campos afectados; no inventar coincidencia, rellenar registros ni abrir revisión humana nueva. La comprobación de todos los productores históricos queda pendiente antes de dar esta parte por preparada. Esta limitación técnica no altera el permiso de CA-012-10 para completar cuando la ausencia histórica sí está acreditada.

Contraste parcial por lectura de Git: `5a59938` introduce descuento/desglose con migración nullable; el parser anterior no devolvía esos campos. `d841b59` introduce conceptos nullable; desde allí el parser devuelve una lista, aunque esté vacía. En `app/` se localizó el importador como creador de documentos; además `CompleteFlowSeeder` y `DemoCompanySeeder` escriben datos preparados directamente con descuento cero, desglose vacío y sin conceptos. Por tanto, no inferir cobertura sólo por fecha de emisión/creación ni tratar las listas vacías de esos productores como ausencia. No se ha comprobado qué versiones, seeders o cargas externas se ejecutaron en una base real.

### Atomicidad de documentos y originales

Preparar archivo temporal privado y medir bytes/hash; validar y publicar en ubicación interna inmutable antes de confirmar la referencia en base de datos. Si falla almacenamiento, no confirmar documento nuevo ni resultado exitoso. Serializar por empresa/UUID y volver a leer bajo bloqueo el documento existente antes de completar original; la restricción única existente sigue siendo la última protección ante carreras.

Una transacción por documento confirma documento/asociación a original y, para SAT, resultado persistente de entrada conjuntamente. La importación manual sólo responde con su resultado tras confirmar la transacción, sin crear un paquete SAT ficticio. El archivo publicado sin referencia por rollback queda huérfano para limpieza controlada; nunca borrar archivos con referencia comprometida ni temporales de un worker vivo. Si ya existe original al obtener el bloqueo, no reemplazarlo: informar duplicado. Los paquetes locales íntegros se reutilizan; una copia incompleta o con hash distinto no cuenta como descargada y requiere tratamiento manual del fallo, no redescarga silenciosa.

## Preparación de dimensionamiento, custodia y contraste SAT

### Ficha de capacidad pendiente

El usuario confirmó que la capacidad del VPS para este sistema **aún no está definida**. Cuando se elija, obtener sólo datos no secretos: proveedor/plan, vCPU, RAM total y límite de los contenedores/workers, disco total y libre para temporales/originales, espacio/retención de respaldos, servicios que comparten VPS y si backend/cola/disco están en la misma máquina. Hostinger es la propuesta previa, no una capacidad contratada o comprobada para esta entrega. No asumir que otro proyecto comparte infraestructura ni leer credenciales de SSH o `.env` para averiguarlo.

Con esos datos, definir un presupuesto de memoria y disco que reserve capacidad para base de datos, frontend, copias y sistema; escoger concurrencia global, bytes máximos de respuesta SOAP/base64, ZIP comprimido/descomprimido, entradas por paquete y temporales acumulados por proceso/empresa. Medir con fixtures sintéticos crecientes y maliciosos, más de 50 entradas y XML cercanos a 10 MiB; registrar pico RAM/CPU, duración, bytes escritos y espacio libre mínimo, sin usar documentos fiscales reales. Si la librería carga toda la respuesta en memoria, medir esa duplicación o elegir otra estrategia antes de fijar un máximo seguro. No adoptar los ejemplos de lectura de paquetes de una librería como prueba de procesamiento acotado.

Salida exigible de BE-012-10: cifras configurables justificadas por medición, umbral de disco, política de temporales/paquetes y retención aún no acordada, máximo de ejecución y coordinación supervisor/cola. Paquetes y temporales no heredan automáticamente la conservación de los XML originales. Sin esos resultados la descarga real no se habilita.

### Encargo de revisión jurídica

El usuario confirmó que aún no dispone de asesoría para esta revisión. Queda preparado el encargo: entregar a la persona asesora el flujo y actores de CA-012-12/17/18/19/20/21, advertencia del manual SAT, proveedor/ubicación del alojamiento y propuesta de claves externas. Solicitar respuesta documentada sobre:

- Viabilidad y condiciones de custodia de e.firmas propias y de clientes en infraestructura de terceros; alcance de las obligaciones del titular y responsabilidades del operador/proveedores.
- Qué acredita facultades del representante, autorización del cliente, finalidades y vigencia/retiro; quién verifica la evidencia y qué se debe conservar. No resolverlo con la aceptación de un contador.
- Aviso de privacidad y términos versionados, transferencias/proveedores, medidas de seguridad, acceso administrativo, atención de incidentes y responsables.
- Plazos y mecanismos para retirar/eliminar credenciales, copias cifradas, respaldos y evidencias; restauración sin reactivar credenciales retiradas. Separar esto de la conservación fiscal de XML y del historial.

El usuario declara que ya existen aprobación fiscal/legal y autorización de titulares. La aplicación conservará la referencia a esa autorización sin copiar documentos sensibles a la spec. Los archivos de credenciales se cifran en almacenamiento privado de la aplicación; la clave se configura fuera del código y de Git. No guardar archivos o contraseñas en el repositorio ni en rutas públicas.

### Matriz de contraste SAT

| Tema | Evidencia disponible | Pendiente y tratamiento seguro |
|---|---|---|
| Ventana histórica | Manual v1.5: cinco ejercicios anteriores más el actual. README PhpCfdi: seis años atrás desde el día actual. | No fijar un corte local distinto por suposición. El adaptador conserva rechazo SAT como error de antigüedad, no como cero resultados. Contrastar límites con datos controlados y autorización posterior; no se acredita una ventana efectiva. |
| Cambiar certificado | RFC identifica al solicitante; no se ha acreditado continuidad con otro certificado. | Verificar identificadores existentes con la credencial nueva válida del mismo RFC; cualquier rechazo detiene y conserva avances. No reenviar la consulta ni garantizar continuidad. |
| Cuotas/repeticiones | Manual de descarga: hasta dos descargas de paquete, disponible 72 horas desde generación. PhpCfdi reporta además límite a solicitudes idénticas y código 5002. | Tratar operaciones y contadores por separado. No cambiar un segundo del rango para eludir cuotas, ni hacer pruebas automatizadas contra SAT o pasar a metadata como sustituto del alcance. |
| Respuestas por etapa | Una verificación incluye código de comunicación, estado de la solicitud y códigos de su resultado. | Adaptador debe preservar los tres por separado; un código de aceptación de transporte no prueba solicitud terminada. Respuesta contradictoria/desconocida interrumpe, sin inventar éxito. |

Fuente comunitaria consultada el 2026-10-28: [README de PhpCfdi](https://github.com/phpcfdi/sat-ws-descarga-masiva/blob/main/README.md) y [distinción de cuotas, issue 78](https://github.com/phpcfdi/sat-ws-descarga-masiva/issues/78). No sustituyen los manuales enlazados en spec ni una prueba real. La librería es candidata, no dependencia elegida o instalada; confirmar licencia, versión compatible, firmas, control de tiempos, memoria y ausencia de reintentos antes de seleccionarla.

Contrato del adaptador: operaciones `authenticate`, `submit`, `verify`, `download` con RFC/selección o identificadores explícitos y límites del plan. Salidas tipadas que distinguen respuesta confirmada, rechazo y resultado de envío desconocido; `verify` devuelve estados/códigos, cantidad informada y lista de paquetes; `download` entrega un archivo privado acotado con hash/bytes, no un array de todos los XML. Tokens sólo en custodia transitoria protegida por versión de credencial, nunca en la cola. Autenticarse antes de una operación cuando no hay token utilizable es parte normal del flujo; una autenticación/comunicación fallida no se repite automáticamente. Hosts SAT predefinidos y TLS verificado, sin aceptar URLs del navegador o del contenido de un paquete.

## Bloqueantes de preparación

El listado funcional consolidado está en [spec.md, pendientes bloqueantes de preparación](spec.md#pendientes-bloqueantes-de-preparación). Las precisiones siguientes delimitan el trabajo pendiente del plan; no reabren acuerdos aprobados.

- Propuesta de contratos HTTP/datos/estados y coordinación preparada en este plan; falta revisión compartida y resolver los puntos condicionados de evidencia/custodia, límites de carga y productores históricos. No equivale a una implementación ni a contratos jurídicos aprobados.
- Fijar límite de ejecución local y tiempos de supervisor/bloqueo según medición. La exclusión y las transiciones ya están definidas; su recuperación tras caídas requiere prueba controlada, no se acredita con la configuración del repositorio.
- Dimensionar límites totales de paquetes, entradas, memoria, disco temporal y concurrencia global con capacidad del VPS y pruebas controladas; volumen mensual real desconocido.
- Validación histórica definitiva frente a la ventana efectiva del SAT, tamaños/límites de procesamiento y recuperación en cada respuesta del servicio. La referencia America/Mexico_City para hoy y las fechas de emisión sin conversión ya están acordadas. Distinguir lo documentado de comprobaciones reales no realizadas.
- Auditar productores históricos para acreditar ausencia de campos; mapeo/normalización preparado en el contrato del importador. La política de CA-012-10 permanece vigente, sin rellenar registros ni asumir equivalencias entre null/cero/lista vacía.
- Revisión fiscal/legal de custodia de clientes, evidencia de facultades y autorización, políticas de conservación/eliminación y proveedor de claves separado del VPS.
- Coordinación documental completada en SPEC-004/005; no es un bloqueo abierto ni acredita implementación. El trabajo se centraliza en las tareas de SPEC-012 según la correspondencia siguiente.

## Correspondencia con SPEC-004/005

| Criterios coordinados | Criterios de SPEC-012 | Trabajo centralizado |
|---|---|---|
| CA-004-01/03/10/11/12/13: originales y resultados, sin rellenar datos históricos | CA-012-07/09/10/11 | BE-012-03, BE-012-10 y FE-012-05 |
| CA-004-14: nómina/traslado para consulta general | CA-012-06 | BE-012-02 y FE-012-05 |
| CA-005-01/07: administrador, confirmación y ausencia de fallback | CA-012-14/15/16 | BE-012-09 y FE-012-06 |
| CA-005-02/04: importador común y continuidad contable de tipos permitidos | CA-012-06/09/10/11 | BE-012-02/03 y FE-012-05 |

La aprobación histórica de SPEC-004/005 se conserva identificada como evidencia anterior. La actualización actual requiere sus propias pruebas y QA; no se duplican tareas ni se añade una dependencia circular de preparación desde esas specs hacia SPEC-012.

La spec permanece en Borrador: disponer de este plan preliminar no la hace lista para desarrollar ni acredita implementación o QA.
