# AR01 · Principios de arquitectura — DICOSUR

**PETI · Sección 5.1** · Taller 10 · Clasificación **Restringida**

Siete principios gobiernan las decisiones de arquitectura del plan. Cada uno deriva de un hallazgo del diagnóstico (secciones 2.4, 3.1, 3.3 y 3.4) o de una estrategia (Sección 3.5), y se cita en el modelo de Archi como elemento *Principle* de la capa de motivación.

---

## AP-01 · Dato único con dueño

| Campo | Contenido |
|---|---|
| **Declaración** | Cada entidad de negocio tiene una única fuente autoritativa y un dueño de dato designado por cargo. |
| **Razón** | Las decisiones se toman con cifras discrepantes: el cliente vive en tres lugares (8 400 · 340 · 8 900 registros) y tres áreas mantienen hojas de clientes propias (D7). El inventario de datos encontró **5 de 10 entidades sin fuente autoritativa y 5 de 10 sin dueño** (AR02). |
| **Implicancias** | Ningún proyecto puede crear una segunda base de una entidad existente. Todo proyecto que consuma una entidad usa su fuente autoritativa. El paquete de gobierno del dato (WP-03) se ejecuta antes que el de analítica (WP-07). |
| **Trazabilidad** | D7 (Sección 2.4, supuesto básico #3) · F2 (Sección 3.1.3, VRIO: ventaja no capturada) · E-09 → P-08 |

## AP-02 · Integración por servicios, no por archivos ni por re-digitación

| Campo | Contenido |
|---|---|
| **Declaración** | Las aplicaciones intercambian datos mediante servicios publicados y documentados; no por archivos planos nocturnos ni por volver a digitar. |
| **Razón** | El ERP y el WMS se sincronizan una vez por noche (INT-01) y los pedidos del portal se vuelven a digitar (INT-02): el stock del día es una estimación y el portal no puede prometer disponibilidad. |
| **Implicancias** | Toda integración nueva se publica en la capa de integración. Las integraciones por archivo existentes se migran a servicios antes de construir sobre ellas (ruteo, portal). |
| **Trazabilidad** | D3 y D4 (Sección 3.1.1, CV-03 y CV-05) · E-01, E-02 |

## AP-03 · Continuidad antes que funcionalidad

| Campo | Contenido |
|---|---|
| **Declaración** | Ningún proyecto agrega funcionalidad sobre una plataforma que no tiene soporte del fabricante o cuya recuperación no se ha probado. |
| **Razón** | La plataforma del servidor del ERP terminó sus actualizaciones de seguridad extendidas el 13/10/2026 (A2, PE-05) y el respaldo diario en disco local no se ha restaurado en 12 meses (D6). Un único servidor aloja ERP, WMS y base de datos. |
| **Implicancias** | WP-01 (continuidad y plataforma) es la primera ola de la hoja de ruta. La capa de integración se construye sobre la plataforma migrada, no sobre la actual. |
| **Trazabilidad** | A2 (Sección 3.3, PE-05) · D6 (Sección 3.1.4) · E-05, E-12 → P-01, P-03 |

## AP-04 · Privacidad y seguridad desde el diseño

| Campo | Contenido |
|---|---|
| **Declaración** | Toda entidad con datos personales está registrada como tratamiento, clasificada y protegida antes de ser integrada, compartida o analizada. |
| **Razón** | 6 de 10 entidades contienen datos personales (AR02) y no existe registro de actividades de tratamiento (D5), con el D. S. 016-2024-JUS vigente y multas de hasta 100 UIT (A3, PE-09). |
| **Implicancias** | El registro de tratamientos (WP-02) precede al maestro de clientes y a la analítica. Las vistas que se entregan a la organización no muestran detalle técnico sensible. |
| **Trazabilidad** | D5 (Sección 3.1.5) · A3 y A6 (Sección 3.3, PE-08 y PE-09) · E-11 → P-02 |

## AP-05 · Canal digital primero

| Campo | Contenido |
|---|---|
| **Declaración** | El pedido del cliente se captura en origen por un canal digital integrado; la atención telefónica es la excepción asistida, no la regla. |
| **Razón** | Solo el 6 % de los 61 200 pedidos de 2025 entró por el portal (D3), mientras dos mayoristas con aplicación de pedidos ya atienden bodegas de Tacna (A1) y el 60,1 % de los hogares tiene internet (O1). |
| **Implicancias** | El portal se integra al ERP y al inventario en tiempo real; cada pedido nuevo de canal telefónico se registra en el mismo flujo digital. |
| **Trazabilidad** | Visión (Sección 2.2) · OE-04 · D3, O1, A1 · E-01, E-08 → P-04, P-07 |

## AP-06 · Una hoja de cálculo no es un sistema de registro

| Campo | Contenido |
|---|---|
| **Declaración** | Ningún proceso crítico se ejecuta sobre una hoja de cálculo como fuente de datos; las hojas son solo para análisis personal sobre datos de la fuente autoritativa. |
| **Razón** | Seis hojas de cálculo operan como sistema (APP-06 a APP-11); el ruteo, que soporta el 22 % del costo operativo, corre sobre una de ellas (D4). |
| **Implicancias** | Cada hoja que funciona como sistema tiene un reemplazo en la arquitectura objetivo y una fecha de retiro en el paquete de trabajo correspondiente. |
| **Trazabilidad** | D4 (Sección 3.1.1, CV-03) · D1 (Sección 3.1.5) · E-02, E-07 → P-05, P-06 |

## AP-07 · Ningún sistema depende de una sola persona

| Campo | Contenido |
|---|---|
| **Declaración** | Todo componente de aplicación tiene código y configuración versionados, documentación de arquitectura y al menos dos responsables capaces de operarlo. |
| **Razón** | Un solo desarrollador conoce el código del portal B2B (D2) y 2 de 8 personas de TI renunciaron en 12 meses (A5). |
| **Implicancias** | WP-09 (gestión del conocimiento) se ejecuta en la primera ola, antes de modificar el portal. Ningún paquete de trabajo se cierra sin su documentación en el repositorio. |
| **Trazabilidad** | D2 (Sección 3.1.3, VRIO) · A5 (Sección 3.2.2) · E-10 → P-09 |
