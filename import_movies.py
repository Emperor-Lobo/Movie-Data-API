import requests
import mysql.connector
import json

# ---------- CONFIG ----------

API_KEY = "7c6eca28d3d2cd801a8a05c47d28c7c4"
BASE_URL = "https://api.themoviedb.org/3"

DB_CONFIG = {
    "host": "localhost",
    "user": "flaskuser",
    "password": "MotDePasse!123",   
    "database": "tp_flask_tmdb",
    "charset": "utf8mb4"
}


# Si ta table s'appelle `movie` et pas `movies`, change le nom dans la requête SQL plus bas.


# ---------- FONCTION POUR RÉCUPÉRER LES FILMS ----------

def fetch_popular_movies(page=1, language="fr-FR"):
    """
    Récupère les films populaires à partir de l'API TMDb pour une page donnée.
    """
    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": language,
        "page": page
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])


# ---------- IMPORT DANS MYSQL ----------

def import_movies(max_pages=1):
    """
    Importe les films des pages 1..max_pages dans la table movies.
    Utilise tmdb_id comme clé unique pour éviter les doublons.
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # ⚠️ Si ta table s'appelle `movie` (sans s), remplace `movies` ici :
    insert_sql = """
        INSERT INTO movies (
            tmdb_id,
            title,
            original_title,
            original_language,
            overview,
            poster_path,
            backdrop_path,
            release_date,
            popularity,
            vote_average,
            vote_count,
            adult,
            video,
            raw_json
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            original_title = VALUES(original_title),
            original_language = VALUES(original_language),
            overview = VALUES(overview),
            poster_path = VALUES(poster_path),
            backdrop_path = VALUES(backdrop_path),
            release_date = VALUES(release_date),
            popularity = VALUES(popularity),
            vote_average = VALUES(vote_average),
            vote_count = VALUES(vote_count),
            adult = VALUES(adult),
            video = VALUES(video),
            raw_json = VALUES(raw_json);
    """

    total_inserted = 0

    try:
        for page in range(1, max_pages + 1):
            print(f"🔎 Récupération des films populaires, page {page}...")
            movies = fetch_popular_movies(page=page)

            if not movies:
                print("Aucun résultat, arrêt.")
                break

            for film in movies:
                values = (
                    film.get("id"),
                    film.get("title"),
                    film.get("original_title"),
                    film.get("original_language"),
                    film.get("overview"),
                    film.get("poster_path"),
                    film.get("backdrop_path"),
                    film.get("release_date"),
                    film.get("popularity"),
                    film.get("vote_average"),
                    film.get("vote_count"),
                    film.get("adult"),
                    film.get("video"),
                    json.dumps(film, ensure_ascii=False)
                )
                cursor.execute(insert_sql, values)
                total_inserted += 1

            conn.commit()
            print(f"✅ Page {page} importée.")

    except Exception as e:
        print("❌ Erreur pendant l'import :", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    print(f"🎬 Import terminé. Films traités (insert ou update) : {total_inserted}")


if __name__ == "__main__":
    # Pour commencer, importe juste la page 1
    import_movies(max_pages=1)
    # Si tu veux plus tard : import_movies(max_pages=5) pour plus de pages
