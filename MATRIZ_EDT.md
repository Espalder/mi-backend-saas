# Matriz de Trazabilidad según la Estructura de Desglose del Trabajo (EDT)

Esta matriz relaciona cada elemento de la EDT con los entregables y módulos/componentes del sistema donde se evidencia su cumplimiento.

---

| Código EDT | Descripción EDT                                 | Entregable/Módulo relacionado                        | Estado   |
|------------|-------------------------------------------------|------------------------------------------------------|----------|
| 1.1        | Acta de constitución                            | Informe Final, Documentación                         | Cumplido |
| 1.2        | Planificación del proyecto                      | Informe Final, Cronograma, Matriz RACI               | Cumplido |
| 1.3        | Seguimiento y control                           | Informe Final, Documentación, Reuniones              | Cumplido |
| 2.1.1      | Backend (API de productos)                      | backend_saas/app/api/productos.py                    | Cumplido |
| 2.1.2      | Frontend (pantalla de productos)                | frontend_saas/src/pages/ProductosPage.tsx            | Cumplido |
| 2.1.3      | Pruebas funcionales (Inventario)                | Pruebas, Documentación, Reportes de pruebas          | Cumplido |
| 2.2.1      | Backend (registro de ventas, control de stock)  | backend_saas/app/api/ventas.py                       | Cumplido |
| 2.2.2      | Frontend (facturación)                          | frontend_saas/src/pages/VentasPage.tsx               | Cumplido |
| 2.2.3      | Reporte PDF (Ventas)                            | Reportes PDF, frontend_saas/src/pages/ReportesPage.tsx | Cumplido |
| 2.3.1      | Consultas analíticas                            | backend_saas/app/api/reportes.py                     | Cumplido |
| 2.3.2      | Dashboards interactivos                         | frontend_saas/src/pages/ReportesPage.tsx             | Cumplido |
| 2.3.3      | Exportación a PDF (Reportes)                    | Reportes PDF, frontend_saas/src/pages/ReportesPage.tsx | Cumplido |
| 3.1        | Manual de usuario                               | DOCUMENTACION_COMPLETA_SISTEMA_SAAS.pdf, README.md   | Cumplido |
| 3.2        | Manual técnico                                  | DOCUMENTACION_COMPLETA_SISTEMA_SAAS.pdf              | Cumplido |
| 3.3        | Talleres de formación                           | Documentación, Manuales, Registros de capacitación   | Cumplido |
| 4.1        | Pruebas de rendimiento (JMeter)                  | Reportes de pruebas, Documentación                   | Cumplido |
| 4.2        | Implementación en empresas piloto                | Informe Final, Documentación, Registros de despliegue| Cumplido |
| 4.3        | Encuestas de satisfacción                        | Informe Final, Resultados de encuestas               | Cumplido |

---

**Leyenda:**
- **EDT**: Estructura de Desglose del Trabajo
- **Estado**: Cumplido / Parcial / Pendiente 