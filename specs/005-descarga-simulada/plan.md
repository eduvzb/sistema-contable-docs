# Plan técnico — SPEC-005

La actualización de CA-005-01/02/04/07 de [spec.md](spec.md) se coordina con el [plan preliminar de SPEC-012](../012-descarga-masiva-sat/plan.md). Los contratos de confirmación, autorización y resultados siguen pendientes; no se fijan aquí endpoints ni esquemas alternativos.

- Trabajo centralizado: BE-012-09 y FE-012-06 para acceso exclusivo del administrador, advertencia y confirmación; BE-012-02/03 y FE-012-05 para integración con el importador común. No duplicar estas tareas en otra implementación.
- Conservar el comportamiento síncrono y los resultados vacío, parcial y de fallo controlado existentes, salvo los cambios expresamente acordados. No trasladar estados de la descarga real a la simulación.
- Probar petición directa de contador o sin confirmación rechazada, cancelar sin incorporaciones, simulación sin SAT/e.firma ni fallback, y continuidad de documentos previos en bandeja/pólizas para tipos permitidos.
- La primera etapa controlada de SPEC-012 fue autorizada y concentra la implementación compartida de esta actualización. No autoriza conexión real ni despliegue; la QA previa sólo acredita la versión anterior y el cierre nuevo requiere evidencia en [verificacion.md](verificacion.md).
