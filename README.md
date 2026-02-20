# Carlos-modulo-1_final
Planifique un sistema de Gestión de biblioteca 

Donde lo Estructure asi: 

## Sistema de Gestión de Biblioteca (Piloto IA)
Este proyecto es un piloto experimental diseñado para demostrar la integración de la Inteligencia Artificial en el flujo de desarrollo de software (SDLC). El sistema permite gestionar un catálogo de libros, procesar préstamos y registrar devoluciones de forma eficiente.

## Estructura del Sistema
El núcleo del sistema se divide en dos componentes principales:

# 1. Entidad Libro (Class Libro)
Representa la unidad básica de información del catálogo.

Atributos: ID único, título, autor y estado de disponibilidad.

Funcionalidad: Formateo automático de la información del libro para visualización del usuario.

# 2. Motor de Gestión (Class Biblioteca)
Controla la lógica de negocio y el almacenamiento de datos.

Gestión de Inventario: Permite agregar libros al sistema mediante un diccionario para búsquedas rápidas por ID.

Búsqueda Flexible: Implementa un motor de búsqueda semántica (asistido por IA) que permite encontrar obras por coincidencias parciales en títulos o autores, ignorando mayúsculas y minúsculas.

Módulo de Préstamos: * Valida la existencia del ejemplar.

Verifica si el libro ya está en préstamo para evitar duplicidad.

Asigna el libro a un usuario específico.

Módulo de Devoluciones: * Restablece la disponibilidad del ejemplar.

Limpia el registro del historial de préstamos activos.

## Flujo de Desarrollo Asistido por IA
Para este proyecto, se han aplicado herramientas de IA en las siguientes etapas:

Planificación: Definición de los métodos necesarios para un flujo lógico de préstamo y devolución.

Generación de Código: Creación de la lógica de clases en Python y refactorización de la función de búsqueda.

Documentación: Generación de este archivo README.md y de los docstrings internos del código.

Reflexión Ética: Análisis sobre la propiedad del código generado y la privacidad de los datos de los usuarios (historial de préstamos).
