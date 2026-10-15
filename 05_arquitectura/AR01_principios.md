# AR01 · Principios de arquitectura — Municipalidad Distrital de Alto Selva

**PETI · Sección 5.1** · Taller 10 · Clasificación **Restringida**

Siete principios gobiernan las decisiones de arquitectura del plan. Cada uno deriva de un hallazgo del diagnóstico, tomado de la ficha de la organización (`docs/caso/FICHA.md`) y del inventario de la arquitectura actual (`docs/caso/arquitectura-actual.md`), y se registra en el modelo de Archi como elemento *Principle* de la capa de motivación.

## Hallazgos de partida

| Código | Hallazgo verificable | Fuente |
|---|---|---|
| H-01 | No existe Comité de Gobierno Digital, ni Líder de Gobierno Digital, ni Plan de Gobierno Digital, pese a ser exigibles | Ficha §B y §E · R.M. 119-2018-PCM · D. Leg. 1412 |
| H-02 | No existe PETI ni comité de TI; el jefe de TI rotó tres veces en cuatro años | Ficha §B y §E |
| H-03 | Trámite documentario: desarrollo propio en PHP, sin documentación y sin soporte; el desarrollador ya no trabaja en la entidad | Ficha §C · Inventario §2 |
| H-04 | Rentas y catastro con soporte vencido desde 2023; estuvo caído nueve días hábiles en la amnistía tributaria de 2025 | Ficha §C y §G |
| H-05 | Respaldos a disco local sin restauración probada, sin copia fuera de la sede; servidor único sin autonomía de energía | Ficha §F · Inventario §6 |
| H-06 | Integraciones manuales: el correo de mesa de partes se imprime y se registra; la recaudación se digita al SIAF-SP al cierre del día | Inventario §4 |
| H-07 | Tres hojas de cálculo operan como sistema: control de expedientes físicos, fiscalización predial y registro de licencias | Inventario §2 |
| H-08 | El registro civil no tiene sistema: se opera en papel y hojas | Ficha §D · Inventario §3 |
| H-09 | Ninguna entidad tiene dueño reconocido por todos («el sistema que lo tiene»); el expediente no tiene fuente digital y 1 340 quedaron sin estado tras la caída | Inventario §5 y §7 |
| H-10 | Datos personales de contribuyentes sin registro de tratamiento; sin segundo factor en ningún sistema; nunca hubo capacitación en seguridad | Ficha §F y §H |
| H-11 | Red plana sin segmentación y un solo proveedor de internet | Inventario §6 |
| H-12 | Cambios en producción sin registro ni aprobación; incidentes en cuaderno físico; sin inventario de activos; contratos sin niveles de servicio | Ficha §F |

---

## AP-01 · Gobierno digital exigible primero

| Campo | Contenido |
|---|---|
| **Declaración** | Ninguna inversión de TI se aprueba fuera del Plan de Gobierno Digital ni sin pasar por el Comité de Gobierno Digital y su Líder designado. |
| **Razón** | La municipalidad es entidad pública: el D. Leg. 1412, el D. S. 029-2021-PCM y la R.M. 119-2018-PCM le exigen Comité, Líder y Plan de Gobierno Digital, y no tiene ninguno (H-01). Sin esa instancia, el jefe de TI decide solo y rota (H-02). |
| **Implicancias** | El paquete WP-01 (gobierno digital y de TI) va en la primera ola. Los dueños de dato los designa el Comité. Todo proyecto del portafolio (Sección 7) cita la línea del Plan de Gobierno Digital que atiende. |
| **Trazabilidad** | H-01 · H-02 · Sección 4.1 (obligaciones normativas) · objetivo declarado de TI (Ficha §A) |

## AP-02 · Dato único con dueño por cargo

| Campo | Contenido |
|---|---|
| **Declaración** | Cada entidad de negocio tiene una única fuente autoritativa digital y un dueño de dato designado por cargo. |
| **Razón** | Hoy el dueño es «el sistema que lo tiene» y, si dos sistemas discrepan, «se pregunta al que lo lleva» (H-09). La deuda del contribuyente difiere entre rentas y fiscalización; el inventario de datos encontró **4 de 8 entidades sin fuente autoritativa digital y 5 de 8 sin dueño** (AR02). |
| **Implicancias** | Ningún proyecto crea una segunda base de una entidad existente. Las hojas de cálculo que duplican una entidad se retiran cuando su fuente autoritativa existe (WP-03). |
| **Trazabilidad** | H-09 · H-07 · Inventario §5 y §7 |

## AP-03 · Continuidad antes que funcionalidad

| Campo | Contenido |
|---|---|
| **Declaración** | Ningún proyecto agrega funcionalidad sobre un sistema cuya recuperación no se ha probado o que no tiene soporte vigente. |
| **Razón** | El servidor de rentas estuvo caído nueve días hábiles en plena amnistía tributaria, sin respaldo restaurable ni contrato de soporte, y la recaudación se llevó en cuadernos (H-04, H-05). |
| **Implicancias** | WP-04 (continuidad de la infraestructura) es la primera ola técnica: respaldo fuera de la sede con prueba de restauración y servidor con energía ininterrumpida antes de tocar rentas o trámite. |
| **Trazabilidad** | H-04 · H-05 · COBIT 2019 DSS04 (Sección 4.2) · incidente del periodo (Ficha §G) |

## AP-04 · Ningún sistema crítico sin soporte, código ni documentación

| Campo | Contenido |
|---|---|
| **Declaración** | Todo componente de aplicación que soporta un proceso misional tiene soporte vigente con niveles de servicio medibles, o código fuente versionado y documentado bajo control de la municipalidad. |
| **Razón** | El trámite documentario depende de un desarrollador que se fue y no dejó documentación (H-03); rentas y catastro tiene el soporte vencido (H-04); ningún contrato de TI define niveles de servicio (H-12). |
| **Implicancias** | Los contratos nuevos incluyen niveles de servicio y entrega de documentación. Los desarrollos propios se versionan en el repositorio institucional antes de pasar a producción (WP-05, WP-08). |
| **Trazabilidad** | H-03 · H-04 · H-12 · COBIT 2019 APO09 y BAI03 |

## AP-05 · El registro digital es la fuente; ni el papel ni la hoja de cálculo lo son

| Campo | Contenido |
|---|---|
| **Declaración** | El expediente, la licencia y el acta se registran una vez, en el sistema que les corresponde, y ese registro manda sobre el papel y sobre cualquier hoja de cálculo. |
| **Razón** | Hoy «el físico manda» en expedientes y licencias, tres hojas de cálculo operan como sistema (H-07) y el registro civil se lleva en papel (H-08). |
| **Implicancias** | Cada hoja que funciona como sistema tiene reemplazo y fecha de retiro en un paquete de trabajo. El archivo físico pasa a ser respaldo documental, no fuente. |
| **Trazabilidad** | H-07 · H-08 · H-09 · D. S. 029-2021-PCM (expediente electrónico) |

## AP-06 · Interoperabilidad por servicios del Estado, no por re-digitación

| Campo | Contenido |
|---|---|
| **Declaración** | Los sistemas intercambian datos mediante servicios publicados y, hacia otras entidades, mediante la Plataforma de Interoperabilidad del Estado (PIDE); no se imprime ni se vuelve a digitar. |
| **Razón** | La mesa de partes virtual llega por correo que se imprime, la recaudación se digita al SIAF-SP al cierre del día y el portal de transparencia se carga a mano (H-06). |
| **Implicancias** | Toda integración nueva pasa por la capa de interoperabilidad (WP-07). El registro civil digital se construye sobre ella para consultar a RENIEC. |
| **Trazabilidad** | H-06 · D. Leg. 1412 (interoperabilidad) · Inventario §4 |

## AP-07 · Privacidad y seguridad desde el diseño

| Campo | Contenido |
|---|---|
| **Declaración** | Toda entidad con datos personales está registrada como tratamiento, clasificada y protegida con autenticación de dos factores y red segmentada antes de integrarse o publicarse. |
| **Razón** | 7 de 8 entidades contienen datos personales (AR02), los de contribuyentes no tienen registro de tratamiento, no hay segundo factor y la red es plana (H-10, H-11), con la Ley 29733 y el D. S. 016-2024-JUS vigentes. |
| **Implicancias** | El registro de tratamientos (WP-02) precede a los servicios digitales al ciudadano (WP-06). Las vistas que se entregan a la organización no muestran detalle técnico sensible. |
| **Trazabilidad** | H-10 · H-11 · riesgo conocido 3 (Ficha §H) · Ley 29733 · D. S. 016-2024-JUS |
