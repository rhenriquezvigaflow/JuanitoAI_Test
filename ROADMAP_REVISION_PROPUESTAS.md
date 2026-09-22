# Revisión de propuestas: reutilización y roadmap preliminar

Fecha: 21 de septiembre de 2026.

Actualización del 22 de septiembre: ya se recibió y revisó código v0.6.9. La evidencia técnica y la estimación revisada están en [AUDITORIA_TECNICA_V069_Y_ROADMAP.md](AUDITORIA_TECNICA_V069_Y_ROADMAP.md). Las observaciones de este documento sobre falta de código describen el estado de la revisión inicial.

## Alcance de la revisión

Se revisaron los textos de siete guías PDF, la imagen modo-avanzado.png, las capturas compartidas, las taxonomías, los criterios de complejidad y secciones de extracción, consolidación, cobertura, aclaraciones y síntesis del archivo requerimientos.txt. Este archivo reúne múltiples prompts, pese a su nombre. La carpeta contiene documentación y configuración exportada; no se encontró código fuente ejecutable. Las capacidades descritas por las guías aún deben contrastarse con implementación y pruebas. No se han evaluado propuestas reales.

Esta propuesta amplía el primer acercamiento: el objetivo prioritario ahora es revisar propuestas antes de enviarlas, para reducir errores y tiempo de trabajo. La evaluación histórica alimenta la biblioteca de referencias y los casos de prueba.

## Recomendación

Conservar la arquitectura de expediente, evidencias, hallazgos y reproceso incremental. Simplificar los reportes para el usuario. Añadir una capa estructurada de equipos, partidas, parámetros y relaciones, junto con verificaciones deterministas de cantidades y cálculos. Usar búsqueda documental para antecedentes y explicación de hallazgos.

Una propuesta pequeña puede requerir menos análisis contractual y, a la vez, controles rigurosos sobre todas las partidas. La simplificación debe quitar trabajo irrelevante, no ocultar cobertura incompleta.

## Qué reutilizar, adaptar y construir

| Componente documentado | Decisión preliminar | Condición o adaptación |
| --- | --- | --- |
| Ingesta, clasificación e inventario | Reutilizar concepto; verificar código | Conservar jerarquía, permisos, versión y estado de lectura |
| Hallazgos estructurados con IDs y fuentes | Reutilizar y ampliar | Añadir hoja/celda para Excel y región de plano para evidencia visual |
| Dependencias y «Procesar lo que falta» | Reutilizar | Validar invalidación de datos derivados, aislamiento por proyecto y ejecución concurrente |
| Estado vigente tras aclaraciones | Reutilizar | Aplicar también a revisiones de planos, selecciones y presupuestos |
| Cobertura requisito/oferta | Adaptar | Distinguir contradicción, ausencia comprobada y extracción incompleta |
| Visor con trazabilidad | Reutilizar o adaptar | Centrarlo en alertas, equipos, costeo y revisión humana |
| Plan de ejecución, registros y consumo | Reutilizar | Medir también espera, tiempo humano, OCR y costo por propuesta completa |
| Configuración y contratos JSON protegidos | Reutilizar patrón | Versionar reglas y validar cambios con ejemplos antes de activarlos |
| Taxonomía EPC y complejidad 10/20/40 HH | Reemplazar configuración | Definir familias y esfuerzos reales del nuevo cliente |
| Briefs extensos, cronograma y análisis contractual | Activar por necesidad | No ejecutar todos los módulos para todos los casos |
| Inventario de equipos y relación con partidas | Construir o verificar si existe fuera de lo entregado | No está acreditado en la documentación revisada |
| Verificación aritmética y comercial del Excel | Construir o verificar | Reglas precisas por plantilla y evidencia por celda |
| Lectura visual de planos y conciliación | Nueva prueba técnica | El soporte de PDF textual no demuestra comprensión de diagramas |
| Biblioteca corporativa y de fabricantes | Diseñar | Responsables, versiones, aprobación y aplicabilidad |
| Chat del expediente | Verificar/desarrollar | Preguntas sugeridas no equivalen a conversación libre con recuperación de evidencia |

La reutilización de código también requiere confirmar acceso y autorización para adaptarlo al nuevo cliente. No es posible estimar un porcentaje de reutilización con capturas y prompts solamente.

## Hallazgos concretos en los materiales

1. **La lectura de planos es una brecha crítica.** «Logs, errores y avisos», página 2, indica que un PDF escaneado sin texto no se lee. Un PDF vectorial con texto tampoco garantiza que se detecten símbolos, relaciones o cantidades. Se requiere una prueba con planos reales.
2. **La extracción está optimizada para priorizar.** requerimientos.txt, alrededor de la línea 126, limita a 40 candidatos por respuesta. Es por respuesta, no necesariamente por expediente. Sirve para síntesis; para equipos se necesita extracción completa por lotes, conciliación y señal de incompletitud.
3. **La cobertura tiene una frontera ambigua.** Alrededor de las líneas 550–610 aparecen tanto «no_evaluable» por información insuficiente como la instrucción de marcar «brecha» al no encontrar evidencia. Separar: evidencia ausente en documentación revisada, fuente requerida no disponible y fuente que no pudo leerse.
4. **Hay mínimos de salida inadecuados para casos pequeños.** La síntesis de preguntas pide entre 15 y 25. Cambiar a cero o más preguntas justificadas, sin mínimo. Revisar igualmente los mínimos de alertas.
5. **Los reportes heredan omisiones de extracción.** «Cómo funciona el análisis» explica que la síntesis trabaja sobre hallazgos. Conservar ese ahorro, pero hacer que una validación pueda consultar la evidencia original cuando falte un dato o exista conflicto.
6. **La clasificación enruta los documentos.** taxonomias.txt conecta roles documentales a módulos y deja otros sin análisis. Añadir roles explícitos para costeo, cotización de proveedor, lista de equipos, selección de fabricante y plano. Verificar que una clasificación errónea no descarte una fuente necesaria.
7. **El perfil de empresa necesita coherencia.** complejidad.txt define EPC/llave en mano como habitual, mientras que el prompt de requisitos incluye ejemplos de alcance o contrato inusual que podrían interpretarse como estratégicos. No basta copiar los ejemplos: centralizar el perfil real del nuevo cliente y probar consistencia entre módulos.

## Arquitectura propuesta

```text
SharePoint / expediente          Biblioteca técnica aprobada
          |                              |
          v                              v
Inventario y versiones          Catálogos / referencias / reglas
          |                              |
          v                              v
Extracción de texto, tablas, equipos y evidencia visual
          |
          v
Registro estructurado de equipos, partidas y parámetros
          |
          +--> Reglas de cantidades, aritmética y coherencia
          +--> Consulta documental y comparación contextual
          |
          v
Hallazgos con evidencia, alcance y estado de revisión
          |
          v
Directorio + visor + bandeja de revisión + chat
```

### Papel de RAG y MCP

RAG recupera información pertinente de la biblioteca para fundamentar respuestas. Es útil para localizar especificaciones, antecedentes similares y explicaciones. No garantiza inventariar todos los equipos ni verificar todas las filas de una planilla: eso corresponde al procesamiento completo y a consultas/reglas estructuradas.

MCP es una interfaz para ofrecer herramientas y recursos a aplicaciones de IA. Puede exponer buscar_documentos, obtener_equipo, consultar_cotizacion o ejecutar_revision. No sustituye la base de datos, la ingesta, los permisos ni el motor de validación.

Recomendación: un backend modular con API propia; añadir un servidor MCP como fachada si otras aplicaciones deben consumir sus herramientas. No es necesario implementarlo para el primer piloto. n8n puede disparar sincronizaciones o coordinar tareas; las reglas y evidencias deben persistir en el servicio de revisión.

Referencias primarias: [RAG, Microsoft Learn](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview) y [arquitectura MCP](https://modelcontextprotocol.io/docs/learn/architecture).

### Administración del conocimiento

| Tipo | Tratamiento propuesto | Responsable y vigencia |
| --- | --- | --- |
| Expediente activo | Archivos originales, versiones y evidencias aisladas por proyecto | Responsable de la propuesta |
| Catálogos y selecciones de fabricantes | Documentos indexados más parámetros estructurados cuando corresponda | Especialista técnico; modelo, versión y condiciones de aplicación |
| Precios y cotizaciones | Registros estructurados y documentos originales | Compras/comercial; moneda, fecha, vigencia y condiciones |
| Propuestas exitosas | Biblioteca de patrones y soluciones revisadas | Ingeniero aprobador; contexto, límites y fecha |
| Reglas de revisión | Validaciones versionadas con ejemplos correctos e incorrectos | Dueño técnico de cada regla |
| Correcciones y aprendizajes | Pendientes de revisión antes de publicación | Revisor; no convertir comentarios del chat en reglas automáticamente |

Todo elemento debe tener origen, responsable, fecha/revisión, estado de aprobación, ámbito de uso y permisos. Los documentos obsoletos se conservan para trazabilidad pero no se presentan como vigentes. Una propuesta adjudicada es una referencia, no prueba de que sus cálculos o precios sigan siendo correctos.

La recuperación debe combinar términos exactos (TAG, código, modelo) con búsqueda semántica y filtros de fabricante, familia, versión y proyecto. Los permisos también se aplican a resultados derivados y cachés. No mezclar antecedentes confidenciales de clientes por similitud documental.

Las selecciones de software de fabricante se almacenan junto con entradas, unidades, modelo seleccionado, salida, fecha y versión del software si está disponible. Preferir exportaciones estructuradas sobre reconstrucción visual. No prometer automatización del programa hasta conocer API, formatos y condiciones de uso.

## Caso «cuatro bombas en plano, dos en costeo»

Flujo propuesto:

1. Identificar las revisiones de plano y costeo que se comparan y el alcance de suministro.
2. Extraer las instancias de equipos: TAG, tipo, sistema, ubicación y evidencia. Distinguir símbolos de leyenda, repeticiones entre hojas, equipos existentes, opcionales y reservas.
3. Extraer partidas: referencia, descripción, cantidad, unidad, precio unitario, moneda, subtotal, fórmula y celdas fuente.
4. Relacionar equipos y partidas. Admitir una partida que contiene varios equipos, paquetes/skids y equipos aportados por el cliente; los emparejamientos inciertos pasan a revisión.
5. Comparar cantidades normalizadas dentro del mismo alcance. Si faltan dos equipos sin explicación documentada, generar discrepancia con las evidencias de ambos lados.
6. El ingeniero confirma o descarta con motivo. La revisión y su justificación quedan registradas.

Estados útiles: discrepancia confirmada por regla, discrepancia probable por extracción visual, información insuficiente, excepción justificada. La severidad del impacto se registra aparte de la certeza de extracción.

Ejemplo ficticio: P-101A/B y P-102A/B aparecen como cuatro equipos distintos en la revisión vigente; la partida asociada contempla dos unidades. Mostrar «diferencia de dos unidades pendiente de aclarar», junto a plano y celdas. No afirmar automáticamente que debe aumentarse el precio: primero comprobar alcance y composición de la partida.

## Qué errores abordar primero

| Control | Método | Lugar en el roadmap |
| --- | --- | --- |
| Cantidad × precio, subtotales y suma de partidas | Cálculo determinista según plantilla | Primer piloto |
| Referencias rotas, fórmulas omitidas y valores cacheados antiguos | Inspección y recálculo controlado con motor compatible | Primer piloto, según formato |
| Cantidades entre lista de equipos y costeo | Cruce por identificadores y reglas de alcance | Primer piloto |
| Moneda, unidad y cotización vigente | Comparación con fuente aprobada | Primer piloto |
| Equipos entre plano y costeo | Exportación estructurada o extracción visual validada | Prueba temprana; ampliar tras medir |
| Parámetros entre selección de fabricante y propuesta | Comparación con unidades y condiciones equivalentes | Segunda ampliación |
| Precio atípico respecto a antecedentes | Detección de anomalías contextualizada | Posterior; atípico no equivale a incorrecto |
| Adecuación de selección hidráulica o de membranas | Herramientas y reglas de ingeniería aprobadas, con entradas completas | Alcance especializado posterior |

Leer fórmulas de Excel no equivale a ejecutarlas. Identificar macros, vínculos externos, hojas ocultas, redondeo, impuestos, descuentos y diferencia entre margen y recargo. No ejecutar macros de archivos recibidos como parte de la ingesta general.

El producto debe publicar un catálogo de controles soportados y mostrar cuáles se ejecutaron en cada propuesta. «Sin hallazgos» significa sin hallazgos dentro de esos controles y su cobertura, no ausencia universal de errores.

## Roadmap por hitos

No se fija todavía un calendario contractual. Los formatos de planos y el código disponible pueden cambiar sustancialmente el esfuerzo.

| Fase | Trabajo y entregable | Criterio de salida |
| --- | --- | --- |
| 0. Definición y línea base | Código, flujo actual, muestra de 10–20 expedientes si está disponible, catálogo de errores, horas por tarea y familia piloto | Ingeniero responsable acuerda controles prioritarios y conjunto de referencia |
| 1. Prueba técnica de extracción | Una plantilla de costeo y un formato/familia de planos; extracción de equipos y partidas con fuentes | Medir cobertura y errores de extracción; decidir exportación estructurada, visión o entrada asistida |
| 2. Piloto de revisión | Directorio, reglas prioritarias, cruce equipos/costeo, bandeja de hallazgos y aprobación humana | Comparación ciega con revisión experta; cada alerta tiene evidencia y regla/versión |
| 3. Conocimiento y chat | Biblioteca aprobada, búsqueda con filtros y chat por expediente | Respuestas sustentadas, permisos correctos y abstención ante información insuficiente |
| 4. Piloto operacional | Propuestas nuevas, ejecución concurrente, seguimiento de tiempos y costos | Ahorro neto y calidad aceptables con umbrales acordados |
| 5. Escalamiento | Más familias, formatos, fabricantes y controles técnicos | Cada ampliación supera su conjunto de pruebas y tiene responsable |

Realizar la prueba de planos temprano: es una incertidumbre central. La interfaz y el chat no deben postergarla. La integración de SharePoint se aprovecha si el código existente la implementa adecuadamente; no se presupone a partir de un selector de carpetas.

### Medición y conjunto de referencia

Incluir casos con errores conocidos, casos correctos y excepciones: bombas de reserva incluidas, equipos fuera de suministro, paquetes que agrupan unidades, planos duplicados, revisión obsoleta y archivo ilegible. Separar expedientes usados para ajustar reglas de otros reservados para validación. Errores sembrados complementan, no reemplazan, casos reales.

Medir por tipo de control: errores reales detectados, falsos positivos, errores omitidos, exactitud de cantidades/TAGs, cobertura de lectura y tiempo de revisión/corrección. Registrar también latencia, propuestas concurrentes y costo total por expediente. Acordar umbrales con negocio antes del piloto.

### Objetivo de pasar de cinco a dos ingenieros

Es una hipótesis de capacidad a validar. A igual volumen, horas disponibles, calidad y mezcla de trabajo, exige que las horas humanas totales necesarias bajen al 40% de la situación actual: una reducción del 60%.

Medir el proceso completo: recepción, interpretación, selección/dimensionamiento, consultas, cotizaciones, preparación, revisión y retrabajo. Si revisar documentos es solo una fracción pequeña del esfuerzo, automatizar esa fracción no alcanza la meta. Incluir el tiempo de resolver falsas alarmas, mantener la biblioteca y supervisar excepciones. No convertir una reducción del tiempo de análisis de IA en ahorro humano equivalente.

## Información necesaria para cerrar alcance y estimación

1. **Volumen y mezcla:** propuestas por mes, picos, familias frecuentes, duración del ciclo y horas por tarea.
2. **Muestra representativa:** expediente recibido, versiones, propuesta enviada, plano, lista de equipos, costeo nativo y correcciones del revisor. Incluir ejemplos correctos y errores relevantes.
3. **Software y formatos:** nombres/versiones de fabricantes y CAD, exportaciones disponibles, TAGs, plantillas Excel, macros, vínculos y acceso a selecciones originales.
4. **Reglas del negocio:** catálogo inicial de errores, tolerancias, unidades, alcance de suministro y quién valida cada regla.
5. **Código existente:** repositorio, arquitectura, dependencias, modelo de datos, despliegue, conector de carpetas, pruebas y posibilidad de adaptación.
6. **Operación y acceso:** SharePoint/sitios, permisos, infraestructura autorizada, usuarios concurrentes, presupuesto operacional y responsables de revisión.
7. **Aceptación:** qué controles deben funcionar para el piloto, tiempo esperado, falsos positivos tolerables y criterio para ampliar la automatización.

Se puede iniciar el roadmap con cuatro insumos: familia piloto, expedientes completos, experto que valide y formatos/software usados. El volumen y las horas actuales permiten después dimensionar capacidad y evaluar la meta comercial.
