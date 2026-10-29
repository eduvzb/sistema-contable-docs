# Tareas de frontend — SPEC-012

Desglose de [spec.md](spec.md) y [plan.md](plan.md). Se autorizó implementar la primera etapa controlada para pruebas humanas. Las tareas completas siguen abiertas porque la operación real y sus controles no están verificados; el usuario confirma aprobación fiscal/legal y autorización de titulares para custodia de clientes, sin que ello acredite integración o despliegue productivo.

## Dependencias previas

- Contratos técnicos compartidos propuestos en [plan.md](plan.md#contrato-http), pendientes de revisión y de los puntos condicionados allí indicados; coordinación documental de SPEC-004/005 completada. La interfaz puede implementarse con respuestas ficticias sólo tras autorización de implementación y cierre del contrato afectado; no debe anunciar operaciones reales que el backend aún no admita.
- FE-012-01 y la habilitación de credenciales reales dependen de integrar la política y evidencia de autorización que el usuario confirma como aprobadas, además de completar controles técnicos y comprobación de producción.
- Mantener la arquitectura de la feature fiscal: componentes → hooks → API de feature → cliente compartido; contratos compartidos sin duplicarlos en componentes. Ninguna tarea ejecuta acciones en el VPS.
- Cada condición de cierre incluye pruebas de interacción con Vitest y React Testing Library, sin sustituirlas por snapshots ni exigir recorrido integral por navegador. Registrar evidencia en [verificacion.md](verificacion.md); la revisión visual queda para QA humana.

## Tareas pendientes

- [ ] **FE-012-07 — Observar y detener el piloto local sin cargar FIEL por web.**
  - CA: CA-012-25, CA-012-03/05/08/14/22/23/24.
  - Depende de: BE-012-11 y contrato del piloto local temporal del plan.
  - Hecho cuando: historial distingue registros reales de pruebas, estado SAT, espera, incertidumbre y reanudación en terminal; permite detener con permiso vigente y explica STOPPING sin prometer cancelación SAT. No ofrece carga de FIEL ni reanudación real web; pruebas de interacción y regresiones ejecutadas.

- [ ] **FE-012-01 — Cargar y administrar credenciales con autorización previa.**
  - CA: CA-012-12, CA-012-13, CA-012-14, CA-012-17, CA-012-18, CA-012-19, CA-012-20, CA-012-21, CA-012-29.
  - Depende de: contrato técnico de credenciales/aceptación y de edición de empresa; política aprobada y evidencia de autorización; BE-012-04 para integración real; autorización de implementación.
  - Hecho cuando: administrador y contador asignado ven carga inicial y reemplazo desde la edición de empresa; sólo administrador ve retiro y ningún rol recupera secretos guardados. Sin aceptación y referencia de autorización requeridas no se transmiten archivos/contraseña; cambios de empresa o cierre del formulario no conservan adjuntos ni secretos. La interfaz explica finalidad, impacto del retiro y límites sin prometer revocación SAT. Pruebas de roles, aceptación previa, errores, limpieza de selección y ausencia de secretos ejecutadas con evidencia.

- [ ] **FE-012-02 — Solicitar descargas por periodo, dirección y tipos.**
  - CA: CA-012-01, CA-012-02, CA-012-04, CA-012-13, CA-012-14.
  - Depende de: contrato técnico de solicitudes y contexto; BE-012-01 y BE-012-05 para integración real; autorización de implementación.
  - Hecho cuando: se eligen uno o varios de los cinco tipos y emitidos/recibidos/ambos, con días inclusivos dentro del periodo activo; faltantes, rango inválido, credencial no disponible o proceso activo se explican sin fallback simulado. El selector muestra la referencia Ciudad de México, permite hoy y comunica que no es un cierre definitivo ni una sincronización posterior; no desplaza fechas por la zona del navegador. Un cambio de contexto no envía datos de la empresa anterior y doble clic no provoca solicitudes repetidas. Pruebas de selección, fechas históricas/hoy/futuro, medianoche y zona de navegador distinta, contexto y respuestas de validación/concurrencia ejecutadas con evidencia.
  - Contrato preparado: clave idempotente por intención, 202 como aceptación local y códigos 409 para conflicto/custodia/credencial. Un error de transporte no debe producir automáticamente una nueva clave ni otro envío; recuperar estado antes de ofrecer nueva acción.

- [ ] **FE-012-03 — Mostrar historial y resultado persistente de cada descarga.**
  - CA: CA-012-03, CA-012-05, CA-012-07, CA-012-10, CA-012-14, CA-012-22.
  - Depende de: contrato técnico de historial/resultados; BE-012-08 y resultados de BE-012-06 para integración real; autorización de implementación.
  - Hecho cuando: se distinguen preparación SAT, descarga e importación local, espera prolongada, resultado vacío, importaciones válidas, duplicados, originales completados y rechazos con sus diferencias. Reabrir o volver a iniciar sesión recupera el resultado desde backend y no sólo desde memoria del navegador; respuestas tardías no mezclan empresas. Pruebas de estados, resultados parciales, consulta posterior y aislamiento ejecutadas con evidencia.
  - Contrato preparado: paginación de historial/resultados y `summary.is_complete`; tratar la espera prolongada como aviso, no fallo. No cargar todos los resultados en el detalle ni confundir cantidad SAT con nuevos documentos locales.

- [ ] **FE-012-04 — Reintentar o detener seguimiento según permisos actuales.**
  - CA: CA-012-04, CA-012-08, CA-012-14, CA-012-20, CA-012-23, CA-012-24.
  - Depende de: FE-012-03; contrato técnico de acciones y estados; BE-012-07 para integración real.
  - Hecho cuando: administrador o contador asignado pueden detener solicitudes ajenas de su empresa; la acción no se llama cancelación ante SAT. El reintento es explícito, respeta otra activa y comunica falta de credenciales, vencimiento o imposibilidad de continuar, sin programarse al abrir la pantalla o restaurar e.firma. Pruebas de permisos, conflicto, errores y ausencia de acciones automáticas ejecutadas con evidencia.

- [ ] **FE-012-05 — Integrar los nuevos tipos y resultados de importación en la bandeja.**
  - CA: CA-012-06, CA-012-07, CA-012-09, CA-012-10, CA-012-11, CA-012-14.
  - Depende de: contratos técnicos de documentos y resultados de importación; BE-012-02 y BE-012-03 para integración real; coordinación con SPEC-004; autorización de implementación.
  - Hecho cuando: nómina y traslado aparecen con datos generales y sin selección para nuevas relaciones con pólizas ni propuestas contables; las demás rutas de selección fiscal respetan la misma restricción. La importación informa original completado o incompatibilidad sin aparentar creación de un documento nuevo y reconcilia la bandeja sin duplicados, conservando filtros/contexto. No se añade descarga de originales al equipo. Pruebas de carga manual, resultados, tipos, selección contable y regresiones de I/E/P ejecutadas con evidencia.
  - Cobertura adicional: mostrar que el original se completó comparando sólo los datos históricos disponibles, sin presentar una validación integral; ante rechazo, distinguir campos esenciales faltantes de datos diferentes. Comprobar que no se anuncia actualización de conceptos/descuento/desglose ni se ofrece una revisión humana no incluida en alcance.
  - Contrato preparado: consumir `outcomes` como resultado autoritativo, sin sumar de nuevo `imported`/`rejected`; aceptar I/E/P/N/T en tipos compartidos y `original_available` sin URL. Probar los resultados nuevos antes del despliegue coordinado con el importador.

- [ ] **FE-012-06 — Reservar la simulación al administrador con advertencia previa.**
  - CA: CA-012-14, CA-012-15, CA-012-16.
  - Depende de: contrato técnico de confirmación; BE-012-09 para integración real; coordinación con SPEC-005; autorización de implementación.
  - Hecho cuando: sólo administrador ve la opción de pruebas internas, distinta de descarga real; se advierte incorporación de documentos ficticios y cancelar no envía la operación. No aparece automáticamente tras errores SAT y no se exige marca de empresa de pruebas. Pruebas de visibilidad, confirmación/cancelación, petición enviada, error y resumen de simulación ejecutadas con evidencia.
