CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tmdb_id INT NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    original_title VARCHAR(255),
    original_language VARCHAR(10),
    overview TEXT,
    poster_path VARCHAR(255),
    backdrop_path VARCHAR(255),
    release_date VARCHAR(20),
    popularity FLOAT,
    vote_average FLOAT,
    vote_count INT,
    adult BOOLEAN,
    video BOOLEAN,
    raw_json TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
