# 5. Arquitectura empresarial

**PETI de DICOSUR · v0.10** · Clasificación **Restringida** · Modelo: `05_arquitectura/DICOSUR_arquitectura.archimate` (ArchiMate 3.2, formato de Archi)

## 5.1 Principios de arquitectura

Siete principios gobiernan las decisiones del plan. El detalle de cada uno (declaración, razón, implicancias y trazabilidad) está en [`AR01_principios.md`](AR01_principios.md).

| Código | Principio | Deriva de |
|---|---|---|
| AP-01 | Dato único con dueño | D7 · F2 · E-09 |
| AP-02 | Integración por servicios, no por archivos ni por re-digitación | D3 · D4 · E-01 · E-02 |
| AP-03 | Continuidad antes que funcionalidad | A2 (PE-05) · D6 · E-05 · E-12 |
| AP-04 | Privacidad y seguridad desde el diseño | D5 · A3 · A6 · E-11 |
| AP-05 | Canal digital primero | Visión (2.2) · D3 · O1 · A1 |
| AP-06 | Una hoja de cálculo no es un sistema de registro | D4 · D1 · E-02 · E-07 |
| AP-07 | Ningún sistema depende de una sola persona | D2 · A5 · E-10 |

## 5.2 Arquitectura actual (as-is)

Fuente: inventario entregado por la organización ([`docs/caso/arquitectura-actual.md`](../docs/caso/arquitectura-actual.md)). Vista por capas: `graficos/V01_arquitectura_actual_capas.png`.

### 5.2.1 Capa de negocio: actores, procesos y servicios

- **Actores:** cliente (bodega), vendedor, jefe de almacén, jefe de despacho, analista comercial, tesorería. **Roles:** solicitante de pedido, aprobador de crédito, despachador.
- **Procesos (cadena de valor, 3.1.1):** abastecimiento · toma de pedido por teléfono y papel · aprobación de crédito · preparación · ruteo y despacho · facturación · cobranza · atención de reclamos por correo · análisis comercial · gestión de personal.
- **Servicios de negocio:** entrega en 24 h · crédito a 30 días · atención de reclamo.
- **Objetos de negocio:** cliente · producto · pedido · comprobante · ruta de despacho.

### 5.2.2 Capa de datos: entidades, fuentes autoritativas y dueños

Diez entidades inventariadas en [`AR02_entidades.csv`](AR02_entidades.csv) (vista `V03_estructura_informacion.png`).

**Entidades sin fuente autoritativa: 5 de 10** (cliente, precio, inventario, ruta de despacho, cuenta por cobrar). **Sin dueño: 5 de 10** (cliente, producto, precio, pedido, ruta). **Sin fuente ni dueño a la vez: 3 de 10** (cliente, precio, ruta). **Con datos personales: 6 de 10**, una de ellas con datos sensibles (trabajador, Restringida).

El cliente es el caso más grave: reside en el ERP (8 400), en el portal (340) y en la hoja comercial (8 900); 500 clientes de la hoja no existen en el ERP.

### 5.2.3 Capa de aplicación: componentes, servicios e integraciones

Doce componentes: ERP, portal B2B, WMS, planilla, facturación electrónica, correo y **seis hojas de cálculo que funcionan como sistema** (ruteo, clientes, precios, cobranza, personal y reportes). Servicios: registro de pedido, consulta de stock, emisión de comprobante. Integraciones: ERP↔WMS por archivo plano nocturno; portal→ERP por re-digitación; ERP→portal por carga diaria de archivo; ERP→OSE por servicio web (la única en línea).

### 5.2.4 Capa de tecnología: nodos, servicios y redes

Servidor local único del ERP (aloja ERP, WMS y base de datos; plataforma en fin de soporte), VPS externo del portal, 41 estaciones y 18 dispositivos móviles. Servicios: base de datos, servicio web, respaldo diario en disco local sin prueba de restauración, correo en la nube y carpeta compartida. Redes: LAN de oficina, LAN y Wi-Fi del almacén, un enlace a internet.

### 5.2.5 Vista de cooperación proceso-aplicación

| Proceso | Sistema que lo soporta | Nivel |
|---|---|---|
| Abastecimiento | ERP Compras | ✓ Bueno |
| Toma de pedido | Teléfono + papel + portal B2B (6 %) | ✗ Deficiente |
| Aprobación de crédito | ERP Créditos | ✓ Bueno |
| Preparación del pedido | WMS + lectores de código de barras | ✓ Bueno |
| Ruteo y despacho | Hoja de cálculo de ruteo | ✗ Deficiente |
| Facturación | ERP Ventas + facturación electrónica | ✓ Bueno |
| Cobranza | ERP + hoja de cobranza | ~ Parcial |
| Atención de reclamos | Correo electrónico | ✗ Deficiente |
| Análisis comercial y reportes | Hojas de cálculo | ✗ Deficiente |
| Gestión de personal y planilla | Planilla + hoja de personal | ~ Parcial |

**Procesos sin soporte o con soporte deficiente: 4 de 10**; otros 2 con soporte parcial. Vista: `V02_cooperacion_proceso_aplicacion.png`.

## 5.3 Arquitectura objetivo (to-be)

### 5.3.1 Derivación: de la visión, las capacidades y las estrategias a la arquitectura

| Insumo | Sección | Qué aporta a la arquitectura objetivo |
|---|---|---|
| Capacidades de TI requeridas | 3.1.5 | Analítica y cumplimiento (madurez 1/5) deben existir: tablero de gestión y registro de tratamientos |
| Visión y objetivos | 2.2 · 6.2 | OE-04 elevar el canal digital (hoy 6 %): portal integrado al ERP y al stock en línea |
| Estrategias del FODA cruzado | 3.5 | E-01, E-02, E-05, E-07, E-09, E-10, E-11, E-12: qué se construye, se compra o se retira |
| Marcos adoptados | 4.2 | COBIT DSS04 (continuidad) y DSS02 / ITIL (atención de solicitudes e incidentes) |
| Proyectos no negociables | 4.1.5 | Plataforma con soporte (ESU terminadas el 13/10/2026) y cumplimiento del D. S. 016-2024-JUS |

### 5.3.2 Cambios por capa, con su origen trazado

| Capa | Elemento actual | Elemento objetivo | Origen del cambio |
|---|---|---|---|
| Negocio | Toma de pedido por teléfono y papel | Autoservicio del cliente por canal digital, con atención asistida como excepción | Visión 2.2 · AP-05 · E-08 |
| Negocio | Atención de reclamos por correo | Atención con registro y trazabilidad (mesa de atención) | ITIL / COBIT DSS02 (4.2) · E-06 |
| Negocio | Sin dueños de dato | Rol «dueño del dato» designado por cargo | AP-01 |
| Datos | Cliente en tres lugares sin dueño | Maestro de clientes del ERP como fuente autoritativa; dueño: gerente comercial | AP-01 · E-09 |
| Datos | Precio en hoja de cálculo | Lista de precios única en el ERP | AP-01 · AP-06 |
| Datos | Stock contable (ERP) y físico (WMS) | Stock autoritativo del WMS publicado como servicio | AP-01 · AP-02 |
| Datos | Sin registro de datos personales | Registro de actividades de tratamiento | 4.1 · D. S. 016-2024-JUS · E-11 |
| Aplicación | Portal B2B sin integración | Portal integrado (web y móvil) al ERP y al stock en tiempo real | Visión 2.2 · E-01 |
| Aplicación | Ruteo en hoja de cálculo | Planificador de rutas integrado al WMS | E-02 (3.5) · AP-06 |
| Aplicación | Integración por archivo plano nocturno | Capa de integración con servicios publicados | AP-02 |
| Aplicación | Análisis en hojas de cálculo | Tablero de gestión sobre el maestro consolidado | E-07 (3.5) |
| Aplicación | Hojas de clientes, precios, cobranza y personal | Retiradas | AP-06 |
| Tecnología | Servidor único sin redundancia | Nodo de contingencia + respaldo verificado con copia inmutable | DSS04 (4.3) · E-12 |
| Tecnología | Plataforma en fin de soporte | Plataforma con soporte vigente | 3.3 PE-05 · E-05 |

### 5.3.3 Vistas objetivo

`graficos/V04_arquitectura_objetivo_capas.png` (elementos nuevos o modificados en tono intenso).

## 5.4 Análisis de brechas

### 5.4.1 Tabla de brechas por capa y tipo

16 brechas en [`AR03_brechas.csv`](AR03_brechas.csv), 78 semanas-persona.

| Capa | Nuevo | Modificar | Retirar | Total |
|---|---|---|---|---|
| Negocio | 2 | 1 | 0 | 3 |
| Datos | 1 | 3 | 0 | 4 |
| Aplicación | 3 | 2 | 1 | 6 |
| Tecnología | 1 | 2 | 0 | 3 |
| **Total** | **7** | **8** | **1** | **16** |

### 5.4.2 Paquetes de trabajo derivados

| Paquete | Brechas | Esfuerzo (sem-p) | Proyecto (7.1) |
|---|---|---|---|
| WP-01 Continuidad y plataforma del ERP | B-01 · B-02 · B-03 | 18 | P-01 · P-03 |
| WP-02 Cumplimiento de datos personales | B-04 | 4 | P-02 |
| WP-03 Gobierno del dato y maestros | B-05 · B-06 · B-07 · B-09 | 14 | P-08 · P-06 (gobierno) |
| WP-04 Capa de integración por servicios | B-08 | 8 | **P-12 (nuevo)** |
| WP-05 Canal digital integrado | B-10 · B-11 | 12 | P-04 · P-07 |
| WP-06 Ruteo y trazabilidad de despacho | B-12 | 7 | P-05 |
| WP-07 Analítica y retiro de hojas de cálculo | B-13 · B-15 | 8 | P-06 |
| WP-08 Atención de reclamos con trazabilidad | B-14 | 4 | P-11 |
| WP-09 Gestión del conocimiento del portal | B-16 | 3 | P-09 |

### 5.4.3 Dependencias y secuencia obligada

- **Ola 1:** WP-01 · WP-02 · WP-09 (sin dependencias).
- **Ola 2:** WP-04 (requiere la plataforma migrada de WP-01).
- **Ola 3:** WP-03 (requiere el registro de tratamientos de WP-02 y los servicios de WP-04).
- **Ola 4:** WP-05 · WP-06 · WP-07 · WP-08.

Ruta crítica por esfuerzo: **WP-01 → WP-04 → WP-03 → WP-05 = 52 semanas-persona**. La analítica (WP-07) queda después del gobierno del dato (WP-03) y del cumplimiento (WP-02).

**Los paquetes de trabajo son el insumo directo del portafolio (Sección 7.1).** El análisis agrega un proyecto que el FODA cruzado no había nombrado: la capa de integración (P-12), de la que dependen el canal digital, el ruteo y el maestro de stock.
