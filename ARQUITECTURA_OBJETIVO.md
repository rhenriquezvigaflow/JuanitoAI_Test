# Arquitectura objetivo — revisión de muchas propuestas

Actualizado: 22 de septiembre de 2026. Propuesta de arquitectura, no implementación ni decisión contractual.

## Alcance confirmado por el solicitante

- Acceso con cuentas corporativas mediante SSO; roles y registro de acciones.
- Un administrador adjunta propuesta, PDF del plano, costeo y otros antecedentes.
- Procesamiento en el servidor independiente del navegador.
- Evaluación mediante prompts especializados, documentos del expediente, RAG y API OpenAI.
- Resultados persistentes y consultables por los usuarios autorizados; chat para preguntas y acotaciones.
- Historial de propuestas analizadas para auditoría.
- Reutilización de propuestas y evaluaciones como antecedentes de futuros análisis.
- Editor de prompts en la interfaz.
- Prioridad: muchas propuestas pequeñas, revisión útil y menor error. La generación de propuestas no es el núcleo inicial.

## Decisión tecnológica recomendada

Conservar Python/FastAPI y la metodología del código ECO. Incorporar PostgreSQL para estado, entidades y auditoría; pgvector para búsqueda semántica, acompañado de búsqueda textual y consultas exactas por TAG/modelo. Guardar archivos originales en almacenamiento de archivos/objetos, con referencias desde la base.

LangChain es opcional y complementario a pgvector: puede aportar conectores y componentes de recuperación. Usarlo detrás de un servicio de conocimiento si reduce código propio; no es necesario migrar todo el orquestador. La RAG API de LibreChat ya declara LangChain + FastAPI + PostgreSQL/pgvector: es candidato de reutilización, pendiente de comprobar sus contratos, permisos e integración con el dominio de propuestas.

Mantener un único servicio lógico de conocimiento para evaluación y chat. No crear dos corpus corporativos divergentes, uno para la aplicación y otro para LibreChat. La integración puede usar API o herramientas MCP; los permisos y filtros se verifican en el backend según identidad autenticada, no a partir de IDs que el modelo suministre sin validar. Si se adopta LibreChat, revisar su infraestructura adicional, incluyendo MongoDB para sus propios datos, y fijar una versión probada.

## Revisión visual directa como primera ruta

El ejercicio PDF + costeo descrito por el solicitante es la primera prueba a replicar. Con un modelo con visión, la entrada PDF puede incorporar texto e imágenes de las páginas. No se exige construir un intérprete de CAD para este piloto.

Flujo inicial:

1. Inventariar archivos, revisiones y páginas; leer Excel conservando celdas, ceros, fórmulas y valores.
2. Entregar al modelo el PDF visual y el costeo normalizado, con referencias a las celdas originales.
3. Solicitar equipos/TAGs visibles, cantidades, correspondencias, discrepancias y evidencia por página. Si una región o TAG es incierto, indicarlo.
4. Ejecutar comprobaciones aritméticas en código; asociar sus resultados al análisis.
5. Verificar los hallazgos candidatos mediante una segunda revisión dirigida cuando haya ambigüedad, plano denso o impacto elevado; no repetir indiscriminadamente todas las llamadas.
6. Presentar errores, discrepancias probables y mejoras por separado, con acción y evidencia.

Un conteo correcto en un ejemplo demuestra viabilidad inicial, no precisión general. Probar también leyendas, bombas de reserva, equipos repetidos entre hojas, paquetes incluidos en una partida, revisiones incompatibles y planos ilegibles. La ampliación de resolución, revisión por regiones o exportación estructurada se añade donde la evidencia lo justifique.

## Flujo operativo y prompts

Alta del expediente → carga → validación de entradas → trabajo en cola → revisión → resultado versionado → consultas/comentarios → validación de aprendizajes.

Familias iniciales de prompts:

| Operación | Salida esperada |
| --- | --- |
| Identificar documentos y alcance | Roles, revisiones y antecedentes faltantes |
| Extraer requisitos y parámetros | Datos relevantes con fuente |
| Leer plano | Equipos, cantidades observadas y ambigüedades |
| Conciliar plano y costeo | Relaciones y discrepancias |
| Revisar coherencia técnica | Contradicciones de parámetros, unidades o selección |
| Consultar antecedentes aprobados | Evidencia pertinente y límites de aplicabilidad |
| Evaluar calidad y oportunidades | Hallazgos priorizados, cobertura y acciones |
| Responder preguntas posteriores | Respuesta sustentada en expediente y evaluación seleccionados |

No ejecutar todas las operaciones para todos los casos: seleccionar según archivos, familia y controles pertinentes. Los controles económicos exactos son funciones de código, no prompts de cálculo libre.

El editor permite cambiar instrucciones, criterios y ejemplos, manteniendo contratos de salida protegidos. Cada publicación guarda autor, versión, fecha y pruebas. Las evaluaciones previas conservan la versión utilizada; un cambio de prompt no las reescribe. Para recalificar se crea otra ejecución.

## Identidad, roles y visibilidad

SSO con el proveedor corporativo; Microsoft Entra ID es la opción a confirmar si sus cuentas son Microsoft 365.

Roles propuestos: administrador (usuarios/configuración/carga), revisor técnico (validar/corregir hallazgos y aprobar conocimiento), lector (consultar resultados y conversar), auditor (examinar historial). Una persona puede tener varias capacidades; no se requiere crear cuatro grupos de personas.

Supuesto inicial: resultados compartidos con todos los usuarios corporativos habilitados para la aplicación. Confirmar si existen expedientes restringidos. La autorización se aplica tanto al visor como a archivos, recuperación, chat y exportaciones. Los permisos de LibreChat no sustituyen automáticamente los permisos del expediente.

Separar conversación de decisión: una acotación del usuario puede convertirse en observación vinculada a un hallazgo; una corrección formal requiere permiso y queda registrada. El chat no sobrescribe el análisis firmado.

## Memoria y aprendizaje

Guardar todo análisis para auditoría, con estados independientes de su elegibilidad como conocimiento:

- Análisis automático: disponible con esa etiqueta y fuentes, sin convertirse en regla aprobada.
- Revisión validada: hallazgos aceptados/corregidos y antecedentes confirmados pueden recuperarse en nuevas propuestas.
- Lección aprobada: regla o recomendación generalizable, con dueño, alcance y vigencia.

Esto es mejora de la base de conocimiento; no entrenamiento automático del modelo. Conservar propuestas defectuosas como casos negativos etiquetados y su corrección. Impedir que una conclusión generada sin respaldo gane autoridad por haber sido recuperada repetidamente. Congelar las fuentes/versions usadas en cada ejecución para poder auditar cómo se llegó al resultado.

La biblioteca incluye manuales, especificaciones, selecciones y propuestas históricas aprobadas. Cada documento debe tener origen, revisión, fabricante/modelo cuando aplique, vigencia, permisos y responsable. El conocimiento general del LLM sirve para interpretar o sugerir; los datos específicos, precios y conclusiones de cumplimiento deben apoyarse en fuentes o reglas verificadas.

## Ajuste del roadmap

1. Replicar PDF + costeo con ejemplos reales, a la vez que se define contrato de hallazgos y pauta de aceptación.
2. Construir expediente, carga, SSO, roles y ejecución persistente.
3. Integrar revisión visual, validaciones de costeo, resultados y auditoría.
4. Integrar el servicio compartido de conocimiento y chat; evaluar LibreChat mediante una prueba de SSO + alcance por expediente + citas.
5. Añadir publicación de prompts, validación de aprendizajes y medición operacional.

La ingesta de la biblioteca puede avanzar junto al núcleo cuando llegue la documentación. La reutilización de históricos requiere sus estados de validación antes de activarse como antecedente preferente. El calendario anterior sigue siendo orientativo: no se reduce automáticamente porque un ejemplo visual funcionó ni se aumenta por exigir CAD que no forma parte del primer alcance.

## Decisiones aún por confirmar

- Visibilidad común para toda la empresa o restricciones por proyecto/grupo.
- SSO corporativo concreto y acceso de IT para configurarlo.
- Quién valida hallazgos y publica conocimiento/prompts; posibilidad de reunir esos permisos en una persona.
- Volumen, tamaño de expedientes y ejemplos para medir calidad, costo y tiempos.
- LibreChat como aplicación conectada o chat integrado en la pantalla del expediente: probar la integración antes de fijarlo.

## Fuentes oficiales consultadas

- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview).
- [pgvector](https://github.com/pgvector/pgvector): búsqueda vectorial y combinación con full-text de PostgreSQL.
- [OpenAI: file inputs](https://developers.openai.com/api/docs/guides/file-inputs): entrada PDF con texto e imágenes de página en modelos con visión.
- [LibreChat RAG API](https://www.librechat.ai/docs/configuration/rag_api): LangChain, FastAPI y PostgreSQL/pgvector.
- [LibreChat access control](https://www.librechat.ai/docs/features/access_control).
- [LibreChat OAuth2/OIDC](https://www.librechat.ai/docs/configuration/authentication/OAuth2-OIDC).
