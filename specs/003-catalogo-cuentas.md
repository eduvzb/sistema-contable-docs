# SPEC-003 — Catálogo de cuentas

**Estado:** Borrador  
**Usuario:** Administrador o contador con empresa accesible  
**Dependencias:** [SPEC-001](001-acceso-usuarios-empresas.md), [SPEC-002](002-contexto-contable.md)

## Propósito y alcance

Administrar el catálogo propio de cada empresa: consultar, crear, editar, activar/desactivar cuentas e importar un catálogo inicial. Representar jerarquía conforme a OQ-001, sin fijar un máximo de niveles no documentado.

No incluye mapeo automático al catálogo SAT, patrones ni migración histórica. La importación inicial del catálogo sí está dentro del alcance.

## Fuentes

- [Alcance §8: catálogo](../docs/planeacion/003%20-%20MVP-Scope.md#8-cat%C3%A1logo-de-cuentas).
- [BR-001](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#3-br-001--toda-operaci%C3%B3n-pertenece-a-una-empresa), [BR-003](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#5-br-003--cada-empresa-tiene-su-propio-cat%C3%A1logo-de-cuentas), [BR-004](../docs/planeacion/005%20-%20Reglas%20de%20negocio.md#6-br-004--cada-partida-utiliza-una-cuenta-contable) (confirmadas).
- [OQ-001](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#3-oq-001--jerarqu%C3%ADa-de-cuentas-contables) (jerarquía provisional); [OQ-017](../docs/planeacion/006%20-%20Preguntas%20Abiertas.md#19-oq-017--migraci%C3%B3n) (migración completa posterior).

## Comportamiento y criterios de aceptación

El usuario operativo administra las cuentas de una empresa accesible y las deja disponibles para captura manual de partidas en SPEC-006. El administrador accede a cualquiera y el contador solo a sus asignadas, conforme a DT-008/SPEC-001. La jerarquía no define por sí sola qué niveles pueden recibir movimientos.

| ID | Dado / cuando | Resultado esperado |
|---|---|---|
| CA-003-01 | Se crea una cuenta con los datos que defina el contrato. | Queda en el catálogo de la empresa seleccionada y puede consultarse. |
| CA-003-02 | Se edita una cuenta existente de la empresa. | Se muestran los datos actualizados; la cuenta conserva su pertenencia empresarial. |
| CA-003-03 | Se activa o desactiva una cuenta. | Su condición se conserva y es consultable; el efecto sobre nuevos movimientos se debe decidir antes de Lista. |
| CA-003-04 | Se importan cuentas válidas según el formato que se concrete. | Quedan disponibles en el catálogo de la empresa, incluyendo las relaciones jerárquicas representadas en el formato. |
| CA-003-05 | Se relaciona una cuenta hija con una cuenta padre conforme a OQ-001. | La jerarquía se conserva y puede consultarse sin un máximo de niveles inventado. |
| CA-003-06 | Se intenta usar en una partida de A una cuenta que pertenece a B. | La operación no permite contabilizar con la cuenta ajena, conforme a BR-003. |
| CA-003-07 | Se intenta consultar o editar el catálogo de una empresa no asignada. | El backend impide el acceso y conserva los datos. |

## Pendientes y decisiones

- **Antes de Lista:** campos/códigos y unicidad; naturaleza de las cuentas necesaria para SPEC-008; niveles que reciben movimientos y efecto de inactividad sobre nuevas partidas; edición de cuentas ya utilizadas; formato de importación, duplicados, errores y resultado de lotes. Concretar integridad de la jerarquía (ciclos y referencias inválidas).
- **Supuesto para validar:** jerarquía sin máximo de niveles fijado, OQ-001. La observación del catálogo real debe cerrar las decisiones necesarias para captura y balanza.
- **Posterior:** catálogo SAT automático, migración de pólizas/saldos históricos y reglas de selección automática.

## Plan técnico y contratos

- Backend: operaciones de catálogo por empresa e importación con el formato acordado; define el contrato de consulta/selección de cuentas que consumen SPEC-006 y SPEC-008.
- Frontend: listado/jerarquía, formulario y carga de catálogo con resultado comprensible.
- Concretar fallos de importación y edición antes de escribir sus criterios de error definitivos; no asumir procesamiento asíncrono.

Aplican las [decisiones técnicas compartidas](../docs/decisiones.md). Los contratos aún no están cerrados: resolver los detalles necesarios antes de Lista, sin introducir reglas para completar huecos.

## Verificación

**Evidencia de producto:** pendiente; no ejecutada. No existe implementación vinculada todavía.

Prever cobertura de operaciones de catálogo, jerarquía e importación. Proteger BR-003 con pruebas de referencias a otra empresa tanto en catálogo como al registrar partidas.

Al implementar, registrar criterios cubiertos, prueba/comprobación, resultado, revisión de spec y referencias a backend/frontend. La revisión documental de esta entrega está en el [índice](README.md#verificaci%C3%B3n-documental).

## Cambios

- **2026-09-07:** primera redacción a partir de Planeación y del plan SDD autorizado. Se conservan supuestos y pendientes; no se declara comportamiento implementado.
- **2026-09-07:** se alineó el acceso operativo global del administrador con DT-008/SPEC-001, sin cambiar el alcance del catálogo.
