# Arquitectura

bio-harness separa la orquestación, la mecánica determinista, el trabajo acotado de los modelos, el contexto privado del proyecto y la autoridad compartida del proyecto. El runtime es global; la metodología del proyecto permanece privada salvo que se promueva deliberadamente.

## Arquitectura completa del sistema

```mermaid
flowchart TB
    U["USUARIO"] --> O["SOL/MEDIUM ORCHESTRATOR"]

    subgraph GH["GLOBAL HARNESS"]
        O --> D["DIRECT"]
        O --> TB["TOOLBOX"]
        O --> LW["LUNA WORKERS"]
        LW --> R["researcher"]
        LW --> QI["quick-implementer"]
        LW --> I["implementer"]
        LW --> V["validator"]
        O --> SP["SOL PREMIUM"]
        SP --> P["planner"]
        SP --> RV["reviewer"]
    end

    subgraph PC["CONTEXTO DEL PROYECTO"]
        ST["PROJECT SHARED TRUTH"]
        PS["PRIVATE .ai STATE"]
    end

    HG["HUMAN GATES"] --> O
    ST --> O
    PS -. "complementa; no invalida" .-> O
    D --> VA["VALIDATION"]
    TB --> VA
    LW --> VA
    SP --> VA
    VA --> O
```

El orquestador interpreta, enruta e integra. `researcher`, `quick-implementer`, `implementer` y `validator` cubren trabajo Luna acotado; `planner` y `reviewer` reservan Sol para razonamiento con consecuencias relevantes. La verdad compartida gobierna el proyecto, `.ai` aporta contexto privado, los human gates resuelven límites de autoridad y toda afirmación final depende de validación.

## Global, blueprint y proyecto

```mermaid
flowchart TB
    B["bio-harness"] --> G["GLOBAL RUNTIME"]
    B --> BL["BLUEPRINT REUTILIZABLE"]
    B --> P["PROJECT STATE"]

    subgraph GLOBAL["GLOBAL"]
        G --> G1["AGENTS.md · routing · agents"]
        G --> G2["toolbox · config/runtime integration"]
    end

    subgraph BLUEPRINT["BLUEPRINT"]
        BL --> B1["assets de project-bootstrap"]
        BL --> B2["plantillas .ai · SDD · tools"]
    end

    subgraph PROJECT["PROJECT"]
        P --> P1[".ai/PROJECT.md · specs · state"]
        P --> P2["mistakes · tools · audit/progress"]
    end

    BL -. "no instancia automáticamente" .-> P
```

Staging contiene fuente y posibilidades inertes. Que exista el blueprint no crea `.ai`, specs, registros ni tools en ningún repositorio: `project-bootstrap` inspecciona primero y sólo activa lo necesario con la autoridad adecuada.

## Ciclo de vida de una solicitud

```mermaid
flowchart TD
    R["REQUEST"] --> U["Comprender requisitos"]
    U --> A["Evaluar riesgo, autoridad y complejidad"]
    A --> S{"Seleccionar ruta"}
    S --> D["DIRECT"]
    S --> T["TOOL"]
    S --> W["WORKER"]
    S --> P["PREMIUM ROLE"]
    S --> H["HUMAN GATE"]
    H --> X["Ejecutar alcance aprobado"]
    D --> X
    T --> X
    W --> X
    P --> X
    X --> V["Validar"]
    V --> E{"¿Evidencia suficiente?"}
    E -->|Sí| I["Integrar evidencia"]
    I --> O["Informar resultado"]
    E -->|No| F["Conservar fallo y reparar o escalar"]
    F --> A
```

El reintento vuelve a la evaluación con evidencia nueva. No reinicia a ciegas ni prueba primero un modelo débil cuando el riesgo ya justifica un rol premium.

## Estado y autoridad

```mermaid
flowchart LR
    S["Repositorio fuente"] --> I["Instalador validado"]
    I --> G["Runtime global<br/>AGENTS, routing, agents, toolbox, skill"]
    G --> P["Sesión del proyecto"]
    B["Blueprint privado"] --> PB["project-bootstrap adaptativo"]
    PB --> AI["Workspace privado .ai"]
    H["Verdad compartida con seguimiento"] --> P
    AI --> P
    AI -. "no puede invalidar" .-> H
```

- **Runtime global**: el pequeño acuerdo siempre cargado, la política de enrutamiento bajo demanda, las definiciones explícitas de agentes, el soporte de toolbox global y la skill project-bootstrap.
- **Blueprint/fuente**: candidatos y plantillas inertes y versionados bajo `staging/`; su presencia no los instala ni activa.
- **Estado privado del proyecto**: artefactos `.ai/` seleccionados y creados sólo después de inspeccionar el proyecto y establecer privacidad local segura.
- **Verdad compartida del proyecto**: instrucciones, contratos, código fuente, tests, arquitectura y documentación del equipo con seguimiento. Las contradicciones con `.ai` se hacen visibles y se resuelven según la autoridad compartida aplicable, salvo que un humano cambie ese contrato.

## Divulgación progresiva

```mermaid
flowchart TD
    A["SIEMPRE: global AGENTS"] --> N{"Necesidad de la tarea"}
    N --> PR["project router"]
    N --> RP["routing policy"]
    N --> SP["spec relevante"]
    N --> TM["tool manifest"]
    N --> AI["agent instructions"]
    N --> IS["código fuente relevante"]
    N --> AE["evidencia de auditoría"]
    TS["Ahorro de tokens"] -. "nunca elimina" .-> C["restricciones · contratos · autoridad · evidencia de fallos"]
```

Sólo se cargan capas profundas cuando aportan algo a la tarea. El `AGENTS.md` global permanece pequeño; specs, manifests, implementación y evidencia se leen bajo demanda. Ahorrar contexto nunca justifica omitir un requisito crítico o un límite de aprobación.

## Ciclo de vida de fuente a runtime

Los cambios comienzan en staging, pasan una validación determinista y una revisión proporcional y después atraviesan la migración basada en hashes. La instalación V2 ordinaria deja deliberadamente `config.toml` sin cambios. La migración del modelo parent es una operación separada y vinculada a evidencia.
