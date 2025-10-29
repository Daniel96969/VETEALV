# Biblioteca 

**Proyecto:** Sistema de Biblioteca (consola) — compacto y seguro

## Qué hace

* Registrar libros, usuarios y préstamos.
* Devolver libros y listar registros.
* Contraseñas seguras (salt + PBKDF2), consultas parametrizadas y estructura modular.

## Instalación rápida

1. Crear entorno y activar:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Ejecutar `crear_bd.sql` en tu servidor MySQL (crea la BD y tablas).
3. Ajustar credenciales en `conexion.py`.

## Ejecutar

```bash
python main.py
```

Selecciona la opción deseada en el menú.

## Archivos clave

* `main.py` — interfaz y menú
* `conexion.py` — conexión MySQL (IConexionBD)
* `modelos/` — Libro, Usuario, Prestamo
* `servicios/` — lógica de libros, usuarios, préstamos
* `crear_bd.sql` — script para crear la base de datos

## Notas de seguridad

* No uses root en producción; crea un usuario con permisos mínimos.
* Mantén `salt` y `password_hash` (no guardes contraseñas en texto).
* Todas las consultas usan parámetros para evitar inyección SQL.

---

Si quieres, te entrego también una versión extendida o el `report.md` para la parte de vulnerabilidad (educativo).
