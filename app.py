import os
import requests
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------------------------
# Config Flask
# -------------------------------------------------
app = Flask(__name__)

# ⚠️ change-moi en vraie valeur secrète
app.config["SECRET_KEY"] = "change_this_secret_key"

# -------------------------------------------------
# Config MySQL (adapter user / mdp si besoin)
# -------------------------------------------------
DB_USER = "flaskuser"
DB_PASSWORD = "MotDePasse!123"   # le même que dans CREATE USER
DB_HOST = "localhost"
DB_NAME = "tp_flask_tmdb"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------------------------------
# Config API TMDb
# -------------------------------------------------
TMDB_API_KEY = "7c6eca28d3d2cd801a8a05c47d28c7c4"
TMDB_BASE_URL = "https://api.themoviedb.org/3"


# -------------------------------------------------
# Modèles
# -------------------------------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    original_title = db.Column(db.String(255))
    original_language = db.Column(db.String(10))
    overview = db.Column(db.Text)
    poster_path = db.Column(db.String(255))
    backdrop_path = db.Column(db.String(255))
    release_date = db.Column(db.String(20))
    popularity = db.Column(db.Float)
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    adult = db.Column(db.Boolean)
    video = db.Column(db.Boolean)


# -------------------------------------------------
# Fonctions utilitaires TMDb
# -------------------------------------------------
def search_movies_tmdb(query, language="fr-FR"):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "language": language,
        "query": query
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json().get("results", [])


# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/")
def index():
    # Page d'accueil : redirige selon état de connexion
    if "user_id" in session:
        return redirect(url_for("catalogue"))
    return redirect(url_for("login"))


# --------- Inscription ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not username or not email or not password:
            flash("Tous les champs sont obligatoires.", "danger")
            return redirect(url_for("register"))

        if password != confirm:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return redirect(url_for("register"))

        # Vérifier si l'utilisateur existe déjà
        existing = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing:
            flash("Nom d'utilisateur ou email déjà utilisé.", "warning")
            return redirect(url_for("register"))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Inscription réussie, vous pouvez vous connecter.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# --------- Connexion ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form.get("username_or_email")
        password = request.form.get("password")

        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Bienvenue {user.username} !", "success")
            return redirect(url_for("catalogue"))
        else:
            flash("Identifiants incorrects.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


# --------- Déconnexion ----------
@app.route("/logout")
def logout():
    session.clear()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("login"))


# --------- Catalogue (films en base MySQL) ----------
@app.route("/catalogue")  # GET par défaut
def catalogue():
    if "user_id" not in session:
        flash("Vous devez être connecté pour accéder au catalogue.", "warning")
        return redirect(url_for("login"))

    movies = Movie.query.order_by(Movie.vote_average.desc()).all()
    return render_template("catalogue.html", movies=movies)


# --------- Recherche via API TMDb ----------
@app.route("/search", methods=["GET", "POST"])
def search():
    if "user_id" not in session:
        flash("Vous devez être connecté pour rechercher un film.", "warning")
        return redirect(url_for("login"))

    query = None
    results = []

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            try:
                results = search_movies_tmdb(query)
            except Exception as e:
                print("Erreur API TMDb :", e)
                flash("Erreur lors de l'appel à l'API TMDb.", "danger")

    return render_template(
        "search.html",
        query=query,
        results=results,
    )


# -------------------------------------------------
# Lancement
# -------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        # Ne recrée PAS les tables si tu les as faites à la main,
        # mais ça ne pose pas de problème si la structure est identique.
        db.create_all()
    app.run(debug=True)
