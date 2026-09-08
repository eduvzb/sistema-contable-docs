# Sistema Contable — Guía Explicada de Escenarios Contables

> **Documento de referencia:** `04-accounting-scenarios-explained.md`  
> **Estado:** Documento de apoyo  
> **Audiencia:** Producto, desarrollo y personas sin formación contable  
> **Documento de referencia en este vault:** [004 - Escenarios contables](../004%20-%20Escenarios%20contables.md)  
> **Propósito:** Explicar en lenguaje sencillo qué significa cada escenario contable del documento oficial  
> **Última actualización:** 2026-08-31

**Navegación:** [Inicio](../00%20-%20Inicio.md) · [Escenarios oficiales](../004%20-%20Escenarios%20contables.md)

---

# 1. Cómo usar este documento

Este archivo es una traducción práctica del documento:

[004 - Escenarios contables](../004%20-%20Escenarios%20contables.md)

El documento oficial describe lo que el sistema debe representar.

Este documento explica:

- por qué existe cada escenario;
- qué está pasando en términos cotidianos;
- qué debe entender un desarrollador;
- qué no debemos asumir todavía.

Este documento **no es la fuente oficial de reglas contables**.

Cuando exista una diferencia entre ambos documentos, prevalece:

[004 - Escenarios contables](../004%20-%20Escenarios%20contables.md)

---

# 2. Idea principal del sistema

Antes de entrar a cada escenario, hay que entender cuatro piezas.

## FiscalDocument

Es el CFDI que recibimos en XML.

Piensa en él como:

> “La evidencia fiscal de que ocurrió una operación.”

Ejemplo:

Una empresa compra una computadora y recibe una factura.

Ese XML se convierte dentro del sistema en un:

```text
FiscalDocument
```

---

## AccountingPolicy

Es la póliza contable.

Piensa en ella como:

> “La forma en que el contador explica contablemente qué ocurrió.”

La factura dice cuánto se compró, quién vendió, qué impuestos existen, etc.

La póliza dice:

> “Este importe afecta estas cuentas contables de esta manera.”

---

## AccountingPolicyEntry

Son las líneas que forman la póliza.

Por ejemplo:

```text
Cuenta A   Cargo   $10,000
Cuenta B   Cargo    $1,600
Cuenta C   Abono   $11,600
```

Esas líneas son las que finalmente mueven la contabilidad.

---

## Account

Es una cuenta contable.

Ejemplos:

```text
Bancos
Clientes
Proveedores
Ventas
Gastos
IVA
```

Puedes imaginar el catálogo de cuentas como un conjunto de “cajones” donde se clasifican los movimientos financieros.

---

# 3. AC-001 — Ingreso PUE

## En palabras sencillas

La empresa vende algo y emite una factura que se considera pagada en una sola exhibición.

Ejemplo:

```text
La empresa vende un servicio por $11,600.
```

Tenemos:

```text
$10,000 servicio
$1,600 IVA
```

El XML nos dice que la operación ocurrió.

Pero el XML por sí solo no nos dice exactamente cómo quiere registrarla contablemente esa empresa.

Por eso el contador crea una:

```text
AccountingPolicy
```

y decide qué cuentas deben moverse.

## Lo que debe entender el sistema

```text
Factura
→ póliza
→ partidas
→ cuentas
→ balanza
```

## Lo que todavía no sabemos

No debemos programar todavía algo como:

> “Toda factura PUE siempre genera exactamente estas tres cuentas.”

Eso tiene que confirmarlo negocio.

---

# 4. AC-002 — Egreso PUE

## En palabras sencillas

Es el caso inverso.

La empresa compra algo o tiene un gasto y recibe una factura.

Ejemplo:

```text
Compra material de oficina por $11,600.
```

La factura puede contener:

```text
$10,000 gasto
$1,600 IVA
```

El contador decide cómo se registra.

Puede involucrar conceptos como:

```text
Gasto
IVA
Banco
Proveedor
```

## Qué nos importa como desarrolladores

No necesitamos conocer todavía el asiento perfecto.

Necesitamos que el sistema permita al contador construirlo.

Ese es un principio muy importante del MVP:

> Primero permitir contabilizar correctamente de forma manual; después automatizar.

---

# 5. AC-003 — Factura PPD

## ¿Qué cambia respecto a PUE?

En PUE estamos hablando de una operación que se plantea como pagada en una sola exhibición.

En PPD el dinero puede llegar después o en partes.

Ejemplo:

```text
Hoy recibes una factura por $100,000.
Pero todavía no la pagas.
```

Contablemente ya existe algo:

```text
debes $100,000
```

aunque:

```text
tu banco todavía no perdió $100,000
```

Esa diferencia es importante.

Por eso aparecen conceptos como:

```text
Cuenta por pagar
Cuenta por cobrar
Provisión
```

## La idea que debe soportar el software

La factura puede existir primero.

El pago puede aparecer después.

Por tanto:

```text
Factura ≠ Pago
```

Y eso significa que una factura puede terminar relacionada con varios movimientos contables.

---

# 6. AC-004 — Pago parcial

## Ejemplo

Debes:

```text
$100,000
```

pero solamente pagas:

```text
$40,000
```

Entonces todavía quedan:

```text
$60,000
```

El sistema debe entender que la factura:

- existe;
- no está totalmente liquidada;
- ya recibió un pago;
- todavía tiene saldo pendiente.

## Mentalmente podemos verlo así

```text
Factura $100,000
├── Pagado $40,000
└── Pendiente $60,000
```

El complemento de pago sirve para relacionar fiscalmente ese pago con la factura correspondiente.

---

# 7. AC-005 — Pagos en diferentes meses

Este es uno de los escenarios más importantes.

Ejemplo:

```text
Factura: $100,000

Julio:
pagan $50,000

Agosto:
pagan $50,000
```

No podemos modelar la factura como:

```text
Factura → una sola póliza
```

porque hay movimientos en momentos diferentes.

Necesitamos algo como:

```text
Factura
├── Póliza de julio
└── Póliza de agosto
```

Por eso hablamos de una relación:

```text
muchos a muchos
```

entre documentos y pólizas.

No necesitas pensar en base de datos todavía.

Desde negocio significa simplemente:

> “Una factura puede participar en más de un movimiento contable.”

---

# 8. AC-006 — Varios XML en una póliza

También puede ocurrir lo contrario.

El contador puede decidir contabilizar varias facturas juntas.

Ejemplo:

```text
Factura A
Factura B
Factura C
      ↓
una misma póliza
```

Así que no podemos asumir:

```text
1 factura = 1 póliza
```

Esa sería una restricción falsa.

La relación real necesita ser flexible.

---

# 9. AC-007 — Un XML en varias pólizas

Es parecido al escenario de pagos parciales.

Una factura puede generar:

```text
registro inicial
pago 1
pago 2
```

y cada uno puede representar un movimiento diferente.

Por eso cuando alguien abra una factura necesitamos poder responder:

> “¿Qué movimientos contables se hicieron con este documento?”

---

# 10. AC-008 — Póliza sin XML

Este escenario es fácil de pasar por alto.

No toda la contabilidad nace de una factura.

Puede haber:

- ajustes;
- reclasificaciones;
- cierres;
- correcciones internas.

Por ejemplo, el contador podría necesitar mover un importe de una cuenta a otra.

En ese caso existe:

```text
AccountingPolicy
```

pero no necesariamente:

```text
FiscalDocument
```

## Consecuencia importante

Nunca debemos diseñar el sistema suponiendo:

```text
Toda póliza requiere XML.
```

Eso sería incorrecto para el dominio que estamos intentando representar.

---

# 11. AC-009 — Provisión

“Provisión” puede sonar complicado, pero la idea básica que necesitamos entender ahora es sencilla.

Significa registrar que existe una obligación o derecho aunque el dinero todavía no se haya movido.

Ejemplo:

```text
Recibes una factura hoy.
La pagarás dentro de 30 días.
```

Hoy ya sabes:

```text
le debes dinero a alguien
```

pero tu banco todavía no cambió.

Podemos pensar el flujo como:

```text
Factura
↓
Reconocer deuda
↓
Más adelante pagar
```

La forma contable exacta sigue pendiente de confirmación.

---

# 12. AC-010 — IVA pendiente

Aquí tampoco necesitamos convertirnos en contadores para entender el problema del software.

La idea es:

> El momento en que aparece una factura no siempre coincide con el momento en que se paga o cobra.

Y el tratamiento del IVA puede depender de esos momentos.

Entonces el sistema probablemente necesitará distinguir algo parecido a:

```text
IVA asociado a la factura
```

de:

```text
IVA asociado al pago/cobro efectivo
```

Lo importante para nosotros es conservar toda la historia:

```text
Factura
↓
Pago
↓
Complemento
↓
Póliza
↓
IVA
```

La regla fiscal exacta la validará posteriormente el contador.

---

# 13. AC-011 — Póliza descuadrada

En contabilidad debe cumplirse:

```text
Cargos = Abonos
```

Si tienes:

```text
Cargos: $10,000
Abonos:  $8,000
```

faltan:

```text
$2,000
```

La póliza está descuadrada.

Pero mientras el contador la está preparando puede ser útil guardar el avance.

Por eso proponemos:

```text
DRAFT
```

puede estar incompleto.

Mientras:

```text
POSTED
```

debe estar balanceado.

Es un supuesto del MVP y todavía debe validarse.

---

# 14. AC-012 — Trazabilidad desde una factura

Esta funcionalidad es central.

Imagina que dentro de seis meses alguien encuentra este UUID:

```text
ABC-123...
```

El sistema debería poder responder:

> “¿Qué hicimos contablemente con esta factura?”

Deberíamos poder navegar:

```text
Factura
→ pólizas
→ partidas
→ cuentas
→ periodos
```

Eso es trazabilidad.

---

# 15. AC-013 — Trazabilidad desde una póliza

También necesitamos poder hacer la pregunta al revés:

> “¿Por qué existe esta póliza?”

Entonces desde una póliza debemos llegar a:

```text
facturas
complementos
UUID
importes
```

cuando esos documentos existan.

Esto ayuda mucho en revisión y auditoría.

---

# 16. AC-014 — Balanza

Puedes pensar en la balanza como un resumen de cómo quedaron las cuentas después de registrar movimientos.

Ejemplo muy simplificado:

```text
Cuenta       Inicial   Cargos   Abonos   Final

Bancos       100,000   20,000   10,000   ...
Clientes      50,000   15,000    5,000   ...
```

No necesitamos dominar ahora las reglas de naturaleza de cuentas.

Para el MVP nos importa demostrar que:

```text
Pólizas
↓
Partidas
↓
afectan cuentas
↓
se reflejan en balanza
```

Si eso funciona, estamos validando una parte muy importante del corazón contable.

---

# 17. AC-015 — XML duplicado

Los CFDI tienen un UUID.

Si importamos el mismo XML dos veces, no queremos terminar creyendo que son dos operaciones distintas.

Entonces:

```text
mismo UUID
→ detectar duplicado
```

La lógica avanzada para sustituciones y casos especiales se puede añadir después.

---

# 18. AC-016 — Descarga simulada

Este escenario existe porque para el cliente la descarga automática es muy importante.

Pero todavía no queremos resolver la integración real con SAT.

Entonces hacemos una simulación.

El usuario verá algo parecido a:

```text
Descargar XML
↓
Buscando documentos...
↓
23 documentos encontrados
↓
Importar
```

Por detrás los archivos pueden venir de datos preparados para el MVP.

## ¿Estamos engañando al cliente?

No, siempre que dejemos claro que es una simulación.

Lo que estamos validando es:

> “¿Así quieren que funcione el proceso?”

No estamos afirmando:

> “Ya tenemos resuelta la integración con SAT.”

Esta diferencia es importante.

---

# 19. ¿Por qué dejamos algunos escenarios para después?

Porque queremos validar primero el núcleo.

Hay situaciones como:

- cancelaciones;
- notas de crédito;
- retenciones;
- moneda extranjera;
- cierre contable;
- conciliación bancaria;
- contabilidad electrónica.

Todas son importantes.

Pero intentar resolverlas antes de comprobar el flujo principal haría el MVP demasiado grande.

La estrategia es:

```text
primero representar bien
↓
después completar
↓
después automatizar
```

---

# 20. El modelo mental que debes conservar

Cuando leas documentación del proyecto, piensa siempre en estas capas:

```text
¿Qué documento fiscal existe?
        ↓
¿Qué pasó en el negocio?
        ↓
¿Cómo decidió representarlo el contador?
        ↓
¿Qué póliza creó?
        ↓
¿Qué partidas creó?
        ↓
¿Qué cuentas cambiaron?
        ↓
¿Cómo aparece en la balanza?
```

Ese flujo explica gran parte del sistema.

---

# 21. Cinco reglas mentales útiles

## Regla 1

```text
Factura ≠ póliza
```

La factura es evidencia fiscal.

La póliza es representación contable.

---

## Regla 2

```text
Factura ≠ pago
```

Especialmente en PPD.

---

## Regla 3

```text
1 XML ≠ necesariamente 1 póliza
```

Puede haber varias.

---

## Regla 4

```text
1 póliza ≠ necesariamente 1 XML
```

Puede contener varios o incluso ninguno.

---

## Regla 5

```text
XML → póliza → partidas → cuentas → balanza
```

es la columna vertebral del MVP.

---

# 22. Qué debes poder explicar después de leer este documento

Sin necesidad de conocer contabilidad avanzada, deberías poder explicar:

1. por qué un CFDI y una póliza son cosas diferentes;
2. por qué PPD hace que una factura pueda tener varios movimientos;
3. por qué necesitamos complementos de pago;
4. por qué la relación XML-póliza es flexible;
5. por qué algunas pólizas no requieren XML;
6. qué significa que una póliza esté balanceada;
7. qué significa trazabilidad;
8. cómo los movimientos terminan afectando una balanza;
9. qué partes del flujo todavía necesitan validación de un contador;
10. qué estamos validando con la descarga simulada.

---

# 23. Pregunta que responde este documento

Mientras el documento oficial pregunta:

> **¿Puede el sistema representar correctamente los escenarios contables?**

este documento busca que tú puedas responder:

> **¿Entiendo qué está ocurriendo en cada escenario, por qué el sistema necesita representarlo y qué parte todavía depende del criterio de un contador?**
