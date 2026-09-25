# Ejemplos de XML CFDI

Estos archivos son fixtures documentales para probar la importación de CFDI 4.0 en el MVP. Están alineados con [SPEC-004](../../specs/004-documentos-fiscales/spec.md) y [SPEC-007](../../specs/007-ppd-complementos/spec.md).

| Archivo | Escenario | Empresa del ejemplo |
|---|---|---|
| [`cfdi-ingreso-pue.xml`](cfdi-ingreso-pue.xml) | CFDI de ingreso emitido, cobrado en una sola exhibición (`I`/`PUE`). | `FLU010101AAA` |
| [`cfdi-egreso-ppd.xml`](cfdi-egreso-ppd.xml) | CFDI de egreso recibido, pendiente de pago (`E`/`PPD`). | `FLU010101AAA` |
| [`cfdi-pago-ppd.xml`](cfdi-pago-ppd.xml) | Complemento de pago parcial relacionado con el egreso PPD (`P`). | `FLU010101AAA` |

## Flujo representado

```text
cfdi-egreso-ppd.xml (3,712.000000)
              ▲
              │ ImpPagado = 1,500.000000
              │
cfdi-pago-ppd.xml (pago parcial)
```

Los UUID y RFC corresponden al flujo demo del seeder `CompleteFlowSeeder`. El complemento conserva el UUID de la factura en `DoctoRelacionado/@IdDocumento` y el importe parcial en `@ImpPagado`.

## Uso

Para probar la importación manual, carga uno o varios archivos desde la bandeja de documentos dentro de la empresa `FLU010101AAA` y el periodo correspondiente de 2026. También pueden usarse como cuerpos de prueba para:

```text
POST /api/companies/{companyId}/fiscal-document-imports
```

Los archivos no contienen una firma digital ni un timbre fiscal verificable por el SAT. Son ejemplos estructuralmente compatibles con el parser del MVP y no deben utilizarse como comprobantes fiscales reales.
