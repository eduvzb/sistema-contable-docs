# Specs del MVP

Una spec por funcionalidad, compartida por backend y frontend. Para trabajar usa el [flujo SDD](../docs/flujo-spec.md) y la [plantilla](_plantilla.md).

## Orden y dependencias

SPEC-001 y SPEC-002 están **Listas**; las demás specs iniciales permanecen en **Borrador**. Los pendientes de cada una explican qué falta antes de Lista; no significan que todo el MVP esté bloqueado para su definición.

| Spec | Funcionalidad | Dependencias de preparación |
|---|---|---|
| [SPEC-001](001-acceso-usuarios-empresas.md) | Acceso, usuarios y empresas — **Lista** | Ninguna |
| [SPEC-002](002-contexto-contable.md) | Contexto contable — **Lista** | [SPEC-001](001-acceso-usuarios-empresas.md) |
| [SPEC-003](003-catalogo-cuentas.md) | Catálogo de cuentas | [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md) |
| [SPEC-004](004-documentos-fiscales.md) | Documentos fiscales | [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md) |
| [SPEC-005](005-descarga-simulada.md) | Descarga simulada | [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md), [SPEC-004](004-documentos-fiscales.md) |
| [SPEC-006](006-polizas-trazabilidad.md) | Pólizas y trazabilidad | [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md), [SPEC-003](003-catalogo-cuentas.md), [SPEC-004](004-documentos-fiscales.md) |
| [SPEC-007](007-ppd-complementos.md) | PPD y complementos | [SPEC-002](002-contexto-contable.md), [SPEC-004](004-documentos-fiscales.md), [SPEC-006](006-polizas-trazabilidad.md) |
| [SPEC-008](008-balanza-basica.md) | Balanza básica | [SPEC-002](002-contexto-contable.md), [SPEC-003](003-catalogo-cuentas.md), [SPEC-006](006-polizas-trazabilidad.md) |
| [SPEC-009](009-reportes-exportacion.md) | Reportes y exportación | [SPEC-002](002-contexto-contable.md), [SPEC-004](004-documentos-fiscales.md), [SPEC-006](006-polizas-trazabilidad.md), [SPEC-008](008-balanza-basica.md) |

Preparar acceso/contexto; después cuentas y documentos; luego pólizas; finalmente PPD/balanza y reportes. La simulación puede prepararse cuando exista el contrato de incorporación de documentos. No se necesita terminar PPD para preparar la balanza básica o los reportes del flujo PUE.

**Integraciones posteriores, sin duplicar contratos:** SPEC-004 consume el indicador derivado de relaciones POSTED definido por SPEC-006; SPEC-005 verifica continuidad con SPEC-006; la trazabilidad de complementos/pagos se completa con SPEC-007. Estas integraciones son necesarias para considerar completas las capacidades correspondientes, aunque la preparación básica de XML ocurra antes. Backend y frontend comparten ID y revisión de spec; los contratos se concretan antes de Lista.

## Cobertura del alcance

Cada sección funcional del MVP tiene responsable; esta tabla enlaza a la fuente, no la sustituye.

| Sección del alcance | Responsable |
|---|---|
| [§3](../docs/planeacion/003%20-%20MVP-Scope.md#3-usuarios-incluidos) | [SPEC-001](001-acceso-usuarios-empresas.md) |
| [§4](../docs/planeacion/003%20-%20MVP-Scope.md#4-empresas) | [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md) |
| [§5](../docs/planeacion/003%20-%20MVP-Scope.md#5-periodos-contables) | [SPEC-002](002-contexto-contable.md) |
| [§6](../docs/planeacion/003%20-%20MVP-Scope.md#6-importaci%C3%B3n-y-obtenci%C3%B3n-de-xml) | [SPEC-004](004-documentos-fiscales.md), [SPEC-005](005-descarga-simulada.md) |
| [§7](../docs/planeacion/003%20-%20MVP-Scope.md#7-consulta-de-documentos-fiscales) | [SPEC-004](004-documentos-fiscales.md) |
| [§8](../docs/planeacion/003%20-%20MVP-Scope.md#8-cat%C3%A1logo-de-cuentas) | [SPEC-003](003-catalogo-cuentas.md) |
| [§9](../docs/planeacion/003%20-%20MVP-Scope.md#9-p%C3%B3lizas-contables) | [SPEC-006](006-polizas-trazabilidad.md) |
| [§10](../docs/planeacion/003%20-%20MVP-Scope.md#10-partidas-contables) | [SPEC-006](006-polizas-trazabilidad.md) |
| [§11](../docs/planeacion/003%20-%20MVP-Scope.md#11-relaci%C3%B3n-xml--p%C3%B3liza) | [SPEC-006](006-polizas-trazabilidad.md) |
| [§12](../docs/planeacion/003%20-%20MVP-Scope.md#12-ingresos) | [SPEC-006](006-polizas-trazabilidad.md) |
| [§13](../docs/planeacion/003%20-%20MVP-Scope.md#13-egresos) | [SPEC-006](006-polizas-trazabilidad.md) |
| [§14](../docs/planeacion/003%20-%20MVP-Scope.md#14-pue) | [SPEC-004](004-documentos-fiscales.md), [SPEC-006](006-polizas-trazabilidad.md) |
| [§15](../docs/planeacion/003%20-%20MVP-Scope.md#15-ppd-y-complementos-de-pago) | [SPEC-007](007-ppd-complementos.md) |
| [§16](../docs/planeacion/003%20-%20MVP-Scope.md#16-reportes-incluidos) | [SPEC-008](008-balanza-basica.md), [SPEC-009](009-reportes-exportacion.md) |
| [§17](../docs/planeacion/003%20-%20MVP-Scope.md#17-auditor%C3%ADa-m%C3%ADnima) | [SPEC-006](006-polizas-trazabilidad.md) |

[El recorrido §18](../docs/planeacion/003%20-%20MVP-Scope.md#18-flujo-completo-que-debe-demostrar-el-mvp), [los escenarios mínimos §19](../docs/planeacion/003%20-%20MVP-Scope.md#19-escenarios-m%C3%ADnimos-a-probar) y [los criterios de éxito §20](../docs/planeacion/003%20-%20MVP-Scope.md#20-criterios-de-%C3%A9xito-del-mvp) se comprueban mediante las specs y el recorrido integrado de abajo. Los objetivos §1/2 y el resumen §27 se concretan mediante esta cobertura.

**Exclusiones:** [§21](../docs/planeacion/003%20-%20MVP-Scope.md#21-fuera-del-mvp) y [Alcance §22](../docs/planeacion/003%20-%20MVP-Scope.md#22-fase-posterior-1--consolidaci%C3%B3n-contable), [Alcance §23](../docs/planeacion/003%20-%20MVP-Scope.md#23-fase-posterior-2--fiscal), [Alcance §24](../docs/planeacion/003%20-%20MVP-Scope.md#24-fase-posterior-3--automatizaci%C3%B3n), [Alcance §25](../docs/planeacion/003%20-%20MVP-Scope.md#25-fase-posterior-4--integraciones) delimitan automatización, SAT real, DIOT, IVA avanzado, CFDI especiales, cierre/reapertura, bancos, contabilidad electrónica, reportería avanzada, portal de clientes y fases futuras. OQ-017 pospone migración histórica. Importar el catálogo inicial, conservar datos de moneda y representar pagos manualmente siguen dentro del MVP; no equivalen a implementar esas fases.

## Correspondencia de reglas

Los estados se copian de las fuentes sin promover supuestos a confirmaciones. Las pruebas concretas se registrarán en las specs.

| Regla | Estado de la fuente | Spec responsable / criterio |
|---|---|---|
| [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa) | CONFIRMADA | [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md) — CA-001-05; CA-002-02/04 y criterios de aislamiento de cada función |
| [BR-002](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#4-br-002--el-contador-trabaja-dentro-de-un-periodo) | CONFIRMADA | [SPEC-002](002-contexto-contable.md), [SPEC-006](006-polizas-trazabilidad.md) — CA-002-03; CA-006-01 |
| [BR-003](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#5-br-003--cada-empresa-tiene-su-propio-cat%C3%A1logo-de-cuentas) | CONFIRMADA | [SPEC-003](003-catalogo-cuentas.md), [SPEC-006](006-polizas-trazabilidad.md) — CA-003-06; CA-006-08 |
| [BR-004](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#6-br-004--cada-partida-utiliza-una-cuenta-contable) | CONFIRMADA | [SPEC-006](006-polizas-trazabilidad.md) — CA-006-01 |
| [BR-005](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#7-br-005--una-p%C3%B3liza-contabilizada-debe-estar-balanceada) | CONFIRMADA COMO REGLA DEL MVP | [SPEC-006](006-polizas-trazabilidad.md) — CA-006-03/04 |
| [BR-006](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#8-br-006--una-p%C3%B3liza-incompleta-puede-guardarse-como-borrador) | SUPUESTO MVP | [SPEC-006](006-polizas-trazabilidad.md) — CA-006-02 |
| [BR-007](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#9-br-007--una-p%C3%B3liza-puede-relacionarse-con-varios-xml) | CONFIRMADA | [SPEC-006](006-polizas-trazabilidad.md) — CA-006-06 |
| [BR-008](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#10-br-008--un-xml-puede-relacionarse-con-varias-p%C3%B3lizas) | CONFIRMADA | [SPEC-006](006-polizas-trazabilidad.md), [SPEC-007](007-ppd-complementos.md) — CA-006-07; CA-007-04/08 |
| [BR-009](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#11-br-009--una-p%C3%B3liza-puede-existir-sin-xml) | CONFIRMADA COMO NECESIDAD DEL MODELO | [SPEC-006](006-polizas-trazabilidad.md) — CA-006-05 |
| [BR-010](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#12-br-010--el-mismo-cfdi-no-debe-importarse-dos-veces) | SUPUESTO MVP | [SPEC-004](004-documentos-fiscales.md) — CA-004-03 |
| [BR-011](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#13-br-011--el-xml-original-debe-conservarse) | CONFIRMADA COMO REGLA DEL MVP | [SPEC-004](004-documentos-fiscales.md) — CA-004-01 |
| [BR-012](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#14-br-012--pue-y-ppd-se-tratan-como-escenarios-diferentes) | CONFIRMADA COMO NECESIDAD FUNCIONAL | [SPEC-004](004-documentos-fiscales.md), [SPEC-006](006-polizas-trazabilidad.md), [SPEC-007](007-ppd-complementos.md) — CA-004-04; CA-006-10; CA-007-01 |
| [BR-013](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#15-br-013--una-factura-ppd-puede-tener-varios-pagos) | CONFIRMADA | [SPEC-007](007-ppd-complementos.md) — CA-007-03/04 |
| [BR-014](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#16-br-014--los-pagos-pueden-ocurrir-en-distintos-periodos) | CONFIRMADA | [SPEC-007](007-ppd-complementos.md) — CA-007-04/08 |
| [BR-015](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#17-br-015--los-complementos-deben-conservar-su-relaci%C3%B3n-con-la-factura) | PENDIENTE DE VALIDACIÓN NORMATIVA | [SPEC-007](007-ppd-complementos.md) — CA-007-02/05 |
| [BR-016](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#18-br-016--el-contador-selecciona-manualmente-las-cuentas-contables) | CONFIRMADA PARA MVP | [SPEC-006](006-polizas-trazabilidad.md) — CA-006-01/10 |
| [BR-017](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#19-br-017--las-p%C3%B3lizas-contabilizadas-afectan-la-balanza) | CONFIRMADA | [SPEC-008](008-balanza-basica.md) — CA-008-02/03/04 |
| [BR-018](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#20-br-018--debe-existir-trazabilidad-desde-el-xml) | CONFIRMADA | [SPEC-006](006-polizas-trazabilidad.md) — CA-006-07/11 |
| [BR-019](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#21-br-019--debe-existir-trazabilidad-desde-la-p%C3%B3liza) | CONFIRMADA | [SPEC-006](006-polizas-trazabilidad.md) — CA-006-06/11 |
| [BR-020](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#22-br-020--la-descarga-autom%C3%A1tica-se-simula-en-el-mvp) | CONFIRMADA PARA MVP | [SPEC-005](005-descarga-simulada.md) — CA-005-01/02/04/06 |

## Correspondencia de escenarios

| Escenario | Tratamiento en el MVP |
|---|---|
| [AC-001](../docs/planeacion/004%20-%20Escenarios%20contables.md#3-escenario-ac-001--ingreso-pue) | [SPEC-006](006-polizas-trazabilidad.md), [SPEC-008](008-balanza-basica.md) — ingreso PUE manual, CA-006-10 y CA-008-02. |
| [AC-002](../docs/planeacion/004%20-%20Escenarios%20contables.md#4-escenario-ac-002--egreso-pue) | [SPEC-006](006-polizas-trazabilidad.md), [SPEC-008](008-balanza-basica.md) — egreso PUE manual, CA-006-10 y CA-008-02. |
| [AC-003](../docs/planeacion/004%20-%20Escenarios%20contables.md#5-escenario-ac-003--factura-ppd-pendiente-de-pago-o-cobro) | [SPEC-007](007-ppd-complementos.md) — factura pendiente, CA-007-01. |
| [AC-004](../docs/planeacion/004%20-%20Escenarios%20contables.md#6-escenario-ac-004--pago-parcial-de-factura-ppd) | [SPEC-007](007-ppd-complementos.md) — pago parcial, CA-007-03; cálculo general pendiente. |
| [AC-005](../docs/planeacion/004%20-%20Escenarios%20contables.md#7-escenario-ac-005--m%C3%BAltiples-pagos-en-distintos-periodos) | [SPEC-007](007-ppd-complementos.md) — periodos distintos, CA-007-04/08. |
| [AC-006](../docs/planeacion/004%20-%20Escenarios%20contables.md#8-escenario-ac-006--varios-xml-en-una-misma-p%C3%B3liza) | [SPEC-006](006-polizas-trazabilidad.md) — varios XML, CA-006-06. |
| [AC-007](../docs/planeacion/004%20-%20Escenarios%20contables.md#9-escenario-ac-007--un-xml-relacionado-con-varias-p%C3%B3lizas) | [SPEC-006](006-polizas-trazabilidad.md) — varias pólizas, CA-006-07. |
| [AC-008](../docs/planeacion/004%20-%20Escenarios%20contables.md#10-escenario-ac-008--p%C3%B3liza-sin-cfdi) | [SPEC-006](006-polizas-trazabilidad.md) — sin CFDI, CA-006-05; no agrega tipo CIERRE/AJUSTE. |
| [AC-009](../docs/planeacion/004%20-%20Escenarios%20contables.md#11-escenario-ac-009--provisi%C3%B3n) | [SPEC-006](006-polizas-trazabilidad.md), [SPEC-007](007-ppd-complementos.md) — solo representación manual; automatización de provisión excluida por OQ-006. |
| [AC-010](../docs/planeacion/004%20-%20Escenarios%20contables.md#12-escenario-ac-010--iva-pendiente-y-pago-posterior) | [SPEC-006](006-polizas-trazabilidad.md), [SPEC-007](007-ppd-complementos.md) — registro manual sin prescribir tratamiento; automatización de IVA excluida por OQ-007. |
| [AC-011](../docs/planeacion/004%20-%20Escenarios%20contables.md#13-escenario-ac-011--p%C3%B3liza-descuadrada-en-borrador) | [SPEC-006](006-polizas-trazabilidad.md) — borrador descuadrado, CA-006-02/03. |
| [AC-012](../docs/planeacion/004%20-%20Escenarios%20contables.md#14-escenario-ac-012--consulta-de-trazabilidad-desde-un-cfdi) | [SPEC-006](006-polizas-trazabilidad.md), [SPEC-007](007-ppd-complementos.md) — desde XML, CA-006-07/11 y CA-007-08. |
| [AC-013](../docs/planeacion/004%20-%20Escenarios%20contables.md#15-escenario-ac-013--consulta-de-trazabilidad-desde-una-p%C3%B3liza) | [SPEC-006](006-polizas-trazabilidad.md) — desde póliza, CA-006-06/11. |
| [AC-014](../docs/planeacion/004%20-%20Escenarios%20contables.md#16-escenario-ac-014--balanza-despu%C3%A9s-de-contabilizar) | [SPEC-008](008-balanza-basica.md) — balanza, CA-008-01/02/03/04. |
| [AC-015](../docs/planeacion/004%20-%20Escenarios%20contables.md#17-escenario-ac-015--documento-duplicado) | [SPEC-004](004-documentos-fiscales.md) — duplicado, CA-004-03. |
| [AC-016](../docs/planeacion/004%20-%20Escenarios%20contables.md#18-escenario-ac-016--descarga-simulada-de-xml) | [SPEC-005](005-descarga-simulada.md) — simulación, CA-005-01/02/04/06. |

[AC-F01 a AC-F10](../docs/planeacion/004%20-%20Escenarios%20contables.md#19-escenarios-posteriores-al-mvp) quedan posteriores al MVP. Los estados y pendientes de cada escenario permanecen en la fuente y se reflejan en las specs: representar el flujo no valida cuentas ni tratamiento fiscal.

## Recorrido integrado previsto

Guion de aceptación del MVP; **no ejecutado**. Preparar datos de prueba y contratos antes de convertirlo en pruebas de producto.

| Paso | Criterios relacionados |
|---|---|
| 1. Iniciar sesión | CA-001-01/02 |
| 2–3. Seleccionar empresa y periodo | CA-001-05; CA-002-01/02 |
| 4–5. Importar y localizar factura | CA-004-01/02/03/04; alternativa de descarga CA-005-01/02 |
| 6–8. Crear póliza, registrar partidas y seleccionar cuentas | CA-003-01/06; CA-006-01/08 |
| 9. Relacionar factura | CA-006-06/07 |
| 10–11. Validar balance y contabilizar | CA-006-02/03/04 |
| 12. Consultar y reconstruir la operación; comprobar corrección manual permitida | CA-006-09/11/13; CA-004-05 |
| 13. Ver impacto en balanza | CA-008-02/03/04 |
| 14. Exportar información | CA-009-01/02/03/04/06 |

Variantes: ingreso y egreso PUE, factura PPD pendiente, pago parcial y pagos en dos periodos (SPEC-007); póliza sin XML y varios XML por póliza (SPEC-006). Repetir controles de empresa no asignada en consulta, mutación, archivos y exportación. La comprensión del flujo, posibilidad de corrección manual y utilidad de la trazabilidad se validan con contadores durante la demostración (alcance §20), sin declararlas satisfechas por pruebas técnicas solamente.

## Verificación documental

**2026-09-07 — Revisión documental completada.** Esta comprobación no cambia las specs a Lista o Implementada ni acredita reglas fiscales.

- Validación local de los 26 Markdown: 389 enlaces relativos, incluidas 165 referencias con ancla, sin destinos ausentes ni enlaces Obsidian pendientes.
- Comparación de hashes de los nueve originales: sin cambios. Comparación de las copias: contenido preservado salvo la conversión de enlaces documentada en el mapa de fuentes.
- Nueve specs en Borrador, 67 criterios únicos y referencias a criterios existentes; dependencias de preparación sin ciclos. Las integraciones posteriores están identificadas aparte.
- Cobertura: las 20 BR tienen correspondencia y conservan exactamente su estado de fuente; los 16 AC están clasificados y AC-F01 a AC-F10 quedan posteriores. Las secciones funcionales §3–17 del alcance tienen responsable; §18–20 se reflejan en el recorrido y sus variantes.
- Revisión de uso del flujo con una funcionalidad nueva (SPEC-005) y una corrección (duplicados en SPEC-004): cada paso tiene fuente, responsable, preparación y evidencia prevista sin exigir archivos de tareas ni aprobaciones repetidas.
- Revisión de coherencia: SAT solo simulado, captura contable manual, supuestos etiquetados y decisiones ausentes localizadas por spec. Numeración, edición de POSTED, saldos PPD e iniciales siguen abiertos; no se resolvieron mediante reglas inventadas.

Las pruebas del producto y la demostración con contadores de las specs aún no implementadas **no se ejecutaron**. SPEC-001 conserva su evidencia real en su propia sección de verificación; el resto de esta revisión se refiere a documentación.
