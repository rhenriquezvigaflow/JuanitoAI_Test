# GOLDEN-001 — Resultados esperados

> Ground truth provisional elaborado mediante revisión experta simulada del expediente. Sirve para desarrollo y pruebas iniciales. Antes de declararlo criterio corporativo debe ser ratificado por especialistas responsables de Proceso/Ingeniería/Costos.
>
> Este archivo no contiene nombres de cliente, precios sensibles ni documentos originales porque el repositorio es público.

## Objetivo

Definir qué debe detectar JuanAI en el primer expediente antes de implementar el MVP completo. El spike debe validar extracción, normalización, conciliación, reglas determinísticas, cobertura y trazabilidad de evidencia.

## Resultados esperados aprobados provisionalmente

### ER-01 — Caudales de diseño y simulación

**Decisión:** `consistente`.

JuanAI debe verificar alimentación, producto y rechazo después de normalizar unidades y escenario. La igualdad numérica se decide en código.

Esperado:

- alimentación: consistente;
- producto: consistente;
- rechazo: consistente;
- evidencia del PFD y de la simulación asociada al mismo finding.

### ER-02 — Filtros de pretratamiento

**Decisión:** `consistente`.

JuanAI debe reconocer cuatro equipos de pretratamiento equivalentes entre el PFD y el costeo, incluyendo tipo/tamaño cuando la extracción tenga cobertura suficiente.

Regla importante: no contar equipos únicamente por apariciones de palabras; usar agrupación visual/geométrica del plano.

### ER-03 — Membranas: cantidad y modelo

**Decisión:** `consistente` usando el bloque de resultados calculados de la simulación.

JuanAI debe conciliar:

- cantidad total de elementos;
- modelo canónico de membrana;
- revisión/escenario usado como fuente.

Si el encabezado narrativo de una revisión contradice el bloque calculado, ese conflicto debe registrarse por separado como ER-10 y no degradar silenciosamente este control.

### ER-04 — Portamembranas / pressure vessels

**Decisión:** `consistente`.

JuanAI debe reconocer `pressure vessel`, `caja de presión` y `portamembrana` como equivalencias controladas y comparar cantidades de forma determinística.

### ER-05 — Conciliación Costeo ↔ APU por partidas

**Decisión:** `discrepancia_comprobada` en al menos una partida relevante.

El sistema no debe validar el APU solamente porque un total final parezca conciliable. Debe comparar cada centro de costo/partida y señalar diferencias antes de consolidar.

Esperado:

- mostrar valor de Costeo;
- mostrar valor de APU;
- mostrar diferencia absoluta y porcentual;
- relacionar cualquier ajuste manual que compense la diferencia;
- requerir revisión humana si el ajuste no posee justificación trazable.

### ER-06 — Resumen económico APU con referencias rotas

**Decisión:** `discrepancia_comprobada`.

El resumen contiene una referencia `#REF!` y referencias a posiciones que no contienen los totales esperados.

JuanAI debe:

- identificar celda y fórmula;
- mostrar la hoja objetivo;
- distinguir referencia inexistente de referencia válida a celda vacía/equivocada;
- marcar los totales derivados afectados;
- agrupar efectos que compartan una misma causa raíz.

Severidad provisional: `critica` cuando la referencia rota alimenta el total contractual.

### ER-07 — Referencias Excel y nombres definidos dañados

**Decisión:**

- referencias rotas del APU: `discrepancia_comprobada`;
- nombres definidos globales inválidos del costeo: `discrepancia_probable` hasta medir impacto.

El costeo contiene nombres globales con referencias inválidas y nombres locales con referencias utilizables. JuanAI debe conservar nombre, ámbito y fórmula y determinar qué definición resuelve una fórmula concreta antes de afirmar que el cálculo económico está incorrecto.

### ER-08 — Fórmula con valor almacenado y dependencias dudosas

**Decisión:** `informacion_insuficiente`.

Si existe un resultado almacenado pero la dependencia que originó el cálculo está dañada o es ambigua, JuanAI puede mostrar el valor cacheado como evidencia histórica, pero no debe presentarlo como cálculo reproducido.

Esperado:

```json
{
  "status": "informacion_insuficiente",
  "calculation_reproduced": false,
  "stored_value_available": true,
  "requires_human_review": true
}
```

### ER-09 — Ajuste manual en total APU

**Decisión:** `discrepancia_comprobada` de trazabilidad.

El APU contiene un ajuste numérico explícito dentro de una fórmula de total.

JuanAI debe:

- detectar el literal;
- identificar la fórmula y celda;
- vincularlo a las partidas potencialmente compensadas;
- preguntar por la autorización del ajuste.

No debe eliminarlo ni corregirlo automáticamente.

Puede transformarse posteriormente en `excepcion_justificada` solo cuando exista respaldo aprobado.

### ER-10 — Conflicto de metadatos en la simulación

**Decisión:** `discrepancia_comprobada`.

La descripción de la revisión contiene parámetros de escenario distintos a los resultados calculados del mismo informe. JuanAI debe mantener separados:

- texto/metadata de revisión;
- resultados calculados;
- diagrama y corrientes del informe.

No debe escoger automáticamente uno como verdadero. Debe generar una pregunta para identificar cuál escenario es el vigente/canónico.

Severidad provisional: `alta` porque afecta el uso de la simulación como fuente de diseño.

### ER-11 — PDFs visuales sin texto extraíble

**Decisión:** no es un hallazgo por sí mismo.

Los documentos químicos pueden requerir procesamiento visual. El sistema debe registrar cobertura, por ejemplo:

```json
{
  "text_layer_available": false,
  "visual_processing_required": true,
  "document_status": "processable_visual"
}
```

Solo usar `documento_ilegible_o_parcial` cuando falle también la ruta visual/OCR o la evidencia obtenida sea insuficiente.

### ER-12 — Alternativas químicas

**Decisión:** `no_aplica` como discrepancia entre alternativas.

Las dos proyecciones representan productos distintos. JuanAI debe mantenerlas como escenarios independientes y nunca sumar las dosis ni convertir una alternativa en regla universal.

### ER-13 — Proyección química vs costeo

**Decisión:** `informacion_insuficiente` hasta confirmar selección y base de cálculo.

Antes de comparar dosis, JuanAI debe resolver:

- producto seleccionado;
- concentración del producto;
- unidad/base de dosis;
- caudal asociado;
- horas de operación por día;
- días de operación incluidos en el costeo;
- si el costeo incluye uno o varios meses.

Sin esos datos, cualquier diferencia se convierte en pregunta, no en incumplimiento.

### ER-14 — Referencia externa faltante

**Decisión para este expediente:** `no_aplica`.

La revisión actual no confirmó con evidencia suficiente una referencia externa faltante que deba formar parte del ground truth de GOLDEN-001. La regla genérica `external_reference_missing` se mantiene en el catálogo de JuanAI para otros expedientes, pero no debe considerarse un error conocido de este caso.

## Casos positivos que el sistema debe preservar

GOLDEN-001 debe contener controles correctos para medir falsos positivos. Como mínimo:

- caudal de alimentación;
- caudal de producto;
- caudal de rechazo;
- cantidad de filtros de pretratamiento;
- tipo/tamaño de filtros;
- cantidad de membranas;
- modelo de membrana en el bloque calculado;
- cantidad de portamembranas.

JuanAI falla el golden set si transforma estos casos correctos en discrepancias sin evidencia adicional.

## Casos negativos conocidos del expediente

Como mínimo:

- referencia rota en resumen APU;
- referencias del resumen que no apuntan al total efectivo esperado;
- propagación del error a total/IVA cuando corresponda;
- discrepancia de al menos una partida Costeo ↔ APU;
- ajuste hardcodeado sin trazabilidad explícita;
- conflicto de metadatos vs resultados calculados en la simulación;
- nombres definidos inválidos que requieren análisis de impacto.

## Reglas de aceptación provisional para SPIKE-001

1. Todos los findings deben tener evidencia localizable.
2. Los casos positivos definidos arriba deben resultar `consistente`.
3. Los errores Excel conocidos deben ser detectados sin LLM.
4. `evidencia_no_encontrada` e `informacion_insuficiente` no se convierten en incumplimiento.
5. Los conflictos de revisión/escenario generan pregunta y revisión humana.
6. Ningún ajuste económico manual queda aceptado automáticamente.
7. Las fórmulas no se consideran recalculadas por el solo hecho de leerlas con una biblioteca de archivos.
8. Los documentos visuales deben pasar por una ruta de cobertura visual antes de declararse ilegibles.

## Salida mínima del SPIKE-001

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

## Estado del ground truth

**Aprobado para desarrollo del spike:** sí, como ground truth provisional.

**Aprobado como criterio corporativo definitivo:** no.

Antes de promover estas reglas a producción, un especialista responsable debe ratificar especialmente:

- C09 Costeo ↔ APU;
- C12/C13 impacto real de nombres definidos del costeo;
- C14/C15 explicación del ajuste y partidas asociadas;
- C17 revisión oficial de la simulación;
- C19 selección y cálculo de químicos.
