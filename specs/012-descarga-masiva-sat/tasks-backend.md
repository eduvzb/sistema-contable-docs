# Tareas de backend — SPEC-012

Desglose de [spec.md](spec.md) y [plan.md](plan.md). El usuario autorizó implementar la primera etapa controlada para pruebas humanas. Las tareas completas siguientes permanecen abiertas porque incluyen conexión y comprobaciones no cubiertas por esa etapa; no se retiran como si todos sus «Hecho cuando» estuvieran acreditados. El usuario confirma aprobación fiscal/legal y autorización de titulares para custodia de clientes; dimensionamiento y contraste SAT de la funcionalidad completa siguen pendientes.

## Dependencias previas

- **Diseño de credenciales definido:** carpeta privada de aplicación, archivos cifrados, clave fuera del código, referencia de autorización y reemplazo atómico. Los contratos de las operaciones de descarga permanecen en el plan; productores históricos, límites de ejecución/carga y ventana efectiva SAT siguen pendientes para esas partes.
- **Aprobación confirmada por el usuario:** existe aprobación fiscal/legal y autorización de titulares para custodia de empresas cliente. BE-012-04 concreta la implementación solicitada: archivos/contraseña cifrados en carpeta privada de aplicación, clave fuera del código, autorización vigente y reemplazo validado/atómico. No requiere diseñar un proveedor de secretos ni un sistema adicional de respaldo para esta entrega.
- **Coordinación documental completada:** criterios, planes y tareas de SPEC-004/005 enlazados con la correspondencia de [plan.md](plan.md#correspondencia-con-spec-004005). Las tareas siguientes concentran su implementación pendiente; no se duplican ni se considera aprobada por la QA histórica.
- Implementar requiere autorización expresa adicional. Las condiciones de cierre siguientes describen comprobaciones futuras; sus resultados deberán registrarse en [verificacion.md](verificacion.md), ejecutando pruebas con Sail conforme al flujo.

## Tareas pendientes

- [ ] **BE-012-01 — Persistir solicitudes y reservar una descarga activa por empresa.**
  - CA: CA-012-01, CA-012-02, CA-012-03, CA-012-04, CA-012-05, CA-012-14.
  - Depende de: contratos técnicos de solicitudes, datos, fechas y reserva; autorización de implementación. Coordinación documental completada.
  - Hecho cuando: la selección validada persiste con empresa, periodo, solicitante y seguimiento; peticiones concurrentes no crean dos procesos activos de la misma empresa, otras empresas siguen independientes y las consultas ajenas se rechazan. Hoy se calcula en America/Mexico_City, sin desplazar días de emisión ni cambiar globalmente la zona del sistema; se rechazan fechas futuras y se admiten históricos 4.0 según límites SAT, sin corte artificial en abril de 2023. Las pruebas de validación, medianoche/zonas distintas, persistencia, aislamiento y concurrencia están ejecutadas y documentadas.
  - Contrato preparado: rutas de creación/consulta e idempotencia; slot empresarial separado de reservas contables. Probar clave repetida con entrada igual/diferente, contexto capturado y autorización vigente incluso al repetir clave.

- [ ] **BE-012-02 — Admitir nómina y traslado sólo para consulta fiscal.**
  - CA: CA-012-06, CA-012-07, CA-012-14.
  - Depende de: contratos técnicos de importación y consulta de tipos; coordinación con SPEC-004 y consumidores contables; autorización de implementación.
  - Hecho cuando: el importador compartido admite los cinco tipos en CFDI 4.0 y conserva los datos generales; rechaza versiones/RFC no admitidos y bloquea nuevas relaciones con pólizas y propuestas para N/T, sin inclusión automática en DIOT ni alteración de relaciones históricas. Pruebas válidas, errores y regresiones de I/E/P, pagos, conceptos, pólizas y DIOT ejecutadas con evidencia.

- [ ] **BE-012-03 — Conservar originales y completar los faltantes sin modificar documentos.**
  - CA: CA-012-07, CA-012-09, CA-012-10, CA-012-11, CA-012-14.
  - Depende de: BE-012-02; contratos técnicos de almacenamiento, integridad y comparación de datos históricos; coordinación con SPEC-004.
  - Hecho cuando: nuevas incorporaciones manuales y del importador SAT guardan originales privados exactos; los históricos pueden seguir sin archivo; un duplicado compatible completa sólo el original faltante y uno incompatible informa diferencias sin modificar registro, pólizas ni original conservado. Fallos de archivo/base de datos y carreras entre importaciones no dejan éxitos falsos, referencias rotas ni documentos repetidos. Pruebas de precisión decimal, ausencia histórica, integridad y acceso registradas, sin habilitar descarga al equipo.
  - Cobertura adicional: esenciales ausentes producen rechazo por campo; histórico sin conceptos/descuento/desglose puede completar sólo el archivo si coincide lo conservado, sin rellenar esos campos e informando comparación limitada. Probar cero/lista vacía realmente conservados frente a ausencia histórica, total cero válido, moneda XXX y decimales equivalentes. No abrir una revisión humana ni afirmar autenticidad/vigencia SAT por comparar datos.
  - Contrato preparado: `outcomes` canónicos y proyecciones de compatibilidad, comparación desde columnas originales y transacción por documento/resultado. Antes de ejecutar, auditar productores históricos; no usar el Resource que transforma null en lista vacía ni omitir campos con procedencia desconocida.

- [ ] **BE-012-04 — Proteger el ciclo de vida y la autorización de la e.firma.**
  - CA: CA-012-12, CA-012-13, CA-012-14, CA-012-17, CA-012-18, CA-012-19, CA-012-20, CA-012-21, CA-012-29.
  - Depende de: contrato técnico de credenciales, aceptación, evidencia de autorización, auditoría, claves y eliminación; autorización de implementación.
  - Hecho cuando: administrador y contador con asignación vigente pueden cargar o reemplazar FIEL con aceptación y evidencia requeridas; sólo el administrador puede retirarla. El reemplazo valida empresa, RFC y credencial nueva, y persiste archivos/contraseña cifrados en `storage/app/private/fiel/{companyId}`, fuera de Git y webroot; un fallo conserva íntegra la credencial anterior. La llave de cifrado no se guarda con los archivos. Los secretos no son recuperables desde la interfaz ni aparecen en registros, colas o respuestas; el retiro impide nuevas comunicaciones sin borrar XML/historial. Pruebas de roles, RFC/vigencia, cifrado, error de reemplazo y ausencia de exposición documentadas. Sin secretos ni comunicaciones SAT reales en pruebas automatizadas.

- [ ] **BE-012-05 — Presentar las consultas SAT del proceso y conservar sus identificadores.**
  - CA: CA-012-01, CA-012-02, CA-012-03, CA-012-08, CA-012-13, CA-012-14, CA-012-19.
  - Depende de: BE-012-01 y BE-012-04; contrato técnico del adaptador SAT, descomposición por dirección/tipos y tratamiento de envíos inciertos; infraestructura de ejecución de BE-012-10 para operación persistente.
  - Hecho cuando: una selección local se comunica al SAT sólo con su RFC, rango, tipos y estado vigente, guardando cada identificador confirmado. Falta de credencial, envío sin respuesta concluyente y rechazos/límites se distinguen sin simular resultados ni reenviar automáticamente. Pruebas con respuestas controladas documentan selección, aislamiento, códigos de error e incertidumbre; no utilizan e.firmas reales ni consumen cuotas SAT.
  - Contrato preparado: una consulta por combinación dirección/tipo (una a diez), secuencial, sin ampliar selección; adaptador tipado e intención externa persistida. Probar fallo en la primera o intermedia sin enviar las restantes ni repetir `UNKNOWN`.

- [ ] **BE-012-06 — Seguir consultas, guardar paquetes e incorporar sus XML.**
  - CA: CA-012-03, CA-012-05, CA-012-06, CA-012-07, CA-012-08, CA-012-09, CA-012-10, CA-012-11, CA-012-22.
  - Depende de: BE-012-03 y BE-012-05; contratos técnicos de seguimiento, paquetes, límites y resultado consolidado.
  - Hecho cuando: el proceso persiste sin pantalla abierta, consulta avances, muestra espera prolongada desde las 24 horas de aceptación de cada consulta sin detenerla, descarga paquetes privados y utiliza el importador común. El resultado distingue todos los paquetes pendientes de una importación completa, parcial o vacía; un rechazo individual no elimina incorporaciones válidas. Pruebas de reloj, múltiples consultas/paquetes, filtros, límites/vencimiento y errores de almacenamiento/procesamiento ejecutadas con evidencia.
  - Cobertura adicional: valores configurables iniciales del plan (verificación cada 5 minutos, conexión hasta 10 segundos, comunicaciones hasta 60 segundos o descarga hasta 180 segundos), bloques secuenciales de hasta 50 XML y límite individual de 10 MiB. Probar timeout sin reenvío automático, rechazo individual, ZIP peligroso/tamaños falsos y exceso de recursos sin éxito completo aparente. Los máximos totales de paquetes y recursos dependen del dimensionamiento pendiente, no de una cifra inferida de volumen.

- [ ] **BE-012-07 — Reanudar o detener procesos sin duplicar operaciones.**
  - CA: CA-012-04, CA-012-08, CA-012-14, CA-012-20, CA-012-23, CA-012-24.
  - Depende de: BE-012-01, BE-012-04 y BE-012-06; contratos técnicos de reanudación, detención y sincronización de ejecución.
  - Hecho cuando: fallo/retiro/detención liberan la reserva; administrador o contador actualmente asignado pueden detener aunque no iniciaran el proceso. Reanudar es manual, adquiere reserva sólo sin otra activa, reutiliza identificadores/paquetes y no revive al restaurar credenciales ni por trabajo antiguo encolado. Pruebas de carreras, pérdida de acceso, credenciales cambiadas, envíos inciertos y paquetes locales documentan que no se reintenta automáticamente ni se promete cancelación remota.
  - Contrato preparado: estado transitorio `STOPPING`, generación de ejecución y retiro serializado con inicio de comunicación; no liberar slot mientras siga ejecutándose la unidad anterior. Probar worker vivo, worker terminado y respuesta externa tardía antes de dar por comprobada la recuperación tras caídas.

- [ ] **BE-012-08 — Consultar historial, avances y resultados sin exponer secretos.**
  - CA: CA-012-03, CA-012-05, CA-012-07, CA-012-10, CA-012-14, CA-012-19, CA-012-22, CA-012-23, CA-012-24.
  - Depende de: BE-012-01; contrato técnico de consulta e historial. Los casos completos requieren BE-012-06 y BE-012-07.
  - Hecho cuando: consultas autorizadas devuelven selección inicial, estado local/SAT distinguido, avances y resultados por documento, incluyendo original completado y diferencias rechazadas, sin archivos públicos ni credenciales. Historial y resultado siguen disponibles tras cerrar sesión y no mezclan empresas. Pruebas de consulta, aislamiento, auditoría y estados persistentes ejecutadas con evidencia.
  - Contrato preparado: historial paginado de 25, resultados de 50; detalle con consultas/resumen sin todos los XML. Probar recuentos sin sumar proyecciones y duplicados entre consultas como si fueran nuevos documentos.

- [ ] **BE-012-09 — Restringir la simulación y exigir confirmación.**
  - CA: CA-012-14, CA-012-15, CA-012-16.
  - Depende de: contrato técnico de confirmación de simulación; coordinación con SPEC-005; autorización de implementación.
  - Hecho cuando: sólo administrador puede ejecutar la simulación confirmada en cualquier empresa; petición directa de contador o sin confirmación no incorpora documentos. No se consulta SAT ni se usan credenciales reales. Pruebas de permisos, confirmación, cancelación, resultado vacío/parcial, duplicados y ausencia de fallback automático ejecutadas con evidencia; no se eliminan documentos ficticios previos.

- [ ] **BE-012-10 — Verificar operación persistente y almacenamiento privado.**
  - CA: CA-012-03, CA-012-09, CA-012-14, CA-012-21.
  - Depende de: contratos técnicos de ejecución y almacenamiento; revisión jurídica/política aprobada para la parte de credenciales; autorización de implementación y de cualquier intervención en el VPS, que no se concede con este desglose.
  - Hecho cuando: procesos de trabajo y seguimiento pueden recuperarse tras reinicio; archivos temporales, originales y respaldos tienen acceso privado y recuperación comprobada. Para credenciales, claves separadas y eliminación/respaldos cumplen la política aprobada sin reactivar credenciales retiradas al restaurar. La evidencia distingue pruebas controladas de la comprobación real del entorno; configuración presente en el repositorio no se toma como despliegue comprobado.
  - Cobertura adicional: confirmar capacidad de RAM, CPU y disco y dimensionar memoria, espacio temporal, paquetes comprimidos/descomprimidos, entradas y concurrencia global mediante pruebas controladas. Registrar el volumen mensual desconocido sin inventar una carga de producción; no habilitar paquetes sin límites seguros definidos y comprobados.
