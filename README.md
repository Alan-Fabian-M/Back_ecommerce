⚙️ Instalación
Clonar el repositorio

    git clone https://github.com/tu_usuario/tu_proyecto.git
    cd tu_proyecto

Crear entorno virtual e instalar dependencias

    python -m venv venv
    source venv/bin/activate  # en Windows: venv\Scripts\activate
    pip install -r requirements.txt

Configurar la base de datos


Edita el archivo app/config.py o tus variables de entorno con tu cadena de conexión PostgreSQL:

    SQLALCHEMY_DATABASE_URI = "postgresql://usuario:contraseña@localhost:5432/nombre_basedatos"


Inicializar la base de datos con datos de prueba

    python seeders/seed.py


▶️ Ejecutar el servidor

    python run.py

Esto levantará el servidor en http://localhost:5000.

🌐 CORS habilitado
Este backend permite solicitudes desde tu frontend Angular (por defecto http://localhost:4200). Si vas a desplegar, recuerda editar esto en app/__init__.py.

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

🔐 Autenticación con JWT

* El login devuelve un token JWT.
* El token se debe incluir en el encabezado de las peticiones:
    
        Authorization: Bearer <tu_token>

Para verificar el rol o la identidad del usuario autenticado, hay una función auxiliar decode_token() que devuelve el token y el rol.

🧪 Endpoints disponibles:

Método	URL	                                Descripción
GET	/api/usuarios	                        Obtener todos los usuarios
GET	/api/usuarios/<int:id>	                Obtener usuario por ID
GET	/api/usuarios/<string:nombre>	        Buscar usuarios por nombre
GET	/api/usuarios/rol/<string:nombre_rol>	Buscar usuarios por nombre del rol
POST	/api/usuarios	                    Crear nuevo usuario
PUT	/api/usuarios/<int:id>	                Actualizar usuario por ID
DELETE	/api/usuarios/<int:id>	            Eliminar usuario por ID


🧪 Endpoints disponibles: Roles

Método	URL	                    Descripción
GET	/api/roles	                Obtener todos los roles
GET	/api/roles/<int:id>	        Obtener rol por ID
GET	/api/roles/<string:nombre>	Buscar roles por nombre
POST	/api/roles	            Crear nuevo rol
PUT	/api/roles/<int:id>	        Actualizar rol por ID
DELETE	/api/roles/<int:id>	    Eliminar rol por ID


🧪 Endpoints disponibles: RolPermiso
Método	URL	                                                Descripción
GET	/api/roles_permisos	                                    Obtener todos los roles-permisos
GET	/api/roles_permisos/<int:rol_id>/<int:permiso_id>	    Obtener un rol-permiso por rol_id y permiso_id
POST	/api/roles_permisos	                                Crear un nuevo rol-permiso
PUT	/api/roles_permisos/<int:rol_id>/<int:permiso_id>	    Actualizar un rol-permiso existente
DELETE	/api/roles_permisos/<int:rol_id>/<int:permiso_id>	Eliminar un rol-permiso

🛒 Endpoints disponibles: Producto
Método	URL	                            Descripción
GET	/api/productos	                    Obtener todos los productos
GET	/api/productos/<int:id>	            Obtener un producto específico por ID
POST	/api/productos	                Crear un nuevo producto
PUT	/api/productos/<int:id>	            Actualizar un producto existente
DELETE	/api/productos/<int:id>	        Eliminar un producto


🔑 Endpoints disponibles: Permiso
Método	URL	                        Descripción
GET	/api/permisos	                Obtener todos los permisos
GET	/api/permisos/<int:id>	        Obtener un permiso específico por ID
POST	/api/permisos	            Crear un nuevo permiso
PUT	/api/permisos/<int:id>	        Actualizar un permiso existente
DELETE	/api/permisos/<int:id>	    Eliminar un permiso


🏃‍♂️ Endpoints disponibles: Movimiento
Método	URL	                            Descripción
GET	/api/movimientos	                Obtener todos los movimientos
GET	/api/movimientos/<int:id>	        Obtener un movimiento específico por ID
POST	/api/movimientos	            Crear un nuevo movimiento
PUT	/api/movimientos/<int:id>	        Actualizar un movimiento existente
DELETE	/api/movimientos/<int:id>	    Eliminar un movimiento



🔖 Endpoints disponibles: Marca
Método	URL	                        Descripción
GET	/api/marcas	                    Obtener todas las marcas
GET	/api/marcas/<int:id>	        Obtener una marca específica por ID
GET	/api/marcas/<string:nombre>	    Buscar marcas por nombre (búsqueda parcial, no sensible a mayúsculas)
POST	/api/marcas	                Crear una nueva marca
PUT	/api/marcas/<int:id>	        Actualizar una marca existente
DELETE	/api/marcas/<int:id>	    Eliminar una marca


🔖 Endpoints disponibles: Categoria
Método	URL	                        Descripción
GET	/api/categorias	                Obtener todas las categorías
GET	/api/categorias/<int:id>	    Obtener una categoría específica por ID
POST	/api/categorias	            Crear una nueva categoría
PUT	/api/categorias/<int:id>	    Actualizar una categoría existente
DELETE	/api/categorias/<int:id>	Eliminar una categoría



🔖 Endpoints disponibles: Bitacora
Método	URL	                        Descripción
GET	/api/bitacoras	                Obtener todas las bitácoras
GET	/api/bitacoras/<int:id>	        Obtener una bitácora específica por ID
POST	/api/bitacoras	            Crear una nueva bitácora
PUT	/api/bitacoras/<int:id>	        Actualizar una bitácora existente
DELETE	/api/bitacoras/<int:id>	    Eliminar una bitácora