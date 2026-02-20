### Diagrama de Flujo: Proceso de Préstamo 

Este es el flujo lógico que sigue tu método prestar_libro(id_libro, usuario):

## Fragmento de código
<<<<<<< HEAD

```text
=======
``` text
>>>>>>> 8f4f96561844aa0f30354569f061812b4bb86f0f
graph TD
    A[Inicio: Solicitar préstamo] --> B{¿Existe el ID?}
    B -- No --> C[Retornar: ID no encontrado]
    B -- Sí --> D{¿Está disponible?}
    D -- No --> E[Retornar: Libro ya prestado]
    D -- Sí --> F[Cambiar disponible a False]
    F --> G[Registrar usuario en historial]
<<<<<<< HEAD
    G --> H[Retornar: Confirmación de éxito] 
    ```
=======
    G --> H[Retornar: Confirmación de éxito]
```
>>>>>>> 8f4f96561844aa0f30354569f061812b4bb86f0f
