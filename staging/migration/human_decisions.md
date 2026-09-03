# Decisiones humanas aún necesarias

1. Aprobar o rechazar el candidato V2 unificado en staging después de resolver los findings del quality red-team.
2. Autorizar los targets activos exactos y el baseline de migración para V2 general. Esto instala el enrutamiento de workspace privado, seis roles explícitos, soporte de toolbox y project-bootstrap V2, pero no cambia el modelo parent.
3. Decidir si cada proyecto real debe adoptar un workspace privado `.ai`. La adopción de proyectos es separada y específica para cada ruta; ningún proyecto se inicializa globalmente.
4. Aprobar cualquier migración de una ruta antigua del harness local al proyecto después de revisar su mapa `REUSE`, `ADAPT`, `MIGRATION_PROPOSED`, `CONFLICT` o `SKIP`.
5. Ejecutar y revisar el benchmark de calidad representativo del control Sol/medium y el candidato Luna/medium.
6. Sólo si pasa el quality gate, autorizar por separado la migración reversible del modelo parent a Luna/medium. Un fallo conserva Sol/medium como el resultado V2 compatible correcto.
7. Aprobar de forma independiente cada promoción de tools desde el proyecto al ámbito global; las tools globales que mutan requieren aprobación humana explícita.
