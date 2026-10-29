# Plan técnico — SPEC-001

## Actualización pendiente: editar datos de empresa

- Añadir `PUT /api/companies/{companyId}` con `legal_name`, `commercial_name` y `tax_regime_code`; no aceptar `rfc` ni `account_template_version`. Responder con `CompanyResource`. Reutilizar normalización y validación actuales; el régimen debe pertenecer al catálogo vigente.
- Autorizar administrador o contador con asignación vigente. Buscar empresa mediante el alcance visible actual: empresa inexistente o no visible responde `404`; un campo inválido responde `422` y no deja cambios parciales.
- En el frontend, añadir una acción **Editar empresa** al contexto de empresa seleccionada y reutilizar campos del formulario, precargando datos no secretos. RFC visible pero deshabilitado. El reemplazo de FIEL se especifica y verifica por separado en SPEC-012.
- Pruebas backend de roles/acceso revocado, rechazo de cambios al RFC, normalización, régimen inválido y persistencia atómica. Pruebas de componentes e interacción frontend para abrir, precargar, guardar, cancelar y mostrar errores; Vitest y React Testing Library.

Cuando se solicite una modificación, contrasta el requisito con la implementación, define aquí únicamente los contratos y riesgos nuevos, y crea tareas verificables en [backend](tasks-backend.md) o [frontend](tasks-frontend.md). Registra el cierre de esa entrega en [verificacion.md](verificacion.md).
