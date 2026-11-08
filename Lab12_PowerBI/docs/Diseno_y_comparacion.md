# Laboratorio 12: diseño y comparación de herramientas

Universidad del Valle de Guatemala · Facultad de Ingeniería · CC3066 Data Science · Semestre II de 2026  
Equipo identificado en el avance: Rodrigo Ajmac, Andrés Mazariegos, June Herrera y Sebastián García.  
Versión documental: 8 de noviembre de 2026.

## 1. Público, preguntas y alcance

El informe se dirige a directivos y tomadores de decisiones del turismo que necesitan leer cifras y tendencias sin interpretar procedimientos estadísticos. Usa las mismas series mensuales y resultados de modelos que la versión de Streamlit y Plotly del Laboratorio 10. La fuente termina en junio de 2026.

| Pregunta de gestión | Decisión que apoya | Vista |
|---|---|---|
| ¿Cómo evolucionó el flujo y cuánto se recuperó tras la pandemia? | Seguimiento sectorial y metas de recuperación | V1, V3, V7 |
| ¿Qué ocurrió en un año o mes concreto? | Revisar episodios y comparar periodos | V4, V5 |
| ¿Qué mercados y vías tienen más volumen y cómo se comparan con 2019? | Priorizar promoción y capacidad | V2, V7 |
| ¿En qué meses se concentra el flujo? | Planificar personal y oferta estacional | V6 |
| ¿Cuál de los tres modelos se equivoca menos en un conjunto dado? | Valorar pronósticos para planeación | V8, V8b, V9, V10 |
| ¿Qué límites tienen la fuente y los modelos? | Evitar extrapolaciones indebidas | Avisos de este documento y README |

El alcance comprende ocho series (siete originales y No residentes derivada), observaciones mensuales de enero de 2009 a junio de 2026, y predicciones y métricas ya producidas para siete series. No permite inferir causas, gasto, ocupación, impacto ambiental ni condiciones posteriores a junio de 2026. Los resultados de evaluación son retrospectivos; no son predicciones nuevas.

## 2. Diseño visual y navegación

Se conserva la semántica de la paleta del Laboratorio 10: azul profundo `#1F4E79` para observado y selección; naranja `#D9661F` para estimación o atención; azul claro `#9DBBD9` y gris `#B9C0C8` para contexto. Violeta `#6A4C93` y verde azulado `#2A8C82` distinguen modelos adicionales. El contraste complementario azul-naranja facilita distinguir observado de estimado; los títulos también lo explican mediante texto. La tipografía prevista es Segoe UI.

Cada página tiene arriba una franja fija con cuatro botones de navegación (navegador de páginas nativo: Panorama, Detalle mensual, Calendario y mercados, Pronósticos; el botón de la página activa aparece relleno en azul oscuro) y un botón **↺ Limpiar filtros** (acción nativa «Borrar todos los segmentadores»). Panorama conserva el filtrado cruzado entre V2/V3 y V1. V1 tiene la jerarquía Año → Trimestre → Mes con drill down/up. Los segmentadores son listas desplegables con título en lenguaje llano; los de Detalle y Pronósticos son de selección única y abren con una selección inicial visible (2025 y Total; Total y Post-pandemia), para que el usuario siempre sepa qué está viendo. Si una selección no tiene datos, una tarjeta en naranja oscuro lo explica («Elija un año para ver sus meses», «Sin pronósticos: No residentes es una serie derivada, sin modelos»). El título de cada gráfico plantea una pregunta o define la métrica. Todo lo anterior se comprobó abriendo el informe en Power BI Desktop 2.159.1231.0 el 8 de noviembre de 2026 (capturas 10 a 13).

**Boceto de flujo:** Panorama → Detalle mensual → Panorama; Panorama → Calendario y mercados; Panorama → Pronósticos. El cambio respecto al avance es la adición de las otras tres páginas, ocho gráficos, la franja de navegación y el botón de limpiar. La franja de navegación reemplaza las pestañas de Streamlit; los controles de cada página reemplazan la barra lateral global. En Power BI Desktop (modo edición) los botones requieren Ctrl + clic; en la vista de lectura funcionan con un clic.

## 3. Justificación de las visualizaciones y equivalencia

| Gráfico | Equivalente del Lab 10 | Tipo en Power BI y motivo |
|---|---|---|
| V1, evolución | Línea con granularidad elegible | Línea con jerarquía: la continuidad temporal y el descenso/subida de nivel responden la misma pregunta. |
| V2, mercados y vías | Barras horizontales seleccionables | Barras: categorías con nombres largos; el clic filtra V1 y V3. |
| V3, años | Columnas anuales | Columnas: comparación discreta entre años; filtra otros gráficos. |
| V4, detalle | Barras mensuales y referencias | Columnas mensuales del año elegido con etiquetas de valor: facilita localizar mínimos y máximos. La referencia superpuesta del Lab 10 se sustituye por las etiquetas; sin un año elegido, el gráfico queda vacío y un mensaje pide elegirlo (evita sumar varios años por mes). |
| V5, calendario | Mapa de calor año × mes | Línea mensual: sustitución por continuidad y menor complejidad visual; ya no ofrece lectura simultánea año × mes del mapa original. |
| V6, estacionalidad | Barras divergentes | Columnas por mes con promedio anual: muestra concentración típica; cambia la codificación divergente original. |
| V7, recuperación | Barras con referencia 100 % | Barras de nivel 2025/2019 con etiquetas y línea constante discontinua en 100 («Nivel de 2019»), igual que la referencia del Lab 10. Los segmentadores de la página no filtran V7 (interacción desactivada) porque compara siempre todas las series. |
| V8, MAPE | Dumbbell en dos pruebas | Barras por modelo con prueba elegible: permite comparar tres modelos en un único conjunto; evita sugerir que pruebas distintas son equivalentes. Cada modelo conserva su color de V9 (Holt-Winters naranja, Ingenuo violeta, Suavizado verde azulado). |
| V8b, MAE | Tabla de métricas | Barras con los mismos colores por modelo: conserva unidad de viajeros y complementa el error porcentual. |
| V9, real y pronósticos | Líneas de observados y tres modelos | Líneas: misma escala temporal y comparación directa. |
| V10, error | Dispersión real vs. estimado | Columnas de error con signo del Ingenuo estacional: positivo = sobreestimación; negativo = subestimación. |

V1-V3 proceden del avance; V4-V10 y V8b se añadieron en el proyecto editable. Tarjetas, segmentadores y tablas no se cuentan entre estas once visualizaciones. En V5 y V6 la sustitución pierde parte de la lectura de la primera versión; esto debe considerarse al comparar herramientas.

## 4. Datos, relaciones y cálculos

Se importan siete archivos CSV UTF-8. Power Query lee cada archivo con delimitador coma, promueve encabezados y asigna tipos; el punto decimal se interpreta con cultura `en-US`. El parámetro `RutaDatos` contiene la carpeta de los CSV y puede editarse antes de actualizar. No se transforman filas dentro de Power Query. `fact_observado` tiene grano serie × mes; `fact_predicciones`, serie × prueba × modelo × mes; `fact_metricas`, serie × prueba × modelo. Las cuatro dimensiones `dim_serie`, `dim_fecha`, `dim_modelo` y `dim_prueba` se relacionan con los hechos en dirección única. No hay relaciones directas entre hechos.

La medida `[Viajeros]` selecciona una sola serie o Total cuando no se ha elegido exactamente una. Esto evita sumar Total con países y vías, que se solapan. `[Nivel 2025 frente a 2019]` divide sumas anuales de la misma serie, omite Guatemala (serie discontinuada desde 2023) e ignora el filtro de año porque el indicador siempre compara 2025/2019. `[Promedio mensual por año]` alimenta V6. `[MAPE evaluación]` y `[MAE evaluación]` leen el valor ya guardado en `fact_metricas` para serie y prueba elegidas; sin selección usan Total y post-pandemia. No promedian métricas de conjuntos diferentes. Las medidas de V9 y V10 leen `fact_predicciones`; V10 fija el modelo Ingenuo estacional para que el error no mezcle modelos. El CSV define `error = pronóstico - real`. `[Viajeros del año elegido]` devuelve `[Viajeros]` solo si hay un único año seleccionado (V4). `[Mensaje detalle]`, `[Mensaje pronósticos]` y `[Mensaje sin datos]` devuelven un texto vacío cuando hay datos y una instrucción cuando no los hay; alimentan las tarjetas de aviso exigidas para selecciones sin información. Todas las medidas se guardan en `dim_serie`: Power BI no admite una medida `Viajeros` en `fact_observado`, que ya tiene la columna `viajeros`.

El programa `scripts/validar_datos.py` comprueba que no haya claves repetidas, que los identificadores existan en las dimensiones y que el valor `real` de cada predicción coincida con `fact_observado` para serie y fecha. Resultado comprobado: 1,680 observaciones, 4,284 predicciones y 98 métricas; diferencia máxima de `real` frente a observado igual a cero. Los tres modelos principales tienen IDs 1, 17 y 18. Los demás resultados se conservan, pero los gráficos V8 y V8b filtran `principal = true`. La serie No residentes no posee predicciones: debe mostrarse vacía en Pronósticos si se elige.

## 5. Planificación, responsabilidades y tiempo efectivo

El avance registra las tareas 1-4 como terminadas por Andrés el 5 de noviembre. Las tareas 5-11 estaban planificadas entre el 6 y el 8 de noviembre: Panorama completo (Rodrigo), Calendario y mercados (June), Pronósticos (Andrés), navegación (Sebastián), pruebas (June y Sebastián), comparación (Rodrigo) y entrega (Sebastián). En esta revisión se preparó una definición PBIP ampliada, la validación y este documento. No puede atribuirse ese trabajo a una persona del equipo sin su confirmación.

| Actividad | Responsable previsto | Fecha prevista | Tiempo efectivo Lab 10 | Tiempo efectivo Lab 12 | Estado verificable |
|---|---|---|---|---|---|
| Preparar y validar datos | Andrés | 5 nov | No registrado | No registrado | CSV y validación disponibles |
| Completar páginas Power BI | Rodrigo, June, Andrés y Sebastián | 6-8 nov | No registrado | No registrado | Abierto y verificado en Desktop 2.159 el 8 nov; navegación, limpiar filtros y mensajes añadidos |
| Pruebas de ambas versiones | June y Sebastián | 7 nov | No registrado | No registrado | Protocolo listo; ejecución pendiente |
| Documento y entrega final | Rodrigo y Sebastián | 8 nov | No registrado | No registrado | PDF generado; `Lab12_Observatorio_v2_final.pbix` guardado desde Desktop el 8 nov |

El tiempo efectivo debe anotarse desde los registros reales del equipo; no se infiere a partir de fechas de modificación. Para evitar sobrescribir el binario .pbix, una persona debe integrarlo y registrar su versión. El PBIP permite revisar diferencias de páginas, visuales y medidas por archivo de texto.

## 6. Matriz de comparación de herramientas

| Criterio | Evidencia Lab 10: Streamlit y Plotly | Evidencia Power BI | Implicación para la tarea |
|---|---|---|---|
| Facilidad de aprendizaje | `app.py` expresa controles y gráficos en Python; requiere saber ejecutar dependencias. | La creación inicial se hizo en Desktop; el PBIP es editable como texto, pero también requiere entender campos, relaciones y DAX. | Depende de experiencia previa; falta medir aprendizaje del equipo. |
| Tiempo de desarrollo | La versión Lab 10 existe y tiene diez visuales; no hay bitácora horaria. | El avance tenía tres gráficos; la definición final propuesta tiene once, sin bitácora horaria. | No se puede afirmar cuál fue más rápido sin horas efectivas. |
| Preparación y actualización | La aplicación lee archivos del repositorio y se reinicia/recarga según su código. | Siete CSV importados, parámetro `RutaDatos` y actualización explícita. | Power BI facilita la actualización local si las rutas son válidas; Streamlit permite automatizarla por código. |
| Integración de modelos | Código Python lee resultados existentes y construye las vistas. | Hechos separados de predicciones y métricas; 4,284 y 98 filas conservadas. | Ambos pueden reutilizar resultados sin entrenar de nuevo; hay que respetar el grano. |
| Interacción y navegación | Selecciones Plotly y pestañas Streamlit están implementadas en `app.py`. | V2/V3 filtran V1 y entre sí; V1 tiene drill down/up; franja de navegación y botón «Limpiar filtros» en cada página (verificado en Desktop). | Ambos sirven para exploración; en Power BI la navegación y el filtrado cruzado son nativos y no requieren código. |
| Personalización | Plotly implementa heatmap y dumbbell con código. | Se sustituyen V5 y V8 por visuales nativos. | Streamlit conserva mejor controles y gráficos especializados. |
| Rendimiento | No existe medición comparable en el mismo equipo. | En un equipo Windows 11, la actualización de los siete CSV terminó en menos de un minuto y el cambio de página fue inmediato (observación sin cronómetro, 8 nov). | No emitir conclusión de velocidad comparada hasta medir ambas versiones en el mismo equipo. |
| Colaboración y versiones | `app.py` y archivos de datos son texto legible en Git. | PBIP divide reporte/modelo en JSON y TMDL; .pbix es binario. | PBIP ayuda a revisar cambios; la integración del .pbix debe coordinarse. |
| Compartir y desplegar | Streamlit Community Cloud ofrece despliegue gratuito sujeto a recursos y acceso al repositorio; otras opciones requieren alojamiento propio. | Desktop es gratuito en Windows; compartir en el servicio depende de licencia/capacidad y permisos. | Consulta local y distribución externa tienen requisitos diferentes. |

## 7. Costos, acceso y fuentes oficiales

Power BI Desktop es una aplicación gratuita para Windows. Crear un informe local no equivale a publicarlo para terceros: compartir y colaborar en áreas de trabajo ordinarias requiere licencias Pro o PPU, o una capacidad que permita acceso de usuarios gratuitos, según el escenario. La publicación web abierta expone el contenido públicamente y no sustituye un mecanismo privado de acceso. El proyecto PBIP es un formato documentado que facilita control de versiones. Streamlit Community Cloud permite desplegar aplicaciones gratuitamente mediante GitHub, con límites de recursos y condiciones de acceso al código; una instalación propia exige pagar o administrar alojamiento. No se presupone que la publicación de datos turísticos concretos esté autorizada.

Fuentes oficiales consultadas el **8 de noviembre de 2026**:

- Microsoft, Power BI Desktop: https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-getting-started
- Microsoft, licencias del servicio: https://learn.microsoft.com/en-us/power-bi/fundamentals/service-features-license-type
- Microsoft, proyectos e informe PBIR: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report
- Microsoft, publicación web: https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-publish-to-web
- Streamlit, Community Cloud: https://docs.streamlit.io/deploy/streamlit-community-cloud
- Streamlit, límites de recursos: https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app

No se registran precios monetarios: cambian con región, contrato y fecha; la decisión debe partir de licencias y capacidad efectivamente disponibles para el equipo.

## 8. Protocolo de tres pruebas y evidencia disponible

Las tres tareas deben ejecutarse por la misma persona, en el mismo equipo y con los mismos filtros; se cronometran desde la vista inicial hasta leer el resultado. Se registran clics, dificultades, experiencia previa y diferencias de entorno. Los siguientes valores se comprobaron en los CSV y son **resultados esperados**, no tiempos o resultados observados de una sesión de interfaz.

| Tarea | Pasos en Power BI | Resultado esperado | Valor que muestra Power BI (8 nov) |
|---|---|---|---|
| A. Recuperación de mercados | Botón «3 · Calendario y mercados» → leer V7 (Estados Unidos y El Salvador). | Estados Unidos 146.13 % (679,139/464,743); El Salvador 126.77 %. | V7: 146.1 y 126.8 (captura 12). |
| B. General → detalle → regreso | Panorama: clic en 2020 en V3 → V1 baja a meses (⇊) → hallar mínimo → subir (↑) y quitar la selección; o botón «2 · Detalle mensual», año 2020 → botón «1 · Panorama». | Mayo de 2020: 9,779 viajeros. | Información sobre herramientas de V1: mayo 9,779 (captura 03). |
| C. Tres modelos | Botón «4 · Pronósticos» (abre en Total y Post-pandemia) → leer V8 y V9. | Ingenuo estacional 6.25 %; Holt-Winters 23.41 %; Suavizado 29.46 %. | V8: 6.25, 23.41 y 29.46 (captura 13). |

Los valores de la última columna confirman que el informe responde correctamente. **Clics, tiempo y dificultades deben medirlos integrantes del equipo** en ambas herramientas, con el mismo equipo y la misma selección, y anotarse en `docs/registro_pruebas.csv`; no se registran aquí cifras que no se midieron.

Las pruebas 70/30 y post-pandemia tienen horizontes distintos: 63 y 18 meses respectivamente. El MAPE de una prueba no debe leerse como comparable directamente con el de la otra. Para registrar una ejecución, complete `docs/registro_pruebas.csv` con fecha, evaluador, herramienta, selección, resultado, clics, segundos y observaciones.

## 9. Consistencia y discrepancias

| Indicador y regla | Laboratorio 10 / datos fuente | CSV para Power BI | Visual de Power BI | Diferencia |
|---|---:|---:|---:|---:|
| Total 2025, serie Total, suma de los 12 meses | 3,596,061 | 3,596,061 | 3,596,061 (V3, información sobre herramientas) | 0 |
| Nivel Total 2025/2019, cociente de sumas anuales | 76.71 % | 76.71 % | 76.7 (V7) | 0 pp (redondeo a un decimal) |
| MAPE Ingenuo estacional, Total, post-pandemia | 6.25 % | 6.25 % | 6.25 (V8) | 0 pp |

Los valores de la columna «Visual de Power BI» se leyeron en el informe abierto en Desktop. Falta leer los mismos tres indicadores en la aplicación Streamlit con las mismas selecciones para cerrar la comparación entre versiones. El 76.71 % del Total y el 124.14 % de No residentes difieren porque la cobertura de residentes guatemaltecos retornados cambia desde 2023. La serie marítima también cambia de cobertura, por lo que su cociente 2025/2019 no debe interpretarse automáticamente como caída real de demanda.

## 10. Recomendaciones por escenario

| Escenario | Herramienta más conveniente con la evidencia actual | Condición |
|---|---|---|
| Consulta periódica de indicadores por directivos dentro de una organización | Power BI | Si la institución dispone de Desktop para autores y licencias/capacidad apropiadas para lectores. La navegación por botones y la selección inicial visible reducen la curva para usuarios no técnicos. |
| Exploración con controles y visualizaciones muy personalizados | Streamlit + Plotly | El código existente conserva el mapa de calor y los gráficos especializados. Requiere mantenimiento de Python y alojamiento. |
| Consulta externa en navegador sin instalar software | Streamlit + Plotly | Community Cloud puede servir para un prototipo público sujeto a límites; para datos privados, elegir alojamiento y autenticación apropiados. Power BI en servicio es alternativa si se resuelven licencias y acceso. |

Para este observatorio, conviene mantener Streamlit como versión flexible y usar Power BI para la consulta periódica de directivos, publicándolo solo cuando se resuelva el acceso permitido (licencias y datos). Una comparación final de rapidez y usabilidad exige las tres pruebas medidas en ambos entornos.

## 11. Evidencias visuales

- Capturas 01 a 03 (`docs/capturas/`): **avance** de Power BI y filtros cruzados (clic en Estados Unidos en V2, clic en 2020 en V3 con V1 a nivel de mes).
- Capturas 10 a 13: **versión final** abierta en Power BI Desktop 2.159.1231.0 el 8 de noviembre de 2026, una por página, en su vista inicial.
- Las figuras de `docs/img/` son bosquejos, no pruebas de funcionamiento.
- Falta una captura de la aplicación Streamlit del Laboratorio 10 en ejecución.
