## 1. Prompt enviado a la IA 

"Refactoriza el método de búsqueda en la clase Biblioteca para que sea más flexible, permitiendo buscar tanto por título como por autor sin importar mayúsculas o minúsculas. Además, añade una pequeña sección de prueba al final del archivo para verificar que el préstamo y la devolución funcionan correctamente."

## 2. Respuesta de la IA

"He actualizado la lógica de búsqueda utilizando una list comprehension que normaliza el texto a minúsculas con .lower(). También he implementado un bloque if __name__ == "__main__": para que puedas ejecutar el archivo directamente y ver los resultados en la consola."

## 3. Cambios realizados (Qué he cambiado yo)

Basándome en el archivo Biblioteca.py proporcionado, estos son los cambios técnicos específicos:

Métodobuscar(self, termino) :

Se eliminó la búsqueda por ID exacto.

Se implementó el filtrado dinámico: termino in libro.titulo.lower() or termino in libro.autor.lower().

Ahora devuelve una lista de objetos en lugar de un solo objeto o un mensaje de error.

Gestión de Historial:

Se mejoró el método devolver_libro para que use .pop() sobre el diccionario historial_prestamos, permitiendo recuperar el nombre del usuario que devuelve el libro en el mensaje de confirmación.

Interfaz de Consola (Script de prueba):

Se añadió el bloque de ejecución principal para instanciar la Biblioteca, agregar libros de ejemplo (101, 102) y simular un flujo completo de búsqueda, préstamo y devolución.