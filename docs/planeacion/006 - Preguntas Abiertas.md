# Sistema Contable — Preguntas Abiertas

> **Enfoque:** Dudas pendientes después del análisis de negocio, producto, escenarios, reglas y modelo de dominio

**Navegación:** [Inicio](00%20-%20Inicio.md) · [Análisis](001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md) · [Alcance](003%20-%20Alcance%20del%20producto.md) · [Escenarios](004%20-%20Escenarios%20contables.md) · [Reglas](005%20-%20Reglas%20de%20negocio.md)

---

# 1. Propósito

Este documento concentra únicamente las preguntas que siguen abiertas después de haber definido:

- contexto general del proyecto;
- glosario de dominio;
- glosario contable;
- escenarios contables;
- alcance del producto;
- reglas de negocio;
- modelo de dominio.

No pretende recopilar todas las dudas posibles.

La idea es evitar detener el proyecto por preguntas que pueden resolverse más adelante.

Cada pregunta se clasifica como:

- **BLOQUEANTE**
- **VALIDAR CON USUARIOS**
- **NO PRIORIZADO**
- **REVISIÓN NORMATIVA**

---

# 2. Preguntas bloqueantes del siguiente cambio

Actualmente no existe ninguna pregunta que impida comenzar la definición funcional y técnica del producto.

Cada spec identifica las dudas que bloquean su siguiente cambio; esta lista reúne preguntas de dominio para ampliaciones futuras.

---

# 3. OQ-001 — Jerarquía de cuentas contables

**Prioridad:** VALIDAR CON USUARIOS

## Pregunta

¿Qué nivel de jerarquía necesitan realmente las cuentas contables?

Modelo inicial:

```text
Cuenta padre
└── Cuenta hija
    └── Cuenta hija
```

## Qué validar

- cuántos niveles utilizan normalmente;
- si contabilizan directamente en cualquier nivel;
- si existen cuentas agrupadoras que no reciben movimientos.

---

# 4. OQ-002 — Borradores de pólizas descuadradas

**Prioridad:** VALIDAR CON USUARIOS

## Pregunta

¿El contador necesita guardar una póliza incompleta aunque todavía no esté balanceada?

## Qué validar

Si este flujo representa correctamente su forma de trabajo.

---

# 5. OQ-003 — Momento en que un CFDI se considera contabilizado

**Prioridad:** VALIDAR CON USUARIOS

## Pregunta

¿Qué debe mostrar el sistema cuando un CFDI ya participa en alguna póliza pero todavía tiene movimientos pendientes?

Esto es especialmente importante en PPD.

## Qué validar

- si necesitan distinguir estados adicionales;
- si utilizan conceptos como contabilizado parcial;
- cómo desean visualizar documentos PPD.

---

# 6. OQ-004 — Saldo pendiente en PPD

**Prioridad:** VALIDAR CON USUARIOS

## Pregunta

¿Cómo debe presentarse al usuario el saldo pendiente de una factura PPD?

## Qué validar

- qué importe utilizan como referencia;
- cómo se manejan pagos parciales;
- qué ocurre con diferencias;
- qué información desean ver en pantalla.

---

# 7. OQ-005 — Complementos que pagan múltiples facturas

**Prioridad:** VALIDAR CON USUARIOS / REVISIÓN NORMATIVA

## Pregunta

¿Cómo debe representarse un complemento de pago que está relacionado con varias facturas?

Modelo conceptual inicial:

```text
FiscalDocument [PAYMENT]
├── Factura A
│   └── importe pagado
└── Factura B
    └── importe pagado
```

## Qué falta

- validar la estructura funcional;
- revisar las reglas normativas aplicables;
- comprobar escenarios reales.

---

# 8. OQ-006 — Provisión en operaciones PPD

**Prioridad:** NO PRIORIZADO / REVISIÓN NORMATIVA

## Pregunta

¿Cuándo debe existir una póliza de provisión y cuál debe ser su tratamiento?

## Pendiente

Determinar posteriormente:

- reglas aplicables;
- cuentas utilizadas;
- tratamiento de IVA;
- si existen diferentes formas válidas.

---

# 9. OQ-007 — IVA pendiente y momento de pago/cobro

**Prioridad:** NO PRIORIZADO / REVISIÓN NORMATIVA

## Pregunta

¿Cómo debe manejar el sistema:

- IVA pendiente;
- IVA efectivamente pagado;
- IVA efectivamente cobrado;

especialmente en operaciones PPD y pagos parciales?

# 10. OQ-008 — Estados adicionales de AccountingPolicy

**Prioridad:** NO PRIORIZADO

## Pregunta

¿Se necesitan estados adicionales a:

```text
DRAFT
POSTED
```

Ejemplos futuros:

```text
CANCELLED
REVERSED
```

# 11. OQ-009 — Estados de FiscalDocument

**Prioridad:** VALIDAR CON USUARIOS

## Pregunta

¿Qué estados necesita visualizar el usuario para los documentos fiscales?

## Qué validar

Si el usuario necesita distinguir visualmente:

- pendiente;
- contabilizado;
- parcialmente trabajado;
- con error;
- otros.

---

# 12. OQ-010 — Tipos adicionales de póliza

**Prioridad:** NO PRIORIZADO

## Pregunta

¿Qué tipos de póliza adicionales requiere el despacho?

# 13. OQ-011 — Organization explícita

**Prioridad:** NO PRIORIZADO / DECISIÓN TÉCNICA

## Pregunta

¿Es necesario representar explícitamente una `Organization` en el modelo actual?

# 14. OQ-012 — OpeningBalance

**Prioridad:** NO PRIORIZADO

## Pregunta

¿Cómo se asociarán exactamente los saldos iniciales con:

- ejercicio;
- periodo;
- cuenta contable?

# 15. OQ-013 — Supplier y Customer como entidades

**Prioridad:** NO PRIORIZADO

## Pregunta

¿Proveedor y cliente necesitan ser entidades propias desde el inicio?

## Podrían convertirse en entidades cuando sean necesarias para:

- auxiliares;
- patrones;
- reglas;
- cuentas específicas;
- reportes.

---

# 16. OQ-014 — Cancelaciones de CFDI

**Prioridad:** NO PRIORIZADO / REVISIÓN NORMATIVA

## Pregunta

¿Qué debe ocurrir cuando un CFDI ya contabilizado aparece posteriormente como cancelado?

# 17. OQ-015 — Sustituciones y notas de crédito

**Prioridad:** NO PRIORIZADO / REVISIÓN NORMATIVA

## Pregunta

¿Cómo afectan una póliza previamente registrada:

- un CFDI sustituto;
- una nota de crédito?

# 18. OQ-016 — Reglas de cierre y reapertura

**Prioridad:** NO PRIORIZADO

## Pregunta

¿Qué debe ocurrir cuando un periodo se cierra?

Aspectos pendientes:

- quién puede cerrar;
- qué validaciones se requieren;
- si puede reabrirse;
- quién puede reabrir;
- cómo se audita.

# 19. OQ-017 — Migración

**Prioridad:** NO PRIORIZADO

## Pregunta

¿Qué información histórica debe migrarse al nuevo sistema?

Opciones posibles:

- catálogo de cuentas;
- saldos iniciales;
- XML;
- pólizas;
- relaciones históricas;
- ejercicios anteriores.

# 20. OQ-018 — DIOT y contabilidad electrónica

**Prioridad:** NO PRIORIZADO / REVISIÓN NORMATIVA

## Pregunta

¿Qué archivos y procesos fiscales necesita generar realmente el sistema?

Incluye potencialmente:

- DIOT;
- catálogo;
- balanza;
- contabilidad electrónica;
- otros archivos.

# 21. OQ-019 — Moneda extranjera

**Prioridad:** NO PRIORIZADO / REVISIÓN NORMATIVA

## Pregunta

¿Cómo deben tratarse:

- moneda extranjera;
- tipo de cambio;
- diferencias cambiarias?

# 22. OQ-020 — Conciliación bancaria

**Prioridad:** NO PRIORIZADO

## Pregunta

¿El producto debe incorporar conciliación bancaria?

# 23. Preguntas para revisión normativa

Estas preguntas no necesitan necesariamente una entrevista con el despacho.

Pueden investigarse mediante fuentes normativas.

Prioridad inicial:

1. PUE;
2. PPD;
3. complementos de pago;
4. pagos parciales;
5. IVA asociado a pago/cobro;
6. cancelación de CFDI;
7. sustitución de CFDI;
8. notas de crédito;
9. retenciones;
10. conservación de documentación contable.

---

# 24. Cómo usar las preguntas abiertas

Al preparar una ampliación, consulta sólo las preguntas relacionadas con sus criterios. Valida con contadores la jerarquía de cuentas, la captura de pólizas incompletas, la lectura de estados de CFDI, los pagos parciales y la trazabilidad cuando esos flujos cambien.

Una pregunta bloquea únicamente la entrega cuyo resultado no puede definirse sin responderla. Las ampliaciones no priorizadas no detienen el trabajo actual. Una vez resuelta y reflejada en código y pruebas, retírala de este documento; Git conserva el antecedente.
