# Decisiones vigentes

Registro único para acuerdos compartidos. Las decisiones limitadas a una funcionalidad viven en su spec. Para cambiar un acuerdo, registrar fecha, motivo, qué reemplaza y specs afectadas; no crear un ADR por cada tarea.

| ID | Decisión | Procedencia |
|---|---|---|
| DT-001 | Backend: Laravel, PostgreSQL y Laravel Sanctum. Frontend: Next.js, TypeScript, pnpm y App Router. No se fijan versiones sin preparar la implementación. | AGENTS.md previo a esta reorganización. |
| DT-002 | Backend y frontend viven en repositorios independientes. Este repositorio mantiene las specs compartidas; ambos consumidores referencian su ID y revisión Git. | AGENTS.md original y plan autorizado. |
| DT-003 | Backend: negocio, validación autoritativa, autorización, persistencia y contratos API. Frontend: presentación, interacción, flujos y estado de interfaz; puede representar reglas del backend sin convertirse en autoridad independiente. | AGENTS.md original. |
| DT-004 | Los valores monetarios usan decimales adecuados; no usar punto flotante cuando pueda perderse precisión. Precisión, escala, redondeo y representación API se concretan al preparar las specs afectadas y se registran aquí si son compartidos. | AGENTS.md original; detalle todavía no decidido. |
| DT-005 | Preferir capacidades naturales del framework. Dependencias, Redis, colas, cachés y workers requieren una necesidad concreta; no son infraestructura obligatoria por defecto. | AGENTS.md original. |
| DP-001 | Documentación vigente centralizada aquí; una spec por funcionalidad, con preparación progresiva y verificación en el mismo archivo. | Plan autorizado por el usuario. |
| DP-002 | El MVP vigente lo delimitan alcance, reglas y decisiones provisionales de Planeación según el [mapa de fuentes](fuentes.md). El análisis inicial y las guías no agregan funcionalidades. | Plan autorizado y documentos de Planeación. |
| DT-006 | La primera implementación usa Laravel 13 con PHP 8.4 y Sanctum en backend, PostgreSQL 18 mediante Sail, y Next.js 16 con TypeScript, App Router, Tailwind CSS y pnpm sobre Node 22 en frontend. Los bloqueos fijan versiones instaladas. | Instrucción explícita del usuario para SPEC-001, 2026-09-07. |
| DT-007 | La aplicación propia usa el modo SPA de Sanctum con sesión en cookie HttpOnly, protección CSRF y frontend/API bajo dominio compartido; Laravel es la autoridad de autenticación y autorización. | Instrucción explícita del usuario para SPEC-001 y documentación oficial de Sanctum. |
| DT-008 | Existen solo los roles `admin` y `accountant` en el MVP. El administrador tiene acceso operativo a todas las empresas; el contador solo a las asignadas. Las funcionalidades consumidoras de SPEC-001 aplican esta misma política. | Instrucción explícita del usuario para SPEC-001, 2026-09-07. |
| DT-009 | Los catálogos fiscales necesarios se conservan versionados con procedencia y fecha y se consumen sin depender de SAT en tiempo de ejecución. SPEC-001 inicia esta regla con `c_RegimenFiscal`. | Instrucción explícita del usuario para SPEC-001, 2026-09-07. |
| DT-010 | El contexto contable se identifica explícitamente por empresa y periodo en URLs y contratos API; no se conserva una selección autoritativa implícita en la sesión del backend. El frontend puede recordar el último contexto como conveniencia, pero debe validarlo nuevamente contra la API. | Instrucción explícita del usuario para SPEC-002, 2026-09-07. |
| DT-011 | Los importes contables y fiscales del MVP se almacenan con seis decimales y se representan como texto en contratos JSON para no perder precisión; no se aplica conversión monetaria avanzada. | Decisión explícita al preparar SPEC-004 y SPEC-006, 2026-09-08. |

## Registro de cambios

- **2026-09-07:** se trasladaron DT-001 a DT-005 desde AGENTS.md sin introducir arquitectura adicional. Se registraron DP-001 y DP-002 y la simplificación constitucional autorizada. Los detalles aún no definidos permanecen pendientes; no se aprobaron reglas contables nuevas.
- **2026-09-07:** se registraron DT-006 a DT-009 al preparar SPEC-001: versiones, autenticación SPA, roles/acceso y catálogo fiscal local.
- **2026-09-07:** se registró DT-010 al preparar SPEC-002: contexto explícito y memoria local no autoritativa.
- **2026-09-08:** se registró DT-011 para compartir precisión y representación de importes entre documentos fiscales y pólizas.
