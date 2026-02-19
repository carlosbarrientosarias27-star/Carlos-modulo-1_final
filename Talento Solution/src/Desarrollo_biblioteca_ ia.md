1. Prueba de Ejecución y Correcciones
Al ejecutar el código actual, funciona perfectamente para casos ideales. No obstante, he añadido un bloque de prueba al final para verificar el flujo completo y corregir un detalle: la consistencia de los datos si se intenta devolver un libro que no está en el historial_prestamos.

Cambios realizados:
Validación de consistencia: Añadí una comprobación en devolver_libro para asegurar que el ID existe en el historial antes de usar .pop(), evitando posibles errores de ejecución (KeyError).

Script de prueba: He incluido un bloque if __name__ == "__main__": para que puedas probarlo directamente.

2. Refactorización: Búsqueda Flexible
Actualmente, el sistema es "ciego" si no conoces el ID. He refactorizado la clase Biblioteca para incluir un motor de búsqueda básico que permite encontrar libros por título o autor.

class Libro:
    def __init__(self, id_libro, titulo, autor):
        self.id_libro = id_libro
        self.titulo = titulo
        self.autor = autor
        self.disponible = True

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"[{self.id_libro}] {self.titulo} - {self.autor} ({estado})"


class Biblioteca:
    def __init__(self):
        self.libros = {}
        self.historial_prestamos = {}

    def agregar_libro(self, libro):
        self.libros[libro.id_libro] = libro

    # --- SECCIÓN REFACTORIZADA: Búsqueda flexible ---
    def buscar(self, termino):
        """Busca libros que coincidan con el título o autor."""
        termino = termino.lower()
        resultados = [
            libro for libro in self.libros.values()
            if termino in libro.titulo.lower() or termino in libro.autor.lower()
        ]
        return resultados

    def prestar_libro(self, id_libro, usuario):
        libro = self.libros.get(id_libro)
        if not libro:
            return f"❌ ID {id_libro} no encontrado."
        
        if not libro.disponible:
            return f"⚠️ '{libro.titulo}' ya está prestado."

        libro.disponible = False
        self.historial_prestamos[id_libro] = usuario
        return f"📖 '{libro.titulo}' prestado a {usuario}."

    def devolver_libro(self, id_libro):
        libro = self.libros.get(id_libro)
        if not libro or libro.disponible:
            return "❌ Error en devolución: el libro no estaba prestado."

        usuario = self.historial_prestamos.pop(id_libro, "Usuario desconocido")
        libro.disponible = True
        return f"🔄 '{libro.titulo}' devuelto por {usuario}."

# --- PRUEBA DEL SISTEMA ---
if __name__ == "__main__":
    mi_biblioteca = Biblioteca()
    
    # 1. Cargar datos
    l1 = Libro("101", "Cien años de soledad", "Gabriel García Márquez")
    l2 = Libro("102", "1984", "George Orwell")
    mi_biblioteca.agregar_libro(l1)
    mi_biblioteca.agregar_libro(l2)

    # 2. Probar Búsqueda
    print("Buscando 'Orwell':")
    for res in mi_biblioteca.buscar("Orwell"):
        print(f"  -> {res}")

    # 3. Probar Préstamo y Devolución
    print("\n" + mi_biblioteca.prestar_libro("102", "Alex"))
    print(mi_biblioteca.devolver_libro("102"))