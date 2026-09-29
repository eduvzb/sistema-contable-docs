# Fuentes de contexto

El código y las pruebas de backend y frontend muestran el comportamiento implementado. Las [specs](../specs/README.md) describen cambios solicitados y criterios para nuevas entregas. Los documentos de Planeación ayudan a entender el dominio y a descubrir preguntas; no reemplazan la observación del producto ni convierten propuestas antiguas en trabajo autorizado.

| Fuente | Uso al preparar cambios |
|---|---|
| [Alcance del producto](planeacion/003%20-%20Alcance%20del%20producto.md) | Capacidades y límites actualmente descritos. Contrastar cada afirmación con código y la spec responsable. |
| [Reglas de negocio](planeacion/005%20-%20Reglas%20de%20negocio.md) | Identificar restricciones contables y fiscales que afectan el cambio. |
| [Escenarios contables](planeacion/004%20-%20Escenarios%20contables.md) | Derivar ejemplos verificables y casos límite. |
| [Preguntas abiertas](planeacion/006%20-%20Preguntas%20Abiertas.md) | Localizar cuestiones aún por resolver para ampliaciones futuras. |
| [Glosario](planeacion/002%20-%20Glosario.md) | Aclarar términos; una entidad mencionada no obliga a implementarla. |
| [Análisis inicial](planeacion/001%20-%20An%C3%A1lisis%20Inicial%20del%20Proyecto.md) y [guías](planeacion/00%20-%20Inicio.md) | Contexto y ejemplos, sin autoridad sobre el código actual. |

Cuando una fuente contradiga el comportamiento existente, identifica el caso exacto en código y pruebas. Si el usuario solicita cambiarlo, redacta primero el resultado esperado en la spec; si falta una regla de dominio, deja la duda explícita antes de implementar. Git conserva las versiones anteriores de esta documentación.
