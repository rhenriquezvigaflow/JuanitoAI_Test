# Piloto documental basado en archivos reales

Se revisaron localmente siete archivos: un DOCX funcional, un PFD de una página, una corrida de membranas de diez páginas, dos proyecciones químicas visuales de una página y dos libros XLSX. Los originales, imágenes y precios no se incorporan al repositorio.

## Consecuencias para la implementación

| Evidencia local | Requisito |
| --- | --- |
| Costeo de seis hojas y 1.385 fórmulas | Leer hojas, tablas, nombres definidos, fórmulas y valores guardados; preservar unidades y monedas |
| Plantilla APU de siete hojas y 74 fórmulas | Verificar referencias entre resumen y detalles |
| Una fórmula de resumen contiene `#REF!` | Primer control determinista reproducible sin LLM |
| Dos proyecciones químicas sin texto extraíble | Ruta visual/OCR con evidencia de página; cero texto no significa archivo vacío |
| PFD con equipos agrupados y límites de suministro | Comparar cantidades por sistema y alcance |
| Texto del PFD repite rótulos que visualmente corresponden a menos figuras | No contar equipos por apariciones de palabras |
| Corrida de membranas con etapas, parámetros y avisos | Conservar escenario, revisión, unidades y advertencias |
| Alternativas de producto químico | No sumar dosis alternativas ni convertirlas en reglas universales |

Se realizó inspección documental, lectura con openpyxl y visualización de PDF. No se ejecutaron macros, no se recalcularon los libros completos y no se llamó a OpenAI. No se confirmó que estos archivos reproduzcan exactamente la discrepancia histórica «cuatro bombas frente a dos».

## Alcance y criterios pendientes

El documento funcional prioriza análisis de diseño/costeo y deja la generación de borradores para una etapa posterior con aprobación humana. Requiere preguntas y respuestas con estados: resuelta, pendiente, excepción aceptada, supuesto incorporado y riesgo vigente.

También requiere segregación por proyecto/área, confidencialidad y costos internos/INET como fuente futura. El catálogo exhaustivo de validaciones, tolerancias y el documento “Equipos y Criterios de Proceso VF” están expresamente pendientes de elaboración con especialistas.

La arquitectura permite avanzar sin esos límites: los controles aritméticos y de consistencia se implementan primero; las conclusiones técnicas que dependan de criterios aún no aprobados se presentan como pendientes de validación.

Cada parámetro conserva sustancia/especie, unidad/base de expresión, corriente, escenario, fecha y fuente. Distinguir medición, supuesto, resultado de simulación y límite aprobado. Un catálogo compartido no implica concentraciones ni dosis idénticas para todas las plantas.

## Pruebas iniciales

1. Referencia rota y destinos vacíos entre hojas, indicando fórmula y celda.
2. Cero numérico frente a vacío o fórmula sin resultado guardado.
3. Equipos y partidas con paquetes, reservas y suministro del cliente.
4. Lectura de proyecciones visuales manteniendo alternativas separadas.
5. Conciliación de cantidades/modelos de membranas entre corrida y costeo.
6. Contradicciones por escenario/revisión como preguntas trazables.
7. Respuestas que generan otra evaluación sin borrar la anterior.
8. Autorización consistente en visor, chat, recuperación y descargas.
9. Recuperación tras interrupción y resultados idempotentes.

Este expediente basta para iniciar la implementación y construir con el revisor un conjunto de referencia. La precisión y el ahorro operacional todavía deben medirse.
