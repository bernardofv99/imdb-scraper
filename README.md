# 🎥 IMDb Top Movies Scraper

Este proyecto es una herramienta de scraping y persistencia de datos que extrae información de las películas mejor calificadas en [IMDb](https://www.imdb.com/chart/top/) y las guarda en una base de datos PostgreSQL. Permite también exportar los datos a CSV y ejecutar análisis SQL avanzados.

---

## 📦 Estructura del Proyecto

```
.
├── app
│   ├── crud/
│   │   └── movie_crud.py
│   ├── db/
│   │   ├── session.py
│   │   └── base_class.py
│   ├── models/
│   │   ├── movie.py
│   │   └── actor.py
│   ├── schemas/
│   │   └── movie.py
│   ├── scraping/
│   │   ├── imdb_scraper.py
│   │   └── base_scraper.py
│   └── utils/
│       ├── export_csv.py
│       └── logging_config.py
├── init_db.py
├── main.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🚀 ¿Cómo usarlo?

1. **Instalación**
   ```bash
   docker compose up --build
   ```

2. **Inicializar la Base de Datos**
   ```bash
   docker compose exec scraper python init_db.py
   ```

3. **Ejecutar el Scraper**
   ```bash
   docker compose exec scraper python main.py
   ```

---

## 📤 Exportación a CSV

Todos los datos válidos extraídos se guardan automáticamente en la carpeta `/exports/` con nombre dinámico tipo `export_movies_YYYYMMDD_HHMMSS.csv`.

---

## 🗃️ Modelo de Datos

### 🎬 Tabla `movies`

| Campo             | Tipo      |
|-------------------|-----------|
| id                | int       |
| title             | str       |
| rating            | float     |
| year              | int       |
| duration_minutes  | int       |
| metascore         | int/null  |
| detail_url        | str       |
| external_id       | str (unique) |
| platform          | enum      |

### 🎭 Tabla `actors`

| Campo    | Tipo      |
|----------|-----------|
| id       | int       |
| name     | str       |

### 🔗 Tabla intermedia `movie_actor` (relación muchos-a-muchos)

| Campo       | Tipo  |
|-------------|-------|
| movie_id    | FK -> movies.id |
| actor_id    | FK -> actors.id |

---

## 📊 Consultas SQL Avanzadas

### 1. Top 5 películas con mayor duración promedio por década

```sql
SELECT
  FLOOR(year / 10) * 10 AS decade,
  AVG(duration_minutes) AS avg_duration
FROM movies
GROUP BY decade
ORDER BY avg_duration DESC
LIMIT 5;
```

### 2. Desviación estándar de las calificaciones por año

```sql
SELECT
  year,
  COUNT(*) AS movie_count,
  ROUND(STDDEV(rating)::numeric, 2) AS std_rating
FROM movies
GROUP BY year
HAVING COUNT(*) > 1
ORDER BY year;
```

### 3. Películas con diferencia > 20% entre IMDB y Metascore normalizado

```sql
SELECT
  title,
  rating,
  metascore,
  ROUND(ABS(rating - metascore / 10)::numeric, 2) AS diff,
  ROUND(((ABS(rating - metascore / 10) / rating) * 100)::numeric, 2) AS diff_percent
FROM movies
WHERE metascore IS NOT NULL
  AND (ABS(rating - metascore / 10) / rating) > 0.2
ORDER BY diff_percent DESC;
```

### 4. Vista para relacionar películas y actores, con opción de filtrar por actor

```sql
CREATE OR REPLACE VIEW movie_actor_view AS
SELECT
  m.title AS movie_title,
  a.name AS actor_name,
  m.year,
  m.rating
FROM movies m
JOIN movie_actor ma ON m.id = ma.movie_id
JOIN actors a ON a.id = ma.actor_id;
```

**Ejemplo de consulta:**
```sql
SELECT * FROM movie_actor_view WHERE actor_name ILIKE 'Robert De Niro';
```

### 5. Índice sugerido para mejorar búsquedas por actor

```sql
CREATE INDEX idx_actor_name ON actors (name);
```

---

## 🧠 Mejoras Futuras

- Soporte para más plataformas (Rotten Tomatoes, TMDB, etc.)
- API REST con FastAPI
- Dashboard visual con Streamlit o Dash
- Carga incremental / detección de duplicados avanzada
- Testing con Pytest

---

## 👨‍💻 Autor

Bernardo Flores – Python Backend Developer  
[LinkedIn](www.linkedin.com/in/bernardo-fl)
