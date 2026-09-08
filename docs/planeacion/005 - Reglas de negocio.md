
# Sistema Contable — Reglas de Negocio del MVP

> **Documento de referencia:** `03-business-rules.md`  
> **Nota en este vault:** [005 - Reglas de negocio](005%20-%20Reglas%20de%20negocio.md)
> **Estado:** Borrador simplificado  
> **Enfoque:** Negocio y comportamiento del MVP  
> **Última actualización:** 2026-08-31

**Navegación:** [Inicio](00%20-%20Inicio.md) · [Análisis](001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md) · [MVP](003%20-%20MVP-Scope.md) · [Escenarios](004%20-%20Escenarios%20contables.md)

---

# 1. Propósito

Este documento define las reglas básicas que necesita el MVP para representar el flujo contable principal.

En esta etapa **no se busca diseñar un sistema altamente configurable**.

El objetivo es trabajar con un conjunto simple de reglas que permita:

```text
XML
→ AccountingPolicy
→ AccountingPolicyEntry
→ Cuenta contable
→ Balanza
```

Cuando una regla todavía no esté completamente confirmada, se marcará como:

- **CONFIRMADA**
- **SUPUESTO MVP**
- **PENDIENTE DE VALIDAR**

Más adelante, después de validar el MVP, se decidirá qué reglas deben convertirse en configuraciones.

---

# 2. Principio general del MVP

Durante el MVP se utilizará un comportamiento predefinido.

No se desarrollará todavía un configurador contable completo.

La prioridad es comprobar que el sistema puede representar correctamente el proceso contable.

---

# 3. BR-001 — Toda operación pertenece a una empresa

**Estado:** CONFIRMADA

Toda información contable debe pertenecer a una empresa.

Esto incluye:

- cuentas contables;
- XML;
- pólizas;
- partidas;
- periodos;
- saldos.

La información de una empresa no debe mezclarse con otra.

---

# 4. BR-002 — El contador trabaja dentro de un periodo

**Estado:** CONFIRMADA

Toda póliza debe pertenecer a:

```text
Empresa
+
Ejercicio
+
Periodo
```

Ejemplo:

```text
Empresa X
2026
Julio
```

---

# 5. BR-003 — Cada empresa tiene su propio catálogo de cuentas

**Estado:** CONFIRMADA

Cada empresa puede utilizar su propio catálogo de cuentas contables.

Una cuenta contable de una empresa no debe utilizarse directamente en otra.

---

# 6. BR-004 — Cada partida utiliza una cuenta contable

**Estado:** CONFIRMADA

Toda `AccountingPolicyEntry` debe indicar la cuenta contable afectada.

Ejemplo:

```text
AccountingPolicy
├── Gastos
├── IVA
└── Proveedores
```

---

# 7. BR-005 — Una póliza contabilizada debe estar balanceada

**Estado:** CONFIRMADA COMO REGLA DEL MVP

Para contabilizar una `AccountingPolicy` debe cumplirse:

```text
Total cargos = Total abonos
```

Una póliza que no cumpla esta condición no puede considerarse contabilizada.

---

# 8. BR-006 — Una póliza incompleta puede guardarse como borrador

**Estado:** SUPUESTO MVP

Se permitirá guardar una póliza aunque todavía no esté balanceada, siempre que permanezca como borrador.

```text
DRAFT
→ puede estar incompleta

POSTED
→ cargos = abonos
```

Este comportamiento se validará durante las pruebas.

---

# 9. BR-007 — Una póliza puede relacionarse con varios XML

**Estado:** CONFIRMADA

El contador puede utilizar varios documentos fiscales dentro de una misma póliza.

```text
XML A ─┐
XML B ─┼──→ AccountingPolicy
XML C ─┘
```

---

# 10. BR-008 — Un XML puede relacionarse con varias pólizas

**Estado:** CONFIRMADA

Un documento fiscal puede participar en varios movimientos contables.

Esto permite representar casos como:

- factura inicial;
- pagos parciales;
- movimientos en distintos periodos.

---

# 11. BR-009 — Una póliza puede existir sin XML

**Estado:** CONFIRMADA COMO NECESIDAD DEL MODELO

No toda póliza debe depender de un CFDI.

Puede haber movimientos como:

- ajustes;
- reclasificaciones;
- cierres;
- otros movimientos internos.

Por tanto, relacionar un XML con una póliza es opcional.

---

# 12. BR-010 — El mismo CFDI no debe importarse dos veces

**Estado:** SUPUESTO MVP

El UUID se utilizará para detectar documentos ya existentes.

Si el mismo CFDI vuelve a cargarse:

- se detecta;
- se informa al usuario;
- no se crea una segunda operación equivalente.

Los casos de sustitución o corrección quedan para una fase posterior.

---

# 13. BR-011 — El XML original debe conservarse

**Estado:** CONFIRMADA COMO REGLA DEL MVP

Cuando un XML se incorpora al sistema, debe conservarse para mantener trazabilidad.

El sistema puede extraer y organizar sus datos, pero no debe perder el documento original.

---

# 14. BR-012 — PUE y PPD se tratan como escenarios diferentes

**Estado:** CONFIRMADA COMO NECESIDAD FUNCIONAL

El sistema debe distinguir entre:

```text
PUE
PPD
```

El MVP no automatizará todavía todas las diferencias contables entre ambos.

El contador podrá registrar manualmente las partidas necesarias.

---

# 15. BR-013 — Una factura PPD puede tener varios pagos

**Estado:** CONFIRMADA

El sistema debe poder representar pagos parciales.

Ejemplo:

```text
Factura: $100,000

Pago 1: $40,000
Pago 2: $60,000
```

---

# 16. BR-014 — Los pagos pueden ocurrir en distintos periodos

**Estado:** CONFIRMADA

Una misma factura puede generar movimientos en meses distintos.

Ejemplo:

```text
Factura
├── Julio  → $50,000
└── Agosto → $50,000
```

Cada movimiento debe conservar el periodo al que pertenece.

---

# 17. BR-015 — Los complementos deben conservar su relación con la factura

**Estado:** PENDIENTE DE VALIDACIÓN NORMATIVA

Cuando exista un complemento de pago, el sistema debe conservar la relación con la factura o facturas correspondientes.

Para el MVP se utilizará este comportamiento como parte del escenario PPD.

---

# 18. BR-016 — El contador selecciona manualmente las cuentas contables

**Estado:** CONFIRMADA PARA MVP

El MVP no intentará decidir automáticamente qué cuenta contable utilizar.

El contador seleccionará manualmente las cuentas y podrá modificar las partidas.

La automatización se evaluará después.

---

# 19. BR-017 — Las pólizas contabilizadas afectan la balanza

**Estado:** CONFIRMADA

Las partidas de una póliza contabilizada deben reflejarse en los movimientos y saldos de las cuentas contables.

Una póliza en borrador no debe afectar la balanza definitiva.

---

# 20. BR-018 — Debe existir trazabilidad desde el XML

**Estado:** CONFIRMADA

Desde un documento fiscal debe poder consultarse cómo fue contabilizado.

El usuario debe poder llegar a:

```text
FiscalDocument
↓
AccountingPolicy
↓
AccountingPolicyEntry
↓
Cuenta contable
```

---

# 21. BR-019 — Debe existir trazabilidad desde la póliza

**Estado:** CONFIRMADA

Desde una póliza debe poder consultarse qué documentos fiscales están relacionados con ella, cuando existan.

---

# 22. BR-020 — La descarga automática se simula en el MVP

**Estado:** CONFIRMADA PARA MVP

El cliente debe poder visualizar el flujo:

```text
Solicitar descarga
↓
Servicio externo simulado
↓
XML encontrados
↓
XML incorporados al sistema
↓
Contabilización
```

No se implementará todavía la integración real con SAT.

---

# 23. Reglas que NO resolverá todavía el MVP

El MVP no definirá completamente las reglas de:

- IVA pendiente;
- IVA efectivamente pagado;
- IVA efectivamente cobrado;
- deducibilidad;
- retenciones;
- cancelaciones de CFDI;
- sustituciones;
- notas de crédito;
- cierre contable;
- reapertura;
- moneda extranjera;
- diferencias cambiarias;
- DIOT;
- contabilidad electrónica;
- conciliación bancaria.

Estos conceptos pueden existir en el modelo de conocimiento, pero no deben complicar el primer flujo funcional.

---

# 24. Qué no será configurable todavía

Aunque el producto futuro podría permitir distintas formas de operación, el MVP no tendrá configuraciones avanzadas para:

- comportamiento PPD;
- reglas de IVA;
- agrupación automática;
- provisiones automáticas;
- patrones contables;
- sugerencias automáticas;
- reglas por proveedor;
- reglas por cliente;
- reglas por régimen fiscal.

Para las pruebas se utilizará un comportamiento simple y predefinido.

---

# 25. Qué podrá cambiar después del MVP

Después de validar el flujo principal se analizará cuáles comportamientos deben convertirse en:

```text
Regla fija
Configuración
Sugerencia
Patrón
Automatización
```

Esta decisión no forma parte del MVP.

---

# 26. Revisión normativa

Cuando una regla del MVP tenga implicaciones fiscales o contables, podrá contrastarse posteriormente con:

- legislación aplicable;
- reglas SAT;
- NIF;
- otras fuentes normativas.

Si se encuentra una posible contradicción, se documentará y analizará antes de modificar el comportamiento.

Encontrar una diferencia no significa cambiar automáticamente el sistema.

---

# 27. Set de reglas para pruebas

Para la primera prueba utilizaremos un único conjunto de reglas:

```text
MVP_RULESET_V1
```

Su objetivo será dar un comportamiento estable y repetible al MVP.

No significa que todas sus decisiones sean reglas universales del producto final.

Este ruleset deberá permitir probar:

```text
Empresa
↓
Periodo
↓
Importación / descarga simulada
↓
XML
↓
AccountingPolicy
↓
Partidas
↓
Cuentas contables
↓
Balanza
↓
Trazabilidad
```

---

# 28. Pregunta principal del documento

> **¿Qué reglas mínimas necesitamos fijar para probar correctamente el flujo contable principal sin construir todavía toda la flexibilidad del producto final?**
