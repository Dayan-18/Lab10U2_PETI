# 5. Arquitectura empresarial

**PETI de la Municipalidad Distrital de Alto Selva · v0.10** · Clasificación **Restringida** · Modelo: `05_arquitectura/ALTOSELVA_arquitectura.archimate` (ArchiMate 3.2, formato de Archi)

## 5.1 Principios de arquitectura

Siete principios gobiernan las decisiones del plan. El detalle de cada uno (declaración, razón, implicancias y trazabilidad) y los doce hallazgos de los que derivan están en [`AR01_principios.md`](AR01_principios.md).

| Código | Principio | Deriva de |
|---|---|---|
| AP-01 | Gobierno digital exigible primero | H-01 · H-02 · D. Leg. 1412 · R.M. 119-2018-PCM |
| AP-02 | Dato único con dueño por cargo | H-07 · H-09 |
| AP-03 | Continuidad antes que funcionalidad | H-04 · H-05 · incidente de la amnistía 2025 |
| AP-04 | Ningún sistema crítico sin soporte, código ni documentación | H-03 · H-04 · H-12 |
| AP-05 | El registro digital es la fuente; ni el papel ni la hoja de cálculo lo son | H-07 · H-08 · H-09 |
| AP-06 | Interoperabilidad por servicios del Estado, no por re-digitación | H-06 |
| AP-07 | Privacidad y seguridad desde el diseño | H-10 · H-11 · Ley 29733 |

## 5.2 Arquitectura actual (as-is)

Fuente: inventario entregado por la organización ([`docs/caso/arquitectura-actual.md`](../docs/caso/arquitectura-actual.md)), contrastado con las secciones C y D de la ficha ([`docs/caso/FICHA.md`](../docs/caso/FICHA.md)). Vista por capas: `graficos/V01_arquitectura_actual_capas.png`.

### 5.2.1 Capa de negocio: actores, procesos y servicios

- **Actores:** ciudadano y contribuyente (41 800 habitantes), mesa de partes, Subgerencia de Administración Tributaria, Subgerencia de Licencias, Registro Civil, Logística y Tesorería, Recursos Humanos y Unidad de TI (3 personas). **Roles:** administrado (solicitante), contribuyente, fiscalizador.
- **Procesos (ficha §D):** trámite documentario y mesa de partes · recaudación de tributos municipales · licencias de funcionamiento y edificación · registro civil · contrataciones y logística · atención al ciudadano; y, del inventario, gestión de personal y planilla · transparencia y acceso a la información.
- **Servicios de negocio:** recepción y atención de trámites · pago de tributos · otorgamiento de licencias · inscripción y certificados de registro civil · acceso a la información pública.
- **Objetos de negocio:** contribuyente y predio · expediente · licencia · acta de registro civil · trabajador · pago a proveedor.

### 5.2.2 Capa de datos: entidades, fuentes autoritativas y dueños

Ocho entidades inventariadas en [`AR02_entidades.csv`](AR02_entidades.csv) (vista `V03_estructura_informacion.png`).

**Entidades sin fuente autoritativa digital: 4 de 8** (expediente, licencia de funcionamiento, cuenta de usuario, acta de registro civil). **Sin dueño: 5 de 8** (contribuyente y predio, proveedor, pago a proveedor, cuenta de usuario, acta de registro civil). **Sin fuente ni dueño a la vez: 2 de 8** (cuenta de usuario y acta de registro civil). **Con datos personales: 7 de 8**, dos de ellas con datos sensibles (trabajador y acta de registro civil, Restringidas).

El expediente es el caso más grave: reside en el trámite documentario, en la mesa de partes virtual, en una hoja de control y en el archivo físico, con 6 200 al año en cada uno; «el físico manda» y 1 340 expedientes quedaron sin estado recuperable tras la caída. La deuda del contribuyente difiere entre rentas y la hoja de fiscalización.

### 5.2.3 Capa de aplicación: componentes, servicios e integraciones

Diez componentes: SIAF-SP y AIRHSP (MEF), trámite documentario (desarrollo propio en PHP sin documentación ni soporte), rentas y catastro (soporte vencido desde 2023), portal de transparencia estándar (PCM), mesa de partes virtual (formulario web y correo), planilla local y **tres hojas de cálculo que funcionan como sistema** (control de expedientes físicos, fiscalización predial y registro de licencias). Servicios: registro de expedientes, emisión de recibos y cobro de tributos, registro presupuestal y de pagos, publicación de transparencia. Integraciones: **todas manuales** — el correo de mesa de partes se imprime y se registra; la recaudación se digita al SIAF-SP al cierre del día; trámite y rentas no se integran; el portal de transparencia se carga a mano.

### 5.2.4 Capa de tecnología: nodos, servicios y redes

Un servidor en la sede para trámite documentario y rentas, sin autonomía de energía; cliente del SIAF-SP contra la plataforma del MEF; hosting contratado para la mesa de partes virtual; nube del Estado para transparencia; 95 estaciones de trabajo. Servicios: base de datos, servicio web, respaldo a disco local nunca restaurado por completo y correo institucional. Redes: red plana sin segmentación y un solo proveedor de internet; sin respaldo fuera de la sede.

### 5.2.5 Vista de cooperación proceso-aplicación

| Proceso | Sistema que lo soporta | Nivel |
|---|---|---|
| Trámite documentario y mesa de partes | Trámite documentario (sin soporte) + hoja de expedientes | ✗ Deficiente |
| Recaudación de tributos municipales | Rentas y catastro (sin soporte) + hoja de fiscalización | ~ Parcial |
| Licencias de funcionamiento y edificación | Rentas y catastro + hoja de licencias + archivo físico | ✗ Deficiente |
| Registro civil | Ninguno: papel y hojas de cálculo | ✗ Sin soporte |
| Contrataciones y logística | SIAF-SP (MEF) | ✓ Bueno |
| Atención al ciudadano | Mesa de partes virtual (formulario + correo) | ✗ Deficiente |
| Gestión de personal y planilla | AIRHSP (MEF) + planilla local | ~ Parcial |
| Transparencia y acceso a la información | Portal de transparencia estándar (PCM) | ~ Parcial |

**Procesos sin soporte o con soporte deficiente: 4 de 8**; otros 3 con soporte parcial. Solo contrataciones y logística, sostenido por un sistema del MEF, tiene soporte bueno. Vista: `V02_cooperacion_proceso_aplicacion.png`.

## 5.3 Arquitectura objetivo (to-be)

### 5.3.1 Derivación: de la visión, las capacidades y las estrategias a la arquitectura

| Insumo | Sección | Qué aporta a la arquitectura objetivo |
|---|---|---|
| Objetivo declarado de TI | Ficha §A · 2.2 | «Constituir el gobierno digital exigible y recuperar el control de los sistemas críticos»: Comité, Líder y Plan de Gobierno Digital; sistemas críticos con soporte |
| Capacidades de TI requeridas | 3.1.5 | Continuidad, gestión documental electrónica, interoperabilidad y protección de datos deben existir |
| Estrategias del FODA cruzado | 3.5 | Renovar o reemplazar los sistemas sin soporte, retirar hojas y papel, conectar con la PIDE |
| Marcos adoptados | 4.2 | COBIT 2019 APO03 (arquitectura), DSS04 (continuidad), DSS02 y BAI06 (incidentes y cambios) |
| Proyectos no negociables | 4.1.5 | D. Leg. 1412, D. S. 029-2021-PCM, R.M. 119-2018-PCM y Ley 29733 con el D. S. 016-2024-JUS |

### 5.3.2 Cambios por capa, con su origen trazado

| Capa | Elemento actual | Elemento objetivo | Origen del cambio |
|---|---|---|---|
| Negocio | Sin Comité ni Líder de Gobierno Digital | Comité de Gobierno Digital y Líder designados; proceso de gestión del gobierno digital y de TI | AP-01 · R.M. 119-2018-PCM |
| Negocio | Sin dueños de dato | Rol «dueño del dato» designado por cargo | AP-02 |
| Negocio | Trámite donde el físico manda | Trámite con expediente electrónico y mesa de partes digital | AP-05 · D. S. 029-2021-PCM |
| Negocio | Licencias en hoja y archivo físico | Licencias con registro digital y plazos controlados | AP-05 |
| Negocio | Registro civil en papel | Registro civil digital integrado con RENIEC | AP-05 · AP-06 |
| Negocio | Atención por formulario y correo | Atención con seguimiento del trámite en línea | AP-06 |
| Datos | Expediente en cuatro lugares | Expediente electrónico único; dueño: Secretario General | AP-02 · AP-05 |
| Datos | Deuda distinta en rentas y fiscalización | Padrón de rentas como fuente; dueño: Subgerente de Administración Tributaria | AP-02 |
| Datos | Sin registro de datos personales | Registro de actividades de tratamiento | AP-07 · Ley 29733 |
| Aplicación | Trámite documentario sin soporte ni documentación | Gestión documental con soporte y código bajo control de la municipalidad | AP-04 |
| Aplicación | Rentas y catastro con soporte vencido | Rentas y catastro con soporte vigente y fiscalización integrada | AP-03 · AP-04 |
| Aplicación | Integraciones manuales | Capa de interoperabilidad con servicios publicados y conexión a la PIDE | AP-06 |
| Aplicación | Tres hojas de cálculo como sistema y mesa de partes por correo | Retiradas | AP-05 |
| Aplicación | Incidentes en cuaderno, cambios sin registro | Mesa de ayuda e inventario de activos de TI | AP-04 · COBIT DSS02 y BAI06 |
| Tecnología | Servidor sin autonomía de energía | Servidor con energía ininterrumpida y soporte | AP-03 |
| Tecnología | Respaldo a disco local sin restauración | Respaldo fuera de la sede con restauración probada y copia inmutable | AP-03 · COBIT DSS04 |
| Tecnología | Red plana y sin segundo factor | Red segmentada por zonas y autenticación con segundo factor | AP-07 |

### 5.3.3 Vistas objetivo

`graficos/V04_arquitectura_objetivo_capas.png` (elementos nuevos o modificados en tono intenso).

## 5.4 Análisis de brechas

### 5.4.1 Tabla de brechas por capa y tipo

18 brechas en [`AR03_brechas.csv`](AR03_brechas.csv), 76 semanas-persona.

| Capa | Nuevo | Modificar | Reemplazar | Retirar | Total | Esfuerzo (sem-p) |
|---|---|---|---|---|---|---|
| Negocio | 5 | 2 | 0 | 0 | 7 | 26 |
| Datos | 1 | 2 | 0 | 0 | 3 | 10 |
| Aplicación | 1 | 1 | 2 | 1 | 5 | 29 |
| Tecnología | 0 | 3 | 0 | 0 | 3 | 11 |
| **Total** | **7** | **8** | **2** | **1** | **18** | **76** |

### 5.4.2 Paquetes de trabajo derivados

| Paquete | Brechas | Esfuerzo (sem-p) | Proyecto (7.1) |
|---|---|---|---|
| WP-01 Gobierno digital y de TI | B-01 · B-02 · B-03 | 10 | P-01 Comité, Líder y Plan de Gobierno Digital |
| WP-02 Protección de datos y seguridad | B-04 · B-16 | 7 | P-02 Registro de tratamientos y seguridad de la información |
| WP-03 Fuentes autoritativas y retiro de hojas | B-09 · B-10 · B-15 | 9 | P-03 Gobierno del dato municipal |
| WP-04 Continuidad de la infraestructura | B-05 · B-06 | 7 | P-04 Respaldo verificado y continuidad |
| WP-05 Recuperación de sistemas críticos | B-07 · B-08 | 18 | P-05 Rentas con soporte y gestión documental |
| WP-06 Servicios digitales al ciudadano | B-11 · B-13 · B-14 · B-18 | 16 | P-06 Mesa de partes, licencias y registro civil digitales |
| WP-07 Interoperabilidad con el Estado | B-12 | 6 | P-07 Capa de interoperabilidad y conexión a la PIDE |
| WP-08 Gestión de servicios de TI | B-17 | 3 | P-08 Mesa de ayuda, cambios e inventario de activos |

### 5.4.3 Dependencias y secuencia obligada

- **Ola 1:** WP-01 · WP-04 (sin dependencias: gobierno digital y continuidad).
- **Ola 2:** WP-02 (requiere WP-01 y WP-04) · WP-05 (requiere el respaldo y el servidor de WP-04) · WP-08 (requiere WP-01).
- **Ola 3:** WP-07 (requiere los sistemas recuperados de WP-05).
- **Ola 4:** WP-06 (requiere WP-02, WP-05 y WP-07).
- **Ola 5:** WP-03 (las hojas se retiran cuando sus reemplazos de WP-05 y WP-06 ya operan).

Ruta crítica por esfuerzo: **WP-04 → WP-05 → WP-07 → WP-06 → WP-03 = 56 semanas-persona**. Los servicios digitales al ciudadano (WP-06) quedan después de la protección de datos (WP-02) y de la interoperabilidad (WP-07).

**Los paquetes de trabajo son el insumo directo del portafolio (Sección 7.1).** El análisis agrega dos proyectos que la organización no tenía en su lista: la capa de interoperabilidad (P-07), de la que dependen el registro civil digital y la recaudación sin re-digitación, y la mesa de ayuda con registro de cambios (P-08), sin la cual ningún cambio en los sistemas recuperados queda trazado.
