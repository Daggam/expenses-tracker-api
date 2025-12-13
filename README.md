ESTRUCTURA DE CARPETAS:

📂 mi_proyecto_fastapi
├── 📂 app
│   ├── 📂 core          # Configuraciones generales
│   ├── 📂 models        # Tus datos (Schemas Pydantic / Entidades)
│   ├── 📂 repositories  # Acceso a DB (La capa de Persistencia)
│   ├── 📂 services      # Lógica de Negocio (La capa de Servicio)
│   ├── 📂 routers       # Endpoints (La capa de Presentación/Web)
│   └── main.py          # Punto de entrada

# TODO: 
* Crear un deps.py en api para hacer obtener el usuario actual de la sesión (get_current_user)

* Terminar con los endpoints de expenses:
    * Eliminar Expense
    * Actualizar Expense

* Comenzar con los endpoints de usuario:
    * Crear usuario (Login) [Utilización de JWT]
    * Crear Token ("Iniciar sesión")