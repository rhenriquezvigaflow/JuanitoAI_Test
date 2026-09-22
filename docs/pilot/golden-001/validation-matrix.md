# GOLDEN-001 — Matriz de validación

> Matriz inicial basada en el expediente real revisado. Los valores sensibles o que identifiquen directamente al cliente no se versionan en este repositorio público. Los localizadores exactos del caso real se mantienen en el almacenamiento privado del piloto.
>
> **Estado de esta revisión:** evaluación experta simulada para construir el piloto. Sirve como ground truth provisional de desarrollo, pero no reemplaza la aprobación de un especialista responsable de Proceso/Ingeniería/Costos.

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

## Decisión experta simulada

| ID | Control | Fuente A | Fuente B | Tipo | Decisión provisional | Severidad | Acción |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | Caudal de alimentación del proceso vs simulación | PFD | Simulación | Determinístico | `consistente` | baja | Usar como caso positivo del golden set |
| C02 | Caudal de producto vs simulación | PFD | Simulación | Determinístico | `consistente` | baja | Usar como caso positivo del golden set |
| C03 | Caudal de rechazo vs simulación | PFD | Simulación | Determinístico | `consistente` | baja | Usar como caso positivo del golden set |
| C04 | Cantidad de filtros de pretratamiento | PFD | Costeo | Extracción visual + regla | `consistente` | baja | Validar por objetos/regiones, no por conteo de texto |
| C05 | Tipo/tamaño de filtros de pretratamiento | PFD | Costeo | Matching + regla | `consistente` | baja | Crear alias controlado de nomenclatura |
| C06 | Cantidad de elementos de membrana | Simulación | Costeo | Determinístico | `consistente` | baja | Usar como caso positivo del golden set |
| C07 | Modelo de membrana | Simulación | Costeo | Determinístico | `consistente` usando el detalle calculado | baja | El conflicto de metadatos se gestiona en C17 |
| C08 | Cantidad de portamembranas / pressure vessels | Simulación | Costeo | Determinístico | `consistente` | baja | Registrar equivalencia terminológica aprobada |
| C09 | Cobertura y valores de centros de costo de suministro | Costeo | APU | Determinístico | `discrepancia_comprobada` a nivel de partida; el total agregado puede reconciliarse por un ajuste | alta | No aceptar conciliación solo porque el total final coincida |
| C10 | Integridad de referencias entre hojas del resumen APU | APU | APU | Determinístico | `discrepancia_comprobada` | crítica | Bloquear uso del resumen como salida final hasta corregir referencias |
| C11 | Fórmulas con referencias inválidas en el APU | APU | — | Determinístico | `discrepancia_comprobada` | crítica | Reportar causa raíz y dependencias; no reparar automáticamente |
| C12 | Nombres definidos con referencias inválidas en el costeo | Costeo | — | Determinístico | `discrepancia_probable` | media | Existen nombres globales inválidos y nombres locales utilizables; medir impacto antes de declarar costos incorrectos |
| C13 | Fórmula con valor almacenado y dependencia potencialmente dañada | Costeo | — | Determinístico | `informacion_insuficiente` | media | Verificar en Excel o motor compatible qué nombre/ámbito resuelve realmente la fórmula |
| C14 | Ajuste manual numérico dentro del total APU | APU | Costeo | Determinístico | `discrepancia_comprobada` de trazabilidad | alta | Exigir justificación y autorización; puede transformarse en `excepcion_justificada` solo con respaldo |
| C15 | Partida de suministro con valor reutilizado/duplicado frente al costeo | APU | Costeo | Determinístico + revisión | `discrepancia_comprobada` | alta | Corregir partida o documentar excepción; relacionar con C14 |
| C16 | Referencia a fuente externa no incluida | Costeo | Fuente externa | Determinístico | `no_aplica` al GOLDEN-001 actual | — | La inspección actual no confirma este caso; conservar la regla genérica para otros expedientes |
| C17 | Metadatos de revisión de simulación vs resultados calculados del mismo informe | Simulación | Simulación | Determinístico | `discrepancia_comprobada` | alta | Confirmar cuál escenario/revisión es canónico antes de usar la simulación como fuente oficial |
| C18 | Dos alternativas de producto químico | Proyección química A | Proyección química B | Clasificación contextual | `no_aplica` como discrepancia | — | Mantener escenarios separados; no sumarlos ni tratarlos como contradicción |
| C19 | Dosis química vs costeo | Proyección química | Costeo | Regla + contexto | `informacion_insuficiente` | alta | Falta confirmar producto seleccionado, base de dosis y período operativo del costeo |
| C20 | PDF sin texto extraíble pero legible visualmente | PDF visual | — | Cobertura | `no_aplica` como hallazgo | — | Registrar `visual_required` en cobertura; solo usar `documento_ilegible_o_parcial` si falla también la ruta visual/OCR |

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

## Tolerancias propuestas para el piloto

Estas tolerancias son de trabajo y deben ser aprobadas por los especialistas antes de transformarse en reglas corporativas.

| Familia | Tolerancia propuesta |
| --- | --- |
| Cantidades discretas de equipos | Igualdad exacta después de resolver alcance, reserva y suministro del cliente |
| Caudales | ±0,1 m³/h o ±0,5 %, el mayor de ambos, después de normalizar unidades |
| Modelo/código de equipo | Igualdad del identificador canónico; alias solo mediante catálogo aprobado |
| Totales monetarios | Misma moneda y base; tolerancia de redondeo ±1 unidad monetaria o ±0,1 %, el mayor de ambos |
| Referencias Excel usadas en salidas finales | Tolerancia cero para `#REF!`, referencia inexistente o fórmula que apunte a una celda vacía cuando existe un total oficial en otra ubicación |
| Revisión/escenario | Debe existir relación explícita con la revisión oficial; conflictos de metadatos requieren revisión humana |
| Químicos | No comparar dosis hasta igualar producto, concentración, base de dosificación, horas/día, días considerados y escenario |

## Reglas de decisión

1. Los controles aritméticos, referencias, cantidades y unidades se ejecutan en código.
2. El LLM puede ayudar a interpretar nombres, planos y contexto, pero no decide por sí solo una discrepancia económica crítica.
3. Una excepción solo queda cerrada cuando un revisor autorizado la acepta.
4. Cada hallazgo debe conservar la versión de documento, regla, extractor y evaluación que lo originó.
5. Una corrección genera una nueva evaluación; no se sobrescribe el resultado aprobado anterior.
6. Coincidencia de un total agregado no anula una discrepancia de partida ni un ajuste manual no explicado.
7. Cobertura documental se registra aparte del estado del hallazgo; un PDF visual sin capa de texto no es automáticamente ilegible.
