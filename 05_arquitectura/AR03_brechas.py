"""AR03 · Análisis de brechas y paquetes de trabajo — DICOSUR (Taller 10, SI-886).

Lee AR03_brechas.csv (brechas por capa, tipo, esfuerzo y dependencias) y
AR03_paquetes_def.csv (paquetes de trabajo y proyecto del portafolio) y:
  1. resume las brechas por capa y tipo;
  2. agrupa las brechas en paquetes de trabajo con su esfuerzo;
  3. deriva las dependencias entre paquetes y la secuencia obligada (olas),
     y la ruta crítica por esfuerzo;
  4. guarda AR03_paquetes.csv y los gráficos de brechas y secuencia.

El cálculo es del programa; las cifras y su justificación son del equipo.

Uso (desde la raíz del repositorio):
    python 05_arquitectura/AR03_brechas.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent
RAIZ = BASE.parent
GRAFICOS = RAIZ / "graficos"
GRAFICOS.mkdir(exist_ok=True)

b = pd.read_csv(BASE / "AR03_brechas.csv", dtype=str).fillna("")
wp = pd.read_csv(BASE / "AR03_paquetes_def.csv", dtype=str)
b["esfuerzo_sem"] = b["esfuerzo_sem"].astype(int)
lista = lambda s: [x.strip() for x in s.split(";") if x.strip()]

print("=" * 76)
print("AR03 · ANÁLISIS DE BRECHAS Y PAQUETES DE TRABAJO · DICOSUR")
print("=" * 76)

# ---------------------------------------------------------------- 1. brechas por capa y tipo
print(f"\n1. Brechas por capa y tipo ({len(b)} brechas · {b.esfuerzo_sem.sum()} semanas-persona)\n")
tabla = pd.crosstab(b.capa, b.tipo, margins=True, margins_name="Total")
tabla = tabla.reindex(["Negocio", "Datos", "Aplicación", "Tecnología", "Total"])
print(tabla.to_string())

# ---------------------------------------------------------------- 2. dependencias válidas
ids = set(b.id)
malas = [(r.id, d) for r in b.itertuples() for d in lista(r.dependencias) if d not in ids]
if malas:
    print("\n  [FALLA] dependencias a brechas inexistentes:", malas)
    sys.exit(1)

# ---------------------------------------------------------------- 3. paquetes de trabajo
de_brecha = dict(zip(b.id, b.paquete))
filas = []
for p in wp.itertuples():
    sub = b[b.paquete == p.paquete]
    deps = sorted({de_brecha[d] for r in sub.itertuples() for d in lista(r.dependencias)} - {p.paquete})
    filas.append(dict(paquete=p.paquete, nombre=p.nombre, proyecto=p.proyecto, brechas="; ".join(sub.id),
                      n_brechas=len(sub), esfuerzo_sem=int(sub.esfuerzo_sem.sum()), depende_de="; ".join(deps)))
P = pd.DataFrame(filas)

# olas: nivel en el grafo de dependencias (orden topológico)
ola = {}
pendientes = set(P.paquete)
nivel = 1
while pendientes:
    listos = [p for p in pendientes if all(d in ola for d in lista(P.set_index("paquete").loc[p, "depende_de"]))]
    if not listos:
        print("\n  [FALLA] dependencia circular entre:", ", ".join(sorted(pendientes)))
        sys.exit(1)
    for p in listos:
        ola[p] = nivel
    pendientes -= set(listos)
    nivel += 1
P["ola"] = P.paquete.map(ola)

# ruta crítica por esfuerzo (camino más largo del grafo)
esf = dict(zip(P.paquete, P.esfuerzo_sem))
dep = {r.paquete: lista(r.depende_de) for r in P.itertuples()}
largo, previo = {}, {}
for p in sorted(P.paquete, key=lambda x: ola[x]):
    mejor = max(dep[p], key=lambda d: largo[d], default=None)
    largo[p] = esf[p] + (largo[mejor] if mejor else 0)
    previo[p] = mejor
fin = max(largo, key=largo.get)
ruta = [fin]
while previo[ruta[-1]]:
    ruta.append(previo[ruta[-1]])
ruta.reverse()
P["inicio_sem"] = [largo[p] - esf[p] for p in P.paquete]
P = P.sort_values(["ola", "paquete"])
P.to_csv(BASE / "AR03_paquetes.csv", index=False)

print("\n2. Paquetes de trabajo derivados de las brechas\n")
for r in P.itertuples():
    print(f"  {r.paquete}  {r.nombre:<40} {r.n_brechas} brechas  {r.esfuerzo_sem:>3} sem-p  -> {r.proyecto}")
    print(f"         brechas: {r.brechas}" + (f" · depende de: {r.depende_de}" if r.depende_de else " · sin dependencias"))

print("\n3. Secuencia obligada por dependencias\n")
for n in sorted(set(ola.values())):
    print(f"  Ola {n}: " + " · ".join(f"{p} {P.set_index('paquete').loc[p, 'nombre']}" for p in sorted(k for k, v in ola.items() if v == n)))
print(f"\n  Ruta crítica por esfuerzo: {' → '.join(ruta)} = {largo[fin]} semanas-persona")
print("  Regla verificada: WP-07 (analítica) queda después de WP-03 (gobierno del dato) y WP-02 (cumplimiento)"
      if ola["WP-07"] > max(ola["WP-03"], ola["WP-02"]) else "  [ALERTA] la analítica no queda después del gobierno del dato")

# ---------------------------------------------------------------- 4. gráficos
fig, ax = plt.subplots(figsize=(8, 3.6))
t = pd.crosstab(b.capa, b.tipo).reindex(["Negocio", "Datos", "Aplicación", "Tecnología"]).fillna(0)
colores = {"Nuevo": "#2e7d5b", "Modificar": "#e0a526", "Retirar": "#b23b3b"}
izq = [0] * len(t)
for tipo in ["Nuevo", "Modificar", "Retirar"]:
    if tipo in t:
        ax.barh(t.index, t[tipo], left=izq, color=colores[tipo], label=tipo)
        for k, (l, v) in enumerate(zip(izq, t[tipo])):
            if v:
                ax.text(l + v / 2, k, int(v), ha="center", va="center", color="white", fontsize=9, weight="bold")
        izq = [a + c for a, c in zip(izq, t[tipo])]
ax.invert_yaxis()
ax.set_xlabel("Número de brechas")
ax.set_title(f"DICOSUR · {len(b)} brechas por capa y tipo", fontsize=11)
ax.legend(frameon=False, loc="lower right")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(GRAFICOS / "AR03_brechas_por_capa.png", dpi=170)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 3.9))
paleta = {1: "#b23b3b", 2: "#e0a526", 3: "#2e6fa8", 4: "#2e7d5b"}
orden = P.sort_values(["inicio_sem", "paquete"], ascending=[False, False])
for k, r in enumerate(orden.itertuples()):
    critico = r.paquete in ruta
    ax.barh(k, r.esfuerzo_sem, left=r.inicio_sem, color=paleta[r.ola], edgecolor="black" if critico else "none", lw=1.4)
    ax.text(r.inicio_sem + r.esfuerzo_sem + 0.4, k, f"{r.paquete} {r.nombre} ({r.esfuerzo_sem})", va="center", fontsize=7.5, color="#222222")
ax.set_yticks([])
ax.set_xlabel("Semanas-persona acumuladas (inicio más temprano según dependencias)")
ax.set_title("Secuencia obligada de los paquetes de trabajo (borde negro = ruta crítica)", fontsize=10)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, label=f"Ola {n}") for n, c in paleta.items()], frameon=False, ncol=4, loc="upper right", fontsize=8)
ax.set_xlim(0, largo[fin] + 22)
ax.set_ylim(-0.6, len(orden) + 0.6)
ax.spines[["top", "right", "left"]].set_visible(False)
fig.tight_layout()
fig.savefig(GRAFICOS / "AR03_secuencia_paquetes.png", dpi=170)
plt.close(fig)
print("\n  -> 05_arquitectura/AR03_paquetes.csv")
print("  -> graficos/AR03_brechas_por_capa.png")
print("  -> graficos/AR03_secuencia_paquetes.png")
