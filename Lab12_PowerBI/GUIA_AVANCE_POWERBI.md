# Guía del avance en Power BI Desktop (≈ 45 min)

Objetivo del avance en Power BI: **datos y resultados de los tres modelos importados** + **al menos dos visualizaciones funcionales enlazadas**. Esta guía construye V1, V2 y V3 de la página *Panorama* con sus enlaces.

> Idea clave: en Power BI los gráficos se enlazan solos cuando comparten **tablas de dimensión**. Si V2 tiene `dim_serie` en el eje y V1 usa medidas de `fact_observado`, hacer clic en una barra de V2 filtra a V1 a través de la relación `dim_serie → fact_observado`. Por eso los datos vienen en modelo en estrella.

---

## 0. Preparación (2 min)

1. Descomprime `Lab12_PowerBI.zip` dentro del repositorio del equipo (al lado de `Notebooks/`).
2. Los CSV ya vienen listos en `datos_powerbi/`. Si cambian los resultados del Lab 10, se regeneran con:
   `python scripts/preparar_datos_powerbi.py Notebooks/resultados datos_powerbi`
3. Abre Power BI Desktop → **Informe en blanco**. Guárdalo de una vez como `powerbi/Lab12_Observatorio_v1_avance.pbix`.

## 1. Tema con la paleta (1 min)

**Vista → Temas (flecha ▾) → Examinar temas →** `powerbi/tema_observatorio.json`.
Así todos los visuales nacen con la paleta del Lab 10 (azul = observado, naranja = estimación).

## 2. Importar los 7 CSV (8 min)

1. **Archivo → Opciones y configuración → Opciones → Archivo actual → Configuración regional → Inglés (Estados Unidos)**. Esto garantiza que `123.45` se lea como decimal.
2. En la misma ventana, **Archivo actual → Carga de datos →** desmarca **Fecha y hora automáticas**. Usaremos `dim_fecha`, no la tabla oculta que Power BI crea sola.
3. **Inicio → Obtener datos → Texto/CSV**, uno por uno: `dim_serie`, `dim_fecha`, `dim_modelo`, `dim_prueba`, `fact_observado`, `fact_predicciones`, `fact_metricas`.
   - En la vista previa: *Origen del archivo* = **65001: Unicode (UTF-8)** y *Delimitador* = **Coma** → **Cargar**.
4. Revisa los tipos en **Vista de tabla** (icono de cuadrícula, a la izquierda):

| Columna | Tipo |
|---|---|
| `fecha` (en dim_fecha, fact_observado, fact_predicciones) | Fecha |
| `viajeros`, `real`, `pronostico`, `error*`, `MAE`, `RMSE`, `MAPE` | Número decimal |
| `anio`, `mes_num`, `orden`, `modelo_id`, `meses_evaluados` | Número entero |
| `principal`, `tiene_modelos` | Verdadero/Falso |

Para cambiar un tipo: clic en la columna → **Herramientas de columnas → Tipo de datos**.

## 3. Relaciones (5 min)

Ve a **Vista de modelo** (icono de diagrama). Power BI suele detectar las relaciones solo porque las columnas se llaman igual. Verifica que existan **exactamente estas 9**, todas **Uno a varios (1:\*)** y con **dirección de filtro Única**:

| Desde (lado 1) | Hacia (lado \*) | Columna |
|---|---|---|
| dim_serie | fact_observado, fact_predicciones, fact_metricas | `serie_id` |
| dim_fecha | fact_observado, fact_predicciones | `fecha` |
| dim_modelo | fact_predicciones, fact_metricas | `modelo_id` |
| dim_prueba | fact_predicciones, fact_metricas | `prueba` |

Si falta una, arrastra la columna de la dimensión sobre la misma columna del hecho. Si aparece una relación **entre dos tablas fact**, elimínala (clic derecho → Eliminar).

> ¿Por qué así? Las tablas fact nunca se unen entre sí, así que no se multiplican filas. El filtro siempre viaja de la dimensión al hecho, nunca al revés: por eso no hay ambigüedad ni duplicados.

## 4. Orden y jerarquía (4 min)

En **Vista de tabla**:
1. `dim_fecha[mes]` → **Ordenar por columna → mes_num** (para que no salgan en orden alfabético: abr, ago, dic…).
2. `dim_serie[serie]` → **Ordenar por columna → orden**.
3. Panel **Datos**: clic derecho en `dim_fecha[anio]` → **Crear jerarquía**. Arrastra `trimestre` y luego `mes` dentro de la jerarquía nueva. Renómbrala `Año › Trimestre › Mes`.

## 5. Medidas DAX (3 min)

Selecciona la tabla `dim_serie` → **Inicio → Nueva medida**, y pega:

> No la crees en `fact_observado`: esa tabla ya tiene la columna `viajeros` y Power BI rechaza una medida con el mismo nombre (no distingue mayúsculas).

```DAX
Viajeros =
VAR serie_sel =
    IF ( HASONEVALUE ( dim_serie[serie_id] ), SELECTEDVALUE ( dim_serie[serie_id] ), "total" )
RETURN
    CALCULATE ( SUM ( fact_observado[viajeros] ), dim_serie[serie_id] = serie_sel )
```

Formato: **Herramientas de medición → Número entero, separador de miles**.

**Qué hace:** el total ya incluye a los países y las vías, así que sumar todas las series inflaría las cifras unas 3 veces. Esta medida devuelve **solo una serie**: la que esté filtrada, o el Total si no hay una sola elegida.

Segunda medida, para el mensaje cuando no hay datos:

```DAX
Mensaje sin datos =
IF ( ISBLANK ( [Viajeros] ),
     "No hay registros para esta selección. Revise la serie o el rango de años.",
     BLANK () )
```

## 6. Las tres visualizaciones (12 min)

**Segmentador de años.** Visual *Segmentación de datos* → Campo: `dim_fecha[anio]` → en Formato → Configuración de segmentación → Estilo: **Entre**.

**V1 · Línea.** Visual *Gráfico de líneas*.
- Eje X: la jerarquía `Año › Trimestre › Mes`. Eje Y: `[Viajeros]`.
- Título: *¿Cómo ha evolucionado el flujo de viajeros?*
- Prueba el drill: activa la flecha **↓** del encabezado del visual y haz clic en un año (drill down). Con **↑** subes (drill up). El icono **⇊** baja todo un nivel a la vez.

**V2 · Barras horizontales.** Visual *Gráfico de barras agrupadas*.
- Eje Y: `dim_serie[serie]`. Eje X: `[Viajeros]`.
- Panel **Filtros → Filtros en este objeto visual →** `dim_serie[tipo]` → marca solo **País** y **Vía**. Así V2 compara los 6 mercados y vías sin la barra del Total.
- Título: *¿Qué mercados y vías aportan más viajeros?*

**V3 · Columnas por año.** Visual *Gráfico de columnas agrupadas*.
- Eje X: `dim_fecha[anio]`. Eje Y: `[Viajeros]`.
- Título: *¿Cuántos viajeros ingresaron cada año?*

## 7. Enlazar los gráficos (5 min) — el requisito del avance

1. Selecciona **V2** → cinta **Formato → Editar interacciones**. Encima de V1 y V3 aparecen iconos: elige el **embudo (Filtro)** en ambos.
2. Selecciona **V3** → sobre **V1** y **V2** elige el **embudo (Filtro)**.
3. Desactiva **Editar interacciones**.

Prueba:
- Clic en la barra **Estados Unidos** de V2 → V1 y V3 cambian a esa serie. Vuelve a hacer clic para regresar al Total.
- Clic en la columna **2020** de V3 → V2 muestra los mercados de 2020. Si V1 está en nivel mes, muestra los 12 meses de 2020: el mínimo es mayo, con **9,779** viajeros.
- **Verificación rápida:** sin selección, la columna 2025 de V3 debe decir **3,596,061**. Si sale ≈ 3 veces más, la medida `[Viajeros]` no se está usando.

> Ojo: el enunciado aclara que un segmentador que filtra dos gráficos **no** cuenta como enlace. Estos enlaces sí cuentan porque la selección se hace **dentro** de un gráfico y modifica a otro.

## 8. Capturas para el PDF (3 min)

Con **Win + Shift + S** toma y guarda en `docs/capturas/`:
- `01_vista_inicial.png`
- `02_clic_Estados_Unidos_en_V2.png`
- `03_clic_2020_en_V3.png`

Después ejecuta `python scripts/generar_avance_pdf.py`, que inserta las capturas en la sección 6 del PDF. También puedes enviárselas a Claude para que regenere el PDF.

Guarda el .pbix y súbelo al repositorio junto con `datos_powerbi/`.

> **Atajo:** `python scripts/generar_pbip.py` genera `powerbi/Lab12_Observatorio_v1_avance.pbip` con los pasos 1–7 ya hechos. Ábrelo en Power BI Desktop, pulsa **Actualizar** y guárdalo como .pbix (Archivo → Guardar como → tipo *.pbix).
