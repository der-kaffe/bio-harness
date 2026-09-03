# Integraciones excluidas

## job-forge / Geometra

La configuración global actual la genera `@agent-pattern-labs/iso-route` dentro de job-forge 2.14.50. Proporciona valores predeterminados de modelos, profiles inline obsoletos, el launcher MCP de Geometra y entradas de trust de proyectos. El postinstall del paquete creó deliberadamente un symlink hacia el `.codex/config.toml` del consumidor; como la ruta del consumidor era el home, se convirtió en configuración global.

Geometra proporciona una capacidad especializada de MCP/browser mediante:

```text
npx --no-install job-forge mcp:geometra
```

Se excluye del core candidato porque:

- una integración especializada de búsqueda de empleo/browser no debe ser responsable de los valores globales predeterminados de Codex;
- el symlink depende de una caché npx mutable y susceptible de limpieza;
- las tablas de profiles legacy son incompatibles con los profiles actuales de Codex;
- los intentos recientes de resolución con npm fallaron, por lo que una configuración habilitada no demuestra que el server esté sano;
- incluirla incumpliría el requisito de staging de no cambiar ni dar por supuestas integraciones MCP reales.

No se desinstala ni deshabilita nada en el home real.

## Reintroducción independiente futura

Antes de reintroducirla:

1. Confirma un paquete/versión mantenido y resoluble y un launcher compatible.
2. Elige una ubicación estable de instalación independiente del archivo de configuración global.
3. Inspecciona el comportamiento de postinstall/sync y evita que asuma el ownership de `~/.codex`.
4. Prueba el MCP en un `CODEX_HOME` aislado y sin credenciales reales cuando sea posible.
5. Define las tools requeridas, el comportamiento de aprobación, el modo del browser, la exposición de datos y el rollback.
6. Añade únicamente la stanza MCP a la configuración del usuario o del proyecto adecuado tras la aprobación humana.

No restaures el symlink de configuración de la caché npx como mecanismo de integración.
