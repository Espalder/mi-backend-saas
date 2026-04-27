# Matriz de Trazabilidad del Proyecto

Esta matriz relaciona los **requerimientos** (funcionales y no funcionales) con los **módulos/componentes** del sistema y los **entregables** donde se evidencia su cumplimiento.

---

| ID Req. | Requerimiento                                      | Módulo/Componente                | Entregable donde se evidencia         | Estado   |
|---------|----------------------------------------------------|-----------------------------------|---------------------------------------|----------|
| RF-01   | Gestión de usuarios y roles                        | Backend (usuarios), Frontend      | backend_saas/, frontend_saas/         | Cumplido |
| RF-02   | Autenticación y autorización (JWT, roles)          | Backend (auth), Frontend (login)  | backend_saas/app/api/auth.py, frontend_saas/src/context/AuthContext.tsx | Cumplido |
| RF-03   | Gestión de productos/inventario                    | Backend (productos), Frontend     | backend_saas/app/api/productos.py, frontend_saas/src/pages/ProductosPage.tsx | Cumplido |
| RF-04   | Gestión de ventas                                  | Backend (ventas), Frontend        | backend_saas/app/api/ventas.py, frontend_saas/src/pages/VentasPage.tsx | Cumplido |
| RF-05   | Gestión de clientes                                | Backend (clientes), Frontend      | backend_saas/app/api/clientes.py, frontend_saas/src/pages/ClientesPage.tsx | Cumplido |
| RF-06   | Reportes y gráficos avanzados                      | Backend (reportes), Frontend      | backend_saas/app/api/reportes.py, frontend_saas/src/pages/ReportesPage.tsx | Cumplido |
| RF-07   | Multiempresa y aislamiento de datos                | Backend (empresas), Base de datos | backend_saas/app/api/empresas.py, SQL/respaldo_railway.sql | Cumplido |
| RF-08   | Sincronización offline/online                      | Sistema offline, Backend          | sistema_gestion_mejorado_modulos/, backend_saas/ | Cumplido |
| RF-09   | Exportación y respaldo de datos                    | Scripts SQL, Backend, Offline     | SQL/respaldo_railway.sql, scripts_utiles/ | Cumplido |
| RF-10   | Interfaz moderna y responsive                      | Frontend (React + MUI)            | frontend_saas/                        | Cumplido |
| RNF-01  | Seguridad de datos (encriptación, validación)      | Backend, Base de datos            | backend_saas/app/models/usuario.py, requirements.txt | Cumplido |
| RNF-02  | Documentación técnica y manual de usuario          | Documentación, README             | DOCUMENTACION_COMPLETA_SISTEMA_SAAS.pdf, README.md | Cumplido |
| RNF-03  | Despliegue automatizado y portable                 | Dockerfile, render.yaml, scripts  | backend_saas/Dockerfile, backend_saas/render.yaml | Cumplido |
| RNF-04  | Compatibilidad multiplataforma                     | Frontend, Backend, Offline        | frontend_saas/, backend_saas/, sistema_gestion_mejorado_modulos/ | Cumplido |

---

**Leyenda:**
- **RF**: Requerimiento funcional
- **RNF**: Requerimiento no funcional
- **Estado**: Cumplido / Parcial / Pendiente 