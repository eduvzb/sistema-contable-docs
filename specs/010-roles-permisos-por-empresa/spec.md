# SPEC-010 — Roles y permisos por empresa

- **Estado:** Borrador
- **Actualizado:** 2026-10-26
- **Criterios de esta entrega:** CA-010-01, CA-010-02, CA-010-03
- **Usuario:** Administrador y usuarios asignados a una empresa
- **Dependencias:** [SPEC-001 — Acceso, usuarios y empresas](../001-acceso-usuarios-empresas/spec.md)

## Objetivo

Permitir que el acceso de cada usuario a una empresa dependa de un rol predefinido y de los permisos de ese rol. La autorización debe aplicarse en el backend y la interfaz debe mostrar sólo las acciones permitidas.

## Alcance

- Incluye: roles predefinidos, permisos por módulo y acción, asignación de roles por empresa y aplicación de permisos en las operaciones existentes.
- No incluye: roles creados por clientes ni cambios al inicio de sesión, contraseñas o sesiones ya cubiertos por SPEC-001.

## Requisitos funcionales y criterios de aceptación

| ID | Situación | Qué ocurre |
|---|---|---|
| CA-010-01 | Un usuario consulta o realiza una acción en una empresa donde tiene un rol asignado. | El acceso se permite únicamente si el rol asignado incluye el permiso requerido para ese módulo y acción. |
| CA-010-02 | Un usuario intenta consultar o ejecutar una acción sin el permiso requerido, incluso mediante una petición directa. | El backend rechaza la operación y no expone ni modifica datos protegidos; la interfaz no ofrece la acción que el usuario no puede realizar. |
| CA-010-03 | Un administrador asigna o cambia el rol de un usuario para una empresa. | El cambio queda asociado a esa empresa y no concede acceso a otras empresas. |

## Preguntas abiertas

- **Bloquea CA-010-01/02:** ¿Qué roles predefinidos existirán y qué módulos y acciones podrá realizar cada uno? Se acordó que los permisos serán por módulo y acción, pero falta la matriz concreta.
- **Bloquea CA-010-01/03:** ¿El administrador global actual conserva acceso total y puede asignar roles, además de los roles por empresa? Definir también cómo se migran los usuarios actuales `admin` y `accountant` sin ampliar ni retirar acceso inesperadamente.
- **Bloquea CA-010-03:** ¿Qué respuesta y protección se requieren al quitar o cambiar un rol mientras el usuario mantiene una sesión abierta?

## Fuentes

- [SPEC-001 — Acceso, usuarios y empresas](../001-acceso-usuarios-empresas/spec.md)
- Backend actual: `UserRole`, `UserPolicy`, `CompanyPolicy` y políticas de los módulos contables.
- Frontend actual: contrato `User.role` y controles de interfaz basados en `admin` / `accountant`.
