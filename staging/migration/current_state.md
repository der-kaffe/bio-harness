# Estado activo y en staging actual

El preflight V2 original y autoritativo es `../audit/v2_preflight_baseline.md`; la instalación completada está registrada en `../audit/HARNESS_V2_HYBRID_INSTALL_20260902T231047Z.md`. Codex 0.152.0 activo usa `gpt-5.6-sol` con razonamiento medium, workspace-write, aprobaciones on-request, memories deshabilitadas, la capacidad multi-agent existente y el soporte validado de la toolbox global.

La fuente unificada en staging define el enrutamiento privado `.ai` de proyectos, una toolbox dirigida por manifests, seis roles con pins explícitos, una política bajo demanda de enrutamiento que prioriza la calidad, tests deterministas de infraestructura y evidencia de calidad conservada. El researcher instalado es Luna/medium; el validator es Luna/low con protecciones explícitas para sólo skips y mutación de fuente. El `config.toml` en staging conserva Sol/medium. `config.luna-candidate.toml` es inerte, falló su quality gate y no puede activarse mediante la migración V2 general.

Los documentos anteriores de auditoría y simulación siguen siendo evidencia histórica de V1 y no deben invalidar este baseline V2 actual.
