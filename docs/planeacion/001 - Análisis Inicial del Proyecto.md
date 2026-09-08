# Sistema Contable — Análisis Inicial del Proyecto

> **Estado:** Borrador de descubrimiento / análisis inicial  
> **Propósito:** Documento base de conocimiento del proyecto  
> **Fuente:** Primera conversación de levantamiento de requerimientos  
> **Última actualización:** 2026-08-31

**Navegación:** [Inicio](00%20-%20Inicio.md) · [Glosario](002%20-%20Glosario.md) · [MVP](003%20-%20MVP-Scope.md) · [Escenarios](004%20-%20Escenarios%20contables.md) · [Reglas](005%20-%20Reglas%20de%20negocio.md) · [Preguntas](006%20-%20Preguntas%20Abiertas.md)

---

## 1. Resumen ejecutivo

El proyecto busca construir una **plataforma contable web multiempresa** que concentre procesos que actualmente se realizan utilizando varias aplicaciones de escritorio.

El flujo actual está fragmentado entre herramientas como:

- Conta Fiscal.
- DD / Documentos Digitales.
- Sistemas de descarga masiva de XML.
- Herramientas adicionales para DIOT u otros procesos.

La intención del nuevo sistema es centralizar principalmente:

- Gestión de empresas y usuarios.
- Importación y administración de CFDI/XML.
- Catálogo de cuentas.
- Creación de pólizas contables.
- Relación entre XML y pólizas.
- Registro de ingresos y egresos.
- Manejo de PUE, PPD y complementos de pago.
- IVA.
- DIOT.
- Balanza de comprobación.
- Reportes y exportaciones.
- Reglas y patrones contables por empresa.

El núcleo funcional del sistema puede resumirse como:

> **Transformar información fiscal proveniente de CFDI/XML en movimientos contables, manteniendo trazabilidad entre documentos, pólizas, cuentas, impuestos y periodos.**

---

## 2. Contexto actual

El despacho trabaja aproximadamente con:

- **50 a 60 empresas.**
- **6 usuarios simultáneos**, aproximadamente.

El proceso actual requiere utilizar varios sistemas y realizar pasos manuales entre ellos.

Flujo identificado:

1. Ingresar al portal o servicio relacionado con SAT.
2. Descargar XML emitidos y recibidos.
3. Incorporar los XML al repositorio de documentos.
4. Abrir el sistema contable.
5. Seleccionar documentos.
6. Crear o asociar pólizas.
7. Asignar cuentas contables.
8. Generar partidas.
9. Revisar IVA y DIOT.
10. Generar reportes.
11. Exportar archivos para procesos fiscales.

### Problemas detectados

- Información distribuida entre distintos sistemas.
- Cambio lento entre empresas.
- Procesos manuales repetitivos.
- Lentitud al manejar grandes cantidades de XML.
- Dependencia de infraestructura local.
- Riesgo de interrupción por fallos del servidor de oficina.
- Dificultad para trabajar remotamente.
- Necesidad de repetir configuraciones contables frecuentes.

---

## 3. Objetivo del producto

Construir una aplicación web que permita a un despacho contable administrar múltiples empresas y ejecutar el flujo contable mensual desde una única plataforma.

El sistema deberá permitir:

```text
Empresa
  ↓
Periodo
  ↓
Importación de XML
  ↓
Clasificación
  ↓
Selección de documentos
  ↓
Creación de póliza
  ↓
Asignación de cuentas
  ↓
Generación de partidas
  ↓
Validación contable
  ↓
Balanza / reportes / procesos fiscales
```

---

## 4. Principios iniciales del sistema

### 4.1 Multiempresa

Toda la información contable deberá pertenecer a una empresa.

Cada empresa mantiene de forma independiente:

- Datos fiscales.
- Periodos.
- Catálogo de cuentas.
- XML.
- Pólizas.
- Saldos.
- Configuración fiscal.
- Reglas contables.
- Patrones contables.

### 4.2 Trazabilidad

Debe ser posible conocer la relación entre:

```text
CFDI/XML
↕
Complementos / documentos relacionados
↕
Pólizas
↕
Partidas
↕
Cuentas
↕
Impuestos
↕
Periodo contable
```

### 4.3 Flexibilidad controlada

Durante las primeras etapas del producto conviene evitar reglas excesivamente rígidas.

En términos generales:

1. El sistema propone.
2. El usuario puede modificar.
3. El sistema advierte inconsistencias.
4. Las reglas validadas pueden convertirse posteriormente en bloqueos.

### 4.4 Automatización progresiva

La prioridad inicial es construir correctamente el dominio contable.

La automatización deberá añadirse después de contar con reglas suficientemente validadas.

---

# 5. Actores del sistema

## 5.1 Administrador

Responsabilidades identificadas:

- Crear usuarios.
- Crear empresas.
- Asignar empresas a usuarios.
- Configurar permisos.
- Administrar configuraciones generales.
- Administrar catálogos.
- Consultar todas las empresas.
- Desactivar o eliminar empresas.
- Administrar límites de usuarios.

## 5.2 Contador

Responsabilidades:

- Seleccionar una empresa.
- Seleccionar un periodo.
- Consultar XML.
- Crear pólizas.
- Asignar cuentas.
- Revisar impuestos.
- Generar reportes.
- Consultar balanzas.
- Preparar información fiscal.

## 5.3 Roles potenciales posteriores

No están confirmados para el MVP:

- Supervisor contable.
- Auditor.
- Auxiliar contable.
- Cliente con acceso de lectura.

---

# 6. Empresas

Cada empresa debe contener, como mínimo:

- RFC.
- Razón social.
- Régimen fiscal.
- Catálogo de cuentas.
- Periodos contables.
- XML.
- Pólizas.
- Configuración de IVA.
- Configuración de DIOT.
- Saldos iniciales.
- Reglas contables.
- Patrones contables.

Los administradores deben poder asignar empresas específicas a cada contador.

Ejemplo:

```text
Contador A
├── Empresa 1
├── Empresa 2
└── Empresa 3

Contador B
├── Empresa 4
└── Empresa 5
```

---

# 7. Periodos contables

El contexto principal de trabajo deberá estar determinado por:

- Empresa.
- Año.
- Mes.

Ejemplo:

```text
Empresa: Empresa X
Ejercicio: 2026
Periodo: Julio
```

Estados potenciales de un periodo:

- Abierto.
- En proceso.
- Cerrado.
- Bloqueado.

> Los estados anteriores son una propuesta derivada del análisis y deben validarse.

Se identificó que el trabajo contable puede realizarse posteriormente al mes de origen.

Ejemplo:

> Durante agosto puede contabilizarse información correspondiente a julio.

---

# 8. Documentos fiscales / CFDI / XML

Este módulo representa uno de los componentes centrales del sistema.

## 8.1 Tipos de documentos identificados

- Facturas emitidas.
- Facturas recibidas.
- Complementos de pago emitidos.
- Complementos de pago recibidos.
- Nómina emitida.
- Notas de crédito.
- Documentos relacionados.
- Adendas.

Algunos de estos tipos deben validarse para determinar si pertenecen al MVP.

---

## 8.2 Formas de incorporación

### MVP

- Carga manual.
- Carga masiva.

### Futuro

- Descarga automática desde SAT o proveedor externo.
- Descarga programada.
- Sincronización periódica.

La descarga automática **no está confirmada como requisito del MVP**.

---

## 8.3 Información a extraer

Campos identificados:

- UUID.
- RFC emisor.
- RFC receptor.
- Nombre del emisor.
- Nombre del receptor.
- Fecha.
- Serie.
- Folio.
- Subtotal.
- IVA.
- Total.
- Tipo de comprobante.
- Método de pago.
- Forma de pago.
- Moneda.
- Tipo de cambio.
- Uso de CFDI.
- Régimen fiscal.
- Conceptos.
- Impuestos.
- Documentos relacionados.
- Complementos.
- Adendas.

---

## 8.4 Estado de procesamiento

El sistema actual utiliza señales visuales para indicar distintos estados.

El nuevo sistema deberá contar con un estado equivalente.

Estados conceptuales posibles:

- Importado.
- Pendiente de contabilizar.
- Seleccionado.
- Contabilizado.
- Relacionado con póliza.
- Con error.

> La nomenclatura definitiva aún debe definirse.

---

# 9. Catálogo de cuentas

Cada empresa deberá disponer de su propio catálogo.

Capacidades identificadas:

- Crear cuentas.
- Editar cuentas.
- Activar o desactivar cuentas.
- Importación masiva.
- Relacionar cuentas internas con catálogo SAT.
- Manejar cuentas auxiliares.
- Registrar saldos iniciales.
- Manejar cuentas por cliente o proveedor.

Ejemplos de cuentas relevantes:

- Bancos.
- Clientes.
- Proveedores.
- IVA acreditable.
- IVA trasladado.
- Ventas.
- Gastos.
- Compras.
- Inventarios.

## Migración

El levantamiento sugiere que podría no ser necesario migrar todo el histórico.

Una estrategia potencial sería migrar únicamente:

- Catálogo de cuentas.
- Saldos iniciales.
- Correspondencias entre cuentas existentes y nuevas.

Esto aún debe validarse por empresa.

---

# 10. Pólizas contables

Tipos principales identificados:

- Diario.
- Ingresos.
- Egresos.
- Cierre.
- Ajustes.

También pueden existir series o tipos personalizados.

Ejemplos:

- Ingreso 1.
- Ingreso 2.
- Transferencia.
- Cheque.
- Tarjeta.
- Ajuste de cierre.

## Datos básicos

Una póliza deberá contener:

- Empresa.
- Periodo.
- Fecha.
- Tipo.
- Número.
- Concepto.
- Moneda.
- Estado.
- Usuario creador.
- Partidas.
- XML relacionados.

## Numeración

Posibilidades detectadas:

- Consecutiva.
- Automática.
- Editable.
- Configurable por tipo.

Ejemplo:

```text
I-001
I-002
E-001
D-001
```

---

# 11. Partidas contables

Una partida puede contener:

- Cuenta contable.
- Cargo.
- Abono.
- Concepto.
- Referencia.
- XML relacionado.
- Impuesto.
- Tasa de IVA.
- Cliente o proveedor.
- Centro de costo, si aplica.

## Regla contable fundamental

```text
Total cargos = Total abonos
```

Una póliza no deberá considerarse finalizada si está descuadrada.

Debe definirse posteriormente si una póliza descuadrada:

- No puede guardarse.
- Puede guardarse como borrador.
- No puede cerrarse o contabilizarse.

---

# 12. Flujo de ingresos

Flujo identificado:

1. Seleccionar empresa.
2. Seleccionar periodo.
3. Consultar XML de ingresos.
4. Seleccionar uno o varios documentos.
5. Crear póliza de ingresos.
6. Asignar cuentas.
7. Generar partidas.
8. Relacionar documentos.
9. Guardar póliza.

Cuentas comunes:

- Clientes.
- Bancos.
- Ventas.
- IVA trasladado.

---

# 13. Flujo de egresos

Flujo identificado:

1. Seleccionar XML recibido.
2. Crear póliza de egreso.
3. Definir proveedor o acreedor.
4. Definir banco.
5. Definir cuenta de gasto o compra.
6. Definir IVA acreditable.
7. Guardar póliza.

Cuentas comunes:

- Proveedores.
- Acreedores.
- Bancos.
- Compras.
- Gastos.
- IVA acreditable.

Además existen configuraciones relacionadas con DIOT:

- Tipo de gasto.
- Deducción.
- Tipo de operación.
- Tasa de IVA.
- Zona fronteriza.
- Resto del país.
- Acumula o deduce.

---

# 14. PUE, PPD y complementos de pago

Esta es una de las áreas con mayor complejidad del dominio.

## 14.1 PUE

Pago en una sola exhibición.

El tratamiento contable exacto deberá validarse con los usuarios contables.

## 14.2 PPD

Pago en parcialidades o diferido.

Puede requerir:

- Registrar la factura.
- Registrar posteriormente pagos.
- Relacionar complementos.
- Manejar pagos parciales.
- Manejar pagos en distintos periodos.
- Reconocer movimientos de IVA según corresponda.

---

## 14.3 Ejemplo de pago parcial

Factura:

```text
Total: $100,000
```

Pagos:

```text
Julio  -> $50,000
Agosto -> $50,000
```

Esto implica potencialmente:

```text
Factura
├── Complemento julio
│   └── Póliza julio
└── Complemento agosto
    └── Póliza agosto
```

---

## 14.4 Cardinalidades identificadas

- Una factura puede tener varios complementos.
- Una factura puede estar relacionada con varias pólizas.
- Una póliza puede contener varios XML.
- Un XML puede estar relacionado con varias pólizas.
- Un complemento debe relacionarse con una factura.
- Un complemento puede asociarse con una póliza.

Estas relaciones deberán modelarse explícitamente en el dominio y la base de datos.

---

# 15. Patrones contables

Una de las principales oportunidades de automatización consiste en recordar cómo suele contabilizarse una operación.

Ejemplo:

```text
Proveedor X
→ Cuenta de gasto Y
→ Cuenta de proveedor Z
→ IVA acreditable
→ Banco A
```

Cuando vuelva a aparecer un documento equivalente, el sistema podría sugerir esas cuentas.

## Atributos potenciales del patrón

- Empresa.
- RFC proveedor.
- RFC cliente.
- Concepto.
- Clave de producto.
- Tipo de CFDI.
- Método de pago.
- Tipo de póliza.
- Cuenta de gasto.
- Cuenta de IVA.
- Cuenta bancaria.
- Cuenta de proveedor o cliente.

## Comportamiento esperado

1. El sistema detecta un patrón.
2. Sugiere cuentas.
3. El usuario acepta o modifica.
4. La corrección puede alimentar futuras sugerencias.

La sugerencia no debería impedir que el contador modifique el asiento.

---

# 16. Reglas contables

Se identificó que muchas reglas dependen de:

- Empresa.
- Régimen fiscal.
- Tipo de operación.
- Criterios del contador.
- Método de pago.
- Periodo.
- Política interna.

Ejemplos:

- Cuenta asociada a un proveedor.
- Momento de registrar banco.
- Uso de clientes o proveedores.
- Provisionamiento.
- Manejo PPD.
- Tratamiento de IVA.
- Tratamiento de pagos parciales.
- Diferencias entre personas físicas y morales.

## Estrategia propuesta

### Primera etapa

- Permitir operaciones.
- Mostrar advertencias.
- Registrar decisiones.

### Etapa posterior

- Configurar reglas.
- Validar automáticamente.
- Bloquear operaciones cuya regla esté confirmada.

---

# 17. IVA

Tasas identificadas:

- 16 %.
- 8 %.
- 0 %.
- Exento.

Conceptos mencionados:

- IVA acreditable.
- IVA trasladado.
- IVA pendiente.
- IVA pagado.
- IVA cobrado.
- IVA deducible.
- IVA no deducible.

También debe distinguirse entre:

- Zona fronteriza.
- Resto del país.

## Catálogo de impuestos

Posibles atributos:

- Clave.
- Porcentaje.
- Tipo.
- Gravado / exento.
- Aplicación fronteriza.
- Aplicación nacional.
- Cuenta asociada.
- Configuración DIOT.

---

# 18. DIOT

El sistema deberá poder preparar información para DIOT.

Campos mencionados:

- Tipo de tercero.
- Tipo de operación.
- País.
- Nacional o extranjero.
- Tasa de IVA.
- IVA acreditable.
- IVA no acreditable.
- IVA retenido.
- Zona fronteriza.
- Resto del país.
- Proveedor.
- RFC.
- Base.
- Impuesto.

El sistema actual genera un TXT separado por `|`.

Ejemplo conceptual:

```text
RFC|TIPO_TERCERO|TIPO_OPERACION|BASE|IVA|RETENCION
```

Funciones identificadas:

- Configuración por operación.
- Consolidación por periodo.
- Comparación contra balanza.
- Detección de diferencias.
- Validación.
- Generación de TXT.
- Descarga.

## No confirmado

El envío directo al SAT se mencionó como posibilidad futura, pero **no está confirmado como requisito**.

---

# 19. Balanza y auxiliares

Después de contabilizar debe poder generarse:

- Balanza de comprobación.
- Auxiliares.
- Saldos.
- Movimientos.
- Cargos.
- Abonos.

La balanza deberá permitir revisar cuentas relevantes como:

- IVA acreditable.
- IVA trasladado.
- Clientes.
- Proveedores.
- Bancos.
- Gastos.
- Ingresos.

---

# 20. Conciliaciones y validaciones

El sistema deberá facilitar la comparación entre:

- XML.
- Pólizas.
- Balanza.
- IVA.
- DIOT.
- Reportes fiscales.

Inconsistencias potenciales a detectar:

- XML contabilizado sin configuración DIOT.
- XML sin cuenta de IVA.
- Factura sin complemento esperado.
- Complemento sin factura relacionada.
- Factura duplicada.
- Diferencias entre IVA fiscal y contable.
- Documento sin tasa.
- Póliza descuadrada.

> Debe validarse cuáles de estas verificaciones pertenecen al MVP y cuáles a fases posteriores.

---

# 21. Reportes y exportaciones

Exportaciones identificadas:

- Excel.
- TXT.
- PDF, potencialmente.

Reportes:

- XML.
- Pólizas.
- Balanza.
- Auxiliares.
- Saldos.
- IVA.
- DIOT.
- Catálogo de cuentas.

## Reportería de XML

Se desea un reporte configurable donde el usuario pueda seleccionar columnas.

Ejemplos:

- RFC.
- Razón social.
- Serie.
- Folio.
- Fecha.
- UUID.
- Subtotal.
- IVA.
- Total.
- Método de pago.
- Forma de pago.
- Tipo de comprobante.
- Conceptos.
- Clave de producto.
- Moneda.
- Régimen.

Flujo esperado:

1. Elegir tipo de documento.
2. Elegir periodo.
3. Seleccionar columnas.
4. Aplicar filtros.
5. Exportar.

---

# 22. Auditoría

El sistema debe conservar trazabilidad de acciones relevantes.

Ejemplos:

- Quién creó una póliza.
- Quién modificó una póliza.
- Quién modificó una cuenta.
- Quién eliminó o desactivó un registro.
- Fecha y hora.
- Empresa afectada.
- Valores anteriores y posteriores, cuando corresponda.

El alcance exacto de auditoría para el MVP deberá definirse.

---

# 23. Infraestructura

La solución propuesta es una plataforma web alojada en la nube.

Beneficios esperados:

- Acceso remoto.
- Menor dependencia del servidor de oficina.
- Actualizaciones centralizadas.
- Respaldos.
- Mejor escalabilidad.
- Acceso desde navegador.

Aspectos técnicos a considerar:

- Respaldos.
- Seguridad de información fiscal.
- Registro de errores.
- Reintentos.
- Procesamiento asíncrono.
- Importaciones masivas.
- Recuperación ante fallos.

---

# 24. Rendimiento

El rendimiento es un requisito importante debido a problemas detectados en el sistema actual.

Problemas actuales:

- Apertura lenta de empresas.
- Cambio lento entre empresas.
- Generación lenta de archivos.
- Bloqueos al procesar gran cantidad de movimientos.
- Problemas con grandes volúmenes de XML.

Consideraciones técnicas propuestas:

- Procesamiento en segundo plano.
- Colas.
- Indicadores de progreso.
- Paginación.
- Búsqueda eficiente.
- Índices de base de datos.
- Caché cuando corresponda.
- Importaciones por lotes.

---

# 25. Operación mensual propuesta

```text
1. Seleccionar empresa
2. Seleccionar periodo
3. Importar XML
4. Clasificar documentos
5. Crear pólizas
6. Relacionar XML
7. Aplicar cuentas
8. Revisar IVA
9. Revisar DIOT
10. Generar balanza
11. Corregir diferencias
12. Cerrar periodo
```

---

# 26. Módulos funcionales

## M01 — Autenticación y usuarios

- Inicio de sesión.
- Recuperación de contraseña.
- Roles.
- Permisos.
- Sesiones.
- Auditoría básica.

## M02 — Empresas

- Crear.
- Editar.
- RFC.
- Régimen fiscal.
- Ejercicios.
- Periodos.
- Asignación de usuarios.

## M03 — Catálogo de cuentas

- Importación.
- Alta y edición.
- Relación SAT.
- Saldos iniciales.
- Auxiliares.

## M04 — Documentos fiscales

- Carga XML.
- Clasificación.
- Consulta.
- Visualización.
- Relación.
- Exportación.

## M05 — Pólizas

- Crear.
- Editar.
- Eliminar.
- Duplicar.
- Numeración.
- Partidas.
- Relación con XML.

## M06 — Reglas y patrones

- Patrones por proveedor.
- Patrones por cliente.
- Patrones por concepto.
- Patrones por empresa.
- Sugerencias.

## M07 — IVA

- Tasas.
- Cuentas.
- Configuración.
- Validación.
- Conciliación.

## M08 — DIOT

- Configuración.
- Validación.
- Consolidado.
- TXT.
- Historial.

## M09 — Reportes

- XML.
- Pólizas.
- Auxiliares.
- Balanza.
- Saldos.
- IVA.
- DIOT.

## M10 — Auditoría

- Historial de operaciones.
- Usuario.
- Fecha.
- Empresa.
- Cambios.

---

# 27. MVP propuesto

El MVP debe concentrarse en demostrar que el sistema puede ejecutar correctamente el flujo contable principal.

## 27.1 Administración

- Usuarios.
- Roles básicos.
- Empresas.
- Asignación empresa ↔ usuario.
- Periodos.

## 27.2 XML

- Carga manual masiva.
- Parseo de CFDI.
- Clasificación emitido / recibido.
- Consulta.
- Filtros.
- Visualización de atributos.
- Detección básica de duplicados por UUID.

## 27.3 Contabilidad

- Catálogo de cuentas.
- Creación y edición de pólizas.
- Partidas.
- Validación cargo = abono.
- Relación XML ↔ póliza.
- Contabilización de ingresos.
- Contabilización de egresos.
- PUE.
- PPD.
- Complementos de pago.

## 27.4 Reportes

- Pólizas.
- XML.
- Balanza.
- Exportación Excel.

## 27.5 Plataforma

- Aplicación web.
- Base de datos centralizada.
- Infraestructura en nube.
- Respaldos.
- Auditoría básica.

---

# 28. Fuera del MVP inicial / fases posteriores

Funcionalidades candidatas para posteriores iteraciones:

- Descarga automática del SAT.
- DIOT completa.
- Envío directo de DIOT.
- Automatización de reglas.
- Patrones contables avanzados.
- Conciliación de IVA.
- Reportes totalmente configurables.
- Migración histórica completa.
- Cierre formal de periodos.
- Contabilidad electrónica.
- Integración bancaria.
- Conciliación bancaria.
- Portal para clientes.
- Aplicación móvil.
- Flujos de aprobación.
- Clasificación automática.
- Sugerencias inteligentes.
- Detección avanzada de errores.

---

# 29. Modelo de dominio inicial

Entidades candidatas:

```text
Organization
User
Role
Permission
Company
CompanyUser
FiscalRegime
AccountingPeriod

AccountCatalog
Account
AccountBalance

FiscalDocument
FiscalDocumentConcept
FiscalDocumentTax
FiscalDocumentRelation
PaymentComplement

Policy
PolicyEntry
PolicyDocument

AccountingRule
AccountingPattern

TaxRate
DIOTConfiguration
DIOTRecord

Import
Export
AuditLog
```

## Relaciones principales

```text
Organization
└── Companies
    ├── AccountingPeriods
    ├── Accounts
    ├── FiscalDocuments
    ├── Policies
    ├── AccountingRules
    └── AccountingPatterns
```

```text
Policy
├── PolicyEntries
└── FiscalDocuments (N:M)
```

```text
FiscalDocument
├── Concepts
├── Taxes
├── RelatedDocuments
├── PaymentComplements
└── Policies (N:M)
```

---

# 30. Reglas de negocio identificadas

## RN-001 — Balance de póliza

Una póliza contabilizada debe cumplir:

```text
SUM(cargos) = SUM(abonos)
```

## RN-002 — Contexto de trabajo

Toda operación contable debe pertenecer a:

```text
Empresa + Periodo
```

## RN-003 — Asignación de empresas

Un usuario contador solo podrá operar empresas a las que tenga acceso.

## RN-004 — Complementos

Un complemento de pago debe relacionarse con el CFDI correspondiente.

## RN-005 — Múltiples complementos

Una factura puede tener más de un complemento de pago.

## RN-006 — Relación documento-póliza

Una póliza puede relacionarse con múltiples documentos fiscales.

## RN-007 — Relación póliza-documento

Un documento fiscal puede participar en múltiples pólizas cuando el proceso contable lo requiera.

## RN-008 — Pagos parciales

Una factura puede generar movimientos contables en distintos periodos debido a pagos parciales.

## RN-009 — Patrones por empresa

Los patrones contables deben pertenecer al contexto de una empresa.

## RN-010 — Configuración fiscal

La configuración de IVA y DIOT puede cambiar por empresa y régimen fiscal.

---

# 31. Decisiones preliminares

Estas decisiones surgen del análisis inicial y deberán confirmarse durante la definición formal del producto.

| ID | Decisión preliminar |
|---|---|
| D-001 | El producto será una aplicación web multiempresa. |
| D-002 | El MVP priorizará la importación manual de XML antes que integración directa con SAT. |
| D-003 | La relación XML ↔ póliza deberá conservar trazabilidad explícita. |
| D-004 | PUE, PPD y complementos de pago pertenecen al núcleo contable. |
| D-005 | Las reglas automáticas deberán comenzar como sugerencias o advertencias. |
| D-006 | La automatización avanzada no debe desarrollarse antes de validar el modelo contable. |
| D-007 | El sistema debe soportar catálogos contables diferentes por empresa. |
| D-008 | La arquitectura debe considerar procesamiento masivo y asíncrono desde el inicio. |

---

# 32. Riesgos

## R-001 — Complejidad contable

La contabilización no depende únicamente del XML.

Puede depender de:

- Régimen.
- Empresa.
- Tipo de persona.
- Política interna.
- Periodo.
- Método de pago.
- Criterio profesional.

**Mitigación:** validar reglas con contadores antes de convertirlas en restricciones del sistema.

---

## R-002 — Exceso de flexibilidad

Replicar completamente la libertad del sistema actual podría conservar errores operativos.

**Mitigación:** advertencias primero; reglas configurables y bloqueos posteriormente.

---

## R-003 — Reglas demasiado rígidas

Implementar restricciones sin validar puede impedir escenarios contables legítimos.

**Mitigación:** diseñar reglas configurables y diferenciar advertencia de error bloqueante.

---

## R-004 — Migración

Cada empresa puede tener:

- Catálogo diferente.
- Cuentas personalizadas.
- Históricos inconsistentes.
- Saldos con diferencias.

**Mitigación:** definir estrategia de migración y realizar pilotos con empresas representativas.

---

## R-005 — Complementos de pago

Los pagos parciales y movimientos entre periodos representan una de las áreas más delicadas.

**Mitigación:** diseñar y validar estos escenarios antes de cerrar el modelo de dominio.

---

## R-006 — DIOT

Las reglas y archivos fiscales requieren validación especializada.

**Mitigación:** mantener DIOT fuera del primer flujo crítico hasta contar con reglas confirmadas, si el negocio lo permite.

---

# 33. Preguntas abiertas

## Alcance

- [ ] ¿El sistema reemplazará completamente Conta Fiscal?
- [ ] ¿Reemplazará también DD / Documentos Digitales?
- [ ] ¿Qué funcionalidades deben permanecer en sistemas existentes durante la transición?

## SAT / CFDI

- [ ] ¿La descarga directa del SAT pertenece al MVP?
- [ ] ¿Cómo se obtendrán los XML?
- [ ] ¿Se utilizará SAT directamente o un proveedor tercero?
- [ ] ¿Cómo se manejarán CFDI cancelados?
- [ ] ¿Cómo se manejarán sustituciones de CFDI?
- [ ] ¿Cómo se manejarán notas de crédito?
- [ ] ¿Cómo se manejarán retenciones?
- [ ] ¿Qué tratamiento tendrá la nómina?
- [ ] ¿Qué versiones de CFDI deben soportarse?

## Contabilidad

- [ ] ¿Una póliza descuadrada puede guardarse como borrador?
- [ ] ¿Cuándo una póliza se considera contabilizada?
- [ ] ¿Existe proceso de autorización?
- [ ] ¿Las pólizas pueden modificarse después de contabilizadas?
- [ ] ¿Cómo funcionan cierres y reaperturas de periodos?
- [ ] ¿Cómo se manejan monedas extranjeras?
- [ ] ¿Cómo se manejan tipos de cambio?

## Catálogo

- [ ] ¿Se utilizará obligatoriamente el catálogo SAT?
- [ ] ¿Cada empresa mantendrá un catálogo completamente personalizado?
- [ ] ¿Cómo se mapearán cuentas actuales contra nuevas cuentas?

## Migración

- [ ] ¿Se migrará histórico?
- [ ] ¿Cuántos ejercicios?
- [ ] ¿Solo catálogo y saldos iniciales?
- [ ] ¿Se migrarán pólizas?
- [ ] ¿Se migrarán XML?
- [ ] ¿Se migrarán relaciones XML ↔ póliza?

## IVA / DIOT

- [ ] ¿DIOT pertenece al MVP?
- [ ] ¿El sistema únicamente generará el TXT?
- [ ] ¿Se contempla envío directo posteriormente?
- [ ] ¿Qué validaciones deben realizarse antes de generar DIOT?

## Integraciones futuras

- [ ] ¿Se necesita conciliación bancaria?
- [ ] ¿Se necesita contabilidad electrónica?
- [ ] ¿Se requieren XML de catálogo y balanza SAT?
- [ ] ¿Se integrarán bancos?
- [ ] ¿Se integrarán sistemas de nómina?

---

# 34. Épicas iniciales

## EP-01 — Gestión de usuarios y empresas

> Como administrador quiero crear usuarios y asignarles empresas para controlar qué información puede consultar y modificar cada contador.

## EP-02 — Importación de documentos fiscales

> Como contador quiero importar XML de forma masiva para trabajar con los documentos fiscales de una empresa.

## EP-03 — Consulta de documentos

> Como contador quiero filtrar XML por periodo, tipo y estado para localizar documentos rápidamente.

## EP-04 — Catálogo de cuentas

> Como contador quiero administrar el catálogo de cuentas de una empresa para utilizarlo en las pólizas.

## EP-05 — Creación de pólizas

> Como contador quiero crear pólizas con cargos y abonos para registrar operaciones contables.

## EP-06 — Relación XML ↔ póliza

> Como contador quiero relacionar documentos fiscales con pólizas para conservar la trazabilidad contable.

## EP-07 — PUE, PPD y complementos

> Como contador quiero registrar facturas y pagos parciales para reflejar correctamente operaciones que ocurren en diferentes momentos o periodos.

## EP-08 — Patrones contables

> Como contador quiero que el sistema recuerde configuraciones utilizadas anteriormente para reducir trabajo repetitivo.

## EP-09 — Reportes

> Como contador quiero exportar XML, pólizas y balanzas para revisar y compartir información.

## EP-10 — IVA y DIOT

> Como contador quiero configurar el tratamiento fiscal de operaciones para preparar correctamente la información de IVA y DIOT.

---

# 35. Flujo prioritario para prototipo

El primer flujo funcional que debería poder probarse de extremo a extremo es:

```text
Login
  ↓
Seleccionar empresa
  ↓
Seleccionar periodo
  ↓
Importar XML
  ↓
Consultar documentos
  ↓
Seleccionar uno o varios XML
  ↓
Crear póliza
  ↓
Agregar / sugerir partidas
  ↓
Validar cargos y abonos
  ↓
Relacionar XML con póliza
  ↓
Guardar / contabilizar
  ↓
Consultar póliza
  ↓
Generar balanza básica
```

Este flujo permite validar el corazón del producto antes de implementar automatizaciones fiscales o inteligentes.

---

# 36. Orden sugerido de definición

Antes de desarrollar funcionalidad extensa conviene cerrar progresivamente:

## Paso 1 — Dominio

Definir formalmente:

- Empresa.
- Periodo.
- Cuenta.
- Documento fiscal.
- Relación entre CFDI.
- Complemento de pago.
- Póliza.
- Partida.
- Impuesto.

## Paso 2 — Casos contables

Documentar ejemplos reales de:

- Ingreso PUE.
- Egreso PUE.
- Ingreso PPD.
- Egreso PPD.
- Pago parcial.
- Varios complementos.
- Nota de crédito.
- Cancelación.
- Retención.
- Operación en moneda extranjera.

## Paso 3 — Reglas

Por cada caso definir:

- Datos de entrada.
- Cuentas involucradas.
- Partidas esperadas.
- Impuestos.
- Periodo.
- Relación con CFDI.
- Validaciones.
- Casos excepcionales.

## Paso 4 — UX

Diseñar:

- Selector empresa / periodo.
- Bandeja de XML.
- Vista de XML.
- Editor de póliza.
- Selector de cuentas.
- Relación documento ↔ póliza.
- Pantalla de revisión.

## Paso 5 — MVP técnico

Implementar el flujo principal end-to-end.

## Paso 6 — Automatización

Agregar patrones, sugerencias y reglas después de validar el comportamiento manual.

---

# 37. Criterio de éxito del MVP

El MVP debería demostrar que un contador puede completar el siguiente ciclo sin depender del sistema contable actual para ese flujo específico:

```text
Importar CFDI
→ identificar operación
→ crear póliza
→ asignar cuentas
→ relacionar documentos
→ validar balance
→ consultar movimientos
→ generar balanza
→ exportar información
```

El objetivo del MVP no debería ser automatizar toda la contabilidad.

El objetivo debería ser comprobar que el nuevo modelo:

1. Representa correctamente los casos contables reales.
2. Mantiene trazabilidad.
3. Es suficientemente rápido para trabajo cotidiano.
4. Permite crecer hacia reglas y automatización.

---

# 38. Próximos documentos recomendados

Este análisis debería utilizarse como entrada para documentos separados.

```text
knowledge/
├── [00 - Inicio.md](00%20-%20Inicio.md)
├── [01 - Glosario de dominio](002%20-%20Glosario.md)
├── [02 - Preguntas abiertas](006%20-%20Preguntas%20Abiertas.md)
├── [03 - Reglas de negocio](005%20-%20Reglas%20de%20negocio.md)
├── [04 - Escenarios contables](004%20-%20Escenarios%20contables.md)
├── [05 - Alcance del MVP](003%20-%20MVP-Scope.md)
└── 06 - Modelo de dominio (pendiente de crear)
```

Posteriormente:

```text
specs/
├── authentication/
├── companies/
├── fiscal-documents/
├── accounts/
├── policies/
├── payments/
└── reporting/
```

---

# 39. Estado del conocimiento
 
Este documento representa un **primer levantamiento**, no una especificación final.

Las siguientes categorías deben mantenerse separadas durante el proyecto:

### Confirmado

Información expresamente indicada durante el levantamiento.

### Propuesta

Diseño o comportamiento sugerido para resolver una necesidad.

### Pendiente de validar

Aspectos que requieren confirmación de contadores o responsables del negocio.

### Futuro

Funcionalidades que no deberían condicionar el MVP salvo que se confirme lo contrario.

Esta separación será importante para evitar que hipótesis iniciales terminen implementándose accidentalmente como reglas contables.
