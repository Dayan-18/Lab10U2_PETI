"""AR02 · Estructura de la información y cooperación proceso-aplicación — Municipalidad Distrital de Alto Selva (Taller 10, SI-886).

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
MARCA = {"Bueno": "✓ Bueno", "Parcial": "~ Parcial", "Deficiente": "✗ Deficiente", "Sin soporte": "✗ Sin soporte"}
MALOS = ["Deficiente", "Sin soporte"]

print("=" * 78)
print("AR02 · ESTRUCTURA DE LA INFORMACIÓN Y COOPERACIÓN PROCESO-APLICACIÓN · ALTO SELVA")
print("=" * 78)

print("\n1. Vista de cooperación proceso-aplicación (actual)\n")
print(f" {'PROCESO':<42}│ {'SISTEMA QUE LO SOPORTA':<58}│ NIVEL")
print(" " + "─" * 42 + "┼" + "─" * 59 + "┼" + "─" * 14)
for r in pro.itertuples():
    print(f" {r.Proceso:<42}│ {r._3:<58}│ {MARCA[r.Nivel]}")
n_def = pro.Nivel.isin(MALOS).sum()
n_par = (pro.Nivel == "Parcial").sum()
print(f"\n  Procesos sin soporte o con soporte deficiente: {n_def} de {len(pro)}"
      f"  ({', '.join(pro[pro.Nivel.isin(MALOS)].Proceso)})")
print(f"  Procesos con soporte parcial: {n_par} de {len(pro)}  ({', '.join(pro[pro.Nivel == 'Parcial'].Proceso)})")
hojas = sorted({a.strip() for s in pro.Aplicaciones for a in s.split(";")} & {f"APP-{n:02d}" for n in range(6, 9)})
print(f"  Hojas de cálculo que soportan procesos: {len(hojas)} ({', '.join(hojas)})")

print("\n2. Estructura de la información\n")
print(f" {'Entidad':<27}{'Registros por sistema':<44}{'Fuente autoritativa':<32}{'Dueño':<26}{'Personales'}")
for r in ent.itertuples(index=False):
    print(f" {r[0]:<27}{r[2][:42]:<44}{r[3][:30]:<32}{r[4]:<26}{r[7]}")

sin_fuente = ent[ent["¿Fuente autoritativa?"].str.startswith("Ninguna")].Entidad.tolist()
sin_duenio = ent[ent["Dueño del dato (cargo)"] == "Ninguno"].Entidad.tolist()
ambos = [e for e in sin_fuente if e in sin_duenio]
personales = ent[ent["¿Contiene datos personales?"].str.startswith("Sí")].Entidad.tolist()
print(f"\n  Entidades sin fuente autoritativa digital: {len(sin_fuente)} de {len(ent)}  ({', '.join(sin_fuente)})")
print(f"  Entidades sin dueño de dato:               {len(sin_duenio)} de {len(ent)}  ({', '.join(sin_duenio)})")
print(f"  Sin fuente y sin dueño a la vez:           {len(ambos)} de {len(ent)}  ({', '.join(ambos)})")
print(f"  Entidades con datos personales:            {len(personales)} de {len(ent)}  ({', '.join(personales)})")
print("  Clasificación: " + " · ".join(f"{k} {v}" for k, v in ent["Clasificación"].value_counts().items()))

pd.DataFrame([
    ("Procesos sin soporte o con soporte deficiente", n_def, len(pro)),
    ("Procesos con soporte parcial", n_par, len(pro)),
    ("Entidades sin fuente autoritativa", len(sin_fuente), len(ent)),
    ("Entidades sin dueño", len(sin_duenio), len(ent)),
    ("Entidades sin fuente ni dueño", len(ambos), len(ent)),
    ("Entidades con datos personales", len(personales), len(ent)),
], columns=["Indicador", "N", "M"]).to_csv(SALIDAS / "AR02_indicadores.csv", index=False)
print("\n  -> docs/evidencias/S10/salidas/AR02_indicadores.csv")
