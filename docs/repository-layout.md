# Estructura del repositorio

Este repositorio versiona la fuente reproducible del harness y su evidencia. Los homes activos de runtime y los backups de la máquina no son fuente.

```text
bio-harness/
├── README.md
├── .github/workflows/validate.yml # Validación determinista en push/PR
├── docs/                       # Guías de arquitectura y operación dirigidas a usuarios
├── staging/
│   ├── global/
│   │   ├── codex/              # AGENTS, agents, routing, config, rules y toolbox globales
│   │   └── agents/             # Fuente autosuficiente de la skill project-bootstrap
│   ├── blueprint/project/      # Menú inerte y activado progresivamente para proyectos privados
│   ├── migration/              # Instalación, rollback y migración opcional del parent en V2
│   └── audit/                  # Tests deterministas, fixtures, resultados de calidad y procedencia
├── migration-execution/        # Programa histórico de migración V1
└── .gitignore                  # Excluye backups de la máquina y residuos generados
```

## Clases del ciclo de vida

| Área | Clase | Propósito |
|---|---|---|
| `README.md`, `docs/` | Documentación | Entry points estables para usuarios y maintainers |
| `.github/workflows/validate.yml` | CI | Ejecuta invariantes deterministas sin instalar el harness ni llamar modelos |
| `staging/global/` | Fuente / staging | Archivos candidatos globales instalables; inertes hasta su migración |
| `staging/blueprint/` | Blueprint | Plantillas privadas opcionales del proyecto, nunca política aplicada en bloque |
| `staging/migration/` | Fuente de migración | Instalación basada en hashes, rollback y cambio de modelo sujeto a gate |
| `staging/audit/test_v2.py` y validators | Test | Validación estructural y de políticas determinista |
| `staging/audit/fixtures/`, `quality/` | Test / auditoría | Fixtures de escenarios, evidencia conservada de pruebas y resultados de gates |
| Otros registros en `staging/audit/` | Auditoría / histórico | Baselines, revisiones, procedencia y evidencia de instalación |
| `migration-execution/` | Histórico | Fuente de migración anterior conservada como procedencia, no como guía V2 |

`backups/`, el estado generado de simulaciones, las cachés de Python, los archivos temporales y los snapshots anteriores al bootstrap son exclusivamente locales. La evidencia detallada de auditoría puede contener rutas absolutas históricas; la documentación general evita depender de ellas.
