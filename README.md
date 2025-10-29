README.md — Sistema de Biblioteca (Refactorizado)

Proyecto: Sistema de Biblioteca (refactorizado)
Propósito: Implementar buenas prácticas (SOLID), encriptación de contraseñas, consultas parametrizadas y código modular para una aplicación de gestión de libros, usuarios y préstamos. (Requisitos y entregables especificados en el enunciado). 

Ejercicio 12 (2)

Contenido de este README

Descripción breve

Estructura del proyecto

Requisitos (software)

Instalación y configuración rápida

Script SQL (crear BD y tablas)

Ejecución del programa

Qué se implementó (mapeado a lo pedido en el Word)

Puntos extra (instrucciones para la parte de vulnerabilidad, con advertencias)

Buenas prácticas y recomendaciones de seguridad

Licencia / entrega

1) Descripción breve

Esta aplicación es un sistema de biblioteca en consola (Python) que permite:

Registrar libros y usuarios.

Registrar préstamos y devoluciones.

Listar libros, usuarios y préstamos.

El código está refactorizado para seguir principios SOLID, separar responsabilidades y usar consultas parametrizadas y almacenamiento seguro de contraseñas (hash + salt). Estas mejoras responden directamente a los requisitos del enunciado del ejercicio. 

Ejercicio 12 (2)

2) Estructura del proyecto (sugerida)

(Nombre de carpetas y archivos propuestos para el repositorio)

biblioteca/
├── conexion.py                 # Clase ConexionBD que implementa IConexionBD
├── modelos/
│   ├── libro.py                # Clase Libro
│   ├── usuario.py              # Clase Usuario (hash + salt)
│   └── prestamo.py             # Clase Prestamo
├── servicios/
│   ├── libro_servicio.py       # Lógica de libros
│   ├── usuario_servicio.py     # Lógica de usuarios
│   └── prestamo_servicio.py    # Lógica de prestamos
├── main.py                     # BibliotecaApp: interfaz de consola / menú
├── crear_bd.sql                # Script SQL para crear BD y tablas
├── requirements.txt
└── README.md                   # (este archivo)


Nota: en el repositorio entregue una captura del programa funcionando (imagen) y el README en la raíz, tal como pide el enunciado. 

Ejercicio 12 (2)

3) Requisitos (software)

Python 3.8+

MySQL Server (o MariaDB) accesible localmente o por conexión remota (para pruebas locales usar localhost).

Paquetes Python: mysql-connector-python (u otro conector compatible).
Ejemplo requirements.txt mínimo:

mysql-connector-python

4) Instalación y configuración rápida

Clona el repositorio:

git clone https://github.com/<tu-usuario>/biblioteca.git
cd biblioteca


Crea un entorno virtual e instala dependencias:

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt


Ejecuta el script SQL para crear la base de datos y tablas (ver sección 5). Puedes ejecutar crear_bd.sql en MySQL Workbench o desde consola:

-- ejecutar contenido de crear_bd.sql


Ajusta la configuración de conexión en conexion.py (host, user, password, database). Crea un usuario MySQL con privilegios limitados para la app (principio de menor privilegio).

5) Script SQL (crear_bd.sql)

Incluye el script tal como se muestra en el enunciado; se puede guardar en crear_bd.sql y ejecutarlo:

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


Este script es el mismo sugerido en el enunciado del ejercicio. Ejecuta esto antes de usar la aplicación. 

Ejercicio 12 (2)

6) Ejecución del programa

Desde la raíz del proyecto:

python main.py


El programa mostrará el menú de consola con opciones:

Registrar Libro

Registrar Usuario

Registrar Préstamo

Devolver Libro

Listar Libros

Listar Préstamos

Listar Usuarios

Salir

Sigue las indicaciones en pantalla; el código valida IDs numéricos básicos y campos requeridos.

7) Qué se implementó (mapeo directo a lo pedido en el Word)

Del enunciado (resumen) se pedía:

Aplicar principios SOLID → Sí: separación de conexión, modelos y servicios; interfaz IConexionBD para desacoplar dependencias. 

Ejercicio 12 (2)

Encriptación de contraseñas → Sí: Usuario usa salt y hash (PBKDF2-HMAC-SHA256) antes de almacenar password_hash y salt. 

Ejercicio 12 (2)

Consultas parametrizadas → Sí: todas las consultas usan parámetros (%s) para prevenir inyección SQL. 

Ejercicio 12 (2)

Validación de datos y manejo de errores → Sí: validaciones en registro de libros/usuarios y manejo básico de excepciones en conexión/ejecución de consultas. 

Ejercicio 12 (2)

Código modular y mantenible → Sí: sugerida separación en archivos conexion.py, modelos/, servicios/, main.py. 

Ejercicio 12 (2)

8) Puntos extra (vulnerabilidad de inyección SQL) — Instrucciones y advertencia

El enunciado propone como puntos extra implementar deliberadamente una vulnerabilidad de inyección SQL, demostrar el ataque y documentarlo. ADVERTENCIA IMPORTANTE: la demostración sólo debe hacerse en un entorno controlado y local (por ejemplo, una VM o contenedor que no esté conectado a redes públicas ni datos reales). No intentes ejecutar ataques contra sistemas que no son de tu propiedad o sin autorización explícita.

Sugerencia de flujo para la parte extra (documentación para clase):

Crear una rama en tu repositorio puntos-extra donde implementarás una versión deliberadamente insegura (por ejemplo, una función buscar_usuario_inseguro que concatene el input en la consulta).

Marcar claramente en el README y en el código que esa rama/archivo contiene vulnerabilidades intencionales y que su propósito es educativo.

Demostración en laboratorio local: en tu máquina local (o VM), ejecutar la versión vulnerable y mostrar cómo una entrada manipula la consulta.

Documentar el proceso: capturas de pantalla, el payload usado (en clase), paso a paso del exploit y, crucialmente, cómo se mitigó (cambiar a consultas parametrizadas, validación, uso de ORM, privilegios mínimos).

Entrega: incluir en el repositorio la rama con la vulnerabilidad, un report.md que explique el experimento y la rama segura que corrige la vulnerabilidad.

No incluyo payloads detallados en este README público por razones éticas y de seguridad. Si necesitas ayuda para preparar la presentación (diapositivas, report.md que explique el proceso sin payloads explícitos), lo hago sin proporcionar instrucciones explotables en entornos no controlados. 

Ejercicio 12 (2)

9) Buenas prácticas y recomendaciones de seguridad (resumen)

Nunca uses credenciales root para la app; crea un usuario con permisos mínimos.

Almacena salt y password_hash (no la contraseña en texto). Se usa PBKDF2 con iteraciones (ya implementado). 

Ejercicio 12 (2)

Usa consultas parametrizadas siempre. Evita concatenar strings para construir SQL. 

Ejercicio 12 (2)

Hacer back-ups periódicos y tests unitarios para la lógica de servicios.

Registrar eventos importantes (errores) a logs locales, no imprimir datos sensibles en producción.

Para despliegue real, usar TLS entre app y DB y control de acceso a la base.

10) Entrega y comprobaciones (qué subir a GitHub)

Código fuente completo (estructura modular).

crear_bd.sql (script SQL).

requirements.txt.

README.md (este archivo).

Captura de pantalla del programa (imagen en /docs/ o en la raíz).

(Opcional, para punto extra) Rama puntos-extra/ con report.md que documente la vulnerabilidad y su corrección.



Un main.py y división en módulos exactamente como la estructura sugerida (si deseas que lo genere ahora, lo hago).

