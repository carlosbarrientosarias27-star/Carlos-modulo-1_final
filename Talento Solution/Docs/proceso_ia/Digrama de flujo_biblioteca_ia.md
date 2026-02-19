### Diagrama de Flujo: Proceso de Préstamo 

Este es el flujo lógico que sigue tu método prestar_libro(id_libro, usuario):

Fragmento de código
graph TD
    A[Inicio: Solicitar préstamo] --> B{¿Existe el ID?}
    B -- No --> C[Retornar: ID no encontrado]
    B -- Sí --> D{¿Está disponible?}
    D -- No --> E[Retornar: Libro ya prestado]
    D -- Sí --> F[Cambiar disponible a False]
    F --> G[Registrar usuario en historial]
    G --> H[Retornar: Confirmación de éxito]