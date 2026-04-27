%% Diagrama de despliegue EXTENSO y EXPLICADO: SaaS + Offline + Administración + Seguridad

flowchart TD
  %% USUARIOS Y DISPOSITIVOS
  subgraph Usuarios
    PCWeb["PC Usuario (Navegador Web)"]
    Movil["Dispositivo Móvil (Web/App)"]
    PCOffline["PC Usuario (App Offline)"]
    Admin["Administrador (Panel Admin)"]
  end

  %% SEGURIDAD Y ACCESO
  subgraph Seguridad
    FW["Firewall/Proxy"]
    LB["Balanceador de Carga"]
  end

  %% INFRAESTRUCTURA SAAS
  subgraph SaaS["Infraestructura SaaS (Cloud)"]
    CDN["CDN (Recursos Estáticos)"]
    FE["Frontend React (Render/Netlify)"]
    API["API Backend FastAPI (Railway/Render)"]
    Auth["Servicio de Autenticación (JWT, OAuth)"]
    DB["Base de Datos PostgreSQL (Railway)"]
    Storage["Almacenamiento de Imágenes/Archivos (Cloud)"]
    Email["Servicio de Email (SMTP/SendGrid)"]
    Backup["Backup Automático y Manual"]
    Monitor["Monitorización y Logs (Cloud)"]
    Jobs["Tareas Programadas (CRON, Workers)"]
    APIExt["APIs Externas (Facturación, SMS, etc.)"]
  end

  %% INFRAESTRUCTURA LOCAL
  subgraph Local["Infraestructura Local (Offline)"]
    LocalApp["Aplicación Local (Python Tkinter)"]
    LocalDB["Base de Datos Local (SQLite)"]
    LocalBackup["Respaldo Local (Archivos .json/.csv)"]
    LocalUser["Usuario Local"]
  end

  %% FLUJOS DE USUARIO SAAS
  PCWeb -- "1. Solicita página" --> CDN
  Movil -- "1. Solicita página/app" --> CDN
  CDN -- "2. Entrega recursos estáticos" --> PCWeb
  CDN -- "2. Entrega recursos estáticos" --> Movil
  PCWeb -- "3. Interacción (login, CRUD, reportes, etc.)" --> FE
  Movil -- "3. Interacción (login, CRUD, reportes, etc.)" --> FE
  FE -- "4. Solicitudes API (REST)" --> FW
  FW -- "5. Filtrado y seguridad" --> LB
  LB -- "6. Balanceo de carga" --> API
  API -- "7. Autenticación y autorización" --> Auth
  API -- "8. Acceso/Modificación de datos" --> DB
  API -- "9. Subida/descarga de imágenes" --> Storage
  API -- "10. Envía emails (notificaciones, recuperación)" --> Email
  API -- "11. Registro de logs y monitoreo" --> Monitor
  API -- "12. Backups programados/manuales" --> Backup
  API -- "13. Llamadas a APIs externas" --> APIExt
  Jobs -- "14. Tareas programadas (reportes, limpieza, etc.)" --> API

  %% ADMINISTRACIÓN
  Admin -- "1. Acceso seguro (2FA, VPN)" --> FW
  Admin -- "2. Panel de administración" --> FE
  FE -- "3. Acceso a logs, backups, gestión de usuarios" --> API

  %% FLUJOS OFFLINE
  LocalUser -- "1. Usa la app local" --> LocalApp
  LocalApp -- "2. Acceso/Modificación de datos" --> LocalDB
  LocalApp -- "3. Respaldo manual/automático" --> LocalBackup

  %% SINCRONIZACIÓN Y MIGRACIÓN
  LocalApp -. "Sincronización eventual (cuando hay internet)" .-> API
  LocalBackup -. "Migración/Importación de datos" .-> DB

  %% NOTAS Y DESCRIPCIONES
  classDef cloud fill:#e3f2fd,stroke:#1976d2,stroke-width:2px;
  classDef local fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
  classDef seguridad fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
  class CDN,FE,API,DB,Storage,Auth,Email,Backup,Monitor,Jobs,APIExt cloud;
  class LocalApp,LocalDB,LocalBackup,LocalUser local;
  class FW,LB seguridad;

  %% EXPLICACIONES
  note right of PCWeb
    "El usuario accede al sistema SaaS desde cualquier navegador moderno.\nPuede operar desde PC o móvil."
  end
  note right of PCOffline
    "El usuario puede trabajar sin conexión usando la app local.\nLos datos se guardan en una base local y pueden sincronizarse luego."
  end
  note right of FW
    "El firewall y el balanceador de carga protegen y distribuyen el tráfico entrante.\nSolo permiten tráfico seguro (HTTPS, VPN, 2FA para admins)."
  end
  note right of API
    "El backend expone endpoints REST protegidos con JWT/OAuth.\nGestiona usuarios, roles, empresas, inventario, ventas, reportes, etc."
  end
  note right of DB
    "Base de datos multi-tenant, separa datos por empresa.\nRespaldos automáticos y restauración en caso de fallo.\nAcceso restringido solo desde la API."
  end
  note right of LocalApp
    "La app local replica funcionalidades básicas:\ngestión de inventario, ventas, reportes y respaldo local.\nPermite exportar/importar datos."
  end
  note right of Jobs
    "Tareas programadas: generación de reportes, limpieza de datos, backups, notificaciones automáticas, etc."
  end
  note right of APIExt
    "Integración con servicios externos: facturación electrónica, SMS, APIs de terceros, etc."
  end

---

### Explicación de cada parte (ampliada)

- **Usuarios y Dispositivos:**  
  - PC Usuario (Navegador Web): Acceso desde cualquier lugar, interfaz moderna.
  - Dispositivo Móvil: Acceso móvil responsivo o app dedicada.
  - PC Usuario (App Offline): Uso sin conexión, ideal para zonas sin internet.
  - Administrador: Acceso a panel de gestión, logs, backups, usuarios, etc.

- **Seguridad y Acceso:**  
  - Firewall/Proxy: Filtra tráfico, protege de ataques, permite solo conexiones seguras.
  - Balanceador de Carga: Distribuye solicitudes entre instancias del backend.

- **Infraestructura SaaS (Cloud):**  
  - CDN: Entrega rápida de archivos estáticos (JS, CSS, imágenes).
  - Frontend React: Interfaz de usuario, desplegada en la nube.
  - API Backend FastAPI: Lógica de negocio, autenticación, gestión de datos.
  - Servicio de Autenticación: Login, roles, permisos, JWT, OAuth.
  - Base de Datos PostgreSQL: Multi-tenant, datos separados por empresa.
  - Almacenamiento de Imágenes/Archivos: Logos, fotos, documentos.
  - Servicio de Email: Notificaciones, recuperación de contraseña.
  - Backup Automático y Manual: Copias de seguridad programadas y bajo demanda.
  - Monitorización y Logs: Seguimiento de errores, auditoría, alertas.
  - Tareas Programadas: Reportes automáticos, limpieza, backups, etc.
  - APIs Externas: Integración con servicios de facturación, SMS, etc.

- **Infraestructura Local (Offline):**  
  - Aplicación Local: Permite trabajar sin conexión, interfaz en Tkinter.
  - Base de Datos Local: Guarda datos en SQLite.
  - Respaldo Local: Exportar/importar datos, migración a SaaS.
  - Usuario Local: Opera la app en modo offline.

- **Sincronización y Migración:**  
  - Cuando hay internet, la app local puede sincronizar datos con el SaaS.
  - Se pueden migrar datos de la versión offline a la online y viceversa.
  - Respaldo local permite restaurar información ante fallos.

- **Administración:**
  - Acceso seguro para administradores (VPN, 2FA).
  - Panel de administración para gestión avanzada.
  - Acceso a logs, backups, usuarios, configuración avanzada.

- **Notas:**
  - El sistema está diseñado para alta disponibilidad, seguridad y escalabilidad.
  - La arquitectura permite trabajar tanto en la nube como en modo offline.
  - La integración con servicios externos amplía las capacidades del sistema. 