## 1. Revisa todo el código generado por IA: 

# ¿Hay algo sospechosamente copiado? 

    No en el sentido de robo de propiedad intelectual, sino en el uso de patrones genéricos.

Estructura de "Libro/Biblioteca": Es el ejemplo clásico de los tutoriales de Programación Orientada a Objetos (POO). La IA tiende a usar id_libro, titulo y autor porque es el estándar educativo. No es un problema, pero es código "de manual".

Filtros de búsqueda: El uso de termino.lower() y comprensiones de lista para buscar es una solución muy eficiente y común que la IA genera por defecto.

Comentarios y Emojis: El uso de íconos (📖, ❌, ⚠️) en los return es una marca muy característica de modelos de lenguaje modernos (como yo) para hacer la salida de consola más amigable. En un entorno profesional de backend, esos mensajes suelen ser simples strings o códigos de error.

# ¿Hay riesgos de seguridad? 

Aunque el código funciona para una prueba local, presenta riesgos si piensas escalarlo o conectarlo a una web:

🚩 Inyección de Datos (Manipulación de Memoria)
El método agregar_libro confía ciegamente en lo que recibe.

Riesgo: Si permites que un usuario externo defina el id_libro, podría sobrescribir un libro existente simplemente usando un ID que ya esté en el diccionario self.libros.

Solución: Validar si el ID ya existe antes de insertar.

🚩 Manejo de Concurrencia (Race Conditions)
Si este código se ejecutara en un servidor donde dos personas intentan tomar el mismo libro al mismo tiempo:

Riesgo: Ambos podrían pasar la validación if libro.disponible simultáneamente antes de que el estado cambie a False.

Solución: En el futuro, necesitarás "bloqueos" (locks) o transacciones de base de datos.

🚩 Persistencia Volátil
Actualmente, todo vive en el diccionario self.libros.

Riesgo: Si el script se detiene o hay un error, todos los datos se pierden. No hay una capa de persistencia (SQL, JSON o CSV). 

## 2. Uso de IA en este proyecto 

# ¿Qué Herramientas usaste? 
Google Geminis 

# ¿Para Qúe? 

    La IA no solo "escribió" líneas, sino que actuó como un consultor técnico en las siguientes áreas:

Estructuración de Clases: Definición de la relación lógica entre la clase Libro (entidad) y Biblioteca (controlador).

Refactorización de Búsqueda: Implementación de la búsqueda flexible mediante comprensiones de lista y normalización con .lower().

Generación de Casos de Prueba: Creación del bloque if __name__ == "__main__": para verificar el flujo de préstamos y devoluciones rápidamente.

Auditoría de Seguridad: Identificación de riesgos como la falta de persistencia de datos y la ausencia de validación de IDs duplicados. 

# ¿Qué porcentaje aproximado de código viene de IA? 

Código generado/sugerido por IA: 85%. La estructura completa de las clases y la lógica de los métodos principales (prestar, devolver, buscar) fue propuesta por el modelo.

Código/Lógica propia del usuario: 15%. Definición de los requisitos de negocio (qué atributos debe tener un libro) y la supervisión/ajuste de los mensajes de retorno. 

# Tus 3 reglas personales para usar IA de forma responsable 

    Para no depender ciegamente de la tecnología y mantener la calidad, sigo estas reglas:

Regla de la "Línea por Línea": Nunca pego código que no sea capaz de explicar. Si la IA usa una función que no conozco (como .pop() en diccionarios), debo investigar qué hace antes de integrarla.

Validación del "Peor Escenario": Siempre pregunto a la IA: "¿Cómo puede romperse este código?". Esto ayuda a identificar fallos de seguridad o bugs que la propia IA omitió en su primera respuesta.

Autoría Híbrida: La IA propone la estructura, pero yo personalizo la experiencia (mensajes de error, lógica específica de negocio) para asegurar que el software tenga un propósito humano y no sea solo un "copia y pega" genérico.
