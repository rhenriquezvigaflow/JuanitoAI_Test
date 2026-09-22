# GOLDEN-001 — Inventario del expediente

> Este repositorio es público. No versionar nombres de cliente, precios, credenciales, documentos originales ni valores de diseño sensibles. La relación entre los alias usados aquí y los archivos originales debe mantenerse en almacenamiento privado aprobado.

## Objetivo

Preparar el primer expediente de referencia para validar el flujo de JuanAI antes del desarrollo completo del MVP. El caso debe permitir probar lectura documental, conciliación entre fuentes, reglas determinísticas y evidencia localizable.

## Alcance documental

| Alias | Tipo | Rol en el análisis | Spike 1 | Observaciones |
| --- | --- | --- | --- | --- |
| `DOC-PFD-001` | PDF / PFD | Diseño y flujo de proceso | Sí | Documento visual; conservar página y región como evidencia |
| `DOC-SIM-001` | PDF / simulación | Corrida de membranas y parámetros de proceso | Sí | Conservar revisión, escenario, unidades, avisos y página |
| `DOC-COST-001` | XLSX / costeo | Costeo maestro, equipos, cantidades, monedas y fórmulas | Sí | No ejecutar macros; preservar fórmula y valor almacenado |
| `DOC-APU-001` | XLSX / APU | Resumen económico y consolidación por partidas | Sí | Validar referencias entre hojas, subtotales y ajustes |
| `DOC-CHEM-001` | PDF visual | Alternativa de proyección química | No, Spike 2 | Requiere ruta visual/OCR si no existe texto extraíble |
| `DOC-CHEM-002` | PDF visual | Segunda alternativa de proyección química | No, Spike 2 | Mantener alternativas separadas; no sumarlas automáticamente |

## Metadatos que deben mantenerse fuera de Git

Para cada alias registrar en el almacenamiento privado:

- nombre original del archivo;
- hash SHA-256;
- revisión y fecha;
- propietario o responsable;
- clasificación de confidencialidad;
- ubicación privada aprobada;
- estado de proceso;
- cobertura de extracción;
- advertencias o errores de lectura;
- relación con documentos reemplazados o vigentes.

## Alcance del Spike 1

El primer spike trabajará únicamente con:

1. `DOC-PFD-001`;
2. `DOC-SIM-001`;
3. `DOC-COST-001`;
4. `DOC-APU-001`.

El objetivo no es determinar si la propuesta completa está correcta, sino demostrar que JuanAI puede:

- extraer datos relevantes;
- normalizar equipos, cantidades y parámetros;
- comparar fuentes heterogéneas;
- ejecutar reglas reproducibles;
- distinguir discrepancia, falta de evidencia y excepción;
- entregar evidencia localizable por página, región, hoja y celda.

## Condiciones para declarar GOLDEN-001 preparado

- [ ] TI confirmó dónde se almacenan los originales.
- [ ] TI confirmó qué datos pueden enviarse a modelos de IA.
- [ ] Los seis documentos tienen alias, hash, revisión y clasificación.
- [ ] El especialista técnico/comercial responsable está asignado.
- [ ] La matriz de validación fue revisada por el especialista.
- [ ] Los resultados esperados fueron aprobados como ground truth inicial.
- [ ] Ningún documento o dato confidencial fue agregado a Git.
