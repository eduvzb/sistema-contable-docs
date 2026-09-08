
# Sistema Contable — Escenarios Contables

> **Documento de referencia:** `04-accounting-scenarios.md`  
> **Nota en este vault:** [004 - Escenarios contables](004%20-%20Escenarios%20contables.md)
> **Estado:** Borrador funcional  
> **Audiencia:** Contadores, responsables de negocio, producto y desarrollo  
> **Propósito:** Describir los escenarios contables que el sistema debe poder representar  
> **Última actualización:** 2026-08-31

**Navegación:** [Inicio](00%20-%20Inicio.md) · [MVP](003%20-%20MVP-Scope.md) · [Reglas](005%20-%20Reglas%20de%20negocio.md) · [Guía explicada](Conceptos/Gu%C3%ADa%20Explicada%20de%20Escenarios%20Contables.md)

---

# 1. Propósito

Este documento describe los principales escenarios contables que el sistema deberá soportar.

No pretende definir todavía todas las reglas fiscales ni las cuentas exactas utilizadas por el despacho.

Su objetivo es establecer:

- qué sucede en cada operación;
- qué documentos participan;
- qué movimientos deben poder representarse;
- qué relaciones deben conservarse;
- qué resultados deben poder consultarse;
- qué aspectos siguen pendientes de validar.

Cuando una regla contable exacta no haya sido confirmada, el escenario se mantiene como estructura funcional y se marca como:

```text
PENDIENTE DE VALIDAR
```

---

# 2. Convenciones

## Documento fiscal

Se utilizará:

```text
FiscalDocument
```

para representar un CFDI importado al sistema.

## Póliza contable

Se utilizará:

```text
AccountingPolicy
```

## Partida contable

Se utilizará:

```text
AccountingPolicyEntry
```

## Estado de las reglas

Los escenarios pueden contener:

- **CONFIRMADO:** identificado directamente en el levantamiento.
- **SUPUESTO MVP:** comportamiento provisional.
- **PENDIENTE DE VALIDAR:** requiere confirmación del despacho.

---

# 3. Escenario AC-001 — Ingreso PUE

**Estado:** PENDIENTE DE VALIDAR

## Contexto

La empresa emite un CFDI de ingreso con método de pago PUE.

El contador desea registrar la operación dentro del periodo correspondiente.

## Entrada

- empresa;
- periodo;
- CFDI emitido;
- importe;
- impuestos;
- forma de pago;
- cuentas contables seleccionadas por el contador.

## Flujo

```text
FiscalDocument emitido
    ↓
Selección del documento
    ↓
Creación de AccountingPolicy
    ↓
Registro de AccountingPolicyEntries
    ↓
Asignación de cuentas
    ↓
Validación de cargos y abonos
    ↓
Contabilización
```

## Resultado esperado

- el CFDI queda relacionado con la póliza;
- la póliza queda balanceada;
- las partidas afectan las cuentas correspondientes;
- el movimiento aparece en la balanza;
- el documento puede identificarse como contabilizado.

## Cuentas potencialmente involucradas

- clientes;
- bancos;
- ventas;
- IVA trasladado.

## Pendiente de validar

- asiento contable exacto;
- momento del reconocimiento del cobro;
- tratamiento exacto de IVA;
- cuentas utilizadas por cada empresa.

---

# 4. Escenario AC-002 — Egreso PUE

**Estado:** PENDIENTE DE VALIDAR

## Contexto

La empresa recibe un CFDI correspondiente a una compra o gasto con método de pago PUE.

## Flujo

```text
FiscalDocument recibido
    ↓
Selección del documento
    ↓
Creación de AccountingPolicy
    ↓
Selección de proveedor / acreedor
    ↓
Asignación de cuentas
    ↓
Registro de partidas
    ↓
Validación
    ↓
Contabilización
```

## Resultado esperado

- el CFDI queda relacionado;
- la póliza queda balanceada;
- el gasto, compra o activo queda registrado;
- el movimiento afecta la balanza;
- el documento puede identificarse como contabilizado.

## Cuentas potencialmente involucradas

- proveedores;
- acreedores;
- bancos;
- gastos;
- compras;
- IVA acreditable.

## Pendiente de validar

- tratamiento exacto de PUE;
- diferencias entre proveedor y acreedor;
- reglas de deducibilidad;
- cuentas fiscales;
- IVA.

---

# 5. Escenario AC-003 — Factura PPD pendiente de pago o cobro

**Estado:** PENDIENTE DE VALIDAR

## Contexto

Existe un CFDI PPD cuyo pago o cobro todavía no ha ocurrido.

El sistema debe poder registrar la existencia de la operación sin asumir que el dinero ya fue recibido o pagado.

## Flujo conceptual

```text
FiscalDocument PPD
    ↓
Registro contable inicial
    ↓
Cuenta por cobrar / cuenta por pagar
    ↓
Operación pendiente
```

La operación podrá generar posteriormente nuevos movimientos cuando ocurran los pagos.

## Resultado esperado

- el CFDI queda registrado;
- puede existir una AccountingPolicy inicial;
- la operación permanece pendiente de liquidación;
- posteriormente pueden relacionarse complementos y nuevas pólizas;
- debe mantenerse el saldo pendiente.

## Pendiente de validar

- uso de provisión;
- cuentas exactas;
- tratamiento inicial de IVA;
- momento de reconocimiento de impuestos;
- diferencias entre ingresos y egresos.

---

# 6. Escenario AC-004 — Pago parcial de factura PPD

**Estado:** PENDIENTE DE VALIDAR

## Contexto

Una factura PPD no se liquida completamente.

Ejemplo:

```text
Factura: $100,000
Pago:     $40,000
Pendiente: $60,000
```

## Flujo

```text
FiscalDocument
    ↓
PaymentComplement
    ↓
AccountingPolicy de pago/cobro
    ↓
Actualización del saldo pendiente
```

## Resultado esperado

- el complemento queda relacionado con la factura;
- el pago queda relacionado con una póliza;
- la factura conserva saldo pendiente;
- se conserva el importe ya pagado/cobrado;
- la trazabilidad permite reconstruir la operación.

## Pendiente de validar

- movimiento exacto de IVA;
- cuentas contables;
- forma de calcular saldos;
- comportamiento cuando el complemento incluye varias facturas.

---

# 7. Escenario AC-005 — Múltiples pagos en distintos periodos

**Estado:** CONFIRMADO COMO NECESIDAD FUNCIONAL

## Contexto

Una misma factura recibe pagos parciales en diferentes periodos.

Ejemplo:

```text
Factura: $100,000

Julio:
$50,000

Agosto:
$50,000
```

## Flujo

```text
FiscalDocument
├── PaymentComplement julio
│   └── AccountingPolicy julio
└── PaymentComplement agosto
    └── AccountingPolicy agosto
```

## Resultado esperado

- la factura puede relacionarse con múltiples pólizas;
- cada pago conserva su periodo;
- cada complemento conserva su relación con la factura;
- el saldo pendiente puede consultarse;
- la operación puede reconstruirse cronológicamente.

## Regla funcional

```text
FiscalDocument N:M AccountingPolicy
```

cuando el proceso contable lo requiera.

## Pendiente de validar

- tratamiento del IVA entre periodos;
- movimientos exactos;
- reglas cuando existen diferencias entre factura y pagos.

---

# 8. Escenario AC-006 — Varios XML en una misma póliza

**Estado:** CONFIRMADO COMO NECESIDAD FUNCIONAL

## Contexto

El contador desea contabilizar varios documentos dentro de una misma póliza.

## Flujo

```text
FiscalDocument A ─┐
FiscalDocument B ─┼──→ AccountingPolicy
FiscalDocument C ─┘
```

## Resultado esperado

- una póliza puede relacionarse con múltiples documentos;
- puede consultarse qué documentos forman parte de la póliza;
- cada documento conserva su trazabilidad;
- la póliza contiene las partidas necesarias para representar la operación.

## Pendiente de validar

- restricciones sobre qué documentos pueden agruparse;
- reglas de numeración o concepto;
- diferencias por tipo de póliza.

---

# 9. Escenario AC-007 — Un XML relacionado con varias pólizas

**Estado:** CONFIRMADO COMO NECESIDAD FUNCIONAL

## Contexto

Una misma factura puede producir diferentes movimientos contables.

Ejemplo:

```text
Factura PPD
├── AccountingPolicy inicial
├── AccountingPolicy pago 1
└── AccountingPolicy pago 2
```

## Resultado esperado

Desde el documento debe ser posible consultar todas las pólizas relacionadas.

Desde cada póliza debe ser posible regresar al documento origen.

---

# 10. Escenario AC-008 — Póliza sin CFDI

**Estado:** PENDIENTE DE VALIDAR

## Contexto

Existen movimientos contables que pueden no originarse directamente en un CFDI.

Ejemplos potenciales:

- ajuste;
- reclasificación;
- cierre;
- corrección interna.

## Flujo

```text
AccountingPolicy
    ↓
AccountingPolicyEntries
    ↓
Accounts
```

sin requerir:

```text
FiscalDocument
```

## Resultado esperado

La relación con documentos fiscales debe ser opcional.

## Implicación funcional

```text
AccountingPolicy → FiscalDocument
```

no debe ser una dependencia obligatoria.

---

# 11. Escenario AC-009 — Provisión

**Estado:** PENDIENTE DE VALIDAR

## Contexto

Se registra una operación antes de que ocurra el movimiento efectivo de dinero.

Puede utilizarse para representar:

- una cuenta por cobrar;
- una cuenta por pagar;
- un ingreso pendiente;
- un gasto pendiente.

## Flujo conceptual

```text
FiscalDocument
    ↓
AccountingPolicy de provisión
    ↓
Cuenta por cobrar / pagar
    ↓
Pago o cobro posterior
```

## Resultado esperado

El sistema debe poder diferenciar el registro inicial de la operación del movimiento posterior de dinero.

## Pendiente de validar

- cuándo se utiliza;
- tipos de póliza;
- cuentas;
- tratamiento de IVA;
- reglas por tipo de operación.

---

# 12. Escenario AC-010 — IVA pendiente y pago posterior

**Estado:** PENDIENTE DE VALIDAR

## Contexto

Una operación PPD puede requerir distinguir entre el IVA registrado inicialmente y el IVA asociado al momento en que ocurre el pago o cobro.

## Flujo conceptual

```text
Factura
    ↓
IVA pendiente
    ↓ pago/cobro
IVA efectivamente pagado/cobrado
```

## Resultado esperado

El sistema debe ser capaz de representar el cambio de estado contable del IVA sin perder relación con:

- factura;
- complemento;
- póliza;
- periodo.

## Pendiente de validar

- cuentas exactas;
- reglas de reconocimiento;
- pagos parciales;
- diferencias entre ingresos y egresos.

---

# 13. Escenario AC-011 — Póliza descuadrada en borrador

**Estado:** SUPUESTO MVP

## Contexto

El contador comienza a preparar una póliza pero todavía no termina de capturar las partidas.

## Comportamiento propuesto

Se permite:

```text
Guardar como borrador
```

aunque:

```text
SUM(cargos) != SUM(abonos)
```

No se permite:

```text
Contabilizar
```

hasta que:

```text
SUM(cargos) = SUM(abonos)
```

## Pendiente de validar

- si el despacho requiere guardar pólizas incompletas;
- si existe otro estado equivalente;
- cuándo una póliza se considera definitiva.

---

# 14. Escenario AC-012 — Consulta de trazabilidad desde un CFDI

**Estado:** CONFIRMADO COMO NECESIDAD FUNCIONAL

## Contexto

El contador localiza un CFDI y desea saber cómo fue contabilizado.

## Resultado esperado

Desde el documento debe poder consultar:

- estado;
- pólizas relacionadas;
- periodos;
- partidas relacionadas;
- cuentas afectadas;
- complementos;
- pagos registrados.

Ejemplo:

```text
FiscalDocument
├── AccountingPolicy #001
│   ├── Account A
│   └── Account B
└── AccountingPolicy #034
    ├── Account C
    └── Account D
```

---

# 15. Escenario AC-013 — Consulta de trazabilidad desde una póliza

**Estado:** CONFIRMADO COMO NECESIDAD FUNCIONAL

## Contexto

El contador consulta una póliza y desea conocer qué documentos originaron o respaldan el movimiento.

## Resultado esperado

Debe poder consultar:

- XML relacionados;
- UUID;
- emisor/receptor;
- importes;
- complementos relacionados;
- periodo.

---

# 16. Escenario AC-014 — Balanza después de contabilizar

**Estado:** CONFIRMADO COMO NECESIDAD FUNCIONAL

## Contexto

Después de registrar pólizas, el contador consulta la balanza.

## Resultado esperado

Por cuenta debe poder observar, como mínimo:

```text
Saldo inicial
+ cargos
- abonos
= saldo final
```

La fórmula exacta de presentación dependerá de la naturaleza de las cuentas.

El objetivo funcional es que las pólizas contabilizadas afecten los saldos consultables.

---

# 17. Escenario AC-015 — Documento duplicado

**Estado:** SUPUESTO MVP

## Contexto

El usuario intenta importar nuevamente un CFDI cuyo UUID ya existe para la empresa.

## Comportamiento propuesto

El sistema debe:

- identificar el duplicado;
- evitar crear un segundo documento fiscal equivalente;
- informar al usuario.

## Pendiente de validar

- si pueden existir excepciones;
- manejo de XML corregidos;
- relación con sustituciones.

---

# 18. Escenario AC-016 — Descarga simulada de XML

**Estado:** DEFINIDO PARA MVP

## Contexto

El cliente desea visualizar cómo funcionará en el futuro la obtención automática de documentos fiscales.

En el MVP no existirá todavía integración real con SAT.

## Flujo

```text
Seleccionar empresa
    ↓
Solicitar descarga
    ↓
Servicio externo simulado
    ↓
Documentos encontrados
    ↓
Incorporación al repositorio
    ↓
Consulta / contabilización
```

## Resultado esperado

El usuario puede validar:

- cómo inicia el proceso;
- cómo sabe que se está ejecutando;
- qué documentos fueron encontrados;
- cómo llegan a su bandeja;
- cómo continúa el flujo contable.

## Fuera de este escenario

- autenticación real con SAT;
- certificados;
- credenciales fiscales;
- sincronización real;
- errores oficiales;
- consulta real de cancelaciones.

---

# 19. Escenarios posteriores al MVP

Los siguientes casos se consideran relevantes, pero no forman parte del flujo mínimo inicial.

## AC-F01 — Cancelación de CFDI

Debe conservar documento, estado, relaciones e historial.

## AC-F02 — Sustitución de CFDI

Debe conservar relación entre documento sustituido y sustituto.

## AC-F03 — Nota de crédito

Debe relacionarse con una operación previa y reflejar su efecto contable.

## AC-F04 — Retenciones

Debe representar impuestos retenidos y sus movimientos.

## AC-F05 — Moneda extranjera

Debe conservar moneda, tipo de cambio e importe convertido.

## AC-F06 — Cierre contable

Debe controlar cuándo un periodo deja de aceptar modificaciones.

## AC-F07 — Reapertura

Debe permitir modificar excepcionalmente un periodo cerrado con trazabilidad.

## AC-F08 — Póliza de cierre

Debe representar movimientos propios del cierre contable.

## AC-F09 — Conciliación bancaria

Debe comparar movimientos bancarios con movimientos contables.

## AC-F10 — Contabilidad electrónica

Debe generar la información fiscal requerida cuando se incorpore esta función.

---

# 20. Escenarios prioritarios para validar con el primer MVP

Los escenarios que deberían probarse primero son:

```text
AC-001 Ingreso PUE
AC-002 Egreso PUE
AC-003 Factura PPD
AC-004 Pago parcial
AC-005 Pagos en distintos periodos
AC-006 Varios XML en una póliza
AC-007 Un XML en varias pólizas
AC-008 Póliza sin CFDI
AC-011 Póliza en borrador
AC-012 Trazabilidad desde CFDI
AC-014 Balanza
AC-016 Descarga simulada
```

Estos escenarios permiten validar el núcleo del modelo antes de incorporar automatización o fiscalización avanzada.

---

# 21. Pregunta que debe responder este documento

> **¿Puede el modelo del sistema representar correctamente las principales situaciones que un contador necesita registrar durante la operación mensual?**

Las cuentas exactas, reglas fiscales y excepciones deberán confirmarse progresivamente sin impedir que el modelo funcional avance.
