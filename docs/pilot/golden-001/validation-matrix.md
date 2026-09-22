# GOLDEN-001 — Matriz de validación

> Matriz inicial basada en el expediente real revisado. Los valores sensibles o que identifiquen directamente al cliente no se versionan en este repositorio público. Los localizadores exactos del caso real se mantienen en el almacenamiento privado del piloto.

## Estados permitidos

- `consistente`
- `discrepancia_comprobada`
- `discrepancia_probable`
- `evidencia_no_encontrada`
- `documento_no_disponible`
- `documento_ilegible_o_parcial`
- `informacion_insuficiente`
- `excepcion_justificada`
- `no_aplica`

`evidencia_no_encontrada` nunca equivale por sí sola a incumplimiento.

## Matriz inicial

| ID | Control | Fuente A | Fuente B | Tipo | Resultado inicial | Revisión humana |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | Caudal de alimentación del proceso vs simulación | PFD | Simulación | Determinístico | Esperado consistente | Confirmar vigencia de ambas revisiones |
| C02 | Caudal de producto vs simulación | PFD | Simulación | Determinístico | Esperado consistente | Confirmar unidad y escenario |
| C03 | Caudal de rechazo vs simulación | PFD | Simulación | Determinístico | Esperado consistente | Confirmar unidad y escenario |
| C04 | Cantidad de filtros de pretratamiento | PFD | Costeo | Extracción visual + regla | Esperado consistente | Confirmar cómo interpretar equipos agrupados |
| C05 | Tipo/tamaño de filtros de pretratamiento | PFD | Costeo | Matching + regla | Esperado consistente | Confirmar equivalencia de nomenclaturas |
| C06 | Cantidad de elementos de membrana | Simulación | Costeo | Determinístico | Esperado consistente | Confirmar revisión vigente |
| C07 | Modelo de membrana | Simulación | Costeo | Determinístico | Esperado consistente | Confirmar equivalencias de nombre/modelo |
| C08 | Cantidad de portamembranas / pressure vessels | Simulación | Costeo | Determinístico | Esperado consistente | Confirmar terminología usada por ingeniería |
| C09 | Centros de costo de suministro | Costeo | APU | Determinístico | Parcialmente consistente | Revisar partidas especiales y exclusiones |
| C10 | Integridad de referencias entre hojas | APU | APU | Determinístico | Discrepancia comprobada en al menos una referencia | Confirmar si es error del libro o plantilla en construcción |
| C11 | Fórmulas con referencias inválidas | Costeo/APU | — | Determinístico | Debe reportarse sin inferir costo incorrecto automáticamente | Validar severidad |
| C12 | Nombres definidos con referencia inválida | Costeo | — | Determinístico | Debe reportarse como riesgo de integridad | Validar si afecta cálculo vigente |
| C13 | Fórmula con valor almacenado pero dependencias dañadas | Costeo | — | Determinístico | `informacion_insuficiente` o `discrepancia_probable` | Especialista decide impacto |
| C14 | Ajustes hardcodeados en total APU | APU | Costeo | Determinístico | Requiere explicación | Confirmar si es ajuste autorizado |
| C15 | Partidas duplicadas o con valor reutilizado | APU | Costeo | Regla + revisión | `discrepancia_probable` | Confirmar intención comercial |
| C16 | Referencia a fuente externa no incluida | Costeo | Fuente externa | Determinístico | `evidencia_no_encontrada` | Solicitar respaldo si aplica |
| C17 | Descripción/resumen de simulación vs resultados calculados | Simulación | Simulación | Determinístico | Posible discrepancia de metadatos | Confirmar escenario vigente |
| C18 | Alternativas de producto químico | Proyección química A | Proyección química B | Clasificación contextual | No deben sumarse ni tratarse como contradicción automática | Definir alternativa seleccionada |
| C19 | Dosis química vs costeo | Proyección química | Costeo | Regla + contexto | `informacion_insuficiente` mientras no se conozca producto seleccionado | Revisión técnica obligatoria |
| C20 | Documentos ilegibles o sin texto extraíble | PDF visual | — | Cobertura | `documento_ilegible_o_parcial` solo si falla la ruta visual/OCR | No convertir ausencia de texto en archivo vacío |

## Evidencia mínima requerida

### PDF / plano

- alias del documento;
- revisión;
- página;
- región o coordenadas;
- etiqueta visible;
- fragmento/recorte verificable.

### XLSX

- alias del libro;
- revisión;
- hoja;
- celda o rango;
- fórmula;
- valor almacenado;
- unidad/moneda cuando aplique;
- dependencias relevantes.

### Simulación

- alias del archivo;
- revisión;
- escenario;
- parámetro;
- unidad;
- valor;
- fecha de ejecución si existe.

## Reglas de decisión

1. Los controles aritméticos, referencias, cantidades y unidades se ejecutan en código.
2. El LLM puede ayudar a interpretar nombres, planos y contexto, pero no decide por sí solo una discrepancia económica crítica.
3. Una excepción solo queda cerrada cuando un revisor autorizado la acepta.
4. Cada hallazgo debe conservar la versión de documento, regla, extractor y evaluación que lo originó.
5. Una corrección genera una nueva evaluación; no se sobrescribe el resultado aprobado anterior.
