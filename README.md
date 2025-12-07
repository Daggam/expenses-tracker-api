ESTRUCTURA DE CARPETAS:

📂 mi_proyecto_fastapi
├── 📂 app
│   ├── 📂 core          # Configuraciones generales
│   ├── 📂 models        # Tus datos (Schemas Pydantic / Entidades)
│   ├── 📂 repositories  # Acceso a DB (La capa de Persistencia)
│   ├── 📂 services      # Lógica de Negocio (La capa de Servicio)
│   ├── 📂 routers       # Endpoints (La capa de Presentación/Web)
│   └── main.py          # Punto de entrada