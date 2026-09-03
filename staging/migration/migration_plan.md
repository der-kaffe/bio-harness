# Preview de migración del Harness V2

Esto es preparación, no autorización. No lo ejecutes contra homes activos hasta que se aprueben los targets exactos y el baseline.

## Instalación V2 general

`v2_migrate.py` crea snapshots y previews, instala y ejecuta rollback de:

- `AGENTS.md` global;
- política de enrutamiento bajo demanda;
- seis definiciones explícitas de agentes;
- utilidad del sistema de toolbox y tests;
- skill project-bootstrap autosuficiente, referencias, helper y assets.

Excluye deliberadamente `config.toml`, skills no relacionadas, la configuración de Git, proyectos y autenticación/estado. El snapshot registra los hashes, modos y ausencias de targets, el conjunto completo de archivos project-bootstrap existentes y los hashes de los candidatos. Plan/install se detiene ante drift del candidato, target, root o universo de targets. Install crea backups duraderos de los targets y registra una intención `PREPARED` antes de cada mutación de archivo; después registra `COMMITTED` tras el reemplazo o la eliminación atómica. Recovery reconcilia los hashes actuales con los estados prepared/committed, rechaza el drift posterior y sólo elimina directorios creados por la instalación cuando siguen vacíos.

Usa primero un home simulado. Para una instalación activa, captura un baseline aprobado justo antes de la ventana exclusiva de migración y revisa el plan antes de `install`.

## Migración opcional y separada del parent

`migrate_parent_model.py` es una operación distinta. Sólo acepta el control Sol/medium esperado y el hash exacto de config. Valida un comprobante de quality gate dirigido por contenido, vuelve a ejecutar su evaluator fijado contra las fixtures/resultados con hashes exactos y exige el hash del comprobante aprobado por el humano. Escribe de forma duradera el backup y el journal `PREPARED` antes de cambiar únicamente el modelo a Luna y después registra `COMMITTED`; el rollback también recupera una transacción preparada y rechaza el drift posterior.

Nunca agrupes este paso opcional con la instalación V2 general. Ejecútalo sólo después de que las fixtures de control Sol/medium precedan y respalden un resultado Luna/medium sin regresiones y un humano apruebe el resultado.
