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

**Qué cubre:** que `prestar_libro`, `devolver_libro` y `buscar` siguen funcionando tras cualquier cambio.

---

### 1.2 Linting y formato de código

Aplicar `flake8` (estilo PEP8) y `black` (formato) automáticamente. Si el código no cumple el estándar, el pipeline falla antes de hacer merge.

```yaml
- run: pip install flake8 black
- run: black --check biblioteca.py
- run: flake8 biblioteca.py
```

---

### 1.3 Cobertura de tests

Generar un informe de cobertura con `pytest-cov` y publicarlo en cada PR para saber qué líneas no están probadas.

```bash
pytest --cov=biblioteca --cov-report=xml tests/
```

Se puede integrar con servicios como Codecov para ver la evolución de la cobertura en el tiempo.

---

### 1.4 Gestión de dependencias

Si el proyecto crece y usa librerías externas (`SQLAlchemy`, `FastAPI`, etc.), un script con `pip-audit` detecta vulnerabilidades conocidas en las dependencias:

```bash
pip install pip-audit
pip-audit
```

Se puede programar como tarea semanal en GitHub Actions.

---

### 1.5 Exportación/backup automático del catálogo

Un script cron que serialice el estado de la biblioteca a JSON o CSV cada noche:

```python
# scripts/backup.py
import json, datetime
from biblioteca import Biblioteca

def exportar(biblioteca: Biblioteca, path: str):
    datos = [
        {"id": id_, "titulo": l.titulo, "autor": l.autor, "disponible": l.disponible}
        for id_, l in biblioteca.libros.items()
    ]
    with open(path, "w") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
```

```yaml
# Programado cada día a las 2:00 AM (GitHub Actions)
on:
  schedule:
    - cron: '0 2 * * *'
```

---

### 1.6 Generación automática de changelog

Con `git-cliff` o `conventional-commits`, generar un `CHANGELOG.md` automático en cada release basado en los mensajes de commit. Sin IA, sin ambigüedad.

---

### 1.7 Notificaciones de préstamos vencidos

Un script que recorra `historial_prestamos`, compare fechas y envíe un email o notificación si hay devoluciones pendientes:

```python
# scripts/alertas.py
from datetime import datetime, timedelta

def prestamos_vencidos(historial: dict, plazo_dias: int = 15):
    hoy = datetime.now()
    return [
        (id_libro, info)
        for id_libro, info in historial.items()
        if hoy - info["fecha_prestamo"] > timedelta(days=plazo_dias)
    ]
```

Esto es lógica pura: no necesita IA.

---

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
| Linting y formato | flake8 + black | Reglas bien definidas |
| Cobertura de tests | pytest-cov + Codecov | Métrica objetiva |
| Backup del catálogo | Script cron + JSON | Lógica pura |
| Alertas de vencimiento | Script + email/webhook | Comparación de fechas |
| Changelog automático | git-cliff | Basado en commits |
| **Búsqueda semántica** | **Sentence Transformers / embeddings** | Lenguaje natural ambiguo |
| **Recomendaciones** | **ML colaborativo / embeddings** | Patrones latentes en datos |
| **Asistente conversacional** | **LLM (Claude / GPT)** | Interfaz en lenguaje natural |
| **Detección de anomalías** | **Clasificador ML** | Patrones no capturables con reglas |
| **Enriquecimiento de catálogo** | **LLM generativo** | Generación de contenido |
| **Revisión de código** | **LLM en CI/CD** | Razonamiento semántico sobre código |

---

## Conclusión

La regla práctica es sencilla: **si puedes escribir la condición exacta, automatízalo con un script**. Si la tarea requiere entender contexto, lenguaje natural o detectar patrones complejos, **la IA aporta valor real**. En `Biblioteca.py`, la base de automatización clásica (tests, CI, backups, alertas) debe estar sólida antes de añadir capas de IA encima.