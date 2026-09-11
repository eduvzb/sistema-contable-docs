# Constitución del proyecto

**Estado:** Activa. Define principios duraderos, no funcionalidades, tecnologías ni pasos operativos.

## Principios

1. **Entender antes de construir.** Definir problema, resultado esperado y forma de comprobarlo antes de adoptar una solución.
2. **Decidir explícitamente.** Distinguir decisiones, supuestos e incógnitas; conservar la razón de las decisiones importantes.
3. **Preferir simplicidad.** Introducir complejidad solo para necesidades demostradas, no para posibilidades futuras.
4. **Asignar responsabilidades claras.** Cada comportamiento debe tener un responsable reconocible y límites comprensibles.
5. **Mantener una fuente de verdad.** Identificar la definición vigente y sus fuentes; evitar versiones contradictorias y reinterpretaciones silenciosas.
6. **Poder verificar la correctitud.** Contrastar resultados con lo esperado, hacer visibles los errores y no normalizar fallos conocidos.
7. **Cambiar intencionalmente.** Explicar qué cambia, por qué y qué decisión reemplaza; conservar lo que no se pretende modificar. Toda excepción debe ser explícita, justificada y limitada; si se vuelve habitual, revisar la regla.

## Autoridad y cambios

La jerarquía se conserva: **Constitución → decisiones vigentes → specs vigentes → documentación de dominio → diseño → implementación**.

Una fuente inferior no modifica silenciosamente una superior. La precedencia no autoriza a inventar reglas en una spec: cualquier cambio de dominio debe registrarse explícitamente y actualizar su fuente. Un borrador no sustituye una decisión vigente.

Las contradicciones se resuelven en la fuente responsable antes de implementar el comportamiento afectado. El [mapa de fuentes](fuentes.md) distingue alcance, reglas, supuestos y material de apoyo.

Cambiar un principio es excepcional: debe identificarse el principio, explicar por qué dejó de ser adecuado y dejar constancia del cambio. Las necesidades puntuales no justifican modificar esta constitución.
