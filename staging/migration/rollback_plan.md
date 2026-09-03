# Rollback del Harness V2

El rollback restaura los bytes exactos registrados antes de la instalación, no contenido reconstruido.

Para la instalación V2 general:

1. Detente y conserva la evidencia del fallo y el journal de estado duradero.
2. Valida la versión del manifest, el universo de targets registrado y los roots exactos de Codex/agents.
3. Para cada acción preparada o completada, en orden inverso, reconcilia el target actual con sus hashes anterior/instalado.
4. Restaura los archivos existentes desde backups verificados y con sus modos originales.
5. Elimina los archivos recién creados sólo cuando sigan coincidiendo con el hash candidato; después elimina los directorios creados por la instalación sólo si están vacíos.
6. Restaura archivos project-bootstrap obsoletos sólo cuando su target registrado siga ausente.
7. Conserva e informa cualquier edición humana posterior en vez de sobrescribirla.
8. Verifica AGENTS global, routing, agents, toolbox, project-bootstrap, el hash agregado de skills no relacionadas y que la config no haya cambiado.

El rollback nunca cambia un proyecto, el exclude de Git, `.gitignore`, la configuración global de Git, auth, memory ni skills no relacionadas.

La migración opcional del parent Luna tiene su propio comprobante de quality gate, journal duradero de migración y backup. Un humano aprueba el hash exacto del comprobante del gate. Apply vuelve a validar su evaluator, fixtures, resultados y hashes de candidate-config antes de registrar `PREPARED`; rollback gestiona estados prepared y committed y rechaza drift no relacionado. El fallo o rollback de este paso opcional no elimina workers, tools, routing ni project-bootstrap del Harness V2.
