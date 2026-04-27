# Sistema de Gestión Empresarial (Offline y SaaS Multiempresa)

## Descripción
Este proyecto es un sistema integral de gestión empresarial, diseñado para funcionar tanto en modo offline (aplicación de escritorio con Tkinter y SQLite/MySQL) como en la nube bajo el modelo SaaS multiempresa (FastAPI + React). Permite gestionar empresas, usuarios, productos, clientes, ventas, reportes y más, con aislamiento total de datos entre empresas.

## Características principales
- **Modo Offline/Online:** Trabajo local con sincronización automática a la nube.
- **SaaS Multiempresa:** Cada empresa tiene su propio universo de datos.
- **Autenticación JWT y roles:** Seguridad robusta y control de acceso granular.
- **Frontend moderno:** React + Material UI, responsive y con excelente UX.
- **Backend robusto:** FastAPI, SQLAlchemy, Pydantic, PostgreSQL/MySQL.
- **Control de versiones:** Git y GitHub, con buenas prácticas y trazabilidad total.
- **Reportes avanzados:** Gráficos de barras y torta con filtros por fechas.
- **Sistema de roles:** Admin, vendedor e inventario con permisos específicos.

## Estructura del proyecto
```
A1-A2/
  ├─ backend_saas/         # Backend FastAPI (SaaS)
  ├─ frontend_saas/        # Frontend React (SaaS)
  ├─ sistema_gestion_mejorado_modulos/  # Sistema offline/online (Tkinter)
  ├─ backup_sistema_actual/ # Respaldos y versiones previas
  ├─ images/               # Recursos gráficos
  ├─ scripts SQL           # Migraciones y alteraciones de BD
  ├─ keep_alive.py         # Script de keep-alive para backend
  └─ otros archivos utilitarios
```

## Instalación y ejecución

### Requisitos generales
- Python 3.10+
- Node.js 18+
- npm 9+
- MySQL o PostgreSQL (según entorno)
- Git

### Backend (FastAPI)
1. Instala dependencias:
   ```sh
   cd backend_saas
   pip install -r requirements.txt
   ```
2. Configura variables de entorno en `.env` o `config.py`.
3. Ejecuta migraciones SQL si es necesario.
4. Inicia el servidor:
   ```sh
   uvicorn main:app --reload
   ```

### Frontend (React)
1. Instala dependencias:
   ```sh
   cd frontend_saas
   npm install
   ```
2. Configura la URL del backend en las variables de entorno.
3. Ejecuta en desarrollo:
   ```sh
   npm start
   ```
4. Para producción:
   ```sh
   npm run build
   ```

### Sistema Offline (Tkinter)
1. Instala dependencias:
   ```sh
   cd sistema_gestion_mejorado_modulos
   pip install -r requirements.txt
   ```
2. Configura credenciales de MySQL en `DB_CONFIG`.
3. Ejecuta:
   ```sh
   python main_offline.py
   ```

## Dependencias principales
- **Backend:** fastapi, uvicorn, sqlalchemy, pydantic, python-jose, passlib[bcrypt], mysql-connector-python
- **Frontend:** react, @mui/material, @mui/icons-material, axios, react-router-dom, chart.js, react-chartjs-2, dayjs
- **Offline:** tkinter, mysql-connector-python, sqlite3, passlib[bcrypt]

## Sistema de Roles y Permisos

### Roles disponibles:
- **admin:** Acceso total a todas las funcionalidades
- **vendedor:** Acceso a Dashboard, Inventario, Ventas, Clientes y Reportes
- **inventario:** Acceso solo a Dashboard e Inventario

### Permisos por módulo:
- **Dashboard:** Todos los roles
- **Inventario:** Todos los roles
- **Ventas:** admin y vendedor
- **Clientes:** admin y vendedor
- **Reportes:** admin y vendedor
- **Usuarios:** Solo admin
- **Empresa:** Solo admin

## Funcionalidades de Reportes

### Características implementadas:
- **Filtros por fechas:** Selección de rango personalizado (día, semana, mes, año)
- **Vista de tabla:** Lista detallada de ventas con filtrado exacto
- **Gráfico de barras:** Ventas por día con datos agrupados
- **Gráfico de torta:** Ventas por categoría de productos
- **Exportación PDF:** Generación de reportes en formato PDF
- **Filtrado preciso:** Uso de dayjs para filtrado exacto de fechas

### Endpoints de reportes agregados:
- `GET /ventas/agrupadas-por-dia`: Ventas agrupadas por día
- `GET /ventas/agrupadas-por-categoria`: Ventas agrupadas por categoría

## Dependencias y validación de formularios

### Backend (FastAPI)
- **Pydantic**: Usado para la validación de datos en todos los endpoints y modelos. Permite definir esquemas y validar automáticamente los datos recibidos en los formularios de creación/edición de productos, clientes, ventas, etc.
- **FastAPI**: Permite recibir y validar datos de formularios (JSON) de manera automática.

### Frontend (React)
- **React**: Los formularios (registro, productos, clientes, ventas, etc.) se implementan como formularios controlados usando el estado de React.
- **Material UI (MUI)**: Se utiliza para los componentes visuales de los formularios (inputs, selects, diálogos, etc.).
- **Chart.js y react-chartjs-2**: Para la generación de gráficos en reportes
- **dayjs**: Para el manejo de fechas y filtros temporales
- **Validación**: En esta versión del proyecto, la validación de formularios se realiza manualmente en el código React, verificando campos obligatorios, formatos y restricciones antes de enviar los datos al backend. No se utilizan librerías externas como `formik` o `yup`.

### Sistema Offline (Tkinter)
- **Tkinter**: Usado para crear los formularios gráficos en la aplicación de escritorio (campos de entrada, botones, etc.).
- **Validación**: Se realiza directamente en el código Python, comprobando los datos antes de guardarlos en la base de datos. No se usan librerías externas de validación.

---

Esta sección detalla con precisión las dependencias y métodos usados para la gestión y validación de formularios en cada parte del sistema.

## Despliegue
- **Backend:** Render, Railway, o VPS propio
- **Frontend:** Vercel, Netlify, o servidor propio
- **Variables de entorno:** `.env` para backend y frontend

## Pruebas y buenas prácticas
- Pruebas multiempresa: aislamiento total de datos
- Seguridad: JWT, roles, validación de empresa
- Control de versiones: commits atómicos, ramas separadas, pull requests, push inmediato tras cambios clave
- Backup y restauración: scripts y archivos en `/backup_sistema_actual/`

## Control de versiones y flujo de trabajo

Durante el desarrollo de este sistema se utilizó **Git** para el control de versiones y **GitHub** como repositorio remoto, siguiendo buenas prácticas para asegurar la trazabilidad y calidad del código.

- **Estructura de ramas:**
  - Se trabajó principalmente en la rama `main`, creando ramas temporales para nuevas funcionalidades o correcciones importantes, por ejemplo:
    - `feature/soporte-multiempresa`
    - `bugfix/endpoint-empresas-me`
    - `docs/actualizar-readme`
    - `feature/reportes-graficos`
    - `fix/permisos-vendedor`

- **Convenciones de commits:**
  - Se emplearon mensajes de commit claros y estructurados, siguiendo el formato:
    - `feat: descripción de nueva funcionalidad`
    - `fix: descripción de corrección`
    - `docs: cambios en documentación`
  - Ejemplos reales:
    - `feat: agregar validación de empresa en endpoints de ventas`
    - `fix: corregir error 422 en endpoint /empresas/me`
    - `docs: agregar sección de dependencias en README`
    - `feat(reportes): agregar gráficos de barras y torta con filtros`
    - `fix(reportes): filtrar ventas en tabla solo dentro del rango exacto de fechas`
    - `fix: corregir imports y eliminar useTheme no usado`

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
  - Pruebas y validaciones antes de cada merge.

Este flujo permitió mantener la calidad, seguridad y trazabilidad del proyecto en todo momento.

## Problemas resueltos recientemente

### Correcciones de permisos:
- **Problema:** El rol vendedor no podía acceder a Clientes y Reportes
- **Solución:** Se corrigieron las rutas en el frontend para permitir acceso a vendedores

### Mejoras en reportes:
- **Problema:** Filtros de fechas incluían ventas fuera del rango seleccionado
- **Solución:** Se implementó filtrado exacto usando dayjs con plugins `isSameOrAfter` e `isSameOrBefore`

### Correcciones de compilación:
- **Problema:** Errores de ESLint por imports no usados y orden incorrecto
- **Solución:** Se eliminaron imports innecesarios y se reordenaron las configuraciones de dayjs y Chart.js

## Agradecimientos
Este proyecto es el resultado de muchas horas de trabajo, aprendizaje y colaboración. Gracias a quienes aportaron ideas, probaron y confiaron en la visión de un sistema robusto, flexible y preparado para el mundo offline y SaaS multiempresa.

---

**Para más detalles, consulta el documento `DOCUMENTACION_COMPLETA_SISTEMA_SAAS.md` y su versión PDF.** 