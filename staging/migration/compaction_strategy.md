# Estrategia de compaction

Mantén los valores predeterminados de compaction de Codex 0.152.0. Por ahora no se justifica ningún threshold de tokens, alcance, prompt ni hook de compaction personalizado.

Regla metodológica: **la información duradera debe externalizarse antes de que la pérdida de contexto sea relevante**.

- Los hechos críticos pertenecen al registro source-of-truth.
- Las elecciones aceptadas/propuestas pertenecen al decision register.
- El comportamiento requerido pertenece a las especificaciones.
- El trabajo actual reanudable pertenece al run state.
- La historia completada relevante pertenece a progress.

Los resúmenes de conversación y el output de compaction ayudan a navegar, no son almacenamiento autoritativo. Un futuro hook previo a compaction sólo podrá evaluarse si evidencia repetida demuestra que las sesiones pierden estado crítico reanudable y una comprobación segura, que no fabrique información, puede detectar esa condición. No debe autoaceptar decisiones ni sobrescribir contenido humano.
