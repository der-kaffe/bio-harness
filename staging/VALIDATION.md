# Validación del staging del Harness V2

Validado el 2026-09-02 con Codex CLI 0.152.0. El quality red-team y la instalación híbrida local están completos. No se realizó ninguna adopción de proyecto, cambio del exclude de Git de un proyecto real ni migración del modelo parent.

| Comprobación | Resultado |
|---|---|
| `python3 -B staging/audit/validate_staging.py` | PASS |
| Tests unificados de infraestructura/política | 38/38 PASS |
| Tests independientes de toolbox | 3/3 PASS |
| Tests independientes de privacidad de Git | 4/4 PASS |
| Schema de fixtures/resultados de calidad | 67 fixtures PASS |
| Validator de la skill project-bootstrap | PASS |
| Paridad de assets entre blueprint y copia instalada | PASS |
| Presupuesto del AGENTS global | 294 words; PASS |
| Presupuesto de la política de enrutamiento | 549 words; PASS |
| Presupuesto del enrutador privado del proyecto | 129 words; PASS |
| Revisión de calidad independiente Sol/low | APPROVE tras la corrección |

La suite prueba worktrees normales y vinculados, rutas con espacios, rutas privadas aparentes con seguimiento, repositorios dirty/sin Git/mal formados, excludes idempotentes, fallos de read-only y symlinks, descubrimiento y precedencia de tools locales/globales, paquetes mal formados/con traversal/enlazados, descubrimiento sin ejecución, scaffolding exclusivo del proyecto, invariantes de catálogo/configuración, orden que prioriza la calidad, evidencia de resultados, control Sol antes de Luna, instalación/rollback general, discrepancias de root, recuperación real de un journal PREPARED interrumpido, migración exacta del parent vinculada a evidencia y rechazo de drift.

La primera pasada del reviewer encontró journals de mutación no duraderos, un gate Luna exclusivamente booleano, evidencia de resultados débil, ambigüedad del root de rollback y residuos de directorios creados. Se corrigieron. Una segunda pasada encontró gaps en la recuperación de prefijos parciales y la vinculación exacta entre control/candidato; se corrigieron y la revisión final de cierre no informó ningún finding BLOCKER ni MAJOR.

## Decisión de calidad

- Control del parent Sol/medium: 24 PASS, 0 regresiones.
- Candidato parent Luna/medium: 18 PASS, 3 PASS_WITH_MINOR_DIFFERENCE, 3 ROUTING_REGRESSION, 0 regresiones de seguridad.
- Decisión sobre el parent: `KEEP_SOL_MEDIUM_PARENT`.
- Researcher: Luna/medium después de que Luna/low omitiera evidencia material.
- Validator: Luna/low después de corregir y volver a probar el contrato para sólo skips/mutación de fuente.
- El híbrido V2 se instaló localmente mediante la migración validada; no se ejercitó ningún bootstrap de proyecto real.
- La disponibilidad de modelos a nivel de cuenta no se volvió a probar con workloads de pago; la configuración/capacidades locales actuales de Codex y el uso activo de Sol son la evidencia disponible.
