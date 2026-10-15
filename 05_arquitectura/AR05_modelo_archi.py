"""AR05 · Modelo ArchiMate 3.2 de DICOSUR en formato de Archi + vistas PNG (Taller 10, SI-886).

Construye el modelo a partir de los archivos de texto versionables:
  AR05_elementos.csv   elementos por capa, con su estado (A actual · O objetivo · AO ambos)
  AR05_relaciones.csv  relaciones ArchiMate entre elementos
  AR03_brechas.csv     (si existe) brechas y paquetes de trabajo de la capa de implementación

y genera:
  05_arquitectura/DICOSUR_arquitectura.archimate   modelo nativo de Archi (se abre con File > Open)
  graficos/V0x_*.png                               las vistas, dibujadas con las mismas coordenadas
                                                   que las vistas del modelo

Uso (desde la raíz del repositorio):
    python 05_arquitectura/AR05_modelo_archi.py
"""
import hashlib
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import pandas as pd

BASE = Path(__file__).resolve().parent
RAIZ = BASE.parent
GRAFICOS = RAIZ / "graficos"
GRAFICOS.mkdir(exist_ok=True)
SALIDA_MODELO = BASE / "DICOSUR_arquitectura.archimate"

el = pd.read_csv(BASE / "AR05_elementos.csv", dtype=str).fillna("")
rel = pd.read_csv(BASE / "AR05_relaciones.csv", dtype=str).fillna("")
brechas = pd.read_csv(BASE / "AR03_brechas.csv", dtype=str).fillna("") if (BASE / "AR03_brechas.csv").exists() else None
paquetes = pd.read_csv(BASE / "AR03_paquetes.csv", dtype=str).fillna("") if (BASE / "AR03_paquetes.csv").exists() else None

# ---------------------------------------------------------------- elementos de implementación (brechas y paquetes)
if brechas is not None:
    extra = []
    for b in brechas.itertuples():
        extra.append((b.id, "Implementación", "Gap", f"{b.id} {b.brecha}", "AO", b.capa))
    if paquetes is not None:
        for p in paquetes.itertuples():
            extra.append((p.paquete, "Implementación", "WorkPackage", f"{p.paquete} {p.nombre}", "AO", f"Ola {p.ola}"))
    el = pd.concat([el, pd.DataFrame(extra, columns=el.columns)], ignore_index=True)
    filas = []
    for b in brechas.itertuples():
        filas.append(("", "Association", b.id, "PLT-01", "", "AO"))
        filas.append(("", "Association", b.id, "PLT-02", "", "AO"))
        if paquetes is not None:
            filas.append(("", "Association", b.paquete, b.id, "", "AO"))
    rel = pd.concat([rel, pd.DataFrame(filas, columns=rel.columns)], ignore_index=True)
    rel["id"] = [f"R-{i:03d}" for i in range(1, len(rel) + 1)]

E = {r.id: r for r in el.itertuples()}
CARPETA = {"Negocio": "business", "Aplicación": "application", "Tecnología": "technology",
           "Motivación": "motivation", "Implementación": "implementation_migration"}
NOMBRE_CARPETA = {"business": "Business", "application": "Application", "technology": "Technology &amp; Physical",
                  "motivation": "Motivation", "implementation_migration": "Implementation &amp; Migration"}


def uid(*partes):
    return "id-" + hashlib.md5("|".join(partes).encode()).hexdigest()


def en(estado_el, plateau):
    return plateau in estado_el


def rel_en(r, plateau):
    if r.estado:
        return plateau in r.estado
    return en(E[r.origen].estado, plateau) and en(E[r.destino].estado, plateau)


# ---------------------------------------------------------------- vistas
W, H = 150, 58  # tamaño de un elemento en la vista


def fila(ids, x0, y0, ancho=W, sep=12):
    return [(i, x0 + k * (ancho + sep), y0, ancho, H) for k, i in enumerate(ids)]


def columna(ids, x0, y0, ancho=W, sep=14):
    return [(i, x0, y0 + k * (H + sep), ancho, H) for k, i in enumerate(ids)]


NIVEL = dict(zip(*[pd.read_csv(BASE / "AR02_procesos_aplicacion.csv")[c] for c in ("id", "Nivel")]))
COLOR_NIVEL = {"Bueno": "#b7e1b0", "Parcial": "#ffe08a", "Deficiente": "#f4a6a6"}
ENT = pd.read_csv(BASE / "AR02_entidades.csv")
SIN_FUENTE_DO = {"DO-01", "DO-02", "DO-03", "DO-05", "DO-07", "DO-08"}  # objetos de datos de entidades sin fuente autoritativa

PROC_A = ["PRO-01", "PRO-02", "PRO-03", "PRO-04", "PRO-05", "PRO-06", "PRO-07", "PRO-08", "PRO-09", "PRO-10"]
PROC_O = ["PRO-01", "PRO-02O", "PRO-03", "PRO-04", "PRO-05", "PRO-06", "PRO-07", "PRO-08O", "PRO-09", "PRO-10"]
APPS_A = [f"APP-{n:02d}" for n in range(1, 13)]
APPS_O = ["APP-02O", "APP-01", "APP-03", "APP-13", "APP-05", "APP-04", "APP-16", "APP-15", "APP-12"]

VISTAS = []

# V01 · Arquitectura actual por capas
VISTAS.append(dict(
    clave="V01", nombre="V01 Arquitectura actual — vista por capas", plateau="A", archivo="V01_arquitectura_actual_capas.png",
    rels={"Serving", "Flow", "Triggering", "Realization", "Association", "Assignment"},
    grupos=[
        ("Capa de negocio", 10, 10, 1975, 250,
         fila(["ACT-02", "ACT-03", "ACT-06", "ACT-05", "ROL-01", "ROL-02", "ROL-03"], 20, 30) +
         fila(["SRV-01", "SRV-02", "SRV-03"], 1180, 30) +
         fila(PROC_A, 20, 160, ancho=185, sep=12)),
        ("Capa de aplicación", 10, 280, 1975, 260,
         fila(["APP-08", "APP-02", "APP-01", "APP-03", "APP-06", "APP-05", "AIF-01", "AIF-02"], 20, 40, ancho=185, sep=12) +
         fila(["APP-07", "APP-11", "APP-09", "APP-12", "APP-04", "APP-10"], 610, 170, ancho=185, sep=12)),
        ("Capa de tecnología", 10, 560, 1975, 230,
         fila(["NOD-01", "NOD-02", "NOD-03", "NOD-04"], 20, 30, ancho=210) +
         fila(["TSV-01", "TSV-02", "TSV-03", "TSV-04", "TSV-05"], 920, 30, ancho=190) +
         fila(["NET-01", "NET-02", "NET-03"], 20, 150, ancho=210)),
    ]))

# V02 · Cooperación proceso-aplicación
VISTAS.append(dict(
    clave="V02", nombre="V02 Cooperación proceso-aplicación (actual)", plateau="A", archivo="V02_cooperacion_proceso_aplicacion.png",
    rels={"Serving"}, color=lambda i: COLOR_NIVEL.get(NIVEL.get(i, ""), None),
    grupos=[
        ("Procesos de la cadena de valor (color = nivel de soporte)", 10, 10, 330, 760, columna(PROC_A, 20, 35, ancho=290, sep=14)),
        ("Aplicaciones que los soportan", 640, 10, 330, 900,
         columna(["APP-01", "APP-02", "APP-08", "APP-03", "APP-06", "APP-05", "APP-09", "APP-12", "APP-07", "APP-11", "APP-04", "APP-10"],
                 20, 35, ancho=290, sep=12)),
    ],
    notas=[(10, 790, 330, 120, "Nivel de soporte\nVerde: bueno (4)\nAmarillo: parcial (2)\nRojo: deficiente o sin sistema (4 de 10)")]))

# V03 · Estructura de la información
VISTAS.append(dict(
    clave="V03", nombre="V03 Estructura de la información (actual)", plateau="A", archivo="V03_estructura_informacion.png",
    rels={"Access", "Realization", "Assignment"}, color=lambda i: "#f4a6a6" if i in SIN_FUENTE_DO else None,
    grupos=[
        ("Objetos de negocio", 10, 10, 1060, 110, fila(["BO-01", "BO-02", "BO-03", "BO-04", "BO-05"], 40, 35, ancho=180, sep=24)),
        ("Objetos de datos (rojo = entidad sin fuente autoritativa)", 10, 150, 1060, 190,
         fila(["DO-01", "DO-02", "DO-03", "DO-04"], 20, 35, ancho=240, sep=16) + fila(["DO-05", "DO-06", "DO-07", "DO-08"], 20, 115, ancho=240, sep=16)),
        ("Aplicaciones que los mantienen", 10, 370, 1060, 110, fila(["APP-01", "APP-02", "APP-07", "APP-08", "APP-03"], 20, 35, ancho=190, sep=16)),
    ],
    notas=[(10, 500, 1060, 60, "5 de 10 entidades sin fuente autoritativa y 5 de 10 sin dueño (AR02_entidades.csv). "
                               "El cliente reside en tres objetos de datos: ERP (8 400), portal (340) y hoja comercial (8 900).")]))

# V04 · Arquitectura objetivo por capas
VISTAS.append(dict(
    clave="V04", nombre="V04 Arquitectura objetivo — vista por capas", plateau="O", archivo="V04_arquitectura_objetivo_capas.png",
    rels={"Serving", "Flow", "Triggering", "Realization", "Association", "Assignment", "Access"},
    color=lambda i: "#7fd3d3" if E[i].estado == "O" and E[i].capa == "Aplicación" else
                    ("#f2e36b" if E[i].estado == "O" and E[i].capa == "Negocio" else
                     ("#93c47d" if E[i].estado == "O" and E[i].capa == "Tecnología" else None)),
    grupos=[
        ("Capa de negocio", 10, 10, 1975, 250,
         fila(["ACT-02", "ACT-03", "ACT-06", "ACT-05", "ROL-01", "ROL-02", "ROL-03", "ROL-04"], 20, 30) +
         fila(["SRV-04", "SRV-01", "SRV-02", "SRV-03"], 1340, 30, ancho=150) +
         fila(PROC_O, 20, 160, ancho=185, sep=12)),
        ("Capa de aplicación", 10, 280, 1975, 290,
         fila(APPS_O, 20, 40, ancho=200, sep=14) +
         fila(["AIF-02", "AIF-03", "ASV-05", "ASV-04"], 20, 150, ancho=200, sep=14) +
         fila(["APP-14"], 880, 150, ancho=420) +
         fila(["DO-01", "DO-05O", "DO-07O", "DO-09", "DO-10"], 1330, 150, ancho=120, sep=8)),
        ("Capa de tecnología", 10, 590, 1975, 230,
         fila(["NOD-01O", "NOD-05", "NOD-02", "NOD-03", "NOD-04"], 20, 30, ancho=210) +
         fila(["TSV-01", "TSV-02", "TSV-03O", "TSV-04", "TSV-05"], 1140, 30, ancho=160) +
         fila(["NET-01", "NET-02", "NET-03"], 20, 150, ancho=210)),
    ],
    notas=[(10, 840, 1975, 50, "Tono intenso = elemento nuevo o modificado respecto de la arquitectura actual. "
                               "Las integraciones pasan por la capa de integración (AP-02); ningún proceso crítico corre sobre hoja de cálculo (AP-06).")]))

# V05 · Brechas y paquetes de trabajo (si ya existe el análisis)
if brechas is not None and paquetes is not None:
    wps = paquetes.paquete.tolist()
    gaps = brechas.assign(o=brechas.paquete.map({w: k for k, w in enumerate(wps)})).sort_values(["o", "id"]).id.tolist()
    VISTAS.append(dict(
        clave="V05", nombre="V05 Brechas y paquetes de trabajo", plateau="AO", archivo="V05_brechas_paquetes.png",
        rels={"Association"}, filtro=lambda r: r.origen.startswith("WP-"),
        grupos=[
            ("Mesetas", 10, 10, 1975, 110, fila(["PLT-01"], 20, 35, ancho=300) + fila(["PLT-02"], 1640, 35, ancho=300)),
            ("Brechas (AR03_brechas.csv)", 10, 140, 1975, 190,
             fila(gaps[:8], 20, 35, ancho=230, sep=14) + fila(gaps[8:], 20, 110, ancho=230, sep=14)),
            ("Paquetes de trabajo (salida de AR03_brechas.py)", 10, 350, 1975, 120, fila(wps, 20, 40, ancho=205, sep=12)),
        ]))

# ---------------------------------------------------------------- escritura del modelo .archimate
def xml_modelo():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<archimate:model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
           'xmlns:archimate="http://www.archimatetool.com/archimate" name="DICOSUR — Arquitectura empresarial (PETI v0.10)" '
           f'id="{uid("modelo")}" version="5.0.0">']
    for capa, tipo in CARPETA.items():
        out.append(f'  <folder name="{NOMBRE_CARPETA[tipo]}" id="{uid("carpeta", tipo)}" type="{tipo}">')
        for r in el[el.capa == capa].itertuples():
            out.append(f'    <element xsi:type="archimate:{r.tipo}" name="{escape(r.nombre)}" id="{uid(r.id)}">')
            out.append(f'      <property key="codigo" value="{r.id}"/>')
            out.append(f'      <property key="estado" value="{ {"A": "actual", "O": "objetivo", "AO": "actual y objetivo"}[r.estado] }"/>')
            if r.nota:
                out.append(f'      <documentation>{escape(r.nota)}</documentation>')
            out.append('    </element>')
        out.append('  </folder>')
    out.append(f'  <folder name="Other" id="{uid("carpeta", "other")}" type="other"/>')
    out.append(f'  <folder name="Relations" id="{uid("carpeta", "relations")}" type="relations">')
    for r in rel.itertuples():
        nombre = f' name="{escape(r.nombre)}"' if r.nombre else ""
        acceso = ' accessType="3"' if r.tipo == "Access" else ""
        out.append(f'    <element xsi:type="archimate:{r.tipo}Relationship"{nombre} id="{uid(r.id, r.origen, r.destino)}" '
                   f'source="{uid(r.origen)}" target="{uid(r.destino)}"{acceso}/>')
    out.append('  </folder>')
    out.append(f'  <folder name="Views" id="{uid("carpeta", "diagrams")}" type="diagrams">')
    for v in VISTAS:
        out.extend(xml_vista(v))
    out.append('  </folder>')
    out.append('</archimate:model>')
    return "\n".join(out) + "\n"


def objetos_vista(v):
    """Devuelve {codigo: (x_abs, y_abs, w, h, grupo)} y la lista de relaciones visibles."""
    pos = {}
    for g, gx, gy, gw, gh, hijos in v["grupos"]:
        for i, x, y, w, h in hijos:
            pos[i] = (gx + x, gy + y, w, h, g)
    visibles = []
    for r in rel.itertuples():
        if r.origen in pos and r.destino in pos and r.tipo in v["rels"] and v.get("filtro", lambda r: True)(r):
            if v["plateau"] == "AO" or rel_en(r, v["plateau"]):
                visibles.append(r)
    return pos, visibles


def xml_vista(v):
    pos, visibles = objetos_vista(v)
    k = v["clave"]
    src, tgt = {}, {}
    for r in visibles:
        src.setdefault(r.origen, []).append(r)
        tgt.setdefault(r.destino, []).append(uid(k, "c", r.id))
    color = v.get("color", lambda i: None)
    out = [f'    <element xsi:type="archimate:ArchimateDiagramModel" name="{escape(v["nombre"])}" id="{uid(k)}">']
    for g, gx, gy, gw, gh, hijos in v["grupos"]:
        out.append(f'      <child xsi:type="archimate:Group" id="{uid(k, "g", g)}" name="{escape(g)}">')
        out.append(f'        <bounds x="{gx}" y="{gy}" width="{gw}" height="{gh}"/>')
        for i, x, y, w, h in hijos:
            c = color(i)
            fill = f' fillColor="{c}"' if c else ""
            tc = f' targetConnections="{" ".join(tgt[i])}"' if i in tgt else ""
            out.append(f'        <child xsi:type="archimate:DiagramObject" id="{uid(k, "o", i)}"{tc}{fill} archimateElement="{uid(i)}">')
            out.append(f'          <bounds x="{x}" y="{y}" width="{w}" height="{h}"/>')
            for r in src.get(i, []):
                out.append(f'          <sourceConnection xsi:type="archimate:Connection" id="{uid(k, "c", r.id)}" '
                           f'source="{uid(k, "o", r.origen)}" target="{uid(k, "o", r.destino)}" archimateRelationship="{uid(r.id, r.origen, r.destino)}"/>')
            out.append('        </child>')
        out.append('      </child>')
    for n, (x, y, w, h, texto) in enumerate(v.get("notas", [])):
        out.append(f'      <child xsi:type="archimate:Note" id="{uid(k, "n", str(n))}">')
        out.append(f'        <bounds x="{x}" y="{y}" width="{w}" height="{h}"/>')
        out.append(f'        <content>{escape(texto)}</content>')
        out.append('      </child>')
    out.append('    </element>')
    return out


# ---------------------------------------------------------------- dibujo de las vistas (notación ArchiMate)
COLOR_CAPA = {"Negocio": "#ffffb5", "Aplicación": "#b5ffff", "Tecnología": "#c9e7b7", "Motivación": "#ccccff"}
COLOR_TIPO = {"Gap": "#e0ffe0", "Plateau": "#e0ffe0", "WorkPackage": "#ffe0e0"}
ETIQUETA = {"BusinessActor": "actor", "BusinessRole": "rol", "BusinessProcess": "proceso", "BusinessService": "servicio",
            "BusinessObject": "objeto de negocio", "ApplicationComponent": "componente", "ApplicationService": "servicio de aplicación",
            "ApplicationInterface": "interfaz", "DataObject": "objeto de datos", "Node": "nodo", "TechnologyService": "servicio tecnológico",
            "CommunicationNetwork": "red", "Gap": "brecha", "WorkPackage": "paquete de trabajo", "Plateau": "meseta", "Principle": "principio"}
ESTILO = {  # (estilo de línea, punta de flecha)
    "Serving": ("-", "->"), "Flow": ("--", "-|>"), "Triggering": ("-", "-|>"), "Realization": (":", "-|>"),
    "Access": (":", "->"), "Assignment": ("-", "-|>"), "Composition": ("-", "-"), "Association": ("-", "-"),
}


def recorta(x0, y0, x1, y1, caja):
    """Punto donde el segmento centro→centro sale de la caja destino."""
    bx, by, bw, bh = caja
    cx, cy = bx + bw / 2, by + bh / 2
    dx, dy = x0 - cx, y0 - cy
    if dx == 0 and dy == 0:
        return cx, cy
    t = min((bw / 2) / abs(dx) if dx else 1e9, (bh / 2) / abs(dy) if dy else 1e9)
    return cx + dx * t, cy + dy * t


def dibuja(v):
    pos, visibles = objetos_vista(v)
    color = v.get("color", lambda i: None)
    ancho = max(gx + gw for _, gx, gy, gw, gh, _ in v["grupos"]) + 20
    alto = max([gy + gh for _, gx, gy, gw, gh, _ in v["grupos"]] + [y + h for x, y, w, h, _ in v.get("notas", [])]) + 20
    esc = 100
    fig = plt.figure(figsize=(ancho / esc, alto / esc))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, ancho)
    ax.set_ylim(alto, 0)
    ax.axis("off")
    for g, gx, gy, gw, gh, _ in v["grupos"]:
        ax.add_patch(Rectangle((gx, gy), gw, gh, facecolor="#f4f4f4", edgecolor="#8a8a8a", lw=0.8, ls="--"))
        ax.text(gx + 8, gy + 14, g, fontsize=8.5, weight="bold", color="#333333", va="center")
    for r in visibles:
        x0, y0, w0, h0, _ = pos[r.origen]
        x1, y1, w1, h1, _ = pos[r.destino]
        c0 = (x0 + w0 / 2, y0 + h0 / 2)
        c1 = (x1 + w1 / 2, y1 + h1 / 2)
        p1 = recorta(*c0, *c1, (x1, y1, w1, h1))
        p0 = recorta(*c1, *c0, (x0, y0, w0, h0))
        ls, punta = ESTILO.get(r.tipo, ("-", "-"))
        col = "#1f5fa8" if r.tipo == "Flow" else "#555555"
        ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle=punta, ls=ls, lw=0.8, color=col, shrinkA=0, shrinkB=0,
                                                          mutation_scale=9))
        if r.tipo == "Composition":
            ax.plot(*p0, marker="D", ms=4, color="#555555")
        if r.tipo == "Assignment":
            ax.plot(*p0, marker="o", ms=3.5, color="#555555")
    for i, (x, y, w, h, _) in pos.items():
        e = E[i]
        fc = color(i) or COLOR_TIPO.get(e.tipo) or COLOR_CAPA.get(e.capa, "#eeeeee")
        redondo = e.tipo in ("BusinessService", "ApplicationService", "TechnologyService")
        caja = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={h / 2 if redondo else 6}",
                              facecolor=fc, edgecolor="#4d4d4d", lw=0.9)
        ax.add_patch(caja)
        if e.tipo in ("BusinessObject", "DataObject"):
            ax.plot([x, x + w], [y + 12, y + 12], color="#4d4d4d", lw=0.7)
        ax.text(x + w - 4, y + 7, ETIQUETA.get(e.tipo, e.tipo), fontsize=4.6, ha="right", va="center", color="#555555", style="italic")
        nombre = textwrap.fill(e.nombre, max(14, int(w / 6.2)))
        ax.text(x + w / 2, y + h / 2 + 5, nombre, fontsize=6.3, ha="center", va="center", color="#111111", linespacing=1.05)
    for x, y, w, h, texto in v.get("notas", []):
        ax.add_patch(Rectangle((x, y), w, h, facecolor="#ffffff", edgecolor="#8a8a8a", lw=0.7))
        ax.text(x + 8, y + 10, textwrap.fill(texto, int(w / 5.3)) if "\n" not in texto else texto,
                fontsize=6.6, va="top", ha="left", color="#222222", linespacing=1.3)
    fig.savefig(GRAFICOS / v["archivo"], dpi=170, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    SALIDA_MODELO.write_text(xml_modelo(), encoding="utf-8")
    print("=" * 72)
    print("AR05 · MODELO ARCHIMATE DE DICOSUR")
    print("=" * 72)
    for capa in CARPETA:
        sub = el[el.capa == capa]
        print(f"  {capa:<15} {len(sub):>3} elementos  (actual {sub.estado.str.contains('A').sum():>2} · objetivo {sub.estado.str.contains('O').sum():>2})")
    print(f"  {'Relaciones':<15} {len(rel):>3}")
    print(f"  {'Vistas':<15} {len(VISTAS):>3}")
    print(f"\n  -> 05_arquitectura/{SALIDA_MODELO.name}")
    for v in VISTAS:
        dibuja(v)
        print(f"  -> graficos/{v['archivo']}")
