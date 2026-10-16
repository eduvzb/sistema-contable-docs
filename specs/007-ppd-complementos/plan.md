# Plan técnico — SPEC-007

## Entrega CA-007-05

Convertir las relaciones ya autorizadas del detalle fiscal en acciones para consultar la factura o complemento dentro del diálogo existente, incluso de otro periodo. Reutilizar GET de detalle por empresa e ID; referencias no importadas conservan su aviso sin acción. No cambia asignaciones, importes ni contratos backend.

Las respuestas tardías tras cerrar, cambiar empresa/periodo o abrir otro documento se descartan. Una carga fallida informa el error y permite reintentar. Vitest y React Testing Library verifican navegación factura/complemento, referencias pendientes, error y respuestas tardías. La aprobación humana anterior se conserva para el alcance previo; la interacción nueva requiere QA humana.
