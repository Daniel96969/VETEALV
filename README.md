📚 Sistema de Biblioteca Seguro
Un sistema de biblioteca desarrollado en Python con conexión a MySQL que implementa medidas de seguridad robustas para la gestión de usuarios y libros.

🌟 Características Principales
Característica	Descripción
🔐 Autenticación Segura	Sistema de registro e inicio de sesión con contraseñas encriptadas
🗄️ Base de Datos MySQL	Conexión robusta y operaciones eficientes con MySQL
🔒 Encriptación SHA-256	Contraseñas protegidas con hash seguro
👥 Gestión de Usuarios	Administración completa de usuarios del sistema
📖 Gestión de Libros	Control completo del inventario de libros
⚡ Interfaz Consola	Menús interactivos y fáciles de usar
🛡️ Validaciones	Manejo de errores y validación de datos
🏗️ Estructura del Proyecto
text
biblioteca_segura/
│
├── 📄 biblioteca.py          # Código principal del sistema
├── 📄 README.md              # Documentación del proyecto
└── 📄 requirements.txt       # Dependencias del proyecto
🧩 Clases Principales
🔌 ConexionBD
Maneja la conexión con la base de datos MySQL y ejecución de consultas SQL.

python
# Ejemplo de conexión
conexion = ConexionBD(host, usuario, password, database)
🔐 Encriptador
Gestiona la encriptación y verificación de contraseñas usando SHA-256.

python
# Encriptar contraseña
hash_seguro = Encriptador.encriptar_password("mi_contraseña")
👤 Usuario
Representa un usuario del sistema con sus atributos y métodos.

📖 Libro
Administra la información y persistencia de los libros.

🧠 SistemaAutenticacion
Controla el registro y autenticación de usuarios de manera segura.

🏛️ SistemaBiblioteca
Clase principal que coordina los menús e interacción con el usuario.

🗄️ Configuración de la Base de Datos
Crear Base de Datos y Tablas
sql
CREATE DATABASE biblioteca2;
USE biblioteca2;

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('Estudiante', 'Profesor', 'Administrativo') NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(64) NOT NULL
);

-- Tabla de libros
CREATE TABLE libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    anio INT NOT NULL,
    disponible BOOLEAN DEFAULT TRUE
);
⚙️ Requisitos del Sistema
Prerrequisitos
Python 3.8 o superior

Servidor MySQL activo

Librerías necesarias:

bash
pip install mysql-connector-python
Instalación y Ejecución
Clonar o descargar el repositorio

Configurar la base de datos MySQL con el script proporcionado

Ejecutar el programa:

bash
python biblioteca.py
🎯 Funcionalidades del Sistema
🔑 Autenticación
Registro seguro de nuevos usuarios

Inicio de sesión con credenciales validadas

Cierre de sesión seguro

📚 Gestión de Libros
Registro de nuevos libros en el sistema

Listado completo del inventario

Control de disponibilidad

👥 Administración de Usuarios
Listado de usuarios registrados

Gestión de tipos de usuario (Estudiante, Profesor, Administrativo)

🛡️ Medidas de Seguridad
Medida	Implementación
Contraseñas Encriptadas	Hash SHA-256 para almacenamiento seguro
Validación de Datos	Verificación de entradas para prevenir errores
Prevención de Duplicados	Validación de emails únicos en el sistema
Manejo de Errores	Control de excepciones para mayor estabilidad
📋 Menús del Sistema
Menú Principal
text
=== SISTEMA DE BIBLIOTECA SEGURO ===
1. Iniciar Sesión
2. Registrar Usuario
3. Salir
Menú de Usuario
text
=== MENÚ USUARIO ===
1. Registrar Libro
2. Listar Libros
3. Listar Usuarios
4. Cerrar Sesión
🚀 Uso del Sistema
Registro: Crear una nueva cuenta con tipo de usuario específico

Autenticación: Iniciar sesión con email y contraseña

Gestión: Acceder a las funcionalidades según permisos

Navegación: Utilizar menús intuitivos para las operaciones

📊 Ejemplo de Flujo
<img width="1958" height="2447" alt="deepseek_mermaid_20251106_4487a1" src="https://github.com/user-attachments/assets/3dcc8514-6c73-45d9-85d4-3b2e6eaadc00" />

🐛 Solución de Problemas
Error de Conexión a MySQL
Verificar que el servidor MySQL esté ejecutándose

Confirmar credenciales de acceso

Validar que la base de datos exista

Problemas de Autenticación
Revisar que el usuario esté registrado

Verificar que la contraseña sea correcta

Confirmar formato de email válido

📄 Licencia
Este proyecto es de libre uso con fines educativos. Desarrollado para prácticas de Python + MySQL + Seguridad.
