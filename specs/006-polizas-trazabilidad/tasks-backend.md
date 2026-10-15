# Tareas de backend — SPEC-006

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

## BE-006-07 — Configuración global de reutilización

- [ ] Crear persistencia, migración inicial y endpoints de configuración según el plan.
- **CA:** CA-006-30/34/35.
- **Depende de:** ninguna tarea de esta entrega.
- **Hecho cuando:** GET devuelve el booleano persistido; PUT valida y permite cambios solo al administrador; instalaciones nuevas y existentes comienzan con `false`, sin modificar vínculos. Pruebas cubren permisos, entradas inválidas, persistencia y ausencia inesperada de configuración sin habilitar reutilización.

## BE-006-08 — Validación atómica de vínculos nuevos

- [ ] Aplicar la restricción compartida al crear y editar pólizas, conservando vínculos anteriores y serializando comprobación y escritura con la configuración.
- **CA:** CA-006-07/20/31/32/33/34.
- **Depende de:** BE-006-07.
- **Hecho cuando:** pruebas de endpoints acreditan rechazo con UUID para vínculos nuevos a documentos usados en DRAFT/POSTED y otros periodos, conservación de relaciones previas compartidas, retirada y posterior incorporación, uso permitido al activar la opción y rollback sin efectos en partidas, vínculos o sugerencias. La misma protección se aplica a peticiones manipuladas y pantallas desactualizadas; las validaciones de autorización y empresa siguen pasando.

## BE-006-09 — Concurrencia y regresiones

- [ ] Verificar conflictos entre periodos con transacciones reales y ajustar las pruebas existentes de reutilización al nuevo valor inicial.
- **CA:** CA-006-07/30/32/33/34.
- **Depende de:** BE-006-08.
- **Hecho cuando:** con dos conexiones a un motor con bloqueos reales, solo una de dos pólizas logra vincular un CFDI libre con la opción desactivada; la actualización del ajuste y el guardado se serializan sin evaluar un valor obsoleto. Las pruebas afectadas de configuración, pólizas, documentos, acceso, contexto y complementos pasan. Se registra el motor y los comandos reales en verificación, sin atribuir cobertura de concurrencia a SQLite en memoria.
