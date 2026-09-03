# Activación del workspace privado

Clasifica las rutas existentes y propuestas como `REUSE`, `ADAPT`, `MIGRATION_PROPOSED`, `CONFLICT` o `SKIP`. Mover o eliminar un layout antiguo requiere aprobación explícita.

| Artefacto | Activar sólo cuando |
|---|---|
| `.ai/PROJECT.md` | El enrutamiento privado aporta una ayuda material; mantenlo como un mapa pequeño. |
| `.ai/run_state.md` | El trabajo abarca varias sesiones y Git/issues no proporcionan un checkpoint suficiente. |
| `.ai/handoff.md` | Se está produciendo una transferencia real. |
| `.ai/mistakes.md` | Reaparece un fallo sustancialmente equivalente del agente/proceso. |
| `.ai/audit/` | Una auditoría acotada compara la evidencia esperada con la actual. |
| `.ai/progress/` | Las conclusiones relevantes aún no quedan claras en Git/issues. |
| `.ai/specs/<feature>/` | La ambigüedad, el riesgo o la durabilidad justifican SDD privado. |
| `.ai/state/` | El estado operativo privado estructurado tiene un responsable y un ciclo de vida definidos. |
| `.ai/tools/<name>/` | El trabajo mecánico determinista reutilizable supera la heurística de extracción. |

Usa `SKIP` de forma predeterminada. Los elementos existentes `ai/`, `specs/`, `.agents/`, `.codex/` o `AGENTS.md` en el root pueden ser compartidos, privados o legacy; inspecciona su seguimiento y autoridad antes de clasificarlos.
