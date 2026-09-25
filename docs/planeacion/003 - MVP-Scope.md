# Sistema Contable — Alcance del MVP

> **Documento de referencia:** `05-mvp-scope.md`  
> **Nota en este vault:** [003 - MVP-Scope](003%20-%20MVP-Scope.md)
> **Estado:** Borrador inicial  
> **Enfoque:** Negocio y operación contable  
> **Última actualización:** 2026-08-31

**Navegación:** [Inicio](00%20-%20Inicio.md) · [Análisis](001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md) · [Preguntas abiertas](006%20-%20Preguntas%20Abiertas.md) · [Escenarios](004%20-%20Escenarios%20contables.md) · [Reglas](005%20-%20Reglas%20de%20negocio.md)

---

# 1. Objetivo del MVP

El objetivo del MVP es validar que el nuevo sistema puede sustituir el flujo contable principal que hoy se realiza entre varias herramientas.

El MVP debe permitir que un contador pueda:

```text
Seleccionar empresa
    ↓
Seleccionar periodo
    ↓
Importar XML
    ↓
Consultar documentos
    ↓
Seleccionar documentos
    ↓
Crear póliza
    ↓
Asignar cuentas
    ↓
Registrar partidas
    ↓
Relacionar XML con póliza
    ↓
Validar cargos y abonos
    ↓
Consultar balanza básica
```

El MVP no busca automatizar toda la contabilidad.

Busca comprobar que el sistema representa correctamente el trabajo real del contador y puede ejecutar el flujo contable principal de una empresa.

---

# 2. Problema de negocio que debe resolver

Actualmente el trabajo contable está dividido entre diferentes herramientas.

El contador necesita realizar pasos separados para:

- obtener XML;
- consultar documentos;
- seleccionar facturas;
- crear pólizas;
- asignar cuentas;
- relacionar documentos;
- revisar movimientos;
- generar reportes.

El MVP debe concentrar estas actividades dentro de una sola plataforma.

---

# 3. Usuarios incluidos

## Administrador

Debe poder:

- registrar empresas;
- registrar contadores;
- restablecer contraseñas temporales de contadores;
- asignar y retirar empresas a contadores;
- consultar las empresas existentes.

El primer administrador se crea y recupera desde consola. No se crean otros administradores desde la interfaz. El administrador tiene acceso operativo a todas las empresas; los contadores únicamente a sus asignaciones.

## Contador

Debe poder:

- acceder únicamente a las empresas asignadas;
- seleccionar una empresa;
- seleccionar un periodo;
- importar y consultar XML;
- crear y modificar pólizas;
- asignar cuentas;
- consultar movimientos;
- generar reportes básicos.

---

# 4. Empresas

El MVP debe permitir administrar múltiples empresas.

Cada empresa deberá manejar de forma independiente:

- datos fiscales básicos;
- periodos;
- catálogo de cuentas;
- XML;
- pólizas;
- movimientos contables.

Sus datos fiscales básicos incluyen RFC obligatorio y único, razón social obligatoria y un único régimen fiscal elegido del catálogo oficial versionado. La validación estructural del RFC no sustituye una consulta de situación ante SAT.

El usuario debe trabajar siempre dentro del contexto:

```text
Empresa + Periodo
```

---

# 5. Periodos contables

El contador debe poder seleccionar:

- ejercicio;
- mes.

Ejemplo:

```text
Empresa: Empresa X
Ejercicio: 2026
Periodo: Julio
```

Para el MVP será suficiente distinguir inicialmente entre:

```text
ABIERTO
CERRADO
```

El comportamiento exacto del cierre queda pendiente de validación.

---

# 6. Importación y obtención de XML

El MVP debe permitir cargar XML de forma manual y masiva.

El sistema debe poder:

- recibir múltiples XML;
- identificar documentos duplicados;
- clasificar documentos;
- extraer información relevante;
- mostrar los documentos importados.

## Simulación de descarga automática

Aunque en esta fase no será necesario implementar una integración real con SAT, el MVP deberá **simular el flujo de descarga automática de XML mediante un servicio externo ficticio o controlado**.

El objetivo es que el cliente pueda visualizar y validar una de las partes más importantes de su proceso futuro:

```text
Seleccionar empresa
    ↓
Solicitar descarga de XML
    ↓
Sistema consulta servicio externo simulado
    ↓
Se muestran documentos encontrados
    ↓
Documentos se incorporan al repositorio
    ↓
Contador continúa con el proceso contable
```

Para efectos del MVP, el comportamiento podrá utilizar información previamente preparada o documentos de prueba.

Lo que se desea validar es:

- que el usuario entienda cómo iniciará la descarga;
- que pueda visualizar el progreso o resultado del proceso;
- que los documentos obtenidos aparezcan en la bandeja correspondiente;
- que posteriormente pueda contabilizarlos normalmente;
- que el flujo represente correctamente la experiencia esperada por el cliente.

### Alcance de esta simulación

El MVP **sí incluye**:

- acción para iniciar una descarga;
- representación de un servicio externo;
- resultado de documentos encontrados;
- incorporación de XML al sistema;
- estados básicos del proceso;
- continuidad hacia el flujo contable.

El MVP **no incluye todavía**:

- conexión real con SAT;
- autenticación real ante SAT;
- manejo de certificados o credenciales fiscales;
- sincronización automática programada;
- tratamiento completo de errores externos;
- validación contra servicios oficiales.

Por lo tanto, durante el MVP se validará el **flujo de negocio de descarga automática**, mientras que la integración real quedará para una fase posterior.

---

# 7. Consulta de documentos fiscales

El contador debe poder consultar los documentos de una empresa y periodo.

Debe poder distinguir, como mínimo:

- emitidos;
- recibidos.

Debe poder consultar información como:

- UUID;
- RFC emisor;
- RFC receptor;
- fecha;
- serie;
- folio;
- subtotal;
- impuestos;
- total;
- método de pago;
- forma de pago;
- moneda;
- tipo de comprobante.

Debe existir una forma clara de saber si un documento:

- está pendiente;
- ya fue relacionado con una póliza;
- presenta algún problema.

La nomenclatura definitiva de estados queda pendiente.

---

# 8. Catálogo de cuentas

Cada empresa debe tener su propio catálogo de cuentas.

El MVP debe permitir:

- consultar cuentas;
- crear cuentas;
- editar cuentas;
- activar o desactivar cuentas;
- importar un catálogo inicial.

No se requiere todavía automatizar la relación con el catálogo SAT.

---

# 9. Pólizas contables

El contador debe poder crear `AccountingPolicy`.

Tipos mínimos:

- ingreso;
- egreso;
- diario.

Otros tipos pueden existir posteriormente.

Una póliza debe contener:

- fecha;
- tipo;
- número;
- concepto;
- partidas;
- documentos relacionados;
- estado.

---

# 10. Partidas contables

Cada póliza debe permitir registrar partidas con:

- cuenta;
- cargo;
- abono;
- concepto;
- referencia.

Regla mínima:

```text
Total cargos = Total abonos
```

Para el MVP se propone permitir guardar una póliza descuadrada como borrador, pero no considerarla contabilizada.

Este comportamiento queda pendiente de validación con negocio.

---

# 11. Relación XML ↔ póliza

El MVP debe conservar trazabilidad entre documentos fiscales y pólizas.

Debe soportar:

```text
Una póliza
→ varios XML
```

y también:

```text
Un XML
→ varias pólizas
```

cuando el proceso contable lo requiera.

La relación entre póliza y XML debe ser opcional, ya que pueden existir pólizas sin documento fiscal asociado.

---

# 12. Ingresos

El MVP debe permitir contabilizar operaciones básicas de ingreso.

Flujo esperado:

```text
Seleccionar XML emitido
    ↓
Crear póliza
    ↓
Asignar cuentas
    ↓
Registrar partidas
    ↓
Relacionar documento
    ↓
Guardar / contabilizar
```

Cuentas comunes que pueden intervenir:

- clientes;
- bancos;
- ventas;
- IVA.

Las reglas exactas de contabilización quedan pendientes de confirmación.

---

# 13. Egresos

El MVP debe permitir contabilizar operaciones básicas de egreso.

Flujo esperado:

```text
Seleccionar XML recibido
    ↓
Crear póliza
    ↓
Asignar cuentas
    ↓
Registrar partidas
    ↓
Relacionar documento
    ↓
Guardar / contabilizar
```

Cuentas comunes:

- proveedores;
- acreedores;
- bancos;
- gastos;
- compras;
- IVA.

Las reglas exactas quedan pendientes de confirmación.

---

# 14. PUE

El MVP debe distinguir documentos PUE.

En esta fase el sistema debe permitir que el contador registre manualmente las cuentas y partidas correspondientes.

La ampliación autorizada en SPEC-006 permite prellenar partidas desde importes fiscales estructurados; el contador elige o revisa las cuentas, corrige el asiento y decide cuándo guardarlo o contabilizarlo.

---

# 15. PPD y complementos de pago

El MVP debe soportar el escenario básico de PPD.

Debe ser posible representar:

- factura pendiente;
- uno o varios complementos;
- pagos parciales;
- pagos en diferentes periodos;
- varias pólizas relacionadas con una misma factura.

Ejemplo:

```text
Factura $100,000
├── Pago julio  $50,000
└── Pago agosto $50,000
```

Este escenario es importante para validar el modelo de negocio.

Las reglas exactas de IVA y movimientos contables quedan pendientes de confirmación.

---

# 16. Reportes incluidos

El MVP debe generar reportes básicos.

Como mínimo:

## XML

Listado de documentos con información principal.

## Pólizas

Listado de pólizas y sus partidas.

## Balanza básica

Debe permitir consultar:

- cuenta;
- saldo inicial;
- cargos;
- abonos;
- saldo final.

## Exportación

Debe existir al menos exportación a Excel de los reportes principales.

---

# 17. Auditoría mínima

El MVP debe conservar información básica sobre:

- quién creó una póliza;
- quién modificó una póliza;
- fecha de creación;
- fecha de modificación;
- empresa;
- periodo.

No es necesario todavía un sistema completo de auditoría histórica de todos los campos.

---

# 18. Flujo completo que debe demostrar el MVP

El MVP se considerará funcional cuando un contador pueda realizar este proceso:

```text
1. Iniciar sesión
2. Seleccionar empresa
3. Seleccionar periodo
4. Importar XML
5. Localizar una factura
6. Crear una AccountingPolicy
7. Registrar partidas
8. Seleccionar cuentas
9. Relacionar la factura
10. Validar cargos y abonos
11. Contabilizar la póliza
12. Consultarla posteriormente
13. Ver su impacto en una balanza básica
14. Exportar información
```

---

# 19. Escenarios mínimos a probar

El MVP debe probarse, como mínimo, con estos escenarios:

## Escenario 1 — Ingreso PUE

Una factura emitida que se contabiliza dentro del periodo.

## Escenario 2 — Egreso PUE

Una factura recibida que se contabiliza dentro del periodo.

## Escenario 3 — Factura PPD

Una factura registrada inicialmente pendiente de pago o cobro.

## Escenario 4 — Pago parcial

Una factura PPD con un primer pago parcial.

## Escenario 5 — Múltiples pagos

Una factura con pagos en dos periodos diferentes.

## Escenario 6 — Póliza sin XML

Una póliza de ajuste o movimiento interno sin documento fiscal asociado.

## Escenario 7 — Varios XML en una póliza

Una póliza relacionada con múltiples documentos.

---

# 20. Criterios de éxito del MVP

El MVP será considerado exitoso si permite validar que:

1. El contador entiende el flujo sin depender de varias aplicaciones.
2. Los XML pueden utilizarse como punto de partida para contabilizar.
3. La relación entre XML, pólizas, partidas y cuentas es clara.
4. Los escenarios PUE y PPD pueden representarse correctamente.
5. Los pagos parciales pueden mantenerse entre diferentes periodos.
6. Las pólizas afectan correctamente la balanza.
7. El contador puede corregir manualmente las cuentas y partidas.
8. El modelo no impide operaciones contables legítimas.
9. El sistema permite identificar qué documentos ya fueron contabilizados.
10. El contador puede consultar posteriormente cómo se contabilizó un documento.

---

# 21. Fuera del MVP

Las siguientes funcionalidades quedan fuera de esta primera versión.

## Automatización

- contabilización automática;
- sugerencia automática de cuentas;
- aprendizaje de patrones;
- reglas automáticas avanzadas;
- inteligencia artificial;
- clasificación automática por conceptos.

Excepción posterior autorizada: SPEC-006 prellena importes y recuerda cuentas elegidas por el contador para un emisor y componente equivalentes. No contabiliza al pulsar «Continuar» ni decide el tratamiento fiscal de la cuenta.

## SAT

Queda fuera del MVP la integración real con SAT.

No se implementará todavía:

- conexión real para descarga automática de XML;
- autenticación real ante SAT;
- sincronización periódica;
- consulta automática de cancelaciones;
- envío directo de información al SAT.

El **flujo de descarga automática sí será representado mediante una simulación** para que pueda validarse con el cliente.

## DIOT

- generación completa de DIOT;
- archivo TXT definitivo;
- validaciones fiscales avanzadas;
- envío al SAT.

## IVA avanzado

- conciliación automática de IVA;
- reglas automáticas de IVA pendiente;
- IVA efectivamente pagado;
- IVA efectivamente cobrado;
- validaciones fiscales avanzadas.

El modelo debe poder evolucionar hacia estos conceptos, pero no es necesario automatizarlos en el MVP.

## CFDI especiales

- cancelaciones;
- sustituciones;
- notas de crédito;
- retenciones complejas;
- nómina;
- casos fiscales especiales.

Estos casos se documentarán y validarán posteriormente.

## Contabilidad avanzada

- cierre contable completo;
- reapertura formal;
- pólizas automáticas de cierre;
- depreciaciones;
- amortizaciones;
- diferencias cambiarias;
- activos fijos.

## Bancos

- integración bancaria;
- importación de estados de cuenta;
- conciliación bancaria automática.

## Contabilidad electrónica

- generación de archivos de contabilidad electrónica;
- catálogo SAT definitivo;
- balanza electrónica;
- envío de archivos fiscales.

## Reportería avanzada

- reportes personalizados;
- diseñador de reportes;
- dashboards;
- indicadores;
- comparación entre empresas;
- reportes fiscales avanzados.

## Clientes

- portal para clientes;
- acceso de solo lectura;
- aprobación de movimientos;
- carga de documentos por clientes.

---

# 22. Fase posterior 1 — Consolidación contable

Después de validar el MVP, la siguiente fase puede concentrarse en mejorar el trabajo cotidiano.

Posibles funcionalidades:

- patrones contables;
- sugerencias de cuentas;
- reglas por proveedor;
- reglas por cliente;
- catálogo SAT;
- saldos iniciales;
- cierre de periodos;
- mejoras de reportes;
- mejores validaciones.

---

# 23. Fase posterior 2 — Fiscal

Una segunda evolución puede incorporar:

- DIOT;
- IVA avanzado;
- retenciones;
- cancelaciones;
- sustituciones;
- notas de crédito;
- contabilidad electrónica;
- validaciones fiscales.

---

# 24. Fase posterior 3 — Automatización

Una vez validado el comportamiento contable:

- clasificación automática;
- contabilización asistida;
- sugerencias por patrones;
- detección de inconsistencias;
- automatización de operaciones repetitivas;
- descarga automática de CFDI.

---

# 25. Fase posterior 4 — Integraciones

Posteriormente pueden evaluarse:

- bancos;
- conciliación bancaria;
- SAT;
- sistemas externos;
- portal para clientes;
- otros sistemas administrativos.

---

# 26. Principio de alcance

Para decidir si una funcionalidad entra en el MVP se utilizará esta pregunta:

> **¿Es necesaria para demostrar que un contador puede transformar documentos fiscales en registros contables y obtener una balanza trazable?**

Si la respuesta es no, probablemente debe quedar para una fase posterior.

---

# 27. Resumen del MVP

El MVP se concentra en cinco capacidades:

```text
1. Empresas y periodos

2. XML fiscales

3. Catálogo de cuentas

4. AccountingPolicy + partidas

5. Balanza y reportes básicos
```

El corazón funcional será:

```text
XML
    ↓
AccountingPolicy
    ↓
AccountingPolicyEntry
    ↓
Account
    ↓
TrialBalance
```

Todo lo relacionado con automatización, fiscalización avanzada e integraciones externas deberá agregarse después de validar correctamente este flujo.
