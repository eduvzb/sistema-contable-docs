
# Sistema Contable — Glosario de Contabilidad para Desarrollo  
  
> **Documento de referencia:** `01b-accounting-glossary-explained.md`    
> **Nota en este vault:** [Guía de conceptos](Gu%C3%ADa%20de%20conceptos.md)
> **Estado:** Documento de apoyo    
> **Audiencia:** Desarrollo, producto y personas sin formación contable    
> **Propósito:** Explicar el lenguaje contable necesario para entender el negocio del proyecto    
> **Última actualización:** 2026-08-31

**Navegación:** [Inicio](../00%20-%20Inicio.md) · [Glosario de dominio](../002%20-%20Glosario.md)

---
  
# 1. Propósito  
  
Este documento explica conceptos contables en lenguaje sencillo.  
  
No pretende sustituir formación contable ni establecer reglas fiscales oficiales.  
  
Su objetivo es que una persona de desarrollo pueda entender:  
  
- qué está intentando registrar un contador;  
- por qué existen cuentas, cargos y abonos;  
- qué representa una póliza;  
- cómo una factura termina afectando una balanza;  
- por qué una factura y un pago no siempre ocurren al mismo tiempo;  
- qué significan cuentas por cobrar, cuentas por pagar, IVA, provisiones y otros conceptos utilizados dentro del proyecto.  
  
La pregunta principal que intenta responder este documento es:  
  
> **¿Qué está representando realmente el contador cuando utiliza el sistema?**  
  
---  
  
# 2. La idea más importante: la contabilidad cuenta una historia  
  
La contabilidad intenta representar económicamente lo que ocurre dentro de una empresa.  
  
Por ejemplo:  
  
```text  
La empresa vende un servicio.  
```  
  
Eso puede producir varias consecuencias:  
  
```text  
La empresa ganó un ingreso.  
El cliente debe dinero.  
La empresa generó IVA.  
Posteriormente el cliente paga.  
El dinero entra al banco.  
```  
  
Aunque para una persona esto puede sentirse como una sola operación, contablemente son diferentes efectos.  
  
El sistema contable existe para registrar esos efectos de forma ordenada.  
  
---  
  
# 3. Cuenta contable  
  
Una **cuenta contable** es una categoría donde se registran movimientos del mismo tipo.  
  
Puedes imaginarla como un cajón.  
  
Ejemplos:  
  
```text  
Bancos  
Clientes  
Proveedores  
Ventas  
Gastos de oficina  
IVA acreditable  
IVA trasladado  
```  
  
Si entra o sale dinero de una cuenta bancaria, el movimiento se registra en una cuenta llamada algo parecido a:  
  
```text  
Bancos  
```  
  
Si un cliente nos debe dinero:  
  
```text  
Clientes  
```  
  
Si nosotros debemos dinero a un proveedor:  
  
```text  
Proveedores  
```  
  
## Ejemplo mental  
  
Piensa en varios contenedores:  
  
```text  
[Bancos]  
[Clientes]  
[Proveedores]  
[Ventas]  
[Gastos]  
[IVA]  
```  
  
Cada operación mueve cantidades entre esos contenedores.  
  
---  
  
# 4. Catálogo de cuentas  
  
El **catálogo de cuentas** es la lista organizada de todas las cuentas que utiliza una empresa.  
  
Ejemplo simplificado:  
  
```text  
1000 Activos  
├── 1100 Bancos  
├── 1200 Clientes  
└── 1300 Inventarios  
  
2000 Pasivos  
└── 2100 Proveedores  
  
4000 Ingresos  
└── 4100 Ventas  
  
5000 Gastos  
├── 5100 Papelería  
└── 5200 Servicios  
```  
  
Cada empresa puede organizar su catálogo de manera diferente.  
  
Por eso el sistema contable no debe asumir que todas las empresas utilizan exactamente las mismas cuentas.  
  
---  
  
# 5. Cuenta padre y cuenta auxiliar  
  
Las cuentas pueden organizarse jerárquicamente.  
  
Ejemplo:  
  
```text  
Bancos  
├── BBVA  
├── Santander  
└── Banorte  
```  
  
`Bancos` puede funcionar como agrupador.  
  
Mientras:  
  
```text  
BBVA  
```  
  
puede ser una cuenta más específica.  
  
Algo similar puede ocurrir con clientes:  
  
```text  
Clientes  
├── Cliente A  
├── Cliente B  
└── Cliente C  
```  
  
A estos niveles específicos normalmente se les puede llamar auxiliares o subcuentas, dependiendo del sistema y catálogo.  
  
---  
  
# 6. Movimiento contable  
  
Un **movimiento contable** representa un cambio en una cuenta.  
  
Ejemplo:  
  
```text  
Banco aumenta $10,000.  
```  
  
o:  
  
```text  
Proveedores disminuye $5,000.  
```  
  
Los movimientos se registran mediante cargos y abonos.  
  
---  
  
# 7. Cargo y abono  
  
Los movimientos contables se registran en dos lados:  
  
```text  
Cargo  
Abono  
```  
  
En inglés suelen llamarse:  
  
```text  
Debit  
Credit  
```  
  
La parte que suele confundir al principio es que:  
  
> **Cargo no significa necesariamente “salida de dinero”.**  
  
y:  
  
> **Abono no significa necesariamente “entrada de dinero”.**  
  
Su significado depende del tipo de cuenta.  
  
Por ahora, como desarrollador, la regla más importante es:  
  
```text  
Toda póliza contabilizada debe tener:  
Total cargos = Total abonos  
```  
  
---  
  
# 8. ¿Por qué cargos y abonos deben ser iguales?  
  
La contabilidad utiliza partida doble.  
  
Esto significa que una operación afecta al menos dos lugares.  
  
Ejemplo sencillo:  
  
La empresa recibe $10,000 en el banco por una venta.  
  
Podemos pensar:  
  
```text  
Banco aumenta       $10,000  
Ventas aumenta      $10,000  
```  
  
Contablemente esos efectos se representan con lados opuestos.  
  
Ejemplo conceptual:  
  
```text  
Bancos     Cargo   10,000  
Ventas     Abono   10,000  
```  
  
Entonces:  
  
```text  
Cargos = 10,000  
Abonos = 10,000  
```  
  
La operación está balanceada.  
  
---  
  
# 9. Partida doble  
  
La **partida doble** es el principio según el cual cada operación tiene efectos compensados.  
  
No significa necesariamente que siempre haya exactamente dos líneas.  
  
Puede existir:  
  
```text  
Cargo 1  
Cargo 2  
Abono 1  
Abono 2  
```  
  
Siempre que:  
  
```text  
SUM(cargos) = SUM(abonos)  
```  
  
Ejemplo:  
  
```text  
Gasto             Cargo    10,000  
IVA acreditable   Cargo     1,600  
Proveedores       Abono    11,600  
```  
  
Resultado:  
  
```text  
Cargos = 11,600  
Abonos = 11,600  
```  
  
---  
  
# 10. Partida contable  
  
Una **partida contable** es una línea individual dentro de una póliza.  
  
Ejemplo:  
  
```text  
Cuenta: Gastos de oficina  
Cargo: 10,000  
Abono: 0  
```  
  
otra partida:  
  
```text  
Cuenta: IVA acreditable  
Cargo: 1,600  
Abono: 0  
```  
  
otra:  
  
```text  
Cuenta: Proveedores  
Cargo: 0  
Abono: 11,600  
```  
  
Estas tres partidas juntas forman una póliza.  
  
En el proyecto:  
  
```text  
AccountingPolicyEntry  
```  
  
---  
  
# 11. Póliza contable  
  
Una **póliza contable** es un conjunto de partidas que representan una operación o grupo de operaciones.  
  
Ejemplo:  
  
```text  
Póliza de compra  
  
Gasto             Cargo    10,000  
IVA acreditable   Cargo     1,600  
Proveedores       Abono    11,600  
```  
  
En nuestro proyecto utilizaremos:  
  
```text  
AccountingPolicy  
```  
  
La póliza responde a una pregunta como:  
  
> **¿Cómo decidió el contador representar esta operación dentro de la contabilidad?**  
  
---  
  
# 12. Factura y póliza no son lo mismo  
  
Este es uno de los conceptos más importantes del proyecto.  
  
Una factura dice:  
  
> “Ocurrió una operación fiscal.”  
  
Una póliza dice:  
  
> “Así se registró esa operación contablemente.”  
  
Entonces:  
  
```text  
Factura ≠ Póliza  
```  
  
Puede existir:  
  
```text  
1 factura → varias pólizas  
```  
  
y también:  
  
```text  
varias facturas → 1 póliza  
```  
  
Incluso:  
  
```text  
1 póliza → ningún XML  
```  
  
cuando se trata de ajustes u otros movimientos internos.  
  
---  
  
# 13. Saldo  
  
El **saldo** es el valor acumulado que tiene una cuenta después de considerar sus movimientos.  
  
Ejemplo simplificado:  
  
```text  
Banco inicia con:      100,000  
Entradas:               30,000  
Salidas:                20,000  
  
Saldo resultante:      110,000  
```  
  
El cálculo real depende de la naturaleza de la cuenta, pero esta idea es suficiente para entender el negocio.  
  
---  
  
# 14. Saldo inicial  
  
El **saldo inicial** es el valor con el que una cuenta comienza un periodo o ejercicio.  
  
Ejemplo:  
  
```text  
Banco al comenzar enero:  
$100,000  
```  
  
Ese importe no necesariamente fue generado dentro del nuevo sistema.  
  
Puede venir de:  
  
- un periodo anterior;  
- una migración;  
- otro sistema contable.  
  
Por eso los saldos iniciales son importantes para migrar empresas.  
  
---  
  
# 15. Balanza de comprobación  
  
La **balanza de comprobación** es un reporte que resume las cuentas y sus movimientos.  
  
Ejemplo simplificado:  
  
```text  
Cuenta        Inicial   Cargos   Abonos   Final  
  
Bancos        100,000   30,000   20,000   110,000  
Clientes       20,000   10,000    5,000    25,000  
Proveedores    15,000    4,000    7,000    18,000  
```  
  
La balanza sirve para revisar cómo quedó la contabilidad después de registrar pólizas.  
  
En el proyecto, una pregunta importante del MVP es:  
  
> **¿Las pólizas que registramos terminan reflejándose correctamente en la balanza?**  
  
---  
  
# 16. Auxiliar contable  
  
Un **auxiliar** muestra el detalle de los movimientos de una cuenta.  
  
Si la balanza dice:  
  
```text  
Banco: $110,000  
```  
  
el auxiliar permite preguntar:  
  
> “¿De dónde salen esos $110,000?”  
  
Entonces podríamos ver:  
  
```text  
01 julio  +10,000  
05 julio   -5,000  
10 julio  +20,000  
...  
```  
  
La balanza resume.  
  
El auxiliar explica.  
  
---  
  
# 17. Activo  
  
Un **activo** representa recursos o derechos que tiene la empresa.  
  
Ejemplos:  
  
```text  
Dinero en bancos  
Clientes que deben dinero  
Inventarios  
Equipo  
Edificios  
```  
  
Una cuenta por cobrar normalmente se considera un activo porque representa dinero que la empresa tiene derecho a recibir.  
  
---  
  
# 18. Pasivo  
  
Un **pasivo** representa obligaciones de la empresa.  
  
Ejemplos:  
  
```text  
Deudas con proveedores  
Préstamos  
Impuestos por pagar  
```  
  
Si la empresa debe $50,000 a un proveedor, existe una obligación.  
  
Eso forma parte de sus pasivos.  
  
---  
  
# 19. Capital  
  
El **capital contable** representa, de forma simplificada, la parte del valor de la empresa atribuible a sus propietarios después de considerar activos y obligaciones.  
  
Una relación básica es:  
  
```text  
Activos = Pasivos + Capital  
```  
  
No es necesario profundizar demasiado en este concepto para el MVP, pero ayuda a entender la lógica de equilibrio contable.  
  
---  
  
# 20. Ingreso  
  
Un **ingreso** representa valor generado por la actividad de la empresa.  
  
Ejemplo:  
  
```text  
Venta de servicio: $10,000  
```  
  
No debe confundirse automáticamente con entrada de dinero.  
  
Una empresa puede generar un ingreso hoy:  
  
```text  
Venta $10,000  
```  
  
pero cobrarlo dentro de 30 días.  
  
Entonces:  
  
```text  
Ingreso ≠ Cobro  
```  
  
Esta diferencia es clave para entender PPD.  
  
---  
  
# 21. Gasto  
  
Un **gasto** representa recursos utilizados para operar o generar ingresos.  
  
Ejemplos:  
  
```text  
Renta  
Papelería  
Internet  
Servicios profesionales  
Combustible  
```  
  
Tampoco significa necesariamente que ya se pagó.  
  
Puede existir:  
  
```text  
Gasto reconocido hoy  
Pago dentro de 30 días  
```  
  
Entonces:  
  
```text  
Gasto ≠ Pago  
```  
  
---  
  
# 22. Cliente  
  
Un **cliente** es una persona o empresa a la que nuestra empresa vende bienes o servicios.  
  
Si todavía no ha pagado, normalmente puede existir una:  
  
```text  
Cuenta por cobrar  
```  
  
relacionada con ese cliente.  
  
---  
  
# 23. Proveedor  
  
Un **proveedor** es una persona o empresa de la que compramos bienes o servicios.  
  
Si todavía no le hemos pagado, normalmente puede existir una:  
  
```text  
Cuenta por pagar  
```  
  
---  
  
# 24. Acreedor  
  
Un **acreedor** también representa un tercero al que la empresa debe dinero.  
  
La diferencia práctica entre:  
  
```text  
Proveedor  
Acreedor  
```  
  
puede depender de la clasificación utilizada por el contador.  
  
Para nuestro proyecto no debemos imponer todavía una diferencia automática.  
  
---  
  
# 25. Cuenta por cobrar  
  
Una **cuenta por cobrar** representa dinero que otra persona o empresa nos debe.  
  
Ejemplo:  
  
```text  
Vendemos $100,000.  
El cliente pagará después.  
```  
  
En ese momento:  
  
```text  
Ingreso existe  
Dinero en banco todavía no  
Cliente nos debe $100,000  
```  
  
Ese derecho de cobro se representa mediante una cuenta por cobrar.  
  
---  
  
# 26. Cuenta por pagar  
  
Una **cuenta por pagar** representa dinero que nosotros debemos.  
  
Ejemplo:  
  
```text  
Compramos $50,000.  
Pagaremos dentro de 30 días.  
```  
  
Entonces:  
  
```text  
Compra/gasto existe  
Banco todavía no disminuye  
Debemos $50,000 al proveedor  
```  
  
---  
  
# 27. Cobro  
  
Un **cobro** ocurre cuando la empresa recibe efectivamente dinero.  
  
Ejemplo:  
  
```text  
Cliente debía $100,000.  
Cliente deposita $100,000.  
```  
  
Ahora ocurre:  
  
```text  
Banco aumenta  
Cuenta por cobrar disminuye  
```  
  
Por eso:  
  
```text  
Ingreso ≠ Cobro  
```  
  
---  
  
# 28. Pago  
  
Un **pago** ocurre cuando la empresa entrega dinero para liquidar una obligación.  
  
Ejemplo:  
  
```text  
Debíamos $50,000 a un proveedor.  
Transferimos $50,000.  
```  
  
Ahora:  
  
```text  
Banco disminuye  
Cuenta por pagar disminuye  
```  
  
Por eso:  
  
```text  
Gasto ≠ Pago  
```  
  
---  
  
# 29. Provisión  
  
Para este proyecto podemos entender provisionalmente una **provisión** como el registro de una operación antes de que el dinero sea pagado o cobrado.  
  
Ejemplo:  
  
```text  
Hoy recibimos factura.  
Pagaremos después.  
```  
  
Hoy podemos reconocer:  
  
```text  
Existe un gasto.  
Existe una deuda.  
```  
  
Más adelante:  
  
```text  
Se realiza el pago.  
```  
  
La forma exacta en que el despacho utiliza provisiones sigue pendiente de validación.  
  
---  
  
# 30. PUE  
  
**PUE** significa:  
  
```text  
Pago en Una sola Exhibición  
```  
  
Dentro del proyecto se utiliza para distinguir operaciones donde el pago se plantea como realizado en una sola exhibición.  
  
La regla contable exacta todavía debe validarse.  
  
Como desarrollador, simplemente debes recordar:  
  
```text  
PUE y PPD representan escenarios diferentes.  
```  
  
---  
  
# 31. PPD  
  
**PPD** significa:  
  
```text  
Pago en Parcialidades o Diferido  
```  
  
La idea sencilla es:  
  
> La factura existe, pero el pago puede ocurrir después.  
  
Ejemplo:  
  
```text  
Factura: $100,000  
```  
  
Pagos:  
  
```text  
Julio:  $40,000  
Agosto: $60,000  
```  
  
Por eso PPD introduce complejidad adicional.  
  
---  
  
# 32. Complemento de pago  
  
Un **complemento de pago** es un CFDI que permite relacionar fiscalmente un pago con una o más facturas.  
  
Para nuestro modelo mental:  
  
```text  
Factura  
    ↓Pago  
    ↓Complemento  
```  
  
Ejemplo:  
  
```text  
Factura $100,000  
├── Complemento pago $40,000  
└── Complemento pago $60,000  
```  
  
Esto ayuda a saber cuánto se ha pagado y qué sigue pendiente.  
  
---  
  
# 33. IVA  
  
**IVA** significa:  
  
```text  
Impuesto al Valor Agregado  
```  
  
Ejemplo:  
  
```text  
Servicio: $10,000  
IVA 16%:  $1,600  
Total:   $11,600  
```  
  
La empresa puede cobrar IVA en ventas y pagar IVA en compras.  
  
Esto genera diferentes cuentas y tratamientos.  
  
---  
  
# 34. IVA trasladado  
  
De forma simplificada, el **IVA trasladado** es el IVA que la empresa cobra a sus clientes en una operación gravada.  
  
Ejemplo:  
  
```text  
Venta: $10,000  
IVA:    $1,600  
```  
  
El cliente paga:  
  
```text  
$11,600  
```  
  
Los $1,600 representan IVA dentro de la operación.  
  
---  
  
# 35. IVA acreditable  
  
De forma simplificada, el **IVA acreditable** es IVA asociado a compras o gastos que puede utilizarse fiscalmente según las reglas aplicables.  
  
Ejemplo:  
  
```text  
Compra: $10,000  
IVA:     $1,600  
```  
  
El tratamiento exacto depende de las reglas fiscales y de la operación.  
  
Para el proyecto, no debemos asumir que todo IVA de una compra siempre será automáticamente acreditable.  
  
---  
  
# 36. IVA pendiente  
  
En algunos escenarios el sistema necesita diferenciar entre:  
  
```text  
IVA relacionado con una factura  
```  
  
y:  
  
```text  
IVA relacionado con un pago/cobro efectivo  
```  
  
Por eso aparece el concepto:  
  
```text  
IVA pendiente  
```  
  
Es especialmente importante en operaciones PPD.  
  
La regla exacta todavía debe confirmarse.  
  
---  
  
# 37. Retención  
  
Una **retención** ocurre cuando una parte de un impuesto no se entrega directamente al proveedor o receptor del pago, sino que se retiene para darle el tratamiento fiscal correspondiente.  
  
Ejemplo conceptual:  
  
```text  
Importe bruto  
- retención  
= importe efectivamente entregado  
```  
  
Puede existir:  
  
- retención de IVA;  
- retención de ISR;  
- otros casos.  
  
Las reglas exactas deben venir de expertos contables/fiscales.  
  
---  
  
# 38. Deducible  
  
Un gasto **deducible** es un gasto que puede considerarse para efectos fiscales bajo determinadas reglas.  
  
No todos los gastos necesariamente tienen el mismo tratamiento.  
  
El sistema eventualmente puede necesitar distinguir:  
  
```text  
Deducible  
Parcialmente deducible  
No deducible  
```  
  
Pero el MVP no debe intentar decidir esto automáticamente.  
  
---  
  
# 39. Nota de crédito  
  
Una **nota de crédito** modifica o disminuye una operación previa.  
  
Ejemplo:  
  
```text  
Factura original: $10,000  
```  
  
Posteriormente existe una corrección:  
  
```text  
Nota de crédito: -$2,000  
```  
  
Conceptualmente, la operación termina teniendo un efecto neto menor.  
  
El tratamiento exacto se validará después.  
  
---  
  
# 40. Cancelación de CFDI  
  
Una cancelación significa que un CFDI deja de estar vigente fiscalmente.  
  
Pero para nuestro sistema:  
  
```text  
Cancelar ≠ borrar  
```  
  
Necesitamos conservarlo porque pudo haber sido:  
  
- importado;  
- contabilizado;  
- relacionado con pólizas;  
- sustituido por otro documento.  
  
La trazabilidad debe permanecer.  
  
---  
  
# 41. Sustitución de CFDI  
  
Una sustitución ocurre cuando un CFDI se reemplaza por otro.  
  
Podemos imaginar:  
  
```text  
CFDI original  
    ↓cancelado  
    ↓CFDI sustituto  
```  
  
El sistema debe conservar esa relación.  
  
No debe comportarse como si el documento original nunca hubiera existido.  
  
---  
  
# 42. Póliza de ajuste  
  
Una **póliza de ajuste** sirve para corregir o reclasificar movimientos contables.  
  
Ejemplo conceptual:  
  
```text  
Se registró un gasto en la cuenta equivocada.  
```  
  
El contador puede necesitar moverlo:  
  
```text  
Cuenta incorrecta  
    ↓Cuenta correcta  
```  
  
Esto puede ocurrir sin un CFDI nuevo.  
  
Por eso:  
  
```text  
AccountingPolicy puede existir sin FiscalDocument.  
```  
  
---  
  
# 43. Cierre contable  
  
Un **cierre contable** significa que el contador considera terminado un periodo o ejercicio.  
  
Conceptualmente:  
  
```text  
Periodo abierto  
↓  
revisión  
↓  
cierre  
↓  
Periodo cerrado  
```  
  
Después del cierre normalmente no deberían hacerse cambios ordinarios.  
  
La política exacta debe confirmarse.  
  
---  
  
# 44. Reapertura  
  
Una **reapertura** ocurre cuando un periodo cerrado necesita volver a modificarse.  
  
Ejemplo:  
  
```text  
Julio estaba cerrado.  
Se detecta un error.  
Un usuario autorizado reabre julio.  
```  
  
Este tipo de acción debería dejar trazabilidad.  
  
---  
  
# 45. Póliza de cierre  
  
Una **póliza de cierre** representa movimientos específicos realizados al finalizar un periodo o ejercicio.  
  
No necesitamos conocer todavía su mecánica exacta.  
  
Para el proyecto basta con entender que es:  
  
```text  
un tipo especial de AccountingPolicy  
```  
  
relacionado con el cierre.  
  
---  
  
# 46. Moneda extranjera  
  
Una operación en **moneda extranjera** ocurre cuando el documento utiliza una moneda distinta a la moneda base de la empresa.  
  
Ejemplo:  
  
```text  
100 USD  
```  
  
Si la contabilidad se lleva en MXN, necesitamos conocer cuánto representan esos dólares en pesos.  
  
Ahí aparece el tipo de cambio.  
  
---  
  
# 47. Tipo de cambio  
  
El **tipo de cambio** es el factor utilizado para convertir una moneda a otra.  
  
Ejemplo:  
  
```text  
100 USD  
× 18 MXN/USD  
= 1,800 MXN  
```  
  
Es importante conservar el tipo de cambio utilizado históricamente.  
  
No deberíamos recalcular una operación pasada con el tipo de cambio de hoy.  
  
---  
  
# 48. Conciliación bancaria  
  
La **conciliación bancaria** consiste en comparar:  
  
```text  
lo que dice el banco  
```  
  
contra:  
  
```text  
lo que dice nuestra contabilidad  
```  
  
Ejemplo:  
  
El banco muestra:  
  
```text  
Transferencia -$5,000  
```  
  
El sistema contable también debería tener un movimiento que explique esos $5,000.  
  
Si no existe, tenemos una diferencia por investigar.  
  
---  
  
# 49. Contabilidad electrónica  
  
Dentro de este proyecto, **contabilidad electrónica** se refiere a procesos y archivos contables estructurados requeridos para cumplir determinadas obligaciones fiscales.  
  
No significa simplemente:  
  
```text  
“usar un sistema digital”  
```  
  
Puede implicar generar información específica como:  
  
- catálogo;  
- balanza;  
- archivos requeridos fiscalmente.  
  
Quedará para fases posteriores.  
  
---  
  
# 50. Estado de resultados  
  
El **estado de resultados** es un reporte que resume, de forma simplificada:  
  
```text  
Ingresos  
- Costos  
- Gastos  
= Resultado  
```  
  
Ayuda a responder:  
  
> “¿La empresa ganó o perdió dinero durante un periodo?”  
  
Aunque no es el foco inmediato del MVP, es un reporte contable importante.  
  
---  
  
# 51. Balance general / estado de situación financiera  
  
Este reporte muestra, de manera resumida:  
  
```text  
Activos  
Pasivos  
Capital  
```  
  
Ayuda a responder:  
  
> “¿Qué tiene la empresa, qué debe y cuál es su posición financiera?”  
  
Relación básica:  
  
```text  
Activos = Pasivos + Capital  
```  
  
---  
  
# 52. Diario  
  
En contabilidad, el **diario** registra operaciones de forma cronológica.  
  
Dentro de sistemas mexicanos también podemos encontrar:  
  
```text  
Póliza de diario  
```  
  
que suele utilizarse para movimientos que no corresponden directamente a ingreso o egreso.  
  
La utilización concreta dependerá del despacho.  
  
---  
  
# 53. Mayor  
  
El **mayor** organiza los movimientos por cuenta.  
  
Mientras el diario pregunta:  
  
> “¿Qué ocurrió en orden cronológico?”  
  
el mayor ayuda a preguntar:  
  
> “¿Qué ocurrió específicamente en esta cuenta?”  
  
Por ejemplo:  
  
```text  
Cuenta Bancos  
├── movimiento 1  
├── movimiento 2  
└── movimiento 3  
```  
  
---  
  
# 54. Ejercicio  
  
Un **ejercicio contable** es normalmente el año contable.  
  
Ejemplo:  
  
```text  
Ejercicio 2026  
```  
  
Dentro de ese ejercicio existen periodos.  
  
---  
  
# 55. Periodo  
  
Un **periodo** es una división del ejercicio utilizada para trabajar la contabilidad.  
  
En nuestro proyecto normalmente será mensual.  
  
Ejemplo:  
  
```text  
Ejercicio: 2026  
Periodo: Julio  
```  
  
Así que el contexto de trabajo será:  
  
```text  
Empresa  
+  
Ejercicio  
+  
Periodo  
```  
  
---  
  
# 56. Contabilizar  
  
**Contabilizar** significa convertir una operación en un registro contable que afecta formalmente las cuentas.  
  
Esto es diferente de:  
  
```text  
Guardar borrador  
```  
  
Una póliza puede estar capturada pero todavía no contabilizada.  
  
Cuando se contabiliza, sus partidas deben afectar los saldos y reportes correspondientes.  
  
---  
  
# 57. Borrador  
  
Un **borrador** es un registro todavía incompleto o editable.  
  
Ejemplo:  
  
```text  
Póliza:  
Cargos 10,000  
Abonos 8,000  
```  
  
Está descuadrada.  
  
Podemos permitir guardar el trabajo como borrador, aunque todavía no pueda contabilizarse.  
  
Este comportamiento es un supuesto del MVP.  
  
---  
  
# 58. Trazabilidad  
  
La **trazabilidad** significa poder reconstruir el camino de una operación.  
  
Ejemplo:  
  
```text  
CFDI  
↓  
Póliza  
↓  
Partidas  
↓  
Cuentas  
↓  
Balanza  
```  
  
o al revés:  
  
```text  
Balanza  
↓  
Cuenta  
↓  
Partida  
↓  
Póliza  
↓  
CFDI  
```  
  
Es una de las características más importantes del sistema.  
  
---  
  
# 59. El ejemplo completo  
  
Supongamos que la empresa compra un servicio.  
  
Factura:  
  
```text  
Servicio: $10,000  
IVA:      $1,600  
Total:   $11,600  
```  
  
Todavía no paga.  
  
Podríamos entenderlo conceptualmente como:  
  
```text  
Recibimos CFDI  
        ↓Existe gasto  
        ↓Existe IVA  
        ↓Debemos dinero al proveedor  
```  
  
El contador crea una póliza:  
  
```text  
Gasto             Cargo    10,000  
IVA               Cargo     1,600  
Proveedor         Abono    11,600  
```  
  
Después paga:  
  
```text  
Proveedor         Cargo    11,600  
Banco             Abono    11,600  
```  
  
Así podemos ver dos momentos diferentes:  
  
```text  
1. Reconocer la operación.  
2. Pagar la operación.  
```  
  
Esta separación explica por qué una sola factura puede terminar relacionada con varias pólizas.  
  
> Los asientos anteriores son ejemplos pedagógicos y no deben considerarse reglas definitivas del proyecto hasta validarse con los contadores.  
  
---  
  
# 60. Mapa mental del negocio  
  
Si quieres entender casi todo el MVP, conserva este flujo:  
  
```text  
Algo ocurre en la empresa  
        ↓Puede existir un CFDI  
        ↓El contador interpreta la operación  
        ↓Crea una AccountingPolicy  
        ↓Agrega AccountingPolicyEntries  
        ↓Cada partida afecta una Account  
        ↓Las cuentas acumulan movimientos  
        ↓Los movimientos forman saldos  
        ↓Los saldos aparecen en balanzas y reportes  
```  
  
Cuando existe pago diferido:  
  
```text  
Factura  
↓  
Cuenta por cobrar/pagar  
↓  
Pago o cobro posterior  
↓  
Nueva póliza  
```  
  
---  
  
# 61. Diferencias que conviene memorizar  
  
## Factura vs póliza  
  
```text  
Factura = documento fiscal  
Póliza = registro contable  
```  
  
## Ingreso vs cobro  
  
```text  
Ingreso = valor generado  
Cobro = dinero recibido  
```  
  
## Gasto vs pago  
  
```text  
Gasto = valor consumido/reconocido  
Pago = dinero entregado  
```  
  
## Cuenta por cobrar vs banco  
  
```text  
Cuenta por cobrar = me deben  
Banco = ya tengo el dinero  
```  
  
## Cuenta por pagar vs banco  
  
```text  
Cuenta por pagar = debo  
Banco = de aquí saldrá el dinero cuando pague  
```  
  
## Balanza vs auxiliar  
  
```text  
Balanza = resumen  
Auxiliar = detalle  
```  
  
## CFDI cancelado vs eliminado  
  
```text  
Cancelado = permanece con otro estado  
Eliminado = desaparece  
  
Para este sistema:  
cancelar nunca debe significar borrar el historial.  
```  
  
---  
  
# 62. Las 10 ideas que más te conviene dominar  
  
Si entiendes estas diez ideas, ya tienes una base bastante buena para hablar del proyecto con contadores:  
  
1. **Una cuenta es una categoría donde se acumulan movimientos.**  
2. **Una póliza agrupa partidas contables.**  
3. **Cada partida afecta una cuenta.**  
4. **Cargos y abonos deben quedar balanceados.**  
5. **Una factura y una póliza no son lo mismo.**  
6. **Un ingreso no necesariamente significa que ya cobramos.**  
7. **Un gasto no necesariamente significa que ya pagamos.**  
8. **PPD permite que factura y pago ocurran en momentos diferentes.**  
9. **La balanza resume cómo quedaron las cuentas.**  
10. **La trazabilidad permite explicar cómo un CFDI terminó afectando la contabilidad.**  
  
---  
  
# 63. Qué todavía debe enseñarnos un contador  
  
Este documento permite entender el lenguaje general.  
  
Sin embargo, todavía necesitaremos que los expertos del negocio nos expliquen:  
  
- qué cuentas usan realmente;  
- qué asiento realizan en cada situación;  
- cuándo provisionan;  
- cómo manejan IVA pendiente;  
- qué diferencias aplican entre PUE y PPD;  
- cómo registran cancelaciones;  
- qué reglas consideran obligatorias;  
- cuáles son excepciones;  
- cómo realizan cierres;  
- cómo trabajan DIOT;  
- qué información necesitan revisar cada mes.  
  
Es decir:  
  
> Podemos entender **la estructura del problema** sin ser contadores, pero las reglas específicas del despacho deben venir de quienes realizan la contabilidad.
