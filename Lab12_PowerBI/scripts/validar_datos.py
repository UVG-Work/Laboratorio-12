"""Validación reproducible de los CSV entregados, sin recalcular modelos."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1] / "datos_powerbi"
o = pd.read_csv(BASE / "fact_observado.csv")
p = pd.read_csv(BASE / "fact_predicciones.csv")
m = pd.read_csv(BASE / "fact_metricas.csv")
series = pd.read_csv(BASE / "dim_serie.csv")
models = pd.read_csv(BASE / "dim_modelo.csv")
tests = pd.read_csv(BASE / "dim_prueba.csv")
dates = pd.read_csv(BASE / "dim_fecha.csv")

assert not o.duplicated(["serie_id", "fecha"]).any()
assert not p.duplicated(["serie_id", "prueba", "modelo_id", "fecha"]).any()
assert not m.duplicated(["serie_id", "prueba", "modelo_id"]).any()
assert set(o.serie_id) <= set(series.serie_id)
assert set(p.serie_id) <= set(series.serie_id)
assert set(p.modelo_id) <= set(models.modelo_id)
assert set(p.prueba) <= set(tests.prueba)
assert set(o.fecha) <= set(dates.fecha)

j = p.merge(o, on=["serie_id", "fecha"], how="left", validate="many_to_one")
assert j.viajeros.notna().all()
assert (j.real - j.viajeros).abs().max() < 1e-8
assert (p.error - (p.pronostico - p.real)).abs().max() < 0.02
assert (p.error_abs - p.error.abs()).abs().max() < 0.02

o["anio"] = pd.to_datetime(o.fecha).dt.year
total = o[o.serie_id.eq("total")]
assert total[total.anio.eq(2025)].viajeros.sum() == 3596061
assert total[total.fecha.eq("2020-05-01")].viajeros.iloc[0] == 9779

principal = models[models.principal.eq(True)]
assert len(principal) == 3
assert set(principal.modelo_id) == {1, 17, 18}

print(f"OK: {len(o)} observaciones, {len(p)} predicciones, {len(m)} métricas; claves y valores reales coherentes.")
print("Total 2025: 3,596,061; mayo 2020: 9,779; tres modelos principales: 1, 17, 18.")
