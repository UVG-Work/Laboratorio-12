"""Completa la definición editable PBIP del Laboratorio 12.

No modifica las predicciones ni entrena modelos. Puede ejecutarse varias veces.
"""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "powerbi" / "Lab12_Observatorio_v2_final"
REPORT = PROJECT.with_suffix(".Report") / "definition"
MODEL = PROJECT.with_suffix(".SemanticModel") / "definition"
PAGES = REPORT / "pages"


def dump(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def col(table: str, name: str) -> dict:
    return {"Column": {"Expression": {"SourceRef": {"Entity": table}}, "Property": name}}


def measure(name: str) -> dict:
    return {"Measure": {"Expression": {"SourceRef": {"Entity": "dim_serie"}}, "Property": name}}


def projection(field: dict, query_ref: str, label: str | None = None) -> dict:
    return {"field": field, "queryRef": query_ref, "nativeQueryRef": label or query_ref.rsplit(".", 1)[-1]}


def title(text: str) -> dict:
    return {"title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}},
                                       "text": {"expr": {"Literal": {"Value": "'" + text.replace("'", "''") + "'"}}}}}]}


def visual(name: str, kind: str, x: int, y: int, w: int, h: int,
           roles: dict[str, list[dict]], heading: str) -> dict:
    return {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json",
            "name": name, "position": {"x": x, "y": y, "z": 0, "width": w, "height": h, "tabOrder": 0},
            "visual": {"visualType": kind, "query": {"queryState": {r: {"projections": v} for r, v in roles.items()}},
                       "visualContainerObjects": title(heading), "drillFilterOtherVisuals": True}}


def put(page: str, obj: dict) -> None:
    dump(PAGES / page / "visuals" / obj["name"] / "visual.json", obj)


def only_primary_models(obj: dict) -> dict:
    obj["filterConfig"] = {"filters": [{"name": "solo_tres_modelos", "field": col("dim_modelo", "principal"),
        "type": "Categorical", "filter": {"Version": 2,
        "From": [{"Name": "m", "Entity": "dim_modelo", "Type": 0}],
        "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "m"}},
            "Property": "principal"}}], "Values": [[{"Literal": {"Value": "true"}}]]}}}]}}]}
    return obj


def slicer(page: str, name: str, table: str, column: str, x: int, w: int, heading: str) -> None:
    s = visual(name, "slicer", x, 12, w, 76,
               {"Values": [projection(col(table, column), f"{table}.{column}", column)]}, heading)
    put(page, s)


def page(name: str, display: str, interactions: list[tuple[str, str]] = []) -> None:
    dump(PAGES / name / "page.json",
         {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.0.0/schema.json",
          "name": name, "displayName": display, "displayOption": "FitToPage", "height": 720, "width": 1280,
          "visualInteractions": [{"source": a, "target": b, "type": "DataFilter"} for a, b in interactions]})


def m(name: str) -> dict:
    return projection(measure(name), "dim_serie." + name, name)


def c(table: str, name: str) -> dict:
    return projection(col(table, name), f"{table}.{name}", name)


def add_measures() -> None:
    path = MODEL / "tables" / "dim_serie.tmdl"
    source = path.read_text(encoding="utf-8")
    marker = "\n\tcolumn serie_id"
    if "\tmeasure 'Nivel 2025 frente a 2019'" in source:
        return
    dax = r'''
	measure 'Nivel 2025 frente a 2019' =
			VAR base = CALCULATE ( [Viajeros], REMOVEFILTERS ( dim_fecha ), dim_fecha[anio] = 2019 )
			VAR actual = CALCULATE ( [Viajeros], REMOVEFILTERS ( dim_fecha ), dim_fecha[anio] = 2025 )
			RETURN IF ( SELECTEDVALUE ( dim_serie[serie_id] ) = "gt", BLANK (), DIVIDE ( actual, base ) * 100 )
		formatString: 0.0

	measure 'Promedio mensual por año' =
			AVERAGEX ( VALUES ( dim_fecha[anio] ), [Viajeros] )
		formatString: #,0

	measure 'MAPE evaluación' =
			VAR s = IF ( HASONEVALUE ( dim_serie[serie_id] ), SELECTEDVALUE ( dim_serie[serie_id] ), "total" )
			VAR p = IF ( HASONEVALUE ( dim_prueba[prueba] ), SELECTEDVALUE ( dim_prueba[prueba] ), "post-pandemia" )
			RETURN CALCULATE ( MAX ( fact_metricas[MAPE] ), dim_serie[serie_id] = s, dim_prueba[prueba] = p )
		formatString: 0.00

	measure 'MAE evaluación' =
			VAR s = IF ( HASONEVALUE ( dim_serie[serie_id] ), SELECTEDVALUE ( dim_serie[serie_id] ), "total" )
			VAR p = IF ( HASONEVALUE ( dim_prueba[prueba] ), SELECTEDVALUE ( dim_prueba[prueba] ), "post-pandemia" )
			RETURN CALCULATE ( MAX ( fact_metricas[MAE] ), dim_serie[serie_id] = s, dim_prueba[prueba] = p )
		formatString: #,0.00

	measure 'Real evaluación' =
			VAR s = IF ( HASONEVALUE ( dim_serie[serie_id] ), SELECTEDVALUE ( dim_serie[serie_id] ), "total" )
			VAR p = IF ( HASONEVALUE ( dim_prueba[prueba] ), SELECTEDVALUE ( dim_prueba[prueba] ), "post-pandemia" )
			RETURN CALCULATE ( MAX ( fact_predicciones[real] ), dim_serie[serie_id] = s, dim_prueba[prueba] = p )
		formatString: #,0

	measure 'Pronóstico Holt-Winters' =
			VAR s = IF ( HASONEVALUE ( dim_serie[serie_id] ), SELECTEDVALUE ( dim_serie[serie_id] ), "total" )
			VAR p = IF ( HASONEVALUE ( dim_prueba[prueba] ), SELECTEDVALUE ( dim_prueba[prueba] ), "post-pandemia" )
			RETURN CALCULATE ( MAX ( fact_predicciones[pronostico] ), dim_serie[serie_id] = s, dim_prueba[prueba] = p, dim_modelo[modelo_id] = 1 )
		formatString: #,0

	measure 'Pronóstico ingenuo estacional' =
			VAR s = IF ( HASONEVALUE ( dim_serie[serie_id] ), SELECTEDVALUE ( dim_serie[serie_id] ), "total" )
			VAR p = IF ( HASONEVALUE ( dim_prueba[prueba] ), SELECTEDVALUE ( dim_prueba[prueba] ), "post-pandemia" )
			RETURN CALCULATE ( MAX ( fact_predicciones[pronostico] ), dim_serie[serie_id] = s, dim_prueba[prueba] = p, dim_modelo[modelo_id] = 17 )
		formatString: #,0

	measure 'Pronóstico suavizado simple' =
			VAR s = IF ( HASONEVALUE ( dim_serie[serie_id] ), SELECTEDVALUE ( dim_serie[serie_id] ), "total" )
			VAR p = IF ( HASONEVALUE ( dim_prueba[prueba] ), SELECTEDVALUE ( dim_prueba[prueba] ), "post-pandemia" )
			RETURN CALCULATE ( MAX ( fact_predicciones[pronostico] ), dim_serie[serie_id] = s, dim_prueba[prueba] = p, dim_modelo[modelo_id] = 18 )
		formatString: #,0

	measure 'Error mensual evaluación' =
			VAR s = IF ( HASONEVALUE ( dim_serie[serie_id] ), SELECTEDVALUE ( dim_serie[serie_id] ), "total" )
			VAR p = IF ( HASONEVALUE ( dim_prueba[prueba] ), SELECTEDVALUE ( dim_prueba[prueba] ), "post-pandemia" )
			RETURN CALCULATE ( MAX ( fact_predicciones[error] ), dim_serie[serie_id] = s, dim_prueba[prueba] = p, dim_modelo[modelo_id] = 17 )
		formatString: #,0
'''
    path.write_text(source.replace(marker, "\n" + dax + marker, 1), encoding="utf-8")


def main() -> None:
    # Ruta fija para la copia del repositorio solicitada por el usuario. Se puede cambiar como parámetro en Desktop.
    route = str(Path(r"C:\Users\sebas\OneDrive\Escritorio\Github\Data sciencie\Laboratorio-12\Lab12_PowerBI\datos_powerbi")) + "\\"
    expr = MODEL / "expressions.tmdl"
    text = expr.read_text(encoding="utf-8")
    text = text.replace(text.split('expression RutaDatos = ', 1)[1].split(' meta ', 1)[0], json.dumps(route, ensure_ascii=False), 1)
    expr.write_text(text, encoding="utf-8")
    add_measures()

    # Conserva V1-V3 del avance, con su jerarquía y sus interacciones comprobadas.
    page("panorama", "1 · Panorama", [(a, b) for a in ("v2barras", "v3columnas") for b in ("v1linea", "v2barras", "v3columnas") if a != b])
    page("detalle", "2 · Detalle mensual")
    slicer("detalle", "seleccion_anio", "dim_fecha", "anio", 20, 300, "Elija un año")
    slicer("detalle", "seleccion_serie", "dim_serie", "serie", 340, 460, "Elija una serie")
    put("detalle", visual("v4detalle", "clusteredColumnChart", 20, 105, 1240, 595,
                          {"Category": [c("dim_fecha", "mes")], "Y": [m("Viajeros")]},
                          "V4 · ¿En qué mes cambió el flujo? Use el filtro de año"))

    page("calendario", "3 · Calendario y mercados", [("v5calendario", "v6estacional"), ("v7recuperacion", "v5calendario")])
    slicer("calendario", "seleccion_serie_cal", "dim_serie", "serie", 20, 440, "Serie")
    slicer("calendario", "seleccion_anio_cal", "dim_fecha", "anio", 480, 360, "Año")
    put("calendario", visual("v5calendario", "lineChart", 20, 105, 620, 280,
                             {"Category": [c("dim_fecha", "fecha")], "Y": [m("Viajeros")]},
                             "V5 · ¿Cómo varía el flujo mes a mes?"))
    put("calendario", visual("v6estacional", "clusteredColumnChart", 650, 105, 610, 280,
                             {"Category": [c("dim_fecha", "mes")], "Y": [m("Promedio mensual por año")]},
                             "V6 · ¿En qué meses se concentra el flujo?"))
    put("calendario", visual("v7recuperacion", "clusteredBarChart", 20, 400, 1240, 300,
                             {"Category": [c("dim_serie", "serie")], "Y": [m("Nivel 2025 frente a 2019")]},
                             "V7 · Nivel de 2025 frente a 2019 (%) · 100 = igual"))

    page("pronosticos", "4 · Pronósticos")
    slicer("pronosticos", "seleccion_serie_pred", "dim_serie", "serie", 20, 440, "Serie con modelos")
    slicer("pronosticos", "seleccion_prueba", "dim_prueba", "prueba_nombre", 480, 500, "Conjunto de evaluación")
    put("pronosticos", only_primary_models(visual("v8mape", "clusteredBarChart", 20, 105, 610, 265,
                              {"Category": [c("dim_modelo", "modelo_nombre")], "Y": [m("MAPE evaluación")]},
                              "V8 · MAPE (%) por modelo · menor es mejor")))
    put("pronosticos", only_primary_models(visual("v8mae", "clusteredBarChart", 650, 105, 610, 265,
                              {"Category": [c("dim_modelo", "modelo_nombre")], "Y": [m("MAE evaluación")]},
                              "V8b · Error absoluto medio (viajeros)")))
    put("pronosticos", visual("v9pronosticos", "lineChart", 20, 380, 790, 320,
                              {"Category": [c("dim_fecha", "fecha")], "Y": [m("Real evaluación"), m("Pronóstico Holt-Winters"),
                                                                              m("Pronóstico ingenuo estacional"), m("Pronóstico suavizado simple")]},
                              "V9 · Observado y predicciones importadas"))
    put("pronosticos", visual("v10error", "clusteredColumnChart", 820, 380, 440, 320,
                              {"Category": [c("dim_fecha", "fecha")], "Y": [m("Error mensual evaluación")]},
                              "V10 · Error mensual del ingenuo estacional (pronóstico - real)"))
    dump(PAGES / "pages.json", {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
                               "pageOrder": ["panorama", "detalle", "calendario", "pronosticos"], "activePageName": "panorama"})
    print("Proyecto PBIP actualizado: 11 visualizaciones en 4 páginas (V1-V10 + V8b).")


if __name__ == "__main__":
    main()
