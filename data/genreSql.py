input_file = 'genres.txt'
output_sql = 'insert_movies_genre.sql'

with open(input_file, 'r') as infile, open(output_sql, 'w') as outfile:
    genres_set = set()  # Pour éviter les doublons

    # Écriture de la création de la table
    outfile.write("CREATE TABLE IF NOT EXISTS movies_genre (\n"
                  "    id SERIAL PRIMARY KEY,\n"
                  "    name VARCHAR(255) UNIQUE,\n"
                  "    description TEXT\n"
                  ");\n\n")

    for line in infile:
        # Séparer les genres sur chaque ligne
        genres = [genre.strip() for genre in line.split(',')]

        for genre in genres:
            if genre and genre not in genres_set:  # Assure-toi que le genre n'est pas vide
                genres_set.add(genre)
                # Échapper les apostrophes dans le genre et la description
                genre_escaped = genre.replace("'", "''")
                description = f"description of {genre_escaped}"
                
                # Créer la requête SQL d'insertion
                outfile.write(f"INSERT INTO movies_genre (name, description) "
                              f"VALUES ('{genre_escaped}', '{description}');\n")  # Ajoute un point-virgule

# Optionnel: Indique que le fichier SQL a été généré avec succès
print("Le fichier SQL a été généré avec succès.")