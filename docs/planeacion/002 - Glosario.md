
# Sistema Contable — Glosario de Dominio

> **Documento de referencia:** `01-domain-glossary.md`  
> **Nota en este vault:** [002 - Glosario](002%20-%20Glosario.md)  
> **Estado:** Borrador inicial  
> **Propósito:** Unificar el lenguaje del proyecto entre negocio, producto y desarrollo  
> **Última actualización:** 2026-08-31

**Navegación:** [Inicio](00%20-%20Inicio.md) · [Análisis](001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md) · [MVP](003%20-%20MVP-Scope.md) · [Escenarios](004%20-%20Escenarios%20contables.md) · [Guía de conceptos](Conceptos/Gu%C3%ADa%20de%20conceptos.md)

---

# 1. Propósito

Este documento define los términos principales utilizados dentro del proyecto del sistema contable.

El objetivo es evitar ambigüedades entre:

- lenguaje contable;
- lenguaje fiscal;
- lenguaje utilizado por los usuarios;
- nombres utilizados en código;
- nombres utilizados en base de datos;
- nombres utilizados en especificaciones.

Este glosario no pretende sustituir definiciones fiscales o legales oficiales.

Representa el significado operativo que cada concepto tendrá dentro del sistema.

Cada definición puede encontrarse en uno de estos estados:

- **CONFIRMADO:** concepto identificado directamente durante el levantamiento.
- **DECISIÓN TÉCNICA:** convención definida para el diseño del sistema.
- **SUPUESTO MVP:** comportamiento o interpretación provisional.
- **PENDIENTE DE VALIDAR:** requiere confirmación con usuarios contables.
- **FUERA DEL MVP:** concepto relevante pero no prioritario en la primera versión.

---

# 2. Organización

**Estado:** DECISIÓN TÉCNICA

Entidad que representa al despacho, firma o grupo que utiliza la plataforma y administra múltiples empresas.

Una organización puede contener:

- usuarios;
- empresas;
- configuraciones generales;
- permisos;
- límites operativos.

Nombre sugerido en dominio:

```text
Organization
```

Relación conceptual:

```text
Organization
└── Companies
```

---

# 3. Usuario

**Estado:** CONFIRMADO

Persona que accede a la plataforma.

Puede tener diferentes responsabilidades según su rol.

Ejemplos:

- administrador;
- contador;
- futuro auditor;
- futuro supervisor;
- futuro cliente de solo lectura.

Nombre sugerido en dominio:

```text
User
```

---

# 4. Administrador

**Estado:** CONFIRMADO

Usuario con permisos para administrar el entorno general.

Responsabilidades identificadas:

- crear usuarios;
- crear empresas;
- asignar empresas;
- administrar permisos;
- consultar múltiples empresas;
- modificar configuraciones generales.

Nombre sugerido:

```text
Administrator
```

---

# 5. Contador

**Estado:** CONFIRMADO

Usuario que realiza la operación contable cotidiana.

Trabaja dentro del contexto de una empresa y un periodo.

Responsabilidades identificadas:

- consultar CFDI/XML;
- crear pólizas;
- seleccionar cuentas;
- revisar IVA;
- generar reportes;
- consultar balanzas;
- preparar DIOT.

Nombre sugerido:

```text
Accountant
```

---

# 6. Empresa

**Estado:** CONFIRMADO

Entidad contable y fiscal independiente administrada dentro de la plataforma.

Cada empresa posee su propia información.

Ejemplos:

- RFC;
- razón social;
- régimen fiscal;
- periodos;
- catálogo de cuentas;
- XML;
- pólizas;
- saldos;
- reglas contables;
- configuración fiscal.

Nombre sugerido:

```text
Company
```

Una empresa debe ser considerada uno de los principales límites del dominio.

La información de una empresa no deberá mezclarse con la de otra.

---

# 7. Asignación de empresa

**Estado:** CONFIRMADO

Relación que determina qué usuarios pueden consultar u operar una empresa.

Ejemplo:

```text
Usuario A
├── Empresa 1
├── Empresa 2
└── Empresa 3
```

Nombre técnico candidato:

```text
CompanyUser
```

o:

```text
CompanyMembership
```

La nomenclatura definitiva se decidirá durante el diseño técnico.

---

# 8. Ejercicio contable

**Estado:** CONFIRMADO

Año al que pertenecen los registros contables.

Ejemplo:

```text
Ejercicio: 2026
```

Un ejercicio contiene múltiples periodos.

Nombre sugerido:

```text
FiscalYear
```

o:

```text
AccountingYear
```

**Pendiente técnico:** elegir una única convención.

---

# 9. Periodo contable

**Estado:** CONFIRMADO

Mes dentro de un ejercicio en el que se agrupan y procesan movimientos contables.

Ejemplo:

```text
Empresa: Empresa X
Ejercicio: 2026
Periodo: Julio
```

El contexto principal de trabajo del contador será:

```text
Empresa + Periodo
```

Nombre sugerido:

```text
AccountingPeriod
```

Estados potenciales:

- abierto;
- en proceso;
- cerrado;
- bloqueado.

**Estado de esos estados:** SUPUESTO MVP.

---

# 10. CFDI

**Estado:** CONFIRMADO

Comprobante Fiscal Digital por Internet.

Dentro del sistema representa el documento fiscal contenido normalmente en un archivo XML.

El proyecto debe evitar utilizar `CFDI` y `XML` como si fueran exactamente el mismo concepto.

Distinción propuesta:

```text
XML
= archivo físico o digital recibido/importado

CFDI
= documento fiscal interpretado a partir del XML
```

Esta separación puede resultar importante técnicamente.

---

# 11. XML fiscal

**Estado:** CONFIRMADO

Archivo que contiene la información estructurada del CFDI.

Puede ser:

- cargado manualmente;
- cargado masivamente;
- descargado posteriormente desde un servicio externo.

Datos importantes extraídos:

- UUID;
- RFC;
- fecha;
- subtotal;
- impuestos;
- total;
- tipo;
- método de pago;
- forma de pago;
- moneda;
- conceptos;
- relaciones.

Nombre técnico candidato:

```text
FiscalDocument
```

La recomendación es no llamar a la entidad principal simplemente `Xml`.

---

# 12. Documento fiscal

**Estado:** DECISIÓN TÉCNICA

Representación normalizada dentro del sistema de un CFDI importado.

Permite desacoplar la lógica del dominio del archivo XML original.

Ejemplo conceptual:

```text
Archivo XML
    ↓ parseo
FiscalDocument
    ├── datos generales
    ├── conceptos
    ├── impuestos
    ├── relaciones
    └── archivo original
```

Nombre sugerido:

```text
FiscalDocument
```

---

# 13. UUID

**Estado:** CONFIRMADO

Identificador fiscal único del CFDI.

Será uno de los principales identificadores utilizados para:

- detectar duplicados;
- localizar documentos;
- establecer relaciones;
- mantener trazabilidad.

Nombre sugerido:

```text
uuid
```

---

# 14. CFDI emitido

**Estado:** CONFIRMADO

Documento fiscal en el que la empresa seleccionada actúa como emisor.

En términos generales puede representar operaciones de ingreso, aunque el tratamiento exacto depende del tipo de documento.

Nombre conceptual:

```text
IssuedFiscalDocument
```

No necesariamente requiere una entidad diferente; puede representarse mediante atributos del documento.

---

# 15. CFDI recibido

**Estado:** CONFIRMADO

Documento fiscal en el que la empresa seleccionada actúa como receptor.

Generalmente se relacionará con:

- compras;
- gastos;
- proveedores;
- IVA acreditable.

Nombre conceptual:

```text
ReceivedFiscalDocument
```

---

# 16. Tipo de comprobante

**Estado:** CONFIRMADO

Clasificación fiscal del CFDI.

Puede distinguir diferentes tipos de documentos.

Ejemplos relevantes para el proyecto:

- ingreso;
- egreso;
- pago;
- nómina.

La lista definitiva deberá obtenerse de las versiones de CFDI soportadas.

---

# 17. Factura

**Estado:** CONFIRMADO

Término de negocio utilizado para referirse a determinados CFDI asociados a una operación de compra o venta.

Dentro de la aplicación conviene mantener `FiscalDocument` como entidad técnica general y utilizar `Factura` como concepto del dominio cuando corresponda.

No todo CFDI deberá asumirse como factura.

---

# 18. PUE

**Estado:** CONFIRMADO

Pago en Una sola Exhibición.

Valor utilizado en CFDI para indicar que la operación se plantea como pagada en una sola exhibición.

El sistema debe distinguir PUE de PPD porque su tratamiento contable puede ser diferente.

Nombre conceptual:

```text
PUE
```

El comportamiento contable exacto sigue sujeto a reglas específicas.

---

# 19. PPD

**Estado:** CONFIRMADO

Pago en Parcialidades o Diferido.

Permite representar operaciones cuyo pago ocurre posteriormente o mediante múltiples pagos.

Puede implicar:

- factura inicial;
- uno o varios pagos;
- complementos de pago;
- movimientos en distintos periodos;
- diferentes momentos de reconocimiento de impuestos.

Nombre conceptual:

```text
PPD
```

---

# 20. Complemento de pago

**Estado:** CONFIRMADO

Documento fiscal utilizado para registrar pagos relacionados con una factura, especialmente en operaciones PPD.

Una factura puede tener múltiples complementos.

Ejemplo:

```text
Factura $100,000
├── Complemento julio  $50,000
└── Complemento agosto $50,000
```

Nombre sugerido:

```text
PaymentComplement
```

---

# 21. Pago parcial

**Estado:** CONFIRMADO

Pago que cubre solamente una parte del importe pendiente de una factura.

Puede provocar que una misma factura participe en movimientos contables de diferentes periodos.

Ejemplo:

```text
Factura: $100,000

Julio:
$50,000

Agosto:
$50,000
```

El sistema debe conservar el historial de estos pagos.

---

# 22. Documento relacionado

**Estado:** CONFIRMADO

Relación fiscal existente entre un CFDI y otro.

Ejemplos potenciales:

- complemento relacionado con factura;
- nota de crédito relacionada;
- sustitución;
- otros CFDI relacionados.

Nombre sugerido:

```text
FiscalDocumentRelation
```

La semántica exacta deberá conservar el tipo de relación fiscal.

---

# 23. Nota de crédito

**Estado:** PENDIENTE DE VALIDAR

Documento que puede reducir, corregir o afectar una operación previamente registrada.

Fue mencionado como caso que el sistema deberá contemplar, pero todavía no se ha definido su flujo contable.

No debería implementarse una regla automática hasta contar con escenarios reales.

---

# 24. CFDI cancelado

**Estado:** PENDIENTE DE VALIDAR

CFDI cuyo estado fiscal indica cancelación.

El sistema deberá eventualmente definir:

- cómo detectar cancelaciones;
- qué ocurre si ya fue contabilizado;
- si genera alertas;
- si requiere reversa;
- cómo se conserva el historial.

---

# 25. Adenda

**Estado:** CONFIRMADO

Información adicional que puede estar incluida dentro de ciertos XML y que no necesariamente forma parte del contenido fiscal principal.

Debe preservarse si está presente.

La necesidad de interpretarla automáticamente dependerá de cada caso.

---

# 26. Concepto de CFDI

**Estado:** CONFIRMADO

Detalle de producto, servicio u otro concepto incluido dentro del documento fiscal.

Puede contener información relevante para:

- clasificación;
- reportes;
- patrones contables;
- futuras sugerencias de cuentas.

Nombre sugerido:

```text
FiscalDocumentConcept
```

---

# 27. Impuesto del CFDI

**Estado:** CONFIRMADO

Impuesto registrado dentro del documento fiscal.

Puede contener información como:

- tipo;
- base;
- tasa;
- importe;
- traslado;
- retención.

Nombre sugerido:

```text
FiscalDocumentTax
```

---

# 28. Método de pago

**Estado:** CONFIRMADO

Dato fiscal utilizado dentro del CFDI.

Tiene especial relevancia para distinguir escenarios PUE y PPD.

No debe confundirse con forma de pago.

Nombre técnico:

```text
payment_method
```

---

# 29. Forma de pago

**Estado:** CONFIRMADO

Dato fiscal que representa la forma utilizada para realizar un pago.

No debe confundirse con método de pago.

Nombre técnico:

```text
payment_form
```

---

# 30. Moneda

**Estado:** CONFIRMADO

Moneda en la que se expresa una operación.

Nombre sugerido:

```text
currency
```

El sistema deberá contemplar potencialmente:

- MXN;
- monedas extranjeras;
- tipo de cambio.

El flujo de monedas extranjeras todavía está pendiente de validar.

---

# 31. Tipo de cambio

**Estado:** PENDIENTE DE VALIDAR

Valor utilizado para convertir una operación entre monedas.

Aunque el dato puede venir en el CFDI, todavía no se han definido las reglas contables para moneda extranjera.

---

# 32. Catálogo de cuentas

**Estado:** CONFIRMADO

Conjunto de cuentas contables utilizadas por una empresa.

Cada empresa puede tener un catálogo diferente.

Capacidades esperadas:

- importar;
- crear;
- editar;
- activar;
- desactivar;
- relacionar con catálogo SAT;
- manejar auxiliares;
- registrar saldos iniciales.

Nombre sugerido:

```text
AccountCatalog
```

---

# 33. Cuenta contable

**Estado:** CONFIRMADO

Elemento utilizado para clasificar y acumular movimientos contables.

Ejemplos:

- bancos;
- clientes;
- proveedores;
- ventas;
- gastos;
- compras;
- IVA acreditable;
- IVA trasladado.

Nombre sugerido:

```text
Account
```

---

# 34. Cuenta SAT

**Estado:** CONFIRMADO

Cuenta o código asociado al catálogo requerido o utilizado por SAT.

El sistema podría mantener una relación entre:

```text
Cuenta interna
↕
Código agrupador / cuenta SAT
```

El comportamiento exacto deberá definirse posteriormente.

---

# 35. Cuenta auxiliar

**Estado:** CONFIRMADO

Cuenta utilizada para mantener un nivel adicional de detalle dentro del catálogo.

Puede utilizarse, por ejemplo, para:

- clientes;
- proveedores;
- bancos;
- conceptos específicos.

La estructura jerárquica definitiva del catálogo deberá modelarse posteriormente.

---

# 36. Saldo inicial

**Estado:** CONFIRMADO

Saldo con el que inicia una cuenta en un ejercicio o periodo determinado.

Es especialmente importante para la migración de empresas existentes.

Nombre sugerido:

```text
OpeningBalance
```

o:

```text
AccountBalance
```

---

# 37. Póliza

**Estado:** CONFIRMADO

Registro contable que agrupa un conjunto de partidas.

Puede estar relacionada con uno o varios documentos fiscales.

Tipos identificados:

- diario;
- ingreso;
- egreso;
- cierre;
- ajuste.

Nombre sugerido:

```text
Policy
```

> Nota técnica: aunque `Policy` es traducción literal común dentro de sistemas mexicanos, puede confundirse en inglés con reglas o políticas de autorización. Durante arquitectura conviene valorar nombres como `AccountingEntryBatch`, `JournalEntry` o mantener `Policy` como término ubicuo del proyecto.

---

# 38. Tipo de póliza

**Estado:** CONFIRMADO

Clasificación de una póliza.

Ejemplos:

- ingreso;
- egreso;
- diario;
- cierre;
- ajuste.

Pueden existir series adicionales configurables.

Nombre sugerido:

```text
PolicyType
```

---

# 39. Número de póliza

**Estado:** CONFIRMADO

Identificador consecutivo de una póliza dentro de un contexto determinado.

Ejemplos:

```text
I-001
I-002
E-001
```

La estrategia exacta de numeración todavía debe definirse.

---

# 40. Partida contable

**Estado:** CONFIRMADO

Movimiento individual que forma parte de una póliza.

Contiene normalmente:

- cuenta;
- cargo o abono;
- importe;
- concepto;
- referencia;
- impuestos;
- relaciones relevantes.

Nombre sugerido:

```text
PolicyEntry
```

o:

```text
JournalEntryLine
```

---

# 41. Cargo

**Estado:** CONFIRMADO

Movimiento registrado en el lado de cargos de una partida contable.

Nombre técnico candidato:

```text
debit
```

---

# 42. Abono

**Estado:** CONFIRMADO

Movimiento registrado en el lado de abonos de una partida contable.

Nombre técnico candidato:

```text
credit
```

---

# 43. Póliza balanceada

**Estado:** CONFIRMADO

Póliza donde:

```text
SUM(cargos) = SUM(abonos)
```

Una póliza contabilizada deberá encontrarse balanceada.

---

# 44. Póliza descuadrada

**Estado:** SUPUESTO MVP

Póliza donde:

```text
SUM(cargos) != SUM(abonos)
```

Supuesto inicial:

- puede existir temporalmente como borrador;
- no puede contabilizarse.

Este comportamiento deberá validarse con usuarios.

---

# 45. Borrador de póliza

**Estado:** SUPUESTO MVP

Estado temporal de una póliza que todavía puede modificarse y no representa un registro contable definitivo.

Permitiría:

- partidas incompletas;
- correcciones;
- pólizas temporalmente descuadradas.

Nombre conceptual:

```text
DRAFT
```

---

# 46. Póliza contabilizada

**Estado:** SUPUESTO MVP

Póliza que ha superado las validaciones necesarias y forma parte formal de los movimientos contables.

Condición mínima propuesta:

```text
Total cargos = Total abonos
```

Otros requisitos deberán validarse.

Nombre conceptual:

```text
POSTED
```

---

# 47. Relación XML ↔ póliza

**Estado:** CONFIRMADO

Asociación que mantiene la trazabilidad entre documentos fiscales y registros contables.

Debe soportar relaciones muchos a muchos.

Ejemplo:

```text
Factura
├── Póliza de provisión
└── Póliza de pago
```

y:

```text
Póliza
├── Factura A
├── Factura B
└── Complemento C
```

Nombre técnico candidato:

```text
PolicyDocument
```

---

# 48. Ingreso

**Estado:** CONFIRMADO

Operación relacionada con entradas económicas o documentos emitidos, según el contexto contable.

Puede involucrar cuentas como:

- clientes;
- bancos;
- ventas;
- IVA trasladado.

El tratamiento exacto depende del escenario.

---

# 49. Egreso

**Estado:** CONFIRMADO

Operación relacionada con salidas económicas, compras o gastos.

Puede involucrar:

- proveedores;
- acreedores;
- bancos;
- compras;
- gastos;
- IVA acreditable.

---

# 50. Proveedor

**Estado:** CONFIRMADO

Tercero del que la empresa recibe bienes o servicios.

Puede estar relacionado con:

- CFDI recibidos;
- cuentas por pagar;
- DIOT;
- patrones contables.

Puede ser útil contar con una entidad propia en fases posteriores.

---

# 51. Cliente

**Estado:** CONFIRMADO

Tercero al que la empresa vende bienes o presta servicios.

Puede estar relacionado con:

- CFDI emitidos;
- cuentas por cobrar;
- patrones contables.

---

# 52. Acreedor

**Estado:** CONFIRMADO

Tercero con el que existe una obligación de pago que puede clasificarse contablemente de forma distinta a proveedor.

La distinción exacta dependerá del catálogo y reglas de cada empresa.

---

# 53. Banco

**Estado:** CONFIRMADO

Cuenta o institución utilizada para registrar movimientos financieros.

En el MVP puede representarse inicialmente mediante cuentas contables.

Una entidad bancaria independiente podría introducirse posteriormente si se implementa conciliación bancaria.

---

# 54. IVA

**Estado:** CONFIRMADO

Impuesto al Valor Agregado.

Tasas mencionadas:

- 16 %;
- 8 %;
- 0 %;
- exento.

El sistema deberá preservar tanto la información fiscal del CFDI como su tratamiento contable.

---

# 55. IVA acreditable

**Estado:** CONFIRMADO

IVA asociado generalmente a operaciones recibidas y susceptible de tratamiento como acreditable según las reglas aplicables.

El sistema deberá permitir relacionarlo con cuentas contables específicas.

---

# 56. IVA trasladado

**Estado:** CONFIRMADO

IVA trasladado en operaciones realizadas por la empresa.

Puede relacionarse con operaciones de ingreso y cuentas específicas.

---

# 57. IVA pendiente

**Estado:** CONFIRMADO

Concepto mencionado durante el levantamiento relacionado con IVA todavía no reconocido como pagado o cobrado.

La definición operacional exacta deberá establecerse durante los escenarios PPD.

---

# 58. IVA pagado

**Estado:** CONFIRMADO

Concepto relacionado con IVA correspondiente a operaciones cuyo pago ya ocurrió.

El flujo exacto debe documentarse mediante escenarios contables.

---

# 59. IVA cobrado

**Estado:** CONFIRMADO

Concepto relacionado con IVA correspondiente a operaciones cuyo cobro ya ocurrió.

El tratamiento exacto debe validarse mediante casos reales.

---

# 60. IVA deducible / no deducible

**Estado:** CONFIRMADO

Clasificación mencionada dentro del tratamiento fiscal de gastos.

Las reglas exactas dependen de la operación y deberán documentarse posteriormente.

---

# 61. Tasa de impuesto

**Estado:** CONFIRMADO

Configuración que representa una tasa o tratamiento impositivo.

Ejemplos:

```text
IVA 16 %
IVA 8 %
IVA 0 %
Exento
```

Nombre sugerido:

```text
TaxRate
```

---

# 62. DIOT

**Estado:** CONFIRMADO

Declaración Informativa de Operaciones con Terceros.

El sistema actual prepara información por proveedor y puede generar un archivo TXT.

Información relevante mencionada:

- RFC;
- tipo de tercero;
- tipo de operación;
- país;
- base;
- IVA;
- retenciones;
- zona fronteriza.

Nombre sugerido:

```text
DIOT
```

La implementación completa no está confirmada para el primer MVP.

---

# 63. Registro DIOT

**Estado:** DECISIÓN TÉCNICA

Representación interna de la información necesaria para preparar la DIOT de una operación o proveedor.

Nombre sugerido:

```text
DIOTRecord
```

No necesariamente debe almacenarse de forma permanente; puede derivarse de los movimientos contables.

Esta decisión deberá tomarse durante el diseño.

---

# 64. Balanza de comprobación

**Estado:** CONFIRMADO

Reporte que resume los movimientos y saldos de las cuentas contables.

Debe permitir consultar:

- saldos;
- cargos;
- abonos;
- movimientos;
- cuentas.

Nombre sugerido:

```text
TrialBalance
```

---

# 65. Auxiliar contable

**Estado:** CONFIRMADO

Reporte detallado de movimientos asociados a una cuenta.

Debe permitir rastrear cómo se forma el saldo de una cuenta determinada.

Nombre sugerido:

```text
Ledger
```

o:

```text
AccountLedger
```

---

# 66. Conciliación fiscal

**Estado:** CONFIRMADO

Proceso de comparación entre distintas fuentes de información.

Ejemplos:

```text
XML ↔ Pólizas
Pólizas ↔ Balanza
Balanza ↔ IVA
IVA ↔ DIOT
```

Su objetivo es detectar diferencias o registros incompletos.

---

# 67. Patrón contable

**Estado:** CONFIRMADO

Configuración aprendida o registrada a partir de operaciones anteriores para sugerir cómo contabilizar una nueva operación similar.

Ejemplo:

```text
RFC proveedor X
→ gasto Y
→ proveedor Z
→ IVA acreditable
→ banco A
```

Nombre sugerido:

```text
AccountingPattern
```

Un patrón:

- pertenece a una empresa;
- puede sugerir;
- debe poder modificarse;
- no debe bloquear por sí mismo.

---

# 68. Regla contable

**Estado:** CONFIRMADO

Condición utilizada para validar, advertir o determinar el tratamiento de una operación.

Ejemplos:

- una póliza contabilizada debe estar balanceada;
- cierto tipo de operación requiere determinadas cuentas;
- ciertas configuraciones fiscales deben existir.

Nombre sugerido:

```text
AccountingRule
```

---

# 69. Sugerencia contable

**Estado:** DECISIÓN TÉCNICA

Recomendación generada por el sistema a partir de reglas, patrones o información previa.

Una sugerencia no obliga al usuario.

Ejemplo:

```text
Proveedor: ABC SA
Cuenta sugerida: Gastos de papelería
IVA: IVA acreditable
```

Nombre conceptual:

```text
AccountingSuggestion
```

---

# 70. Advertencia

**Estado:** DECISIÓN TÉCNICA

Validación que informa de una posible inconsistencia pero permite continuar.

Ejemplo:

```text
Este proveedor normalmente se contabiliza en otra cuenta.
```

Nombre conceptual:

```text
WARNING
```

---

# 71. Error bloqueante

**Estado:** DECISIÓN TÉCNICA

Validación que impide completar una operación.

Ejemplo:

```text
No puede contabilizarse una póliza descuadrada.
```

Nombre conceptual:

```text
ERROR
```

La clasificación de cada regla entre advertencia y error deberá validarse progresivamente.

---

# 72. Importación

**Estado:** CONFIRMADO

Proceso mediante el cual información externa entra al sistema.

Inicialmente aplica principalmente a:

- XML;
- catálogo de cuentas;
- posiblemente saldos iniciales.

Nombre sugerido:

```text
Import
```

---

# 73. Importación masiva

**Estado:** CONFIRMADO

Importación de múltiples archivos o registros dentro de una sola operación.

Será especialmente importante para CFDI/XML.

Debe soportar:

- procesamiento en segundo plano;
- progreso;
- errores individuales;
- detección de duplicados.

---

# 74. Exportación

**Estado:** CONFIRMADO

Proceso mediante el cual el sistema genera información descargable.

Formatos mencionados:

- Excel;
- TXT;
- potencialmente PDF.

Nombre sugerido:

```text
Export
```

---

# 75. Reporte configurable

**Estado:** CONFIRMADO

Reporte donde el usuario puede seleccionar qué columnas desea incluir.

Ejemplo:

```text
[✓] RFC
[✓] UUID
[✓] Fecha
[ ] Conceptos
[✓] Total
[✓] IVA
```

Se identificó especialmente para reportes de XML.

---

# 76. Auditoría

**Estado:** CONFIRMADO

Registro histórico de acciones relevantes realizadas en el sistema.

Debe permitir responder preguntas como:

- quién creó;
- quién modificó;
- cuándo ocurrió;
- qué empresa fue afectada;
- qué valores cambiaron.

Nombre sugerido:

```text
AuditLog
```

---

# 77. Migración

**Estado:** CONFIRMADO

Proceso de traslado de información desde los sistemas actuales al nuevo sistema.

Posibles datos:

- catálogo;
- saldos iniciales;
- pólizas;
- XML;
- relaciones históricas.

El alcance definitivo sigue pendiente.

---

# 78. Regla de migración inicial

**Estado:** SUPUESTO MVP

Para reducir complejidad, la primera estrategia podría consistir en migrar:

```text
Catálogo de cuentas
+
Saldos iniciales
```

sin importar todo el histórico.

Debe validarse con los usuarios antes de considerarse una decisión final.

---

# 79. Estado de documento

**Estado:** SUPUESTO MVP

Estado interno utilizado para representar el avance de un documento dentro del flujo contable.

Estados candidatos:

```text
IMPORTED
PENDING
ACCOUNTED
ERROR
```

Los estados definitivos todavía no están cerrados.

---

# 80. Contabilizar

**Estado:** CONFIRMADO

Acción mediante la cual una operación pasa a formar parte formal de los registros contables.

Dentro del sistema deberá diferenciarse de:

```text
guardar
```

y de:

```text
guardar como borrador
```

El conjunto exacto de validaciones previas está pendiente de definir.

---

# 81. Cerrar periodo

**Estado:** PENDIENTE DE VALIDAR

Proceso mediante el cual un periodo deja de aceptar modificaciones ordinarias.

Debe definirse:

- quién puede cerrarlo;
- qué validaciones requiere;
- si puede reabrirse;
- qué ocurre con documentos posteriores;
- cómo se auditan cambios.

---

# 82. Multiempresa

**Estado:** CONFIRMADO

Capacidad del sistema para administrar múltiples empresas independientes desde una misma plataforma.

No implica compartir información contable entre empresas.

---

# 83. Multi-tenant

**Estado:** DECISIÓN TÉCNICA PENDIENTE

Modelo arquitectónico mediante el cual varios clientes, organizaciones o empresas comparten infraestructura manteniendo separación lógica.

Aunque el producto es multiempresa, todavía debe decidirse si técnicamente se utilizará un modelo multi-tenant formal.

No debe confundirse:

```text
requisito de negocio:
multiempresa

con

decisión arquitectónica:
multi-tenancy
```

---

# 84. Procesamiento asíncrono

**Estado:** DECISIÓN TÉCNICA

Ejecución de tareas pesadas fuera del ciclo inmediato de una petición web.

Casos probables:

- importación masiva de XML;
- parseo;
- generación de reportes;
- exportaciones;
- validaciones masivas;
- futuras sincronizaciones SAT.

Nombre técnico general:

```text
Background Job
```

---

# 85. Trazabilidad

**Estado:** CONFIRMADO

Capacidad de reconstruir cómo un documento fiscal terminó afectando la contabilidad.

Ejemplo:

```text
UUID
↓
CFDI
↓
Complemento
↓
Póliza
↓
Partida
↓
Cuenta
↓
Periodo
```

Es uno de los principios centrales del sistema.

---

# 86. Fuente de verdad

**Estado:** DECISIÓN TÉCNICA

Sistema o dato considerado autoritativo para un determinado concepto.

Ejemplos potenciales:

```text
Archivo XML original
→ fuente de verdad del contenido importado

Póliza contabilizada
→ fuente de verdad del movimiento contable interno
```

Este concepto será importante cuando se implementen sincronizaciones externas.

---

# 87. Glosario técnico recomendado

Para evitar inconsistencias en código y documentación se propone utilizar inicialmente estas convenciones:

| Negocio | Nombre sugerido en código |
|---|---|
| Organización | `Organization` |
| Usuario | `User` |
| Empresa | `Company` |
| Periodo contable | `AccountingPeriod` |
| Documento fiscal / CFDI | `FiscalDocument` |
| Concepto CFDI | `FiscalDocumentConcept` |
| Impuesto CFDI | `FiscalDocumentTax` |
| Relación CFDI | `FiscalDocumentRelation` |
| Complemento de pago | `PaymentComplement` |
| Catálogo de cuentas | `AccountCatalog` |
| Cuenta contable | `Account` |
| Saldo inicial | `OpeningBalance` |
| Póliza | `Policy`* |
| Partida | `PolicyEntry`* |
| Regla contable | `AccountingRule` |
| Patrón contable | `AccountingPattern` |
| Tasa de impuesto | `TaxRate` |
| Registro DIOT | `DIOTRecord` |
| Auditoría | `AuditLog` |
| Importación | `Import` |
| Exportación | `Export` |

`*` Los nombres `Policy` y `PolicyEntry` deben revisarse antes de comenzar la implementación porque pueden resultar ambiguos en inglés.

---

# 88. Términos que no deben confundirse

## XML vs CFDI

```text
XML = representación/archivo
CFDI = documento fiscal
```

---

## Método de pago vs forma de pago

Son atributos fiscales diferentes y deberán almacenarse por separado.

---

## Factura vs CFDI

```text
Factura ⊂ CFDI
```

No todos los CFDI son facturas.

---

## Guardar póliza vs contabilizar póliza

```text
Guardar
= persistir información

Contabilizar
= convertirla en registro contable válido
```

---

## Regla vs patrón

```text
Regla
= valida o determina comportamiento

Patrón
= recuerda o sugiere comportamiento previo
```

---

## Advertencia vs error

```text
Advertencia
= permite continuar

Error
= bloquea la operación
```

---

## Multiempresa vs multi-tenant

```text
Multiempresa
= requisito funcional

Multi-tenant
= decisión arquitectónica
```

---

# 89. Provisión

**Estado:** PENDIENTE DE VALIDAR

Registro contable de una operación antes de que ocurra el cobro o pago efectivo.

Dentro del proyecto, este concepto permite representar situaciones en las que ya existe:

- un ingreso;
- un gasto;
- una cuenta por cobrar;
- una cuenta por pagar;

aunque todavía no haya ocurrido el movimiento bancario correspondiente.

Puede ser especialmente relevante en operaciones PPD.

Ejemplo conceptual:

```text
Factura recibida
    ↓
Provisión
    ↓
Cuenta por pagar
    ↓
Pago posterior
```

**Pendiente de confirmar:**

- cuándo utiliza provisiones el despacho;
- qué cuentas utiliza;
- qué tipos de CFDI generan provisión;
- cómo afecta IVA;
- si la provisión se genera manual o automáticamente.

---

# 90. Cuenta por cobrar

**Estado:** PENDIENTE DE VALIDAR

Importe que un cliente u otro tercero todavía debe pagar a la empresa.

Dentro del sistema puede representar el saldo pendiente derivado de una operación de ingreso que todavía no ha sido cobrada.

Ejemplo conceptual:

```text
Factura emitida
    ↓
Cuenta por cobrar
    ↓
Cobro
    ↓
Banco
```

Normalmente estará asociada a una cuenta contable de clientes o equivalente.

**Pendiente de confirmar:**

- qué cuentas se utilizan;
- cómo se manejan auxiliares por cliente;
- cuándo se considera liquidada;
- cómo se relacionan pagos parciales.

---

# 91. Cuenta por pagar

**Estado:** PENDIENTE DE VALIDAR

Importe que la empresa todavía debe pagar a un proveedor, acreedor u otro tercero.

Dentro del sistema puede representar obligaciones derivadas de CFDI recibidos pendientes de pago.

Ejemplo conceptual:

```text
Factura recibida
    ↓
Cuenta por pagar
    ↓
Pago
    ↓
Banco
```

**Pendiente de confirmar:**

- diferencia operativa entre proveedor y acreedor;
- cuentas utilizadas;
- manejo de auxiliares;
- pagos parciales;
- reglas por tipo de gasto.

---

# 92. Cancelación de CFDI

**Estado:** PENDIENTE DE VALIDAR

Cambio de estado de un CFDI mediante el cual deja de considerarse vigente fiscalmente.

Dentro del sistema, una cancelación no debería eliminar el documento original.

El sistema debería conservar:

- XML original;
- UUID;
- estado fiscal;
- fecha o datos de cancelación cuando estén disponibles;
- relaciones con pólizas;
- historial de cambios.

Ejemplo:

```text
FiscalDocument
├── UUID
├── status: CANCELLED
└── AccountingPolicies relacionadas
```

**Pendiente de confirmar:**

- cómo se detectarán cancelaciones;
- qué debe ocurrir si el CFDI ya fue contabilizado;
- si se genera alerta;
- si se requiere una póliza de reversa;
- cómo se manejan cancelaciones posteriores al cierre del periodo.

---

# 93. Sustitución de CFDI

**Estado:** PENDIENTE DE VALIDAR

Relación mediante la cual un CFDI es sustituido por otro debido a una corrección u otro motivo fiscal válido.

El sistema debe conservar la trazabilidad entre ambos documentos.

Ejemplo conceptual:

```text
CFDI A [CANCELLED]
    ↓ REPLACED_BY
CFDI B [ACTIVE]
```

Esta relación podría representarse mediante:

```text
FiscalDocumentRelation
```

**Pendiente de confirmar:**

- qué tipos de relación deben soportarse;
- cómo afecta pólizas existentes;
- si el nuevo CFDI reemplaza automáticamente asociaciones previas;
- qué advertencias debe mostrar el sistema.

---

# 94. Nota de crédito

**Estado:** PENDIENTE DE VALIDAR

Documento fiscal utilizado para disminuir, corregir o afectar total o parcialmente una operación previa.

Debe poder relacionarse con el documento que modifica.

Ejemplo:

```text
Factura original
    ↓
Nota de crédito
```

El efecto contable puede implicar disminuciones o reclasificaciones de:

- ingresos;
- gastos;
- clientes;
- proveedores;
- impuestos.

**Pendiente de confirmar:**

- flujo exacto utilizado por el despacho;
- cuentas involucradas;
- tratamiento de IVA;
- relación con pólizas previas;
- efecto en saldos pendientes.

---

# 95. Retención

**Estado:** PENDIENTE DE VALIDAR

Importe de un impuesto que uno de los participantes de una operación retiene en lugar de entregarlo íntegramente a la contraparte.

Dentro del sistema debe mantenerse separado de otros impuestos trasladados.

Puede formar parte de:

- información extraída del CFDI;
- partidas contables;
- reportes fiscales;
- DIOT u otros procesos.

Nombre técnico candidato:

```text
TaxWithholding
```

**Pendiente de confirmar:**

- tipos de retención necesarios;
- cuentas contables utilizadas;
- reglas por régimen fiscal;
- impacto en IVA, ISR y reportes.

---

# 96. Deducibilidad

**Estado:** PENDIENTE DE VALIDAR

Clasificación que indica si un gasto puede considerarse total o parcialmente para efectos fiscales.

Dentro del sistema podría manejarse como una característica de una operación, gasto o partida.

Estados conceptuales potenciales:

```text
DEDUCTIBLE
PARTIALLY_DEDUCTIBLE
NON_DEDUCTIBLE
```

Estos estados todavía no son una decisión definitiva.

**Pendiente de confirmar:**

- qué reglas utiliza el despacho;
- si la clasificación se realiza por CFDI, concepto o partida;
- cómo se determina un porcentaje deducible;
- qué impacto tiene en IVA y DIOT.

---

# 97. IVA pendiente

**Estado:** PENDIENTE DE VALIDAR

IVA relacionado con una operación registrada cuyo pago o cobro efectivo todavía no se ha producido según el tratamiento contable utilizado.

Este concepto puede ser especialmente importante para operaciones PPD.

Ejemplo conceptual:

```text
Factura PPD
    ↓
IVA pendiente
    ↓ ocurre pago/cobro
IVA efectivamente pagado/cobrado
```

**Pendiente de confirmar:**

- cuentas utilizadas;
- momento exacto del movimiento;
- reglas diferentes para ingresos y egresos;
- tratamiento de pagos parciales.

---

# 98. IVA efectivamente pagado

**Estado:** PENDIENTE DE VALIDAR

IVA asociado a una operación de compra o gasto cuyo pago ya ocurrió efectivamente.

Dentro del sistema podría representar el cambio desde una cuenta de IVA pendiente hacia una cuenta de IVA acreditable o equivalente.

Ejemplo conceptual:

```text
IVA pendiente
    ↓ pago
IVA efectivamente pagado
```

**Pendiente de confirmar:**

- cuentas exactas utilizadas;
- relación con IVA acreditable;
- tratamiento parcial;
- reglas asociadas a complementos de pago.

---

# 99. IVA efectivamente cobrado

**Estado:** PENDIENTE DE VALIDAR

IVA asociado a una operación de venta o ingreso cuyo cobro ya ocurrió efectivamente.

Dentro del sistema podría representar el cambio desde una cuenta de IVA pendiente hacia una cuenta correspondiente a IVA trasladado/cobrado.

Ejemplo conceptual:

```text
IVA pendiente
    ↓ cobro
IVA efectivamente cobrado
```

**Pendiente de confirmar:**

- cuentas exactas;
- tratamiento de cobros parciales;
- relación con complementos;
- impacto en reportes fiscales.

---

# 100. Cierre contable

**Estado:** PENDIENTE DE VALIDAR

Proceso mediante el cual un periodo contable se considera terminado y deja de aceptar modificaciones ordinarias.

Modelo conceptual propuesto:

```text
AccountingPeriod
OPEN
  ↓ cierre
CLOSED
```

Antes de cerrar un periodo podrían ejecutarse validaciones como:

- pólizas balanceadas;
- documentos pendientes;
- balanza;
- IVA;
- DIOT;
- inconsistencias.

**Pendiente de confirmar:**

- quién puede cerrar;
- validaciones obligatorias;
- si el cierre es mensual o anual;
- qué movimientos siguen permitidos después del cierre.

---

# 101. Reapertura

**Estado:** PENDIENTE DE VALIDAR

Acción excepcional mediante la cual un periodo previamente cerrado vuelve a permitir modificaciones.

Modelo conceptual:

```text
CLOSED
  ↓ reapertura
OPEN
```

La reapertura debería quedar registrada en auditoría.

**Pendiente de confirmar:**

- quién puede reabrir;
- motivos permitidos;
- si requiere autorización;
- qué información debe registrarse;
- si existe algún límite temporal.

---

# 102. Póliza de cierre

**Estado:** PENDIENTE DE VALIDAR

Tipo de `AccountingPolicy` utilizado durante procesos de cierre contable.

Puede utilizarse para realizar movimientos relacionados con el cierre de un periodo o ejercicio.

Nombre sugerido:

```text
AccountingPolicyType.CLOSING
```

**Pendiente de confirmar:**

- qué movimientos incluye;
- cuándo se genera;
- si es automática o manual;
- si corresponde al cierre mensual o anual;
- cuentas que intervienen.

---

# 103. Póliza de ajuste

**Estado:** PENDIENTE DE VALIDAR

Tipo de `AccountingPolicy` utilizada para corregir, reclasificar o ajustar movimientos contables.

Puede existir sin estar vinculada a un CFDI.

Este concepto establece una regla importante para el modelo:

```text
AccountingPolicy
    └── FiscalDocument relation: optional
```

No toda póliza debe requerir un documento fiscal.

Nombre sugerido:

```text
AccountingPolicyType.ADJUSTMENT
```

**Pendiente de confirmar:**

- tipos de ajustes utilizados;
- permisos requeridos;
- tratamiento en periodos cerrados;
- necesidad de referencias o documentos justificativos.

---

# 104. Moneda extranjera

**Estado:** PENDIENTE DE VALIDAR

Operación expresada en una moneda diferente de la moneda base contable de la empresa.

Ejemplos potenciales:

```text
USD
EUR
```

El sistema debería conservar al menos:

- moneda original;
- importe original;
- tipo de cambio utilizado;
- importe convertido cuando corresponda.

**Pendiente de confirmar:**

- moneda base por empresa;
- monedas utilizadas actualmente;
- reglas de conversión;
- manejo de diferencias cambiarias;
- momento en que se toma el tipo de cambio.

---

# 105. Tipo de cambio

**Estado:** PENDIENTE DE VALIDAR

Factor utilizado para convertir el valor de una moneda a otra.

Dentro del sistema debe conservarse el valor utilizado históricamente en cada operación.

Ejemplo:

```text
100 USD
× tipo de cambio
= importe equivalente en MXN
```

El sistema no debería modificar movimientos históricos simplemente porque posteriormente cambió el tipo de cambio de mercado.

**Pendiente de confirmar:**

- fuente del tipo de cambio;
- fecha aplicable;
- posibilidad de captura manual;
- precisión decimal;
- reglas para diferencias cambiarias.

---

# 106. Conciliación bancaria

**Estado:** PENDIENTE DE VALIDAR

Proceso de comparación entre los movimientos registrados en las cuentas contables de bancos y los movimientos reportados por las instituciones bancarias.

Ejemplo conceptual:

```text
Movimientos bancarios
        ↕
Conciliación
        ↕
AccountingPolicyEntries
```

Podría permitir identificar:

- movimientos sin contabilizar;
- movimientos duplicados;
- diferencias de importe;
- depósitos o retiros pendientes.

Probablemente corresponde a una fase posterior al MVP.

**Pendiente de confirmar:**

- si actualmente realizan conciliación dentro del sistema contable;
- formatos bancarios utilizados;
- bancos principales;
- frecuencia;
- nivel de automatización deseado.

---

# 107. Contabilidad electrónica

**Estado:** PENDIENTE DE VALIDAR

Conjunto de procesos y archivos estructurados relacionados con obligaciones de información contable electrónica.

Dentro del proyecto debe distinguirse de simplemente operar una plataforma contable web.

Puede incluir potencialmente:

- catálogo de cuentas;
- balanza;
- archivos estructurados;
- exportaciones requeridas fiscalmente.

Probablemente corresponde a una fase posterior.

**Pendiente de confirmar:**

- qué archivos necesita generar actualmente el despacho;
- periodicidad;
- formatos;
- validaciones;
- si deben enviarse desde el sistema o únicamente descargarse.

---

# 108. Implicaciones de dominio derivadas

Las definiciones anteriores permiten asumir provisionalmente algunas características del modelo, sin considerarlas todavía reglas definitivas del negocio.

## AccountingPolicy puede existir sin CFDI

Ejemplos potenciales:

- póliza de ajuste;
- póliza de cierre;
- reclasificaciones.

Por lo tanto:

```text
AccountingPolicy
    ↕ optional
FiscalDocument
```

---

## Un CFDI puede producir movimientos en diferentes momentos

Especialmente en escenarios PPD:

```text
FiscalDocument
├── AccountingPolicy de provisión
├── PaymentComplement A
│   └── AccountingPolicy de pago/cobro
└── PaymentComplement B
    └── AccountingPolicy de pago/cobro
```

---

## Cancelar un CFDI no significa eliminarlo

El sistema deberá priorizar trazabilidad.

Modelo conceptual:

```text
ACTIVE
↓
CANCELLED
```

El documento debe permanecer disponible para auditoría y relaciones históricas.

---

## Estado fiscal y estado contable son conceptos diferentes

Ejemplo:

```text
FiscalDocument.status
ACTIVE / CANCELLED

AccountingPolicy.status
DRAFT / POSTED / CANCELLED

AccountingPeriod.status
OPEN / CLOSED
```

Los nombres y estados definitivos todavía deben confirmarse.

---

# 109. Regla para evolución del glosario

Cuando aparezca un nuevo término durante:

- entrevistas;
- desarrollo;
- pruebas;
- revisión de casos contables;
- especificaciones;

deberá añadirse aquí antes de utilizar significados distintos en diferentes módulos.

Idealmente cada término debe indicar:

```text
Nombre
Definición
Estado
Ejemplo
Nombre técnico
Relaciones
Preguntas pendientes
```

Esto permitirá que el glosario se convierta progresivamente en el **lenguaje ubicuo del dominio**.
