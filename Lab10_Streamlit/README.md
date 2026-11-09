# Laboratorio 10 · Observatorio de turismo (Streamlit)

Esta es la versión del Laboratorio 10 con la que se compara el informe de Power BI del Laboratorio 12. Los archivos se copiaron sin cambios del repositorio del equipo [`rodrigoajmac/CC3084_Laboratorio_1`](https://github.com/rodrigoajmac/CC3084_Laboratorio_1), commit `c547c67`, carpeta `Notebooks/resultados/`.

| Archivo | Contenido |
|---|---|
| `app.py` | Tablero Streamlit + Plotly con cuatro páginas: Panorama, Calendario y mercados, Pronósticos, y Guía y límites. |
| `series_mensuales.csv` | Siete series mensuales (total, tres países y tres vías), de 2009 a junio de 2026. |
| `resultados.json` | Indicadores y métricas de los modelos del Laboratorio 1. |
| `predicciones.csv` | Valores reales y predichos de las pruebas 70/30 y post-pandemia. |
| `.streamlit/config.toml` | Tema de colores. |
| `Lab10_Diseno_Final.pdf` | Documento de diseño final del Laboratorio 10. |

## Ejecutar

Se necesita Python 3.10 o posterior. Desde esta carpeta:

```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit muestra en la terminal la dirección local de la aplicación. No hace falta entrenar modelos.
