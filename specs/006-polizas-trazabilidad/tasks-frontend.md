# Tareas de frontend — SPEC-006

Los criterios y el estado vigentes están en [spec.md](spec.md). El [plan técnico](plan.md) define contratos y dependencias; los resultados ejecutados se registran en [verificacion.md](verificacion.md).

- [ ] **FE-006-01 — Mover la búsqueda y selección múltiple a la ventana «CFDI relacionados», con orden de selección y vínculos previos visibles.**
  - CA: CA-006-19 revisado y CA-006-20.
  - Depende de: contrato de CFDI del periodo disponible.
  - Hecho cuando: La ventana filtra sólo los CFDI elegibles del periodo, conserva selecciones y relaciones anteriores de otros periodos, y «Continuar» no guarda la póliza; pruebas de componentes pasan.

- [ ] **FE-006-02 — Consumir las propuestas y presentar bloques editables por CFDI, junto con errores identificados por UUID.**
  - CA: CA-006-21/22.
  - Depende de: BE-006-01 y FE-006-01.
  - Hecho cuando: El usuario puede corregir importes y completar cuentas; los CFDI inválidos no impiden continuar con los válidos y la póliza no se guarda al continuar; pruebas de componentes pasan.

- [ ] **FE-006-03 — Aplicar sugerencias de cuentas y propagar al mismo emisor sólo a partidas equivalentes todavía vacías.**
  - CA: CA-006-23/24.
  - Depende de: BE-006-02 y FE-006-02.
  - Hecho cuando: Las elecciones manuales y los importes se conservan; los orígenes se envían al guardar; pruebas de componentes y regresiones pasan.
