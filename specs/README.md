# Índice de specs

Este índice reúne el trabajo por funcionalidad. El estado de cada fila se genera desde su `spec.md`; indica el avance del cambio documentado, no sustituye la comprobación del código y las pruebas de backend y frontend.

No todo cambio requiere una spec. Consulta el [flujo breve](../docs/flujo-spec.md); si hace falta una nueva, usa la [plantilla](./_plantilla/spec.md). `spec.md` basta para registrarla; plan, tareas y verificación separados son opcionales. Las specs existentes conservan su estructura y criterios.

## Funcionalidades

<!-- BEGIN SPEC STATUS -->
| Spec | Funcionalidad | Estado | Dependencias de preparación |
|---|---|---|---|
| [SPEC-001](001-acceso-usuarios-empresas/spec.md) | Acceso, usuarios y empresas | **Implementada** | Ninguna funcionalidad previa. |
| [SPEC-002](002-contexto-contable/spec.md) | Contexto contable | **QA** | [SPEC-001](001-acceso-usuarios-empresas/spec.md) |
| [SPEC-003](003-catalogo-cuentas/spec.md) | Catálogo de cuentas | **QA** | [SPEC-001](001-acceso-usuarios-empresas/spec.md), [SPEC-002](002-contexto-contable/spec.md) |
| [SPEC-004](004-documentos-fiscales/spec.md) | Documentos fiscales | **Implementada** | [SPEC-001](001-acceso-usuarios-empresas/spec.md), [SPEC-002](002-contexto-contable/spec.md) |
| [SPEC-005](005-descarga-simulada/spec.md) | Descarga simulada | **Implementada** | [SPEC-001](001-acceso-usuarios-empresas/spec.md), [SPEC-002](002-contexto-contable/spec.md), [SPEC-004](004-documentos-fiscales/spec.md) |
| [SPEC-006](006-polizas-trazabilidad/spec.md) | Pólizas y trazabilidad | **QA** | [SPEC-001](001-acceso-usuarios-empresas/spec.md), [SPEC-002](002-contexto-contable/spec.md), [SPEC-003](003-catalogo-cuentas/spec.md), [SPEC-004](004-documentos-fiscales/spec.md) |
| [SPEC-007](007-ppd-complementos/spec.md) | PPD y complementos | **QA** | [SPEC-002](002-contexto-contable/spec.md), [SPEC-004](004-documentos-fiscales/spec.md), [SPEC-006](006-polizas-trazabilidad/spec.md) |
| [SPEC-008](008-balanza-basica/spec.md) | Balanza básica | **Implementada** | [SPEC-002](002-contexto-contable/spec.md), [SPEC-003](003-catalogo-cuentas/spec.md), [SPEC-006](006-polizas-trazabilidad/spec.md) |
| [SPEC-009](009-reportes-exportacion/spec.md) | Reportes y exportación | **Implementada** | [SPEC-002](002-contexto-contable/spec.md), [SPEC-004](004-documentos-fiscales/spec.md), [SPEC-006](006-polizas-trazabilidad/spec.md), [SPEC-008](008-balanza-basica/spec.md) |
<!-- END SPEC STATUS -->

## Al retomar trabajo

- Contrasta el requisito con el código y las pruebas de los repositorios afectados. El estado documental no acredita la implementación.
- Las preguntas de dominio que todavía afecten un cambio se registran en la spec correspondiente. El [mapa de fuentes](../docs/fuentes.md) ofrece contexto cuando haga falta.
- Ejecuta `python3 scripts/spec_index.py --check` tras editar una spec; usa `--write` si cambia el índice, revisando antes cualquier cambio local ajeno.
