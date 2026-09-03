# Workspace privado del proyecto

`.ai/` existe para el coding agent de una persona. Es privado de forma predeterminada y no se convierte automáticamente en autoridad del proyecto o del equipo.

```text
.ai/
├── PROJECT.md
├── specs/
├── state/
├── run_state.md
├── handoff.md
├── mistakes.md
├── audit/
├── progress/
└── tools/
```

Esto es un menú. Un repositorio trivial puede no recibir nada; otro quizá sólo necesite `.ai/PROJECT.md`. No se instalan directorios vacíos ni blueprints completos por ceremonia.

## Enrutador y autoridad

`.ai/PROJECT.md` es un pequeño mapa de artefactos privados activos. Sólo debe enlazar specs, estado o manifests de herramientas privados y relevantes para la tarea; no debe duplicar el README, el `AGENTS.md` con seguimiento, los requisitos de producto, la arquitectura ni los comandos del equipo.

```mermaid
flowchart TD
    U["INSTRUCCIÓN HUMANA EXPLÍCITA"] --> T["FUENTE COMPARTIDA APLICABLE<br/>AGENTS · contratos · código · tests · docs"]
    T --> D["TRABAJO DEL PROYECTO"]
    P["GUÍA PRIVADA .ai"] -. "complementa" .-> D
    P -. "si contradice, se informa" .-> T
    E["EVIDENCIA DEL REPOSITORIO<br/>demuestra qué existe"] --> D
```

La instrucción humana actual y la fuente compartida con seguimiento más cercana y aplicable gobiernan el objetivo. La evidencia del repositorio establece la realidad actual, pero no redefine por sí sola el contrato deseado. `.ai` complementa esas fuentes; las contradicciones se informan y no se resuelven silenciosamente a favor del estado privado.

## Privacidad local de Git

En repositorios Git, project-bootstrap resuelve tanto el root como la ruta de exclude:

```bash
git rev-parse --show-toplevel
git rev-parse --git-path info/exclude
```

Comprueba `git ls-files -- .ai .codex .agents` antes de añadir las exclusiones ancladas que falten para `/.ai/`, `/.codex/` y `/.agents/`. Conserva el contenido existente del exclude. Nunca edita el `.gitignore` con seguimiento, deja de seguir archivos, reescribe el historial ni supone que `.git/info/exclude` sea la ubicación resuelta.

Las rutas privadas aparentes que tengan seguimiento son un conflicto, no algo que una exclusión pueda ocultar. Los elementos existentes `ai/`, `specs/`, `.agents/`, `.codex/`, `.ai/` o un `AGENTS.md` raíz deben clasificarse según su seguimiento y autoridad, no según sus nombres.

## Promoción

Cuando el trabajo privado revela algo que los colaboradores necesitan, propón su promoción: explica la necesidad compartida, usa la convención de documentación existente en el repositorio y obtén aprobación cuando el cambio afecte un contrato del equipo o producto. El SDD privado nunca se copia automáticamente a documentación con seguimiento.

```mermaid
flowchart LR
    F["PRIVATE FINDING"] --> P["PROPOSE PROMOTION"]
    P --> D["HUMAN / TEAM DECISION"]
    D -->|Aceptada| S["SHARED DOCUMENTATION"]
    D -->|No aceptada| R["Permanece privada"]
```

La promoción es una decisión explícita, no una consecuencia automática de que el hallazgo parezca útil.

## Escalamiento de errores recurrentes

```mermaid
flowchart LR
    F["FALLO RECURRENTE"] --> I["prompt / instruction"]
    I --> M["memory / skill"]
    M --> T["script / tool"]
    T --> C["test / static check"]
    C --> E["hook / CI / policy"]
```

No todos los fallos recorren toda la cadena: el control se elige según la causa, la repetibilidad y el riesgo. `memory` es sólo una opción futura y sigue deshabilitada en la configuración V2 actual. La repetición puede justificar automatizar la **prevención**, pero nunca concede autoridad automática para ejecutar acciones peligrosas.
