import mysql.connector
from datetime import datetime
import hashlib
import secrets
from abc import ABC, abstractmethod

# =========================
# Interfaz para conexiones a BD
# =========================
class IConexionBD(ABC):
    @abstractmethod
    def ejecutar(self, query, valores=None):
        pass
    
    @abstractmethod
    def consultar(self, query, valores=None):
        pass
    
    @abstractmethod
    def cerrar(self):
        pass

# =========================
# Clase de conexión a MySQL
# =========================
class ConexionBD(IConexionBD):
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Toor",  # Cambiar por la contraseña de tu MySQL
                database="biblioteca"
            )
            self.cursor = self.conexion.cursor(dictionary=True)
            print("Conexión exitosa a la base de datos.")
        except mysql.connector.Error as e:
            print(f"Error de conexión: {e}")

    def ejecutar(self, query, valores=None):
        try:
            self.cursor.execute(query, valores or ())
            self.conexion.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return False

    def consultar(self, query, valores=None):
        try:
            self.cursor.execute(query, valores or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al consultar: {e}")
            return []

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()

# =========================
# Clase Libro
# =========================
class Libro:
    def __init__(self, titulo, autor, anio, disponible=True, id=None):
        self.__id = id
        self.__titulo = titulo
        self.__autor = autor
        self.__anio = anio
        self.__disponible = disponible

    # Getters y Setters
    def get_id(self):
        return self.__id

    def get_titulo(self):
        return self.__titulo

    def get_autor(self):
        return self.__autor

    def get_anio(self):
        return self.__anio

    def get_disponible(self):
        return self.__disponible

    def set_disponible(self, disponible):
        self.__disponible = disponible

    def set_id(self, id):
        self.__id = id

    def __str__(self):
        estado = "Disponible" if self.__disponible else "Prestado"
        return f"[{self.__id}] {self.__titulo} - {self.__autor} ({self.__anio}) -> {estado}"

# =========================
# Clase Usuario
# =========================
class Usuario:
    def __init__(self, nombre, tipo, password=None, id=None):
        self.__id = id
        self.__nombre = nombre
        self.__tipo = tipo
        self.__password_hash = self.__hash_password(password) if password else None
        self.__salt = secrets.token_hex(16) if password else None

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_tipo(self):
        return self.__tipo

    def set_id(self, id):
        self.__id = id

    def __hash_password(self, password):
        """Encripta la contraseña usando salt y hash"""
        if not password:
            return None
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                 self.__salt.encode('utf-8'), 100000).hex()

    def verificar_password(self, password):
        """Verifica si la contraseña coincide con el hash almacenado"""
        if not self.__password_hash or not self.__salt:
            return False
        test_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                      self.__salt.encode('utf-8'), 100000).hex()
        return secrets.compare_digest(self.__password_hash, test_hash)

    def get_password_hash(self):
        return self.__password_hash

    def get_salt(self):
        return self.__salt

    def __str__(self):
        return f"[{self.__id}] {self.__nombre} - {self.__tipo}"

# =========================
# Clase Prestamo
# =========================
class Prestamo:
    def __init__(self, id_usuario, id_libro, fecha_prestamo=None, fecha_devolucion=None, id=None):
        self.__id = id
        self.__id_usuario = id_usuario
        self.__id_libro = id_libro
        self.__fecha_prestamo = fecha_prestamo or datetime.now().date()
        self.__fecha_devolucion = fecha_devolucion

    def get_id(self):
        return self.__id

    def get_id_usuario(self):
        return self.__id_usuario

    def get_id_libro(self):
        return self.__id_libro

    def get_fecha_prestamo(self):
        return self.__fecha_prestamo

    def get_fecha_devolucion(self):
        return self.__fecha_devolucion

    def set_fecha_devolucion(self, fecha_devolucion):
        self.__fecha_devolucion = fecha_devolucion

    def set_id(self, id):
        self.__id = id

    def __str__(self):
        devuelto = self.__fecha_devolucion if self.__fecha_devolucion else "No devuelto"
        return f"Préstamo ID: {self.__id} | Usuario ID: {self.__id_usuario} | Libro ID: {self.__id_libro} | Prestado: {self.__fecha_prestamo} | Devuelto: {devuelto}"

# =========================
# Servicio de Libros
# =========================
class LibroServicio:
    def __init__(self, conexion):
        self.conexion = conexion

    def registrar_libro(self, libro):
        if not libro.get_titulo() or not libro.get_autor():
            print("Error: Título y autor son obligatorios.")
            return False

        resultado = self.conexion.ejecutar(
            "INSERT INTO libros (titulo, autor, anio, disponible) VALUES (%s, %s, %s, %s)",
            (libro.get_titulo(), libro.get_autor(), libro.get_anio(), libro.get_disponible())
        )
        
        if resultado:
            print("Libro registrado correctamente.")
            return True
        else:
            print("Error al registrar el libro.")
            return False

    def obtener_libro_por_id(self, id_libro):
        libros = self.conexion.consultar("SELECT * FROM libros WHERE id=%s", (id_libro,))
        if libros:
            libro_data = libros[0]
            return Libro(
                libro_data['titulo'], 
                libro_data['autor'], 
                libro_data['anio'], 
                libro_data['disponible'],
                libro_data['id']
            )
        return None

    def listar_libros(self):
        libros = self.conexion.consultar("SELECT * FROM libros")
        for libro_data in libros:
            libro = Libro(
                libro_data['titulo'], 
                libro_data['autor'], 
                libro_data['anio'], 
                libro_data['disponible'],
                libro_data['id']
            )
            print(libro)

    def actualizar_disponibilidad(self, id_libro, disponible):
        return self.conexion.ejecutar(
            "UPDATE libros SET disponible = %s WHERE id = %s", 
            (disponible, id_libro)
        )

# =========================
# Servicio de Usuarios
# =========================
class UsuarioServicio:
    def __init__(self, conexion):
        self.conexion = conexion

    def registrar_usuario(self, usuario):
        if not usuario.get_nombre() or not usuario.get_tipo():
            print("Error: Nombre y tipo son obligatorios.")
            return False

        resultado = self.conexion.ejecutar(
            "INSERT INTO usuarios (nombre, tipo, password_hash, salt) VALUES (%s, %s, %s, %s)",
            (usuario.get_nombre(), usuario.get_tipo(), usuario.get_password_hash(), usuario.get_salt())
        )
        
        if resultado:
            print("Usuario registrado correctamente.")
            return True
        else:
            print("Error al registrar el usuario.")
            return False

    def obtener_usuario_por_id(self, id_usuario):
        usuarios = self.conexion.consultar("SELECT * FROM usuarios WHERE id=%s", (id_usuario,))
        if usuarios:
            usuario_data = usuarios[0]
            usuario = Usuario(
                usuario_data['nombre'], 
                usuario_data['tipo'],
                id=usuario_data['id']
            )
            return usuario
        return None

    def listar_usuarios(self):
        usuarios = self.conexion.consultar("SELECT * FROM usuarios")
        for usuario_data in usuarios:
            usuario = Usuario(
                usuario_data['nombre'], 
                usuario_data['tipo'],
                id=usuario_data['id']
            )
            print(usuario)

# =========================
# Servicio de Préstamos
# =========================
class PrestamoServicio:
    def __init__(self, conexion, libro_servicio, usuario_servicio):
        self.conexion = conexion
        self.libro_servicio = libro_servicio
        self.usuario_servicio = usuario_servicio

    def registrar_prestamo(self, prestamo):
        # Verificar que el usuario existe
        usuario = self.usuario_servicio.obtener_usuario_por_id(prestamo.get_id_usuario())
        if not usuario:
            print("Error: Usuario no encontrado.")
            return False

        # Verificar que el libro existe y está disponible
        libro = self.libro_servicio.obtener_libro_por_id(prestamo.get_id_libro())
        if not libro:
            print("Error: Libro no encontrado.")
            return False
            
        if not libro.get_disponible():
            print("Error: El libro no está disponible.")
            return False

        # Registrar préstamo y actualizar disponibilidad
        resultado_prestamo = self.conexion.ejecutar(
            "INSERT INTO prestamos (id_usuario, id_libro, fecha_prestamo, fecha_devolucion) VALUES (%s, %s, %s, %s)",
            (prestamo.get_id_usuario(), prestamo.get_id_libro(), prestamo.get_fecha_prestamo(), prestamo.get_fecha_devolucion())
        )
        
        resultado_actualizacion = self.libro_servicio.actualizar_disponibilidad(prestamo.get_id_libro(), False)
        
        if resultado_prestamo and resultado_actualizacion:
            print("Préstamo registrado correctamente.")
            return True
        else:
            print("Error al registrar el préstamo.")
            return False

    def devolver_libro(self, id_prestamo):
        prestamo_data = self.conexion.consultar("SELECT * FROM prestamos WHERE id=%s", (id_prestamo,))
        if not prestamo_data:
            print("Error: Préstamo no encontrado.")
            return False

        resultado_prestamo = self.conexion.ejecutar(
            "UPDATE prestamos SET fecha_devolucion = %s WHERE id = %s", 
            (datetime.now().date(), id_prestamo)
        )
        
        resultado_actualizacion = self.libro_servicio.actualizar_disponibilidad(
            prestamo_data[0]['id_libro'], True
        )
        
        if resultado_prestamo and resultado_actualizacion:
            print("Libro devuelto correctamente.")
            return True
        else:
            print("Error al devolver el libro.")
            return False

    def listar_prestamos(self):
        prestamos = self.conexion.consultar("SELECT * FROM prestamos")
        for prestamo_data in prestamos:
            prestamo = Prestamo(
                prestamo_data['id_usuario'],
                prestamo_data['id_libro'],
                prestamo_data['fecha_prestamo'],
                prestamo_data['fecha_devolucion'],
                prestamo_data['id']
            )
            print(prestamo)

# =========================
# Aplicación Principal
# =========================
class BibliotecaApp:
    def __init__(self):
        self.conexion = ConexionBD()
        self.libro_servicio = LibroServicio(self.conexion)
        self.usuario_servicio = UsuarioServicio(self.conexion)
        self.prestamo_servicio = PrestamoServicio(
            self.conexion, self.libro_servicio, self.usuario_servicio
        )

    def menu_principal(self):
        while True:
            print("""\n===== SISTEMA DE BIBLIOTECA =====
1. Registrar Libro
2. Registrar Usuario
3. Registrar Préstamo
4. Devolver Libro
5. Listar Libros
6. Listar Préstamos
7. Listar Usuarios
0. Salir
================================
""")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.registrar_libro()
            elif opcion == '2':
                self.registrar_usuario()
            elif opcion == '3':
                self.registrar_prestamo()
            elif opcion == '4':
                self.devolver_libro()
            elif opcion == '5':
                self.listar_libros()
            elif opcion == '6':
                self.listar_prestamos()
            elif opcion == '7':
                self.listar_usuarios()
            elif opcion == '0':
                self.salir()
                break
            else:
                print("Opción no válida.")

    def registrar_libro(self):
        print("\n--- REGISTRAR LIBRO ---")
        titulo = input("Título: ").strip()
        autor = input("Autor: ").strip()
        
        try:
            anio = int(input("Año: "))
        except ValueError:
            print("Error: El año debe ser un número válido.")
            return
            
        libro = Libro(titulo, autor, anio)
        self.libro_servicio.registrar_libro(libro)

    def registrar_usuario(self):
        print("\n--- REGISTRAR USUARIO ---")
        nombre = input("Nombre del usuario: ").strip()
        tipo = input("Tipo (Estudiante/Profesor): ").strip()
        password = input("Contraseña: ").strip()
        
        usuario = Usuario(nombre, tipo, password)
        self.usuario_servicio.registrar_usuario(usuario)

    def registrar_prestamo(self):
        print("\n--- REGISTRAR PRÉSTAMO ---")
        try:
            id_usuario = int(input("ID Usuario: "))
            id_libro = int(input("ID Libro: "))
        except ValueError:
            print("Error: Los IDs deben ser números válidos.")
            return
            
        prestamo = Prestamo(id_usuario, id_libro)
        self.prestamo_servicio.registrar_prestamo(prestamo)

    def devolver_libro(self):
        print("\n--- DEVOLVER LIBRO ---")
        try:
            id_prestamo = int(input("ID del préstamo a devolver: "))
        except ValueError:
            print("Error: El ID debe ser un número válido.")
            return
            
        self.prestamo_servicio.devolver_libro(id_prestamo)

    def listar_libros(self):
        print("\n--- LISTA DE LIBROS ---")
        self.libro_servicio.listar_libros()

    def listar_prestamos(self):
        print("\n--- LISTA DE PRÉSTAMOS ---")
        self.prestamo_servicio.listar_prestamos()

    def listar_usuarios(self):
        print("\n--- LISTA DE USUARIOS ---")
        self.usuario_servicio.listar_usuarios()

    def salir(self):
        self.conexion.cerrar()
        print("Saliendo del sistema...")

# =========================
# Script SQL para crear la base de datos
# =========================
def crear_base_datos():
    sql_script = """
CREATE DATABASE IF NOT EXISTS biblioteca;
USE biblioteca;

CREATE TABLE IF NOT EXISTS libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    anio INT,
    disponible BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255),
    salt VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_libro INT,
    fecha_prestamo DATE,
    fecha_devolucion DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_libro) REFERENCES libros(id)
);
"""
    print("Script SQL para crear la base de datos:")
    print(sql_script)

# =========================
# Programa Principal
# =========================
if __name__ == "__main__":
    print("=== SISTEMA DE BIBLIOTECA REFACTORIZADO ===")
    print("Mejoras implementadas:")
    print("- Principios SOLID aplicados")
    print("- Encriptación segura de contraseñas")
    print("- Código modular y mantenible")
    print("- Validación de datos")
    print("- Prevención de inyección SQL")
    print("- Manejo robusto de errores")
    print()
    
    # Mostrar script de creación de BD
    crear_base_datos()
    print("\nEjecuta el script SQL anterior en MySQL antes de usar el sistema.\n")
    
    # Iniciar aplicación
    app = BibliotecaApp()
    app.menu_principal()
