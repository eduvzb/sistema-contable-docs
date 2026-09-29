# Constitución del proyecto

**Estado:** Activa. Define principios duraderos, no funcionalidades, tecnologías ni pasos operativos.

## Principios

1. **Entender antes de construir.** Definir problema, resultado esperado y forma de comprobarlo antes de adoptar una solución.
2. **Aclarar lo pendiente.** Distinguir requisitos acordados, supuestos por validar e incógnitas que bloquean el siguiente cambio.
3. **Preferir simplicidad.** Introducir complejidad solo para necesidades demostradas, no para posibilidades futuras.
4. **Asignar responsabilidades claras.** Cada comportamiento debe tener un responsable reconocible y límites comprensibles.
5. **Comprobar la realidad del producto.** El código y las pruebas indican el comportamiento implementado; las specs describen el cambio esperado. Resolver sus diferencias antes de modificar el producto.
6. **Poder verificar la correctitud.** Contrastar resultados con lo esperado, hacer visibles los errores y no normalizar fallos conocidos.
7. **Cambiar intencionalmente.** Explicar qué cambia, por qué y cómo se verificará. Mantener las excepciones explícitas y limitadas.

## Cómo resolver diferencias

Para responder qué hace el producto hoy, consulta implementación y pruebas de backend y frontend. Para cambiarlo, usa la instrucción actual del usuario y los criterios de la spec; si faltan reglas de negocio, acláralas antes de codificar. La documentación de dominio aporta contexto, pero no convierte una idea antigua en comportamiento obligatorio. El [mapa de fuentes](fuentes.md) orienta esa consulta.

Cambiar un principio es excepcional: debe identificarse el principio, explicar por qué dejó de ser adecuado y dejar constancia del cambio. Las necesidades puntuales no justifican modificar esta constitución.
