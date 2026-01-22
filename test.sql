USE tp_flask_tmdb;

SHOW TABLES;

DESCRIBE users;
DESCRIBE movies;
SELECT user, host FROM mysql.user;

-- 1. Créer l'utilisateur flaskuser avec un mot de passe
CREATE USER 'flaskuser'@'localhost' IDENTIFIED BY 'MotDePasse!123';

-- 2. Donner tous les droits sur la base tp_flask_tmdb
GRANT ALL PRIVILEGES ON tp_flask_tmdb.* TO 'flaskuser'@'localhost';

FLUSH PRIVILEGES;

SELECT user, host FROM mysql.user;

