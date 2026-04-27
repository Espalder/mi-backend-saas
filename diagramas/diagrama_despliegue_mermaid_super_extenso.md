---
config:
  layout: dagre
---
flowchart LR
  %% USUARIOS Y ADMINISTRADORES
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
    WAF["Web Application Firewall"]
    VPN["VPN Empresarial"]
  end

  %% INFRAESTRUCTURA SAAS
  subgraph SaaS["Infraestructura SaaS (Cloud)"]
    CDN["CDN (Recursos Estáticos)"]
    Frontend["Frontend React (Render/Netlify)"]
    API["API Backend FastAPI (Railway/Render)"]
    Auth["Servicio de Autenticación (JWT, OAuth, 2FA)"]
    DB["Base de Datos PostgreSQL (Railway)"]
    Storage["Almacenamiento de Imágenes/Archivos (Cloud)"]
    Email["Servicio de Email (SMTP/SendGrid)"]
    Backup["Backup Automático y Manual"]
    Monitor["Monitorización y Logs (Cloud)"]
    Jobs["Tareas Programadas (CRON, Workers)"]
    APIExt["APIs Externas (Facturación, SMS, etc.)"]
    Cache["Cache Redis/Memcached"]
    Metrics["Métricas y Alertas"]
  end

  %% INFRAESTRUCTURA LOCAL
  subgraph Local["Infraestructura Local (Offline)"]
    AppOffline["App Tkinter (Offline/Online)"]
    DBLocal["Base de datos SQLite (Local)"]
    LocalBackup["Respaldo Local (Archivos .json/.csv)"]
    LocalPrinter["Impresora Local"]
    LocalScanner["Escáner Local"]
  end

  %% FLUJOS DE USUARIO SAAS
  UsuarioWeb -- "Solicita página" --> CDN
  UsuarioMovil -- "Solicita página/app" --> CDN
  CDN -- "Entrega recursos estáticos" --> UsuarioWeb
  CDN -- "Entrega recursos estáticos" --> UsuarioMovil
  UsuarioWeb -- "Interacción (login, CRUD, reportes, etc.)" --> Frontend
  UsuarioMovil -- "Interacción (login, CRUD, reportes, etc.)" --> Frontend
  Frontend -- "Solicitudes API (REST)" --> WAF
  WAF -- "Filtrado de amenazas" --> Firewall
  Firewall -- "Filtrado y seguridad" --> Balanceador
  Balanceador -- "Balanceo de carga" --> API
  API -- "Autenticación y autorización" --> Auth
  API -- "Acceso/Modificación de datos" --> DB
  API -- "Subida/descarga de imágenes" --> Storage
  API -- "Envía emails (notificaciones, recuperación)" --> Email
  API -- "Registro de logs y monitoreo" --> Monitor
  API -- "Backups programados/manuales" --> Backup
  API -- "Llamadas a APIs externas" --> APIExt
  API -- "Uso de caché" --> Cache
  API -- "Métricas y alertas" --> Metrics
  Jobs -- "Tareas programadas (reportes, limpieza, etc.)" --> API

  %% ADMINISTRACIÓN
  Admin -- "Acceso seguro (VPN, 2FA)" --> VPN
  VPN -- "Acceso restringido" --> WAF
  Admin -- "Panel de administración" --> Frontend
  Frontend -- "Acceso a logs, backups, gestión de usuarios" --> API

  %% FLUJOS OFFLINE
  UsuarioOffline -- "Usa la app local" --> AppOffline
  AppOffline -- "Acceso/Modificación de datos" --> DBLocal
  AppOffline -- "Respaldo manual/automático" --> LocalBackup
  AppOffline -- "Impresión de tickets" --> LocalPrinter
  AppOffline -- "Escaneo de productos" --> LocalScanner

  %% SINCRONIZACIÓN Y MIGRACIÓN
  AppOffline -. "Sincronización eventual (cuando hay internet)" .-> API
  LocalBackup -. "Migración/Importación de datos" .-> DB

  %% ESTILOS
  classDef cloud fill:#e3f2fd,stroke:#1976d2,stroke-width:2px;
  classDef local fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
  classDef seguridad fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
  classDef note fill:#fffbe6,stroke:#bfa500,stroke-width:1px;
  class CDN,Frontend,API,DB,Storage,Auth,Email,Backup,Monitor,Jobs,APIExt,Cache,Metrics cloud;
  class AppOffline,DBLocal,LocalBackup,LocalPrinter,LocalScanner local;
  class Firewall,Balanceador,WAF,VPN seguridad;

  %% NOTAS FUNCIONALES
  NotaUsuarios["Usuarios acceden desde web o móvil al frontend, servido por CDN para mayor velocidad."]:::note
  NotaSeguridad["El tráfico pasa por WAF y firewall antes de llegar al backend."]:::note
  NotaBackend["El backend gestiona autenticación, acceso a base de datos, almacenamiento, emails, backups y monitorización."]:::note
  NotaAdmin["Administradores acceden a paneles avanzados y logs mediante VPN y 2FA."]:::note
  NotaOffline["En modo offline, la app local permite trabajar y sincronizar datos cuando hay internet."]:::note
  NotaBackup["Respaldo local permite migrar o restaurar información."]:::note

  UsuarioWeb -.-> NotaUsuarios
  UsuarioMovil -.-> NotaUsuarios
  WAF -.-> NotaSeguridad
  Firewall -.-> NotaSeguridad
  API -.-> NotaBackend
  DB -.-> NotaBackend
  Admin -.-> NotaAdmin
  VPN -.-> NotaAdmin
  AppOffline -.-> NotaOffline
  DBLocal -.-> NotaOffline
  LocalBackup -.-> NotaBackup
  DB -.-> NotaBackup 