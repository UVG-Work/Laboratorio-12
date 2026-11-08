"""Completa la definición editable PBIP del Laboratorio 12.

No modifica las predicciones ni entrena modelos. Puede ejecutarse varias veces.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "powerbi" / "Lab12_Observatorio_v2_final"
REPORT = PROJECT.with_suffix(".Report") / "definition"
MODEL = PROJECT.with_suffix(".SemanticModel") / "definition"
PAGES = REPORT / "pages"
SCHEMA_VC = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json"
NAV = 52  # franja superior con la navegación entre páginas y el botón «Limpiar filtros»
# Mismos colores que las líneas de V9 en todo el informe; azul queda reservado para lo observado.
COLOR = {"Holt-Winters": "#D9661F", "Ingenuo estacional": "#6A4C93", "Suavizado exponencial": "#2A8C82"}


def dump(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def lit(v: str) -> dict:
    return {"expr": {"Literal": {"Value": v}}}


def col(table: str, name: str) -> dict:
    return {"Column": {"Expression": {"SourceRef": {"Entity": table}}, "Property": name}}


def measure(name: str) -> dict:
    return {"Measure": {"Expression": {"SourceRef": {"Entity": "dim_serie"}}, "Property": name}}


def projection(field: dict, query_ref: str, label: str | None = None) -> dict:
    return {"field": field, "queryRef": query_ref, "nativeQueryRef": label or query_ref.rsplit(".", 1)[-1]}


def title(text: str) -> dict:
    return {"title": [{"properties": {"show": lit("true"), "text": lit("'" + text.replace("'", "''") + "'")}}]}


def visual(name: str, kind: str, x: int, y: int, w: int, h: int,
           roles: dict[str, list[dict]], heading: str) -> dict:
    return {"$schema": SCHEMA_VC,
            "name": name, "position": {"x": x, "y": y + NAV, "z": 0, "width": w, "height": h, "tabOrder": 0},
            "visual": {"visualType": kind, "query": {"queryState": {r: {"projections": v} for r, v in roles.items()}},
                       "visualContainerObjects": title(heading), "drillFilterOtherVisuals": True}}


def put(page: str, obj: dict) -> None:
    dump(PAGES / page / "visuals" / obj["name"] / "visual.json", obj)


def in_filter(name: str, table: str, column: str, value: str) -> dict:
    return {"name": name, "field": col(table, column), "type": "Categorical", "filter": {"Version": 2,
            "From": [{"Name": "t", "Entity": table, "Type": 0}],
            "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "t"}},
                       "Property": column}}], "Values": [[{"Literal": {"Value": value}}]]}}}]}}


def only_primary_models(obj: dict) -> dict:
    obj["filterConfig"] = {"filters": [in_filter("solo_tres_modelos", "dim_modelo", "principal", "true")]}
    return obj


def colores_modelo(obj: dict) -> dict:
    obj["visual"]["objects"] = {"dataPoint": [{"properties": {"fill": {"solid": {"color": lit(f"'{c}'")}}},
        "selector": {"data": [{"scopeId": {"Comparison": {"ComparisonKind": 0,
            "Left": col("dim_modelo", "modelo_nombre"), "Right": {"Literal": {"Value": f"'{n}'"}}}}}]}}
        for n, c in COLOR.items()], "labels": [{"properties": {"show": lit("true")}}]}
    return obj


def m(name: str, etiqueta: str | None = None) -> dict:
    p = projection(measure(name), "dim_serie." + name, name)
    if etiqueta:
        p["displayName"] = etiqueta
    return p


def c(table: str, name: str) -> dict:
    return projection(col(table, name), f"{table}.{name}", name)


def slicer(page: str, name: str, table: str, column: str, x: int, w: int, heading: str,
           default: str | None = None) -> None:
    """Lista desplegable; con valor inicial es de selección única para que la vista nunca quede ambigua."""
    s = visual(name, "slicer", x, 4, w, 80,
               {"Values": [projection(col(table, column), f"{table}.{column}", column)]}, heading)
    s["visual"]["objects"] = {"data": [{"properties": {"mode": lit("'Dropdown'")}}],
                              "header": [{"properties": {"show": lit("false")}}],
                              "selection": [{"properties": {"singleSelect": lit("true" if default else "false")}}]}
    if default:  # selección inicial del segmentador
        s["visual"]["objects"]["general"] = [{"properties": {"filter": {"filter":
                                              in_filter(name, table, column, default)["filter"]}}}]
    put(page, s)


def mensaje(page: str, name: str, medida: str, x: int, y: int, w: int) -> None:
    """Tarjeta de texto: vacía cuando hay datos; explica qué hacer cuando la selección no tiene información."""
    v = visual(name, "card", x, y, w, 52, {"Values": [m(medida)]}, "")
    v["visual"].pop("visualContainerObjects")
    v["visual"]["objects"] = {"labels": [{"properties": {"color": {"solid": {"color": lit("'#A84A12'")}},
                                                         "fontSize": lit("12D")}}],
                              "categoryLabels": [{"properties": {"show": lit("false")}}]}
    put(page, v)


def navegacion(page: str) -> None:
    """Navegador de páginas nativo y botón «Limpiar filtros» (acción Borrar todos los segmentadores)."""
    nav = {"$schema": SCHEMA_VC, "name": "navegacion",
           "position": {"x": 20, "y": 8, "z": 1, "width": 900, "height": 36, "tabOrder": 1},
           "visual": {"visualType": "pageNavigator", "drillFilterOtherVisuals": True}}
    sel = {"id": "default"}
    boton = {"$schema": SCHEMA_VC, "name": "limpiar_filtros",
             "position": {"x": 1100, "y": 8, "z": 1, "width": 160, "height": 36, "tabOrder": 2},
             "visual": {"visualType": "actionButton", "drillFilterOtherVisuals": True,
                        "objects": {"icon": [{"properties": {"shapeType": lit("'blank'")}, "selector": sel}],
                                    "text": [{"properties": {"show": lit("true"), "text": lit("'↺ Limpiar filtros'"),
                                                            "fontColor": {"solid": {"color": lit("'#1F4E79'")}}},
                                              "selector": sel}],
                                    "outline": [{"properties": {"show": lit("true"),
                                                               "lineColor": {"solid": {"color": lit("'#1F4E79'")}}},
                                                 "selector": sel}]},
                        "visualContainerObjects": {"visualLink": [{"properties": {"show": lit("true"),
                                                                                  "type": lit("'ClearAllSlicers'")}}]}}}
    put(page, nav)
    put(page, boton)


def desplazar(page: str) -> None:
    """Baja los visuales que no regenera este script (Panorama) para dejar sitio a la franja de navegación."""
    if (PAGES / page / "visuals" / "navegacion").exists():
        return
    for f in (PAGES / page / "visuals").glob("*/visual.json"):
        obj = json.loads(f.read_text(encoding="utf-8"))
        obj["position"]["y"] += NAV
        dump(f, obj)


def page(name: str, display: str, interactions: list[tuple[str, str]] = [],
         ignorar: list[tuple[str, str]] = []) -> None:
    dump(PAGES / name / "page.json",
         {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.0.0/schema.json",
          "name": name, "displayName": display, "displayOption": "FitToPage", "height": 720 + NAV, "width": 1280,
          "visualInteractions": [{"source": a, "target": b, "type": "DataFilter"} for a, b in interactions]
                               + [{"source": a, "target": b, "type": "NoFilter"} for a, b in ignorar]})


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


def add_ux_measures() -> None:
    """Medidas de interfaz: detalle de un solo año y mensajes cuando la selección no tiene datos."""
    path = MODEL / "tables" / "dim_serie.tmdl"
    source = path.read_text(encoding="utf-8")
    # Una tarjeta mostraría «(Blank)»; con texto vacío queda invisible cuando sí hay datos.
    source = source.replace('Revise la serie o el rango de años.",\n\t\t\t     BLANK () )',
                            'Revise la serie o el rango de años.",\n\t\t\t     "" )')
    if "\tmeasure 'Viajeros del año elegido'" not in source:
        dax = '''
	measure 'Viajeros del año elegido' =
			IF ( HASONEVALUE ( dim_fecha[anio] ), [Viajeros] )
		formatString: #,0

	measure 'Mensaje detalle' =
			IF ( NOT HASONEVALUE ( dim_fecha[anio] ), "Elija un año para ver sus meses.",
			     IF ( ISBLANK ( [Viajeros] ), "No hay registros para esta selección. Revise la serie o el año.", "" ) )

	measure 'Mensaje pronósticos' =
			IF ( ISBLANK ( [MAPE evaluación] ),
			     "Sin pronósticos: No residentes es una serie derivada, sin modelos.", "" )
'''
        source = source.replace("\n\tcolumn serie_id", "\n" + dax + "\n\tcolumn serie_id", 1)
    path.write_text(source, encoding="utf-8")


def main() -> None:
    # Ruta de los CSV en esta copia del repositorio. En otro equipo: Desktop → Editar parámetros → RutaDatos.
    route = str(ROOT / "datos_powerbi") + "\\"
    expr = MODEL / "expressions.tmdl"
    text = expr.read_text(encoding="utf-8")
    text = text.replace(text.split('expression RutaDatos = ', 1)[1].split(' meta ', 1)[0], '"' + route + '"', 1)
    expr.write_text(text, encoding="utf-8")
    add_measures()
    add_ux_measures()

    # Conserva V1-V3 del avance, con su jerarquía y sus interacciones comprobadas.
    page("panorama", "1 · Panorama", [(a, b) for a in ("v2barras", "v3columnas") for b in ("v1linea", "v2barras", "v3columnas") if a != b])
    desplazar("panorama")
    seg = PAGES / "panorama" / "visuals" / "segmento_anio" / "visual.json"
    obj = json.loads(seg.read_text(encoding="utf-8"))
    obj["visual"]["query"]["queryState"]["Values"]["projections"][0]["displayName"] = "Años"
    dump(seg, obj)
    for nombre, n in (("v1linea", 1), ("v2barras", 2), ("v3columnas", 3)):  # numeración igual que V4-V10
        f = PAGES / "panorama" / "visuals" / nombre / "visual.json"
        obj = json.loads(f.read_text(encoding="utf-8"))
        t = obj["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"]["expr"]["Literal"]
        if not t["Value"].startswith("'V"):
            t["Value"] = f"'V{n} · " + t["Value"][1:]
        dump(f, obj)

    page("detalle", "2 · Detalle mensual")
    slicer("detalle", "seleccion_anio", "dim_fecha", "anio", 20, 300, "Elija un año", "2025L")
    slicer("detalle", "seleccion_serie", "dim_serie", "serie", 340, 400, "Elija una serie", "'Total'")
    mensaje("detalle", "mensaje_detalle", "Mensaje detalle", 760, 24, 500)
    v4 = visual("v4detalle", "clusteredColumnChart", 20, 105, 1240, 595,
                {"Category": [c("dim_fecha", "mes")], "Y": [m("Viajeros del año elegido")]},
                "V4 · ¿En qué mes del año elegido subió o bajó el flujo?")
    v4["visual"]["objects"] = {"labels": [{"properties": {"show": lit("true")}}]}
    put("detalle", v4)

    # V7 compara siempre todas las series en 2025/2019: los segmentadores de la página no la filtran.
    page("calendario", "3 · Calendario y mercados", [("v5calendario", "v6estacional"), ("v7recuperacion", "v5calendario")],
         [("seleccion_serie_cal", "v7recuperacion"), ("seleccion_anio_cal", "v7recuperacion")])
    slicer("calendario", "seleccion_serie_cal", "dim_serie", "serie", 20, 400, "Serie (V5 y V6)", "'Total'")
    slicer("calendario", "seleccion_anio_cal", "dim_fecha", "anio", 440, 300, "Años (V5 y V6)")
    mensaje("calendario", "mensaje_calendario", "Mensaje sin datos", 760, 24, 500)
    put("calendario", visual("v5calendario", "lineChart", 20, 105, 620, 280,
                             {"Category": [c("dim_fecha", "fecha")], "Y": [m("Viajeros")]},
                             "V5 · ¿Cómo varía el flujo mes a mes?"))
    put("calendario", visual("v6estacional", "clusteredColumnChart", 650, 105, 610, 280,
                             {"Category": [c("dim_fecha", "mes")], "Y": [m("Promedio mensual por año")]},
                             "V6 · ¿En qué meses se concentra el flujo?"))
    v7 = visual("v7recuperacion", "clusteredBarChart", 20, 400, 1240, 300,
                {"Category": [c("dim_serie", "serie")], "Y": [m("Nivel 2025 frente a 2019")]},
                "V7 · Nivel de 2025 frente a 2019 (%) · la línea 100 = igual que 2019")
    v7["visual"]["objects"] = {"labels": [{"properties": {"show": lit("true")}}],
                               "y1AxisReferenceLine": [{"properties": {"show": lit("true"), "value": lit("100D"),
                                   "lineColor": {"solid": {"color": lit("'#D9661F'")}}, "style": lit("'dashed'"),
                                   "displayName": lit("'Nivel de 2019'"), "dataLabelShow": lit("true")},
                                   "selector": {"id": "1"}}]}
    put("calendario", v7)

    page("pronosticos", "4 · Pronósticos")
    slicer("pronosticos", "seleccion_serie_pred", "dim_serie", "serie", 20, 340, "Serie (vacío = Total)", "'Total'")
    slicer("pronosticos", "seleccion_prueba", "dim_prueba", "prueba_nombre", 380, 420, "Evaluación (vacío = Post-pandemia)",
           "'Post-pandemia'")
    mensaje("pronosticos", "mensaje_pronosticos", "Mensaje pronósticos", 830, 24, 430)
    put("pronosticos", colores_modelo(only_primary_models(visual("v8mape", "clusteredBarChart", 20, 105, 610, 265,
                              {"Category": [c("dim_modelo", "modelo_nombre")], "Y": [m("MAPE evaluación")]},
                              "V8 · Error porcentual medio (MAPE, %) · menor es mejor"))))
    put("pronosticos", colores_modelo(only_primary_models(visual("v8mae", "clusteredBarChart", 650, 105, 610, 265,
                              {"Category": [c("dim_modelo", "modelo_nombre")], "Y": [m("MAE evaluación")]},
                              "V8b · Error absoluto medio (MAE, viajeros por mes)"))))
    put("pronosticos", visual("v9pronosticos", "lineChart", 20, 380, 720, 320,
                              {"Category": [c("dim_fecha", "fecha")], "Y": [m("Real evaluación", "Observado"),
                                                                              m("Pronóstico Holt-Winters", "Holt-Winters"),
                                                                              m("Pronóstico ingenuo estacional", "Ingenuo estacional"),
                                                                              m("Pronóstico suavizado simple", "Suavizado exponencial")]},
                              "V9 · Observado y predicciones importadas"))
    v10 = visual("v10error", "clusteredColumnChart", 750, 380, 510, 320,
                 {"Category": [c("dim_fecha", "fecha")], "Y": [m("Error mensual evaluación")]},
                 "V10 · Error del ingenuo estacional (+ sobreestima)")
    v10["visual"]["objects"] = {"dataPoint": [{"properties": {"fill": {"solid": {"color": lit("'#6A4C93'")}}}}]}
    put("pronosticos", v10)

    for pg in ("panorama", "detalle", "calendario", "pronosticos"):
        navegacion(pg)
    dump(PAGES / "pages.json", {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
                               "pageOrder": ["panorama", "detalle", "calendario", "pronosticos"], "activePageName": "panorama"})
    print("Proyecto PBIP actualizado: 11 visualizaciones en 4 páginas (V1-V10 + V8b), navegación y mensajes.")


if __name__ == "__main__":
    main()
