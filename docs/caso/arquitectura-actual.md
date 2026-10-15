# Inventario de la arquitectura actual — DICOSUR

**Distribuidora Comercial del Sur S.A.C. (DICOSUR)** · Tacna · Documento entregado por la organización para la Semana 10 · Clasificación **Restringida**

> Insumo del Taller 10. Describe lo que **opera hoy**, incluidas las hojas de cálculo que funcionan como sistema. Es consistente con las secciones 2.4 y 3.1 del PETI (Taller 07). **No señala brechas**: encontrarlas es el taller.
>
> Por la regla de seguridad del taller, este inventario no registra direcciones IP, credenciales, nombres de equipos ni versiones exactas de software. La plataforma del servidor del ERP se describe como «plataforma en fin de soporte» (detalle en la Sección 3.3, PE-05).

## 1. Organización

| Dato | Valor |
|---|---|
| Colaboradores | 48 |
| Clientes minoristas activos (bodegas) | 8 400 |
| Flota propia | 9 unidades · 38 rutas de reparto |
| Pedidos 2025 | 61 200 (6 % ingresó por el portal B2B) |
| Áreas | Gerencia General · Gerencia Comercial (ventas y fuerza de ventas) · Logística (almacén y despacho) · Administración y Finanzas (contabilidad, tesorería, créditos y cobranzas) · Recursos Humanos · TI (8 personas) |

## 2. Aplicaciones que operan

| Código | Aplicación | Tipo | Área usuaria | Dónde corre |
|---|---|---|---|---|
| APP-01 | ERP — módulos Compras, Ventas, Inventarios, Créditos y Contabilidad | Paquete comercial | Todas | Servidor local del ERP |
| APP-02 | Portal B2B de pedidos | Desarrollo propio (un solo desarrollador) | Comercial · clientes | VPS externo |
| APP-03 | WMS — gestión de almacén con lectores de código de barras | Paquete comercial | Logística | Servidor local del ERP |
| APP-04 | Sistema de planilla | Paquete comercial | RR. HH. | Estación de trabajo de RR. HH. |
| APP-05 | Conector de facturación electrónica (OSE) | Servicio de terceros | Contabilidad | Nube del proveedor |
| APP-06 | Hoja de cálculo de ruteo | Hoja de cálculo | Despacho | Estación del jefe de despacho |
| APP-07 | Hoja de cálculo comercial de clientes | Hoja de cálculo | Comercial | Carpeta compartida |
| APP-08 | Hoja de cálculo de lista de precios | Hoja de cálculo | Comercial | Carpeta compartida |
| APP-09 | Hoja de cálculo de cobranza | Hoja de cálculo | Créditos y cobranzas | Estación de tesorería |
| APP-10 | Hoja de cálculo de personal | Hoja de cálculo | RR. HH. | Estación de RR. HH. |
| APP-11 | Hojas de cálculo de reportes gerenciales | Hoja de cálculo | Gerencia · Comercial | Carpeta compartida |
| APP-12 | Correo electrónico corporativo | Servicio en la nube | Todas (recibe reclamos) | Nube del proveedor |

No existe CRM, ni herramienta de analítica, ni mesa de atención de reclamos.

## 3. Qué sistema soporta cada proceso

| Proceso (cadena de valor, Sección 3.1.1) | Cómo se ejecuta hoy |
|---|---|
| Abastecimiento (compras a proveedores) | ERP Compras |
| Toma de pedido | Teléfono y nota de pedido en papel del vendedor; 6 % por el portal B2B. Los pedidos del portal se vuelven a digitar en el ERP |
| Aprobación de crédito | ERP Créditos (límite de crédito por cliente) |
| Preparación del pedido | WMS con lectores de código de barras |
| Ruteo y despacho | Hoja de cálculo de ruteo, armada cada noche con la exportación del WMS |
| Facturación | ERP Ventas + conector de facturación electrónica |
| Cobranza | ERP (cuentas por cobrar) + hoja de cálculo de cobranza que mantiene tesorería |
| Atención de reclamos | Correo electrónico; sin registro ni seguimiento |
| Análisis comercial y reportes | Hojas de cálculo armadas a mano en 3 días al cierre de cada mes |
| Gestión de personal y planilla | Sistema de planilla + hoja de cálculo de personal |

## 4. Integraciones

| Código | Origen → destino | Mecanismo | Frecuencia |
|---|---|---|---|
| INT-01 | ERP ↔ WMS | Archivo plano | Nocturna (lote) |
| INT-02 | Portal B2B → ERP | No hay: el pedido se vuelve a digitar | Manual |
| INT-03 | ERP → Portal B2B (stock y precios) | Exportación a archivo y carga manual | Diaria |
| INT-04 | ERP → Facturación electrónica (OSE) | Servicio web del proveedor | En línea |
| INT-05 | Planilla → ERP Contabilidad | Exportación a archivo | Mensual |
| INT-06 | ERP / WMS → hojas de cálculo | Exportación manual a hoja de cálculo | Diaria o mensual |

## 5. Entidades de datos

| Entidad | Sistemas donde reside | Registros por sistema | Observación de la organización |
|---|---|---|---|
| Cliente | ERP · Portal B2B · Hoja comercial | 8 400 · 340 · 8 900 | Cada área usa «su» base |
| Producto | ERP · WMS · Hoja de precios | 3 150 · 3 090 · 2 870 | Altas de producto las hace quien las necesita |
| Precio | ERP · Hoja de precios · Portal B2B | 3 150 · 2 870 · 1 200 | Comercial actualiza la hoja; el ERP se corrige después |
| Pedido | ERP · Portal B2B · WMS | 61 200 · 3 670 · 61 050 | — |
| Comprobante de pago | ERP · Facturación electrónica | 64 800 · 64 800 | — |
| Inventario (stock) | ERP · WMS | 3 150 · 3 090 | Contabilidad usa el ERP; almacén usa el WMS |
| Ruta de despacho | Hoja de ruteo · WMS (guías) | 38 · 38 | Incluye conductor y placa |
| Cuenta por cobrar | ERP · Hoja de cobranza | 2 140 · 2 310 | Tesorería registra acuerdos de pago solo en la hoja |
| Trabajador | Planilla · ERP (usuarios y vendedores) · Hoja de personal | 48 · 52 · 48 | — |
| Proveedor | ERP | 410 | — |

## 6. Tecnología

| Elemento | Descripción |
|---|---|
| Servidor del ERP | Servidor físico local, único, sin redundancia. Aloja el ERP, el WMS y la base de datos. Plataforma en fin de soporte del fabricante |
| VPS del portal | Servidor virtual contratado a un proveedor externo |
| Estaciones de trabajo | 41 equipos de escritorio y portátiles |
| Dispositivos móviles | Teléfonos de la fuerza de ventas (12) y lectores de almacén (6) |
| Servicios | Base de datos del ERP · servicio web del portal · respaldo diario en disco local (sin prueba de restauración en 12 meses) · correo en la nube · carpeta compartida de archivos |
| Redes | LAN de oficina · LAN y Wi-Fi del almacén · enlace a internet (un proveedor) |
