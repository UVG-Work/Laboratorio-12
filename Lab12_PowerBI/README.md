# Laboratorio 12 — Observatorio de turismo en Power BI

Segunda versión del cuadro de mando del Laboratorio 10 (Streamlit + Plotly), ahora en Power BI Desktop. No se entrenan modelos: se importan las predicciones y métricas del Laboratorio 1/10.

## Estructura

```
Lab12_PowerBI/
├── datos_powerbi/            # Modelo en estrella listo para Power BI (CSV UTF-8, punto decimal)
│   ├── dim_serie.csv         # 8 series (7 modeladas + no residentes)
│   ├── dim_fecha.csv         # ene-2009 a jun-2026 (año, trimestre, mes, periodo)
│   ├── dim_modelo.csv        # 18 modelos; columna principal = los 3 comparados
│   ├── dim_prueba.csv        # 70/30 y post-pandemia
│   ├── fact_observado.csv    # viajeros por serie y mes
│   ├── fact_predicciones.csv # TABLA DE PREDICCIONES: real, pronóstico y error por serie, prueba, modelo y mes
│   └── fact_metricas.csv     # TABLA DE MÉTRICAS: MAE, RMSE y MAPE de resultados.json
├── powerbi/
│   ├── tema_observatorio.json      # paleta del observatorio (Vista → Temas → Examinar temas)
│   ├── Lab12_Observatorio_v1_avance.pbix   # informe del avance
│   └── Lab12_Observatorio_v1_avance.pbip   # mismo informe como proyecto de texto (TMDL + PBIR)
├── scripts/
│   ├── preparar_datos_powerbi.py   # regenera datos_powerbi/ desde Notebooks/resultados
│   ├── generar_pbip.py             # genera el .pbip del avance (modelo, medidas, V1–V3 e interacciones)
│   ├── bosquejos.py                # figuras del documento de diseño
│   └── generar_avance_pdf.py       # docs/Lab12_Avance.pdf (inserta docs/capturas/*.png)
├── docs/
│   ├── Lab12_Avance.pdf
│   ├── img/                        # bosquejos, paleta, modelo de datos
│   └── capturas/                   # capturas de Power BI y Streamlit (evidencia)
└── GUIA_AVANCE_POWERBI.md          # paso a paso del avance en Power BI
```

## Los tres modelos

Holt-Winters, Ingenuo estacional y Suavizado exponencial simple (`dim_modelo[principal] = True`). Son los únicos evaluados en ambas pruebas para las siete series. Las variantes SARIMA se incluyen en las tablas, pero su orden cambia entre pruebas.

## Regenerar los datos

```bash
python scripts/preparar_datos_powerbi.py Notebooks/resultados Lab12_PowerBI/datos_powerbi
```

El script verifica que no haya duplicados en ninguna tabla, que el valor real de las predicciones coincida con el observado y que MAE y RMSE recalculados coincidan con `resultados.json` (98 combinaciones).

## Abrir el informe

Power BI Desktop (Windows). Versión utilizada: 2.159.1231.0 (octubre 2026, Microsoft Store). Si los CSV están en otra carpeta: **Transformar datos → Editar parámetros → RutaDatos** (carpeta `datos_powerbi\` con barra final), y después **Inicio → Actualizar**.

## Versión del Laboratorio 10

```bash
cd Notebooks/resultados
streamlit run app.py
```
