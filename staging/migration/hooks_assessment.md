# Evaluación de hooks

El candidato no configura hooks. Codex 0.152.0 admite eventos de hooks del ciclo de vida, tools, compaction y subagentes, pero la compatibilidad por sí sola no justifica la automatización.

| ÁREA | EVALUACIÓN | POSIBLE USO FUTURO | DECISIÓN ACTUAL |
|---|---|---|---|
| Ciclo de vida de sesión | USEFUL | Recordar o comprobar de forma determinista si el estado reanudable está obsoleto en límites relevantes | NOT YET REQUIRED; evitar escrituras obligatorias ruidosas |
| Eventos de tools | USEFUL WITH CARE | Bloquear una forma de comando/tool peligrosa y demostrada con precisión o ejecutar una comprobación determinista barata | NOT YET REQUIRED; no se ha demostrado una política universal y completa de comandos |
| Pre/Post compaction | USEFUL | Comprobar que las decisiones críticas/el estado actual se externalizaron antes de perder contexto | NOT YET REQUIRED; un hook no debe fabricar ni autoaceptar estado |
| Inicio/fin de subagente | USEFUL | Registrar procedencia acotada o exigir un resultado estructurado para workflows de proyecto específicos | NOT YET REQUIRED; evitar overhead de orquestación global |
| Mutación automática de contenido | DANGEROUS/AVOID | Reescribir registros, specs, contenido aprobado o run state sin revisión | AVOID |
| Remediación destructiva automática | DANGEROUS/AVOID | Limpieza, reset, migración, cambios de credenciales | AVOID |
| Acciones de hooks con red | DANGEROUS/AVOID por defecto | Notificaciones o actualizaciones externas | Exigir integración explícita, política de secrets, idempotencia y diseño de aprobación |

Un hook sólo se justifica cuando un fallo recurrente tiene evidencia, existe una comprobación determinista segura, se comprende el comportamiento de fallo y están definidos el rollback/ownership.
