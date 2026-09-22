# GOLDEN-001 — Resultados esperados

> Documento de trabajo para construir el ground truth con especialistas. Este archivo no contiene nombres de cliente, precios ni documentos originales porque el repositorio es público.

## Objetivo

Definir qué debe detectar JuanAI en el primer expediente antes de implementar el MVP completo. El objetivo del spike es validar extracción, normalización, conciliación, reglas determinísticas y trazabilidad de evidencia.

## Resultados confirmados por inspección técnica

### ER-01 — Consistencia de caudales entre diseño y simulación

El PFD y la corrida de membranas contienen valores de alimentación, producto y rechazo que pueden compararse de manera determinística.

Resultado esperado del sistema:

```json
{
  "status": "consistente",
  "control": "process_flow_consistency",
  "evidence": [
    {"source": "DOC-PFD-001", "locator": "pagina/region"},
    {"source": "DOC-SIM-001", "locator": "pagina/parametro"}
  ]
}
```

La regla debe comparar valores después de normalizar unidad y escenario. No requiere LLM para decidir la igualdad numérica.

### ER-02 — Membranas: cantidad y modelo

La simulación y el costeo contienen cantidad total y modelo de membranas que pueden conciliarse.

Resultado esperado:

- extraer modelo normalizado;
- extraer cantidad;
- asociar ambas evidencias;
- reportar `consistente` cuando coinciden;
- reportar `discrepancia_comprobada` solo cuando ambas fuentes son legibles, vigentes y comparables y los valores difieren fuera de tolerancia.

### ER-03 — Portamembranas / pressure vessels

La simulación informa cantidad de cajas de presión y el costeo contiene la partida equivalente.

Resultado esperado:

- reconocer la equivalencia semántica `pressure vessel` / `portamembrana` mediante catálogo o matching controlado;
- realizar la comparación de cantidad en código;
- conservar evidencia de ambos lados.

### ER-04 — Filtros de pretratamiento

El PFD representa equipos de pretratamiento y el costeo incluye la partida correspondiente.

Resultado esperado:

- no contar equipos únicamente por número de apariciones del texto;
- utilizar estructura visual/regiones cuando el PFD repita rótulos;
- comparar cantidad, tipo y tamaño cuando exista evidencia suficiente.

### ER-05 — Referencia rota en APU

El libro APU contiene al menos una referencia `#REF!` en su resumen económico.

Resultado esperado:

```json
{
  "status": "discrepancia_comprobada",
  "control": "excel_broken_reference",
  "severity": "high",
  "evidence": {
    "source": "DOC-APU-001",
    "locator": "hoja/celda",
    "formula": "formula_original"
  }
}
```

El sistema debe indicar la celda y fórmula afectada. No debe intentar reparar automáticamente la fórmula durante el análisis.

### ER-06 — Propagación de error desde una referencia rota

Si una celda con `#REF!` alimenta un subtotal, IVA o total, JuanAI debe registrar la cadena de dependencias afectadas.

Resultado esperado:

- identificar la causa raíz;
- distinguir causa de celdas derivadas afectadas;
- evitar generar múltiples hallazgos independientes cuando todos provienen del mismo error raíz, salvo que negocio defina lo contrario.

### ER-07 — Nombres definidos dañados en el costeo

El libro de costeo contiene nombres definidos a nivel de libro cuya fórmula apunta a `#REF!`, mientras existen definiciones locales válidas para algunos nombres.

Resultado esperado:

- inventariar nombre, ámbito y referencia;
- reportar riesgo de integridad;
- determinar si la fórmula que se evalúa resuelve contra el ámbito local o depende del nombre inválido;
- no declarar automáticamente que todos los costos están incorrectos.

Estado inicial recomendado:

`discrepancia_probable` o `informacion_insuficiente` hasta analizar impacto real.

### ER-08 — Ajuste hardcodeado en total APU

El total de suministro contiene un ajuste numérico explícito dentro de la fórmula.

Resultado esperado:

- detectar el literal dentro de una fórmula de total;
- mostrar fórmula y celda;
- relacionarlo con partidas potencialmente involucradas;
- generar pregunta al especialista.

Estado inicial:

`informacion_insuficiente`.

Pregunta propuesta:

> ¿El ajuste manual incorporado al total de suministro corresponde a una corrección comercial aprobada? Indicar motivo y fuente de autorización.

### ER-09 — Partidas potencialmente inconsistentes entre costeo y APU

Existen partidas del APU cuyo valor requiere conciliación contra el resumen del costeo y cuya interpretación no debe cerrarse automáticamente.

Resultado esperado:

- detectar diferencia cuantitativa;
- presentar ambas fuentes;
- indicar si existe un ajuste en el total que podría compensar la diferencia;
- clasificar como `discrepancia_probable`, nunca como error definitivo sin revisión.

### ER-10 — Referencia externa ausente

Si una fórmula depende de otro libro/archivo que no está dentro del expediente, JuanAI debe registrar la ausencia de respaldo.

Resultado esperado:

```json
{
  "status": "evidencia_no_encontrada",
  "control": "external_reference_missing",
  "action": "solicitar_fuente"
}
```

La ausencia del archivo externo no demuestra que el valor sea incorrecto.

### ER-11 — PDFs visuales sin texto extraíble

Las proyecciones químicas pueden no disponer de texto parseable.

Resultado esperado:

- detectar que la extracción textual es insuficiente;
- ejecutar ruta visual/OCR cuando esté habilitada;
- conservar evidencia de página/región;
- no marcar el archivo como vacío solo porque el extractor textual devuelve cero contenido.

### ER-12 — Alternativas químicas

Dos proyecciones químicas diferentes representan alternativas y no necesariamente una contradicción.

Resultado esperado:

- mantener cada alternativa como escenario separado;
- no sumar sus dosis;
- no transformar ninguna alternativa en regla universal;
- solicitar selección/confirmación cuando el costeo no permita identificar inequívocamente el producto elegido.

## Casos que requieren validación del especialista

Antes de cerrar GOLDEN-001, un especialista debe confirmar para cada control:

| Campo | Valores permitidos |
| --- | --- |
| Decisión | confirmar / corregir / descartar / excepción / no aplica |
| Severidad | crítica / alta / media / baja |
| Comparabilidad | sí / no / condicionada |
| Revisión vigente | identificador de revisión |
| Comentario | explicación técnica o comercial |
| Evidencia adicional | referencia al almacenamiento privado |

## Criterio de cierre del ground truth

GOLDEN-001 se considera listo para implementar cuando:

- [ ] C01–C10 tienen decisión del especialista;
- [ ] las discrepancias conocidas están identificadas;
- [ ] se definió qué casos son correctos para medir falsos positivos;
- [ ] las excepciones tienen justificación explícita;
- [ ] se acordaron tolerancias de cantidad/unidad cuando correspondan;
- [ ] cada resultado esperado tiene evidencia verificable;
- [ ] quedó definida la regla de decisión para ausencia de evidencia;
- [ ] los datos sensibles continúan fuera de Git.

## Salida mínima del SPIKE-001

El spike debe producir, como mínimo:

```text
inventory.json
extracted_pfd.json
extracted_simulation.json
extracted_costing.json
extracted_apu.json
findings.json
coverage.json
```

Cada `finding` debe incluir:

- `control_id`;
- `status`;
- `severity`;
- `description`;
- valores comparados;
- unidad normalizada;
- evidencia A/B;
- regla y versión;
- cobertura;
- certeza cuando haya interpretación IA;
- `requires_human_review`;
- decisión del revisor cuando exista.
