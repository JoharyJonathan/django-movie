import random
from datetime import datetime, timedelta

# Fonction pour générer une date de naissance aléatoire
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Plage de dates pour la génération aléatoire (par exemple, entre 1940 et 2000)
start_date = datetime(1940, 1, 1)
end_date = datetime(2000, 12, 31)

# Remplace 'actors.txt' par le chemin de ton fichier texte contenant les acteurs
input_file = 'actors.txt'
output_file = 'insert_movies_actor.sql'

# Ouverture du fichier texte pour lire les acteurs avec un encodage UTF-8
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        line = line.strip()
        if line.lower() == 'nan' or line == '':  # Ignorer les éléments nan
            continue
        
        # Séparer les noms des acteurs
        actors = [actor.strip() for actor in line.split(',')]
        
        for actor in actors:
            if actor:  # S'assurer que le nom de l'acteur n'est pas vide
                name_parts = actor.split(' ')
                if len(name_parts) >= 2:  # Vérifier que nous avons au moins un prénom et un nom
                    first_name = name_parts[0].replace("'", "''")  # Échapper l'apostrophe dans le prénom
                    last_name = name_parts[1].replace("'", "''")  # Échapper l'apostrophe dans le nom
                    date_of_birth = random_date(start_date, end_date).date()  # Date de naissance aléatoire
                    bio = f'bio of {first_name}'
                    
                    # Écrire la requête SQL d'insertion
                    outfile.write(f"INSERT INTO movies_actor (first_name, last_name, date_of_birth, bio) "
                                  f"VALUES ('{first_name}', '{last_name}', '{date_of_birth}', '{bio}');\n")