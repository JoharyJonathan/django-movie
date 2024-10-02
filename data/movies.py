import csv
import random
from datetime import datetime

# Fonction pour échapper les apostrophes simples dans les chaînes
def escape_single_quotes(value):
    return value.replace("'", "''")

# Fonction pour générer des entrées SQL à partir du fichier CSV
def generate_movie_sql(csv_file, num_entries=80):
    # Lire le fichier CSV
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))

        # Sélectionner aléatoirement 80 lignes
        selected_rows = random.sample(reader, num_entries)

        # Ouvrir un fichier SQL pour écrire les données
        with open("movies_insert.sql", "w", encoding='utf-8') as f:
            f.write("BEGIN;\n")
            for row in selected_rows:
                title = escape_single_quotes(row['title'])
                director = escape_single_quotes(row['director'])
                synopsys = escape_single_quotes(row['description'])  
                description = f"description of {escape_single_quotes(title)}"
                release_year = row['release_year']
                created_at = updated_at = datetime.now().isoformat()  # Date actuelle
                poster = f"photo de {escape_single_quotes(title)}"
                rating = random.randint(1, 5)  # Note entre 1 et 5

                # Créer la requête d'insertion SQL pour la table movies_movie
                sql = f"""INSERT INTO movies_movie (title, description, release_year, director, rating, created_at, updated_at, poster, synopsys) 
                VALUES ('{title}', '{description}', {release_year}, '{director}', {rating}, '{created_at}', '{updated_at}', '{poster}', '{synopsys}');\n"""
                
                f.write(sql)
            f.write("COMMIT;\n")

# Appel de la fonction avec le nom du fichier CSV
generate_movie_sql('netflix_titles.csv', 80)

print("Les données fictives ont été générées avec succès dans 'movies_insert.sql'.")