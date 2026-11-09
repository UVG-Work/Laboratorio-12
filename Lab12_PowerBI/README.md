# Laboratorio 12 · Observatorio de turismo

Segunda versión del observatorio del Laboratorio 10, basada en los mismos registros mensuales y en predicciones **ya calculadas**. No se han entrenado modelos nuevos.

## Estado de la entrega (8 de noviembre de 2026)

| Versión | Archivo | Contenido |
|---|---|---|
| v1 · avance (5 nov) | `powerbi/Lab12_Observatorio_v1_avance.pbix` (+ `.pbip`) | V1-V3 enlazadas |
| **v2 · final (8 nov)** | **`powerbi/Lab12_Observatorio_v2_final.pbix`** (+ `.pbip` editable en texto) | 4 páginas, 11 gráficos (V1-V10 más V8b), navegación, limpiar filtros y mensajes |

El informe final se abrió, actualizó y revisó en Power BI Desktop **2.159.1231.0 (octubre de 2026, Microsoft Store)** el 8 de noviembre de 2026; las capturas `docs/capturas/10_` a `13_` son de esa sesión. Las cifras y claves de los CSV se validaron con `python scripts/validar_datos.py`. No se inventaron tiempos de uso ni clics de pruebas que no se ejecutaron.

## Carpetas

| Carpeta | Contenido |
|---|---|
| `datos_powerbi/` | Siete CSV de dimensiones, observaciones, predicciones y métricas. |
| `powerbi/` | Informes .pbix (avance y final), sus proyectos .pbip editables y el tema. |
| `docs/` | Documento de diseño y comparación (.md y .pdf), registros de pruebas y tiempo, bosquejos y capturas del avance y de la versión final. |
| `scripts/` | Generación del proyecto y validación de datos. |
| `../Lab10_Streamlit/` | Tablero del Laboratorio 10 (`app.py`), sus datos y `Lab10_Diseno_Final.pdf`. |

## Abrir y actualizar

1. En Windows, instale Power BI Desktop (gratuito; se usó la versión **2.159.1231.0**).
2. Abra `powerbi/Lab12_Observatorio_v2_final.pbix`. El archivo ya contiene los datos importados, así que se puede revisar sin actualizar.
3. Para volver a cargar los CSV: **Transformar datos → Editar parámetros → `RutaDatos`** y escriba la ruta absoluta de la carpeta `datos_powerbi` en su equipo, **con barra final** (por ejemplo `C:\repos\Laboratorio-12\Lab12_PowerBI\datos_powerbi\`). Luego pulse **Inicio → Actualizar**.
4. Alternativa editable: abrir `powerbi/Lab12_Observatorio_v2_final.pbip` (mismo informe en texto, útil para revisar cambios en Git); requiere el mismo paso 3 y **Actualizar**.

### Modelo de datos

`fact_observado` tiene una fila por serie y mes; `fact_predicciones`, por serie, prueba, modelo y mes; `fact_metricas`, por serie, prueba y modelo. `dim_serie`, `dim_fecha`, `dim_prueba` y `dim_modelo` filtran los hechos por relaciones 1 a muchos, en una dirección. No hay uniones entre hechos. La serie Total se solapa con países y vías: la medida `[Viajeros]` muestra una sola serie o Total, para impedir la suma de categorías superpuestas. Los tres modelos principales son Holt-Winters (1), Ingenuo estacional (17) y Suavizado exponencial simple (18). La serie No residentes no tiene predicciones.

La validación comprueba unicidad de claves, referencias a dimensiones, igualdad entre `real` y el observado, y cifras de control. Resultados esperados: **1,680 observaciones, 4,284 predicciones y 98 métricas**; Total 2025 **3,596,061**; mayo de 2020 **9,779**.

## Páginas y uso

Cada página tiene arriba cuatro botones para cambiar de página y el botón **↺ Limpiar filtros** (borra todos los segmentadores). En Power BI Desktop los botones se activan con **Ctrl + clic**; en la vista de lectura, con un clic.

1. **Panorama**: V1 línea temporal con jerarquía Año → Trimestre → Mes (flechas ↓, ⇊ y ↑ del encabezado para bajar y subir de nivel); V2 mercados y vías; V3 total anual. Un clic en una barra de V2 o una columna de V3 filtra los demás gráficos; otro clic quita la selección.
2. **Detalle mensual**: abre con 2025 y Total. Elija año y serie para ver V4. Sin año elegido aparece «Elija un año para ver sus meses».
3. **Calendario y mercados**: V5 secuencia mensual, V6 perfil estacional y V7 recuperación de 2025 respecto de 2019 (línea discontinua = 100). Los segmentadores solo afectan a V5 y V6; V7 compara siempre todas las series.
4. **Pronósticos**: abre con Total y Post-pandemia. V8 y V8b muestran MAPE y MAE de los tres modelos (un color por modelo, igual que en V9); V9 traza observado y pronósticos; V10 el error del Ingenuo estacional. MAPE compara **solo una serie y un conjunto de evaluación a la vez**. Si elige No residentes, un aviso indica que esa serie no tiene modelos.

## Tres pruebas propuestas

| Prueba | Secuencia en Power BI | Resultado de referencia de los CSV |
|---|---|---|
| A. Mercado recuperado | Botón «3 · Calendario y mercados» → V7 → compare Estados Unidos y El Salvador. | EE. UU. 146.13 %; El Salvador 126.77 % del nivel de 2019. |
| B. Mes mínimo | Panorama → clic en 2020 en V3 → ⇊ en V1 hasta meses → mínimo → ↑ y clic de nuevo en 2020 para regresar. (Alternativa: botón «2 · Detalle mensual», año 2020 → botón «1 · Panorama».) | Mayo 2020: 9,779 viajeros. |
| C. Tres modelos | Botón «4 · Pronósticos» (ya abre en Total y Post-pandemia) → lea V8 y V9. | Ingenuo estacional: MAPE 6.25 %; Holt-Winters 23.41 %; Suavizado 29.46 %. |

June Herrera Watanabe ejecutó y cronometró las tres pruebas en ambas versiones el 8 de noviembre de 2026. Los resultados están en `docs/registro_pruebas.csv` y en la sección 8 del documento.

**Versión del Laboratorio 10 (Streamlit).** El código, sus datos y el documento de diseño están en `../Lab10_Streamlit/`, copiados del repositorio original `rodrigoajmac/CC3084_Laboratorio_1` (commit `c547c67`). Para ejecutarla desde la raíz del repositorio:

```
cd Lab10_Streamlit
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Reproducir la definición editable

`python scripts/completar_proyecto.py` vuelve a escribir las páginas 2-4, la navegación y las medidas del proyecto PBIP, sin tocar los CSV, y fija `RutaDatos` a la carpeta `datos_powerbi` de la copia donde se ejecuta. Después ejecute `python scripts/validar_datos.py`, abra el .pbip, pulse **Actualizar** y guárdelo como .pbix. `python scripts/generar_pdf.py` regenera `docs/Lab12_Diseno_Comparacion.pdf` desde `docs/Diseno_y_comparacion.md`.

## Limitaciones de los datos

Desde 2023, la fuente deja de registrar residentes guatemaltecos que regresan. Por eso el Total 2025 es 76.71 % del Total 2019, mientras No residentes llega a 124.14 %. La cobertura de cruceristas también cambió: la serie marítima requiere cautela. Las predicciones son evaluaciones retrospectivas, no estimaciones actualizadas de meses posteriores a junio de 2026. No se infieren causas a partir de estas series.
