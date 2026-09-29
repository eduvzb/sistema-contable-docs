
# Sistema Contable — Reglas de negocio

> **Enfoque:** Negocio y comportamiento del producto

**Navegación:** [Inicio](00%20-%20Inicio.md) · [Análisis](001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md) · [Alcance](003%20-%20Alcance%20del%20producto.md) · [Escenarios](004%20-%20Escenarios%20contables.md)

---

# 1. Propósito

Este documento reúne reglas de dominio para interpretar el flujo contable:

```text
XML
→ AccountingPolicy
→ AccountingPolicyEntry
→ Cuenta contable
→ Balanza
```

El estado de una regla indica su validación de negocio o normativa, no si el código la implementa. Para conocer el comportamiento actual, consulta la spec responsable y el código. Los estados usados aquí son:

- **CONFIRMADA**
- **SUPUESTO POR VALIDAR**
- **PENDIENTE DE VALIDAR**

---

# 2. Principio general del producto

Una nueva configuración o regla contable debe responder a una necesidad concreta y quedar definida en una spec antes de implementarse.

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

**Estado:** CONFIRMADA COMO REGLA

Para contabilizar una `AccountingPolicy` debe cumplirse:

```text
Total cargos = Total abonos
```

Una póliza que no cumpla esta condición no puede considerarse contabilizada.

---

# 8. BR-006 — Una póliza incompleta puede guardarse como borrador

**Estado:** SUPUESTO POR VALIDAR

Se permitirá guardar una póliza aunque todavía no esté balanceada, siempre que permanezca como borrador.

```text
DRAFT
→ puede estar incompleta

POSTED
→ cargos = abonos
```

El comportamiento técnico está definido en SPEC-006; la utilidad del flujo para los contadores requiere validación con usuarios.

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

**Estado:** SUPUESTO POR VALIDAR

El UUID se utilizará para detectar documentos ya existentes.

Si el mismo CFDI vuelve a cargarse:

- se detecta;
- se informa al usuario;
- no se crea una segunda operación equivalente.

Los casos de sustitución o corrección quedan para una ampliación futura.

---

# 13. BR-011 — El XML original no se conserva

**Estado:** CONFIRMADA COMO REGLA

Cuando un XML se incorpora al sistema, se extraen, validan y conservan sus datos fiscales normalizados, relaciones y trazabilidad contable. El archivo original no se copia a almacenamiento durable ni se conserva como BLOB.

La carga multipart puede usar el archivo temporal que administra la plataforma durante la solicitud; éste no constituye una conservación durable. Los XML históricos existentes permanecen fuera del alcance de esta regla hasta una limpieza autorizada, pero tampoco se exponen mediante el producto.

---

# 14. BR-012 — PUE y PPD se tratan como escenarios diferentes

**Estado:** CONFIRMADA COMO NECESIDAD FUNCIONAL

El sistema debe distinguir entre:

```text
PUE
PPD
```

El producto no automatizará todavía todas las diferencias contables entre ambos.

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

Para el producto se utilizará este comportamiento como parte del escenario PPD.

---

# 18. BR-016 — El contador selecciona manualmente las cuentas contables

**Estado:** CONFIRMADA PARA EL ALCANCE ACTUAL

El producto no intentará decidir automáticamente qué cuenta contable utilizar.

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

# 22. BR-020 — La descarga automática se simula en el alcance actual

**Estado:** CONFIRMADA PARA EL ALCANCE ACTUAL

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

# 23. Límites y revisión de reglas

Los tratamientos de IVA, deducibilidad, retenciones, cancelaciones, moneda extranjera, cierre, DIOT y conciliación bancaria requieren definición funcional y, cuando corresponda, revisión normativa antes de implementarse. El comportamiento observable de cada entrega se concreta en su spec; el código y las pruebas muestran lo que ya funciona.

Una diferencia entre una regla de este documento y el producto debe investigarse en el caso específico. La regla no autoriza por sí sola a cambiar una operación implementada.
