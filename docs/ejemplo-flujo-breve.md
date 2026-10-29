# Ejemplo de uso del flujo (hipotético)

## Cambio pequeño: aclarar un mensaje

**Petición:** hacer más claro el error cuando un periodo está reservado por otra persona.

- **Investigar:** localizar el mensaje, el conflicto `PERIOD_RESERVED` y su prueba de interfaz en SPEC-002/006 y el frontend.
- **Cambiar:** sólo el texto, sin alterar permisos, reservas ni respuesta del servidor.
- **Comprobar:** prueba de componente afectada, `pnpm lint` y `pnpm typecheck`; comunicar resultados reales. **No crear spec ni PR por rutina.**

**Ensayo de coordinación:** fase por confirmar hasta revisar código; si el texto es el único cambio, implementación directa en frontend, sin subagente. Estatus: «pendiente de comprobar la prueba afectada». No se afirma que esa prueba se ejecutó.

## Cambio complejo: regla nueva de reserva

**Objetivo propuesto:** definir qué ocurre si un usuario intenta guardar una póliza mientras otra persona tiene reservado el periodo. Antes de escribir código, confirmar con el usuario si esta regla difiere de la ya definida en [SPEC-002](../specs/002-contexto-contable/spec.md) y [SPEC-006](../specs/006-polizas-trazabilidad/spec.md). Si no difiere, basta con investigar y probar un posible defecto.

Si realmente cambia la regla, ampliar la spec responsable con sólo lo nuevo:

| Situación | Resultado a acordar |
|---|---|
| Otra persona tiene la reserva al guardar | ¿Qué operación se rechaza y qué datos de la captura se conservan? |
| La reserva cambia entre abrir y guardar | ¿Qué valida el servidor y qué ve el usuario? |

Sólo después de resolver esas preguntas: plan corto para el contrato y la concurrencia si cambian; pruebas backend del rechazo sin escrituras parciales y pruebas frontend de conservación de captura. Registrar resultados ejecutados y QA visual pendiente si aplica. Ninguna respuesta en esta tabla se considera aprobada ni implementada.

**Ensayo de coordinación:** fase de aclaración; bloqueo: distinguir la regla propuesta de SPEC-002/006. El coordinador pregunta antes de delegar código; no se crea una spec nueva por suposición.

## Trabajo entre repositorios: contrato acordado

**Supuesto sólo para ensayar el reparto:** el usuario ya acordó un contrato de error nuevo para una operación de póliza. No se propone cambiar el contrato real de Braval ni se considera aprobada esta idea.

**Ensayo de coordinación:** fase de implementación, condicionada a comprobar el contrato en código. El coordinador conserva la decisión y encarga a dos instancias del mismo desarrollador: backend se ocupa de API y prueba de rechazo sin escritura; frontend, de mostrar el error conservando la captura y su prueba de componente. Cada encargo identifica checkout, archivos propios y skill pertinente. Nadie edita archivos del otro. Al recibir resultados, el coordinador contrasta ambos lados y ejecuta o coordina la verificación final; las pruebas que compartan PostgreSQL `testing` se ejecutan en serie. Estatus al usuario: «backend/front en curso; integración y pruebas conjuntas pendientes». No se acredita un PR ni una prueba hipotética.
