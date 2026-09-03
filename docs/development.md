# Desarrollo y tests

Desarrolla sobre la fuente en staging. No edites la instalación activa `~/.codex` ni `~/.agents` para crear un prototipo de un cambio.

## Cambios habituales

- Acuerdo de trabajo global: edita `staging/global/codex/AGENTS.md` y conserva su pequeño presupuesto de carga permanente.
- Rol de agente: edita el archivo correspondiente bajo `staging/global/codex/agents/`; fija explícitamente el modelo, el reasoning effort y el sandbox.
- Enrutamiento: edita `staging/global/codex/routing/MODEL_ROUTING.md`; mantenlo bajo demanda en lugar de importarlo globalmente.
- project-bootstrap: edita `staging/global/agents/skills/project-bootstrap/` y mantén sus assets autosuficientes y sincronizados con el blueprint cuando la validación exija paridad.
- Blueprint de proyecto: edita `staging/blueprint/project/`; trátalo como un menú de activación.
- Sistema de toolbox: edita `staging/global/codex/toolbox/_system/`. Las herramientas reutilizables nuevas necesitan contratos semánticos estrechos, tests y un alcance justificado; se prefieren las herramientas de proyecto hasta que se apruebe su promoción global.

## Validación determinista

Ejecuta el entry point unificado del repositorio desde la raíz:

```bash
python3 -B staging/audit/validate_staging.py
```

Ejecuta los tests unificados de política e infraestructura, la validación de evidencia de calidad, la validación de project-bootstrap, los tests de toolbox, los tests de privacidad, las comprobaciones de presupuesto, las comprobaciones de paridad de candidatos y las simulaciones de migración. No ejecuta benchmarks de modelos de pago ni instala el harness.

Antes de la revisión o del commit, ejecuta también:

```bash
git diff --check
```

Inspecciona las rutas modificadas y el conjunto exacto en staging. Para documentación, verifica que los enlaces relativos resuelvan y que los fences de Mermaid estén equilibrados. No instales una dependencia sólo para estas comprobaciones ligeras.

## Calidad y revisión

Los cambios de modelo o prompt que afecten una asignación aprobada requieren fixtures representativas del rol. Un cambio de parent propuesto requiere primero un control Sol/medium y no puede aprobarse con una regresión de seguridad, una regresión material de enrutamiento sin resolver o una regresión material de calidad repetida. Se comparan los resultados, no la igualdad de la prosa.

Usa un reviewer de read-only para arquitectura, migración, seguridad, contratos públicos o cambios sustanciales acumulados. Revisa la fuente y la evidencia antes de instalar. La instalación debe utilizar la [migración transaccional](installation.md), crear backups verificados y someterse a una revisión separada posterior a la instalación.

Los resultados de auditoría pertenecen a `staging/audit/`; las explicaciones estables pertenecen a `docs/`. Nunca sustituyas evidencia conservada de pruebas por un resumen sin respaldo.
