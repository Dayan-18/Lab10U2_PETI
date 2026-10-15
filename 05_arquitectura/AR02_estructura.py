"""AR02 · Estructura de la información y cooperación proceso-aplicación — DICOSUR (Taller 10, SI-886).

Lee AR02_entidades.csv y AR02_procesos_aplicacion.csv, imprime la vista de
cooperación proceso-aplicación y cuenta:
  - entidades sin fuente autoritativa, sin dueño y con datos personales;
  - procesos sin soporte o con soporte deficiente.

Uso (desde la raíz del repositorio):
    python 05_arquitectura/AR02_estructura.py
"""
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
SALIDAS = BASE.parent / "docs" / "evidencias" / "S10" / "salidas"
SALIDAS.mkdir(parents=True, exist_ok=True)

ent = pd.read_csv(BASE / "AR02_entidades.csv")
pro = pd.read_csv(BASE / "AR02_procesos_aplicacion.csv")
MARCA = {"Bueno": "✓ Bueno", "Parcial": "~ Parcial", "Deficiente": "✗ Deficiente"}

print("=" * 78)
print("AR02 · ESTRUCTURA DE LA INFORMACIÓN Y COOPERACIÓN PROCESO-APLICACIÓN · DICOSUR")
print("=" * 78)

print("\n1. Vista de cooperación proceso-aplicación (actual)\n")
print(f" {'PROCESO':<31}│ {'SISTEMA QUE LO SOPORTA':<39}│ NIVEL")
print(" " + "─" * 31 + "┼" + "─" * 40 + "┼" + "─" * 13)
for r in pro.itertuples():
    print(f" {r.Proceso:<31}│ {r._3:<39}│ {MARCA[r.Nivel]}")
n_def = (pro.Nivel == "Deficiente").sum()
n_par = (pro.Nivel == "Parcial").sum()
print(f"\n  Procesos sin soporte o con soporte deficiente: {n_def} de {len(pro)}"
      f"  ({', '.join(pro[pro.Nivel == 'Deficiente'].Proceso)})")
print(f"  Procesos con soporte parcial: {n_par} de {len(pro)}  ({', '.join(pro[pro.Nivel == 'Parcial'].Proceso)})")
hojas = sorted({a.strip() for s in pro.Aplicaciones for a in s.split(";")} & {f"APP-{n:02d}" for n in range(6, 12)})
print(f"  Hojas de cálculo que soportan procesos: {len(hojas)} ({', '.join(hojas)})")

print("\n2. Estructura de la información\n")
print(f" {'Entidad':<21}{'Registros por sistema':<24}{'Fuente autoritativa':<21}{'Dueño':<30}{'Personales'}")
for r in ent.itertuples(index=False):
    print(f" {r[0]:<21}{r[2]:<24}{r[3]:<21}{r[4]:<30}{r[7]}")

sin_fuente = ent[ent["¿Fuente autoritativa?"] == "Ninguna"].Entidad.tolist()
sin_duenio = ent[ent["Dueño del dato (cargo)"] == "Ninguno"].Entidad.tolist()
ambos = [e for e in sin_fuente if e in sin_duenio]
personales = ent[ent["¿Contiene datos personales?"].str.startswith("Sí")].Entidad.tolist()
print(f"\n  Entidades sin fuente autoritativa: {len(sin_fuente)} de {len(ent)}  ({', '.join(sin_fuente)})")
print(f"  Entidades sin dueño de dato:       {len(sin_duenio)} de {len(ent)}  ({', '.join(sin_duenio)})")
print(f"  Sin fuente y sin dueño a la vez:   {len(ambos)} de {len(ent)}  ({', '.join(ambos)})")
print(f"  Entidades con datos personales:    {len(personales)} de {len(ent)}  ({', '.join(personales)})")
print("  Clasificación: " + " · ".join(f"{k} {v}" for k, v in ent["Clasificación"].value_counts().items()))

pd.DataFrame([
    ("Procesos con soporte deficiente", n_def, len(pro)),
    ("Procesos con soporte parcial", n_par, len(pro)),
    ("Entidades sin fuente autoritativa", len(sin_fuente), len(ent)),
    ("Entidades sin dueño", len(sin_duenio), len(ent)),
    ("Entidades sin fuente ni dueño", len(ambos), len(ent)),
    ("Entidades con datos personales", len(personales), len(ent)),
], columns=["Indicador", "N", "M"]).to_csv(SALIDAS / "AR02_indicadores.csv", index=False)
print("\n  -> docs/evidencias/S10/salidas/AR02_indicadores.csv")
