# Plan técnico — SPEC-007

Este archivo describe la ejecución técnica de [SPEC-007](spec.md); los criterios funcionales vigentes y el estado sólo se definen allí.

## Contexto para ejecución

El alcance y los criterios de esta entrega están en [spec.md](spec.md); las tareas abiertas por repositorio identifican el trabajo pendiente. Consulta los contratos de las specs dependientes que esta ejecución consume. Las fuentes ya citadas en `spec.md` se reabren sólo ante una contradicción, un cambio posterior de regla o contrato, un supuesto que afecte el resultado, o una solicitud explícita de cambiar comportamiento.

## Plan técnico y contratos

- Backend: extraer `DoctoRelacionado/@IdDocumento` e `ImpPagado` de CFDI 4.0 tipo `P`, persistir una asignación documental con UUID e importe, resolver el documento si pertenece a la misma empresa y extender el detalle fiscal en ambos sentidos. Reutilizar los contratos de pólizas de SPEC-006. No crear una entidad `PaymentComplement` independiente.
- Frontend: detalle fiscal con facturas relacionadas desde un complemento y complementos desde una factura, importes asignados y pólizas/periodos existentes. No mostrar saldo ni estado de liquidación.
- Ejemplo documental de factura PPD y complemento de pago: [ejemplos de XML CFDI](../../docs/ejemplos/README.md).
- Los importes de asignación se almacenan con seis decimales y se representan como texto. El cálculo, las diferencias, los sobrepagos y los errores asociados quedan para una ampliación que deberá actualizar esta spec antes de modificar consumidores.

### Contrato de trazabilidad documental

La importación de un CFDI 4.0 tipo `P` conserva sus referencias `DoctoRelacionado` en una colección `payment_allocations`. Cada elemento contiene:

```json
{
  "related_uuid": "11111111-1111-4111-8111-111111111111",
  "invoice_id": 42,
  "allocated_amount": "40000.000000"
}
```

`invoice_id` es `null` cuando el UUID todavía no está importado en la misma empresa o pertenece a otra empresa. No se crea un `FiscalDocument` ficticio. Desde el detalle de una factura, `payment_complements` expone `id`, `uuid`, `issued_at` y `allocated_amount`; desde el detalle del complemento, `payment_allocations` expone los datos anteriores y, cuando existe, el resumen de la factura relacionada. Las colecciones conservan un orden estable por el identificador de asignación.

Las asignaciones se autorizan con el mismo acceso a la empresa del documento. Una referencia coincidente en otra empresa no se enlaza ni se serializan sus datos. Las pólizas y periodos se consultan mediante `accounting_policies` de SPEC-006; este contrato no añade saldo, liquidación ni cálculo contable.

Aplican las [decisiones técnicas compartidas](../../docs/decisiones.md). El contrato de trazabilidad de este alcance queda cerrado; cualquier ampliación de saldos o tratamiento de pagos debe actualizar esta spec antes de modificar consumidores.

## Orden y coordinación

Las tareas pendientes se registran por repositorio en [backend](tasks-backend.md) y [frontend](tasks-frontend.md). El contrato responsable se prepara antes de implementarlo en un consumidor; las comprobaciones reales se registran en [verificación](verificacion.md).
