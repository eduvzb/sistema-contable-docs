# Mapa de fuentes

## Procedencia y mantenimiento

Se incorporaron los nueve Markdown de `/Users/eduardovazquez/Documents/Drive/personal/Proyectos/Contabilidad/Planeación` el 2026-09-07. Los originales no se modificaron. Su contenido, fechas, estados e identificadores se preservaron; solo se convirtieron enlaces Obsidian a rutas Markdown relativas.

La copia en [planeacion](planeacion/00%20-%20Inicio.md) es desde esta incorporación la fuente mantenida en Git. La carpeta externa es referencia de origen y no se sincroniza automáticamente. Una nueva aportación externa se revisa como cambio explícito, no sobrescribe decisiones vigentes.

Las cabeceras antiguas «Documento de referencia» conservan nombres históricos, no rutas disponibles. «Borrador», «CONFIRMADA» y «SUPUESTO MVP» mantienen su significado original: una necesidad confirmada no implica que todos sus detalles estén definidos o que exista validación normativa.

## Qué consultar

| Fuente | Función y límites |
|---|---|
| [Alcance MVP](planeacion/003%20-%20MVP-Scope.md) | Decide inclusión y exclusión del primer producto; sus fases posteriores no son requisitos actuales. |
| [Reglas BR](planeacion/005%20-%20Reglas%20de%20negocio.md) | Restricciones del MVP, con su estado de certeza. |
| [Preguntas OQ](planeacion/006%20-%20Preguntas%20Abiertas.md) | Supuestos y decisiones provisionales; lo pospuesto no bloquea automáticamente el MVP. |
| [Escenarios AC](planeacion/004%20-%20Escenarios%20contables.md) | Flujos y resultados que alimentan los criterios; no fijan cuentas ni tratamientos fiscales pendientes. |
| [Glosario](planeacion/002%20-%20Glosario.md) | Lenguaje común. Un concepto o entidad candidata no obliga a implementarlo. |
| [Análisis inicial](planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md) | Contexto histórico, candidatos y descubrimiento; no desplaza la delimitación posterior del MVP. |
| [Guía de conceptos](planeacion/Conceptos/Gu%C3%ADa%20de%20conceptos.md) y [guía de escenarios](planeacion/Conceptos/Gu%C3%ADa%20Explicada%20de%20Escenarios%20Contables.md) | Material explicativo de consulta; no es autoridad para nuevas reglas. |

Aplicar la [jerarquía constitucional](constitution.md). Dentro de Planeación, leer cada fuente según su función: alcance para inclusión, BR para restricciones, OQ para decisiones provisionales y AC para ejemplos verificables. Si persiste un conflicto sustantivo, registrarlo en la spec afectada y resolverlo en su fuente antes de implementar. No elegir simplemente el párrafo más conveniente.

## Diferencias identificadas

- **Descarga:** el análisis inicial la deja abierta; alcance §6, BR-020 y AC-016 ya incluyen la simulación y excluyen SAT real. SPEC-005 sigue esa delimitación explícita.
- **Pólizas y estados:** las entidades candidatas del análisis/glosario no agregan estados ni tipos. OQ-008 y OQ-010 delimitan el MVP a DRAFT/POSTED e INGRESO/EGRESO/DIARIO. SPEC-006 conserva BR-006 como supuesto.
- **Migración y saldos:** el glosario contempla migración inicial; alcance y OQ-012/OQ-017 posponen su diseño. La balanza sí incluye saldo inicial, pero su origen y presentación requieren preparación en SPEC-008. No se asume saldo cero.
- **Cierres:** alcance menciona ABIERTO/CERRADO, pero OQ-016 pospone el flujo formal. SPEC-002 no inventa restricciones ni transiciones de cierre.
- **Provisión e IVA:** AC-009/AC-010 explican necesidades; OQ-006/OQ-007 y el alcance excluyen automatizarlas. Las partidas manuales no se convierten en tratamientos fiscales prescritos.
- **Preguntas no bloqueantes:** OQ afirma que se puede iniciar la definición del MVP. Esto permite redactar specs; no resuelve detalles de implementación ausentes. Cada spec distingue validación posterior de decisiones necesarias para quedar Lista.
- **Asincronía:** los ejemplos del glosario no obligan a agregar colas; DT-005 conserva infraestructura bajo demanda.

## Referencias no localizadas

- `PENDING_NORMATIVE_REVIEW` está enlazado desde Inicio, pero no existe entre los archivos proporcionados. Su enlace apunta a esta nota; no se ha realizado ni inventado esa revisión. OQ §23 conserva los temas pendientes.
- Las referencias a un documento de «modelo de dominio» no corresponden a un archivo independiente disponible. El análisis §29 contiene un modelo inicial de entidades candidatas; no se presenta como diseño aprobado.
- El enlace `Conceptos/005 - Reglas de negocio` no tenía archivo en esa subcarpeta. Se resolvió al único documento existente con ese nombre, conservando su etiqueta.
