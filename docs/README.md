# Documentación de bio-harness

Las guías dirigidas a personas explican la arquitectura V2 validada actual. Los experimentos detallados, comprobantes, fixtures y evidencia histórica permanecen bajo [`staging/audit/`](../staging/audit/README.md).

## Mapas visuales

- [Arquitectura general, límites y ciclo de solicitud](architecture.md)
- [Decisión de routing, responsabilidades y paralelismo](model-routing.md)
- [Workspace privado frente a verdad compartida](private-workspace.md)
- [Bootstrap adaptativo de proyectos](project-bootstrap.md)
- [SDD proporcional](sdd.md)
- [Descubrimiento y seguridad de la toolbox](toolbox.md)
- [Human gates](safety.md)
- [Quality red-team y gates de workers](quality-redteam.md)
- [Instalación, activación y rollback](installation.md)
- [Validación local y CI](development.md)

## Arquitectura

- [Arquitectura del sistema](architecture.md)
- [Estructura del repositorio](repository-layout.md)

## Enrutamiento de modelos

- [Enrutamiento de modelos que prioriza la calidad](model-routing.md)
- [Quality red-team](quality-redteam.md)

## Proyectos

- [Workspace privado `.ai`](private-workspace.md)
- [Bootstrap adaptativo de proyectos](project-bootstrap.md)
- [Desarrollo proporcional basado en especificaciones](sdd.md)

## Herramientas

- [Toolbox determinista reutilizable](toolbox.md)

## Seguridad

- [Autoridad y human gates](safety.md)

## Instalación

- [Instalación y rollback](installation.md)

## Desarrollo

- [Cambios en la fuente y validación](development.md)

## Evidencia de auditoría

- [Validación unificada de staging](../staging/VALIDATION.md)
- [Framework de calidad](../staging/audit/quality/README.md)
- [Evidencia del quality red-team](../staging/audit/quality/REDTEAM_REPORT.md)
- [Auditoría de instalación híbrida](../staging/audit/HARNESS_V2_HYBRID_INSTALL_20260902T231047Z.md)
- [Procedencia upstream fijada](../staging/audit/upstream_provenance.md)
