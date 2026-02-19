1. Registro de nuevos ejemplares
Como bibliotecario,

quiero poder agregar libros con ID, título y autor al sistema,

para mantener el catálogo actualizado y disponible para los usuarios.

Criterio de aceptación: El sistema debe permitir instanciar objetos de la clase Libro y almacenarlos en el diccionario de la Biblioteca mediante el método agregar_libro.

2. Búsqueda flexible de libros
Como usuario de la biblioteca,

quiero buscar libros por una palabra clave (ya sea parte del título o del autor),

para encontrar rápidamente lo que deseo leer sin necesidad de saber el ID exacto.

Criterio de aceptación: El método buscar debe ignorar mayúsculas/minúsculas y devolver una lista de todos los libros que contengan el término en su título o autor.

3. Gestión de préstamos
Como bibliotecario,

quiero registrar el préstamo de un libro a un usuario específico mediante su ID,

para saber quién tiene cada libro y evitar que un libro ya prestado se entregue a otra persona.

Criterio de aceptación: Al ejecutar prestar_libro, el estado del libro debe cambiar a disponible = False y el nombre del usuario debe guardarse en el historial.

4. Control de devoluciones
Como bibliotecario,

quiero procesar la devolución de un libro usando su ID,

para que el ejemplar vuelva a aparecer como disponible y se limpie el registro de préstamos activos.

Criterio de aceptación: El método devolver_libro debe validar que el libro esté realmente prestado antes de cambiar su estado a disponible = True y eliminarlo del historial de préstamos.

5. Visualización de estado del libro
Como usuario o administrador,

quiero ver una representación clara del libro que incluya su ID, título, autor y estado actual,

para identificar de un vistazo si puedo solicitarlo o no.

Criterio de aceptación: El método especial __str__ de la clase Libro debe devolver una cadena formateada que muestre si el libro está "Disponible" o "Prestado".