<div align="center">
  <img src="../../../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../../../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">MUNICIPALIDAD DISTRITAL DE ALTO SELVA</h1>

<p align="center">
  Banco de casos · <strong>Empresa 03</strong> · Gobierno local · municipalidad distrital<br>
  <em>Organización ficticia. Cualquier parecido con una empresa real es coincidencia.</em>
</p>

---

## A. Ficha de la organización

| Campo | Contenido |
|---|---|
| **Razón social** | MUNICIPALIDAD DISTRITAL DE ALTO SELVA |
| **Sector** | Gobierno local · municipalidad distrital |
| **Domicilio fiscal** | Provincia de Tacna |
| **RUC** | 20147XXXXX *(enmascarado; es una organización ficticia)* |
| **Años de operación** | 61 |
| **Personal en planilla** | 178 |
| **Personal adicional** | 94 bajo CAS y locación |
| **Facturación / presupuesto anual** | S/ 31.2 millones de presupuesto institucional modificado |
| **Mercado o población atendida** | 41 800 habitantes |
| **Naturaleza** | **Entidad pública.** Le aplica el marco de gobierno digital y el control gubernamental. |
| **Entidades que la regulan o supervisan** | PCM-SGTD (gobierno digital) · Contraloría General · MEF · ANPD · OSCE |

**Objetivo declarado para TI en el periodo.** Constituir el gobierno digital exigible y recuperar el control de los sistemas críticos.

## B. Estructura y gobierno

| | |
|---|---|
| **Personal de TI** | 3 personas |
| **Responsable de TI** | Jefe de la Unidad de Tecnologías de la Información, reporta a Gerencia Municipal. Rotó tres veces en cuatro años |
| **Comité de TI o de gobierno digital** | No existe. |
| **Política de seguridad de la información** | Existe desde 2022, sin difusión ni revisión posterior. |
| **Presupuesto de TI del periodo** | S/ 520 000 · 1.67 % de la facturación |

> **Marco de gobierno digital.** Por ser entidad pública, le son exigibles el Decreto Legislativo 1412, el D. S. 029-2021-PCM y la designación del Comité y del Líder de Gobierno Digital (R.M. 119-2018-PCM). Verificar el estado real de cada obligación es parte del diagnóstico.

## C. Sistemas de información

| Sistema | Descripción | Dónde corre | Desde | ¿Tiene soporte vigente? |
|---|---|---|---|---|
| **SIAF-SP** | Sistema del MEF, obligatorio | Cliente local contra servidor del MEF | 2008 | MEF |
| **Trámite documentario** | Desarrollo propio en PHP, sin documentación | Servidor en la sede | 2015 | No, el desarrollador ya no trabaja aquí |
| **Rentas y catastro** | Producto adquirido por licitación | Servidor en la sede | 2019 | Vencido desde 2023 |
| **Portal de transparencia estándar** | Plataforma de la PCM | Nube del Estado | 2013 | PCM |
| **Mesa de partes virtual** | Formulario web más correo | Hosting contratado | 2020 | No |

**El problema que la organización reconoce.** No existe Comité de Gobierno Digital ni Líder de Gobierno Digital designado, pese a ser exigible. El Plan de Gobierno Digital nunca se formuló.

## D. Procesos de negocio

| N.º | Proceso | ¿Qué sistema lo soporta? |
|---|---|---|
| 1 | Trámite documentario y mesa de partes | Trámite documentario |
| 2 | Recaudación de tributos municipales | Rentas y catastro |
| 3 | Licencias de funcionamiento y edificación | Rentas y catastro |
| 4 | Registro civil | *Sin sistema: se opera en papel* |
| 5 | Contrataciones y logística | SIAF-SP |
| 6 | Atención al ciudadano | Mesa de partes virtual |

## E. Instrumentos de planeamiento existentes

| Instrumento | ¿Existe? | Vigencia | Estado real |
|---|---|---|---|
| Plan Estratégico Institucional (PEI) | Sí | 2023–2027 | Aprobado por resolución, se cumple parcialmente. |
| Plan Operativo Institucional (POI) | Sí | 2025 | Se formula cada año para efectos presupuestales. |
| Plan Estratégico de Tecnologías de la Información (PETI) | **No** | — | **Nunca se ha formulado.** |
| Plan de Gobierno Digital | **No** | — | **Exigible por el D. Leg. 1412 y la R.S.G.D. 005-2018-PCM/SEGDI. No existe.** |
| Política de seguridad de la información | Parcial | — | Existe desde 2022, sin difusión ni revisión posterior. |
| Plan de continuidad del negocio | No | — | No existe. El BIA de `datos/bia.csv` es un borrador incompleto elaborado por un practicante. |
| Inventario de servicios digitales | Parcial | — | Sin responsable asignado. |
| Comité de Gobierno Digital y Líder de Gobierno Digital | **No** | — | **Exigible por la R.M. 119-2018-PCM. No se ha designado.** |

## F. Situación de TI — hechos verificables para el diagnóstico

Son los hechos que la organización admite y que pueden darse por ciertos. Todo lo demás se pregunta en la entrevista.

| Aspecto | Situación verificada |
|---|---|
| **Respaldos** | Se ejecutan a disco local y nunca se ha probado una restauración completa. |
| **Gestión de cambios** | Los cambios en producción se aplican directamente, sin registro ni aprobación. |
| **Segundo factor de autenticación** | No está habilitado en ningún sistema. |
| **Capacitación en seguridad** | Nunca se ha hecho. |
| **Contraseñas** | Hay política escrita desde hace cuatro años, pero el sistema principal no la puede exigir técnicamente. |
| **Registro de incidentes** | Existe un cuaderno físico en TI. |
| **Inventario de activos de TI** | No existe. |
| **Contratos con proveedores de TI** | Los contratos existen pero ninguno define niveles de servicio medibles. |

## G. El incidente del periodo

**Caída del servidor de rentas en campaña de amnistía tributaria**

El servidor de rentas estuvo caído nueve días hábiles durante la amnistía tributaria de 2025. No había respaldo restaurable ni contrato de soporte vigente. La recaudación de esos días se registró en cuadernos y se digitó después.

## H. Riesgos que la organización ya conoce y no ha tratado

| N.º | Riesgo conocido | ¿Tratado? |
|---|---|---|
| 1 | Incumplimiento del marco de gobierno digital | No |
| 2 | Sistema crítico sin soporte ni código fuente documentado | No |
| 3 | Datos personales de contribuyentes sin registro de tratamiento | No |

## I. Datos entregados

Los siete archivos de `datos/` corresponden al periodo del 1 de enero al 31 de diciembre de 2025. Fueron generados con la semilla de esta empresa. **No coinciden con los de ningún otro equipo**.

| Archivo | Qué contiene | Registros |
|---|---|---|
| `pagos.csv` | Población de pagos del periodo — comprobante, fecha, proveedor, concepto, monto, quién registró y quién aprobó | 8 126 |
| `proveedores.csv` | Maestro de proveedores con su contacto y documento de identidad | 89 |
| `empleados.csv` | Planilla del periodo, con fechas de ingreso y cese | 178 |
| `usuarios_erp.csv` | Usuarios del ERP con su perfil, último acceso y estado | 126 |
| `bia.csv` | Análisis de impacto al negocio por proceso, con RTO, RPO y fecha de la última prueba | 6 |
| `presupuesto_ti.csv` | Presupuesto de TI del periodo por partida, planificado contra ejecutado | 7 |
| `inversiones_cerradas.csv` | Tres inversiones cerradas con su beneficio declarado y si se midió | 3 |

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
