"""AR04 · Paso F — Validar y corregir — DICOSUR (Taller 10, SI-886).

Ejecuta sobre el archivo de Archi (DICOSUR_arquitectura.archimate) las tres
comprobaciones del taller y termina con código 1 si alguna falla:
  1. Los elementos están en la capa que les corresponde (carpeta de Archi y tipo
     ArchiMate), las relaciones son válidas en ArchiMate 3.2 y ningún nombre lleva
     detalle técnico sensible (IP, versiones exactas, credenciales).
  2. Toda aplicación del modelo actual existe de verdad en la organización
     (inventario docs/caso/arquitectura-actual.md) y toda hoja de cálculo del
     inventario está modelada como componente de aplicación.
  3. Cada brecha del análisis se puede señalar en los dos modelos: su elemento
     actual está en la arquitectura actual y su elemento objetivo en la objetivo.

Uso (desde la raíz del repositorio):
    python 05_arquitectura/AR04_valida.py
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
RAIZ = BASE.parent
XSI = "{http://www.w3.org/2001/XMLSchema-instance}type"

arbol = ET.parse(BASE / "DICOSUR_arquitectura.archimate").getroot()
inventario = (RAIZ / "docs" / "caso" / "arquitectura-actual.md").read_text(encoding="utf-8")
brechas = pd.read_csv(BASE / "AR03_brechas.csv", dtype=str).fillna("")

CAPA_DE_TIPO = {
    "business": {"BusinessActor", "BusinessRole", "BusinessProcess", "BusinessFunction", "BusinessService", "BusinessObject",
                 "BusinessInterface", "BusinessEvent"},
    "application": {"ApplicationComponent", "ApplicationService", "ApplicationInterface", "ApplicationFunction", "DataObject"},
    "technology": {"Node", "Device", "SystemSoftware", "TechnologyService", "CommunicationNetwork", "Artifact"},
    "motivation": {"Principle", "Goal", "Requirement", "Driver"},
    "implementation_migration": {"WorkPackage", "Plateau", "Gap", "Deliverable"},
}
ACTIVO_NEG = {"BusinessActor", "BusinessRole"}
COMP_APP = {"ApplicationComponent", "ApplicationService", "ApplicationInterface"}
COMP_TEC = {"Node", "TechnologyService", "SystemSoftware", "Device"}
# Subconjunto de la tabla de relaciones de ArchiMate 3.2 (Apéndice B) que usa este modelo
PERMITIDAS = {
    "Assignment": {("BusinessActor", "BusinessRole")} | {(a, b) for a in ACTIVO_NEG for b in ("BusinessProcess", "BusinessFunction")},
    "Serving": {("BusinessService", b) for b in ACTIVO_NEG | {"BusinessProcess"}}
               | {(a, b) for a in COMP_APP for b in ACTIVO_NEG | {"BusinessProcess", "ApplicationComponent"}}
               | {(a, b) for a in COMP_TEC for b in {"ApplicationComponent", "Node"}},
    "Realization": {("BusinessProcess", "BusinessService"), ("ApplicationComponent", "ApplicationService"),
                    ("DataObject", "BusinessObject"), ("Node", "TechnologyService"), ("WorkPackage", "Plateau")},
    "Triggering": {("BusinessProcess", "BusinessProcess")},
    "Flow": {("ApplicationComponent", "ApplicationComponent"), ("BusinessProcess", "BusinessProcess")},
    "Access": {("BusinessProcess", "BusinessObject"), ("ApplicationComponent", "DataObject"), ("ApplicationService", "DataObject")},
    "Composition": {("ApplicationComponent", "ApplicationInterface"), ("Node", "Node")},
}
SENSIBLE = [(r"\b\d{1,3}(\.\d{1,3}){3}\b", "dirección IP"),
            (r"\b(Windows|Linux|Ubuntu|SQL Server|Oracle|PostgreSQL|MySQL)\b[^,;]*\d", "producto con versión"),
            (r"\bv?\d+\.\d+(\.\d+)+\b", "número de versión"),
            (r"(?i)contraseña|password|usuario:|clave:", "credencial")]

fallas = []


def registra(ok, mensaje):
    print(f"  [{'OK' if ok else 'FALLA'}] {mensaje}")
    if not ok:
        fallas.append(mensaje)


def prop(e, clave):
    for p in e.findall("property"):
        if p.get("key") == clave:
            return p.get("value")
    return ""


elementos, relaciones, carpeta_de = {}, [], {}
for carpeta in arbol.findall("folder"):
    for e in carpeta.iter("element"):
        t = e.get(XSI).split(":")[1]
        if t.endswith("Relationship"):
            relaciones.append((t.replace("Relationship", ""), e.get("source"), e.get("target"), e.get("id")))
        elif t != "ArchimateDiagramModel":
            elementos[e.get("id")] = dict(tipo=t, nombre=e.get("name"), codigo=prop(e, "codigo"), estado=prop(e, "estado"),
                                          doc=(e.findtext("documentation") or ""))
            carpeta_de[e.get("id")] = carpeta.get("type")
por_codigo = {v["codigo"]: v for v in elementos.values()}
actual = lambda v: "actual" in v["estado"]
objetivo = lambda v: "objetivo" in v["estado"]

print("=" * 76)
print("AR04 · VALIDACIÓN DEL TALLER 10 · DICOSUR")
print("=" * 76)
print(f"  Modelo: {len(elementos)} elementos · {len(relaciones)} relaciones · "
      f"{sum(1 for e in arbol.iter('element') if e.get(XSI) == 'archimate:ArchimateDiagramModel')} vistas")

# ---------------------------------------------------------------- 1
print("\nComprobación 1 · Cada elemento está en la capa que le corresponde")
mal_capa = [f"{v['codigo']} ({v['tipo']} en carpeta {carpeta_de[k]})" for k, v in elementos.items()
            if v["tipo"] not in CAPA_DE_TIPO.get(carpeta_de[k], set())]
registra(not mal_capa, f"{len(elementos) - len(mal_capa)}/{len(elementos)} elementos en la carpeta de su capa"
         + (f" · fuera de capa: {', '.join(mal_capa)}" if mal_capa else ""))
invalidas = []
for t, s, d, _ in relaciones:
    a, b = elementos[s], elementos[d]
    if t != "Association" and (a["tipo"], b["tipo"]) not in PERMITIDAS.get(t, set()):
        invalidas.append(f"{t} {a['codigo']}({a['tipo']}) → {b['codigo']}({b['tipo']})")
registra(not invalidas, f"{len(relaciones) - len(invalidas)}/{len(relaciones)} relaciones válidas en ArchiMate 3.2"
         + (f" · inválidas: {'; '.join(invalidas)}" if invalidas else ""))
expuestos = [f"{v['codigo']} ({motivo})" for v in elementos.values() for patron, motivo in SENSIBLE
             if re.search(patron, v["nombre"] + " " + v["doc"])]
registra(not expuestos, f"{len(expuestos)} elementos con detalle técnico sensible" + (f": {', '.join(expuestos)}" if expuestos else ""))

# ---------------------------------------------------------------- 2
print("\nComprobación 2 · Toda aplicación del modelo actual existe en la organización")
inv_apps = dict(re.findall(r"^\| (APP-\d\d) \| ([^|]+?) \|", inventario, flags=re.M))
inv_hojas = {c for c, fila in re.findall(r"^\| (APP-\d\d) \|(.+)$", inventario, flags=re.M) if "Hoja de cálculo" in fila}
apps_actual = {v["codigo"]: v for v in elementos.values() if v["tipo"] == "ApplicationComponent" and actual(v)}
inexistentes = [f"{c} {v['nombre']}" for c, v in apps_actual.items() if c not in inv_apps]
registra(not inexistentes, f"{len(apps_actual) - len(inexistentes)}/{len(apps_actual)} componentes actuales existen en el inventario"
         + (f" · no existen: {', '.join(inexistentes)}" if inexistentes else ""))
faltan = [c for c in inv_apps if c not in apps_actual]
registra(not faltan, f"{len(inv_apps) - len(faltan)}/{len(inv_apps)} aplicaciones del inventario están en el modelo actual"
         + (f" · faltan: {', '.join(faltan)}" if faltan else ""))
hojas_ok = [c for c in inv_hojas if por_codigo.get(c, {}).get("tipo") == "ApplicationComponent"]
registra(len(hojas_ok) == len(inv_hojas), f"{len(hojas_ok)}/{len(inv_hojas)} hojas de cálculo modeladas como componentes de aplicación"
         + (f" · mal modeladas: {', '.join(sorted(inv_hojas - set(hojas_ok)))}" if len(hojas_ok) != len(inv_hojas) else ""))

# ---------------------------------------------------------------- 3
print("\nComprobación 3 · Cada brecha se puede señalar en los dos modelos")
lista = lambda s: [x.strip() for x in s.split(";") if x.strip()]
sin_señal = []
for b in brechas.itertuples():
    act, obj = lista(b.elemento_actual), lista(b.elemento_objetivo)
    if b.tipo != "Nuevo" and not act:
        sin_señal.append(f"{b.id}: sin elemento actual")
    if b.tipo != "Retirar" and not obj:
        sin_señal.append(f"{b.id}: sin elemento objetivo")
    for c in act:
        if c not in por_codigo or not actual(por_codigo[c]):
            sin_señal.append(f"{b.id}: {c} no está en el modelo actual")
    for c in obj:
        if c not in por_codigo or not objetivo(por_codigo[c]):
            sin_señal.append(f"{b.id}: {c} no está en el modelo objetivo")
    if b.tipo == "Retirar":
        for c in act:
            if c in por_codigo and objetivo(por_codigo[c]):
                sin_señal.append(f"{b.id}: {c} se retira pero sigue en el modelo objetivo")
registra(not sin_señal, f"{len(brechas)} brechas · {len(sin_señal)} sin señalar en los dos modelos"
         + (f": {'; '.join(sin_señal)}" if sin_señal else ""))
gaps_modelo = {v["codigo"] for v in elementos.values() if v["tipo"] == "Gap"}
registra(set(brechas.id) <= gaps_modelo, f"{len(set(brechas.id) & gaps_modelo)}/{len(brechas)} brechas registradas como elemento Gap del modelo")

print("\n" + ("Resultado: todas las comprobaciones pasaron." if not fallas else f"Resultado: {len(fallas)} comprobaciones fallaron."))
sys.exit(1 if fallas else 0)
