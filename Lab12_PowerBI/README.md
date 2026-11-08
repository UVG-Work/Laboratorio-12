# Laboratorio 12 · Observatorio de turismo

Segunda versión del observatorio del Laboratorio 10, basada en los mismos registros mensuales y en predicciones **ya calculadas**. No se han entrenado modelos nuevos.

## Estado de la entrega (8 de noviembre de 2026)

El proyecto editable `powerbi/Lab12_Observatorio_v2_final.pbip` contiene cuatro páginas y once gráficos (V1-V10 más V8b), junto con los siete CSV, relaciones y medidas. Los gráficos V1-V3 y el archivo `Lab12_Observatorio_v1_avance.pbix` proceden del avance. **El .pbix incluido sigue siendo el avance**: en este entorno no está instalado Power BI Desktop y no se ha podido abrir, refrescar, verificar visualmente ni exportar la versión final a .pbix. Para obtenerlo, abra el .pbip nuevo en Power BI Desktop, actualice los datos y guárdelo como `Lab12_Observatorio_v2_final.pbix`.

Las cifras y claves de los CSV sí se validaron con `python scripts/validar_datos.py`. No se inventaron tiempos de uso, clics o capturas de pruebas que no se ejecutaron.

## Carpetas

| Carpeta | Contenido |
|---|---|
| `datos_powerbi/` | Siete CSV de dimensiones, observaciones, predicciones y métricas. |
| `powerbi/` | Proyecto PBIP editable, tema y .pbix del avance. |
| `docs/` | Documento de diseño y comparación; capturas existentes del avance. |
| `scripts/` | Generación del proyecto y validación de datos. |

## Abrir y actualizar

1. En Windows, use Power BI Desktop. El avance declaró la versión **2.159.1231.0 (octubre de 2026)**; la versión de este proyecto final no pudo comprobarse localmente.
2. Abra `powerbi/Lab12_Observatorio_v2_final.pbip` (el proyecto de texto, no el .pbix del avance).
3. En **Transformar datos → Editar parámetros**, cambie `RutaDatos` a la ruta absoluta de `datos_powerbi` en su equipo, **con barra final**. El valor guardado corresponde a la ruta solicitada en este equipo.
4. Pulse **Inicio → Actualizar**. Verifique que no haya errores de carga ni campos inválidos.
5. Guarde como `powerbi/Lab12_Observatorio_v2_final.pbix`. Compruebe la interacción y las vistas en Desktop antes de entregar.

### Modelo de datos

`fact_observado` tiene una fila por serie y mes; `fact_predicciones`, por serie, prueba, modelo y mes; `fact_metricas`, por serie, prueba y modelo. `dim_serie`, `dim_fecha`, `dim_prueba` y `dim_modelo` filtran los hechos por relaciones 1 a muchos, en una dirección. No hay uniones entre hechos. La serie Total se solapa con países y vías: la medida `[Viajeros]` muestra una sola serie o Total, para impedir la suma de categorías superpuestas. Los tres modelos principales son Holt-Winters (1), Ingenuo estacional (17) y Suavizado exponencial simple (18). La serie No residentes no tiene predicciones.

La validación comprueba unicidad de claves, referencias a dimensiones, igualdad entre `real` y el observado, y cifras de control. Resultados esperados: **1,680 observaciones, 4,284 predicciones y 98 métricas**; Total 2025 **3,596,061**; mayo de 2020 **9,779**.

## Páginas y uso

1. **Panorama**: V1 línea temporal con jerarquía Año → Trimestre → Mes; V2 mercados y vías; V3 total anual. Seleccione una barra en V2 o una columna en V3 para filtrar los demás gráficos. Haga clic otra vez en la marca para quitar la selección.
2. **Detalle mensual**: elija año y serie en los segmentadores para ver V4; use la pestaña Panorama para regresar. Abra el icono de borrador del segmentador para limpiar su filtro.
3. **Calendario y mercados**: V5 secuencia mensual, V6 perfil estacional y V7 recuperación de 2025 respecto de 2019. V7 usa años fijos e ignora el segmentador de año por diseño.
4. **Pronósticos**: V8 y V8b muestran MAPE y MAE de los tres modelos; V9 traza observaciones y pronósticos; V10 el error del Ingenuo estacional. Filtre por serie y prueba. Sin selección, las medidas usan Total y post-pandemia como referencia. MAPE compara **solo una serie y un conjunto de evaluación a la vez**.

Las pestañas inferiores permiten elegir vista. Para restablecer, borre los segmentadores y selecciones de gráficos; el comando nativo **Restablecer valores predeterminados** puede usarse si está disponible en la versión de Desktop. Se debe validar la visibilidad de controles y la ausencia de datos en Desktop.

## Tres pruebas propuestas

| Prueba | Secuencia en Power BI | Resultado de referencia de los CSV |
|---|---|---|
| A. Mercado recuperado | Calendario y mercados → V7 → compare Estados Unidos y El Salvador. | EE. UU. 146.13 %; El Salvador 126.77 % del nivel de 2019. |
| B. Mes mínimo | Panorama → seleccione 2020 → Detalle mensual → año 2020, Total → regrese a Panorama. | Mayo 2020: 9,779 viajeros. |
| C. Tres modelos | Pronósticos → Total → post-pandemia → lea V8 y V9. | Ingenuo estacional: MAPE 6.25 %; Holt-Winters 23.41 %; Suavizado 29.46 %. |

La tabla de pruebas observadas del documento está pendiente de cronometraje por personas reales en ambas versiones. Para el Laboratorio 10, el código está en el repositorio hermano `CC3084_Laboratorio_1/Notebooks/resultados/app.py` y se abre desde esa carpeta con `streamlit run app.py`. La ruta no forma parte de este repositorio; copie o clone el repositorio original para ejecutarla.

## Reproducir la definición editable

`python scripts/completar_proyecto.py` vuelve a escribir las páginas del proyecto PBIP y sus medidas, sin tocar los CSV. Después ejecute `python scripts/validar_datos.py`. El primero usa como ruta inicial de los CSV el directorio de este repositorio en el equipo solicitado; cambie `RutaDatos` en Desktop al moverlo.

## Limitaciones de los datos

Desde 2023, la fuente deja de registrar residentes guatemaltecos que regresan. Por eso el Total 2025 es 76.71 % del Total 2019, mientras No residentes llega a 124.14 %. La cobertura de cruceristas también cambió: la serie marítima requiere cautela. Las predicciones son evaluaciones retrospectivas, no estimaciones actualizadas de meses posteriores a junio de 2026. No se infieren causas a partir de estas series.
