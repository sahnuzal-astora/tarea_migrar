"""
Sistema de gestion de biblioteca con autenticacion y operaciones de productos, prestamos y categorias.
"""

from typing import Optional
from crud.producto_crud import ProductoCRUD
from crud.usuario_crud import UsuarioCRUD
from crud.prestamo_crud import PrestamoCRUD
from crud.libro_crud import LibroCRUD
from crud.revista_crud import RevistaCRUD
from crud.periodico_crud import PeriodicoCRUD
from crud.audiolibro_crud import AudiolibroCRUD
from crud.comic_crud import ComicCRUD
from crud.mapa_crud import MapaCRUD
from crud.tesis_crud import TesisCRUD

from database.config import SessionLocal, create_tables
from usuario import Usuario
import getpass


class SistemaBiblioteca:
    def __init__(self):
        self.db = SessionLocal()
        self.usuario_crud = UsuarioCRUD(self.db)
        self.producto_crud = ProductoCRUD(self.db)
        self.prestamo_crud = PrestamoCRUD(self.db)
        self.libro_crud = LibroCRUD(self.db)
        self.revista_crud = RevistaCRUD(self.db)
        self.periodico_crud = PeriodicoCRUD(self.db)
        self.audiolibro_crud = AudiolibroCRUD(self.db)
        self.comic_crud = ComicCRUD(self.db)
        self.mapa_crud = MapaCRUD(self.db)
        self.tesis_crud = TesisCRUD(self.db)
        self.usuario_actual: Optional[Usuario] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def mostrar_pantalla_login(self) -> bool:
        print("\n" + "=" * 50)
        print("        SISTEMA DE BIBLIOTECA")
        print("=" * 50)
        print("INICIAR SESION")
        print("=" * 50)
        intentos = 0
        max_intentos = 3
        while intentos < max_intentos:
            try:
                print(f"\nIntento {intentos + 1} de {max_intentos}")
                nombre_usuario = input("Nombre de usuario o email: ").strip()
                if not nombre_usuario:
                    print("ERROR: El nombre de usuario es obligatorio")
                    intentos += 1
                    continue
                contrasena = getpass.getpass("Contrasena: ")
                if not contrasena:
                    print("ERROR: La contrasena es obligatoria")
                    intentos += 1
                    continue
                usuario = self.usuario_crud.autenticar_usuario(
                    nombre_usuario, contrasena
                )
                if usuario:
                    self.usuario_actual = usuario
                    print(f"\nEXITO: ¡Bienvenido, {usuario.nombre}!")
                    if usuario.es_admin:
                        print("INFO: Tienes privilegios de administrador")
                    return True
                else:
                    print("ERROR: Credenciales incorrectas o usuario inactivo")
                    intentos += 1
            except KeyboardInterrupt:
                print("\n\nINFO: Operacion cancelada por el usuario")
                return False
            except Exception as e:
                print(f"ERROR: Error durante el login: {e}")
                intentos += 1
        print(
            f"\nERROR: Maximo de intentos ({max_intentos}) excedido. Acceso denegado."
        )
        return False

    def mostrar_menu_principal(self):
        while True:
            print("\n" + "=" * 50)
            print("    SISTEMA DE BIBLIOTECA")
            print("=" * 50)
            print(f"Usuario: {self.usuario_actual.nombre}")
            print(f"Email: {self.usuario_actual.email}")
            if self.usuario_actual.es_admin:
                print("Administrador")
            print("=" * 50)
            print("1. Agregar producto")
            print("2. Pedir prestado libro")
            print("3. Descripción de todos los productos")
            print("4. Devolver libro")
            print("5. Gestionar categorías")
            print("6. Mi Perfil")
            print("0. Cerrar Sesion")
            print("=" * 50)
            opcion = input("\nSeleccione una opcion: ").strip()
            if opcion == "1":
                self.agregar_producto()
            elif opcion == "2":
                self.pedir_prestado()
            elif opcion == "3":
                self.descripcion_productos()
            elif opcion == "4":
                self.devolver_libro()
            elif opcion == "5":
                self.menu_categorias()
            elif opcion == "6":
                self.mostrar_menu_perfil()
            elif opcion == "0":
                print("\n¡Hasta luego!")
                break
            else:
                print("ERROR: Opcion invalida. Intente nuevamente.")

    def agregar_producto(self):
        print("\n--- AGREGAR PRODUCTO ---")
        print("Seleccione categoría:")
        categorias = [
            ("Libro", self.libro_crud),
            ("Mapa", self.mapa_crud),
            ("Periodico", self.periodico_crud),
            ("Audiolibro", self.audiolibro_crud),
            ("Comic", self.comic_crud),
            ("Revista", self.revista_crud),
            ("Tesis", self.tesis_crud),
        ]
        for idx, (cat, _) in enumerate(categorias, 1):
            print(f"{idx}. {cat}")
        cat_idx = self.validar_numero(input("Opción: "))
        if cat_idx is None or not (1 <= cat_idx <= len(categorias)):
            print("Categoría inválida.")
            return
        categoria_nombre, categoria_crud = categorias[cat_idx - 1]
        # Solicitar datos según la categoría
        if categoria_nombre == "Libro":
            genero = self.validar_texto(input("Género: "))
            paginas = self.validar_numero(input("Páginas: "))
            producto_id = self.crear_producto_base()
            if genero and paginas and producto_id:
                categoria_crud.crear_libro(
                    genero, paginas, producto_id, self.usuario_actual.id_usuario
                )
        elif categoria_nombre == "Mapa":
            region = self.validar_texto(input("Región: "))
            escala = self.validar_texto(input("Escala: "))
            tipo = self.validar_texto(input("Tipo: "))
            producto_id = self.crear_producto_base()
            if region and escala and tipo and producto_id:
                categoria_crud.crear_mapa(
                    region, escala, tipo, producto_id, self.usuario_actual.id_usuario
                )
        elif categoria_nombre == "Periodico":
            fecha_publicacion = self.validar_texto(input("Fecha de publicación: "))
            producto_id = self.crear_producto_base()
            if fecha_publicacion and producto_id:
                categoria_crud.crear_periodico(
                    fecha_publicacion, producto_id, self.usuario_actual.id_usuario
                )
        elif categoria_nombre == "Audiolibro":
            narrador = self.validar_texto(input("Narrador: "))
            duracion = self.validar_numero(input("Duración (horas): "))
            formato = self.validar_texto(input("Formato: "))
            producto_id = self.crear_producto_base()
            if narrador and duracion and formato and producto_id:
                categoria_crud.crear_audiolibro(
                    narrador,
                    duracion,
                    formato,
                    producto_id,
                    self.usuario_actual.id_usuario,
                )
        elif categoria_nombre == "Comic":
            ilustrador = self.validar_texto(input("Ilustrador: "))
            editorial = self.validar_texto(input("Editorial: "))
            volumen = self.validar_texto(input("Volumen: "))
            producto_id = self.crear_producto_base()
            if ilustrador and editorial and volumen and producto_id:
                categoria_crud.crear_comic(
                    ilustrador,
                    editorial,
                    volumen,
                    producto_id,
                    self.usuario_actual.id_usuario,
                )
        elif categoria_nombre == "Revista":
            edicion = self.validar_texto(input("Edición: "))
            producto_id = self.crear_producto_base()
            if edicion and producto_id:
                categoria_crud.crear_revista(
                    edicion, producto_id, self.usuario_actual.id_usuario
                )
        elif categoria_nombre == "Tesis":
            universidad = self.validar_texto(input("Universidad: "))
            director = self.validar_texto(input("Director: "))
            grado_academico = self.validar_texto(input("Grado académico: "))
            producto_id = self.crear_producto_base()
            if universidad and director and grado_academico and producto_id:
                categoria_crud.crear_tesis(
                    universidad,
                    director,
                    grado_academico,
                    producto_id,
                    self.usuario_actual.id_usuario,
                )
        print(f"Producto agregado en la categoría '{categoria_nombre}'.")

    def crear_producto_base(self):
        titulo = self.validar_texto(input("Título: "))
        autor = self.validar_texto(input("Autor: "))
        anio = self.validar_numero(input("Año: "))
        disponible = True
        if titulo and autor and anio:
            producto = self.producto_crud.crear_producto(
                titulo=titulo,
                autor=autor,
                anio=anio,
                disponible=disponible,
                id_usuario_crea=self.usuario_actual.id_usuario,
            )
            return producto.id_producto
        return None

    def pedir_prestado(self):
        print("\n--- PEDIR PRESTADO LIBRO ---")
        libros = [
            p
            for p in self.producto_crud.obtener_productos()
            if p.disponible and hasattr(p, "titulo") and hasattr(p, "autor")
        ]
        libros = [
            l
            for l in libros
            if getattr(l, "titulo", None) and getattr(l, "autor", None)
        ]
        if not libros:
            print("No hay libros disponibles para préstamo.")
            return
        print("Libros disponibles:")
        for idx, libro in enumerate(libros, 1):
            print(f"{idx}. {libro.titulo} ({libro.autor})")
        sel = self.validar_numero(input("Seleccione libro: "))
        if sel is None or not (1 <= sel <= len(libros)):
            print("Selección inválida.")
            return
        libro = libros[sel - 1]
        self.prestamo_crud.crear_prestamo(
            usuario_id=self.usuario_actual.id_usuario,
            producto_id=libro.id_producto,
            id_usuario_crea=self.usuario_actual.id_usuario,
        )
        libro.disponible = False
        self.db.commit()
        print(f"Libro '{libro.titulo}' prestado exitosamente.")

    def descripcion_productos(self):
        print("\n--- DESCRIPCIÓN DE TODOS LOS PRODUCTOS ---")
        productos = self.producto_crud.obtener_productos()
        if not productos:
            print("No hay productos registrados.")
            return
        for p in productos:
            estado = "Disponible" if p.disponible else "Prestado"
            print(f"{p.titulo} ({p.autor}, {p.anio}) - {estado}")

    def devolver_libro(self):
        print("\n--- DEVOLVER LIBRO ---")
        prestamos_usuario = self.prestamo_crud.obtener_prestamos_por_usuario(
            self.usuario_actual.id_usuario
        )
        if not prestamos_usuario:
            print("No tienes libros prestados.")
            return
        productos = self.producto_crud.obtener_productos()
        libros_prestados = [
            p
            for p in productos
            if any(pr.producto_id == p.id_producto for pr in prestamos_usuario)
            and not p.disponible
        ]
        for idx, libro in enumerate(libros_prestados, 1):
            print(f"{idx}. {libro.titulo} ({libro.autor})")
        sel = self.validar_numero(input("Seleccione libro a devolver: "))
        if sel is None or not (1 <= sel <= len(libros_prestados)):
            print("Selección inválida.")
            return
        libro = libros_prestados[sel - 1]
        libro.disponible = True
        # Eliminar el préstamo
        for pr in prestamos_usuario:
            if pr.producto_id == libro.id_producto:
                self.db.delete(pr)
        self.db.commit()
        print(f"Libro '{libro.titulo}' devuelto exitosamente.")

    def menu_categorias(self):
        while True:
            print("\n--- GESTIÓN DE CATEGORÍAS ---")
            print("1. Crear categoría")
            print("2. Listar categorías")
            print("3. Actualizar categoría")
            print("4. Eliminar categoría")
            print("0. Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "1":
                self.crear_categoria()
            elif opcion == "2":
                self.listar_categorias()
            elif opcion == "3":
                self.actualizar_categoria()
            elif opcion == "4":
                self.eliminar_categoria()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida.")

    def crear_categoria(self):
        nombre = self.validar_texto(input("Nombre de la categoría: "))
        descripcion = self.validar_texto(input("Descripción (opcional): "))
        if nombre:
            self.categoria_crud.crear_categoria(
                nombre, descripcion, self.usuario_actual.id_usuario
            )
            print("Categoría creada exitosamente.")

    def listar_categorias(self):
        categorias = self.categoria_crud.obtener_categorias()
        if not categorias:
            print("No hay categorías registradas.")
            return
        print("\nCategorías registradas:")
        for idx, cat in enumerate(categorias, 1):
            print(f"{idx}. {cat.nombre} - {cat.descripcion}")

    def actualizar_categoria(self):
        self.listar_categorias()
        categorias = self.categoria_crud.obtener_categorias()
        if not categorias:
            return
        sel = self.validar_numero(input("Seleccione la categoría a actualizar: "))
        if sel is None or not (1 <= sel <= len(categorias)):
            print("Selección inválida.")
            return
        categoria = categorias[sel - 1]
        nuevo_nombre = self.validar_texto(input(f"Nuevo nombre ({categoria.nombre}): "))
        nueva_descripcion = self.validar_texto(
            input(f"Nueva descripción ({categoria.descripcion}): ")
        )
        self.categoria_crud.actualizar_categoria(
            categoria.id_categoria,
            id_usuario_edita=self.usuario_actual.id_usuario,
            nombre=nuevo_nombre or categoria.nombre,
            descripcion=nueva_descripcion or categoria.descripcion,
        )
        print("Categoría actualizada exitosamente.")

    def eliminar_categoria(self):
        self.listar_categorias()
        categorias = self.categoria_crud.obtener_categorias()
        if not categorias:
            return
        sel = self.validar_numero(input("Seleccione la categoría a eliminar: "))
        if sel is None or not (1 <= sel <= len(categorias)):
            print("Selección inválida.")
            return
        categoria = categorias[sel - 1]
        confirm = (
            input(f"¿Está seguro de eliminar '{categoria.nombre}'? (s/n): ")
            .strip()
            .lower()
        )
        if confirm == "s":
            self.categoria_crud.eliminar_categoria(categoria.id_categoria)
            print("Categoría eliminada exitosamente.")

    def mostrar_menu_perfil(self):
        while True:
            print("\n--- MI PERFIL ---")
            print("1. Ver Información Personal")
            print("2. Actualizar Información")
            print("3. Cambiar Contraseña")
            print("0. Volver al menú principal")
            opcion = input("\nSeleccione una opción: ").strip()
            if opcion == "1":
                self.ver_informacion_personal()
            elif opcion == "2":
                self.actualizar_informacion_personal()
            elif opcion == "3":
                self.cambiar_contrasena()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida. Intente nuevamente.")

    def ver_informacion_personal(self):
        try:
            print(f"\n--- INFORMACIÓN PERSONAL ---")
            print(f"Nombre: {self.usuario_actual.nombre}")
            print(f"Email: {self.usuario_actual.email}")
            print(f"Teléfono: {self.usuario_actual.telefono or 'No especificado'}")
            print(f"Estado: {'Activo' if self.usuario_actual.activo else 'Inactivo'}")
            print(
                f"Rol: {'Administrador' if self.usuario_actual.es_admin else 'Usuario'}"
            )
            print(f"Fecha de creación: {self.usuario_actual.fecha_creacion}")
        except Exception as e:
            print(f"ERROR: Error: {e}")

    def actualizar_informacion_personal(self):
        try:
            print(f"\n--- ACTUALIZAR INFORMACIÓN PERSONAL ---")
            print("Deje en blanco para mantener el valor actual")
            nuevo_nombre = input(
                f"Nombre actual ({self.usuario_actual.nombre}): "
            ).strip()
            nuevo_email = input(f"Email actual ({self.usuario_actual.email}): ").strip()
            nuevo_telefono = input(
                f"Teléfono actual ({self.usuario_actual.telefono or 'No especificado'}): "
            ).strip()
            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevo_email:
                cambios["email"] = nuevo_email
            if nuevo_telefono:
                cambios["telefono"] = nuevo_telefono
            if cambios:
                usuario_actualizado = self.usuario_crud.actualizar_usuario(
                    self.usuario_actual.id_usuario, **cambios
                )
                if usuario_actualizado:
                    self.usuario_actual = usuario_actualizado
                    print(f"EXITO: Información actualizada exitosamente")
                else:
                    print("ERROR: Error al actualizar la información")
            else:
                print("INFO: No se realizaron cambios.")
        except ValueError as e:
            print(f"ERROR: Error: {e}")
        except Exception as e:
            print(f"ERROR: Error inesperado: {e}")

    def cambiar_contrasena(self):
        try:
            print(f"\n--- CAMBIAR CONTRASEÑA ---")
            contrasena_actual = getpass.getpass("Contraseña actual: ")
            if not contrasena_actual:
                print("ERROR: La contraseña actual es obligatoria")
                return
            nueva_contrasena = getpass.getpass("Nueva contraseña: ")
            if not nueva_contrasena:
                print("ERROR: La nueva contraseña es obligatoria")
                return
            confirmar_contrasena = getpass.getpass("Confirmar nueva contraseña: ")
            if nueva_contrasena != confirmar_contrasena:
                print("ERROR: Las contraseñas no coinciden")
                return
            if self.usuario_crud.cambiar_contrasena(
                self.usuario_actual.id_usuario, contrasena_actual, nueva_contrasena
            ):
                print("EXITO: Contraseña cambiada exitosamente")
            else:
                print("ERROR: Error al cambiar la contraseña")
        except ValueError as e:
            print(f"ERROR: Error: {e}")
        except Exception as e:
            print(f"ERROR: Error inesperado: {e}")

    def validar_numero(self, valor):
        try:
            return int(valor)
        except ValueError:
            print("Debe ingresar un número válido.")
            return None

    def validar_texto(self, valor):
        if not valor or not valor.strip():
            print("El campo no puede estar vacío.")
            return None
        return valor.strip()

    def ejecutar(self):
        try:
            print("Iniciando Sistema de Biblioteca...")
            print("Configurando base de datos...")
            create_tables()
            print("Sistema listo para usar.")
            if not self.mostrar_pantalla_login():
                print("Acceso denegado. Hasta luego!")
                return
            self.mostrar_menu_principal()
        except KeyboardInterrupt:
            print("\n\nSistema interrumpido por el usuario.")
        except Exception as e:
            print(f"\nError critico: {e}")
        finally:
            self.db.close()


def main():
    with SistemaBiblioteca() as sistema:
        sistema.ejecutar()


if __name__ == "__main__":
    main()
