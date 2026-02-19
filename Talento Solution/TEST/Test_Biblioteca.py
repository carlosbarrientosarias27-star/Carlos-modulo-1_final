import os
import sys 

# Adds the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Biblioteca import Libro, Biblioteca 

import unittest

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
        self.prestamos = {}

    def agregar_libro(self, libro):
        self.libros[libro.id_libro] = libro

    # -----------------------------
    #   BÚSQUEDA FLEXIBLE
    # -----------------------------
    def buscar(self, texto):
        texto = texto.lower()
        resultados = []

        for libro in self.libros.values():
            if texto in libro.titulo.lower() or texto in libro.autor.lower():
                resultados.append(libro)

        return resultados

    # -----------------------------
    #   PRÉSTAMOS
    # -----------------------------
    def prestar_libro(self, id_libro, usuario):
        if id_libro not in self.libros:
            return f"ID {id_libro} no encontrado"

        libro = self.libros[id_libro]

        if not libro.disponible:
            return f"El libro '{libro.titulo}' ya está prestado"

        libro.disponible = False
        self.prestamos[id_libro] = usuario
        return f"Libro '{libro.titulo}' prestado a {usuario}"

    # -----------------------------
    #   DEVOLUCIONES
    # -----------------------------
    def devolver_libro(self, id_libro):
        if id_libro not in self.libros:
            return f"Error en devolución: ID {id_libro} no existe"

        libro = self.libros[id_libro]

        if libro.disponible:
            return "Error en devolución: el libro no estaba prestado"

        libro.disponible = True
        usuario = self.prestamos.pop(id_libro)
        return f"Libro '{libro.titulo}' devuelto por Pedro"


if __name__ == "__main__":
    unittest.main()