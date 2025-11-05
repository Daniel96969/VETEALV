import mysql.connector
import datetime
import hashlib

# -------------------------------
# 🔌 CLASE CONEXIÓN BD
# -------------------------------
class ConexionBD:
    def _init_(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "Toor"
        self.database = "biblioteca2"
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conexion.is_connected():
                print("✅ Conexión exitosa a la base de datos")
                return True
        except mysql.connector.Error as e:
            print(f"❌ Error al conectar: {e}")
            return False

    def desconectar(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("🔌 Conexión cerrada")

    def ejecutar_consulta(self, consulta, parametros=None, fetch=False):
        try:
            if not self.conexion or not self.conexion.is_connected():
                if not self.conectar():
                    return None

            cursor = self.conexion.cursor()
            cursor.execute(consulta, parametros or ())

            if fetch:
                resultado = cursor.fetchall()
                cursor.close()
                return resultado
            else:
                self.conexion.commit()
                cursor.close()
                return True
        except mysql.connector.Error as e:
            print(f"❌ Error en consulta: {e}")
            return False

# -------------------------------
# 🔐 ENCRIPTACIÓN DE CONTRASEÑAS - CORREGIDO
# -------------------------------
class Encriptador:
    @staticmethod
    def encriptar_contrasena(contrasena):
        """Encripta la contraseña usando SHA-256"""
        return hashlib.sha256(contrasena.encode()).hexdigest()

    @staticmethod
    def verificar_contrasena(contrasena, hash_almacenado):
        """Verifica si la contraseña coincide con el hash"""
        # CORRECCIÓN: Usar self.encriptar_contrasena en lugar de la función global
        return Encriptador.encriptar_contrasena(contrasena) == hash_almacenado

# -------------------------------
# 👤 CLASE USUARIO CON CONTRASEÑA ENCRIPTADA
# -------------------------------
class Usuario:
    def _init_(self, nombre="", tipo="Estudiante", email="", contrasena="", id=None):
        self.__id = id
        self.__nombre = nombre
        self.__tipo = tipo
        self.__email = email
        self.__contrasena_hash = Encriptador.encriptar_contrasena(contrasena) if contrasena else ""

    # GETTERS
    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tipo(self):
        return self.__tipo

    @property
    def email(self):
        return self.__email

    # SETTERS
    @nombre.setter
    def nombre(self, valor):
        if isinstance(valor, str) and valor.strip():
            self.__nombre = valor.strip()
        else:
            raise ValueError("❌ Nombre inválido")

    @tipo.setter
    def tipo(self, valor):
        tipos_validos = ["Estudiante", "Profesor", "Administrativo"]
        if valor in tipos_validos:
            self.__tipo = valor
        else:
            raise ValueError(f"❌ Tipo inválido. Debe ser: {', '.join(tipos_validos)}")

    def establecer_contrasena(self, contrasena):
        """Establece una nueva contraseña encriptada"""
        if contrasena and len(contrasena) >= 4:
            self.__contrasena_hash = Encriptador.encriptar_contrasena(contrasena)
        else:
            raise ValueError("❌ La contraseña debe tener al menos 4 caracteres")

    def verificar_contrasena(self, contrasena):
        """Verifica si la contraseña es correcta"""
        return Encriptador.verificar_contrasena(contrasena, self.__contrasena_hash)

    def guardar_en_bd(self, conexion):
        """Guarda o actualiza un usuario en la base de datos"""
        try:
            if self.__id is None:
                consulta = "INSERT INTO usuarios (nombre, tipo, email, contrasena_hash) VALUES (%s, %s, %s, %s)"
                parametros = (self._nombre, self.tipo, self.email, self._contrasena_hash)
            else:
                consulta = "UPDATE usuarios SET nombre=%s, tipo=%s, email=%s, contrasena_hash=%s WHERE id=%s"
                parametros = (self._nombre, self.tipo, self.email, self.contrasena_hash, self._id)

            if conexion.ejecutar_consulta(consulta, parametros):
                print("✅ Usuario guardado exitosamente")
                return True
            return False
        except Exception as e:
            print(f"❌ Error al guardar usuario: {e}")
            return False

    def _str_(self):
        return f"👤 ID: {self._id} - {self.nombre} ({self.tipo}) - {self._email}"

    # MÉTODOS DE CLASE
    @classmethod
    def obtener_por_id(cls, conexion, id_usuario):
        consulta = "SELECT id, nombre, tipo, email, contrasena_hash FROM usuarios WHERE id = %s"
        resultado = conexion.ejecutar_consulta(consulta, (id_usuario,), fetch=True)
        if resultado:
            id, nombre, tipo, email, contrasena_hash = resultado[0]
            usuario = cls(nombre, tipo, email, "", id)
            usuario.__contrasena_hash = contrasena_hash
            return usuario
        return None

    @classmethod
    def obtener_por_email(cls, conexion, email):
        consulta = "SELECT id, nombre, tipo, email, contrasena_hash FROM usuarios WHERE email = %s"
        resultado = conexion.ejecutar_consulta(consulta, (email,), fetch=True)
        if resultado:
            id, nombre, tipo, email, contrasena_hash = resultado[0]
            usuario = cls(nombre, tipo, email, "", id)
            usuario.__contrasena_hash = contrasena_hash
            return usuario
        return None

    @classmethod
    def obtener_todos(cls, conexion):
        consulta = "SELECT id, nombre, tipo, email, contrasena_hash FROM usuarios ORDER BY id"
        resultados = conexion.ejecutar_consulta(consulta, fetch=True)
        usuarios = []
        if resultados:
            for r in resultados:
                id, nombre, tipo, email, contrasena_hash = r
                usuario = cls(nombre, tipo, email, "", id)
                usuario.__contrasena_hash = contrasena_hash
                usuarios.append(usuario)
        return usuarios

# -------------------------------
# 📖 CLASE LIBRO (SIMPLIFICADA)
# -------------------------------
class Libro:
    def _init_(self, titulo="", autor="", anio=0, disponible=True, id=None):
        self.__id = id
        self.__titulo = titulo
        self.__autor = autor
        self.__anio = anio
        self.__disponible = disponible

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @property
    def autor(self):
        return self.__autor

    @property
    def disponible(self):
        return self.__disponible

    def guardar_en_bd(self, conexion):
        try:
            if self.__id is None:
                consulta = "INSERT INTO libros (titulo, autor, anio, disponible) VALUES (%s, %s, %s, %s)"
                parametros = (self._titulo, self.autor, self.anio, self._disponible)
            else:
                consulta = "UPDATE libros SET titulo=%s, autor=%s, anio=%s, disponible=%s WHERE id=%s"
                parametros = (self._titulo, self.autor, self.anio, self.disponible, self._id)

            if conexion.ejecutar_consulta(consulta, parametros):
                print("✅ Libro guardado exitosamente")
                return True
            return False
        except Exception as e:
            print(f"❌ Error al guardar libro: {e}")
            return False

    def _str_(self):
        estado = "✅ Disponible" if self.__disponible else "📖 Prestado"
        return f"📚 ID: {self._id} - '{self.titulo}' por {self._autor} - {estado}"

    @classmethod
    def obtener_por_id(cls, conexion, id_libro):
        consulta = "SELECT id, titulo, autor, anio, disponible FROM libros WHERE id = %s"
        resultado = conexion.ejecutar_consulta(consulta, (id_libro,), fetch=True)
        if resultado:
            id, titulo, autor, anio, disponible = resultado[0]
            return cls(titulo, autor, anio, disponible, id)
        return None

    @classmethod
    def obtener_todos(cls, conexion):
        consulta = "SELECT id, titulo, autor, anio, disponible FROM libros ORDER BY id"
        resultados = conexion.ejecutar_consulta(consulta, fetch=True)
        libros = []
        if resultados:
            for r in resultados:
                id, titulo, autor, anio, disponible = r
                libros.append(cls(titulo, autor, anio, disponible, id))
        return libros

# -------------------------------
# 🔐 SISTEMA DE AUTENTICACIÓN
# -------------------------------
class SistemaAutenticacion:
    def _init_(self, conexion):
        self.conexion = conexion

    def registrar_usuario(self, nombre, tipo, email, contrasena):
        """Registra un nuevo usuario con contraseña encriptada"""
        try:
            # Verificar si el email ya existe
            usuario_existente = Usuario.obtener_por_email(self.conexion, email)
            if usuario_existente:
                print("❌ El email ya está registrado")
                return False

            usuario = Usuario(nombre, tipo, email, contrasena)
            return usuario.guardar_en_bd(self.conexion)
        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")
            return False

    def autenticar_usuario(self, email, contrasena):
        """Autentica un usuario por email y contraseña"""
        usuario = Usuario.obtener_por_email(self.conexion, email)
        if usuario and usuario.verificar_contrasena(contrasena):
            print(f"✅ Bienvenido, {usuario.nombre}!")
            return usuario
        else:
            print("❌ Credenciales incorrectas")
            return None

# -------------------------------
# ⚙ SISTEMA PRINCIPAL MEJORADO
# -------------------------------
class SistemaBiblioteca:
    def _init_(self):
        self.conexion_bd = ConexionBD()
        self.auth = SistemaAutenticacion(self.conexion_bd)
        self.usuario_actual = None

    def iniciar(self):
        print("\n" + "="*50)
        print("        🏛️  SISTEMA DE BIBLIOTECA SEGURO")
        print("="*50)
        
        if not self.conexion_bd.conectar():
            return
        
        self.menu_autenticacion()
        self.conexion_bd.desconectar()

    def menu_autenticacion(self):
        """Menú de autenticación"""
        while True:
            print("\n🔐 SISTEMA DE AUTENTICACIÓN")
            print("1. Iniciar sesión")
            print("2. Registrar nuevo usuario")
            print("3. Salir")
            
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                email = input("Email: ").strip()
                contrasena = input("Contraseña: ").strip()
                self.usuario_actual = self.auth.autenticar_usuario(email, contrasena)
                if self.usuario_actual:
                    self.menu_principal()
                    
            elif opcion == "2":
                self.registrar_usuario()
                
            elif opcion == "3":
                print("👋 ¡Hasta pronto!")
                break
            else:
                print("❌ Opción inválida")

    def registrar_usuario(self):
        """Registra un nuevo usuario"""
        print("\n--- REGISTRAR NUEVO USUARIO ---")
        nombre = input("Nombre completo: ").strip()
        tipo = input("Tipo (Estudiante/Profesor/Administrativo): ").strip()
        email = input("Email: ").strip()
        contrasena = input("Contraseña: ").strip()
        
        if self.auth.registrar_usuario(nombre, tipo, email, contrasena):
            print("✅ Usuario registrado exitosamente")

    def menu_principal(self):
        """Menú principal del sistema"""
        while True:
            print(f"\n🏛️  MENÚ PRINCIPAL - Usuario: {self.usuario_actual.nombre}")
            print("1. 📚 Gestión de Libros")
            print("2. 👤 Listar Usuarios")
            print("3. 🔐 Cerrar sesión")
            
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.menu_libros()
            elif opcion == "2":
                self.listar_usuarios()
            elif opcion == "3":
                self.usuario_actual = None
                print("🔒 Sesión cerrada")
                break
            else:
                print("❌ Opción inválida")

    def menu_libros(self):
        """Menú de gestión de libros"""
        while True:
            print("\n📚 GESTIÓN DE LIBROS")
            print("1. Registrar nuevo libro")
            print("2. Listar todos los libros")
            print("3. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.registrar_libro()
            elif opcion == "2":
                self.listar_libros()
            elif opcion == "3":
                break
            else:
                print("❌ Opción inválida")

    def registrar_libro(self):
        """Registra un nuevo libro"""
        titulo = input("Título: ").strip()
        autor = input("Autor: ").strip()
        libro = Libro(titulo, autor, datetime.datetime.now().year)
        if libro.guardar_en_bd(self.conexion_bd):
            print("✅ Libro registrado exitosamente")

    def listar_libros(self):
        """Lista todos los libros"""
        libros = Libro.obtener_todos(self.conexion_bd)
        if libros:
            print("\n--- LISTA DE LIBROS ---")
            for libro in libros:
                print(f"   {libro}")
        else:
            print("📚 No hay libros registrados")

    def listar_usuarios(self):
        """Lista todos los usuarios"""
        usuarios = Usuario.obtener_todos(self.conexion_bd)
        if usuarios:
            print("\n--- LISTA DE USUARIOS ---")
            for usuario in usuarios:
                print(f"   {usuario}")
        else:
            print("👥 No hay usuarios registrados")

# -------------------------------
# 🏁 FUNCIÓN PRINCIPAL
# -------------------------------
def main():
    sistema = SistemaBiblioteca()
    sistema.iniciar()

if _name_ == "_main_":
    main()
