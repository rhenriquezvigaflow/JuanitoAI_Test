# JuanAI

Plataforma para revisar muchas propuestas de ingeniería, detectar discrepancias entre propuesta, planos y costeo, y consultar resultados respaldados por evidencia.

## Estado

Definición de arquitectura y roadmap. Todavía no hay una aplicación JuanAI implementada, conexión a SharePoint, SSO ni evaluaciones ejecutadas con modelos en este repositorio.

## Arquitectura propuesta

- Python/FastAPI para la aplicación y el servicio de evaluación.
- PostgreSQL y pgvector para datos y recuperación documental, con búsqueda textual complementaria.
- Procesamiento persistente en el servidor, independiente del navegador.
- API OpenAI para revisión documental y visual de PDF; cálculos de costeo verificables en código.
- SSO corporativo, roles, auditoría y resultados versionados.
- Prompts editables y conocimiento aprobado antes de reutilizar aprendizajes.
- LibreChat como candidato para conversación sobre expedientes; LangChain como componente opcional de recuperación.

Las decisiones pendientes y condiciones de implementación se describen en la arquitectura objetivo.

## Documentación

1. [Arquitectura objetivo](ARQUITECTURA_OBJETIVO.md): alcance vigente y decisiones propuestas.
2. [Auditoría técnica de ECO v0.6.9 y roadmap](AUDITORIA_TECNICA_V069_Y_ROADMAP.md): hallazgos en el código de referencia y estimación condicionada.
3. [Roadmap preliminar](ROADMAP_REVISION_PROPUESTAS.md): análisis previo a recibir el código fuente.
4. [Primer acercamiento](PRIMER_ACERCAMIENTO.md): contexto inicial del proyecto.

Ante diferencias, prevalece el alcance actualizado de la arquitectura objetivo. Los documentos históricos se conservan para trazabilidad.

## Primer hito

Validar con expedientes representativos el flujo **PDF del plano + costeo → discrepancias con evidencia**, incluyendo casos correctos, cantidades omitidas, paquetes y revisiones diferentes. En paralelo, definir acceso, persistencia y contratos de resultados.

## Verificación del código de referencia

El código original ECO y sus documentos no están incluidos. Para reproducir la prueba aislada de ingesta sobre una copia autorizada:

```sh
python -m pip install openpyxl
python analisis_tender/verificar_codigo.py --source /ruta/eco-propuestas-ai-v0.6.9
```

El script inspecciona sintaxis y ejecuta funciones de ingesta extraídas del código contra un Excel sintético; no inicia la aplicación ni llama a modelos. El resultado local es `analisis_tender/verificacion_codigo.json`. No constituye una prueba integral ni una suite de JuanAI.
