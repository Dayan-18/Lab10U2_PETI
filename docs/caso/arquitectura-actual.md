<div align="center">
  <strong>MUNICIPALIDAD DISTRITAL DE ALTO SELVA</strong><br>
  <em>Documento del caso</em>
</div>

---

# Inventario de la arquitectura actual

| | |
|---|---|
| **Organización** | MUNICIPALIDAD DISTRITAL DE ALTO SELVA |
| **Documento** | Inventario de la arquitectura actual |
| **Entregado por** | Tecnologías de la Información, a pedido del equipo |
| **Fecha de entrega** | 18 de marzo de 2026 |
| **Clasificación** | Restringido |

> Documento de una organización ficticia, elaborado para el curso. Cualquier parecido con una empresa real es coincidencia.

---

## 1. Qué es este documento

Es lo que el área de tecnologías de la información entrega cuando se le pide **cómo están armados sus sistemas**. No existía. Se armó a pedido del equipo con lo que el área sabe, y el propio jefe advierte que «faltan cosas que solo están en la cabeza de alguien».

## 2. Aplicaciones que operan

Los sistemas de la ficha, más **las hojas de cálculo que operan como sistema**. El área reconoce que sin ellas la organización no funciona.

| Aplicación | Qué es | Dónde corre | ¿Tiene soporte vigente? |
|---|---|---|---|
| **SIAF-SP** | Sistema del MEF, obligatorio | Cliente local contra servidor del MEF | MEF |
| **Trámite documentario** | Desarrollo propio en PHP, sin documentación | Servidor en la sede | No, el desarrollador ya no trabaja aquí |
| **Rentas y catastro** | Producto adquirido por licitación | Servidor en la sede | Vencido desde 2023 |
| **Portal de transparencia estándar** | Plataforma de la PCM | Nube del Estado | PCM |
| **Mesa de partes virtual** | Formulario web más correo | Hosting contratado | No |
| **Hoja de cálculo · Control de expedientes físicos, en mesa de partes** | Libro de cálculo que un área mantiene por su cuenta | PC del área o carpeta compartida | No |
| **Hoja de cálculo · Fiscalización predial** | Libro de cálculo que un área mantiene por su cuenta | PC del área o carpeta compartida | No |
| **Hoja de cálculo · Registro de licencias** | Libro de cálculo que un área mantiene por su cuenta | PC del área o carpeta compartida | No |

## 3. Qué sistema soporta cada proceso

| Proceso de negocio | Sistema que lo soporta |
|---|---|
| Trámite documentario y mesa de partes | Trámite documentario |
| Recaudación de tributos municipales | Rentas y catastro |
| Licencias de funcionamiento y edificación | Rentas y catastro |
| Registro civil | **Ninguno.** Papel y hojas de cálculo |
| Contrataciones y logística | SIAF-SP |
| Atención al ciudadano | Mesa de partes virtual |

## 4. Integraciones entre sistemas

| De | A | Cómo se integra hoy |
|---|---|---|
| Mesa de partes virtual | Trámite documentario | Manual. Se imprime el correo y se registra |
| Trámite documentario | Rentas y catastro | Ninguna |
| Rentas y catastro | SIAF-SP | Manual. La recaudación se digita al cierre del día |
| Portal de transparencia | Nadie | Lo opera la PCM; se carga a mano |

## 5. Entidades de datos y dónde viven

Lo que el área pudo reconstruir. Los conteos son los que cada sistema devuelve hoy; cuando no coinciden, el área no sabe cuál es el bueno.

| Entidad | Sistemas donde reside | Registros por sistema | ¿Fuente autoritativa declarada? | Dueño del dato, por cargo | Discrepancia que el área conoce | Clasificación | ¿Datos personales? |
|---|---|---|---|---|---|---|---|
| Contribuyente y predio | Rentas · Caja · Mesa de partes · Libro de fiscalización | 22 600 predios · pagos del día · 6 200 solicitudes · 1 900 | Rentas, declarada | Ninguno por cargo | La deuda difiere entre rentas y fiscalización | Confidencial | Sí |
| Expediente | Trámite documentario · Mesa de partes virtual · Libro de mesa de partes · Archivo físico | 6 200 al año en cada uno | Ninguna. El físico manda | Secretaría General | 1 340 expedientes sin estado recuperable tras la caída | Interna | Sí |
| Trabajador | AIRHSP del MEF · Planilla local · Usuarios de trámite | 178 · 272 con CAS y locación · 124 | AIRHSP | Recursos Humanos | Los locadores no figuran en ningún sistema | Restringida | Sí |
| Licencia de funcionamiento | Trámite documentario · Libro de licencias · Archivo físico | 410 al año | El archivo físico | Subgerencia de licencias | Plazos distintos en el libro y en el trámite | Interna | Sí |

## 6. Nodos, dispositivos y redes

**Nodos.** Un servidor en la sede para trámite documentario y rentas, sin autonomía de energía · cliente del SIAF-SP contra el MEF · hosting contratado para la mesa de partes virtual · la plataforma del Estado para transparencia · 95 estaciones.

**Redes.** Red plana sin segmentación. Internet de un proveedor. No hay respaldo fuera de la sede.

## 7. Lo que la organización responde

| Pregunta del equipo | Respuesta |
|---|---|
| ¿Existe un diagrama de arquitectura? | «Hay uno de red en una pizarra. Nunca se dibujaron los sistemas» |
| ¿Quién aprueba que un área cree una hoja de cálculo para operar? | «Nadie. Aparecen y después hay que alimentarlas» |
| ¿Quién es el dueño de cada dato? | «El sistema que lo tiene. Si está en dos, los dos» |
| ¿Qué pasa cuando dos sistemas dicen cifras distintas? | «Se pregunta al que lo lleva y se usa esa» |
| ¿Hay principios de arquitectura escritos? | «No» |

## 8. Marco de referencia

| Marco | Qué aporta |
|---|---|
| **TOGAF, 10.ª edición · ADM** | Fases B, C y D para la arquitectura de negocio, de sistemas de información y de tecnología, y el análisis de brechas |
| **ArchiMate 3.2** | El lenguaje con el que se modelan las capas y sus relaciones |
| **COBIT 2019 · APO03** | Gestión de la arquitectura empresarial |

