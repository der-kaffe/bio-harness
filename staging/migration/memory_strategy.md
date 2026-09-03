# Estrategia futura de memory

El candidato no habilita memory.

## Contenido adecuado para memory

- Preferencias personales estables que se aplican entre proyectos.
- Preferencias de interacción repetidas y de bajo riesgo que resulta costoso volver a explicar.
- Recordatorios auxiliares cuya fuente y falibilidad estén claras.

## Contenido inadecuado para memory

- Hechos del proyecto, requisitos aceptados, especificaciones o decisiones.
- Tarea/run state actual, resultados de tests, estado de incidentes o estado de releases.
- Secrets, credenciales, datos personales sin una necesidad definida o hechos externos copiados.
- Decisiones propuestas presentadas como verdad aceptada.
- Cualquier regla que deba aplicarse de forma determinista.

## Gestión de contradicciones

Las fuentes autoritativas y versionadas del proyecto prevalecen sobre memory. La evidencia actual del repositorio establece lo que existe y puede revelar drift; no invalida silenciosamente el target aprobado. Si memory entra en conflicto con una fuente autoritativa, ignórala para la decisión, informa el conflicto cuando sea material y corrige/elimina la memory obsoleta mediante un control explícito en lugar de reescribir la verdad del proyecto.

## Criterios de activación

Evalúa la activación sólo después de observar un uso real entre proyectos. Exige evidencia de recall útil repetido, una revisión del almacenamiento/privacidad local, controles claros por chat, un proceso de inspección/eliminación y tests que demuestren que la memory obsoleta no invalida el contexto del proyecto. Comienza con un alcance estrecho y conserva la capacidad de deshabilitar de forma independiente la generación y el uso.
