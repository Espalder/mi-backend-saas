---

<center>

# SISTEMA DE GESTIÓN EMPRESARIAL MULTIMODALIDAD (OFFLINE Y SAAS)

---

## Portada

**Sistema de Gestión Empresarial Multimodalidad (Offline y SaaS)**  
Autor: [Tu Nombre]  
Fecha: [Fecha de entrega]  
Versión: 2.0.0  

[AQUÍ INSERTAR LOGO DEL PROYECTO]

---

## Resumen Ejecutivo

Este informe documenta el desarrollo completo de un sistema de gestión empresarial con doble modalidad: offline (Tkinter + SQLite/MySQL) y SaaS multiempresa (FastAPI + React). El sistema permite gestionar empresas, usuarios, productos, clientes, ventas, reportes y más, garantizando el aislamiento total de datos entre empresas y una experiencia moderna tanto en escritorio como en la nube.

**Nuevas funcionalidades en v2.0.0:**
- Sistema de reportes avanzado con gráficos de barras y torta
- Filtros de fechas precisos con dayjs
- Corrección de permisos para roles vendedor e inventario
- Mejoras en la experiencia de usuario y estabilidad del sistema

---

## Índice

1. Introducción y contexto
2. Objetivos del sistema
3. Justificación y motivación
4. Arquitectura general del sistema
5. Estructura de carpetas y componentes
6. Requerimientos y dependencias
7. Descripción detallada de módulos
8. Formularios y validación de datos
9. Control de versiones y flujo de trabajo
10. Pruebas y validaciones
11. Problemas encontrados y soluciones
12. Despliegue y uso
13. Diagramas y capturas
14. Conclusiones y recomendaciones
15. Agradecimientos
16. Anexos

---

## 1. Introducción y contexto

El presente proyecto surge de la necesidad de contar con una solución de gestión empresarial flexible, capaz de operar tanto en entornos offline (local) como en la nube bajo el modelo SaaS. Se buscó cubrir las necesidades de pequeñas y medianas empresas que requieren control de inventario, ventas, reportes y administración multiusuario, con la posibilidad de migrar fácilmente entre modalidades.

**Actualizaciones recientes:**
- Implementación de sistema de reportes con gráficos interactivos
- Corrección de permisos y roles de usuario
- Mejoras en la estabilidad y rendimiento del sistema

---

## 2. Objetivos del sistema

- Desarrollar un sistema robusto y seguro para la gestión empresarial.
- Permitir la operación en modo offline (Tkinter + SQLite/MySQL) y SaaS multiempresa (FastAPI + React).
- Garantizar el aislamiento de datos entre empresas en la nube.
- Ofrecer una experiencia de usuario moderna y amigable.
- Facilitar la administración, el control de versiones y el despliegue.
- **Nuevo:** Proporcionar reportes avanzados con visualizaciones gráficas.
- **Nuevo:** Implementar sistema de roles y permisos granular.

---

## 3. Justificación y motivación

La digitalización de procesos empresariales es clave para la competitividad. Muchas empresas requieren soluciones que funcionen sin conexión a internet, pero también desean aprovechar las ventajas del SaaS. Este sistema responde a esa necesidad, permitiendo una transición fluida entre ambos mundos y asegurando la continuidad operativa.

**Beneficios de las nuevas funcionalidades:**
- Reportes visuales facilitan la toma de decisiones
- Sistema de roles mejora la seguridad y control de acceso
- Filtros precisos optimizan la búsqueda de información

---

## 4. Arquitectura general del sistema

El sistema se compone de tres grandes bloques:
- **Backend SaaS:** API RESTful desarrollada con FastAPI, gestionando la lógica de negocio y la persistencia de datos multiempresa.
- **Frontend SaaS:** Aplicación React moderna, responsiva y con excelente UX, conectada al backend vía API.
- **Sistema Offline:** Aplicación de escritorio en Python (Tkinter), capaz de operar con SQLite local o conectarse a la base de datos en la nube.

**Nuevas características arquitectónicas:**
- Integración de Chart.js para visualizaciones
- Sistema de filtros temporales con dayjs
- Endpoints especializados para reportes agrupados

[AQUÍ INSERTAR DIAGRAMA DE ARQUITECTURA GENERAL]

---

## 5. Estructura de carpetas y componentes

[AQUÍ INSERTAR DIAGRAMA DE ESTRUCTURA DE CARPETAS]

Explicación detallada de cada carpeta y archivo relevante, incluyendo backend, frontend, sistema offline, scripts y recursos.

**Archivos modificados recientemente:**
- `frontend_saas/src/pages/ReportesPage.tsx`: Nuevos gráficos y filtros
- `frontend_saas/src/components/MainLayout.tsx`: Corrección de imports
- `frontend_saas/src/routes/AppRouter.tsx`: Corrección de permisos
- `backend_saas/app/api/ventas.py`: Nuevos endpoints para reportes

---

## 6. Requerimientos y dependencias

### Backend (FastAPI)
- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- python-jose
- passlib[bcrypt]
- mysql-connector-python

### Frontend (React)
- React 19+
- @mui/material (Material UI)
- @mui/icons-material
- axios
- react-router-dom
- dayjs
- **Nuevo:** chart.js
- **Nuevo:** react-chartjs-2

### Sistema Offline (Tkinter)
- Python 3.10+
- tkinter
- mysql-connector-python
- sqlite3
- Pillow (para imágenes)

[AQUÍ INSERTAR CAPTURA DE PANTALLA DE INSTALACIÓN DE DEPENDENCIAS]

---

## 7. Descripción detallada de módulos

### Backend
- **Autenticación y autorización:** JWT, roles, permisos, endpoints protegidos.
- **Empresas:** Gestión multiempresa, aislamiento de datos.
- **Usuarios:** Registro, login, edición, roles.
- **Productos, clientes, proveedores, ventas, compras, reportes:** CRUD completo, validaciones, lógica de negocio.
- **Nuevo:** Endpoints especializados para reportes agrupados por día y categoría.

### Frontend
- **Login y registro:** Formularios modernos, validación en frontend y backend.
- **Dashboard:** Visualización de métricas y datos clave.
- **Gestión de entidades:** ABM de productos, clientes, ventas, usuarios, etc.
- **Reportes:** Generación y descarga de reportes en PDF.
- **Nuevo:** Gráficos interactivos de barras y torta.
- **Nuevo:** Filtros de fechas precisos con dayjs.
- **Nuevo:** Sistema de roles y permisos en la interfaz.

### Sistema Offline
- **Interfaz gráfica:** Tkinter, menús, formularios, tablas.
- **Sincronización:** Modo local (SQLite) y modo online (MySQL en Railway).
- **Gestión de datos:** CRUD completo, validaciones en Python.

[AQUÍ INSERTAR CAPTURAS DE PANTALLA DE CADA MÓDULO]

---

## 8. Formularios y validación de datos

- **Backend:** Uso de Pydantic para validar todos los datos recibidos en los endpoints. Ejemplo: validación de campos obligatorios, tipos y unicidad en productos, clientes, ventas, etc.
- **Frontend:** Formularios controlados con React y Material UI. Validación manual en el código, asegurando que los datos sean correctos antes de enviarlos al backend.
- **Offline:** Formularios gráficos con Tkinter, validación directa en Python antes de guardar en la base de datos.
- **Nuevo:** Validación de fechas con dayjs para filtros precisos en reportes.

[AQUÍ INSERTAR CAPTURA DE FORMULARIO DE REGISTRO DE PRODUCTO]

---

## 9. Control de versiones y flujo de trabajo

Durante el desarrollo de este sistema se utilizó **Git** para el control de versiones y **GitHub** como repositorio remoto, siguiendo buenas prácticas para asegurar la trazabilidad y calidad del código.

- **Estructura de ramas:**
  - Se trabajó principalmente en la rama `main`, creando ramas temporales para nuevas funcionalidades o correcciones importantes, por ejemplo:
    - `feature/soporte-multiempresa`
    - `bugfix/endpoint-empresas-me`
    - `docs/actualizar-readme`
    - **Nuevo:** `feature/reportes-graficos`
    - **Nuevo:** `fix/permisos-vendedor`

- **Convenciones de commits:**
  - Se emplearon mensajes de commit claros y estructurados, siguiendo el formato:
    - `feat: descripción de nueva funcionalidad`
    - `fix: descripción de corrección`
    - `docs: cambios en documentación`
  - Ejemplos reales:
    - `feat: agregar validación de empresa en endpoints de ventas`
    - `fix: corregir error 422 en endpoint /empresas/me`
    - `docs: agregar sección de dependencias en README`
    - **Nuevo:** `feat(reportes): agregar gráficos de barras y torta con filtros`
    - **Nuevo:** `fix(reportes): filtrar ventas en tabla solo dentro del rango exacto de fechas`
    - **Nuevo:** `fix: corregir imports y eliminar useTheme no usado`

- **Flujo de trabajo:**
  1. Crear una rama para cada nueva funcionalidad o corrección.
  2. Realizar commits frecuentes y descriptivos.
  3. Subir los cambios a GitHub (`git push`).
  4. (Opcional) Crear un Pull Request para revisión y merge.
  5. Fusionar los cambios a `main` tras revisión y pruebas.

- **Gestión de issues y pull requests:**
  - Se utilizaron issues para registrar bugs y tareas pendientes.
  - Los pull requests se revisaban antes de fusionar a la rama principal.

- **Buenas prácticas:**
  - Commits atómicos y enfocados.
  - Documentación de cada cambio relevante.
  - Antes de unir los cambios al proyecto principal, siempre revisamos que todo funcione bien y que no haya errores.

---

## 10. Pruebas y validaciones

- Pruebas manuales y automáticas de endpoints, formularios y flujos críticos.
- Uso de Postman, PowerShell y el frontend para validar el correcto funcionamiento de la API y la interfaz.
- Pruebas multiempresa: creación de empresas, usuarios, productos y ventas en paralelo para asegurar el aislamiento de datos.
- Validación de roles y permisos en cada operación.
- **Nuevo:** Pruebas de gráficos y filtros de fechas en reportes.
- **Nuevo:** Validación de permisos por rol en todas las rutas.

[AQUÍ INSERTAR CAPTURAS DE PRUEBAS EN POSTMAN Y FRONTEND]

---

## 11. Problemas encontrados y soluciones

### Problemas recientes y sus soluciones:

#### 1. Permisos de roles vendedor
- **Problema:** Los usuarios con rol vendedor no podían acceder a las páginas de Clientes y Reportes
- **Causa:** Las rutas en el frontend estaban protegidas solo para admin
- **Solución:** Se modificó el sistema de rutas para permitir acceso a vendedores a estos módulos
- **Archivos afectados:** `frontend_saas/src/routes/AppRouter.tsx`

#### 2. Filtros de fechas imprecisos
- **Problema:** Los filtros de fechas en reportes incluían ventas fuera del rango seleccionado
- **Causa:** Uso incorrecto de comparaciones de fechas en JavaScript
- **Solución:** Se implementó dayjs con plugins `isSameOrAfter` e `isSameOrBefore` para filtrado exacto
- **Archivos afectados:** `frontend_saas/src/pages/ReportesPage.tsx`

#### 3. Errores de compilación ESLint
- **Problema:** Errores de imports no usados y orden incorrecto de configuraciones
- **Causa:** Imports innecesarios y configuraciones de dayjs/Chart.js en el lugar incorrecto
- **Solución:** Se eliminaron imports no usados y se reordenaron las configuraciones
- **Archivos afectados:** `frontend_saas/src/components/MainLayout.tsx`, `frontend_saas/src/pages/ReportesPage.tsx`

#### 4. Gráficos de reportes
- **Problema:** Necesidad de visualizaciones gráficas para reportes
- **Solución:** Se implementó Chart.js con gráficos de barras y torta
- **Dependencias agregadas:** chart.js, react-chartjs-2

### Problemas históricos y soluciones:

[AQUÍ INSERTAR SECCIÓN DE PROBLEMAS HISTÓRICOS]

---

## 12. Despliegue y uso

### Instrucciones de despliegue actualizadas:

#### Backend (Railway/Render)
1. Conectar repositorio de GitHub
2. Configurar variables de entorno
3. Ejecutar migraciones SQL
4. Desplegar automáticamente

#### Frontend (Vercel)
1. Conectar repositorio de GitHub
2. Configurar variables de entorno
3. Build automático con `npm run build`
4. Despliegue automático

### Nuevas consideraciones:
- **Dependencias:** Asegurar que chart.js y react-chartjs-2 estén instaladas
- **Variables de entorno:** Configurar URLs del backend correctamente
- **Build:** Verificar que no haya errores de ESLint antes del despliegue

[AQUÍ INSERTAR CAPTURAS DE DESPLIEGUE]

---

## 13. Diagramas y capturas

### Nuevas capturas de pantalla:
- **Reportes con gráficos:** Vista de gráficos de barras y torta
- **Filtros de fechas:** Interfaz de selección de rangos temporales
- **Sistema de roles:** Diferentes vistas según el rol del usuario

[AQUÍ INSERTAR CAPTURAS ACTUALIZADAS]

---

## 14. Conclusiones y recomendaciones

### Logros alcanzados:
- Sistema completo y funcional en modo offline y SaaS
- Aislamiento total de datos entre empresas
- Experiencia de usuario moderna y responsiva
- **Nuevo:** Reportes avanzados con visualizaciones gráficas
- **Nuevo:** Sistema de roles y permisos granular
- **Nuevo:** Filtros de fechas precisos y eficientes

### Recomendaciones para futuras mejoras:
- Implementar notificaciones en tiempo real
- Agregar más tipos de gráficos y reportes
- Optimizar el rendimiento para grandes volúmenes de datos
- Implementar auditoría de cambios
- Agregar funcionalidades de exportación en más formatos

---

## 15. Agradecimientos

Este proyecto es el resultado de muchas horas de trabajo, aprendizaje y colaboración. Gracias a quienes aportaron ideas, probaron y confiaron en la visión de un sistema robusto, flexible y preparado para el mundo offline y SaaS multiempresa.

**Agradecimientos especiales por las nuevas funcionalidades:**
- Comunidad de Chart.js por las librerías de visualización
- Desarrolladores de dayjs por la librería de manejo de fechas
- Usuarios que probaron y reportaron problemas de permisos

---

## 16. Anexos

### Anexo A: Nuevos endpoints de reportes
```
GET /ventas/agrupadas-por-dia?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD
GET /ventas/agrupadas-por-categoria?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD
```

### Anexo B: Estructura de roles y permisos
```
admin: acceso total
vendedor: dashboard, inventario, ventas, clientes, reportes
inventario: dashboard, inventario
```

### Anexo C: Dependencias nuevas
```
chart.js: ^4.4.0
react-chartjs-2: ^5.2.0
dayjs: ^1.11.10
```

[AQUÍ INSERTAR OTROS ANEXOS RELEVANTES]

---

**Versión del documento: 2.0.0**  
**Última actualización: [Fecha actual]**  
**Autor: [Tu Nombre]** 