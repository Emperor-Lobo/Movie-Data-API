#  Movie Data API

API REST de gestion et d’exposition de données de films, construite avec **Python, Flask et SQL**.  
Ce projet implémente une mini-plateforme data complète allant de la base de données à l’API, en passant par l’ingestion des données.

Il permet de stocker, interroger et exploiter des données de films via une API utilisable pour de l’**analyse de données**, du **machine learning** ou des **applications web**.

---

##  Fonctionnalités

- Base de données SQL structurée (films, utilisateurs, etc.)
- Import automatique des données via script Python
- API REST Flask pour accéder aux données
- Interface web simple (templates HTML)
- Architecture prête pour l’analyse et le ML

---

##  Architecture

PostegreSql → Scripts Python → API Flask → Clients (Web, ML, Analytics)

---


Le projet suit une logique **Data Product** :  
les données sont modélisées, stockées, traitées et exposées via une API.

---

##  Stack technique

- Python
- Flask
- PostgreSQL
- HTML / CSS
- Scripts d’ingestion de données

---

##  Structure du projet

```bash
Movie-Data-API/
├── app.py # API Flask
├── import_movies.py # Script d’ingestion des données
├── requirements.txt # Dépendances Python
├── database.sql # Schéma PostgreSQL
├── movies.sql # Données de films
├── users.sql # Données utilisateurs
├── static/ # Fichiers CSS / assets
└── templates/ # Pages HTML

```
---

##  Base de données

Le projet utilise une base SQL contenant notamment :
- une table de films
- une table d’utilisateurs
- des tables de test et de validation

Les fichiers `.sql` permettent de recréer l’intégralité de la base.

---

## Import des données

Les données sont chargées dans PostgreSQL via le script :

```bash
python import_movies.py
```
Ce script lit les données et les insère dans la base SQL.

Lancer l’API

1- Installer les dépendances :

```bash
pip install -r requirements.txt
```

2- Créer la base PostgreSQL et importer le schéma :

```bash
psql -U postgres -d moviedb -f database.sql
```

3- Lancer le serveur Flask :

```bash
python app.py
```
