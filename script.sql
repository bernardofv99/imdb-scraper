-- 1. Top 5 películas con mayor duración promedio por década
SELECT
  FLOOR(year / 10) * 10 AS decade,
  AVG(duration_minutes) AS avg_duration
FROM movies
GROUP BY decade
ORDER BY avg_duration DESC
LIMIT 5;

-- 2. Desviación estándar de las calificaciones por año
SELECT
  year,
  COUNT(*) AS movie_count,
  ROUND(STDDEV(rating)::numeric, 2) AS std_rating
FROM movies
GROUP BY year
HAVING COUNT(*) > 1
ORDER BY year;

-- 3. Películas con diferencia > 20% entre IMDB y Metascore normalizado
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

-- 4. Vista para relacionar películas y actores, con opción de filtrar por actor
CREATE OR REPLACE VIEW movie_actor_view AS
SELECT
  m.title AS movie_title,
  a.name AS actor_name,
  m.year,
  m.rating
FROM movies m
JOIN movie_actor ma ON m.id = ma.movie_id
JOIN actors a ON a.id = ma.actor_id;

-- Ejemplo de consulta a la vista:
-- SELECT * FROM movie_actor_view WHERE actor_name ILIKE 'Robert De Niro';
-- SELECT * FROM movie_actor_view WHERE actor_name ILIKE 'Tom Hanks';

-- 5. Índice sugerido para mejorar búsquedas por actor
CREATE INDEX idx_actor_name ON actors (name);