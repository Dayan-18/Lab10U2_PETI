# Taller 10 · Arquitectura empresarial actual y objetivo — Municipalidad Distrital de Alto Selva

**SI-886 · Planeamiento Estratégico de TI** · Semana 10 · Universidad Privada de Tacna

Organización analizada: **Municipalidad Distrital de Alto Selva** (Empresa 03 del banco de casos), gobierno local de la provincia de Tacna: 178 trabajadores en planilla y 94 bajo CAS y locación, 41 800 habitantes, presupuesto institucional modificado de S/ 31.2 millones y una Unidad de TI de 3 personas.

**Integrantes (Grupo S):** Jahuira Pilco, Dayan Elvis (2022075749) · Mamani Cori, Cristhian Carlos (2023077282) · Sierra Ruiz, Iker Alberto (2023077090)

> Documento clasificado **Restringido**. El modelo describe la superficie de sistemas de la organización sin direcciones, credenciales, nombres de equipos ni versiones exactas de software (lo verifica `AR04_valida.py`). El taller pide guardar el modelo en un repositorio **privado**.

## Contenido

```
.
├── docs/caso/arquitectura-actual.md      # Insumo: inventario de la arquitectura actual
├── docs/caso/FICHA.md                    # Insumo: ficha de la organización (secciones C y D)
├── 05_arquitectura/
│   ├── AR01_principios.md                # Paso A · doce hallazgos y siete principios
│   ├── AR02_entidades.csv                # Paso B · estructura de la información (8 entidades)
│   ├── AR02_procesos_aplicacion.csv      # Paso B · cooperación proceso-aplicación
│   ├── AR02_estructura.py                # Paso B · conteos de entidades y procesos
│   ├── AR05_elementos.csv                # Pasos B y C · elementos ArchiMate (A actual · O objetivo)
│   ├── AR05_relaciones.csv               # Pasos B y C · relaciones ArchiMate
│   ├── AR05_modelo_archi.py              # Genera el modelo de Archi y las vistas PNG
│   ├── ALTOSELVA_arquitectura.archimate  # Modelo ArchiMate 3.2 (se abre en Archi)
│   ├── AR03_brechas.csv                  # Paso D · 18 brechas
│   ├── AR03_paquetes_def.csv             # Paso D · paquetes y proyecto del portafolio
│   ├── AR03_brechas.py                   # Paso D · paquetes, olas y ruta crítica
│   ├── AR03_paquetes.csv                 # Paso D · salida del script
│   ├── AR04_valida.py                    # Paso F · las tres comprobaciones
│   ├── AR06_genera_anexos.py             # Anexos A–F
│   ├── AR07_capturas.py                  # Capturas de consola y vistas previas
│   └── 5_arquitectura_empresarial.md     # Sección 5 del PETI
├── graficos/                             # Vistas V01–V05 y gráficos de brechas
├── docs/evidencias/S10/                  # Anexos, salidas (.txt) y capturas
└── informe/                              # Informe del taller (PDF y DOCX)
```

## Cómo se reproduce

```bash
python -m pip install pandas matplotlib openpyxl python-docx pymupdf
python 05_arquitectura/AR02_estructura.py
python 05_arquitectura/AR03_brechas.py
python 05_arquitectura/AR05_modelo_archi.py
python 05_arquitectura/AR04_valida.py
python 05_arquitectura/AR06_genera_anexos.py
python 05_arquitectura/AR07_capturas.py
```

Para revisar el modelo en Archi: *File → Open* y elegir `05_arquitectura/ALTOSELVA_arquitectura.archimate`. Las vistas V01–V05 del modelo tienen las mismas coordenadas que los PNG de `graficos/`.

## Etiquetas

| Etiqueta | Qué marca |
|---|---|
| `v0.10` | PETI v0.10 — arquitectura empresarial (Sección 5) |
| `taller-10` | Commit entregado del Taller 10 |
