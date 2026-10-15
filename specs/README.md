# Índice de specs

Este índice reúne el trabajo por funcionalidad. El estado de cada fila se genera desde su `spec.md`; indica el avance del cambio documentado, no sustituye la comprobación del código y las pruebas de backend y frontend.

Para un cambio nuevo, revisa primero si corresponde a una spec existente. Usa el [flujo de specs](../docs/flujo-spec.md) y la [plantilla](./_plantilla/spec.md). En cada carpeta, `spec.md` define el resultado esperado, `plan.md` prepara un cambio pendiente, las tareas separan backend y frontend, y `verificacion.md` conserva sólo la entrega actual.

## Funcionalidades

<!-- BEGIN SPEC STATUS -->
| Spec | Funcionalidad | Estado | Dependencias de preparación |
|---|---|---|---|
| [SPEC-001](001-acceso-usuarios-empresas/spec.md) | Acceso, usuarios y empresas | **QA** | Ninguna funcionalidad previa. |
| [SPEC-002](002-contexto-contable/spec.md) | Contexto contable | **QA** | [SPEC-001](001-acceso-usuarios-empresas/spec.md) |
| [SPEC-003](003-catalogo-cuentas/spec.md) | Catálogo de cuentas | **QA** | [SPEC-001](001-acceso-usuarios-empresas/spec.md), [SPEC-002](002-contexto-contable/spec.md) |
| [SPEC-004](004-documentos-fiscales/spec.md) | Documentos fiscales | **QA** | [SPEC-001](001-acceso-usuarios-empresas/spec.md), [SPEC-002](002-contexto-contable/spec.md) |
| [SPEC-005](005-descarga-simulada/spec.md) | Descarga simulada | **QA** | [SPEC-001](001-acceso-usuarios-empresas/spec.md), [SPEC-002](002-contexto-contable/spec.md), [SPEC-004](004-documentos-fiscales/spec.md) |
| [SPEC-006](006-polizas-trazabilidad/spec.md) | Pólizas y trazabilidad | **QA** | [SPEC-001](001-acceso-usuarios-empresas/spec.md), [SPEC-002](002-contexto-contable/spec.md), [SPEC-003](003-catalogo-cuentas/spec.md), [SPEC-004](004-documentos-fiscales/spec.md) |
| [SPEC-007](007-ppd-complementos/spec.md) | PPD y complementos | **QA** | [SPEC-002](002-contexto-contable/spec.md), [SPEC-004](004-documentos-fiscales/spec.md), [SPEC-006](006-polizas-trazabilidad/spec.md) |
| [SPEC-008](008-balanza-basica/spec.md) | Balanza básica | **QA** | [SPEC-002](002-contexto-contable/spec.md), [SPEC-003](003-catalogo-cuentas/spec.md), [SPEC-006](006-polizas-trazabilidad/spec.md) |
| [SPEC-009](009-reportes-exportacion/spec.md) | Reportes y exportación | **QA** | [SPEC-002](002-contexto-contable/spec.md), [SPEC-004](004-documentos-fiscales/spec.md), [SPEC-006](006-polizas-trazabilidad/spec.md), [SPEC-008](008-balanza-basica/spec.md) |
<!-- END SPEC STATUS -->

## Al retomar trabajo

- Contrasta el requisito con el código y las pruebas de los repositorios afectados. Si la spec describe algo ya implementado, actualiza su estado y retira tareas cerradas; si el código no cumple el nuevo criterio, conserva la tarea pendiente.
- Las preguntas de dominio que todavía afecten un cambio se registran en la spec correspondiente. El [mapa de fuentes](../docs/fuentes.md) ofrece contexto cuando haga falta.
- Ejecuta `python3 scripts/spec_index.py --write` tras cambiar estados y `python3 scripts/spec_index.py --check` para validar el índice, las rutas y las tareas abiertas.
