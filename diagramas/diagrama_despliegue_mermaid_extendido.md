---
config:
  layout: dagre
---
flowchart TD
  %% USUARIOS Y DISPOSITIVOS
  subgraph Usuarios["Usuarios y Administradores"]
    UsuarioWeb["Usuario Web (Navegador)"]
    UsuarioMovil["Usuario Móvil (Web/App)"]
    UsuarioOffline["Usuario Offline (Tkinter)"]
    Admin["Administrador (Panel Admin)"]
  end

  %% SEGURIDAD Y ACCESO
  subgraph Seguridad["Seguridad y Acceso"]
    Firewall["Firewall/Proxy"]
    Balanceador["Balanceador de Carga"]
  end

  %% INFRAESTRUCTURA SAAS
  subgraph SaaS["Infraestructura SaaS (Cloud)"]
    CDN["CDN (Recursos Estáticos)"]
    Frontend["Frontend React (Render/Netlify)"]
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
    AppOffline["App Tkinter (Offline/Online)"]
    DBLocal["Base de datos SQLite (Local)"]
    LocalBackup["Respaldo Local (Archivos .json/.csv)"]
  end

  %% FLUJOS DE USUARIO SAAS
  UsuarioWeb -- "Solicita página" --> CDN
  UsuarioMovil -- "Solicita página/app" --> CDN
  CDN -- "Entrega recursos estáticos" --> UsuarioWeb
  CDN -- "Entrega recursos estáticos" --> UsuarioMovil
  UsuarioWeb -- "Interacción (login, CRUD, reportes, etc.)" --> Frontend
  UsuarioMovil -- "Interacción (login, CRUD, reportes, etc.)" --> Frontend
  Frontend -- "Solicitudes API (REST)" --> Firewall
  Firewall -- "Filtrado y seguridad" --> Balanceador
  Balanceador -- "Balanceo de carga" --> API
  API -- "Autenticación y autorización" --> Auth
  API -- "Acceso/Modificación de datos" --> DB
  API -- "Subida/descarga de imágenes" --> Storage
  API -- "Envía emails (notificaciones, recuperación)" --> Email
  API -- "Registro de logs y monitoreo" --> Monitor
  API -- "Backups programados/manuales" --> Backup
  API -- "Llamadas a APIs externas" --> APIExt
  Jobs -- "Tareas programadas (reportes, limpieza, etc.)" --> API

  %% ADMINISTRACIÓN
  Admin -- "Acceso seguro (2FA, VPN)" --> Firewall
  Admin -- "Panel de administración" --> Frontend
  Frontend -- "Acceso a logs, backups, gestión de usuarios" --> API

  %% FLUJOS OFFLINE
  UsuarioOffline -- "Usa la app local" --> AppOffline
  AppOffline -- "Acceso/Modificación de datos" --> DBLocal
  AppOffline -- "Respaldo manual/automático" --> LocalBackup

  %% SINCRONIZACIÓN Y MIGRACIÓN
  AppOffline -. "Sincronización eventual (cuando hay internet)" .-> API
  LocalBackup -. "Migración/Importación de datos" .-> DB

  %% ESTILOS
  classDef cloud fill:#e3f2fd,stroke:#1976d2,stroke-width:2px;
  classDef local fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
  classDef seguridad fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
  class CDN,Frontend,API,DB,Storage,Auth,Email,Backup,Monitor,Jobs,APIExt cloud;
  class AppOffline,DBLocal,LocalBackup local;
  class Firewall,Balanceador seguridad;

%% NOTAS EXPLICATIVAS
%% Usuarios acceden desde web o móvil al frontend, que se sirve por CDN para mayor velocidad.
%% El tráfico pasa por firewall y balanceador antes de llegar al backend (API FastAPI).
%% El backend gestiona autenticación, acceso a base de datos, almacenamiento, emails, backups y monitorización.
%% Administradores acceden a paneles avanzados y logs.
%% En modo offline, la app local permite trabajar y sincronizar datos cuando hay internet.
%% Respaldo local permite migrar o restaurar información. 