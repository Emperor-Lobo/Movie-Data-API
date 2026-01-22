USE tp_flask_tmdb;

SHOW TABLES;

SELECT COUNT(*) FROM movies;              -- ou movie si tu l’as appelée comme ça

SELECT tmdb_id, title, release_date, vote_average
FROM movies
LIMIT 10;

SELECT * FROM users;