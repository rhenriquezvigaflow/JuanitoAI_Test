"""Auditoria local sin cargar la app, credenciales ni llamar proveedores.

Ejecuta funciones de ingesta extraidas por AST, sin modificar el fuente.
No constituye una prueba integral de la aplicacion.
"""
import ast
import argparse
import hashlib
import json
import logging
from pathlib import Path
import tempfile

import openpyxl

OUT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Raiz de la copia autorizada de ECO v0.6.9")
    args = parser.parse_args()
    ROOT = args.source.resolve()
    if not (ROOT / "engine/backend/pipeline/executor.py").is_file():
        parser.error("La ruta debe contener engine/backend/pipeline/executor.py")
    parsed = {}
    errors = []
    for path in ROOT.rglob("*.py"):
        try:
            parsed[path] = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except Exception as exc:
            errors.append({"file": str(path.relative_to(ROOT)), "error": str(exc)})
    json_files = list(ROOT.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            errors.append({"file": str(path.relative_to(ROOT)), "error": str(exc)})

    executor = ROOT / "engine/backend/pipeline/executor.py"
    wanted = {"dedupe_files_by_content", "_load_stream_chunks"}
    nodes = [n for n in parsed[executor].body if isinstance(n, ast.FunctionDef) and n.name in wanted]
    assert len(nodes) == 2
    namespace = {"Path": Path, "log": logging.getLogger("audit"), "_STREAM_ROL": {"oferta": "oferta_tecnica"}}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(executor), "exec"), namespace)

    with tempfile.TemporaryDirectory(prefix="fixture_costeo_", dir=OUT) as temp:
        folder = Path(temp)
        book = openpyxl.Workbook()
        sheet = book.active
        sheet.title = "Costeo"
        sheet.append(["Descripcion", "Cantidad", "Precio", "Subtotal"])
        sheet.append(["Bomba principal de proceso", 0, 100, "=B2*C2"])
        sheet.append(["Bomba auxiliar de proceso", 2, 100, 200])
        book.save(folder / "costeo_sintetico.xlsx")
        failures = []
        chunks = namespace["_load_stream_chunks"](folder, "oferta", out_failures=failures)
        assert not failures and len(chunks) == 2
        first = chunks[0]
        assert "Cantidad:" not in first["text"]
        assert "Subtotal:" not in first["text"]
        assert "row_range" not in first
        assert "Precio: 100" in first["text"]

    imports = sorted({
        alias.name.split(".")[0]
        for tree in parsed.values() for node in ast.walk(tree)
        if isinstance(node, ast.Import) for alias in node.names
    } | {
        node.module.split(".")[0]
        for tree in parsed.values() for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    })
    report = {
        "source": str(ROOT),
        "source_executor_sha256": hashlib.sha256(executor.read_bytes()).hexdigest(),
        "python_parsed": len(parsed),
        "json_checked": len(json_files),
        "syntax_errors": errors,
        "imports": imports,
        "fixture": {
            "type": "synthetic XLSX; actual ingestion functions extracted through AST",
            "openpyxl_version": openpyxl.__version__,
            "first_chunk": first,
            "zero_quantity_omitted": True,
            "formula_without_cached_value_omitted": True,
            "row_locator_absent": True,
            "note": "No runtime app, LLM, PDF, UI, permissions or load tests performed.",
        },
    }
    (OUT / "verificacion_codigo.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["python_parsed", "json_checked", "syntax_errors"]}))
    print("XLSX: reproduced zero omission, missing uncached formula result and missing row locator.")


if __name__ == "__main__":
    main()
