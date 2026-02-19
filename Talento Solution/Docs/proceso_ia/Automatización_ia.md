# Automatización e IA en el Proyecto `Biblioteca.py`

> Análisis de qué tareas resolver con scripts/CI clásico y cuáles potenciar con inteligencia artificial.

---

## Contexto del proyecto

`Biblioteca.py` es un sistema de gestión de biblioteca en Python con tres entidades principales:

- **`Libro`** — id, título, autor, estado de disponibilidad.
- **`Biblioteca`** — catálogo (diccionario), búsqueda flexible, historial de préstamos.
- **Operaciones** — `agregar_libro`, `buscar`, `prestar_libro`, `devolver_libro`.

El código actual es funcional pero simple. A medida que crezca (más entidades, base de datos, API, múltiples usuarios) aparecen tareas repetitivas que conviene automatizar, y otras más complejas que se benefician de IA.

---

## Parte 1 — Automatización "normal" (scripts + GitHub Actions)

Estas tareas son **deterministas, repetitivas y bien definidas**. No necesitan IA: un script o un pipeline de CI/CD las resuelve perfectamente y de forma más predecible y barata.

### 1.1 Tests automáticos en cada push

Ejecutar la suite de tests con `pytest` cada vez que se hace un commit o se abre un pull request.

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pytest
      - run: pytest tests/
```
## Parte 2 — Tareas para mejorar con IA

Estas tareas implican **lenguaje natural, contexto semántico, o patrones difíciles de capturar con reglas fijas**. Aquí la IA aporta un salto cualitativo real.

---

### 2.1 Búsqueda semántica del catálogo

**Situación actual:** `buscar("Orwell")` hace una búsqueda exacta de subcadena en título y autor.

**Problema:** Un usuario que busca `"novela distópica futuro"` o `"García Márquez realismo mágico"` no encuentra nada, aunque los libros existan.

**Con IA:** Usar embeddings (OpenAI, Sentence Transformers) para indexar los libros y responder a búsquedas semánticas:

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def indexar_catalogo(libros):
    textos = [f"{l.titulo} {l.autor}" for l in libros.values()]
    return model.encode(textos, convert_to_tensor=True)

def buscar_semantico(query, libros, embeddings):
    query_emb = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, embeddings)[0]
    top = scores.topk(3)
    return [list(libros.values())[i] for i in top.indices]
```

**Resultado:** El usuario escribe en lenguaje natural y obtiene resultados relevantes aunque no recuerde el título exacto.

---

### 2.2 Recomendaciones personalizadas

**Situación actual:** No existe ningún sistema de recomendación.

**Con IA:** Analizar el historial de préstamos de cada usuario y sugerir libros similares a los que ya leyó, usando filtrado colaborativo o embeddings de contenido.

```python
# Lógica conceptual
def recomendar(usuario_id, historial, catalogo, modelo):
    libros_leidos = [historial[id_] for id_ in historial if historial[id_] == usuario_id]
    # Generar embeddings de los libros leídos y buscar los más similares en el catálogo
    ...
```

Esto es imposible de hacer bien con reglas fijas: depende de patrones latentes en los datos.

---

### 2.3 Asistente conversacional para el bibliotecario

En lugar de llamar a funciones directamente, un chatbot interno podría interpretar comandos en lenguaje natural:

```
"Préstame el libro de Orwell a María" → prestar_libro("102", "María")
"¿Quién tiene prestado Sapiens?" → consultar historial
"Muéstrame todos los libros de ciencia ficción disponibles" → buscar + filtrar
```

Con un LLM (GPT-4, Claude, Llama local) actuando como interfaz, cualquier persona puede operar el sistema sin conocer la API.

---

### 2.4 Detección de anomalías y fraudes

**Con IA:** Un modelo de clasificación puede aprender patrones normales de uso y marcar comportamientos sospechosos:

- Un usuario que pide 10 libros en un día.
- El mismo libro "devuelto" varias veces sin haber sido prestado.
- Patrones de edición inusuales en el catálogo.

Con reglas fijas sólo puedes poner umbrales arbitrarios. Con ML el sistema aprende qué es "normal" a partir de los datos reales.

---

### 2.5 Generación automática de descripciones de libros

Si al añadir un libro sólo se tiene título y autor, un LLM puede generar automáticamente una sinopsis, etiquetas de género, nivel de lectura y palabras clave para mejorar la búsqueda:

```python
import anthropic

def enriquecer_libro(titulo: str, autor: str) -> dict:
    client = anthropic.Anthropic()
    prompt = f"""
    Dado el libro "{titulo}" de {autor}, genera un JSON con:
    - sinopsis (2-3 oraciones)
    - generos (lista)
    - nivel_lectura (básico/intermedio/avanzado)
    - palabras_clave (lista)
    """
    # Llamada al API...
```

Esto sería muy costoso de mantener manualmente para catálogos grandes.

---

### 2.6 Revisión inteligente de código (para el equipo dev)

En lugar de sólo linting estático, integrar un step en el pipeline que analice los PRs con un LLM para detectar:

- Bugs lógicos que `flake8` no ve (ej: `historial_prestamos.pop` sin comprobar si el libro realmente estaba prestado).
- Sugerencias de refactorización.
- Documentación faltante.

```yaml
# .github/workflows/ai-review.yml
- name: AI Code Review
  uses: anthropics/claude-code-action@v1
  with:
    prompt: "Revisa este PR buscando bugs lógicos, mejoras de rendimiento y documentación faltante"
```

---

## Resumen comparativo

| Tarea | Herramienta recomendada | Por qué |
|---|---|---|
| Tests en cada push | GitHub Actions + pytest | Determinista, reglas fijas |
| **Búsqueda semántica** | **Sentence Transformers / embeddings** | Lenguaje natural ambiguo |
| **Recomendaciones** | **ML colaborativo / embeddings** | Patrones latentes en datos |
| **Asistente conversacional** | **LLM (Claude / GPT)** | Interfaz en lenguaje natural |
| **Detección de anomalías** | **Clasificador ML** | Patrones no capturables con reglas |
| **Enriquecimiento de catálogo** | **LLM generativo** | Generación de contenido |
| **Revisión de código** | **LLM en CI/CD** | Razonamiento semántico sobre código |

---

## Conclusión

La regla práctica es sencilla: **si puedes escribir la condición exacta, automatízalo con un script**. Si la tarea requiere entender contexto, lenguaje natural o detectar patrones complejos, **la IA aporta valor real**. En `Biblioteca.py`, la base de automatización clásica (tests, CI, backups, alertas) debe estar sólida antes de añadir capas de IA encima.