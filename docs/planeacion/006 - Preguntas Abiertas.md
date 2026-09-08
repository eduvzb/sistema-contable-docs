# Sistema Contable — Preguntas Abiertas

> **Documento de referencia:** `02-open-questions.md`  
> **Nota en este vault:** [006 - Preguntas Abiertas](006%20-%20Preguntas%20Abiertas.md)
> **Estado:** Borrador inicial  
> **Enfoque:** Dudas pendientes después del análisis de negocio, MVP, escenarios, reglas y modelo de dominio  
> **Última actualización:** 2026-08-31

**Navegación:** [Inicio](00%20-%20Inicio.md) · [Análisis](001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md) · [MVP](003%20-%20MVP-Scope.md) · [Escenarios](004%20-%20Escenarios%20contables.md) · [Reglas](005%20-%20Reglas%20de%20negocio.md)

---

# 1. Propósito

Este documento concentra únicamente las preguntas que siguen abiertas después de haber definido:

- contexto general del proyecto;
- glosario de dominio;
- glosario contable;
- escenarios contables;
- alcance del MVP;
- reglas de negocio;
- modelo de dominio.

No pretende recopilar todas las dudas posibles.

La idea es evitar detener el proyecto por preguntas que pueden resolverse más adelante.

Cada pregunta se clasifica como:

- **BLOQUEA MVP**
- **VALIDAR DURANTE MVP**
- **POSTERIOR AL MVP**
- **REVISIÓN NORMATIVA**

---

# 2. Preguntas que bloquean el MVP

Actualmente no existe ninguna pregunta que impida comenzar la definición funcional y técnica del MVP.

Las decisiones mínimas necesarias para avanzar se consideran suficientemente resueltas de forma provisional.

---

# 3. OQ-001 — Jerarquía de cuentas contables

**Prioridad:** VALIDAR DURANTE MVP

## Pregunta

¿Qué nivel de jerarquía necesitan realmente las cuentas contables?

Modelo inicial:

```text
Cuenta padre
└── Cuenta hija
    └── Cuenta hija
```

## Decisión provisional

El sistema debe permitir una estructura jerárquica de cuentas.

No se fija todavía un número máximo de niveles.

## Qué validar

- cuántos niveles utilizan normalmente;
- si contabilizan directamente en cualquier nivel;
- si existen cuentas agrupadoras que no reciben movimientos.

---

# 4. OQ-002 — Borradores de pólizas descuadradas

**Prioridad:** VALIDAR DURANTE MVP

## Pregunta

¿El contador necesita guardar una póliza incompleta aunque todavía no esté balanceada?

## Decisión provisional

Sí.

```text
DRAFT
→ puede estar descuadrada

POSTED
→ debe estar balanceada
```

## Qué validar

Si este flujo representa correctamente su forma de trabajo.

---

# 5. OQ-003 — Momento en que un CFDI se considera contabilizado

**Prioridad:** VALIDAR DURANTE MVP

## Pregunta

¿Qué debe mostrar el sistema cuando un CFDI ya participa en alguna póliza pero todavía tiene movimientos pendientes?

Esto es especialmente importante en PPD.

## Decisión provisional

Un CFDI se considera:

```text
contabilizado
```

cuando existe al menos una `AccountingPolicy` relacionada en estado `POSTED`.

Sin embargo:

```text
contabilizado ≠ liquidado
```

Una factura puede estar contabilizada y conservar saldo pendiente.

## Qué validar

- si necesitan distinguir estados adicionales;
- si utilizan conceptos como contabilizado parcial;
- cómo desean visualizar documentos PPD.

---

# 6. OQ-004 — Saldo pendiente en PPD

**Prioridad:** VALIDAR DURANTE MVP

## Pregunta

¿Cómo debe presentarse al usuario el saldo pendiente de una factura PPD?

## Decisión provisional

Conceptualmente:

```text
Importe de la operación
-
Pagos relacionados
=
Saldo pendiente
```

## Qué validar

- qué importe utilizan como referencia;
- cómo se manejan pagos parciales;
- qué ocurre con diferencias;
- qué información desean ver en pantalla.

---

# 7. OQ-005 — Complementos que pagan múltiples facturas

**Prioridad:** VALIDAR DURANTE MVP / REVISIÓN NORMATIVA

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

## Decisión provisional

El complemento se mantiene como un `FiscalDocument` y conserva relaciones con cada factura correspondiente.

## Qué falta

- validar la estructura funcional;
- revisar las reglas normativas aplicables;
- comprobar escenarios reales.

---

# 8. OQ-006 — Provisión en operaciones PPD

**Prioridad:** POSTERIOR AL MVP / REVISIÓN NORMATIVA

## Pregunta

¿Cuándo debe existir una póliza de provisión y cuál debe ser su tratamiento?

## Decisión para MVP

No automatizar provisiones.

El contador podrá crear manualmente las pólizas necesarias.

## Pendiente

Determinar posteriormente:

- reglas aplicables;
- cuentas utilizadas;
- tratamiento de IVA;
- si existen diferentes formas válidas.

---

# 9. OQ-007 — IVA pendiente y momento de pago/cobro

**Prioridad:** POSTERIOR AL MVP / REVISIÓN NORMATIVA

## Pregunta

¿Cómo debe manejar el sistema:

- IVA pendiente;
- IVA efectivamente pagado;
- IVA efectivamente cobrado;

especialmente en operaciones PPD y pagos parciales?

## Decisión para MVP

No automatizar este tratamiento.

El sistema debe conservar suficiente trazabilidad para incorporarlo posteriormente.

---

# 10. OQ-008 — Estados adicionales de AccountingPolicy

**Prioridad:** POSTERIOR AL MVP

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

## Decisión para MVP

Usar únicamente:

```text
DRAFT
POSTED
```

---

# 11. OQ-009 — Estados de FiscalDocument

**Prioridad:** VALIDAR DURANTE MVP

## Pregunta

¿Qué estados necesita visualizar el usuario para los documentos fiscales?

## Decisión provisional

No crear una máquina de estados compleja.

El MVP puede manejar información como:

```text
importado
con error
```

y derivar su situación contable mediante relaciones con pólizas.

## Qué validar

Si el usuario necesita distinguir visualmente:

- pendiente;
- contabilizado;
- parcialmente trabajado;
- con error;
- otros.

---

# 12. OQ-010 — Tipos adicionales de póliza

**Prioridad:** POSTERIOR AL MVP

## Pregunta

¿Qué tipos de póliza adicionales requiere el despacho?

## Decisión para MVP

Soportar:

```text
INGRESO
EGRESO
DIARIO
```

Conceptos como:

```text
AJUSTE
CIERRE
```

pueden agregarse posteriormente.

---

# 13. OQ-011 — Organization explícita

**Prioridad:** POSTERIOR AL MVP / DECISIÓN TÉCNICA

## Pregunta

¿Es necesario representar explícitamente una `Organization` desde la primera versión?

## Decisión provisional

El MVP puede asumir un único despacho.

La decisión puede tomarse durante arquitectura sin afectar el flujo contable principal.

---

# 14. OQ-012 — OpeningBalance

**Prioridad:** POSTERIOR AL MVP

## Pregunta

¿Cómo se asociarán exactamente los saldos iniciales con:

- ejercicio;
- periodo;
- cuenta contable?

## Decisión provisional

El concepto existe en el dominio, pero no es necesario cerrar su diseño para la primera demostración del flujo contable.

Será importante para migración.

---

# 15. OQ-013 — Supplier y Customer como entidades

**Prioridad:** POSTERIOR AL MVP

## Pregunta

¿Proveedor y cliente necesitan ser entidades propias desde el inicio?

## Decisión para MVP

No.

Inicialmente se utilizará información obtenida de los CFDI:

- RFC;
- razón social;
- emisor;
- receptor.

## Podrían convertirse en entidades cuando sean necesarias para:

- auxiliares;
- patrones;
- reglas;
- cuentas específicas;
- reportes.

---

# 16. OQ-014 — Cancelaciones de CFDI

**Prioridad:** POSTERIOR AL MVP / REVISIÓN NORMATIVA

## Pregunta

¿Qué debe ocurrir cuando un CFDI ya contabilizado aparece posteriormente como cancelado?

## Decisión para MVP

No automatizar el tratamiento.

El diseño debe evitar eliminar historial.

---

# 17. OQ-015 — Sustituciones y notas de crédito

**Prioridad:** POSTERIOR AL MVP / REVISIÓN NORMATIVA

## Pregunta

¿Cómo afectan una póliza previamente registrada:

- un CFDI sustituto;
- una nota de crédito?

## Decisión para MVP

Conservar la capacidad conceptual de relacionar documentos.

No implementar todavía el comportamiento contable completo.

---

# 18. OQ-016 — Reglas de cierre y reapertura

**Prioridad:** POSTERIOR AL MVP

## Pregunta

¿Qué debe ocurrir cuando un periodo se cierra?

Aspectos pendientes:

- quién puede cerrar;
- qué validaciones se requieren;
- si puede reabrirse;
- quién puede reabrir;
- cómo se audita.

## Decisión para MVP

El concepto puede representarse de manera básica, pero el flujo formal de cierre no forma parte del MVP.

---

# 19. OQ-017 — Migración

**Prioridad:** POSTERIOR AL MVP

## Pregunta

¿Qué información histórica debe migrarse al nuevo sistema?

Opciones posibles:

- catálogo de cuentas;
- saldos iniciales;
- XML;
- pólizas;
- relaciones históricas;
- ejercicios anteriores.

## Decisión provisional

No resolver migración completa durante el MVP.

---

# 20. OQ-018 — DIOT y contabilidad electrónica

**Prioridad:** POSTERIOR AL MVP / REVISIÓN NORMATIVA

## Pregunta

¿Qué archivos y procesos fiscales necesita generar realmente el sistema?

Incluye potencialmente:

- DIOT;
- catálogo;
- balanza;
- contabilidad electrónica;
- otros archivos.

## Decisión para MVP

Fuera de alcance.

---

# 21. OQ-019 — Moneda extranjera

**Prioridad:** POSTERIOR AL MVP / REVISIÓN NORMATIVA

## Pregunta

¿Cómo deben tratarse:

- moneda extranjera;
- tipo de cambio;
- diferencias cambiarias?

## Decisión para MVP

Conservar los datos del CFDI cuando existan.

No implementar lógica contable avanzada.

---

# 22. OQ-020 — Conciliación bancaria

**Prioridad:** POSTERIOR AL MVP

## Pregunta

¿El producto debe incorporar conciliación bancaria?

## Decisión para MVP

No.

Se evaluará una vez validado el núcleo contable.

---

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

# 24. Preguntas que sí vale la pena validar con usuarios durante el MVP

En lugar de realizar una entrevista amplia antes de desarrollar, podemos observar y validar durante la demostración:

1. ¿La jerarquía de cuentas contables representa su catálogo?
2. ¿Necesitan guardar pólizas incompletas?
3. ¿Cómo quieren identificar visualmente un CFDI contabilizado?
4. ¿Cómo quieren visualizar pagos parciales y saldo pendiente?
5. ¿El flujo de PPD se entiende correctamente?
6. ¿Los tipos `INGRESO`, `EGRESO` y `DIARIO` cubren la primera prueba?
7. ¿La trazabilidad CFDI → póliza y póliza → CFDI muestra suficiente información?
8. ¿La descarga simulada representa el proceso que esperan?

---

# 25. Qué NO debe detener el desarrollo

Las siguientes preguntas no deben bloquear el inicio de specs o diseño técnico:

- configuración avanzada;
- automatización;
- reglas por proveedor;
- reglas por cliente;
- DIOT;
- conciliación bancaria;
- contabilidad electrónica;
- moneda extranjera avanzada;
- cierre completo;
- migración histórica;
- patrones contables.

---

# 26. Regla para nuevas preguntas

Cuando aparezca una nueva duda deberá evaluarse en este orden:

```text
1. ¿Bloquea realmente el MVP?
        ↓
2. ¿Puede resolverse mediante lógica del dominio?
        ↓
3. ¿Puede resolverse mediante normativa?
        ↓
4. ¿Podemos usar un supuesto temporal?
        ↓
5. ¿Puede validarse durante el MVP?
        ↓
6. Solo entonces convertirla en pregunta bloqueante.
```

La intención es evitar detener el proyecto por incertidumbre que puede resolverse progresivamente.

---

# 27. Estado actual

Con las decisiones provisionales ya tomadas:

> **No existen preguntas abiertas que impidan avanzar hacia specs y diseño técnico del MVP.**

Las preguntas de este documento deben utilizarse como:

- guía para pruebas;
- guía para revisión normativa;
- guía para la siguiente entrevista;
- lista de decisiones posteriores.

