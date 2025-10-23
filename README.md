# Sistema de Biblioteca Refactorizado 🏛️📚
Descripción del Proyecto
Este proyecto es una refactorización completa del Sistema de Biblioteca original, aplicando principios SOLID, buenas prácticas de programación y medidas de seguridad avanzadas. El sistema gestiona libros, usuarios y préstamos en una biblioteca con una arquitectura robusta y mantenible.

🚀 Características Principales
Gestión completa de libros (registro, consulta, disponibilidad)

Administración de usuarios con contraseñas encriptadas

Sistema de préstamos con control de fechas y devoluciones

Interfaz de consola intuitiva y fácil de usar

Base de datos MySQL para persistencia de datos

🔧 Mejoras Implementadas Respecto al Original
1. Principios SOLID Aplicados
SRP (Single Responsibility): Cada clase tiene una única responsabilidad

DIP (Dependency Inversion): Uso de interfaces para desacoplar dependencias

OCP (Open/Closed): Fácil extensión sin modificar código existente

2. Seguridad Avanzada
Encriptación PBKDF2 con salt para contraseñas

Prevención de inyección SQL mediante consultas parametrizadas

Validación exhaustiva de datos de entrada

Manejo seguro de errores sin exposición de información sensible

3. Arquitectura Modular
Separación en capas: Modelos, Servicios y Aplicación

Código reutilizable y fácil de mantener

Abstracción de la base de datos mediante interfaces

4. Robustez y Confiabilidad
Manejo completo de excepciones

Validaciones en múltiples niveles

Transacciones implícitas para operaciones críticas

Mensajes de error claros y orientados al usuario

📋 Requisitos del Sistema
Software Requerido
Python 3.8 o superior

MySQL Server 8.0 o superior

Biblioteca mysql-connector-python

Instalación de Dependencias
bash
pip install mysql-connector-python
🗃️ Estructura de la Base de Datos
Script de Creación
sql
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
🚀 Configuración y Ejecución
1. Configuración de la Base de Datos
python
# En el archivo biblioteca.py, modificar las credenciales:
conexion = mysql.connector.connect(
    host="localhost",
    user="root",           # Tu usuario de MySQL
    password="tu_password", # Tu contraseña de MySQL
    database="biblioteca"
)
2. Ejecutar el Sistema
bash
python biblioteca.py
📖 Manual de Usuario
Menú Principal
text
===== SISTEMA DE BIBLIOTECA =====
1. Registrar Libro
2. Registrar Usuario
3. Registrar Préstamo
4. Devolver Libro
5. Listar Libros
6. Listar Préstamos
7. Listar Usuarios
0. Salir
Funcionalidades Detalladas
1. Registrar Libro
Ingresar título, autor y año

Validación automática de campos obligatorios

Estado inicial: Disponible

2. Registrar Usuario
Nombre y tipo (Estudiante/Profesor)

Contraseña encriptada automáticamente

Almacenamiento seguro con salt

3. Registrar Préstamo
Verificación de existencia de usuario y libro

Control de disponibilidad del libro

Registro automático de fecha

4. Devolver Libro
Actualización de estado del libro

Registro de fecha de devolución

Liberación para nuevos préstamos

🔒 Medidas de Seguridad Implementadas
Encriptación de Contraseñas
python
# Uso de PBKDF2 con salt único por usuario
password_hash = hashlib.pbkdf2_hmac(
    'sha256', 
    password.encode('utf-8'), 
    salt.encode('utf-8'), 
    100000
).hex()
Prevención de Inyección SQL
python
# Consultas parametrizadas en lugar de concatenación
self.cursor.execute(
    "INSERT INTO libros (titulo, autor) VALUES (%s, %s)",
    (titulo, autor)  # Los valores se escapan automáticamente
)
Validación de Datos
Campos obligatorios verificados

Tipos de datos validados (números, fechas)

Longitudes máximas respetadas

🏗️ Arquitectura del Sistema
Patrones de Diseño Utilizados
Repository Pattern: Abstracción del acceso a datos

Service Layer: Lógica de negocio separada

Dependency Injection: Inyección de dependencias para testing

Estructura de Clases
text
BibliotecaApp (Main)
├── ConexionBD (Gestión de BD)
├── LibroServicio (Lógica de libros)
├── UsuarioServicio (Lógica de usuarios)
└── PrestamoServicio (Lógica de préstamos)
📊 Comparativa con Versión Original
Característica	Versión Original	Versión Refactorizada
Principios SOLID	Limitados	Completamente aplicados
Seguridad contraseñas	Texto plano	Encriptación PBKDF2
Inyección SQL	Vulnerable	Prevenida completamente
Modularidad	Código monolítico	Arquitectura por capas
Mantenibilidad	Difícil de extender	Fácil de mantener
Manejo de errores	Básico	Robustez empresarial
🐛 Solución de Problemas
Error de Conexión a MySQL
Verificar que MySQL esté ejecutándose

Confirmar credenciales en el código

Asegurar que la base de datos 'biblioteca' exista

