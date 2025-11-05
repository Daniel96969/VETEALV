# SISTEMA DE BIBLIOTECA SEGURO
📘 Descripción
Este proyecto implementa un sistema de biblioteca en Python con conexión a MySQL.
Permite la gestión de usuarios y libros , con autenticación segura mediante contraseñas encriptadas (SHA-256).

⚙️ Características principales
Conexión y operaciones con MySQL .
Encriptación de contraseñas con hash SHA-256 .
Sistema de autenticación seguro (registro e inicio de sesión).
Gestión completa de usuarios y libros .
Menús interactivos en consola.
Manejo de errores y validaciones de datos.
🧱 Estructura del proyecto
📁 biblioteca_segura/
│
├── biblioteca.py       # Código principal del sistema
├── README.md           # Archivo de documentación
🧩 Clases principales
🔌ConexionBD
Administra la conexión con la base de datos MySQL y ejecuta consultas SQL.

🔐Encriptador
Maneja la encriptación y verificación de contraseñas usando SHA-256.

👤Usuario
Representa un usuario del sistema con sus atributos, incluyendo contraseña encriptada.

📖Libro
Administra la información y persistencia de los libros en la base de datos.

🧠SistemaAutenticacion
Controla el registro y autenticación de usuarios en el sistema.

🏛️SistemaBiblioteca
Clase principal que gestiona los menús e interacción con el usuario.

🗄️ Base de datos MySQL
Antes de ejecutar el sistema, cree la base de datos y tablas necesarias en MySQL:

CREATE DATABASE biblioteca2;
USE biblioteca2;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('Estudiante', 'Profesor', 'Administrativo') NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(64) NOT NULL
);

CREATE TABLE libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    anio INT NOT NULL,
    disponible BOOLEAN DEFAULT TRUE
);
🧰 Requisitos
Python 3.8 o superior
Servidor MySQL
Librerías necesarias (instalar con pip):
pip install mysql-connector-python
▶️Ejecución del programa
Clona o descarga este repositorio.
Asegúrate de que tu base de datos MySQL esté activa.
Ejecuta el programa:
python biblioteca.py
🧑‍💻 Funcionalidades del sistema
Inicio de sesión / Registro de usuarios
Gestión de libros (registro y listado)
Listar usuarios registrados
Cierre de sesión seguro
🧱 Seguridad
Contraseñas nunca se almacenan en texto plano.
Se utiliza el algoritmo de hash SHA-256 para proteger las credenciales.
Validaciones para evitar registros duplicados o datos inválidos.
📦 Licencia
Proyecto de libre uso con fines educativos.
Creado para fines de práctica de Python + MySQL + Seguridad 
